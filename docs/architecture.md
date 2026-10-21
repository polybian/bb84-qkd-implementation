# Architecture

## What this is

A working simulation of **BB84** (Bennett & Brassard, 1984) — the first
quantum key distribution protocol — built on Qiskit. It runs the full
protocol end to end: quantum exchange, basis sifting, QBER estimation,
and the abort decision, twice: once on a clean channel and once under
an intercept-resend eavesdropping attack.

This is #16 in my portfolio and #2 in my quantum series (`quantum-circuits-implementation` was #1),
and the one closest to my background: I come from cybersecurity
(CySA+ trained, SOC-adjacent work), so QKD is where my two worlds meet.

## Layout

```
bb84-qkd-implementation/
├── README.md
├── requirements.txt           # qiskit + qiskit-aer + numpy
├── run_all.sh
├── scripts/
│   ├── common.py              # shared BB84 simulation core
│   ├── 01_bb84_no_eve.py      # clean channel: identical keys, QBER ~0%
│   ├── 02_bb84_with_eve.py    # intercept-resend: QBER ~25%, abort
│   └── 03_key_rate.py         # raw qubits -> final key yield table
├── docs/
│   ├── architecture.md        # this file
│   └── interview-answers.md
└── simplified-explanation.md   # plain-language guide (Spanish)
```

## Protocol flow

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

## How the simulation works

Each qubit is simulated individually on `AerSimulator` (shots=1,
seeded). Alice's preparation and Bob's/Eve's measurements are real
single-qubit circuits: Z-basis preparation is `X?`, X-basis adds `H`
before and after. Eve's intercept-resend is modeled as two sequential
simulations — measure in her basis, then re-prepare the eigenstate she
observed — which is exactly what the attack does physically.

Classical post-processing (sifting, sampling, QBER) is done with numpy
on the recorded outcomes, mirroring the real public-channel discussion.

## The 25%, derived

Eve guesses each basis at random:
- 50%: she guesses Alice's basis → resends the correct state → no error.
- 50%: wrong basis → her measurement yields a random bit, which she
  resends in the wrong basis → Bob, measuring in Alice's (correct)
  basis, gets a random outcome → 50% error.

QBER = 0.5 × 0.5 = **25%**. The simulation asserts the measured QBER
lands in the 20–30% band.

## Design choices

- **Per-qubit simulation** instead of one big circuit: it models Eve's
  mid-protocol intervention naturally and keeps every step inspectable.
- **Seeded RNG + seeded simulator**: the whole run is reproducible;
  the README's numbers can be regenerated bit-for-bit.
- **Assertions as the verdict**: script 01 asserts QBER < 5% and key
  equality; script 02 asserts the 20–30% band and prints ABORT. The
  physics conclusion is a passing check, not commentary.

## What this is not

Not a security proof, not a real QKD implementation (no decoy states,
no finite-key analysis, no privacy amplification — the sample bits are
simply discarded rather than hashed out). It is a faithful
*operational* model of the protocol's core loop, built to be understood
and extended.
