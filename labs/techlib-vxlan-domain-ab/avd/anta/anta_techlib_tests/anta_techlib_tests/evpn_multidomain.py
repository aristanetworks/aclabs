"""Custom ANTA tests — EVPN multi-domain (techlib-vxlan-domain-ab).

Three tests the stock library cannot express:

* VerifyEVPNType4Routes  — ES (Type-4) route presence. With `identifier
  auto lacp` there is no static ES-Import RT, so seeing the PEER's Type-4
  route proves the af-evpn `route type ethernet-segment route-target auto`
  machinery is importing (the Day 54 s6 functional patch).
* VerifyEVPNDFElection   — designated-forwarder expectation per interface.
* VerifyEVPNDPath        — D-PATH domain identifiers on routes that crossed
  the domain boundary.

MOCK-VERIFIED: the parsing targets the documented shapes below; the first
live run may require shape adjustment (flagged inline where EOS JSON is
reconstructed from operational experience rather than captured output).
"""
from __future__ import annotations

from anta.models import AntaCommand, AntaTemplate, AntaTest


class VerifyEVPNType4Routes(AntaTest):
    """Expect at least `minimum` EVPN Type-4 (Ethernet Segment) routes.

    For a two-member all-active ES, `minimum: 2` proves the peer's ES route
    was IMPORTED (the local route is always present) — i.e. auto ES-Import
    RT derivation is working end to end.
    """

    categories = ["evpn", "multihoming"]
    commands = [AntaCommand(command="show bgp evpn route-type ethernet-segment", revision=2)]

    class Input(AntaTest.Input):
        minimum: int = 2
        esis: list[str] = []
        """Optional ESI substrings that must each appear in at least one route key."""

    @AntaTest.anta_test
    def test(self) -> None:
        out = self.instance_commands[0].json_output
        routes = out.get("vrfs", {}).get("default", {}).get("evpnRoutes", {})
        count = len(routes)
        if count < self.inputs.minimum:
            self.result.is_failure(f"Type-4 routes: {count} < minimum {self.inputs.minimum} — peer ES route not imported (check es-rt-auto)")
            return
        missing = [e for e in self.inputs.esis if not any(e in k for k in routes)]
        if missing:
            self.result.is_failure(f"Type-4 routes missing expected ESI(s): {missing}")
            return
        self.result.is_success()


class VerifyEVPNDFElection(AntaTest):
    """Assert this device's DF verdict for one ES-bearing interface.

    SHAPE NOTE: parses `show evpn ethernet-segment` — segments keyed by ESI
    with `esiInterface` and a boolean `designatedForwarder` (reconstructed
    shape; adjust on first live capture if EOS differs).
    """

    categories = ["evpn", "multihoming"]
    commands = [AntaCommand(command="show evpn ethernet-segment", revision=1)]

    class Input(AntaTest.Input):
        interface: str
        expect_df: bool

    @AntaTest.anta_test
    def test(self) -> None:
        out = self.instance_commands[0].json_output
        segs = out.get("ethernetSegments", {}) or out.get("segments", {})
        match = next((s for s in segs.values() if s.get("esiInterface") == self.inputs.interface), None)
        if match is None:
            self.result.is_failure(f"No Ethernet Segment found on {self.inputs.interface}")
            return
        df = bool(match.get("designatedForwarder", False))
        if df is not self.inputs.expect_df:
            self.result.is_failure(f"{self.inputs.interface}: designatedForwarder={df}, expected {self.inputs.expect_df}")
            return
        self.result.is_success()


class VerifyEVPNDPath(AntaTest):
    """Assert D-PATH domain identifiers on a boundary-crossing prefix.

    SHAPE NOTE: parses `show bgp evpn route-type ip-prefix {prefix} detail`;
    expects path entries carrying `dPath.domains[].id` (reconstructed shape).
    """

    categories = ["evpn", "gateway"]

    class Input(AntaTest.Input):
        prefix: str
        expected_domains: list[str]

    @staticmethod
    def _templates() -> list[AntaTemplate]:
        return [AntaTemplate(template="show bgp evpn route-type ip-prefix {prefix} detail", revision=2)]

    commands = _templates()

    def render(self, template: AntaTemplate) -> list[AntaCommand]:
        return [template.render(prefix=self.inputs.prefix)]

    @AntaTest.anta_test
    def test(self) -> None:
        out = self.instance_commands[0].json_output
        routes = out.get("vrfs", {}).get("default", {}).get("evpnRoutes", {})
        seen: set[str] = set()
        for r in routes.values():
            for p in r.get("evpnRoutePaths", []):
                for d in p.get("dPath", {}).get("domains", []):
                    if "id" in d:
                        seen.add(d["id"])
        missing = [d for d in self.inputs.expected_domains if d not in seen]
        if missing:
            self.result.is_failure(f"{self.inputs.prefix}: D-PATH missing domain id(s) {missing}; saw {sorted(seen)}")
            return
        self.result.is_success()
