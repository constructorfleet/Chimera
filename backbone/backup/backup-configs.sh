#!/usr/bin/env bash
set -euo pipefail

timestamp=$(date +"%Y%m%d-%H%M%S")
tar -czf "backup-configs-${timestamp}.tar.gz" -C "$(dirname "$0")/.." configs
