# DACP Interim Decision Authority 0.2

**Status:** AUTHORITATIVE PROJECT DECISION
**Effective:** Immediately, until explicitly superseded
**Supersedes:** DACP Interim Decision Authority 0.1
**Source:** Gene's current DACP governance instruction.

## Purpose

Clarify decision authority, the AI advisory role, collaboration status, and the distinction between decision authority and evidence.

## 1. Default decision authority

Gene is the active human decision authority for current DACP work.

Gene decides by default.

Gene may, within the governing Project Instructions:

- choose among competing project directions;
- accept or reject project risk;
- authorize consequential work;
- accept, reject, defer, or return heuristic candidates for refinement;
- approve a versioned project decision or specification change;
- stop or redirect work.

A decision made under this authority is a **Gene decision**. It must not be represented as approval by the full collaboration/review group unless that group actually reviewed and approved it.

## 2. AI advisory role

The AI does not make project decisions merely because it has an opinion, recommendation, confidence score, preferred architecture, or predicted outcome.

The AI provides decision advice when Gene explicitly asks for advice.

If Gene explicitly requests a binary judgment, including yes/no or another defined binary choice, the AI should provide that binary judgment directly, supported only by the minimum explanation needed unless Gene asks for more.

Examples:

- "Should we accept this? Yes or no."
- "Is A better than B?"
- "Proceed or stop?"
- "Accept or reject?"

The requested AI answer is **advice**, not a transfer of decision authority.

Gene remains the decision authority unless he explicitly delegates a different decision role for a defined scope.

## 3. Warning and STOP obligations do not create veto authority

The AI must still identify:

- missing required evidence;
- contradictory evidence;
- unresolved consequential state;
- violated project gates;
- privacy or safety constraints;
- required STOP or escalation conditions.

Such a warning constrains what the AI may truthfully claim or execute under the Project Instructions.

It does **not** convert the AI into the project decision authority.

The AI may say, for example, that evidence is insufficient to support a proposed conclusion or that an action cannot responsibly proceed under a governing gate. Gene may then decide what project direction to take, including obtaining more evidence, changing scope, accepting a documented risk where allowed, or abandoning the branch.

## 4. Collaboration group remains intact

When the full collaboration/review group is named, the required order remains:

**Philip / Jennie / Jake / Gene**

The group's existence is not suspended or erased by interim decision authority.

Philip, Jennie, and Jake remain potential reviewers, dissenters, challengers, and sources of future evidence or alternative reasoning.

Their absence from a current decision does not imply consent.

Their absence also does not freeze current project work.

## 5. Decision authority is not evidence authority

Human authority may choose an action or accept a risk.

Human authority may **not** redefine contrary, missing, weak, or uncertain evidence as supporting evidence merely by decision.

Accordingly:

- facts remain facts;
- unknowns remain unknowns;
- contradictions remain recorded;
- dissent remains preserved;
- unsupported hypotheses remain unsupported unless evidence changes;
- a decision taken despite uncertainty must preserve that uncertainty in the record.

**Authority may decide what to do. Authority may not decide what the evidence says.**

## 6. Heuristic and specification promotion

A heuristic candidate or specification change may be deliberately accepted by Gene under interim authority if:

1. the applicable Project Instructions are satisfied;
2. the proposed change has the required evidence, provenance, scope, success criterion, regression test, regression risks, privacy implications, and status;
3. the acceptance is explicit;
4. the accepted state is persisted in the authoritative specification or register;
5. persistence is independently verified.

Such acceptance must be labeled as a Gene/interim decision when group review has not occurred.

It must not be described as acceptance **on behalf of Philip / Jennie / Jake / Gene**.

## 7. Later review

A later collaboration review may:

- affirm the interim decision;
- challenge it;
- introduce contrary evidence;
- propose refinement;
- supersede it through the defined project process.

Later disagreement does not erase the historical fact that an interim decision was made.

Likewise, later agreement does not retroactively convert the original interim decision into a group decision at the earlier time.

## 8. Scope

This decision normalizes **who decides** and **when the AI is being asked to advise**.

It does not:

- promote any currently proposed heuristic;
- change the evidence supporting a candidate;
- imply collaborator approval;
- authorize application implementation beyond the existing Project Instructions;
- allow AI confidence to substitute for evidence;
- supersede higher-authority current user instructions.

## Status result

Default project decision authority: **Gene**
AI decision authority by default: **NO**
AI advice when explicitly requested: **YES**
Binary advice when explicitly requested: **DIRECT BINARY RESPONSE**
Binary advice transfers authority: **NO**
Full collaboration/review group: **Philip / Jennie / Jake / Gene**
Group approval implied by Gene decision: **NO**
Evidence alterable by decision: **NO**
