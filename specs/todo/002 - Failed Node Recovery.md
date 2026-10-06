# 002 — Failed node recovery

- Status: Proposed
- Date: 2026-10-06
- Related specification: [001 — acLabs lifecycle](../acLabs/001%20-%20Lifecycle.md)

## Context

A lab may deploy successfully while an individual node fails readiness checks.
During CVP lab testing, `l03` responded to ping and console access but refused SSH.
Its management namespace had no TCP listeners, EOS startup remained incomplete,
and rsyslog repeatedly exited. The underlying cause was not established.

The current startup failure leaves users without a supported way to recover only
the failed node while keeping healthy devices running.

## Task

Implement a topology-aware recovery operation for failed nodes:

1. Capture the failed readiness check and relevant container, service, and startup
   diagnostics before recovery changes or removes evidence.
2. Define a targeted restart/redeployment strategy that preserves healthy nodes,
   topology connections, management addresses, and required onboarding data.
   Make configuration preservation or reset behavior explicit to the user.
3. Support an explicit user-triggered recovery. Review automatic recovery as a
   separate policy, with bounded attempts and clear failure reporting.
4. Recheck node readiness and the applicable lab readiness conditions after
   recovery; a successful restart alone must not produce `READY`. Do not trust
   readiness evidence from before recovery.
5. Verify recovery of one failed node without restarting healthy nodes, and verify
   that an unrecoverable node leaves the lab failed with actionable diagnostics.

## Follow-up

Review the recovery policy and implementation approach before implementation.
Do not assume the observed failure is caused by Containerlab. Changes to existing
startup/readiness timers remain a separate decision.
