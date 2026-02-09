#!/usr/bin/env python3

from textual.app import App, ComposeResult
from textual.widgets import ListView, ListItem, Label, Header, Input
from textual.containers import Vertical
from rich.console import Console
from rich.theme import Theme
import requests
import tarfile
import os
import subprocess
import sys
import shutil
import time
from types import SimpleNamespace
import json

class SingleChoiceUI(App):

    CSS = """
    ListView {
        height: auto;
        width: 40;
        border: round white;
    }
    Header {
        text-align: left;
    }
    """

    def on_mount(self) -> None:
        self.theme = "nord"

    def __init__(
            self,
            # list of options to pick from
            options: list[str],
            # a message to the user to be displayed above the choice list
            label="Please select a single option from the list",
            # app frame decorations
            title="",
            show_clock=True,
            icon="🧩"
        ):
        super().__init__()
        self.options = options
        self.label = label
        self.title = title
        self.show_clock = show_clock
        self.icon = icon

    def compose(self) -> ComposeResult:
        yield Vertical(
            Header(show_clock=self.show_clock, icon=self.icon),
            Label(self.label),
            ListView(
                *[ListItem(Label(option)) for option in self.options]
            )
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected = event.item.query_one(Label).render()
        self.exit(result=selected)

class SimpleInputUI(App):

    CSS = """
    Vertical {
        padding: 2;
    }
    """

    def on_mount(self) -> None:
        self.theme = "nord"

    def __init__(
            self,
            input_fields = [
                {
                    # a message to the user to be displayed above the input field
                    "label": "Please provide your input and press the Enter button",
                    # id used to identify user input data in the code
                    "id": "user_input_value",
                    # a text to be displayed inside the input field
                    "placeholder": "Type your input here...",
                    # default value, if provided - it will override the placeholder
                    "default_value": ""
                }
            ]
        ):
        super().__init__()
        self.input_fields = input_fields

    def compose(self) -> ComposeResult:
        with Vertical():
            for field in self.input_fields:
                yield Label(field['label'])
                yield Input(
                    id=field['id'],
                    placeholder=field['placeholder'],
                    value=field['default_value']
                )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        result_dict = {
            field["id"]: getattr(self.query_one(f"#{field['id']}"), "value") for field in self.input_fields
        }
        self.exit(result=result_dict)

def get_gh_api(url, timeout=180):
    """
    Simple function to get JSON data from GitHub API with pagination
    """
    response_data_combined = list()
    while True:
        response = requests.get(url=url, timeout=45)
        response_data = response.json()
        if isinstance(response_data, list) and response_data:
            response_data_combined.extend(response_data)
        else:
            # if it's a dictionary - simply return it as a result
            response_data_combined = response_data
        # get next url to load
        url = response.links.get("next", {}).get("url")
        # break if that was the final page
        if not url:
            break
    return response_data_combined

if __name__ == "__main__":

    valid_choice = False

    while not valid_choice:

        custom_theme = Theme({"info": "bold cyan", "warning": "magenta", "critical": "bold red"})
        console = Console(theme=custom_theme, log_path=False)
        console.clear()
        console.print("\n\n", end="")

        avd_release_list = list()

        with console.status(
            "Loading the list of available AVD releases from GitHub API... Please wait.", spinner="earth"
        ):
            gh_org = "aristanetworks"
            gh_repo = "avd"
            avd_release_data = get_gh_api(f"https://api.github.com/repos/{gh_org}/{gh_repo}/releases?per_page=100")

            for release in avd_release_data:
                if release['draft'] == False:
                    avd_release_dict = {
                        'tag_name': release['tag_name'],
                        'tarball_url': release['tarball_url'],
                        'prerelease': release['prerelease']
                    }
                    avd_release_list.append(avd_release_dict)

        avd_version = SimpleNamespace()

        avd_version.choices_available = [ avd_release['tag_name'] for avd_release in avd_release_list if avd_release['prerelease'] == False][:10]
        avd_version.choices_available.append("Another AVD release, not listed above")
        avd_version.choices_available.append("I want to use a specific AVD fork")
        avd_version.selector_app = SingleChoiceUI(
            avd_version.choices_available,
            label="What AVD version do you want to use?",
            title="Build Your Lab"
        )
        # present a simple UI to the user to pick a single AVD version
        avd_version.choice_selected = avd_version.selector_app.run()

        # if user wants another version - display a simple UI to enter it manually
        if avd_version.choice_selected == "Another AVD release, not listed above":
            avd_version.another_version_app = SimpleInputUI(
                input_fields=[
                    {
                        "id": "avd_version",
                        "label": "Please provide the AVD version string in vX.X.X format and press the Enter button",
                        "placeholder": "Enter AVD version string in this field... Example: v5.7.2",
                        "default_value": "devel"
                    }
                ]
            )
            user_input = avd_version.another_version_app.run()

            if user_input['avd_version'] not in [ avd_release['tag_name'] for avd_release in avd_release_list] + ["devel"]:
                sys.exit(f"ERROR: {user_input['avd_version']} is not a valid AVD version. Can't find it in the release list.")

            # change user input if devel is selected
            if user_input['avd_version'] == 'devel':
                user_input = {
                    "gh_org": "aristanetworks",
                    "gh_repo": "avd",
                    "gh_branch": "devel"
                }

        elif avd_version.choice_selected == "I want to use a specific AVD fork":
            avd_version.another_version_app = SimpleInputUI(
                input_fields=[
                    {
                        "id": "gh_org",
                        "label": "Please enter the Github org or user name for the fork you want to use",
                        "placeholder": "Example: ClausHolbechArista for github.com/ClausHolbechArista/avd",
                        "default_value": "aristanetworks"
                    },
                    {
                        "id": "gh_repo",
                        "label": "Please enter the Github repository name for the fork you want to use. Expected to be 'avd'",
                        "placeholder": "Example: avd for https://github.com/gmuloc/avd",
                        "default_value": "avd"
                    },
                    {
                        "id": "gh_branch",
                        "label": "Please enter the Github branch for the fork you want to use",
                        "placeholder": "Example: docs/avd-usage-guide for https://github.com/gmuloc/avd/tree/docs/avd-usage-guide",
                        "default_value": "devel"
                    },
                ]
            )
            user_input = avd_version.another_version_app.run()

        else:
            user_input = {
                'avd_version': avd_version.choice_selected
            }

        console.clear()
        console.print("\n\n", end="")
        with console.status(
            "Downloading the AVD archive... Please wait.", spinner="earth"
        ):

            # if user selected a normal or dev release - download release archive from github
            if 'avd_version' in user_input.keys():
                # download archive
                for avd_release in avd_release_list:
                    if avd_release['tag_name'] == user_input['avd_version']:
                        tarball_url = avd_release['tarball_url']
                        break
                tarball_stream = requests.get(tarball_url, stream=True)
                with open('/tmp/avd_release.tar.gz', "wb") as avd_tar_gz:
                    for chunk in tarball_stream.iter_content(chunk_size=8192):
                        if chunk:
                            avd_tar_gz.write(chunk)

            elif all(key in user_input.keys() for key in ['gh_org', 'gh_repo', 'gh_branch']):
                # download archive
                tarball_stream = requests.get(
                    f"https://github.com/{user_input['gh_org']}/{user_input['gh_repo']}/archive/refs/heads/{user_input['gh_branch']}.tar.gz",
                    stream=True
                )
                with open('/tmp/avd_release.tar.gz', "wb") as avd_tar_gz:
                    for chunk in tarball_stream.iter_content(chunk_size=8192):
                        if chunk:
                            avd_tar_gz.write(chunk)

            # extract archive
            # TODO: check that archive is present first
            with tarfile.open('/tmp/avd_release.tar.gz', 'r:gz') as tar:
                archive_name = tar.getmembers()[0].name
                print(archive_name)
                tar.extractall(path="/tmp")
                example_list = os.listdir(f"/tmp/{archive_name}/ansible_collections/arista/avd/examples")

        # ask user to select AVD example
        avd_example_choice_app = SingleChoiceUI(
            example_list,
            label="Select AVD example inventory",
            title="Build Your Lab"
        )
        example_selected = avd_example_choice_app.run()

        # start over if there is no lab topology defined
        if not os.path.isfile(f"/tmp/{archive_name}/ansible_collections/arista/avd/examples/{example_selected}/clab/topology.clab.yml"):
            console.clear()
            console.print("\n\n", end="")
            console.print("WARNING: There is no lab topology defined for selected AVD version and example.", style="warning")
            console.print("Please try another AVD version or example that supports integration with labs.arista.com", style="warning")
            time.sleep(3)
            # sys.exit()
        else:
            valid_choice = True

    workspace_dir = os.environ['CONTAINERWSF']

    # deactivate the task to avoid running them again on browser refresh
    with open(f'{workspace_dir}/.vscode/tasks.json', 'r') as tasks_json:
        lab_tasks = json.load(tasks_json)
    for task in lab_tasks['tasks']:
        if 'lab_selector' in task['command']:
            task['runOptions']['runOn'] = 'default'
    with open(f'{workspace_dir}/.vscode/tasks.json', 'w') as tasks_json:
        json.dump(lab_tasks, tasks_json, indent=4)

    shutil.copytree(f"/tmp/{archive_name}/ansible_collections/arista/avd/examples/{example_selected}", f"{workspace_dir}", dirs_exist_ok=True)

    subprocess.run([
        'pip', 'install',
        f'/tmp/{archive_name}/python-avd[ansible]'
    ], check=True)

    subprocess.run([
        'ansible-galaxy',
        'collection', 'install', '--force',
        f'/tmp/{archive_name}/ansible_collections/arista/avd'
    ])
