#!/usr/bin/env bash
set -e

code-server --bind-addr 0.0.0.0:8080 --auth password --disable-telemetry --disable-update-check --disable-workspace-trust "${CONTAINERWSF}"
