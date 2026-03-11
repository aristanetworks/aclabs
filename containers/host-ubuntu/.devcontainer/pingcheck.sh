#!/bin/bash

# ============================================================
#  ping_monitor.sh — Network Host Ping Monitor
#  Usage: ./ping_monitor.sh
#  Edit the HOSTS array below to match your lab environment.
# ============================================================

# --- CONFIGURATION ----------------------------------------
HOSTS_FILE="${1:-hosts.txt}"   # Default: hosts.txt, or pass a path as $1
INTERVAL=2                     # Seconds between ping rounds
PING_TIMEOUT=1                 # Seconds to wait per ping before declaring failure

# --- LOAD HOSTS -------------------------------------------
if [[ ! -f "$HOSTS_FILE" ]]; then
    echo "Error: hosts file '$HOSTS_FILE' not found."
    echo "Usage: $0 [hosts_file]"
    echo ""
    echo "  hosts file format — one host per line, # for comments:"
    echo "    192.168.1.10"
    echo "    192.168.1.11   # optional inline comment"
    echo ""
    exit 1
fi

# Read file: strip blank lines and comments
mapfile -t HOSTS < <(grep -v '^\s*#' "$HOSTS_FILE" | grep -v '^\s*$' | awk '{print $1}')

if [[ ${#HOSTS[@]} -eq 0 ]]; then
    echo "Error: no hosts found in '$HOSTS_FILE'."
    exit 1
fi

# --- COLORS -----------------------------------------------
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
DIM='\033[2m'
RESET='\033[0m'

# --- STATE ------------------------------------------------
declare -A success_count
declare -A fail_count
declare -A consecutive_fail

for host in "${HOSTS[@]}"; do
    success_count["$host"]=0
    fail_count["$host"]=0
    consecutive_fail["$host"]=0
done

# --- TEMP DIR for parallel ping results -------------------
PING_TMP=$(mktemp -d)
trap "rm -rf '$PING_TMP'; echo ''; echo 'Monitor stopped.'; exit 0" EXIT INT TERM

# --- FUNCTIONS --------------------------------------------

ping_host() {
    local host="$1"
    if ping -c 1 -W "$PING_TIMEOUT" "$host" > /dev/null 2>&1; then
        echo "SUCCESS" > "$PING_TMP/$host"
    else
        echo "FAIL" > "$PING_TMP/$host"
    fi
}

collect_and_display() {
    # Update state from temp results
    for host in "${HOSTS[@]}"; do
        local result_file="$PING_TMP/$host"
        local status="FAIL"
        [[ -f "$result_file" ]] && status=$(< "$result_file")

        if [[ "$status" == "SUCCESS" ]]; then
            success_count["$host"]=$(( success_count["$host"] + 1 ))
            consecutive_fail["$host"]=0
        else
            fail_count["$host"]=$(( fail_count["$host"] + 1 ))
            consecutive_fail["$host"]=$(( consecutive_fail["$host"] + 1 ))
        fi
    done

    # --- Draw the display ---
    clear

    local timestamp
    timestamp=$(date '+%Y-%m-%d  %H:%M:%S')

    echo -e "${BOLD}${CYAN}"
    echo "  ┌─────────────────────────────────────────────────────────────┐"
    printf "  │   🖧  Network Ping Monitor       %s   │\n" "$timestamp"
    echo "  └─────────────────────────────────────────────────────────────┘"
    echo -e "${RESET}"

    # Header row
    printf "  ${BOLD}%-24s %-12s %-16s %s${RESET}\n" \
        "HOST" "STATUS" "OK / FAIL" "CONSECUTIVE FAILS"
    echo -e "  ${DIM}────────────────────────────────────────────────────────────────${RESET}"

    for host in "${HOSTS[@]}"; do
        local result_file="$PING_TMP/$host"
        local status="FAIL"
        [[ -f "$result_file" ]] && status=$(< "$result_file")

        local ok="${success_count[$host]}"
        local fail="${fail_count[$host]}"
        local consec="${consecutive_fail[$host]}"
        local ratio="${ok} / ${fail}"

        # Print host name
        printf "  %-24s" "$host"

        # Print colored status (no printf width — ANSI breaks alignment)
        if [[ "$status" == "SUCCESS" ]]; then
            printf "${GREEN}%-12s${RESET}" "✔  SUCCESS"
        else
            printf "${RED}%-12s${RESET}" "✘  FAIL"
        fi

        # Print ratio
        printf "  %-16s" "$ratio"

        # Print consecutive fail counter only if failing
        if [[ "$consec" -gt 0 ]]; then
            printf "${RED}[%d in a row]${RESET}" "$consec"
        fi

        echo ""
    done

    echo ""
    echo -e "  ${DIM}Polling every ${INTERVAL}s  ·  Ping timeout ${PING_TIMEOUT}s  ·  Ctrl+C to exit${RESET}"
    echo ""
}

# --- MAIN LOOP --------------------------------------------
echo -e "${BOLD}${CYAN}  Starting ping monitor...${RESET}"
sleep 0.5

while true; do
    # Fire off all pings in parallel
    for host in "${HOSTS[@]}"; do
        ping_host "$host" &
    done

    # Wait for all pings to return
    wait

    # Collect results and redraw screen
    collect_and_display

    sleep "$INTERVAL"
done
