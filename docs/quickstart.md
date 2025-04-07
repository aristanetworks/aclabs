# Getting started with Arista Community Labs

This guide is intended for individuals looking to familiarize themselves with the steps necessary to get started with Arista Community Labs, powered by [GitHub Codespaces](https://github.com/features/codespaces/).

<div class="grid cards" markdown>

- :octicons-tasklist-16: [Pre-Requisites](#pre-requisites)
- :octicons-rocket-16: [Start the Lab](#starting-the-lab)
- :material-cursor-default-click: [Interact with the Lab](#interacting-with-the-lab)
- :fontawesome-regular-circle-stop: [Tips and Troubleshooting](#tips-and-troubleshooting)

</div>

## Pre-Requisites

Before launching an Arista Community Lab, the following pre-requisites must be met:

<div class="annotate" markdown>

1. [Arista account](https://www.arista.com)(1) with the ability to download cEOS-lab via [Software Downloads](https://www.arista.com/en/support/software-download)
2. [GitHub account](https://github.com/signup)
3. [GitHub Codespaces Access](https://github.com/features/codespaces)(2)
4. [Arista user token](https://www.arista.com/en/users/profile)

</div>

1. Need an account? Register here! [Arista account registration](https://www.arista.com/en/user-registration).

    The email address used for the account must be associated with a corporate email domain (no Gmail, Yahoo, etc.).

2. For those that have never used Codespaces before, no worries! There is a quick primer on Codespaces included below.

We can find the user token by logging into [arista.com](https://www.arista.com) and selecting [My Profile](https://www.arista.com/en/users/profile).

The tabs below illustrate the steps needed to locate and copy the token:

=== "Login"
    <figure markdown>
    ![Arista Login](assets/img/aclabs-quickstart-aristalogin.png "Arista Login"){ width=500px }
    <figcaption>Arista - Login</figcaption>
    </figure>

=== "My Profile"
    <figure markdown>
    ![Arista My Profile](assets/img/aclabs-quickstart-arista-myprofile.png "My Profile"){ width=500px }
    <figcaption>Arista - My Profile</figcaption>
    </figure>

=== "User Token"
    <figure markdown>
    ![Arista Token](assets/img/aclabs-quickstart-arista-portalaccess.png "User Token"){ width=500px }
    <figcaption>Arista - User Token (Blurred) </figcaption>
    </figure>

??? question "What's with the token? :coin:"
    When an Arista Community Lab is started, the user token will be used to automatically download and import the necessary cEOS-lab image into the lab environment.

## GitHub Codespaces Primer

### Overview

GitHub Codespaces can instantiate a fully configured development or lab environment hosted on GitHub's cloud infrastructure with the click of a button.

Codespaces for Arista Community Labs are pre-packaged with tools such as Python, Ansible, and Ansible Galaxy Collections including [AVD](https://galaxy.ansible.com/ui/repo/published/arista/avd/), [CVP](https://galaxy.ansible.com/ui/repo/published/arista/cvp/), and [EOS](https://galaxy.ansible.com/ui/repo/published/arista/eos/).

[Docker in Docker](https://github.com/microsoft/vscode-dev-containers/blob/main/containers/docker-in-docker/README.md) in alignment with the [Dev Container Specification](https://containers.dev/implementors/spec/) makes all of this possible with Codespaces.

### Costs

GitHub Codespaces is a commercial offering from GitHub. As of October 2024, all GitHub users have 120 hours of Codespace time available for free each month.

By default, if all 120 hours are consumed and the [User's Spending Limit](https://github.com/settings/billing/spending_limit) for Codespaces is $0, then Codespace usage will stop and cannot continue until the hours are replenished the following month.

??? question "When and how would GitHub charge me for this?💰"
    A GitHub user will never be charged for Codespace usage by default. Codespaces will stop working until the hours are renewed the next month.

Users can define a [Payment Method](https://github.com/settings/billing/payment_information) and [Spending Limit](https://github.com/settings/billing/spending_limit) for Codespaces. Once defined, usage beyond 120 hours can continue as long as the spending limit is not exceeded. Once a defined spending limit has been reached, Codespace usage cannot continue until the next month.

Additional information can be found in [GitHub's Codespaces Billing Overivew Page](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-codespaces/about-billing-for-github-codespaces).

??? question "What if I forget about my Codespace? :scream:"
    Don't worry! It won't run forever, at least not by default.

    The `Default idle timeout` and `Default retention period` values can be modified within [GitHub Codespaces Settings](https://github.com/settings/codespaces).

    These parameters can be changed at any time, and should be defined with values that make the most sense for your usage patterns.

    A general recommendation for these values is provided below:

     - **Default idle timeout**: `30 Minutes`
     - **Default retention period**: `1 Day`

Codespaces can be deleted at anytime from the [Codespaces section of GitHub](https://github.com/codespaces).

### Machine Types

Different machine types are available within Codespaces. As a general rule, the greater the number of CPU cores, the greater number of hours that will be consumed during the Codespace's runtime.

[GitHub's Pricing for Paid Usage](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-codespaces/about-billing-for-github-codespaces#pricing-for-paid-usage) chart provides the details of the `usage multiplier` for each available machine type.

For example, as of the writing of this guide:

- :fontawesome-solid-microchip: `2 Core` Machine Types will consume `2` hours for every hour of runtime
- :fontawesome-solid-microchip: `8 Core` Machine Types will consume `8` hours for every hour of runtime
- :fontawesome-solid-microchip: `16 Core` Machine Types will consume `16` hours for every hour of runtime

Some Arista Community Labs make use of larger machine types, such as the :fontawesome-solid-microchip: `16 Core` option.

??? question "My GitHub Account doesn't have access to a larger :fontawesome-solid-microchip: `8 Core` or :fontawesome-solid-microchip: `16 Core` machine types?"
    By default, some larger machine types may not be available for use. In order to resolve this, a ticket can be opened via [GitHub support](https://support.github.com/contact?source=subtitle&tags=rr-general-technical) requesting access to these larger machine types.

    Listed below is a template that can be used for this request:

    ```yaml
    Hello - Can the 8-core and 16-core codespace machine types please be enabled for my account?
    The default 2-core and 4-core machines lack the necessary resources for my use cases.

    Thank you!
    ```

    Once completed, select **Create a Ticket**

## Starting the Lab

!!! note
    All community labs hosted via Codespaces will follow a similar process to the one defined below. Labs that contain exceptions to the process below will have this specifically called out via a note associated with the lab launch button.

Once a lab has been launched via it's respective 'Start Lab' button, a `Create Codespace` window will be opened via a web browser:

<figure markdown>
![Create Codespace](assets/img/lab-enter-token.png "Create Codespace"){ width=500px }
<figcaption> Create a Codespace - Enter your Arista User Token </figcaption>
</figure>

In the `ARTOKEN` field, paste the user token copied from [your arista.com user profile](https://www.arista.com/en/users/profile).

This is a one time requirement, and will be saved for all subsequent Arista Community Lab deployments.

??? question "Where is the token saved? :thinking:"
    Once entered, the token is saved as a GitHub Codespaces `Secret`. This can be viewed via the [Codespaces section of GitHub account settings](https://github.com/settings/codespaces).

    <figure markdown>
    ![Create Codespace](assets/img/codespaces-secrets.png "Codespaces Secrets"){ width=500px }
    <figcaption> Codespaces Secrets </figcaption>
    </figure>

??? note "Watch the expiration date! :hourglass_flowing_sand:"
    User tokens on arista.com have an expiration date listed in the `Token Valid Till` field in the `Portal Access` section of the user profile.

    If the token has expired, click Regenerate Token to create a new one. A token expires one year after it was generated; the user cannot modify this value.

Once the token has been entered, and `Create new Codespace` has been selected, a new tab will open in the browser containing the codespace

??? question "Wait...the codespace opened in my local VS Code!"
    Not a problem! This just means that VS Code is locally installed and `Visual Studio Code` is selected in the `Editor preference` section of the [GitHub account's Codespaces settings](https://github.com/settings/codespaces).

In the newly launched Codespace, a tab is opened displaying an overview of the lab.

The `Post Deploy Script` can be seen running in the terminal.

<figure markdown>
![Post Deployment Script](assets/img/aclabs-quickstart-postdeploy.png "Post Deploy"){ width=500px }
<figcaption>Post Deploy Script Running (Click to Zoom)</figcaption>
</figure>

!!! note "Grab a coffee! :coffee:"
    Depending on the size of the lab, the post deployment script will take between five and ten minutes to complete.

Once the post deployment script has completed, the terminal prompt will change to the GitHub username followed by the name of the lab.

In the screenshot below, the GitHub username is `mitchv85` and the lab is `techlib-eos-tips`.

<figure markdown>
![Post Deployment Script](assets/img/aclabs-quickstart-postdeploy-complete.png "Post Deploy"){ width=500px }
<figcaption>Post Deploy Script Complete (Click to Zoom)</figcaption>
</figure>

At this point, the lab is ready to go! Running the following command in the terminal will provide an overview and status of all deployed nodes:

```bash
make inspect
```

<figure markdown>
![Post Deployment Script](assets/img/aclabs-quickstart-make-inspect.png "Post Deploy"){ width=600px }
<figcaption>Lab Status Output (Click to Zoom)</figcaption>
</figure>

??? danger "Lab didn't start? :bug:"
    If the lab did not start up correctly, please check out the [Tips and Troubleshooting](#tips-and-troubleshooting) section of this guide.

    If this section does not contain a solution, please [open an issue](https://github.com/aristanetworks/aclabs/issues) on the [Arista Community Labs repository](https://github.com/aristanetworks/aclabs).

## Interacting with the Lab

### Accessing Lab Nodes

Once the lab is up and running, open the [ContainerLab extension](https://containerlab.dev/manual/vsc-extension/) by clicking it's icon within the Codespace.

Once in the ContainerLab extension, establish SSH connectivity to any node by expanding the lab topology, right-clicking on the node, and selecting `Connect to SSH`.

After selecting `Connect to SSH`, a new tab containing the SSH session to the selected node will be opened in the terminal window.

=== "ContainerLab Extension"

    <figure markdown>
    ![ContainerLab Extension](assets/img/clab-extension-1.png "ContainerLab Extension"){ width=250px }
    <figcaption>ContainerLab Extension Icon (Click to Zoom)</figcaption>
    </figure>

=== "Connect to SSH"

    <figure markdown>
    ![cLab Connect to SSH](assets/img/clab-extension-2.png "cLab Connect to SSH"){ width=400px }
    <figcaption>ContainerLab Extension - Connect to SSH (Click to Zoom)</figcaption>
    </figure>

=== "SSH Tab in Terminal"

    <figure markdown>
    ![cLab Extension - Log into device](assets/img/clab-extension-3.png "cLab Extension - Log into device"){ width=600px }
    <figcaption>ContainerLab Extension - Log into device (Click to Zoom)</figcaption>
    </figure>

### Check Lab Status

The status of a lab can be checked at any time in the [ContainerLab extension](https://containerlab.dev/manual/vsc-extension/) by right-clicking the lab topology name selecting `Inspect Lab`.

Once selected, a new tab displaying the status of the lab topology will be automatically opened.

=== "Inspect Lab"

    <figure markdown>
    ![cLab Extension - Inspect Lab](assets/img/clab-extension-4.png "cLab Extension - Inspect Lab"){ width=400px }
    <figcaption>ContainerLab Extension - Inspect Lab (Click to Zoom)</figcaption>
    </figure>

=== "Lab Status Output"

    <figure markdown>
    ![cLab Extension - Lab Status](assets/img/clab-extension-5.png "cLab Extension - Lab Status"){ width=600px }
    <figcaption>ContainerLab Extension - Lab Status (Click to Zoom)</figcaption>
    </figure>

### Stop the Lab

A lab can be stopped at any time by right-clicking the lab topology within the [ContainerLab extension](https://containerlab.dev/manual/vsc-extension/) and selecting `Destroy`.

Once the lab has been successfully stopped, a prompt will be shown in the Codespace indicating that it was successfully destroyed.

=== "Stop Lab"

    <figure markdown>
    ![cLab Extension - Stop Lab](assets/img/clab-extension-6.png "cLab Extension - Stop Lab"){ width=400px }
    <figcaption>ContainerLab Extension - Stop Lab (Click to Zoom)</figcaption>
    </figure>

=== "Success Message"

    <figure markdown>
    ![cLab Extension - Successfully Stopped](assets/img/clab-extension-7.png "cLab Extension - Successfully Stopped"){ width=500px }
    <figcaption>ContainerLab Extension - Successfully Stopped (Click to Zoom)</figcaption>
    </figure>

??? question "What about the Codespace? :thinking:"
    Stopping the lab via the [ContainerLab extension](https://containerlab.dev/manual/vsc-extension/) will stop the cLab topology.

    It ***will not*** stop or destroy the Codespace itself.

    There are two common methods for the Codespace itself to be stopped or deleted

    <div class="annotate" markdown>

    - Manually stop and/or delete the Codespace via you [GitHub Codespaces Dashboard](https://github.com/codespaces) (1)

    </div>

    1. <figure markdown>
    ![Delete Codespace](assets/img/clab-extension-8.png "Delete Codespace"){ width=400px }
    <figcaption>Delete Codespace (Click to Zoom)</figcaption>
    </figure>

    <div class="annotate" markdown>

    - Wait for the `Default idle timeout` and `Default retention time` timers to expire in your [GitHub Codespaces Settings](https://github.com/settings/codespaces) (1)

    </div>

    3. <figure markdown>
    ![Codespace Timers](assets/img/clab-extension-9.png "Codespace Timers"){ width=400px }
    <figcaption>Codespace Timers (Click to Zoom)</figcaption>
    </figure>

### Restart the Lab

If stopped, a lab topology can be started back up by right-clicking on the topology and selecting `Deploy` within the [ContainerLab VS Code Extension User Manual](https://containerlab.dev/manual/vsc-extension/).

If the intent is to restart a lab that is currently running, then select the `Redeploy` option.

=== "Start a Stopped Topology"

    <figure markdown>
    ![cLab Extension - Start the Lab](assets/img/clab-extension-11.png "cLab Extension - Start the Lab"){ width=250px }
    <figcaption>Start a Stopped Lab (Click to Zoom)</figcaption>
    </figure>

=== "Restart a Running Topology"

    <figure markdown>
    ![cLab Extension - Restart Lab](assets/img/clab-extension-12.png "cLab Extension - Restart Lab"){ width=250px }
    <figcaption>Restart a Running Lab (Click to Zoom)</figcaption>
    </figure>

Additional features and functionality provided by the ContainerLab VS Code extension can be found in the [ContainerLab VS Code Extension User Manual](https://containerlab.dev/manual/vsc-extension/). :octicons-beaker-16:

A list of all codespaces can be found in the [Codespaces section of GitHub](https://github.com/codespaces). From here, a codespace can be resumed, stopped, deleted, renamed, and more!

??? note "Conserve those hours! :timer:"
    The `Default idle timeout` and `Default retention period` values can be modified within [GitHub Codespaces Settings](https://github.com/settings/codespaces).

    These parameters can be changed at any time, and should be defined with values that make the most sense for your usage patterns.

    A general recommendation for these values is provided below:

     - **Default idle timeout**: `30 Minutes`
     - **Default retention period**: `1 Day`

## Tips and Troubleshooting

### Tip 1 - 'docker login': denied

During the initial lab provisioning, the user's [Arista Access Token](https://www.arista.com/en/users/profile) is used to download cEOS-lab into the Codespace and import it into Docker.

In the event that the user's Arista Access Token has expired, or is not present, the lab will fail to download cEOS-lab from [arista.com](https://www.arista.com/en/support/software-download) and attempt to download the cEOS-lab image from DockerHub.

When this happens, the lab terminal will display the following message:

```bash
Error: Error response from daemon: pull access denied for arista/ceos, repository does not exist or may require 'docker login': denied: requested access to the resource is denied
make: *** [Makefile:9: start] Error 1
```

??? question "I don't see any error messsages, but my lab didn't start! :confused:"
    If the `Codespace Creation Log` is not automatically opened, it can be accessed via the VS Code `Command Palette`:

    - Open the Command Palette by using the key combination aligned to your OS

       - :fontawesome-brands-windows: ++ctrl+shift+p++
       - :simple-apple: ++cmd+shift+p++

    <div class="annotate" markdown>

    - Enter `View` into the Command Palette prompt (1)

    </div>

    1. <figure markdown>
    ![View Creation Log](assets/img/clab-extension-10.png "View Creation Log"){ width=400px }
    <figcaption>View Creation Log (Click to Zoom)</figcaption>
    </figure>

    - Select `Codespaces: View Creation Log`

    This will open a full creation log including what errors may have been encountered during the Codespace creation process.

    An expired or non-existent [Arista user token](https://www.arista.com/en/users/profile) will result in either an `Authentication Failed` when downloading cEOS-lab from arista.com or `docker login: denied`

When a token is created in a user's [arista.com profile](https://www.arista.com/en/users/profile), it is valid for one year.

Follow the steps below to generate a new token and update the `ARTOKEN` secret used by acLabs Codespaces.

- Open your [arista.com user profile](https://www.arista.com/en/users/profile)

- Choose `Regenerate Token`

<figure markdown>
![Regenerate Token](assets/img/aclabs-quickstart-regen-token.png "Regenerate Token"){ width=500px }
<figcaption>Regenerate Token (Click to Zoom)</figcaption>
</figure>

- Copy the token

<div class="annotate" markdown>

- Update the `ARTOKEN` value in your [GitHub Codespaces Settings](https://github.com/settings/codespaces)(1)

</div>

1. :pencil2: In the event that the `ARTOKEN` secret doesn't exist in your [GitHub Codespaces Settings](https://github.com/settings/codespaces), choose `New secret` and create it.

    This value is created automatically the first time an acLabs lab is launched, but in rare situations this auto-creation may not occur.

<figure markdown>
![Update Token in GitHub](assets/img/aclabs-quickstart-update-artoken.png "Update Token in GitHub"){ width=500px }
<figcaption>Update Arista Token in GitHub Codespace Settings (Click to Zoom)</figcaption>
</figure>

Once updated, launch a new acLab(1) and get back to labbing! :lab_coat:
{ .annotate }

1. :pencil2: It's recommended to delete the Codespace where the failure occurred, and instead create a new one by choosing `Create a new one` when prompted to resume the failed Codespace
    ![New Codespace](assets/img/aclabs-quickstart-new-codespace.png){ width=600px }

### Tip 2 - Resuming an acLab

By default, GitHub Codespaces will automatically shutdown(1) after 30 minutes, and will be deleted(2) after 30 days of inactivity.
{ .annotate }

1. :pencil2: Default idle timeout
2. :pencil2: Default retention period

These `Default idle timeout` and `Default retention period` parameters can be changed at any time within [GitHub Codespaces Settings](https://github.com/settings/codespaces).

A general recommendation for these values is provided below:

- **Default idle timeout**: `30 Minutes`
- **Default retention period**: `1 Day`

If the `Default idle timeout` has been reached, then a user may find themselves presented with the following message when re-launching the lab:

<figure markdown>
![Resume the Codespace](assets/img/aclabs-quickstart-resume-codespace-generic.png "Resume the Codespace"){ width=500px }
<figcaption>Resume the Codespace (Click to Zoom)</figcaption>
</figure>

Multiple choices exist at the above prompt:

<div class="annotate" markdown>

1. Create a new instance of the lab in a new Codespace (1)
2. Resume an existing lab that was shutdown due to the idle timeout being reached
3. Delete the existing codespace(2)

</div>

1. Disregard the remainder of this section and jump into the lab! :smile:
2. ![Delete Codespace](assets/img/aclabs-quickstart-delete-codespace.png)

Select `Resume this codespace` to bring the codespace back up.

Once the Codespace is ready(1) the lab can be resumed via the ContainerLab extension by right-clicking the lab name and selecting `Redeploy`
{ .annotate }

1. If the terminal is open and responsive, the Codespace is back up and running!

<figure markdown>
![cLab Extension - Redeploy Lab](assets/img/aclabs-quickstart-redeploy-lab.png "cLab Extension - Redeploy Lab"){ width=500px }
<figcaption>Redeploy the Lab Topology (Click to Zoom)</figcaption>
</figure>

After selecting `Redeploy`, the terminal will present a message indicating that ContainerLab is in the process of redeploying the lab.

If desired, select `View Logs` to monitor the process of the lab as it is started back up.

<figure markdown>
![cLab Extension - Redeploy Logs](assets/img/aclabs-quickstart-redeploy-clab-logs.png "cLab Extension - Redeploy Logs"){ width=650px }
<figcaption>Redeploy Topology Logs (Click to Zoom)</figcaption>
</figure>

When complete, a message indicating success will be presented and it's time to jump back into the lab! :partying_face:

## :test_tube: Happy labbing! :test_tube:
