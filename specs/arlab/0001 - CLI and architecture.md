# 0001 — arlab CLI and architecture

- Status: Draft
- Date: 2026-10-06

## Context

`arlab` will provide reusable CLI operations for Arista lab environments. Its
initial integration is acLabs, starting with invocation from the environment
entrypoint and expanding to other build and runtime phases.

The existing startup code duplicates authentication and historically coordinated
Python scripts through subprocesses and log parsing. A shared package should
provide clear service boundaries and a CLI that can move to a dedicated repository.

The environment behavior is specified separately in
[001 — acLabs lifecycle](../acLabs/001%20-%20Lifecycle.md).

## Decisions

1. The repository/distribution, Python package, and executable name are `arlab`.
   acLabs-specific behavior MAY be implemented through adapters.

2. The CLI MUST parse configuration and invocation options, call Python services
   directly, render results, and return an exit code. Internal coordination MUST
   NOT depend on executing another Python CLI or parsing human-readable logs.
   External programs such as containerlab and Git MAY be run as subprocesses.

3. Configuration MUST be resolved and validated once per invocation and passed
   explicitly to services. Services MUST NOT independently read the same
   environment variables or capture credentials in module-level constants.

4. A shared CloudVision client MUST own authentication, HTTP sessions, certificate
   policy, API requests, and response parsing. Onboarding and verification within
   one invocation MUST reuse the client. Authentication recovery MUST respect the
   calling operation's deadline.

5. Orchestration, workspace updates, onboarding, topology access, deployment,
   device checks, and progress publication MUST have separate responsibilities.
   Services MUST be usable and testable independently of the CLI and terminal UI.

6. Progress MUST be published explicitly through structured state or events.
   Completion of an individual command MUST be distinguishable from readiness of
   an entire lab.

## Proposed commands

These command names are proposals for review.

| Command | Responsibility |
| --- | --- |
| `arlab future knob` | to-be-defined |

## Compatibility

Existing environment inputs and README placeholders retain their names during
migration. The current `/bin/lab_start_controller.py` and `/bin/cv_onboard.py`
commands may remain as thin compatibility entry points.

The existing observer's state-file fields (`status`, `message`, `updated_at`) and
startup log remain compatible until their replacement is reviewed. Package
installation should be independent of a particular container image layout.
