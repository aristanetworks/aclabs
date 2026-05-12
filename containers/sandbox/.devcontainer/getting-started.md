# Welcome to the UCN Sandbox Lab! 🧪

This sandbox is your personal Arista lab in a box — pre-loaded with everything
you need to design, build, deploy, and tear down network topologies without
leaving the IDE.

The **Sandbox Dashboard** in this window is your control panel. Each button
maps to a real workflow you'll use day to day. This guide walks you through
when to click which one, plus how to find your way back if you accidentally
close the dashboard.

---

## 🔑 Default credentials

**Default credentials** for all cEOS and Linux nodes: username `admin`,
password `admin`.

---

## 🚨 Closed the dashboard? Here's how to bring it back

The dashboard tab is **pinned by default** to make it harder to close by
accident — pinned tabs ignore middle-click and survive *Close All*. If
you do close it deliberately (or right-click → Unpin and then close it),
two ways to reopen:

**Option 1: Status bar (easiest).** Look at the bottom-left corner of this
window for a button labeled **🧪 Sandbox Dashboard**. Click it. Done.

**Option 2: Command Palette.** Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on
Mac), type `Sandbox Dashboard: Open`, and hit Enter.

If you ever feel stuck, those two paths will always bring the dashboard back.

---

## 🎬 Quick start: pick your starting point

The **Sources** row of the dashboard is where every lab session begins.
Pick the button that matches what you're trying to do:

### 🎨 Start Building!

> *"I want to design a new topology from scratch."*

Opens the ContainerLab Topology Designer. Drag nodes onto a canvas, wire them
up, save the result as a topology file. Best for greenfield labs where you
don't have a starting point.

### 📥 Import Lab

> *"I have a lab archive and I want to bring it into this sandbox."*

A file picker opens in your browser so you can pick a `.tar`, `.tar.gz`,
`.tar.bz2`, or `.tar.xz` archive from your local machine. The dashboard
streams the file into the sandbox in 4 MB chunks with a real progress bar,
bitrate, and ETA — even multi-hundred-MB archives upload reliably.

The lab replaces your current workspace contents, so existing files will be
permanently deleted. If a lab is currently running, the dashboard will
destroy it (`containerlab destroy --cleanup`, no save) before wiping the
workspace — the destructive-confirmation modal will tell you exactly what's
about to happen so there are no surprises.

### 🐙 Clone from GitHub

> *"I want to work with an existing GitHub repo."*

Enter the repo URL (public or private — you'll be prompted to authenticate
for private repos). After the URL, you'll be asked **how** you want to use
the repo:

- **Track this repo** — keep the existing git history and remote. Push to
  GitHub will push back to the source repo (if you have access). Use this
  when you genuinely want to contribute back.
- **Use as a starting template** — strip the git history and start fresh as
  your own. Push to GitHub will publish to a new repo of your choice. Use
  this when you want the bones of someone's repo but plan to make it your
  own thing.

Like Import, this replaces your current workspace contents — and if a lab
is currently running, it will be destroyed (`containerlab destroy --cleanup`,
no save) before the wipe. The destructive-confirmation modal will disclose
both the files to be removed AND any running labs to be destroyed.

### 📚 Borrow from Tech Library

> *"Show me the curated starter labs and let me grab one."*

Shows a list of labs from the Arista Tech Library. Pick one and it lands
in your workspace, ready to be edited. Best for "I want a known-good
starting point but I'm not sure what shape my topology needs yet."

The borrow happens without initializing a git repo, so your sidebar stays
quiet (no untracked-file noise) unless you explicitly opt into source
control. When you're ready to publish your changes, **Push to GitHub** will
initialize the git repo and create a fresh remote for you.

Like Import and Clone, Borrow replaces your current workspace contents —
and if a lab is currently running, it will be destroyed
(`containerlab destroy --cleanup`, no save) before the wipe.

---

## 🔧 Working with your lab

Once your workspace has a topology, the **Lifecycle** row of the dashboard
is where you'll spend most of your time:

### ▶️ Start

> *"Deploy the topology to ContainerLab."*

Spins up the nodes defined in your `topology.clab.yml` file. ContainerLab
does the heavy lifting; the dashboard just gives you a one-click trigger.

### 🗺️ Topology View

> *"Show me the topology graphically so I can interact with it."*

