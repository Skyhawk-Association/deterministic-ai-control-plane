# DACP Decision Record — VPS Executor Authorization

**Date:** 2026-09-30  
**Decision authority:** Gene  
**Status:** AUTHORITATIVE / ACTIVE upon canonical persistence and independent read-back

## Decision

Gene authorizes ChatGPT and Claude, one executor at a time as he chooses, to use a controlled execution agent on the InMotion VPS for the Skyhawk migration and ongoing Skyhawk administration.

This is an expansion of execution authority from human-carried VPS commands to a machine-qualified execution path. It does not expand project objectives, destructive authority, data/privacy scope, or decision-governance authority.

## Boundaries

The VPS executor must:

- remain governed by CURRENT.md, the active DACP runtime, projects/skyhawk/RULES.md, and germane authoritative references;
- comply with current InMotion Hosting terms, acceptable-use, resource, and root-access requirements;
- use least privilege by default;
- avoid exposing a general-purpose unauthenticated or public root shell;
- use a dedicated service identity and narrowly scoped privilege escalation where elevated actions are genuinely required;
- preserve command identity, bounded stdout/stderr, exit status, timestamps, and audit evidence;
- qualify the complete request -> persist -> execute -> result -> consumer read-back -> verify -> continue pipe before reliance;
- stop on unresolved authority, policy, credential, execution-context, or material-risk uncertainty;
- not bypass provider security controls, platform restrictions, or authentication requirements;
- not perform destructive production actions beyond authority already granted under Skyhawk rules and DACP.

## Human boundary

Gene remains the authority for:

- credential creation or materially broader credential scope;
- expansion of permissions beyond this decision;
- irreversible/destructive authority not already granted;
- acceptance of unresolved material risk;
- provider/account actions that require the account holder;
- legal or policy judgments that cannot be resolved from authoritative provider sources.

## Implementation target

The preferred design is a small auditable agent with an authenticated job/result protocol, dedicated service account, bounded execution, full logging, and an explicit kill switch. Root is not the default execution identity.

A Git-backed transport may be used when it is the simplest qualified route, provided private credentials/secrets are never committed and the end-to-end pipe is proven for each executor.

## Provider-policy constraint

Current InMotion public policy and root-access documentation were reviewed on 2026-09-30 before this decision was operationalized. The executor design must remain within those published constraints and must be revalidated if provider terms materially change.
