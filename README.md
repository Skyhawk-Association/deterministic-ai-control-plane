# Deterministic AI Control Plane

Public canonical repository for the Deterministic AI Control Plane (DACP) specification and its public governance material.

DACP is a supervisory/control layer for probabilistic AI systems. Its operating target is **bounded stochasticity, deterministic commitment**.

## Start here

Read [`CURRENT.md`](CURRENT.md). It is the stable human/AI bootstrap address for the current active specification and governing files.

## Current operating model

- **Gene decides.** Material human judgment, mission, endpoints, governance, authority expansion, and material unresolved-risk acceptance remain Gene's decisions under the governing authority.
- **AI executes.** The AI owns the maximum safely executable share of reasoning, research, synthesis, code/command/configuration generation, tool selection, execution, recursive testing, verification, recovery, and platform translation that it is authorized and competent to perform.
- **Git is durable shared state.** Devices and terminals are execution surfaces, not competing sources of truth.
- **Use is adversarial testing.** Active heuristics are continuously challenged by real work and corrected from evidence through the versioned correction process.

## Public/private boundary

This repository is intentionally public for broad inspection and dissemination. Public visibility is **not** permission to place secrets, credentials, private user data, raw chat archives, private operational logs, or confidential application data here. See [`docs/PUBLIC_PRIVATE_BOUNDARY.md`](docs/PUBLIC_PRIVATE_BOUNDARY.md).

No software license is granted merely by public visibility. Licensing is intentionally left for an explicit later decision.

## Repository structure

- `CURRENT.md` / `CURRENT.json` — stable bootstrap pointers to current active state.
- `authoritative/` — current authoritative public DACP specifications and decisions.
- `history/` — superseded public specification states preserved as provenance.
- `docs/` — operating rules for storage, devices, integrity, and NAS transition.
- `tests/` — public field/regression test descriptions; no claim that passing them proves implementation correctness.
- `MARCHING_ORDERS.md` — the five current infrastructure marching orders.

## Implementation boundary

This repository currently governs specifications, field use, evidence, and project operating rules. It does **not** by itself authorize construction of the DACP web application.
