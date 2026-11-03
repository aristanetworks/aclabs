# 004 — Artifact manifest and creation-time file staging

- Status: Draft
- Date: 2026-11-03

## Context

Labs can require files that cannot be committed to their repository, such as
licensed software, SWIX packages, private VS Code extensions, or lab data. The
host has access to artifact storage, but a lab container and its users must
not receive direct access to that storage collection or its credentials.

The launcher must deliver only the selected lab's declared inputs into its
workspace. A manifest describes those inputs independently of storage layout and
the mechanism used to copy them. This also permits other deployment workflows to
consume the same manifest without depending on devcontainers.

This specification defines the intended contract. It does not describe an
already implemented launcher feature. MUST, MUST NOT, SHOULD, and MAY express
requirements within this draft.

## Decisions

1. Use `customizations.aristaLabs.artifactManifest` to select a lab artifact
   manifest.
2. The manifest declares required files, their workspace-relative destinations,
   and optional SHA-256 checksums. An optional `images` key is accepted as metadata
   for other consumers or future capabilities. The manifest contains no storage
   locations or credentials.
3. Trusted host orchestration resolves sources exclusively through operator-approved
   storage and applies authorization independently of repository declarations.
   Authorization applies to launcher access to storage, not to individual labs.
4. Stage files in the host-side workspace and deliver the prepared workspace before
   the container starts. Do not repeat staging on ordinary restart or attach.
5. Only regular-file delivery is in scope. Image acquisition, copying, import, and
   availability checks are possible future capabilities. The launcher does not
   install extensions, extract archives, or execute files through this feature.
6. A required file staging failure prevents successful environment creation and
   lab deployment.

## Scope and terminology

| Term | Meaning |
| --- | --- |
| Launcher | Trusted host-side orchestration responsible for creating the environment and staging artifacts. |
| Workspace root | The selected lab's effective `workspaceFolder` inside the container, not necessarily the repository root. |
| Artifact storage | Operator-approved storage reachable by the launcher, outside the lab's control. |
| Lab artifact | An input file required by the lab, distinct from logs or reports produced by a run. |
| Creation attempt | Preparation of a newly created environment, identified by launcher-owned state and container identity. |

The launcher MUST stage artifacts in a host-side workspace, then deliver the
prepared workspace into the container before it starts. The container MUST remain
stopped until workspace delivery and verification succeed. Copying artifacts into
an already running container is not supported. Artifact storage MUST NOT be
mounted into the container.

Copying is non-destructive to storage: the source file remains in place. The
manifest does not request a filesystem move.

## Devcontainer interface

```json
{
    "customizations": {
        "aristaLabs": {
            "artifactManifest": "artifacts.yml"
        }
    }
}
```

`artifactManifest` is an optional, nonempty string naming a file relative to the
selected lab workspace root. It is not relative to the devcontainer configuration
directory. For example, when the workspace is `/anta-psirt`, `artifacts.yml`
selects `/anta-psirt/artifacts.yml` in the prepared workspace content.

The launcher MUST resolve the reference against the selected lab content, not
against an arbitrary host working directory. It MUST read the corresponding file
from the trusted checkout or host-side workspace before container startup.
The manifest MUST already be present; it cannot itself be an externally fetched
artifact required to discover the initial requirements.

The reference MUST satisfy the relative-path rules below, remain within the lab
workspace, and resolve to a regular file without following symlinks. URLs,
absolute paths, environment expansion, shell expansion, and glob patterns are not
supported. The launcher MUST NOT execute the value or treat it as a command.

If the property is absent, this feature performs no artifact staging and MUST NOT
automatically discover `artifacts.yml`. If the property is present but invalid,
unreadable, or names a missing file, creation MUST fail.

The namespace is an acLabs launcher integration contract, not a built-in
devcontainer feature. The acLabs launcher MUST process it. Standard devcontainer
tools do not perform artifact staging from this property automatically.

## Manifest format

The manifest is a UTF-8 YAML document with a required `files` list and an optional
`images` list. No other top-level keys are supported. Use `files: []` when no files
are required. Omitted `images` and `images: []` are equivalent. The initial format
has no schema version field.

