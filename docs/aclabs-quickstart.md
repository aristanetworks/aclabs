# Getting started with Arista Community Labs

This guide is intended for individuals looking to familiarize themselves with the steps necessary to spin up an Arista Community Labs topology hosted via [GitHub Codespaces](https://github.com/features/codespaces/).

A deep understanding of GitHub Codespaces is not required to begin using Arista Community Labs. Those seeking more information on how GitHub Codespaces provides the foundation for Arista Community Labs can find this information and more in the [Codespaces Quickstart Guide](./codespaces-quickstart.md).

## Pre-Requisites

Before launching an Arista Community Lab, we need to ensure we have the following:

1. An arista.com account with the ability to download cEOS-lab via [Software Downloads](https://www.arista.com/en/support/software-download)
2. A [GitHub account](https://github.com/signup)
3. A copy of our [arista.com user token](https://www.arista.com/en/users/profile)

We can find our user token by logging into [arista.com](https://www.arista.com) and selecting `My Profile`.

The tabs below illustrate the steps needed to locate and copy the token:

=== "Login"
    <figure markdown>
    ![Arista Login](/assets/img/aclasbs-quickstart-aristalogin.png "Arista Login"){ width=700px }
    <figcaption>Arista - Login</figcaption>
    </figure>

=== "My Profile"
    <figure markdown>
    ![Arista My Profile](/assets/img/aclasbs-quickstart-arista-myprofile.png "My Profile"){ width=700px }
    <figcaption>Arista - My Profile</figcaption>
    </figure>

=== "User Token"
    <figure markdown>
    ![Arista Token](/assets/img/aclasbs-quickstart-arista-portalaccess.png "User Token"){ width=700px }
    <figcaption>Arista - User Token (Blurred) </figcaption>
    </figure>

??? question "What's with the token? :coin:"
    When an Arista Community Lab is started, the user token will be used to automatically download and import the necesary cEOS-lab image into the lab environment

## Starting a Lab

!!! note
    Throughout this guide, we will use the [EVPN Domain A](https://codespaces.new/aristanetworks/aclabs/tree/main?quickstart=1&devcontainer_path=.devcontainer%2Ftechlib-vxlan-domain-a%2Fdevcontainer.json) lab associated with the [EVPN/VXLAN Deployment Guide](https://tech-library.arista.com/data_center/evpnvxlan/deployment_guide/) on [Arista's Tech Library](https://tech-library.arista.com) as reference point. All community labs hosted via Codespaces will follow the same process.

Once a lab has been launched via it's respective 'Start Lab' button, a `Create Codespace` window will be opened via a web browser:

<figure markdown>
![Create Codespace](assets/img/aclabs-quickstart-1.png "Create Codespace"){ width=500px }
<figcaption> Create a Codespace - Enter our user token </figcaption>
</figure>

In the `ARTOKEN` field, we will paste the user token copied from our arista.com user profile. This is a one time requirement, and will be saved for all of our subsequent Arista Community Lab deployments.

??? question "Where is the token saved? :thinking:"
    Once entered, the token is saved as a GitHub Codespaces `Secret`. This can be viewed via the [Codespaces section of our GitHub account settings](https://github.com/settings/codespaces).

??? note "Watch the expiration date! :hourglass_flowing_sand:"
    User tokens on arista.com have an expiration date associated with them, listed in the `Token Valid Till` field in the `Portal Access` section of the user profile.

    If the token has expired, simply click `Regenerate Token` to create a new one. A token expires one year after it was generated; This value cannot be modified by the user.

Once we've pasted in our token and selected `Create new Codespace`, a new tab will open in our browser containing the codespace

??? question "Wait...the codespace opened in my local VS Code!"
    Not a problem - this just means that VS Code is locally installed and `Visual Studio Code` is selected in the `Editor preference` section of our [GitHub account's Codespaces settings](https://github.com/settings/codespaces).

In our newly launched Codespace, we will see the `Post Deploy Script` running in the terminal. This script is getting our lab enviornment ready to launch, and may take a few minutes to complete.

!!! note "Grab a coffee! :coffee:"
    The post deployment script can take a few minutes to run. Grab a coffee while the lab environment is being created.

Once complete, we will be presented with the `Welcome` page. We can use this page to choose a different color theme, or simply close it out. We will also see our GitHub account name and lab shown in the terminal prompt of the Codespace.

At this point, we can `Maximize Terminal` to ensure we have adequate real estate when opening SSH sessions to nodes in our lab topology.

Once the terminal has been maximized, it's time to `Start the Lab` be entering the following command at the terminal:

```bash
make start
```

After starting the lab, we will see a series of `Informational Output` scroll across the terminal as the lab is being instantiated.

When complete, the terminal will display a table containing a `Lab Deployment Summary`. This includes information related to the nodes that were deployed when creating the lab.

=== "Post Deploy Script"
    <figure markdown>
    ![acLab Post Deploy](/assets/img/aclabs-quickstart-postdeploy.png "Post Deploy"){ width=800px }
    <figcaption>Post Deploy Script (Click to Zoom)</figcaption>
    </figure>

=== "Welcome"
    <figure markdown>
    ![Codespace Welcome](/assets/img/aclabs-quickstart-welcome.png "Codespace Welcome"){ width=800px }
    <figcaption>Codespace Welcome (Click to Zoom)</figcaption>
    </figure>

=== "Maximize Terminal"
    <figure markdown>
    ![Maximize Panel](/assets/img/aclabs-quickstart-maximizepanel.png "Maximize Panel"){ width=800px }
    <figcaption>Maximize Terminal Window (Click to Zoom)</figcaption>
    </figure>

=== "Start the Lab"
    <figure markdown>
    ![Start Lab](/assets/img/aclabs-quickstart-make-start.png "Start Lab"){ width=800px }
    <figcaption>Start the Lab (Click to Zoom)</figcaption>
    </figure>

=== "Informational Output"
    <figure markdown>
    ![Info Output](/assets/img/aclabs-quickstart-info-output.png "Info Output"){ width=800px }
    <figcaption>Informational Output (Click to Zoom)</figcaption>
    </figure>

=== "Lab Deployment Summary"
    <figure markdown>
    ![Lab Summary](/assets/img/aclabs-quickstart-lab-deploy-success.png "Lab Summary"){ width=800px }
    <figcaption>Lab Deployment Summary (Click to Zoom)</figcaption>
    </figure>

## Interacting with a Lab

Once the lab has been deployed, we can use the terminal in our Codespace to SSH into the nodes.

A list of `Lab Hosts` that are accessible via `SSH` can be viewed at any time from the terminal by entering the following command:

```bash
sudo clab inspect -a
```

To access an EOS host via our Codespace termianl, use the `ssh` command followed by the host name as shown below

```bash
ssh A-SPINE1
```

Access to Ubuntu hosts requires that the `admin` username be defined as a part of the ssh command:

```bash
ssh admin@HostA1
```

!!! question "What's the password? :lock:"
    Unless stated otherwise, the default username of `admin` and password of `admin` is used for all nodes in an Arista Community lab

Once connected, we can interact with the lab as needed.

=== "Lab Hosts"
    <figure markdown>
    ![Available Hosts](/assets/img/aclabs-quickstart-availablehosts.png "Available Hosts"){ width=800px }
    <figcaption>Lab Hosts Accessible via SSH (Click to Zoom)</figcaption>
    </figure>

=== "SSH"
    <figure markdown>
    ![SSH](/assets/img/aclabs-quickstart-ssh-to-host.png "SSH"){ width=800px }
    <figcaption>SSH to a Lab Host (Click to Zoom)</figcaption>
    </figure>

## Stopping the Lab

When we're finished with our lab, we can spin down the environment by issuing the following command in the terminal of our Codespace:

```bash
make stop
```

Once the lab has stopped, we can then choose to stop or delete our codespace by selecting the `Remote Window` button in the lower lefthand corner of our Codespace, and then choosing `Stop Current Codespace` or `My Codespaces`

<figure markdown>
![Stop Codespace](/assets/img/aclabs-quickstart-stop-codespace.png "Stop Codespace"){ width=800px }
<figcaption>Stop or Delete Codespace (Click to Zoom)</figcaption>
</figure>

If we choose `My Codespaces`, this will open a webpage containing a list of [our current GitHub Codespaces](https://github.com/codespaces/). From here, we can locate our Codespace used for this session and stop or delete it if desired.

<figure markdown>
![My Codespaces](/assets/img/aclabs-quickstart-my-codespaces.png "My Codespaces"){ width=800px }
<figcaption>Our Current Codespaces (Click to Zoom)</figcaption>
</figure>

:test_tube: Happy labbing! :test_tube:
