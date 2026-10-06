# 001 — acLabs lifecycle improvement

- Status: Proposed
- Date: 2026-10-06
- Related specification: [001 — acLabs lifecycle](../acLabs/001%20-%20Lifecycle.md)

## Context

The lifecycle phases are currently spread across image construction, devcontainer
hooks, the shell entrypoint, and Python startup services. Their execution order
does not fully match the boundaries defined in the lifecycle specification.

| Stage | Current ownership | Main issue |
| --- | --- | --- |
| Workspace preparation | Devcontainer hooks, entrypoint, Python controller | Alias setup has multiple invocation points; early access needs visible preparation status and pending runtime values |
| Lab preparation | Entrypoint and onboarding service | Image acquisition blocks editor startup, while onboarding runs asynchronously |
| Deployment | Controller, Make, containerlab | Deployment depends on preparation performed elsewhere |
| Readiness verification | Python controller | A stored `READY` can bypass fresh verification |

## Proposed improvements

1. **Separate environment bootstrap from lab startup.** Installing dependencies
   and editor extensions belongs to image construction. Starting the container
   engine and editor belongs to environment bootstrap. The four lifecycle stages
   describe preparing and operating a particular lab.

2. **Give each operation one owner.** Devcontainer hooks and entrypoints should
   invoke shared operations. Alias generation, workspace substitutions, and
   onboarding should each have one implementation and a defined invocation point.

3. **Support early access with visible preparation status.** Make the editor and
   progress terminal available while preparation continues. Give README
   credentials, access links, repository substitutions, and shell setup explicit
   completion conditions. Perform quick local substitutions as soon as their
   inputs are available; mark pending values clearly and refresh displayed content
   after updates. Optionally defer automatic README opening while still showing
   the progress terminal immediately.

4. **Move image acquisition into asynchronous lab preparation.** Image
   acquisition and CloudVision onboarding should proceed while the editor is
   available. Deployment must wait for all required preparation to succeed.

5. **Define phase prerequisites and outputs.** For example, lab preparation
   produces a verified image reference and usable startup configurations;
   deployment consumes them. Phase completion should be explicit rather than
   inferred from operations performed by another script.

6. **Define repeated-invocation behavior.** Workspace preparation should be safe
   to rerun. Token regeneration needs an explicit policy. Explicit readiness
   verification should collect fresh evidence rather than trust a stored `READY`.

7. **Treat cleanup as a separate operation.** The entrypoint currently prunes
   stopped containers on every invocation. Cleanup needs its own scope and trigger
   rather than being an implicit part of startup.

## Follow-up

Review these proposals before changing implementation. The lifecycle specification
should express intended behavior and ownership independently of current script
boundaries. Timer changes remain a separate decision after live testing.
