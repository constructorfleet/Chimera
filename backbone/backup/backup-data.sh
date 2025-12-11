#!/usr/bin/env bash
set -euo pipefail

timestamp=$(date +"%Y%m%d-%H%M%S")
tar -czf "backup-data-${timestamp}.tar.gz" -C "$(dirname "$0")/.." data