```yaml
files:
  - filename: my-extension-1.2.3.vsix
    path: my-extension-1.2.3.vsix

  - filename: sa178-SecurityAdvisory178_CVE-2026-73440.swix
    path: containerlab/assets/sa178-SecurityAdvisory178_CVE-2026-73440.swix
    sha256: "da9388362250db73fd8721e6889c0f90c8f548b25baee16e64621424200f24c6"
```

### File entries

| Field | Required | Meaning |
| --- | --- | --- |
| `filename` | Yes | Exact basename used to look up the source in approved artifact storage. |
| `path` | Yes | Destination file path relative to the lab workspace root, including the destination filename. |
| `sha256` | No | Expected SHA-256 of the file contents, expressed as exactly 64 hexadecimal characters. |

All field values MUST be strings. A supplied `sha256` MUST be nonempty and valid;
uppercase hexadecimal MAY be accepted and normalized to lowercase. A missing
checksum means no expected-content comparison is requested. YAML null is not an
alternative to omitting an optional field.

`filename` is a basename, not a host path or artifact URL. It MUST NOT contain `/`,
`\`, control characters, or be `.` or `..`. The destination filename MAY differ
from the storage filename. Matching is exact and case-sensitive.

Multiple destinations MAY request the same source filename. Any supplied hashes
for that source MUST agree. Destination paths MUST be unique; file/directory
conflicts such as `assets` and `assets/package.swix` MUST be rejected before copying.

Unknown top-level keys, unknown file-entry keys, duplicate mapping keys, multiple
YAML documents, executable/custom YAML tags, and YAML aliases MUST be rejected.
Parsing MUST use a safe, bounded loader and MUST NOT construct executable objects.
Future format extensions require an explicit contract update.

### Relative-path rules

Manifest references and destination paths use `/` separators. They MUST NOT:

- Be empty or absolute, or use a URI, Windows drive, or UNC form.
- Contain a `.` or `..` component, an empty component, a backslash, or control
  characters.
- End with `/` or designate the workspace root itself.
- Depend on variable substitution, tilde expansion, wildcard expansion, or a shell.

An implementation MUST validate resolved filesystem containment as well as these
lexical rules. A string prefix check is insufficient to establish containment.

### Optional image metadata

`images` MAY be omitted. When present, it MUST be a list of nonempty strings
identifying container images, for example:

```yaml
images:
  - arista/ceos:4.35.5M

files: []
```

The launcher MUST accept this metadata without resolving image references,
accessing registries or image storage, copying image archives, querying runtimes,
or importing images. A nonempty list MUST produce an informational notice that
image handling is outside the current scope, without failing file staging.
The launcher validates the list's structure, but does not verify image-reference
syntax, existence, or availability.

Successful staging MUST NOT imply that listed images are available. The `images`
key does not authorize storage or registry access and MUST NOT be interpreted as
a list of filenames. Image handling is described only as a possible future
capability below.

An image archive explicitly declared under `files` can still be copied as an
ordinary opaque file. Its contents are not inspected or imported, and it receives
no special image handling.

## Approved storage and access

### Storage configuration belongs to the host operator

The launcher MUST use storage configuration supplied through trusted host-side
configuration. The lab repository, manifest, devcontainer configuration, container
environment, and user-supplied `runArgs` MUST NOT add storage sources, change lookup
rules, grant access, or provide storage credentials for this feature.

The launcher MUST be authorized to read artifacts from the configured storage.
The operator establishes that authorization independently of repository
declarations. A manifest requests delivery; it does not grant storage access.
This storage-level authorization is required even though no per-lab artifact
authorization policy is applied.

Every storage source MUST be explicitly approved and configured by the operator.
Reachability or possession of valid credentials alone MUST NOT make a source
eligible. Its configuration and storage credentials MUST remain outside the lab's
control. The launcher MUST verify that resolved artifacts belong to an approved
source and MUST NOT substitute another source when the approved one is unavailable.

This specification does not prescribe a storage provider, backend type, protocol,
storage layout, or client implementation. Those choices belong to the deployment.
Regardless of implementation, sources must satisfy the source approval, isolation,
integrity, and failure requirements in this document. A manifest cannot enable or
select an otherwise unapproved source.

### Initial access model

All labs MAY receive any artifact available through the operator-approved storage
sources by listing its filename under `files`. The implementation has no
per-lab artifact allowlist, entitlement check, or deployment-identity policy.
A valid manifest entry is sufficient to request delivery from approved storage.

For example, any lab may request `my-extension-1.2.3.vsix` or the named SA178 SWIX
if those artifacts are available in approved storage. The launcher copies only
the files listed in that lab's selected manifest; unlisted artifacts are not
delivered.

The operator MUST therefore treat artifacts exposed through approved storage as
available to every lab using this launcher. Keeping storage credentials and direct
storage access outside the container limits the delivery mechanism; it does not
restrict which approved artifacts a lab may request.

Missing storage configuration, unavailable approved storage, and storage access
failures MUST fail closed. No separate per-lab policy is required for creation.
The launcher MUST NOT fall back to an unapproved source or acquisition mechanism.

### Source resolution

For each filename, the launcher MUST:

1. Restrict lookup to operator-approved storage sources and the filenames declared
   in the manifest.
2. Resolve the exact filename using operator-configured lookup rules. Do not use
   wildcard or case-insensitive matching, or search unapproved storage.
3. Require an unambiguous source. Multiple eligible matches MUST fail, even if
   their contents match. Manifest authors cannot select a storage location to
   resolve ambiguity; the operator must correct the lookup configuration.
4. Retrieve only the selected artifact's file contents. Do not interpret the source
   as a directory, executable instruction, or reference granting access to another
   resource. The delivered artifact MUST be a regular file.
5. Preserve the approved source and artifact identity throughout retrieval. Source
   aliases, redirection, or concurrent changes MUST NOT escape approved storage or
   replace the bytes selected for verification and delivery.

Lab workloads MUST NOT be able to modify approved storage or its lookup and source
configuration through this mechanism. The storage integration MUST enforce the
same access boundary regardless of how an artifact is represented internally.

The launcher MUST NOT mount the artifact collection into the lab, copy unlisted
artifacts, or pass storage credentials to the container. It MUST transfer only
files explicitly listed under `files` in the selected manifest.

## Creation lifecycle

The required sequence is:

1. Resolve the selected lab, effective workspace root, manifest reference, and
   trusted storage configuration.
2. Read and validate the complete manifest, check destination conflicts and
   launcher resource limits, and report nonempty image metadata as outside scope.
3. Resolve every required source within approved storage. Read sources into
   launcher-owned temporary staging, enforce size limits, and verify supplied
   checksums.
4. Prepare the host-side workspace and copy verified file bytes to their declared
   relative destinations with the containment, collision, ownership, and permission
   rules below.
5. Deliver the prepared workspace into the stopped container and verify the
   delivered artifact bytes before startup. Host-side paths MUST map to the
   declared destinations beneath the effective container workspace root.
6. Record successful staging in host-controlled state.
7. Start the container and allow initialization hooks and lab preparation to
   proceed.

The implementation MAY reorder independent preparation operations, but MUST NOT
start the container or execute repository-provided hooks before staging and
workspace delivery succeed. The container entrypoint and `postCreateCommand` run
only after that boundary. Copying artifacts after the container has started
does not satisfy this ordering.

During staging and workspace delivery, users and untrusted workloads MUST NOT be
able to mutate the destination workspace. Editor access begins only after the
container starts. Artifact staging is a local workspace preparation operation; it
SHOULD NOT wait for unrelated external lab services or device readiness.

Creation-time staging is distinct from extension installation or lab provisioning.
For example, a later initialization step may install the copied VSIX as the
container user, and Containerlab may use a staged SWIX during device provisioning.
The staging service MUST NOT infer such actions from file extensions.

### Restart, retry, and recreation

- Restarting or attaching to the same container MUST NOT recopy, rehash, repair,
  or overwrite workspace artifacts through this feature. User edits remain intact.
- Editing a manifest or changing artifact storage MUST NOT refresh an existing
  environment automatically.
- A new container creation or rebuild starts a new staging attempt. If it reuses
  an existing workspace, the same destination collision rules apply; recreation
  does not authorize overwriting previous files.
- Retry of a failed creation attempt requires an explicit launcher action. The
  launcher MUST use its own state to distinguish a completed stage from an
  incomplete one, rather than trusting a marker file writable by the lab.
- A completed stage in the same creation attempt is not executed again. A failed
  attempt MUST NOT be marked completed or allowed to deploy.

## Copying, integrity, and destination safety

### Content and integrity

The launcher MUST copy bytes without transforming contents, extracting archives,
interpreting file types, or executing commands. Source files MUST remain unchanged.

When `sha256` is supplied, the launcher MUST compare the digest of the staged
source bytes with the expected digest before publishing the destination file.
A mismatch MUST fail creation; there is no automatic bypass. The transferred
destination bytes MUST also be verified against that same expected digest before
staging succeeds. The implementation MUST copy from the verified snapshot rather
than retrieve a potentially changed source again.

When `sha256` is absent, the launcher MUST still ensure the destination bytes match
the staged source snapshot. It MAY compute an internal digest for that transfer
check, but MUST NOT describe the result as verification against an expected
artifact identity. No hash is silently written back into the manifest.

A checksum establishes correspondence with the reviewed declaration, not
publisher authenticity, authorization, or safety of executable contents.

### Workspace containment and collisions

Every destination MUST stay beneath the effective workspace root. Reject any
symlink in the destination path, including an existing final symlink. Treat the
resolved workspace root as an explicit boundary rather than following paths into
other container mounts or the container filesystem. Destinations under nested
mounts MUST be rejected unless the launcher explicitly establishes them as part
of its trusted workspace delivery boundary.

Use race-resistant operations for parent directory creation and final placement.
Untrusted destination paths MUST NOT be interpolated into shell commands.

Existing regular parent directories MAY be used. An existing destination file or
any incompatible parent MUST cause failure, even when the existing file has the
expected hash. There is no implicit overwrite, merge, or delete behavior.
The manifest MUST NOT overwrite itself or other checked-out files.

Missing parent directories MAY be created beneath the workspace. New files MUST
be owned by the configured workspace user and have mode `0600`; newly created
directories MUST have mode `0700`. Existing parent directory permissions MUST NOT
be broadened. Do not preserve source ownership, ACLs, extended attributes, special
permission bits, or executable permissions. A later trusted setup step may apply
permissions required by the lab.

### Failure and cleanup

The launcher MUST validate all declarations and available destinations before
publishing files. It SHOULD prepare and verify all source snapshots before making
any destination file visible. Individual files MUST be published only after a
complete transfer, using atomic final placement within the destination filesystem.
Destination checks MUST be repeated safely at publication time.

This specification does not require an atomic transaction across all files. If
publication fails partway through, some completed destinations may remain, but the
environment MUST remain failed and MUST NOT proceed to dependent initialization.

The launcher MUST remove private temporary copies on success and failure, and
recover abandoned temporary staging on later launcher startup. Temporary storage
MUST be inaccessible to lab users and other unprivileged host users. Cleanup MUST
NOT delete source artifacts or pre-existing workspace files. Removal of completed
destinations during recovery requires launcher-owned records and a protected
workspace; otherwise use a fresh workspace or explicit operator remediation.

## Resource limits and observability

Trusted launcher configuration MUST bound manifest size, list entry counts,
individual file size, aggregate transfer size, and operation duration. Implementations MUST
document their defaults and enforce limits while reading, not only from initial
filesystem metadata. The manifest cannot raise these limits.

Progress and failure reports MUST distinguish at least:

- Invalid or missing manifest and unsupported requirements.
- Nonempty image metadata accepted without image handling.
- Storage access failure, unavailable storage, missing source, and ambiguous lookup.
- Invalid or escaping paths, unsupported file types, and destination collisions.
- Resource limits, transfer failures, and checksum mismatches.
- Successful completion of artifact staging for the creation attempt.

Logs SHOULD identify the manifest entry and destination relative to the workspace.
They MUST NOT expose credentials, artifact contents, unrestricted storage listings,
or private absolute source paths to lab users. Operator-only diagnostics
MAY include additional source information under the host's normal access controls.

Staging completion means the required files have been delivered. It MUST NOT be
reported as runtime image availability, extension installation success, device
deployment success, or whole-lab readiness. File staging failures MUST produce a
nonzero launcher outcome and a visible failed creation state. Nonempty image
metadata alone does not fail staging and MUST be reported as outside scope.

## Acceptance criteria

An implementation must demonstrate the following behaviors:

1. With no `artifactManifest`, existing launches perform no new staging or implicit
   manifest discovery.
2. A selected manifest copies only listed files from approved storage to the
   declared workspace-relative paths, including creating required parent directories.
3. A supplied correct checksum succeeds; an incorrect or malformed checksum fails.
   Files without a checksum are supported, with transfer correctness checked.
4. Unlisted source files are not delivered. Storage credentials and direct access
   to artifact storage are not exposed to the lab through this mechanism.
5. A manifest cannot introduce storage sources, URLs, credentials, shell operations,
   or access grants. Unsupported fields fail rather than being ignored.
6. Missing artifacts, storage access failures, ambiguous matches, and unavailable
   approved storage fail before dependent initialization; none triggers an
   unapproved fallback.
7. Absolute paths, traversal, symlink escapes, source references that bypass
   storage boundaries, destination conflicts, existing final files, and unsafe nested
   mounts are rejected.
8. Source and destination mutation attempts cannot redirect reads or writes outside
   their approved boundaries or replace verified bytes undetected.
9. Duplicate YAML keys, unsupported YAML constructs, incorrectly typed image
   metadata, and oversized inputs fail within configured limits. Omitted and empty
   `images` are accepted; a nonempty list of nonempty strings is accepted with an
   informational notice and no image-related operations.
10. Restart and attach do not repeat staging. Retry, rebuild, reused workspaces,
    and partial failure follow the defined state and collision rules.
11. A staging error leaves no partially written final file, blocks consumers,
    cleans private temporary copies, and preserves original storage contents.
12. Delivered files have the specified ownership and permissions; extensions and
    archives are neither installed nor executed automatically.
13. Logs provide actionable staging status without disclosing storage credentials,
    file contents, or private storage layout, and do not claim whole-lab readiness.
14. Image metadata does not trigger storage lookup, registry access, archive
    copying, runtime queries, or imports, and does not establish image availability.
15. Artifacts are staged in the host-side workspace and delivered into the stopped
    container before startup. A staging or workspace delivery failure prevents
    container startup, entrypoint execution, and repository-provided hooks.
16. Different labs can request the same or any other artifact in approved storage
    without a separate per-lab entitlement or access policy. Only manifest entries
    and the configured source, validation, and resource limits govern delivery.

## Possible future capability: per-lab artifact access

A future revision could introduce artifact entitlements or per-lab access rules
if deployments require different labs to receive different subsets of storage.
Such a policy is not required or implemented by the initial access model.

## Possible future capability: image handling

A future revision could use `images` to request image acquisition, archive
delivery, runtime import, or availability checks. None of these operations is part
of the current implementation contract, and this document defines no enablement
flag, image catalog, archive naming scheme, or runtime selection interface.

Such a revision would need to define approved sources, the applicable access model,
image identity and integrity, and the target container runtime. Images imported
on the host are not necessarily available to a separate Docker-in-Docker daemon.
The revision would also need to reconcile image delivery and import with the
pre-start file staging lifecycle; importing into an inner daemon may require a
later preparation phase.

## Relationship to other specifications

Artifact delivery is one operation within workspace preparation under
[001 — acLabs lifecycle](001%20-%20Lifecycle.md), and complements
[002 — Environment setup](002%20-%20Environment%20Setup.md). A future `arlab`
integration SHOULD preserve the service boundaries described in
[0001 — arlab CLI and architecture](../arlab/0001%20-%20CLI%20and%20architecture.md):
configuration resolution, manifest validation, source access, copying, and progress
publication must not depend on parsing human-readable CLI output.

The manifest format follows the separately proposed advisory-lab ADR-0004
(artifact storage), ADR-0005 (artifact metadata), and ADR-0017 (artifact naming).
Their copies in this checkout's temporary `adr/` directory are review context,
not a permanent dependency of this document. Advisory CI and acLabs can consume
the same declarations with independent orchestration and storage implementations.
The advisory format requires an `images` list. This acLabs consumer makes that key
optional and accepts its contents only as metadata; image handling is outside the
current scope.

The advisory storage proposal also describes per-lab artifact access restrictions.
This acLabs specification deliberately uses a simpler initial model: every lab
may request any artifact in approved storage. It does not adopt those per-lab
restrictions.

The tool-specific namespace uses the devcontainer specification's
[customizations mechanism](https://containers.dev/implementors/json_reference/#tool-specific-properties).
It does not change the standard semantics of `runArgs`, mounts, or lifecycle hooks.