Opens the ContainerLab Topology Viewer in a new tab. From there:
- **SSH** to a node by right-clicking it and selecting `SSH`. A new terminal
  opens with the SSH session.
- **Packet capture** by right-clicking a link and clicking the Wireshark
  icon. The link's traffic streams into Wireshark.
- **Shortcuts** for keyboard navigation are listed in the viewer's UI
  (look for the Shortcuts icon).

### 📝 Open Topology File

> *"I want to edit the YAML directly."*

Opens your `topology.clab.yml` in an editor tab. Useful for tweaks the
designer doesn't expose.

### 💻 Open Terminal

> *"I need a shell."*

Opens a new terminal in the bottom panel, rooted at your workspace. Each
click opens a fresh terminal — nothing reuses an existing one. Use this for
ad-hoc `clab`, `git`, `make`, or anything else you'd normally do at a
command line.

### 🛑 Stop

> *"Tear down the running lab."*

When you click Stop, the dashboard asks how you want to leave the lab:

- **Save and Stop** captures the running configs first (same effect as
  running Snapshot Lab and letting it wire your topology), then tears
  down the nodes. The next time you Start, your nodes come back up with
  exactly the state they had when you stopped. Use this when you're
  pausing work and want to pick up where you left off.
- **Stop without Saving** skips the snapshot and just tears down the
  running containers. Files in your workspace are left untouched — only
  the running containers are destroyed. Use this when you're done testing
  or you don't care about preserving the running config (e.g., before
  making large topology changes that would invalidate it anyway).

### 💾 Snapshot Lab

> *"Capture the running configs from my nodes back into the workspace."*

Reaches into the running nodes, grabs their current configs, and writes
them into your workspace under `startup-configs/`. Use this after you've
made changes via SSH that you want to preserve as part of the lab. Snapshot
Lab is also the on-ramp into the **Snapshot & Resume** workflow described
below — it'll offer to wire your topology to auto-resume from the snapshot
on next deploy.

### 🔄 Reset Sandbox Workspace

> *"I broke something. Take me back to the original sandbox starting state."*

Wipes your workspace and restores the pristine baseline this lab shipped
with. Useful if you're stuck or just want to start over. **This is
destructive** — you'll get a confirmation prompt before anything happens.

## 💾 Snapshot & Resume — making your lab reproducible

The dashboard has a built-in workflow for capturing your lab's configs and
making them survive a redeploy. Without this wiring, ContainerLab brings
nodes up from scratch every time you run **Start** — which means anything
you configured via SSH gets wiped on the next deploy.

There are **two paths into the same end-state**, depending on whether you
want to keep the lab running while you snapshot:

- **Snapshot Lab** captures configs while the lab keeps running — best
  for "I just made some great changes and want to bank them without
  pausing my work."
- **Save and Stop** captures configs as part of tearing the lab down —
  best for "I'm pausing work and want to pick up exactly where I left
  off next time."

Either path produces the same result:

1. The running configs from each node are captured into
   `startup-configs/` next to your topology file, organized by lab name
   and node name (e.g., `startup-configs/<lab-name>/SPINE1/startup-config`).
