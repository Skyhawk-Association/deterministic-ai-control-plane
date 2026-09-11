# Deterministic AI Control Plane prototype

This directory contains the working DACP prototype and the field/regression evidence that led to the current implementation path.

## Current live path

The default live entrypoint is:

```sh
python3 run_live.py --provider openai
```

`run_live.py` delegates to `run_core_live_integration.py`, which wires one provider-native action stream into one deterministic control path:

`provider native action -> dacp_action_provider -> NativeActionAdapter -> CommitmentCore -> VersionedValueRuntime`

The model proposes actions. The deterministic layer owns consequential admission and completion.

### Current control ownership

`dacp_commitment_core.py` owns:

- exact declaration/action binding;
- verifier admission through a gate-controlled registry;
- authenticated action-bound authority checks;
- commit-time authority revalidation;
- commit-time target revalidation;
- duplicate consequential-dispatch suppression;
- explicit `PENDING` handling for uncertain outcomes;
- independent postcondition verification;
- optional independent oracle comparison;
- fail-closed verification-conflict handling;
- final completion acceptance;
- tamper-aware boundary trace anchoring/reconstruction primitives.

`dacp_core_adapter.py` translates normalized `PREDECLARE`, `CALL`, and `REPORT` actions into the core. It deliberately does not duplicate the core's safety decisions.

`dacp_core_live_runtime.py` is the first minimal live runtime. It supplies a versioned value, authenticated authority proof, conditional write boundary, direct-state verifier, and append-only ledger replay oracle.

`dacp_action_provider.py` is the provider-native action interface for OpenAI and Anthropic. OpenAI is the default/primary implementation path. Anthropic remains available as an optional independent path and is not a required implementation gate.

## Verified live behavior

The current integrated live path is expected to demonstrate all of the following before a successful completion claim is accepted:

1. a matching consequential declaration is admitted;
2. exactly one consequential write dispatch occurs;
3. the resulting state is independently read back;
4. the ledger oracle independently agrees with the observed result;
5. no verification conflict remains;
6. the model's final claim matches the control-plane classification;
7. completion is accepted as `VERIFIED_SUCCEEDED` only after those checks.

A redundant consequential declaration or call after verified completion is blocked without disturbing the completed state.

## Tests

No third-party Python packages are required for the deterministic prototype tests.

Core implementation tests:

```sh
python3 -m unittest -v \
  test_dacp_commitment_core.py \
  test_dacp_core_adapter.py \
  test_dacp_core_live_runtime.py
```

The broader historical regression suite remains useful while migration continues because it preserves failure cases that motivated the consolidated core.

## Legacy / regression surfaces

The following runners and guard modules are **not the current application execution path**. They are intentionally retained as field evidence and regression fixtures while the consolidated implementation absorbs their proven behavior:

- `run_gate_matrix.py`
- `run_uncertain_matrix.py`
- `run_commit_guard_matrix.py`
- `run_rollback_guard_matrix.py`
- `run_authority_guard_matrix.py`
- `run_authority_revocation_matrix.py`
- `run_trace_guard_matrix.py`
- their corresponding `dacp_*_guard.py` and `test_*` modules

Do not add new standalone matrix families merely to test another prompt behavior when the requirement can be expressed and tested directly in `CommitmentCore`. New controls should be added only when current evidence exposes a causal gap the core cannot express simply.

## Credentials

Provider credentials come from environment variables and must never be committed or written into public evidence:

```sh
export OPENAI_API_KEY='...'
export ANTHROPIC_API_KEY='...'
```

Only the credential for the selected provider is required by the default live runner.

## Historical broker v0

The prototype began as a deliberately small two-provider broker experiment. It sent the same prompt to OpenAI and Anthropic, performed no automatic retries, recorded append-only JSONL audit data, supported an optional one-round peer challenge, and distinguished objective verification from mere model agreement.

That work remains useful provenance, but the current implementation no longer depends on two-provider agreement or Claude availability. The project has moved from probabilistic peer comparison toward deterministic commitment at the execution boundary.

Historical broker terminal states included `VERIFIED_MATCH`, `SUPPORTED_AGREEMENT`, `DISAGREEMENT`, and `UNRESOLVED`. The current commitment path instead classifies consequential execution through explicit lifecycle states and accepts success only after deterministic gate and verification evidence.

## Non-goals

The current prototype still does not need an agent framework, vector database, message bus, recursive debate system, automatic heuristic promotion, or multi-model parliament. Additional machinery must earn its existence by solving an evidenced control problem better than the smaller design.
