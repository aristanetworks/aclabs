# Arista Community Labs

Welcome to Arista Community Labs!

This site serves as a repository of labs built by the Arista community, for the Arista community.

## What is a Community Lab?

Whether refreshing one's skills, performing testing, or learning new technologies, protocols, features, and tools, building and maintaining the lab environments necessary to support these endeavors can be fraught with software dependencies and caveats.

Arista Community Labs reduce the burden of this task, with each lab environment built with three primary objectives:

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Ease of Consumption__

    ---

    Labs can be instantiated at any time with the click of a button.

-   :fontawesome-solid-person-running:{ .lg .middle } __Portability__

    ---

    The only local software requirement is a web browser.

-   :material-puzzle:{ .lg .middle } __Modularity__

    ---

    Nodes, image versions, and tools are easily modified over time.

</div>

The lab environments are pre-packaged with tools such as Ansible, Python, and the Arista [AVD](https://galaxy.ansible.com/ui/repo/published/arista/avd/), [CVP](https://galaxy.ansible.com/ui/repo/published/arista/cvp/), and [EOS](https://galaxy.ansible.com/ui/repo/published/arista/eos/) Ansible Galaxy collections.

Labs are created through the use of templates, [Github Actions](https://docs.github.com/en/actions), [Github Codespaces](https://github.com/features/codespaces), and [ContainerLab](https://containerlab.dev)[^2].'

Once started, labs will automatically download(1) the necessary cEOS-lab(2) and other container images necessary for the toplogy.
{ .annotate }

1. Automatic download of cEOS-lab is accomplished via the [Arista EOS Downloader](https://pypi.org/project/eos-downloader/) utility.
2. Downloading cEOS-lab requires an [Arista user token](https://www.arista.com/en/users/profile). See the [Quickstart Guide](./quickstart.md) for more information.

## How do I get started?

The [Quickstart Guide](./quickstart.md) is available to help folks who are trying out the labs for the first time or just need a refresher.

[Get Started :material-greater-than:](./quickstart.md){ .md-button .md-button--primary }

[^1]: This site uses the [Pexels](https://www.pexels.com/) royalty-free image library. Thank you to all Pexels authors and contributors!
[^2]: Containerlab is distributed under the [BSD-3 license](https://github.com/srl-labs/containerlab/blob/main/LICENSE).
