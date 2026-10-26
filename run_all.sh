#!/usr/bin/env bash
# Runs every implementation in order.
set -euo pipefail
cd "$(dirname "$0")"

# Prefer the project's venv (where qiskit lives); fall back to python3.
if [ -x ".venv/bin/python" ]; then
  PY=".venv/bin/python"
else
  PY="python3"
fi

echo "=== 01 - BB84, no eavesdropper (clean channel) ==="
$PY scripts/01_bb84_no_eve.py
echo
echo "=== 02 - BB84 under intercept-resend attack (Eve) ==="
$PY scripts/02_bb84_with_eve.py
echo
echo "=== 03 - Key rate vs raw qubits ==="
$PY scripts/03_key_rate.py
echo
echo "All three implementations completed successfully."
