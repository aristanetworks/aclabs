#!/usr/bin/env bash
#
# lab-deploy.sh — deploy (or destroy) a containerlab topology with a
# bounded retry, a log the user can read, and a status file init_lab.py
# can watch.
#
# Bundled by the techlib container image as /bin/lab-deploy.sh; the techlib
# labs' Makefiles run it from `make start` / `make stop` (falling back to a
# bare `containerlab` call when the image predates it). The lab-base
# entrypoint runs `make start` at container boot, so a lab that fails to come
# up is retried before the user ever sees it.
#
#     lab-deploy.sh deploy  <topology.clab.yml>
#     lab-deploy.sh destroy <topology.clab.yml>
#
# Why a wrapper:
#   * `containerlab deploy` can stop part-way (one wave of nodes created, the
#     rest never scheduled) and its output only went to the container's
#     stdout — nobody could read why. Seen in the field on a 43-node lab:
#     32 containers created, 11 nodes reported "timeout" for 20 minutes.
#   * Two independent signals decide success: containerlab's exit code, and
#     the set of running containers reported by `containerlab inspect`
#     compared with the nodes in the topology. Either one failing means the
#     deploy is retried — once. A deterministic failure (missing cEOS image,
#     bad topology) surfaces after that one retry instead of looping.
#   * Every attempt is bounded (`timeout`), so a deploy that hangs on a
#     wedged runtime becomes a logged, retried failure instead of a boot
#     that never finishes.
#   * One lab, one deploy at a time: a lock under .lab/ refuses a second
#     `make start`/`make stop` while one is running, instead of two
#     `--reconfigure`s tearing down each other's half-built lab.
#
# State, under <lab root>/.lab/ (the lab root is the directory that holds
# assets/ and LAB-READY.md; for the legacy layout the topology sits one level
# down in clab/):
#   deploy.log       this run's full containerlab output (the three previous
#                    runs are kept as deploy.log.1 … .3)
#   attempt.N.log    each attempt's own containerlab output
#   deploy.status    key=value lines, rewritten atomically at every step:
#                      action=deploy|destroy
#                      state=deploying|retrying|ok|failed|destroying|destroyed
#                      pid=<this script's pid — dead pid + deploying/retrying
#                           means it was killed before it could finish>
#                      attempt=N attempts=M expected=N running=N
#                      missing=<comma-separated container names>
#                      error=<the reason, when state=failed>
#                      topology=<path> lab=<name> log=<path>
#                      started=<epoch> updated=<epoch>
#   lock             flock(1) lock held for the duration of a run
#
# Tunables (environment): LAB_DEPLOY_ATTEMPTS (2), LAB_DEPLOY_MAX_WORKERS (10),
# LAB_DEPLOY_TIMEOUT (5m, containerlab's own per-request timeout),
# LAB_DEPLOY_ATTEMPT_TIMEOUT (15m, the bound on one whole deploy attempt),
# LAB_DEPLOY_LOG_LEVEL (debug).

set -u

usage() {
    echo "usage: $0 deploy|destroy <topology.clab.yml>" >&2
    exit 2
}

[ $# -eq 2 ] || usage
ACTION="$1"
case "$ACTION" in deploy|destroy) ;; *) usage ;; esac
TOPOLOGY="$(readlink -f "$2" 2>/dev/null || echo "$2")"
[ -f "$TOPOLOGY" ] || { echo "lab-deploy: topology not found: $TOPOLOGY" >&2; exit 2; }

ATTEMPTS="${LAB_DEPLOY_ATTEMPTS:-2}"
MAX_WORKERS="${LAB_DEPLOY_MAX_WORKERS:-10}"
CLAB_TIMEOUT="${LAB_DEPLOY_TIMEOUT:-5m}"
ATTEMPT_TIMEOUT="${LAB_DEPLOY_ATTEMPT_TIMEOUT:-15m}"
LOG_LEVEL="${LAB_DEPLOY_LOG_LEVEL:-debug}"

# Lab root: the topology's directory, or its parent when the topology lives
# under clab/ (legacy layout). Same rule as init_lab.py's find_topology().
TOPO_DIR="$(dirname "$TOPOLOGY")"
if [ "$(basename "$TOPO_DIR")" = "clab" ] && [ -d "$TOPO_DIR/../assets" ]; then
    LAB_ROOT="$(readlink -f "$TOPO_DIR/..")"
else
    LAB_ROOT="$TOPO_DIR"
fi
STATE_DIR="$LAB_ROOT/.lab"
LOG="$STATE_DIR/deploy.log"
STATUS="$STATE_DIR/deploy.status"
LOCK="$STATE_DIR/lock"

# The state dir must be writable by whoever runs this (avd at boot and at the
# keyboard). Fail loud rather than deploy with no log and no status file.
if ! mkdir -p "$STATE_DIR" 2>/dev/null || [ ! -w "$STATE_DIR" ]; then
    echo "lab-deploy: cannot write $STATE_DIR (owner: $(stat -c %U "$STATE_DIR" 2>/dev/null || echo unknown))" >&2
    exit 2
