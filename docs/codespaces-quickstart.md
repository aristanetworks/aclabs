# Codespaces Quickstart Guide

## What is Github Codespaces

[Github Codespaces](https://github.com/features/codespaces) allows you to start a fully configured development environment directly on the Github cloud infrustructure. There is no need to setup your own machine and with the help of a [deep link](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/setting-up-your-repository/facilitating-quick-creation-and-resumption-of-codespaces#creating-a-link-to-the-codespace-creation-page-for-your-repository) the entire environment can be started by pressing a button.

In our case the development environment means - all the tools we need to start playing with the network lab and the lab infrustructure itself. With the power of [docker-in-docker](https://github.com/microsoft/vscode-dev-containers/blob/main/containers/docker-in-docker/README.md) Codespaces allow to encapsulate all that into a single container. The best part is that Codespaces are based on the [dev container specification](https://containers.dev/implementors/spec/) and dev containers can be started on any other machine with the power of VSCode or another supporting tool, making the environment fully portable.(1)
{ .annotate }

1. At the time of writing the cEOS-lab images for ARM are not yet released and the environment portability is limited to x86 machines. ARM support for acLabs is coming later.

[Codespaces](https://github.com/features/codespaces) is a commertial feature provided by Github. However as of time of writing it has a very generous free monthly quota of 120 core-hours and 15 GB storage every month. It's a lot of lab time for free and [Github Codespaces pricing](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces#pricing-for-paid-usage) is very affordable. Let's take deeper look at how Github billing really works.

## Github Codespaces Billing

Github will never charge you, unless you change your spending limit.

The first thing to know about Github billing is that you will never be charged by default, unless you change your spening limit.

