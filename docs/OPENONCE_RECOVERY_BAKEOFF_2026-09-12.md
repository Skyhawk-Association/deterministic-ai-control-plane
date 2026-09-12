# OpenOnce Recovery Semantics Bakeoff

**Date:** 2026-09-12  
**Status:** IMPLEMENTATION RESEARCH / PUBLIC-SAFE EVIDENCE  
**DACP canonical baseline:** `e954e8aa49ae3d3e31657dae443c432a2f0b817e`  
**OpenOnce evaluated commit:** `92cf4e85f62252ff760033f6e7a0868ce0d7b405` (`openonce` 0.1.0, alpha)

## Question

Can OpenOnce replace, wrap, or materially simplify the accepted DACP local single-resource commitment/recovery kernel without weakening the current DACP contract?

## Success criteria used

The candidate must be evaluated against DACP behavior that is already accepted and verified: preexisting-state no-dispatch completion, durable uncertainty across restart, no blind redispatch while prior success is plausible, exact request mismatch blocking, safe concurrency, independent postcondition verification, authority-bound commitment, and explicit PENDING rather than invented success/failure.

## Primary-source findings

OpenOnce has a serious, relevant recovery model. Its state machine makes `UNKNOWN` first-class. A crash or ambiguous transport failure between `STARTED` and `RECEIPT_RECORDED` is parked rather than retried. Its reconciler probes the external world and resolves `HAPPENED`, `NOT_HAPPENED`, or `INCONCLUSIVE`; inconclusive results route to human review rather than guessing. It also supplies stable provider idempotency keys, request fingerprints, duplicate replay, SQLite durability, CAS-like state transitions, leases, provider capability metadata, receipt contracts, and optional provider-conformance gates.

OpenOnce is not a workflow engine and does not claim exactly-once external effects. Its own stated guarantee is at-least-once execution plus idempotency plus reconciliation. Core dependencies are stdlib-only; SQLite is the zero-infrastructure durable store and PostgreSQL is optional.

## Upstream suite execution

The OpenOnce repository was cloned and pinned to the exact commit above on Windows/Python 3.13. The upstream test suite passed under UTF-8 console mode. Under the default Windows cp1252 console, one runnable documentation example failed only while printing the Unicode empty-set character; the semantic tests were otherwise unaffected. This is a portability rough edge, not evidence of recovery-semantic failure.

## DACP-targeted local bakeoff

A six-case local test was run against OpenOnce using its SQLite store and public API. No provider API or model call was required.

| DACP behavior | Result | Observation |
|---|---|---|
| PREEXISTING_NO_DISPATCH | FAIL | OpenOnce executed the handler once even though the target state was already satisfied. It does not perform DACP's pre-dispatch independent postcondition check. |
| UNKNOWN_BLOCKS_BLIND_RETRY | PASS | Ambiguous side effect parked as `UNKNOWN`; duplicate call did not re-execute. |
| RESTART_NO_REDISPATCH | PASS | Reopening the same SQLite ledger preserved the parked effect and did not dispatch again. |
| RECONCILE_HAPPENED_NO_REDISPATCH | PASS | External probe confirmed the effect; state advanced to committed without another handler call. |
| REQUEST_MISMATCH_BLOCKED | PASS | Reuse of the same explicit idempotency key with different arguments raised an idempotency mismatch before another execution. |
| INCONCLUSIVE_ESCALATES | PASS | Inconclusive external probe advanced to `HUMAN_REVIEW`, not retry or fabricated resolution. |

Result artifact SHA-256 from the local run: `c8c930b4233de4c694ef7605d098f6bc81a2336177148c899a9b74339a005246`.

## Contract comparison

### What OpenOnce does better or more completely today

- richer exception classification between definitely retryable, ambiguous, and definitive failure;
- explicit leases and takeover semantics around in-flight work;
- provider-specific probing as a first-class recovery interface;
- capability metadata that says whether a negative probe is strong enough to re-arm;
- optional conformance evidence before automatic recovery decisions;
- reusable provider-side idempotency keys and receipt contracts.

### What DACP already requires that OpenOnce does not replace

- preexisting-state independent verification before any dispatch;
- action-bound authority identity and target binding before commitment;
- commit-time target re-resolution and rebind behavior;
- predeclared verifier contract and success evidence;
- declared-verifier versus independent-oracle conflict handling;
- DACP request/authority/control evidence and final acceptance semantics;
- task-time control applicability and KNEW/APPLIED/COMPLIED measurement upstream.

Replacing the DACP kernel with OpenOnce would therefore require a substantial DACP wrapper around OpenOnce. That wrapper would retain much of the current commitment kernel while adding an alpha dependency and a second state vocabulary. The simplification case is not demonstrated.

## Decision for DACP 0.1

**KEEP the accepted DACP commitment kernel. Do not add OpenOnce as a runtime dependency for DACP 0.1.**

**BORROW the useful recovery patterns rather than the package dependency:** explicit provider-probe contracts, provider capability metadata, conservative negative-probe semantics, and exception classification should be candidates for narrow DACP implementation where they measurably improve recovery without weakening current gates.

This is a technical implementation decision for the current local single-resource prototype scope, not a claim that OpenOnce is inferior generally. Reconsider adoption if a future OpenOnce release materially closes the preexisting-verification/authority/verification-contract gap, if DACP expands into provider-specific side effects where OpenOnce's provider knowledge materially reduces custom code, or if maintaining DACP's recovery layer becomes more expensive than a wrapper.

## Immediate architectural consequence

The downstream build-vs-borrow question is resolved for DACP 0.1: retain the current kernel and proceed upward. OpenOnce remains a reference implementation and future replacement candidate, not a dependency or critical path.
