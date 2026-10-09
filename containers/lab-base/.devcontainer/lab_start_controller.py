#!/usr/bin/env python3
"""Run lab initialization asynchronously and publish progress for VS Code."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Empty, Queue
from threading import Thread
import fcntl
import ipaddress
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from typing import Any

import paramiko
import requests # TODO: change controller architecture and remove
import urllib3 # TODO: change controller architecture and remove
import yaml

# TODO: change controller architecture and remove
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


STATE_DIR = Path("/tmp/aclabs-lab-start")
STATE_PATH = STATE_DIR / "state.json"
LOCK_PATH = STATE_DIR / "startup.lock"
CVP_URL_PLACEHOLDER = "{{aclabs.cvp_url}}"
LAB_USERNAME_PLACEHOLDER = "{{aclabs.lab_username}}"
LAB_PASSWORD_PLACEHOLDER = "{{aclabs.lab_password}}"
CVP_WAITING_LINE_PREFIX = "Waiting for the CloudVision API at "
CVP_LOGIN_SUCCEEDED = "CloudVision login succeeded."
CVP_ONBOARD_TIMEOUT_SECONDS = 1380
LAB_START_TIMEOUT_SECONDS = 600
DEVICE_READY_TIMEOUT_SECONDS = 300
DEVICE_POLL_INTERVAL_SECONDS = 5
STREAMING_READY_TIMEOUT_SECONDS = 300 # TODO: change controller architecture and remove
DEVICE_USERNAME = os.environ.get("LABUSERNAME") or "arista"
DEVICE_PASSWORD = os.environ.get("LABPASSPHRASE") or "arista"


class LabStartError(RuntimeError):
    """Raised when automatic lab startup cannot be completed."""


def environment_flag(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def cloudvision_onboarding_enabled() -> bool:
    try:
        return ipaddress.ip_address(os.environ.get("CVURL", "")).version == 4
    except ValueError:
        return False


def update_readme_with_cvp_url(workspace: Path) -> None:
    coder_url = os.environ.get("CODER_URL", "").strip().rstrip("/")
    if not coder_url:
        return

    cvp_url = coder_url.replace("coder", "cvp", 1)
    if "://" not in cvp_url:
        cvp_url = f"https://{cvp_url}"

    readme_path = workspace / "README.md"
    try:
        readme = readme_path.read_text(encoding="utf-8")
        readme_path.write_text(
            readme.replace(CVP_URL_PLACEHOLDER, cvp_url),
            encoding="utf-8",
        )
    except OSError as error:
        raise LabStartError(f"Failed to update {readme_path}.") from error


def update_readme_with_lab_credentials(workspace: Path) -> None:
    readme_path = workspace / "README.md"
    try:
        readme = readme_path.read_text(encoding="utf-8")
        readme = readme.replace(
            LAB_USERNAME_PLACEHOLDER,
            DEVICE_USERNAME,
        )
        readme = readme.replace(
            LAB_PASSWORD_PLACEHOLDER,
            DEVICE_PASSWORD,
        )
        readme_path.write_text(readme, encoding="utf-8")
    except OSError as error:
        raise LabStartError(f"Failed to update {readme_path}.") from error


def write_state(
    status: str,
    message: str,
    *,
    log_message: bool = True,
) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    temporary_path = STATE_PATH.with_suffix(".tmp")
    data = {
        "status": status,
        "message": message,
        "updated_at": time.time(),
    }
    temporary_path.write_text(json.dumps(data), encoding="utf-8")
    temporary_path.replace(STATE_PATH)
    if log_message:
        print(message, flush=True)


def existing_status() -> str:
    try:
        data: Any = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    return data.get("status", "") if isinstance(data, dict) else ""


def run_command(
    command: list[str],
    *,
    cwd: Path,
    timeout: int,
    error_message: str,
    suppress_output: bool = False,
) -> None:
    try:
        subprocess.run(
            command,
            cwd=cwd,
            check=True,
            timeout=timeout,
            stdout=subprocess.DEVNULL if suppress_output else None,
            stderr=subprocess.DEVNULL if suppress_output else None,
        )
    except subprocess.TimeoutExpired as error:
        raise LabStartError(
            f"{error_message} Timed out after {timeout} seconds."
        ) from error
    except subprocess.CalledProcessError as error:
        raise LabStartError(
            f"{error_message} Command exited with status {error.returncode}."
        ) from error


def run_cloudvision_onboarding(workspace: Path) -> None:
    process = subprocess.Popen(
        ["/bin/cv_onboard.py"],
        cwd=workspace,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    if process.stdout is None:
        process.kill()
        raise LabStartError("Failed to capture CloudVision onboarding output.")

    output_queue: Queue[str | None] = Queue()

    def read_output() -> None:
        try:
            for line in process.stdout:
                output_queue.put(line)
        finally:
            output_queue.put(None)

    Thread(target=read_output, daemon=True).start()
    deadline = time.monotonic() + CVP_ONBOARD_TIMEOUT_SECONDS
    login_reported = False

    try:
        output_open = True
        while output_open:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise subprocess.TimeoutExpired(
                    process.args,
                    CVP_ONBOARD_TIMEOUT_SECONDS,
                )
            try:
                line = output_queue.get(timeout=min(0.5, remaining))
            except Empty:
                continue
            if line is None:
                output_open = False
                continue

            message = line.strip()
            if message.startswith(CVP_WAITING_LINE_PREFIX):
                continue
            if message == CVP_LOGIN_SUCCEEDED:
                write_state(
                    "ONBOARDING",
                    "CloudVision API responded; preparing onboarding data...",
                    log_message=False,
                )
                login_reported = True
            print(line, end="", flush=True)

        return_code = process.wait(
            timeout=max(0.1, deadline - time.monotonic())
        )
    except subprocess.TimeoutExpired as error:
        process.kill()
        process.wait()
        raise LabStartError(
            "CloudVision onboarding failed. "
            f"Timed out after {CVP_ONBOARD_TIMEOUT_SECONDS} seconds."
        ) from error

    if return_code != 0:
        raise LabStartError(
            "CloudVision onboarding failed. "
            f"Command exited with status {return_code}."
        )
    if not login_reported:
        write_state(
            "ONBOARDING",
            "CloudVision API responded; preparing onboarding data...",
            log_message=False,
        )


def container_engine() -> str:
    for command in ("podman", "docker"):
        if shutil.which(command):
            return command
    raise LabStartError("Failed to find docker or podman.")


def verify_ceos_image(workspace: Path) -> None:
    engine = container_engine()
    result = subprocess.run(
        [engine, "image", "inspect", "arista/ceos:latest"],
        cwd=workspace,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        raise LabStartError(
            "The arista/ceos:latest image is unavailable. "
            "Import the image and run lab_start_controller.py --force."
        )


def onboard_cloudvision(workspace: Path) -> None:
    if not cloudvision_onboarding_enabled():
        return

    update_readme_with_cvp_url(workspace)
    cv_address = os.environ.get("CVURL", "")
    base_url = f"https://{cv_address}"
    write_state(
        "CVP_WAITING",
        f"Waiting for the CloudVision API at {base_url} ...",
        log_message=False,
    )
    run_cloudvision_onboarding(workspace)


def commit_onboarding_changes(workspace: Path) -> None:
    if not cloudvision_onboarding_enabled() or not environment_flag("GIT_INIT"):
        return

    repository = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=workspace,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if repository.returncode != 0:
        return

    subprocess.run(
        ["git", "add", "-u", "--", "clab/init-configs", "README.md"],
        cwd=workspace,
        check=True,
    )
    changes = subprocess.run(
        ["git", "diff", "--cached", "--quiet", "--", "clab/init-configs", "README.md"],
        cwd=workspace,
        check=False,
    )
    if changes.returncode == 0:
        return
    if changes.returncode != 1:
        raise LabStartError("Failed to inspect generated onboarding changes.")

    run_command(
        ["git", "commit", "-m", "Configure lab for on-prem CloudVision"],
        cwd=workspace,
        timeout=60,
        error_message="Failed to commit generated onboarding changes.",
    )


def topology_nodes(workspace: Path) -> list[str]:
    topology_path = workspace / "clab" / "topology.clab.yml"
    try:
        with open(topology_path, "r", encoding="utf-8") as topology_file:
            topology: Any = yaml.safe_load(topology_file)
        nodes = topology["topology"]["nodes"]
    except (OSError, TypeError, KeyError, yaml.YAMLError) as error:
        raise LabStartError(
            f"Failed to load lab nodes from {topology_path}."
        ) from error

    if not isinstance(nodes, dict) or not nodes:
        raise LabStartError(f"No lab nodes were found in {topology_path}.")
    return list(nodes)


def node_is_ready(node: str, username: str, password: str) -> bool:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            hostname=node,
            username=username,
            password=password,
            timeout=3,
            banner_timeout=3,
            auth_timeout=3,
            look_for_keys=False,
            allow_agent=False,
        )
        _, stdout, _ = client.exec_command("pwd", timeout=3)
        return "/" in stdout.read().decode(errors="replace")
    except Exception:
        return False
    finally:
        client.close()


def wait_for_nodes(workspace: Path) -> None:
    nodes = topology_nodes(workspace)
    deadline = time.monotonic() + DEVICE_READY_TIMEOUT_SECONDS
    unavailable = nodes

    write_state("VERIFYING", "Lab deployed; waiting for devices to accept SSH...")
    with ThreadPoolExecutor(max_workers=min(len(nodes), 10)) as executor:
        while time.monotonic() < deadline:
            futures = {
                executor.submit(
                    node_is_ready,
                    node,
                    DEVICE_USERNAME,
                    DEVICE_PASSWORD,
                ): node
                for node in unavailable
            }
            unavailable = [
                futures[future]
                for future in as_completed(futures)
                if not future.result()
            ]
            if not unavailable:
                return
            print(
                "Waiting for devices: " + ", ".join(sorted(unavailable)),
                flush=True,
            )
            time.sleep(DEVICE_POLL_INTERVAL_SECONDS)

    raise LabStartError(
        "Devices did not become ready within "
        f"{DEVICE_READY_TIMEOUT_SECONDS} seconds: "
        + ", ".join(sorted(unavailable))
    )

# TODO: change controller architecture and remove
def cloudvision_session(base_url: str) -> requests.Session:
    session = requests.Session()
    response = session.post(
        f"{base_url}/cvpservice/login/authenticate.do",
        json={
            "userId": DEVICE_USERNAME,
            "password": DEVICE_PASSWORD,
        },
        timeout=(2, 6),
        verify=False,
    )
    response.raise_for_status()
    session_id = response.json().get("sessionId", "")
    if not session_id:
        raise ValueError("CloudVision login response did not contain a session ID.")
    session.cookies.set("access_token", session_id)
    return session

# TODO: change controller architecture and remove
def active_streaming_hostnames(
    session: requests.Session,
    base_url: str,
) -> set[str]:
    response = session.get(
        f"{base_url}/cvpservice/inventory/devices",
        headers={"accept": "application/json"},
        timeout=(2, 6),
        verify=False,
    )
    response.raise_for_status()
    devices = response.json()
    if not isinstance(devices, list):
        raise ValueError("CloudVision inventory response is not a list.")

    return {
        device["hostname"]
        for device in devices
        if isinstance(device, dict)
        and isinstance(device.get("hostname"), str)
        and device.get("streamingStatus") == "active"
    }

# TODO: change controller architecture and remove
def wait_for_cloudvision_streaming(workspace: Path) -> None:
    if not cloudvision_onboarding_enabled():
        return

    topology_hostnames = set(topology_nodes(workspace))
    base_url = f"https://{os.environ['CVURL']}"
    deadline = time.monotonic() + STREAMING_READY_TIMEOUT_SECONDS
    session: requests.Session | None = None

    write_state(
        "VERIFYING",
        "Devices are reachable; waiting for CloudVision streaming...",
    )
    while time.monotonic() < deadline:
        try:
            if session is None:
                session = cloudvision_session(base_url)
            streaming_hostnames = active_streaming_hostnames(session, base_url)
            lab_streaming_hostnames = topology_hostnames & streaming_hostnames
            if lab_streaming_hostnames:
                print(
                    "CloudVision streaming is active for lab device(s): "
                    + ", ".join(sorted(lab_streaming_hostnames)),
                    flush=True,
                )
                return
        except (requests.RequestException, ValueError, AttributeError):
            session = None

        time.sleep(DEVICE_POLL_INTERVAL_SECONDS)

    raise LabStartError(
        "No device from the containerlab topology reported active CloudVision "
        f"streaming within {STREAMING_READY_TIMEOUT_SECONDS} seconds: "
        + ", ".join(sorted(topology_hostnames))
    )


def start_lab(workspace: Path) -> None:
    write_state("DEPLOYING", "Startup prerequisites are ready; starting the lab...")
    run_command(
        ["make", "start"],
        cwd=workspace,
        timeout=LAB_START_TIMEOUT_SECONDS,
        error_message="Lab deployment failed.",
        # we don't want to see the noise from cLab start under normal conditions
        suppress_output=True,
    )


def main() -> int:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOCK_PATH, "w", encoding="utf-8") as lock_file:
        try:
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("Lab startup is already running.", flush=True)
            return 0

        if existing_status() == "READY" and "--force" not in sys.argv[1:]:
            print("Lab is already ready.", flush=True)
            return 0

        try:
            workspace_value = os.environ.get("CONTAINERWSF", "")
            if not workspace_value:
                raise LabStartError("CONTAINERWSF is not set.")
            workspace = Path(workspace_value)
            if not workspace.is_dir():
                raise LabStartError(f"Workspace does not exist: {workspace}")

            write_state("STARTING", "Automatic lab startup has begun.")
            verify_ceos_image(workspace)
            update_readme_with_lab_credentials(workspace)
            onboard_cloudvision(workspace)
            commit_onboarding_changes(workspace)
            start_lab(workspace)
            wait_for_nodes(workspace)
            wait_for_cloudvision_streaming(workspace)
            write_state("READY", "Lab is ready!")
            return 0
        except (LabStartError, OSError, subprocess.SubprocessError) as error:
            write_state("FAILED", f"ERROR: {error}")
            return 1


if __name__ == "__main__":
    raise SystemExit(main())
