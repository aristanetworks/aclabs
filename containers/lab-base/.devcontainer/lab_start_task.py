#!/usr/bin/env python3

# This script can be referenced in .vscode/tasks.json
# It verifies the lab status and shows various important messages to the lab user on start

from rich.theme import Theme
from rich.console import Console
from rich.progress import Progress
import paramiko
import yaml
import os
import time

custom_theme = Theme({"info": "bold cyan", "warning": "magenta", "critical": "bold red"})
console = Console(theme=custom_theme)

console.clear()

console.print("READ THIS FIRST!", style="critical")
console.print("- check README.md", style="critical")
console.print("- wait until the lab will be ready", style="critical")

time.sleep(5)  # give some time for user to read the message =)

console.log("Starting the lab...")

console.log("Loading the list of lab nodes...")
try:
    container_workspace = os.getenv("CONTAINERWSF")
    with open(f"{container_workspace}/clab/topology.clab.yml", "r") as f:
        d = yaml.safe_load(f)
except:
    console.log("Failed to load the lab topology.")

with console.status(
    "Please wait - waiting for lab nodes to come up...", spinner="shark"
):

    lab_node_list = [ node_name for node_name in d['topology']['nodes'].keys() ]

    for node_name in lab_node_list:
        node_not_reachable = True
        while node_not_reachable:
            try:
                lab_username = os.getenv("LABUSERNAME", default="arista")
                lab_password = os.getenv("LABPASSPHRASE", default="arista")
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=node_name, username=lab_username, password=lab_password, timeout=1)
                stdin,stdout,stderr=ssh.exec_command("pwd")
                for out_string in stdout:
                    # we can think of a better check in future
                    # but searching for / in pwd out works and it is consistent for EOS and Linux
                    if '/' in out_string:
                        node_not_reachable = False
                ssh.close()
            except Exception as _:
                pass  # ignore if node is down

console.log("Lab is ready!")

console.print("Please close any open terminals and init a new one before you start working with the lab!", style="warning")
