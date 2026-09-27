# DACP Decision Record 2026-09-27 — Required Pipe Qualification

**Status:** AUTHORITATIVE PROJECT DECISION / GENE DECISION  
**Decided:** 2026-09-27  
**Effective:** upon canonical persistence and independent read-back verification

## Decision

Gene directed that the recurring half-pipe failure be corrected in canonical Git, tested, and written into DACP law.

A required DACP persistence/evidence/handoff pipe is therefore not operational until the intended executor has proven the complete producer-to-consumer route:

WRITE -> PERSIST -> READ BACK -> VERIFY -> CONTINUE

A failed adapter does not establish failed capability while another authorized competent route exists. The executor must automatically use the alternate route before returning mechanical transport work to Gene.

## Evidence

Direct ChatGPT GitHub connector writes were observed to be inconsistently dispatchable: one LOST-D write succeeded, while later writes were blocked by the intermediary despite the repository and authorization remaining valid.

The underlying Git capability was then tested through a materially different authorized route:
- Windows local repository at C:\Users\genea\dacp-work\dacp;
- Git 2.55.0;
- main fast-forwarded from canonical origin;
- test artifact committed and pushed as cad7d174f415c19d704187ad1026220244430f7d;
- independent GitHub connector read-back returned the exact persisted artifact and token;
- the previously blocked LOST-D state update was committed and pushed as d8255d12a18228f797a506f851b64f63e7591f92;
- independent GitHub read-back confirmed main and the exact updated LOST-D line.

This proves the executor-specific ChatGPT Git pipe:
ChatGPT -> Desktop Commander -> Windows local Git clone -> GitHub canonical repository -> independent GitHub read-back.

## Governance changes

- Activate authoritative/DACP_Required_Pipe_Qualification_0.1.md.
- Supersede Project Instructions 0.6 with Project Instructions 0.7, adding required-pipe qualification and failover as a binding project instruction.
- Add regression fixtures D20-D22.
- Update CURRENT.md / CURRENT.json and authoritative status index.

## Scope

This decision does not:
- expand repository or credential authority;
- grant direct A2 production access to an AI;
- make private state public;
- weaken existing verification, privacy, or human-decision controls.

It changes enforcement of already-authorized machine transport and persistence paths so partial adapters cannot strand work or return mechanical transport to Gene.
