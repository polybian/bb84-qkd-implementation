"""
Shared BB84 simulation core.

Models the BB84 quantum key distribution protocol qubit by qubit on the
Qiskit Aer simulator:

  Alice prepares each qubit in a random bit (0/1) and random basis (Z/X).
  Bob measures each qubit in a random basis (Z/X).
  Optionally, Eve performs an intercept-resend attack: she measures each
  qubit in a random basis and forwards the eigenstate she observed.

After the quantum exchange, bases are compared over the public channel:
only positions where Alice and Bob used the SAME basis are kept
("sifting" — roughly half the raw qubits). A random ~20% sample of the
sifted key is then disclosed to estimate the QBER (quantum bit error
rate); the sample bits are discarded and the rest is the final key.
"""

import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator


def _measure_one(bit: int, prep_basis: int, meas_basis: int, seed: int) -> int:
    """Prepare one qubit as (bit, prep_basis) and measure in meas_basis.

    basis 0 = Z (computational), basis 1 = X (Hadamard).
    """
    qr = QuantumRegister(1, "q")
    cr = ClassicalRegister(1, "c")
    qc = QuantumCircuit(qr, cr)
    if bit:
        qc.x(qr[0])
    if prep_basis == 1:
        qc.h(qr[0])
    if meas_basis == 1:
        qc.h(qr[0])
    qc.measure(qr[0], cr[0])
    sim = AerSimulator(seed_simulator=seed)
    counts = sim.run(qc, shots=1).result().get_counts()
    return int(list(counts.keys())[0])


def run_bb84(n: int, seed: int, eve: bool = False) -> dict:
    rng = np.random.default_rng(seed)
    alice_bits = rng.integers(0, 2, n)
    alice_bases = rng.integers(0, 2, n)
    bob_bases = rng.integers(0, 2, n)
    eve_bases = rng.integers(0, 2, n) if eve else None

    bob_bits = np.zeros(n, dtype=int)
    for i in range(n):
        b = int(alice_bits[i])
        ab = int(alice_bases[i])
        bb = int(bob_bases[i])
        if eve:
            eb = int(eve_bases[i])
            # Eve intercepts: measures in her basis, resends what she saw.
            eve_out = _measure_one(b, ab, eb, seed * n + i)
            bob_bits[i] = _measure_one(eve_out, eb, bb, seed * n + 10_000_000 + i)
        else:
            bob_bits[i] = _measure_one(b, ab, bb, seed * n + i)

    # Sifting: keep positions where bases matched.
    keep = alice_bases == bob_bases
    sifted_alice = alice_bits[keep]
    sifted_bob = bob_bits[keep]

    # QBER estimation on a disclosed ~20% sample (sample is discarded).
    m = len(sifted_alice)
    sample_size = max(1, m // 5)
    sample_idx = rng.choice(m, size=sample_size, replace=False)
    errors = int(np.sum(sifted_alice[sample_idx] != sifted_bob[sample_idx]))
    qber = errors / sample_size
    final_key = np.delete(sifted_alice, sample_idx)

    return {
        "n": n,
        "eve": eve,
        "sifted_len": m,
        "sample_size": sample_size,
        "sample_errors": errors,
        "qber": qber,
        "final_key_len": len(final_key),
        "final_key_head": "".join(str(int(x)) for x in final_key[:32]),
        "sifted_alice": sifted_alice,
        "sifted_bob": sifted_bob,
    }
