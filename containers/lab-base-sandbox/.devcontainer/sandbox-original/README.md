# Welcome to the UCN Sandbox Lab! 🧪

This sandbox is your personal Arista lab in a box — pre-loaded with everything
you need to design, build, deploy, and tear down network topologies without
leaving the IDE.

The **Sandbox Dashboard** in this window is your control panel. Each button
maps to a real workflow you'll use day to day. This guide walks you through
when to click which one, plus how to find your way back if you accidentally
close the dashboard.

> [!WARNING]
> This lab is in preview. It's fully functional, but breaking changes can
> happen. We are working hard on building the best lab collection and your
> feedback is always appreciated.

---

## 🔑 Default credentials

**Default credentials** for all cEOS and Linux nodes: username `admin`,
password `admin`.

---

## 🚨 Closed the dashboard? Here's how to bring it back

This happens — it's a normal VS Code tab and easy to close by accident. Two
ways to reopen it:

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

### 📥 Import Workspace (tar)

> *"I have a tarball of a workspace and I want to bring it into this sandbox."*

Two options when you click: pick a tarball **from your local machine** (a
file picker opens in your browser), or pick one **already in this sandbox**
(e.g., something you created via `tar` in the terminal). The tarball replaces
your current workspace contents, so existing files in the workspace will be
permanently deleted.

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

Like Import, this replaces your current workspace contents.

### 📚 Borrow from Tech Library

> *"Show me the curated starter labs and let me grab one."*

Shows a list of labs from the Arista Tech Library. Pick one and it lands in
your workspace as a fresh git repo on `main` — ready to be edited and
published as your own. Best for "I want a known-good starting point but
I'm not sure what shape my topology needs yet."

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

Shuts down all the running ContainerLab nodes. Files in your workspace are
left untouched — only the running containers are destroyed. Use this when
you're done testing or before making large topology changes.

### 💾 Save Configs

> *"Capture the running configs from my nodes back into the workspace."*

Reaches into the running nodes, grabs their current configs, and writes
them into your workspace. Use this after you've made changes via SSH that
you want to preserve as part of the lab.

### 🔄 Reset Sandbox Workspace

> *"I broke something. Take me back to the original sandbox starting state."*

Wipes your workspace and restores the pristine baseline this lab shipped
with. Useful if you're stuck or just want to start over. **This is
destructive** — you'll get a confirmation prompt before anything happens.

---

## 📤 When you're done

The **Destinations** row is for getting your work out of the sandbox:

### 📦 Export Workspace (tar)

> *"Bundle up everything in my workspace as a tarball."*

Creates a `.tar.gz` of your workspace at `/sandbox/<name>-<timestamp>.tar.gz`.
After it completes, the dashboard will tell you how to download the file to
your local machine: right-click the file in the Explorer sidebar (left
panel) and choose **Download**.

### 🚀 Push to GitHub

> *"Publish my workspace to a GitHub repo."*

Walks you through publishing your workspace to GitHub. If you cloned a repo
in "Track" mode, this pushes back to that repo. Otherwise, it'll prompt you
to create a new repo under your account (or choose an existing one to push
into).

---

## 🎯 Arista-specific shortcuts

If you're working with Arista's cloud-managed networking platform, the
**Arista Integrations** row gives you one-click access:

### ☁️ Reserve a CVaaS Tenant

> *"Get me a CVaaS environment to test against."*

Reserves a CVaaS tenant for use with this lab. Useful when you want to
exercise CVaaS workflows (provisioning, monitoring, change control) but
don't have a permanent tenant.

### 🔽 Download cEOS Image

> *"Pull the latest cEOS container image into this sandbox."*

Downloads the cEOS container image so it's available for your lab nodes.
Pre-built sandboxes already include the image, but if you've reset or want
a different version, this fetches it on demand.

### 📡 Onboard to CVaaS

> *"Connect this lab's switches to my CVaaS tenant."*

Wires the running nodes in your lab up to a CVaaS tenant so you can manage
them from CVaaS just like production switches. Pairs naturally with
**Reserve a CVaaS Tenant** if you don't already have a tenant.

---

## 💡 Tips & Tricks

- **The dashboard's Lab Overview card** at the top changes based on what
  you're working on — it shows lab name, helpful links, and resource
  badges. Worth a glance before you start.
- **Buttons disable themselves** when they don't apply (e.g., "Stop" is
  disabled if no lab is running). If something looks grayed out, hover for
  a tooltip explaining why.
- **Most actions are reversible.** Cloned the wrong repo? Click Reset and
  start over. Imported the wrong tarball? Reset. The dashboard is designed
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
- **Want a refresher?** Watch the [UCN Sandbox Lab overview video](https://youtu.be/_YxHMcES0o4).

Happy labbing! 🥳🧪
