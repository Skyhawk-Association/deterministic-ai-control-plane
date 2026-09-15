# DACP 0.1.6-CHARLIE Activation Decision

## Change Synopsis

- Records Gene's explicit approval of `0.1.6-CHARLIE` Design Pass 7 as the active DACP runtime specification.
- Promotes the exact reviewed Charlie blob without modifying the approved specification text.
- Supersedes `0.1.5-BRAVO` as the active runtime control hypothesis while preserving Bravo as provenance and predecessor baseline.
- Records promotion-time reconfirmation that Microsoft's Agent Control Specification (ACS) naming collision remains current, supporting Charlie's `Control Working Set (CWS)` terminology.
- Preserves the explicit limitation that Charlie's review evidence is design/conceptual evidence, not implementation proof.

**Status:** AUTHORITATIVE PROJECT DECISION / ACTIVE / GENE INTERIM DECISION  
**Effective:** 2026-09-15 upon canonical persistence and independent read-back verification  
**Decision authority:** Gene  
**Decision:** Gene explicitly approved `0.1.6-CHARLIE` Design Pass 7 as the active DACP runtime specification.

## Activated specification

The exact approved specification is:

`docs/DACP_Runtime_Expression_0.1.6-CHARLIE.md`

Approved blob SHA before activation: `545c9fac04f66eb1f188bb861ec7bc55362aecb5`.

This activation changes the lifecycle status of that exact content from noncanonical candidate to the current active DACP runtime specification. The approved specification text itself is not modified by activation.

## Supersession

`0.1.6-CHARLIE` supersedes `0.1.5-BRAVO` as the active runtime control specification. Bravo remains preserved as provenance and as Charlie's predecessor control baseline.

## Evidence and provenance

The decision followed:
- iterative ChatGPT design and reconciliation passes;
- multiple independent Claude adversarial/quality reviews;
- correction of all material defects found during those reviews;
- final independent Claude review of Design Pass 7 with verdict `READY FOR GENE REVIEW` and no material defects in the checked categories;
- independent canonical Git read-back of the exact Design Pass 7 blob;
- promotion-time reconfirmation on 2026-09-15 that Microsoft continues to publish Agent Control Specification (ACS) as an open runtime-governance standard, preserving the external naming-collision basis for Charlie's `Control Working Set (CWS)` rename.

Microsoft promotion evidence:
- `https://devblogs.microsoft.com/foundry/build-2026-open-trust-stack-ai-agents/`
- `https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-build-2026/`

Charlie remains a control hypothesis under real use. Its design/review evidence is not implementation proof, and activation does not by itself claim that existing DACP application slices have been migrated to or regression-tested against Charlie.

## Promotion basis

This activation is valid under `DACP_Interim_Decision_Authority_0.2.md`: Gene explicitly approved the versioned specification change. It does not imply approval by Philip / Jennie / Jake / Gene as a group.

Gene's approval also resolves Charlie §17's lifecycle boundary for promotion: the reviewed Design Pass 7 evidence is accepted as sufficient for activation of the runtime control hypothesis while implementation/regression proof remains separately outstanding.

## Verification requirement

Do not treat this decision as active until:
1. this activation record is persisted in canonical Git;
2. `CURRENT.md`, `CURRENT.json`, and `VERSION` identify Charlie as active;
3. the exact Charlie blob remains `545c9fac04f66eb1f188bb861ec7bc55362aecb5`; and
4. the resulting canonical files are independently read back.
