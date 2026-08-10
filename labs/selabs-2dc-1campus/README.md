# Arista_labs_AVD_demo

## Table of Contents
- [Arista\_labs\_AVD\_demo](#arista_labs_avd_demo)
  - [Table of Contents](#table-of-contents)
  - [Credentials](#credentials)
  - [Requirements](#requirements)
  - [topology](#topology)
  - [Instructions](#instructions)
    - [UCN sandbox](#ucn-sandbox)
    - [Import the lab files from the aclabs repository](#import-the-lab-files-from-the-aclabs-repository)
    - [Deploy the lab](#deploy-the-lab)
    - [Validation](#validation)
  - [Run AVD](#run-avd)
  - [GitHub Self-hosted runner](#github-self-hosted-runner)
  - [Demos](#demos)
    - [Digital twin testing](#digital-twin-testing)
  - [Manually deploy or destroy a ContainerLab (clab) topology](#manually-deploy-or-destroy-a-containerlab-clab-topology)
    - [Deploy a clab topology](#deploy-a-clab-topology)
    - [Destroy a clab topology](#destroy-a-clab-topology)
    - [Redeploy the clab topology](#redeploy-the-clab-topology)


## Credentials

The default user/pass for all nodes are cvpadmin / arista123

## Requirements

Minimum version for AVD is 6.3.0
    <details>
      <summary>Expand for AVD upgrade instructions</summary>

Option 1: manually at the terminal
run those two commands:
```
pip install pyavd --upgrade
ansible-galaxy collection install arista.avd --upgrade
```

Option 2: Sandbox Dashboard

If you have closed the `Sandbox Dashboard` tab, you can open it with the button close to the bottom left corner

![dashboard](./media/sandbox11.png)

</details>

## topology

![Topology diagram](./media/diagram.png)

## Instructions

### UCN sandbox

1- "LAUNCH" a UCN sandbox in Arista Labs [here](https://labs.arista.com/prolabs/ucn-sandbox)

2- When ready, connect to the sandbox interface, you should be in web VScode
![webvscode](./media/sandbox1.png)

### Import the lab files from the aclabs repository

1- In the Sandbox Dashboard, click on `Borrow from SE labs`
![borrow](./media/sandbox2.png) and select `selabs-2dc-1campus` from the popup menu.

### Deploy the lab

> [!TIP] You will need a CVP/CVaaS service account token for the step bellow.  
> You can find instructions on how to create a service account [here](https://www.arista.io/help/articles/settings-access-management-service-account-tokens#c2V0dGluZ3MuYWFhU2VydmljZUFjY291bnRzOnRva2Vucw==-adding-a-token-to-a-service-account)

> [!Note]
> you can reserve a CVaaS instance in ProLbas [here](https://labs.arista.com/prolabs/cvaas-reservation)

Run `make preplab` in the sandbox web VSCode terminal.  This will start an interactive prompt that will ask you for inputs required for the lab and github repo.

![deploy](./media/sandbox4.png)
> [!NOTE]
> The git email address need to match the email associated with your GitHub account.

The intecative prompt will authenticate VSCode with GitHub.
Select `GtiHub.com`, `HTTPS`, `Login with web browser`, copy the one time code on the terminal and hit `Enter`

![deploy2](./media/sandbox5.png)
> [!WARNING]
> do not use `Ctrl-c` to copy the one time code from the terminal, it will terminate the playbook execution. 

This will trigger the VScode GitHub extension en open a new browser tab on your desktop to go through authentication.
Follow the steps and paste the one time code when you get to this screen

![deploy3](./media/sandbox14.png)

If the authentication worked, you will get this screen.

![deploy4](./media/sandbox15.png)

The playbook will initialize the local directory as a repository and create a remote private repository on GitHub.

Next it will deploy the ContainerLab topology

![deploy5](./media/sandbox16.png)

Wait until the terminal displays a list of deployed devices

![deploy6](./media/sandbox17.png)


### Validation

1- Try to ssh to a device, example `ssh cvpadmin@dc1-leaf1`
> [!Note]
> user is cvpadmin and password is arista123

![test](./media/sandbox9.png)

2- Validate that the EOS devices are in CVP

![cvp](./media/sandbox10.png)

## Run AVD

You can deploy all configurations with `make deploy-all_digital_twin_clab`.  AVD is configured to create CVP Change Controls but not auto execute.  You have to review/approve/execute in CVP UI for the changes to deploy.
![deploy](./media/sandbox12.png)

> [!Note]
> You can see all the available make commands with `make help`
![help](./media/sandbox13.png)

> [!IMPORTANT]
> When running validation, <code style="color : name_color">[ERROR]</code> during ANTA execution does not mean the playbook errored out, it means there were some ANTA tests failures.
![error](./media/anta.png)

## GitHub Self-hosted runner
> [!NOTE]
> This is only required if you plan to demo CI/CD pipelines

1- In your GitHub forked repositiory, click on `Settings / Actions / Runners / New self-hosted runner`

![runner](./media/runner1.png)

2- Follow the instructions for a linux runner
![runner2](./media/runner2.png)


Detailled instructions on how to create a new GitHub self-hosted runner can be found [here](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners)

## Demos

### Digital twin testing

> [!IMPORTANT]
> This demo requires that the UCN Sandbox host is configured as a github self-hosted runner as per [this step](#github-self-hosted-runner)

This demo show how we can use Arista AVD in conjutction with digital twins to **reduce operational risks** and significatly reduce outages.

In this demo, we had a service (SVI).  
Upon the branch commit, a pipeline will be triggered to build the configuration for production and digital twin.
Upon the PR creation, a pipeline will be triggered to automatically deploy the changes to the clab digital twin and run ANTA validation.  The ANTA report will then be added in the PR as comments.

1- Create a branch, click on the branch shortcut on the bottom left in the sandbox VScode and seclect `+create new branch...`, then enter a name for your branch on the top popup menu.  Example `new vlan`.

![new_branch](./media/demo1-1.png)

2- Edit one of the file under `/sites/_global_vars/TENANTS_NETWORKS/` and add an SVI.  Example: In `BLUE.yml`, add svi 103 with this yaml:
```yaml
          - id: 103
            name: BLUE_VLAN_103
            tags: [ DC1, DC2 ]
            enabled: true
            ip_address_virtual: 192.168.3.1/24
```

![edit](./media/demo1-2.png)

> [!NOTE]
> Do not run the AVD build, we want the pipeline to do that for us.

3- Commit the change to the branch and push to the remote repository

As soon as you publish the branch, the pipeline will trigger and a Ubuntu VM on GitHub cloud will run the AVD build and commit the changes back to the branch in the remote respository

![branch](./media/demo1-3.png)

If you click on the executing action, you can see the steps execution in real time

![branch2](./media/demo1-4.png)

When the workflow is done executing, you can click on `code / <select your branch>` you will see the last commit was done by `github-actions[bot]`.

![branch3](./media/demo1-5.png)

You can click on the commit hash (`ee22ef8` in the picture above) and see all files changes by the workflow.

![branch4](./media/demo1-6.png)

This will generate configuration and documentation for production and the digital twin.

4- Create a PR.  Click on `code` and `Compare & pull request` in the top banner

![pr](./media/demo1-7.png)

> [!NOTE]
> If the banner is not there you can click on `Pull requests / New pull request` 

Make sure the PR is showing diff between your branch (ex: new-vlan) and main, then click on `Create pull request`

![pr2](./media/demo1-8.png)

As soon as the PR is created, it will trigger the workflow called `Deploy & test configuration in the digital twin`

![pr3](./media/demo1-9.png)

You can follow the job status by clicking on `Actions` tab and the the running job

![pr4](./media/demo1-10.png)

Wait for both jobs in the workflow to complete successfully

![pr5](./media/demo1-11.png)

Once completed, your PR should be updated with the ANTA reports for each sites

![pr6](./media/demo1-12.png)

Great Success!!

Imagine showing up to a CAB meeting with this kind of data!!!!

## Manually deploy or destroy a ContainerLab (clab) topology

> [!NOTE] 
> The clab topology should have been deployed during the step above.
> This is a reference if you want to manually deploy or destroy a topology.

### Deploy a clab topology

option 1: 

Use the `ContainerLab` extension, in the `undeployed local labs` section, expend the file repo file structure under `arista_labs_avd_demo/digital_twin/clab/` and click on three dots next to `topology.clab.yml` and click `Deploy`.  you have to wait until the popup window in the bottom right displays `deploy completed successfilly`

![deploy](./media/sandbox7.png)

Option 2:

In the terminal, run `make deploy_clab_topology`

![deploy2](./media/sandbox8.png)

It will take 5-6 minutes to deploy the lab.

### Destroy a clab topology

option 1:

Use the `ContainerLab` extension,  in the `running labs` section, select the active lab, click on the 3 dots menu and `Destroy (Cleanup)`

![destroy](./media/sandbox6.png)

option 2:

In the terminal, run `make destroy_clab_topology`

![destroy2](./media/sandbox18.png)

### Redeploy the clab topology

If you want to quickly redeploy the clab topology to start fresh, enter `make redeploy_clab_topology` in the terminal
