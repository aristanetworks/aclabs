# 004 — Artifact manifest and creation-time file staging

- Status: Draft
- Date: 2026-11-03

## Context

Labs require external files such as licensed software, SWIX packages, private
extensions, and lab data. A manifest lets trusted host orchestration deliver the
selected files without exposing artifact storage or its credentials to the lab.
This draft defines intended behavior, not an implemented feature.

## Decision

### Configuration and manifest

The acLabs launcher MUST process `customizations.aristaLabs.artifactManifest`:

```json
{
    "customizations": {
        "aristaLabs": {
            "artifactManifest": "artifacts.yml"
        }
    }
}
```

The value is a nonempty path relative to the lab's effective `workspaceFolder`,
not the devcontainer configuration directory. The manifest must already exist in
that workspace's checked-out content. An absent property means no staging or
implicit discovery; an invalid, missing, or unreadable selected manifest fails
creation. This is a launcher-specific integration, not standard devcontainer
behavior.

The manifest is one UTF-8 YAML document with a required `files` list and optional
`images` list. No schema version or other top-level keys are supported.

```yaml
files:
  - filename: my-extension-1.2.3.vsix
    path: my-extension-1.2.3.vsix

  - filename: sa178-SecurityAdvisory178_CVE-2026-73440.swix
    path: containerlab/assets/sa178-SecurityAdvisory178_CVE-2026-73440.swix
    sha256: "da9388362250db73fd8721e6889c0f90c8f548b25baee16e64621424200f24c6"
```

| File field | Required | Meaning |
| --- | --- | --- |
| `filename` | Yes | Exact, case-sensitive storage basename; not a path or URL. |
| `path` | Yes | Destination relative to the lab workspace root, including filename. |
| `sha256` | No | Expected content digest: exactly 64 hexadecimal characters. |

Field values MUST be nonempty strings; omit optional values rather than using
null. Destination filenames may differ from source filenames. Multiple entries
may share a source, but supplied hashes for that source must agree and destinations
must not conflict. `files: []` requests no files.

Use safe, bounded YAML parsing. Reject unknown fields, duplicate mapping keys,
multiple documents, custom tags, aliases, invalid field types, and malformed
checksums.

`images`, when present, MUST be a list of nonempty strings. Omitted and empty lists
are equivalent. A nonempty list produces an informational notice that image
handling is outside scope; it does not fail file staging or trigger image lookup,
syntax or availability checks, registry access, copying, or import. Image archives
listed under `files` are ordinary opaque files.

### Storage and access

The launcher MUST resolve files exclusively through operator-approved storage and
apply authorization independently of repository declarations. Authorization applies
to launcher access to storage, not to individual labs. Any lab may request any
artifact in approved storage by listing it in the manifest; no separate per-lab
allowlist or entitlement check is required.

Storage sources, lookup rules, credentials, and launcher limits MUST come from
trusted host configuration. Repository content, container settings, and `runArgs`
cannot add sources or grant access. This contract does not prescribe a storage
provider, backend, protocol, layout, or client implementation.

Resolve each declared filename to exactly one artifact using operator-configured
rules. Missing or ambiguous matches, unavailable storage, and storage access
failures MUST fail creation without an unapproved fallback. Wildcard and
case-insensitive lookup are unsupported. Source aliases, redirects, or concurrent
changes MUST NOT escape approved storage or substitute unverified content.

Copy only listed files. The launcher MUST NOT expose storage credentials, mount
artifact storage into the container, or provide direct storage access or mutation
through this feature. Approval of storage makes its artifacts requestable by every
lab; it does not cause unlisted artifacts to be delivered.

### Creation lifecycle

1. Validate the selected manifest, source resolution, destinations, and resource
   limits; retrieve files into private host-side staging and verify supplied hashes.
2. Place the verified files at their declared paths in the host-side workspace,
   then deliver the prepared workspace into the stopped container. Verify that
   delivered bytes match the staged content and any supplied hashes.
3. Record completion in host-controlled state, then start the container and allow
   initialization hooks, editor access, and lab preparation.

The container and repository-provided hooks MUST NOT start before staging and
workspace delivery succeed. Untrusted workloads and users MUST NOT modify the
workspace during preparation. Copying into a running container is unsupported.

Staging runs only on creation. Restart, attach, manifest edits, or storage changes
do not refresh existing files. Rebuild or recreation starts a new attempt; a reused
workspace remains subject to the same collision rules. Retry requires an explicit
launcher action and host-controlled completion records, not lab-writable markers.

### File safety and integrity

- Manifest references and destinations MUST be nonempty workspace-relative paths
  using `/` separators. Reject absolute paths, URI/drive/UNC forms, empty or `.` or
  `..` components, trailing separators, backslashes, and control characters.
  Source basenames must also exclude separators and `.` or `..` values. No shell,
  variable, tilde, or wildcard expansion is performed.
- Enforce actual workspace containment with race-resistant operations, not string
  prefixes. Reject symlinks in manifest or destination paths and nested mounts
  outside the launcher's trusted workspace boundary. Never execute path values.
- Reject duplicate destinations, file/directory conflicts, existing final files,
  and incompatible parents. Do not overwrite the manifest or checked-out content,
  even if an existing file has the expected hash. Existing regular parent
  directories may be reused; missing parents may be created.
- Copy unchanged bytes from the verified snapshot and preserve source artifacts.
  A supplied SHA-256 MUST match before publication and after delivery. Without a
  supplied hash, still verify transfer correctness; do not claim expected-content
  verification or write a computed hash into the manifest. Checksums establish
  correspondence with the declaration, not publisher authenticity or safety.
- Deliver regular files owned by the workspace user with mode `0600`; create
  directories with mode `0700`. Do not broaden existing permissions or preserve
  source ownership, ACLs, extended attributes, executable or special permission
  bits. Later setup may adjust permissions as needed.
- Do not extract archives, install extensions, execute files, or infer provisioning
  actions from file extensions. Those actions belong to later lab preparation.

### Failure and reporting

Any required-file failure MUST produce a failed creation state and nonzero outcome,
preventing container startup and dependent operations. Validate declarations and
destinations before publication; publish individual files atomically after complete
transfer. A transaction across all files is not required: completed files may
remain after partial failure, but startup remains blocked.

Private temporary copies MUST be inaccessible to lab users and other unprivileged
host users, removed after success or failure, and recovered after interrupted
attempts. Cleanup must preserve source artifacts and pre-existing workspace files.
Recovery of published files requires host-owned records and a protected workspace;
otherwise use a fresh workspace or explicit operator remediation.

Operator configuration MUST bound manifest size, entry counts, individual and
aggregate file sizes, and operation duration, enforced during reads. Report
validation, storage, lookup, collision, integrity, transfer, and limit failures,
as well as successful staging and out-of-scope image metadata. Logs may identify
entries and relative destinations but MUST NOT expose credentials, file contents,
storage listings, or private source locations to lab users. Staging completion
means files were delivered, not that extensions, images, devices, or the lab are
ready.

## Future capabilities

- Image acquisition, copying, import, and availability checks require a separate
  decision about approved sources, identity, and target runtime. Host images are
  not necessarily available to a separate DinD daemon, whose import phase may
  need to occur after startup.
- Per-lab artifact entitlements may be introduced separately if deployments need
  different access scopes.

Neither capability is required by this decision.
