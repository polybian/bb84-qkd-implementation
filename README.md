# bb84-qkd-implementation

A complete, runnable simulation of **BB84** (Bennett & Brassard, 1984) —
the first quantum key distribution protocol — built with Qiskit. Alice
and Bob exchange qubits, sift bases, estimate the error rate, and keep
or abort the key. Run twice: once on a clean channel, once under an
intercept-resend eavesdropping attack.

This one is closest to my background: I'm a CySA+-trained security
person, so QKD is where my two worlds — cybersecurity and quantum —
meet.

## The three implementations

| # | Script | What it demonstrates |
|---|--------|----------------------|
| 1 | `01_bb84_no_eve.py` | **Clean channel** — Alice and Bob end with identical keys, QBER 0% |
| 2 | `02_bb84_with_eve.py` | **Intercept-resend attack** — QBER jumps to ~25%, key aborted |
| 3 | `03_key_rate.py` | **Key yield** — raw qubits → final secret key at several scales |

## Architecture

```
Alice                          Quantum channel                        Bob
  │  random bits + random bases ──qubits──▶ (Eve?) ──qubits──▶ measure random bases
  │                                    Public channel                         │
  │◀────────────── compare bases ──────────────▶│
  │  keep matching positions (~50%)             │  keep matching positions
  │◀────────────── disclose 20% sample ────────▶│
  │  QBER < threshold? ──YES──▶ final secret key                              │
  │                    └──NO──▶ ABORT                                         │
```

Each qubit is a real single-qubit Qiskit circuit on the Aer simulator
(seeded, reproducible); sifting and QBER estimation mirror the actual
public-channel discussion. See [docs/architecture.md](docs/architecture.md)
for the full design, including the derivation of the 25%.

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

bash run_all.sh
```

## Validation

Measured on Qiskit Aer 2.6.0 (seeded), 2026-10-21:

| Implementation | Prediction | Measured |
|------------|-----------|----------|
| Clean channel (2000 qubits) | QBER ~0%, identical keys | QBER **0.00%** (0/198 sample errors); 991 sifted → **793-bit** final key — assertion passed |
| Intercept-resend (2000 qubits) | QBER ~25% → abort | QBER **26.77%** (53/198), inside the 20–30% band — assertion passed, key **aborted** |
| Key rate | yield → ~40% | 41.5% / 38.4% / 38.3% / 39.6% at 200/500/1000/2000 raw qubits — assertion passed |

The ~40% yield is exactly sifting (1/2) × sampling (4/5): the price of
information-theoretic eavesdropping detection.

## Why this matters (the one-paragraph version)

Classical key exchange can be intercepted silently. In BB84,
eavesdropping is *detectable by physics*: Eve's measurement disturbs the
qubits, the QBER spikes from ~0% to ~25%, and Alice and Bob abort before
any secret is at risk. This implementation makes that abstract guarantee concrete
— you watch the numbers move.

## Plain-language guide

[simplified-explanation.md](simplified-explanation.md) —
BB84 explained as if you were eight years old: spies, magic glasses,
and the wax seal nobody can fake (Spanish).
