"""
03 — Key rate: what BB84 costs.

Runs the clean protocol at several raw-qubit counts and shows where the
bits go: ~50% lost to sifting (basis mismatch), ~20% of the sifted key
sacrificed for QBER estimation, the rest is usable secret key.

Takeaway: BB84 turns ~1000 raw qubits into ~400 secret bits — roughly a
40% yield. That is the price of information-theoretic security.

Run:
    python3 scripts/03_key_rate.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_bb84


def main() -> None:
    print(f"{'raw':>6}  {'sifted':>7}  {'sample':>7}  {'final key':>9}  {'yield':>6}")
    print("-" * 45)
    for n in (200, 500, 1000, 2000):
        r = run_bb84(n, seed=7, eve=False)
        y = 100 * r["final_key_len"] / n
        print(f"{n:>6}  {r['sifted_len']:>7}  {r['sample_size']:>7}  "
              f"{r['final_key_len']:>9}  {y:>5.1f}%")
        assert r["qber"] < 0.05
    print("\nOK — yield converges to ~40%: sifting (1/2) x sampling (4/5).")


if __name__ == "__main__":
    main()
