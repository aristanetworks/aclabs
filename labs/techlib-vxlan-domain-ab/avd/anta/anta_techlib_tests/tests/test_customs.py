"""Mock-verified unit tests for the techlib custom ANTA tests.

Pattern: instantiate each AntaTest with a throwaway device and injected
`eos_data`, run the coroutine, assert the result verdict + message.
"""
import asyncio

import pytest
from anta.device import AsyncEOSDevice

from anta_techlib_tests.evpn_multidomain import (
    VerifyEVPNDFElection,
    VerifyEVPNDPath,
    VerifyEVPNType4Routes,
)
from anta_techlib_tests.oism import VerifyMldSnoopingVlans

DEV = AsyncEOSDevice(name="mock", host="127.0.0.1", username="x", password="x")


def run(test_cls, inputs, eos_data):
    t = test_cls(DEV, inputs=inputs, eos_data=eos_data)
    asyncio.run(t.test())
    return t.result


T4_TWO = {"vrfs": {"default": {"evpnRoutes": {
    "RD: 10.0.2.1:1 ethernet-segment 0000:aaaa:1111:2222:0001": {},
    "RD: 10.0.2.2:1 ethernet-segment 0000:aaaa:1111:2222:0001": {},
}}}}
T4_ONE = {"vrfs": {"default": {"evpnRoutes": {
    "RD: 10.0.2.1:1 ethernet-segment 0000:aaaa:1111:2222:0001": {},
}}}}


def test_type4_pass():
    r = run(VerifyEVPNType4Routes, {"minimum": 2}, [T4_TWO])
    assert r.result == "success"


def test_type4_fail_import_broken():
    r = run(VerifyEVPNType4Routes, {"minimum": 2}, [T4_ONE])
    assert r.result == "failure"
    assert "es-rt-auto" in r.messages[0]


def test_type4_esi_substring():
    r = run(VerifyEVPNType4Routes, {"minimum": 1, "esis": ["dead:beef"]}, [T4_ONE])
    assert r.result == "failure" and "dead:beef" in r.messages[0]


ES_DF = {"ethernetSegments": {"0000:bbbb:0007:0008:0000": {
    "esiInterface": "Port-Channel9", "designatedForwarder": True}}}
ES_NDF = {"ethernetSegments": {"0000:bbbb:0007:0008:0000": {
    "esiInterface": "Port-Channel9", "designatedForwarder": False}}}


def test_df_pass_primary():
    r = run(VerifyEVPNDFElection, {"interface": "Port-Channel9", "expect_df": True}, [ES_DF])
    assert r.result == "success"


def test_df_fail_wrong_winner():
    r = run(VerifyEVPNDFElection, {"interface": "Port-Channel9", "expect_df": True}, [ES_NDF])
    assert r.result == "failure"


def test_df_fail_no_segment():
    r = run(VerifyEVPNDFElection, {"interface": "Port-Channel1", "expect_df": True}, [ES_DF])
    assert r.result == "failure" and "No Ethernet Segment" in r.messages[0]


DPATH = {"vrfs": {"default": {"evpnRoutes": {"r1": {"evpnRoutePaths": [
    {"dPath": {"domains": [{"id": "99:99"}, {"id": "1:1"}]}}]}}}}}


def test_dpath_pass():
    r = run(VerifyEVPNDPath, {"prefix": "10.10.10.0/24", "expected_domains": ["99:99"]}, [DPATH])
    assert r.result == "success"


def test_dpath_fail_missing_domain():
    r = run(VerifyEVPNDPath, {"prefix": "10.10.10.0/24", "expected_domains": ["2:2"]}, [DPATH])
    assert r.result == "failure" and "2:2" in r.messages[0]


MLD_OK = {"globalEnabled": True, "vlans": {"10": {}, "30": {}}}
MLD_OFF = {"globalEnabled": False, "vlans": {}}


def test_mld_pass():
    r = run(VerifyMldSnoopingVlans, {"minimum_vlans": 2}, [MLD_OK])
    assert r.result == "success"


def test_mld_fail_disabled():
    r = run(VerifyMldSnoopingVlans, {"minimum_vlans": 2}, [MLD_OFF])
    assert r.result == "failure"
