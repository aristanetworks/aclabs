#!/usr/bin/env python3
"""Onboard a lab to a running on-prem CloudVision instance."""

import os
import re
import shlex
from dataclasses import dataclass
from pathlib import Path
import requests
import urllib3
import ipaddress
import time
import sys
from typing import Any

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class OnboardingError(RuntimeError):
    """Raised when CloudVision onboarding cannot be completed."""

@dataclass(frozen=True)
class Settings:
    cv_url: str
    username: str
    password: str
    workspace: Path
    login_timeout: int = 1200
    service_account: str = "labs-dot-arista"

    @classmethod
    def from_environment(cls) -> "Settings":
        values = {
            "CVURL": os.environ.get("CVURL", ""),
            "LABUSERNAME": os.environ.get("LABUSERNAME") or "arista",
            "LABPASSPHRASE": os.environ.get("LABPASSPHRASE") or "arista",
            "CONTAINERWSF": os.environ.get("CONTAINERWSF", ""),
        }
        missing = [name for name, value in values.items() if not value]
        if missing:
            raise OnboardingError(
                f"Required environment variable(s) are missing: {', '.join(missing)}"
            )

        try:
            address = ipaddress.ip_address(values["CVURL"])
        except ValueError as error:
            raise OnboardingError(
                "CVURL must be the IPv4 address of an on-prem CVP instance."
            ) from error
        if address.version != 4:
            raise OnboardingError(
                "CVURL must be the IPv4 address of an on-prem CVP instance."
            )

        return cls(
            cv_url=str(address),
            username=values["LABUSERNAME"],
            password=values["LABPASSPHRASE"],
            workspace=Path(values["CONTAINERWSF"]),
        )

