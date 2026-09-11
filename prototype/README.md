# Deterministic AI Control Plane prototype

This directory contains the working DACP prototype and the field/regression evidence that led to the current implementation path.

## Current live path

The default live entrypoint is:

```sh
python3 run_live.py --provider openai
```

That command uses the durable local file runtime by default. Unless overridden, state is stored at `~/.dacp/runtime/tracked-value.json`. `DACP_STATE_FILE` or `--state-file <path>` may override it. The in-memory runtime remains available explicitly for disposable/test runs with `--runtime memory`.

The current path is:

`operation manifest -> provider native action -> DACPControlSession -> NativeActionAdapter -> CommitmentCore -> DACPRuntime`

with a separate authority input:

`pinned authority manifest -> PinnedFileAuthorityProvider -> CommitmentCore`

The model proposes actions. The operation manifest describes requested intent. The authority provider supplies permission. The runtime owns only state access, execution mechanics, verification, and evidence. The deterministic core owns consequential admission and completion.

## Operation manifests are requests, not permission

The default request is `operations/tracked-value-deploy.json`, schema `dacp-operation-manifest-0.1`. A different operation may be supplied with `--operation-manifest <path>`.

Every live result records the exact operation manifest path, schema, and SHA-256. Loading an operation manifest never creates authority. Before provider execution can lead to commitment, the manifest-derived action must match independently supplied authority.

## Authority is separate from the executor

The default prototype authority is `authorities/tracked-value-deploy-authority.json`, schema `dacp-authority-manifest-0.1`. Its exact expected SHA-256 is pinned in the versioned live runner. The runtime cannot mint, broaden, revoke, or repair that authority.

`PinnedFileAuthorityProvider` loads a grant only when the initial bytes match the trusted SHA-256 pin. It rechecks the authority file on every authority resolution. If the file is missing or changed after initialization, the cached trusted grant is returned with `trust_root_compromised=true`, causing consequential commitment to fail closed rather than trusting the changed file.

An alternate authority file requires both `--authority-manifest <path>` and `--authority-sha256 <trusted-pin>`. Supplying a file without an independently provided pin is rejected.

This pinned-file authority is a bounded prototype trust root, not the intended final human-authentication mechanism. It proves separation of authority from the executor and tamper detection. A production authority source must ultimately be backed by an authenticated user/service control boundary appropriate to the consequence.

## Runtime boundary

`dacp_runtime_contract.py` defines `DACPRuntime`. A runtime exposes target resolution, execution, direct verification, oracle verification, routine reads, and evidence snapshots. It does **not** expose `resolve_authority()`.

`dacp_file_runtime.py` is the default durable runtime. It persists state and ledger together using versioned preconditions, atomic replacement, and readback. It knows how to perform a mechanically valid `SET_STATE`; it does not decide which value is authorized. Repeating an already-satisfied operation is idempotent and does not increment the version or append another ledger event.

`dacp_core_live_runtime.py` provides the same execution/state boundary in memory for deterministic tests and disposable runs.

## Control ownership

`dacp_commitment_core.py` owns exact declaration/action binding, authority validation, commit-time target and authority revalidation, duplicate suppression, uncertain-outcome handling, independent verification/oracle comparison, verification conflicts, and final acceptance.

`dacp_control_session.py` owns the provider conversation shell. `dacp_core_adapter.py` translates normalized PREDECLARE/CALL/REPORT actions into core operations. Neither is allowed to silently replace core authority or completion decisions.

`dacp_authority_provider.py` owns authority-source parsing, pin validation, target-bound proof generation, revocation state, and authority integrity evidence. `dacp_operation_manifest.py` owns operation-request parsing only.

## Evidence

Current live artifacts record source commit identity, operation manifest identity, authority integrity evidence before and after execution, runtime pre/post snapshots, durable state SHA-256 before and after execution, core lifecycle events, provider turns, dispatch count, applied count, and final acceptance.

A valid already-satisfied durable run requires zero applied writes, unchanged version/ledger, identical pre/post state SHA-256, no verification conflict, intact authority evidence, and `VERIFIED_SUCCEEDED`.

## Tests

Core implementation tests include:

```sh
python3 -m unittest -v \
  test_dacp_commitment_core.py \
  test_dacp_core_adapter.py \
  test_dacp_authority_provider.py \
  test_dacp_control_session.py \
  test_dacp_core_live_runtime.py \
  test_dacp_file_runtime.py \
  test_run_core_live_integration_session.py \
  test_run_live.py
```

The broader historical matrix runners remain regression/evidence surfaces, not the current application execution path. Do not add standalone matrix families when a requirement can be expressed and tested directly in the consolidated core.

## Credentials

Provider credentials come from environment variables and must never be committed or written into public evidence. OpenAI is the primary implementation path; Anthropic remains optional and is not a required gate.

## Non-goals

The prototype still does not need an agent framework, vector database, message bus, recursive debate system, automatic heuristic promotion, or multi-model parliament. Additional machinery must solve an evidenced control problem better than the smaller design before it earns a chair at the table.
