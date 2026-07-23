"""Custom ANTA test — OISM MLD snooping state (no stock equivalent)."""
from __future__ import annotations

from anta.models import AntaCommand, AntaTest


class VerifyMldSnoopingVlans(AntaTest):
    """MLD snooping globally enabled with at least `minimum_vlans` member VLANs.

    SHAPE NOTE: parses `show mld snooping` — `globalEnabled` bool + `vlans`
    dict (reconstructed shape; adjust on first live capture).
    """

    categories = ["multicast", "oism"]
    commands = [AntaCommand(command="show mld snooping", revision=1)]

    class Input(AntaTest.Input):
        minimum_vlans: int = 2

    @AntaTest.anta_test
    def test(self) -> None:
        out = self.instance_commands[0].json_output
        if not out.get("globalEnabled", False):
            self.result.is_failure("MLD snooping globally disabled")
            return
        n = len(out.get("vlans", {}))
        if n < self.inputs.minimum_vlans:
            self.result.is_failure(f"MLD snooping member VLANs: {n} < minimum {self.inputs.minimum_vlans}")
            return
        self.result.is_success()
