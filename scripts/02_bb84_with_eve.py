"""
02 — BB84 under intercept-resend attack: Eve gets caught.

Eve intercepts every qubit, measures it in a random basis, and forwards
the eigenstate she observed. Physics punishes her: whenever she guesses
the wrong basis (50% of the time), she resends a random state, and Bob —
on the positions where his basis matches Alice's — sees a 50% error
rate. Expected QBER: 0.5 * 0.5 = 25%.

That 25% is the whole point of QKD: eavesdropping is not just illegal,
it is *detectable*. Alice and Bob see the QBER spike and abort.

Run:
    python3 scripts/02_bb84_with_eve.py [--qubits 2000] [--seed 7]
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

    r = run_bb84(args.qubits, args.seed, eve=True)

    print(f"Raw qubits exchanged : {r['n']}")
    print(f"Sifted key length   : {r['sifted_len']}")
    print(f"Disclosed sample    : {r['sample_size']} bits, "
          f"{r['sample_errors']} errors")
    print(f"QBER                : {100 * r['qber']:.2f}%  (theory: ~25%)")

    assert 0.20 < r["qber"] < 0.30, f"QBER {r['qber']:.3f} outside expected band!"
    print("\nOK — QBER ~25% as theory predicts.")
    print("VERDICT: eavesdropping detected. Alice and Bob ABORT the key.")


if __name__ == "__main__":
    main()
