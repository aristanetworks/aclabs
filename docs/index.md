# Arista Community Labs

Welcome to Arista Community Labs!

This site serves as a repository of labs built by the Arista community, for the Arista community.

??? info "🚧  Pardon our dust 🏗️"
    The Arista Community Labs repository is under active development with new labs and features coming soon!

    Labs that currently reside in the following locations are being migrated to Arista Community Labs:

    - [One-Click Demos](https://arista-netdevops-community.github.io/one-click-se-demos/)
    - [AVD with cEOS-Lab](https://arista-netdevops-community.github.io/avd-cEOS-Lab/)

## What is a Community Lab?

Whether refreshing one's skills, performing testing, or learning new technologies, protocols, features, and tools, building and maintaining the lab environments necessary to support these endeavors can be a daunting task fraught with software dependencies and caveats.

Arista Community Labs reduce the burden of this task, with each lab environment built with three primary objectives:

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Ease of Consumption__

    ---

    Labs can be instantiated at any time with a single click of a button.

-   :fontawesome-solid-person-running:{ .lg .middle } __Portability__

    ---

    The only local software requirement is a web browser.

-   :material-puzzle:{ .lg .middle } __Modularity__

    ---

    Nodes, image versions, and tools are easily modified over time.

</div>

The lab environments are pre-packaged with tools such as Ansible, Python, and the Arista [AVD](https://galaxy.ansible.com/ui/repo/published/arista/avd/), [CVP](https://galaxy.ansible.com/ui/repo/published/arista/cvp/), and [EOS](https://galaxy.ansible.com/ui/repo/published/arista/eos/) Ansible Galaxy collections.

Labs are created through the use of templates, [Github Actions](https://docs.github.com/en/actions), [Github Codespaces](https://github.com/features/codespaces), and [ContainerLab](https://containerlab.dev)[^1].'

Once started, labs will automatically download(1) the necessary cEOS-lab(2) and other container images necessary for the toplogy.
{ .annotate }

1. Automatic download of cEOS-lab is accomplished via the [Arista EOS Downloader](https://pypi.org/project/eos-downloader/) utility.
2. Downloading cEOS-lab requires an [Arista user token](https://www.arista.com/en/users/profile). See the [Quickstart Guide](./quickstart.md) for more information.

## How do I get started?

The [Quickstart Guide](./quickstart.md) is available to help folks who are trying out the labs for the first time or just need a refresher.

[^1]: Containerlab is distributed under conditions of [BSD-3 license](https://github.com/srl-labs/containerlab/blob/main/LICENSE).