fi

# ── topology facts (python3 + pyyaml are in lab-base; init_lab.py needs them too)
# Prints: lab name, then one expected container name per line, using
# containerlab's naming rule for the topology's `prefix:` key — the same rule
# init_lab.py's LabConfig.container_name() applies.
topology_facts() {
    python3 - "$TOPOLOGY" <<'PY'
import sys, yaml
with open(sys.argv[1]) as f:
    topo = yaml.safe_load(f) or {}
name = str(topo.get("name", "unnamed-lab"))
prefix = topo.get("prefix")
nodes = (topo.get("topology") or {}).get("nodes") or {}
print(name)
for node in nodes:
    if prefix is None:
        print(f"clab-{name}-{node}")
    elif prefix == "":
        print(node)
    elif prefix == "__lab-name":
        print(f"{name}-{node}")
    else:
        print(f"{prefix}-{name}-{node}")
PY
}

if ! FACTS="$(topology_facts)"; then
    echo "lab-deploy: could not read $TOPOLOGY (python3 with pyyaml is required)" >&2
    exit 2
fi
LAB_NAME="$(printf '%s\n' "$FACTS" | head -n 1)"
EXPECTED="$(printf '%s\n' "$FACTS" | tail -n +2 | sort)"
EXPECTED_COUNT="$(printf '%s\n' "$EXPECTED" | grep -c .)"

STARTED="$(date +%s)"
ATTEMPT=0
ATTEMPT_LOG=""
RUNNING_COUNT=0
MISSING=""
ERROR=""

# Rewrite the status file atomically: readers (init_lab.py, a curious user)
# never see a half-written file.
write_status() {
    local state="$1"
    local tmp="$STATUS.tmp.$$"
    {
        echo "action=$ACTION"
        echo "state=$state"
        echo "pid=$$"
        echo "attempt=$ATTEMPT"
        echo "attempts=$ATTEMPTS"
        echo "expected=$EXPECTED_COUNT"
        echo "running=$RUNNING_COUNT"
        echo "missing=$MISSING"
        echo "error=$ERROR"
        echo "topology=$TOPOLOGY"
        echo "lab=$LAB_NAME"
        echo "log=$LOG"
        echo "started=$STARTED"
        echo "updated=$(date +%s)"
    } > "$tmp" && mv -f "$tmp" "$STATUS"
}

log_line() {
    echo "[lab-deploy $(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG"
}

# One run per lab at a time. The boot-time `make start` and a user's
# `make start`/`make stop` must never overlap: two `--reconfigure`s would
# destroy each other's half-built lab and the retry logic would ping-pong.
exec 9>"$LOCK"
if ! flock -n 9; then
    other="$(sed -n 's/^pid=//p' "$STATUS" 2>/dev/null)"
    echo "lab-deploy: another lab-deploy is running for $LAB_NAME${other:+ (pid $other)}; wait for it to finish (see $STATUS)" >&2
    exit 3
fi

# Killed mid-run (Ctrl-C, SIGTERM, the terminal going away): say so in the
# status file and the log rather than leaving state=deploying forever.
on_signal() {
    trap - INT TERM HUP
    ERROR="interrupted by signal before the $ACTION finished"
    log_line "$ERROR"
    write_status failed
    exit 130
}
trap on_signal INT TERM HUP

# The reason an attempt failed, for the status file and for init_lab.py's
# failure panel: containerlab's own error lines first (`ERRO[...]`,
# `level=error`, a leading `Error:`, a Go panic), and only if there is none a
# looser match. Read from this attempt's own capture, never the shared log,
# so a line from an earlier attempt can never be reported as this one's.
last_error_line() {
    local line
    line="$(grep -aE 'ERRO\[|level=error|^Error: |panic:' "$ATTEMPT_LOG" | tail -n 1)"
    [ -n "$line" ] || line="$(grep -aiE 'error|fail' "$ATTEMPT_LOG" | grep -av '^\[lab-deploy' | tail -n 1)"
    printf '%s' "$line" | cut -c1-300
}

# Ask containerlab which of the expected containers are running. Sets
# RUNNING_COUNT and MISSING (comma-separated container names, in sorted
# order). `inspect --format json` returns {"<lab>": [ {name, state, ...} ]};
# an absent lab yields {} or an empty array; an inspect failure counts as
# "nothing running", which errs toward a retry.
verify_running() {
    local json running
    json="$(sudo containerlab inspect --topo "$TOPOLOGY" --format json 2>>"$LOG")" || json="{}"
    running="$(printf '%s' "$json" | python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
except Exception:
    data = {}
items = []
if isinstance(data, dict):
    for v in data.values():
        if isinstance(v, list):
            items.extend(v)
elif isinstance(data, list):
    items = data
for c in items:
    if isinstance(c, dict) and c.get("state") == "running" and c.get("name"):
        print(c["name"])
' | sort)"
    RUNNING_COUNT="$(printf '%s\n' "$running" | grep -c .)"
    MISSING="$(comm -23 <(printf '%s\n' "$EXPECTED") <(printf '%s\n' "$running") | grep . | paste -sd, -)"
}

