# Codespaces Quickstart Guide

## What is Github Codespaces

[Github Codespaces](https://github.com/features/codespaces) allows you to start a fully configured development environment directly on the Github cloud infrastructure. There is no need to setup your own machine and with the help of a [deep link](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/setting-up-your-repository/facilitating-quick-creation-and-resumption-of-codespaces#creating-a-link-to-the-codespace-creation-page-for-your-repository) the entire environment can be started by pressing a button.

In our case the development environment means - all the tools we need to start playing with the network lab and the lab infrastructure itself. With the power of [docker-in-docker](https://github.com/microsoft/vscode-dev-containers/blob/main/containers/docker-in-docker/README.md) Codespaces help to encapsulate all that into a single container. The best part is that Codespaces are based on the [dev container specification](https://containers.dev/implementors/spec/) and dev containers can be started on any other machine with the power of VSCode or another supporting tool, making the environment fully portable.(1)
{ .annotate }

1. At the time of writing the cEOS-lab images for ARM are not yet released and the environment portability is limited to x86 machines. ARM support for acLabs is coming later. And a __nerdy warning__: your host setup matters! A bad Docker installation or Linux kernel configuration can break everything.

[Codespaces](https://github.com/features/codespaces) is a commercial feature provided by Github. However as of time of writing it has a very generous free monthly quota of 120 core-hours and 15 GB storage every month. It's a lot of lab time for free and [Github Codespaces pricing](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces#pricing-for-paid-usage) is very affordable. Let's take deeper look at how Github billing really works.

## Github Codespaces Billing

The first thing to know about Github billing is that you will never be charged by default, unless you change your spending limit.  
To check you spending limit, you can go to your Github account `Settings`(1) > `Billing and plans` > `Spending limits`(2) > `Codespaces` > `Limit spending`(3). The default will be zero. That will prevent any extra expenses and stop all Codespaces when monthly quota is over. However you can certainly consider increasing that to some minimum amount if you plan to run bigger Codespaces instances often enough.
{ .annotate }

1. ![gh account settings](assets/img/gh-account-settings.png){ .opacity09 }
2. ![gh spending limits](assets/img/gh-spending-limits.png){ .opacity09 }
3. ![gh limit spending](assets/img/gh-limit-spending.png){ .opacity09 }

When you run a 4-core Codespace instance (the default size available to all Github users) for 1 hour, you'll consume 4 core-hours from your quota. That means, if you run this kind of instance no-stop, you'll be able to run it for 120/4 = 30 hours until your free quota will be over. Core-hours quota will only be used when Codespace is running. When stopped manually or via idle timeout - no core-hours will be billed. The idle timeout is the period of time after which a Codespace will be stopped if not used. Default of 30 minutes is generally fine for all use cases, however you can change it in `Settings` > `Codespaces` > `Default idle timeout`

![codespace idle timeout](assets/img/codespace-idle-timeout.png){ .opacity09 }

The storage is billed monthly, but will be consumed as long as container exists. Even when it's stopped. A Codespace that is using 4GB of storage will consume 4GB out of your 15GB quota if it exists for an entire month (even if not actively used). The retention period defines when the Codespaces will be deleted if not actively used. For an average lab environment it's feasible to reduce the default retention period of 30 days to a lower value in `Settings` > `Codespaces` > `Default retention period`. This will significantly reduce the storage utilization.

![codespace retention period](assets/img/codespace-retention-period.png){ .opacity09 }

The list of all running Codespaces is available on [github.com/codespaces](https://github.com/codespaces). The best way to reduce CPU and storage utilization is to delete them from the list immediately when you finish working with the lab.

![codespace delete](assets/img/codespace-delete.png)

You can find more details about Codespaces billing on [Github documentation](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces).
