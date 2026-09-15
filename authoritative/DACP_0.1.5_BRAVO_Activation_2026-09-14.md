# DACP 0.1.5-BRAVO Activation Decision

**Status:** AUTHORITATIVE PROJECT DECISION / ACTIVE / GENE INTERIM DECISION  
**Effective:** 2026-09-14 upon canonical persistence and independent read-back verification  
**Decision authority:** Gene  
**Decision:** Gene explicitly approved `0.1.5-BRAVO` in toto with no changes.

## Activated specification

The exact approved specification is:

`docs/DACP_Runtime_Expression_0.1.5-BRAVO.md`

Approved blob SHA before activation: `22a02142a46347d0690b47459069d3d237984554`.

This activation changes the lifecycle status of that exact content from noncanonical candidate to the current active DACP runtime specification. The specification text itself is not modified.

## Supersession

`0.1.5-BRAVO` supersedes `DACP_Heuristics_Specification_0.1.4.md` as the active runtime control specification. The 0.1.4 specification remains preserved as provenance and as the predecessor control baseline whose objectives Bravo is intended to preserve.

## Evidence and provenance

The decision followed:
- independent ChatGPT and Claude teardown passes;
- cross-review and reconciliation;
- matrix/graph architecture review;
- independent 12-scenario conceptual test passes by both models;
- final reconciliation correcting privacy escalation, source-precedence, consequence/reversibility, overlay-retirement, watcher/REQUIRED, and critical-junction issues.

The scenario tests remain conceptual field evidence, not implementation proof. Bravo itself preserves that limitation.

## Promotion basis

This activation is valid under `DACP_Interim_Decision_Authority_0.2.md`: Gene explicitly approved the versioned specification change. It does not imply approval by Philip / Jennie / Jake / Gene as a group.

## Verification requirement

Do not treat this decision as active until:
1. this activation record is persisted in canonical Git;
2. `CURRENT.md`, `CURRENT.json`, and `VERSION` identify Bravo as active; and
3. the resulting canonical files are independently read back.