# Deterministic AI Control Plane prototype

This directory contains the working DACP prototype and the field/regression evidence that led to the current implementation path.

## Current resolved-operation path

The default entrypoint is:

```sh
python3 run_live.py
```

The resolved commitment path is:

`operation manifest -> DACPResolvedOperation -> NativeActionAdapter -> CommitmentCore -> DACPRuntime`

with separate authority:

`pinned authority manifest -> PinnedFileAuthorityProvider -> CommitmentCore`

and, for the durable file runtime, separate recovery/concurrency controls:

`interprocess resource lock -> durable dispatch-intent journal -> reconciliation before redispatch`

A provider/model is not part of resolved commitment. Provider/model adapters remain available only for upstream orientation or planning where probabilistic reasoning actually contributes before the exact operation is formed.

## Resolved commitment lifecycle

For an already-resolved operation, the control plane:

1. loads the exact operation request;
2. resolves the current target;
3. validates independently supplied action-bound authority;
4. checks the declared postcondition independently;
5. if already satisfied, verifies with the oracle and closes with zero dispatches;
6. otherwise writes durable dispatch intent before executor invocation;
7. commits exactly once through the core gate;
8. independently verifies the resulting state and compares the oracle;
9. records the terminal journal disposition and final acceptance.

A successful fresh mutation requires exactly one dispatch and one applied write. An already-satisfied replay requires zero dispatches and zero writes.

## Operation manifests are requests, not permission

The default request is `operations/tracked-value-deploy.json`, schema `dacp-operation-manifest-0.1`. A different operation may be supplied with `--operation-manifest <path>`.

Every live result records the exact operation manifest path, schema, and SHA-256. Loading an operation manifest never creates authority. The manifest-derived action must match independently supplied authority before consequential commitment can proceed.

## Authority is separate from the executor

The default prototype authority is `authorities/tracked-value-deploy-authority.json`, schema `dacp-authority-manifest-0.1`. Its canonical-JSON SHA-256 is pinned in the versioned live runner. The runtime cannot mint, broaden, revoke, or repair authority.

`PinnedFileAuthorityProvider` authenticates the grant against the configured canonical-JSON SHA-256 pin and rechecks integrity at use time. CRLF/LF differences, insignificant whitespace, and object-key order do not change authority identity; semantic changes do. Missing, malformed, or semantically changed authority fails closed.

An alternate authority file requires both `--authority-manifest <path>` and `--authority-sha256 <trusted-pin>`.

This pinned-file authority is a bounded prototype trust root, not the intended final human-authentication mechanism. Production authority must ultimately be backed by an authenticated user/service control boundary appropriate to the consequence.

## Durable runtime

`dacp_file_runtime.py` is the default runtime. Unless overridden, state lives at `~/.dacp/runtime/tracked-value.json`; `DACP_STATE_FILE` or `--state-file` may change it. The runtime persists value, version, and ledger together with atomic replacement and readback verification.

The runtime knows how to perform a mechanically valid `SET_STATE`; it does not decide which value is authorized. Repeating an already-satisfied operation is idempotent and does not increment version or append a ledger event.

The in-memory runtime remains available explicitly with `--runtime memory` for disposable/testing use.

## Crash and uncertain-outcome recovery

`dacp_commit_journal.py` persists `DISPATCH_INTENT` before the executor call. The journal record binds operation ID, stable request fingerprint, target fingerprint, action fingerprint, and authority ID.

If a process restarts with unresolved dispatch intent:

- if independent verifier and oracle prove the intended postcondition, the control plane records `RESOLVED_SUCCEEDED` and closes with zero redispatches;
- if the effect is not proven, the operation remains `PENDING` with zero redispatches;
- if the same operation ID now resolves to a materially different request fingerprint, recovery is blocked rather than silently adopting the new request.

A crash or timeout is therefore not treated as proof of failure and does not license a duplicate consequential operation.

## Concurrent-process control

`dacp_file_lock.py` provides a stdlib-only advisory exclusive lock for the durable resource. The lock is acquired before runtime/journal inspection and is released by the operating system if the process dies.

Only one resolved commitment process may inspect-and-commit a given durable state resource at a time. A second process that cannot obtain the lock within its configured timeout returns `PENDING` with zero dispatches and zero writes. The live CLI exposes `--lock-timeout`; the default is 10 seconds.

This serialization closes the local check/act race between multiple DACP processes. It does not claim distributed locking across machines or storage systems.

## Verification and evidence

Current artifacts record exact source commit, operation manifest identity, authority integrity before and after use, runtime pre/post snapshots and SHA-256 values, commit-journal state, lock evidence, dispatch/applied counts, verifier/oracle results, lifecycle events, and final acceptance.

The bundled acceptance surface is:

```sh
python3 run_conditional_acceptance.py
```

It runs the deterministic unit suite plus durable lifecycle cases covering:

- fresh mutation;
- idempotent replay;
- restart after unresolved intent with no proven effect;
- restart after unresolved intent with a verified effect;
- a second process blocked by the resource lock without dispatch.

The bundle emits one `conditional-acceptance-*.json` artifact.

## CI acceptance

`.github/workflows/prototype-conditional-acceptance.yml` runs the same bundle on both `windows-latest` and `ubuntu-latest` and uploads the acceptance artifact. This is the preferred mechanical regression surface because the resolved path has no provider credential dependency.

## Tests

The consolidated suite includes:

```sh
python3 -m unittest -v \
  test_dacp_commitment_core.py \
  test_dacp_core_adapter.py \
  test_dacp_authority_provider.py \
  test_dacp_control_session.py \
  test_dacp_commit_journal.py \
  test_dacp_file_lock.py \
  test_dacp_resolved_operation.py \
  test_dacp_core_live_runtime.py \
  test_dacp_file_runtime.py \
  test_run_core_live_integration_session.py \
  test_run_live.py
```

## Remaining prototype boundaries

The current implementation proves a local single-resource resolved-commitment control path. It does not yet claim distributed consensus, distributed locking, production identity/authentication, general multi-resource transactions, or a durable remote trust anchor for the local commit journal. Those require evidence and architecture specific to the eventual production endpoint rather than speculative machinery now.

Provider adapters, historical matrix runners, and broader research artifacts remain available as evidence surfaces, but they are not the current resolved commitment execution path.