# One deploy attempt, bounded. `--reconfigure` destroys whatever a previous
# attempt left before it deploys, so a retry needs no separate destroy.
deploy_once() {
    ATTEMPT=$((ATTEMPT + 1))
    write_status "$([ "$ATTEMPT" -gt 1 ] && echo retrying || echo deploying)"
    log_line "deploy attempt $ATTEMPT of $ATTEMPTS: $LAB_NAME ($EXPECTED_COUNT nodes) from $TOPOLOGY (bound ${ATTEMPT_TIMEOUT})"
    ATTEMPT_LOG="$STATE_DIR/attempt.$ATTEMPT.log"
    timeout --foreground -k 30s "$ATTEMPT_TIMEOUT" \
        sudo containerlab deploy --log-level "$LOG_LEVEL" --topo "$TOPOLOGY" \
            --max-workers "$MAX_WORKERS" --timeout "$CLAB_TIMEOUT" --reconfigure 2>&1 | tee "$ATTEMPT_LOG" | tee -a "$LOG"
    local rc="${PIPESTATUS[0]}"
    verify_running
    log_line "attempt $ATTEMPT: containerlab exit $rc, running $RUNNING_COUNT of $EXPECTED_COUNT${MISSING:+, missing: $MISSING}"
    if [ "$rc" -eq 0 ] && [ -z "$MISSING" ]; then
        ERROR=""
        return 0
    fi
    if [ "$rc" -eq 124 ]; then
        ERROR="deploy attempt $ATTEMPT exceeded ${ATTEMPT_TIMEOUT} and was killed (${RUNNING_COUNT}/${EXPECTED_COUNT} nodes running)"
    else
        ERROR="$(last_error_line)"
        [ -n "$ERROR" ] || ERROR="containerlab exit $rc with ${RUNNING_COUNT}/${EXPECTED_COUNT} nodes running"
    fi
    return 1
}

destroy_once() {
    log_line "destroy: $LAB_NAME from $TOPOLOGY"
    ATTEMPT_LOG="$STATE_DIR/destroy.log"
    timeout --foreground -k 30s "$ATTEMPT_TIMEOUT" \
        sudo containerlab destroy --log-level "$LOG_LEVEL" --topo "$TOPOLOGY" --cleanup 2>&1 | tee "$ATTEMPT_LOG" | tee -a "$LOG"
    return "${PIPESTATUS[0]}"
}

# Keep the last three runs' logs; start this run fresh.
rotate_logs() {
    local i
    for i in 3 2 1; do
        [ -f "$LOG.$i" ] && mv -f "$LOG.$i" "$LOG.$((i + 1))"
    done
    rm -f "$LOG.4"
    [ -f "$LOG" ] && mv -f "$LOG" "$LOG.1"
    : > "$LOG"
    rm -f "$STATE_DIR"/attempt.*.log "$STATE_DIR/destroy.log"
}

case "$ACTION" in
deploy)
    rotate_logs
    while :; do
        if deploy_once; then
            write_status ok
            log_line "lab $LAB_NAME is deployed: $RUNNING_COUNT of $EXPECTED_COUNT nodes running (attempt $ATTEMPT)"
            exit 0
        fi
        if [ "$ATTEMPT" -ge "$ATTEMPTS" ]; then
            write_status failed
            log_line "lab $LAB_NAME FAILED to deploy after $ATTEMPT attempt(s): $ERROR"
            echo "lab-deploy: see $LOG" >&2
            exit 1
        fi
        log_line "attempt $ATTEMPT failed: $ERROR — retrying"
    done
    ;;
destroy)
    rotate_logs
    write_status destroying
    rc=0
    destroy_once || rc=$?
    verify_running
    if [ "$rc" -eq 0 ]; then
        ERROR=""
        write_status destroyed
        log_line "lab $LAB_NAME destroyed ($RUNNING_COUNT of $EXPECTED_COUNT nodes still running)"
        exit 0
    fi
    if [ "$rc" -eq 124 ]; then
        ERROR="destroy exceeded ${ATTEMPT_TIMEOUT} and was killed (${RUNNING_COUNT}/${EXPECTED_COUNT} nodes still running)"
    else
        ERROR="$(last_error_line)"
        [ -n "$ERROR" ] || ERROR="containerlab destroy exit $rc (${RUNNING_COUNT}/${EXPECTED_COUNT} nodes still running)"
    fi
    write_status failed
    log_line "lab $LAB_NAME destroy FAILED: $ERROR"
    echo "lab-deploy: see $LOG" >&2
    exit 1
    ;;
esac