2. The dashboard offers to **wire your topology** to auto-resume from
   those snapshots on next deploy. You'll see a plain-language modal
   explaining exactly what will change (e.g., *"This updates 4 cEOS
   nodes in your topology file to always start from `startup-configs/`"*).
   Existing values are preserved as YAML comments so you can revert if
   you need to. Your `.gitignore` is also updated so the snapshots
   travel with your lab repo.
3. Next time you **Start** the lab, your nodes come back up with the
   configs you snapshotted. (For Save and Stop, "next time" is the
   next Start; for Snapshot Lab, the lab is already running so the
   wiring takes effect on the *next* Stop/Start cycle.)

If your topology is already wired this way, the dashboard recognizes that
and skips the modal. If you don't want to wire your topology automatically,
you can decline the offer and edit the YAML yourself — the dashboard never
modifies your topology without explicit confirmation.

This pairs especially well with **Push to GitHub**: snapshot, wire,
commit, push, and your lab is reproducible by anyone who clones it.

---

The **Destinations** row is for getting your work out of the sandbox:

### 📦 Export Lab

> *"Bundle up everything in my workspace as a lab archive."*

Creates a `.tar.gz` of your workspace at `/sandbox/<name>-<timestamp>.tar.gz`.
After it completes, the dashboard will tell you how to download the file to
your local machine: right-click the file in the Explorer sidebar (left
panel) and choose **Download**.

### 🚀 Push to GitHub

> *"Publish my work to a GitHub repo."*

For new repos: the dashboard creates them as **private only** on your
GitHub account. You'll see a verification modal listing what to double-
check before publishing (no customer information, tokens, production
configs, etc.) — clicking *I have verified — push as private* is your
explicit acknowledgment. You'll then type a name, and the dashboard
handles the rest.

For existing remotes (e.g., a repo you tracked via Clone from GitHub):
this just pushes back to the source. First-time auth uses VS Code's
built-in GitHub sign-in — no token typing required.

---

## 🎯 Arista-specific shortcuts

If you're working with Arista's cloud-managed networking platform, the
**Arista Integrations** row gives you one-click access:

### ☁️ Reserve a CVaaS Tenant

> *"Get me a CVaaS environment to test against."*

Reserves a CVaaS tenant for use with this lab. Useful when you want to
exercise CVaaS workflows (provisioning, monitoring, change control) but
don't have a permanent tenant.

### 🔽 Import cEOS Image

> *"Get a cEOS-lab image into this sandbox so my topology can use it."*

A QuickPick offers two paths — pick the one that matches what you have:

- **Download from arista.com.** Pulls a versioned cEOS-lab release directly
  into Docker. You'll be prompted for your arista.com token on first use
  (saved securely after that), then for the version you want (e.g.,
  `4.35.4M`). If the image is already cached locally, the dashboard tells
  you up front and offers a Force Re-download escape hatch.
- **Upload from local machine.** A file picker opens for you to choose a
  `.tar`, `.tar.gz`, or `.tar.xz` cEOS-lab image you've already downloaded —
  useful for custom builds, archived versions, or images supplied by your
  team. After the upload, you'll type a tag (e.g., `4.35.4M`); the dashboard
  prefixes it with `arista/ceos:` and imports it into Docker. The uploaded
  file is cleaned up automatically after the import succeeds.

Either path leaves you with a cEOS image tagged like `arista/ceos:<your-tag>`,
ready to reference in your `topology.clab.yml` as `image: arista/ceos:<your-tag>`.

### 📡 Onboard to CVaaS

> *"Connect this lab's switches to my CVaaS tenant."*

Wires the running nodes in your lab up to a CVaaS tenant so you can manage
them from CVaaS just like production switches. Pairs naturally with
**Reserve a CVaaS Tenant** if you don't already have a tenant.

### 📦 Change AVD Version

> *"Switch this lab to a different version of the Arista AVD collection."*

Detects the AVD collection version currently installed in this sandbox and
opens a picker so you can switch to something else: `devel` for the bleeding
edge, the top stable releases, or a Custom version you enter yourself.
Useful when a lab needs a specific AVD version different from the one
shipped with this sandbox, or when you're testing against a pre-release.
You'll get a confirmation prompt before any existing version is replaced.

---

## 💡 Tips & Tricks

- **The dashboard's Lab Overview card** at the top changes based on what
  you're working on — it shows lab name, helpful links, and resource
  badges. Worth a glance before you start.
- **Buttons disable themselves** when they don't apply (e.g., "Stop" is
  disabled if no lab is running). If something looks grayed out, hover for
  a tooltip explaining why.
- **Most actions are reversible.** Cloned the wrong repo? Click Reset and
  start over. Imported the wrong lab archive? Reset. The dashboard is designed
  to encourage experimentation.
- **The ContainerLab VS Code Extension** is also pre-installed and gives
  you richer interaction with running labs (look for the ContainerLab icon
  in the activity bar on the far left). The dashboard's Topology View
  button is the quickest way in, but the extension panel offers more.

---

## 🆘 Need more help?

- **Closed the dashboard?** Click the **🧪 Sandbox Dashboard** button in
  the bottom-left status bar, or run `Sandbox Dashboard: Open` from the
  Command Palette (`Ctrl/Cmd+Shift+P`).
- **Found a bug or have feedback?** Use the **🐞 Report an Issue** link in
  the dashboard's Welcome card.

Happy labbing! 🥳🧪