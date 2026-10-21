"""
01 — BB84 without an eavesdropper: the clean key exchange.

Alice and Bob run the BB84 protocol over a simulated quantum channel
with no attacker. After sifting, their keys must match: the QBER
(quantum bit error rate) estimated on the disclosed sample should be
~0% (exactly 0% on a noise-free simulator).

Run:
    python3 scripts/01_bb84_no_eve.py [--qubits 2000] [--seed 7]
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_bb84


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qubits", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    r = run_bb84(args.qubits, args.seed, eve=False)

    print(f"Raw qubits exchanged : {r['n']}")
    print(f"Sifted key length   : {r['sifted_len']} "
          f"({100 * r['sifted_len'] / r['n']:.1f}% of raw — bases matched)")
    print(f"Disclosed sample    : {r['sample_size']} bits, "
          f"{r['sample_errors']} errors")
    print(f"QBER                : {100 * r['qber']:.2f}%")
    print(f"Final secret key    : {r['final_key_len']} bits")
    print(f"Key (first 32 bits) : {r['final_key_head']}")

    assert r["qber"] < 0.05, f"Unexpected errors with no eavesdropper: {r['qber']}"
    assert (r["sifted_alice"] == r["sifted_bob"]).all(), "Keys diverged!"
    print("\nOK — Alice and Bob share an identical secret key; channel is clean.")


if __name__ == "__main__":
    main()