class CloudVisionOnboarder:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = f"https://{settings.cv_url}"
        self.session = requests.Session()

    def _post_json(
        self,
        path: str,
        payload: dict[str, Any],
        error_message: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> Any:
        try:
            response = self.session.post(
                f"{self.base_url}{path}",
                json=payload,
                headers=headers,
                timeout=(5, 30),
                verify=False,
            )
            response.raise_for_status()
            data = response.json()
        except requests.HTTPError as error:
            response = error.response
            status = response.status_code if response is not None else "unknown"
            detail = response.text.strip() if response is not None else ""
            if len(detail) > 1000:
                detail = f"{detail[:1000]}..."
            suffix = f" HTTP {status}"
            if detail:
                suffix = f"{suffix}: {detail}"
            raise OnboardingError(f"{error_message}{suffix}") from error
        except requests.RequestException as error:
            raise OnboardingError(f"{error_message} {error}") from error
        except ValueError as error:
            raise OnboardingError(
                f"{error_message} CloudVision returned invalid JSON."
            ) from error

        return data

    def login(self) -> None:
        wait_until = time.monotonic() + self.settings.login_timeout
        payload = {
            "userId": self.settings.username,
            "password": self.settings.password
        }

        print(
            f"Waiting for the CloudVision API at {self.base_url} ...",
            file=sys.stderr,
        )

        while time.monotonic() < wait_until:
            try:
                response = self.session.post(
                    f"{self.base_url}/cvpservice/login/authenticate.do",
                    json=payload,
                    timeout=(2, 6),
                    verify=False,
                )
                response.raise_for_status()
                session_id = response.json().get("sessionId", "")
                if session_id:
                    self.session.cookies.set("access_token", session_id)
                    print("CloudVision login succeeded.", file=sys.stderr)
                    return
            except (requests.RequestException, ValueError, AttributeError):
                pass
            time.sleep(5)

        raise OnboardingError(
            "Not able to login to CloudVision within "
            f"{self.settings.login_timeout} seconds."
        )

    def create_api_token(self) -> str:

        print(
            f"Attempting to create a service account at {self.base_url} ...",
            file=sys.stderr,
        )

        service_account_payload = {
            "key": {"name": self.settings.service_account},
            "status": "ACCOUNT_STATUS_ENABLED",
            "description": "Service account created by lab onboarding logic",
            "groups": {"values": ["network-admin"]},
        }
        self._post_json(
            "/api/resources/serviceaccount/v1/AccountConfig",
            service_account_payload,
            "Failed to create or update the "
            f"'{self.settings.service_account}' CloudVision service account.",
        )

        print(
            "Service account was successfully created. "
            f"Attempting to create a token for the service account at {self.base_url} ...",
            file=sys.stderr,
        )

        token_payload = {
            "user": self.settings.service_account,
            "description": "Service account API token created by lab onboarding logic",
            "validFor": "86400s",
        }
        response_data = self._post_json(
            "/api/resources/serviceaccount/v1/TokenConfig",
            token_payload,
            "Failed to create a CloudVision service-account token.",
        )
        value = response_data.get("value")
        token = value.get("token", "") if isinstance(value, dict) else ""
        if not token:
            raise OnboardingError(
                "CloudVision returned an empty service-account token."
            )

        print(
            "Service account API token was created successfully.",
            file=sys.stderr,
        )

        return token

    def create_onboarding_token(self) -> str:

        print(
            f"Attempting to generate an onboarding token at {self.base_url} ...",
            file=sys.stderr,
        )

        response_data = self._post_json(
            "/api/resources/admin.Enrollment/AddEnrollmentToken",
            {
                "enrollmentToken": {
                    "reenrollDevices": ["*"],
                    "validFor": "86400s",
                }
            },
            "Failed to create a CloudVision device onboarding token.",
        )

        if isinstance(response_data, list) and response_data:
            response_data = response_data[0]

        token = ""
        if isinstance(response_data, dict):
            enrollment_token = response_data.get("enrollmentToken")
            if isinstance(enrollment_token, dict):
                token = enrollment_token.get("token", "")
            if not token:
                token = response_data.get("token", "")

        if not token:
            preview = repr(response_data)
            if len(preview) > 1000:
                preview = f"{preview[:1000]}..."
            raise OnboardingError(
                "Could not extract the device enrollment token from "
                f"CloudVision response: {preview}"
            )

        print(
            "Onboarding token was successfully generated.",
            file=sys.stderr,
        )

        return token

    def write_onboarding_token(self, token: str) -> None:
        token_path = self.settings.workspace / "clab" / "cv-onboarding-token"

        print(
            f"Writing onboarding token to {token_path}.",
            file=sys.stderr,
        )

        try:
            with open(token_path, "w", encoding="utf-8") as token_file:
                token_file.write(f"{token}\n")
        except OSError as error:
            raise OnboardingError(
                f"Failed to write the cEOS onboarding token to {token_path}."
            ) from error

    def write_runtime_environment(self, api_token: str) -> None:
        runtime_path = self.settings.workspace / ".vscode" / "runtime.env"

        print(
            f"Writing runtime environment variables to {runtime_path}.",
            file=sys.stderr,
        )

        try:
            with open(runtime_path, "w", encoding="utf-8") as runtime_file:
                runtime_file.write(
                    f"export CV_API_TOKEN={shlex.quote(api_token)}\n"
                )
        except OSError as error:
            raise OnboardingError(
                f"Failed to write runtime environment variables to {runtime_path}."
            ) from error

        zshrc_path = Path.home() / ".zshrc"
        quoted_runtime_path = shlex.quote(str(runtime_path))
        source_line = (
            f"[[ -f {quoted_runtime_path} ]] && source {quoted_runtime_path}"
        )

        try:
            zshrc = (
                zshrc_path.read_text(encoding="utf-8")
                if zshrc_path.exists()
                else ""
            )
            if source_line not in zshrc.splitlines():
                with open(zshrc_path, "a", encoding="utf-8") as zshrc_file:
                    if zshrc and not zshrc.endswith("\n"):
                        zshrc_file.write("\n")
                    zshrc_file.write(
                        "# Load variables generated by cv_onboard.py.\n"
                        f"{source_line}\n"
                    )
        except (OSError, UnicodeDecodeError) as error:
            raise OnboardingError(
                f"Failed to configure {zshrc_path} to load {runtime_path}."
            ) from error

    def update_startup_configs(self) -> None:

        print(
            "Updating lab startup configs for CloudVision and relayed "
            "lab credentials...",
            file=sys.stderr,
        )

        config_dir = self.settings.workspace / "clab" / "init-configs"
        if not config_dir.is_dir():
            raise OnboardingError(
                f"Missing cEOS bootstrap configuration directory: {config_dir}"
            )

        cv_address = f"-cvaddr={self.settings.cv_url}:9910"
        terminattr_line = re.compile(
            r"^.*\bTerminAttr\b.*-cvaddr=\S+.*$",
            re.MULTILINE,
        )
        credential_line = re.compile(
            rf"^username\s+{re.escape(self.settings.username)}(?:\s+.*)?$",
            re.MULTILINE,
        )
        any_credential_line = re.compile(r"^username\s+.*$", re.MULTILINE)
        no_aaa_root_line = re.compile(r"^no aaa root\s*$", re.MULTILINE)
        desired_credential_line = (
            "username "
            f"{self.settings.username} privilege 15 role network-admin "
            f"secret {self.settings.password}"
        )
        terminattr_files = 0

        def update_line(match: re.Match[str]) -> str:
            line = re.sub(
                r"-cvaddr=\S+",
                cv_address,
                match.group(0),
                count=1,
            )
            return line.replace("token-secure,", "token,")

        for config_path in config_dir.glob("*.cfg"):

            try:
                config = config_path.read_text(encoding="utf-8")
            except UnicodeDecodeError as error:
                raise OnboardingError(
                    f"Bootstrap configuration {config_path} is not valid UTF-8."
                ) from error
            except OSError as error:
                raise OnboardingError(
                    f"Failed to read bootstrap configuration {config_path}."
                ) from error

            config, terminattr_replacements = terminattr_line.subn(
                update_line,
                config,
            )
            config, credential_replacements = credential_line.subn(
                lambda _: desired_credential_line,
                config,
                count=1,
            )
            if credential_replacements == 0:
                existing_credential = any_credential_line.search(config)
                if existing_credential:
                    position = existing_credential.start()
                    config = (
                        config[:position]
                        + f"{desired_credential_line}\n"
                        + config[position:]
                    )
                else:
                    no_aaa_root = no_aaa_root_line.search(config)
                    if no_aaa_root:
                        position = no_aaa_root.end()
                        config = (
                            config[:position]
                            + f"\n!\n{desired_credential_line}"
                            + config[position:]
                        )
                    else:
                        config = f"{desired_credential_line}\n{config}"

            try:
                with open(config_path, "w", encoding="utf-8") as config_file:
                    config_file.write(config)
            except OSError as error:
                raise OnboardingError(
                    f"Failed to update bootstrap configuration {config_path}."
                ) from error
            if terminattr_replacements:
                terminattr_files += 1

        if terminattr_files == 0:
            raise OnboardingError(
                f"No TerminAttr configuration with -cvaddr was found in {config_dir}."
            )

    def onboard(self) -> None:
        self.login()
        api_token = self.create_api_token()
        onboarding_token = self.create_onboarding_token()
        self.write_onboarding_token(onboarding_token)
        self.update_startup_configs()
        self.write_runtime_environment(api_token)
        print(
            "CloudVision onboarding data is ready; cEOS-lab will stream to "
            f"{self.settings.cv_url}:9910.",
            file=sys.stderr,
        )

def main() -> int:
    try:
        CloudVisionOnboarder(Settings.from_environment()).onboard()
    except OnboardingError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
