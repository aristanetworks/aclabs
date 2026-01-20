#!/usr/bin/env python3

# This script can be referenced in .vscode/tasks.json
# It verifies the lab status and shows various important messages to the lab user on start

from rich.theme import Theme
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import paramiko
import yaml
import os
import sys
import time

custom_theme = Theme({"info": "bold cyan", "warning": "magenta", "critical": "bold red"})
console = Console(theme=custom_theme)

console.clear()

# Two blank lines before
console.print("\n\n", end="")

title = Text()
title.append("c", style="grey")
title.append("A", style="red")
title.append("r", style="green")
title.append("L", style="bold cyan")
title.append("\n", style="")

subtitle = Text("   Containerized Arista Labs", style="white")

banner = Text()
banner.append("   ")
banner.append(title)
banner.append(subtitle)

panel = Panel(
    banner,
    border_style="cyan",
    padding=(1, 4),
    expand=False
)

console.print(panel)

# Two blank lines after
console.print("\n\n", end="")

console.print("READ THIS FIRST!", style="critical")
console.print("- check README.md", style="critical")
console.print("- wait until the lab will be ready", style="critical")

# Two blank lines after
console.print("\n\n", end="")

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

    # set the timer to exit after 5 min if some lab devices are still not reachable
    lab_timeout = 300
    timer = time.time() + lab_timeout

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
            if (time.time() > timer) and node_not_reachable:
                console.log(f"ERROR: can not reach some lab nodes. Something is wrong. Breaking after {lab_timeout} seconds. Last node not reachable: {node_name}", style="critical")
                sys.exit(1)

console.log("Lab is ready!")

console.print("Please close any open terminals and init a new one before you start working with the lab!", style="warning")
