# DACP Continuous Execution and Human-Boundary Control 0.1

## Change Synopsis

- Corrects a demonstrated execution-friction defect in which the AI could stop after reporting an intermediate result even though authorized mechanical work remained.
- Makes progress reporting non-terminal by default: commentary/status updates do not close the task.
- Requires continued authorized execution until the task objective is reached, a genuine human-only boundary is encountered, or evidence requires STOP.
- Requires automatic resumption after a human-only boundary ends, without waiting for Gene to restate the already-authorized objective.
- Preserves Gene's decision authority, all existing safety/privacy/evidence gates, and all limits on application implementation.

**Status:** AUTHORITATIVE PROJECT CORRECTION / ACTIVE UNDER STANDING DELEGATED CORRECTION AUTHORITY  
**Effective:** Upon canonical persistence and independent read-back verification  
**Authority:** `authoritative/DACP_Operational_Use_and_Correction_Authority_0.1.md`  
**Refines:** `authoritative/Project Instructions 0.4.txt` HUMAN / AI ROLE ALLOCATION  
**Scope:** Turn closure, progress reporting, continuation, and human-only boundary handling across DACP-governed work

## 1. Failure addressed

Observed field behavior showed repeated cases where an intermediate command, install, verification result, or status update was reported to Gene and the AI then ended the turn even though the next authorized mechanical step was already known and executable.

This behavior creates unnecessary user friction and contradicts the accepted allocation: Gene decides; the AI executes the maximum safely executable share.

## 2. Corrected control

For an active DACP task, completion of a substep is not task completion.

The AI must continue through all currently authorized, competent, mechanically executable work without requiring another user prompt merely to continue.

A progress update is commentary, not closure.

The AI may end execution only when at least one of these conditions is true:

1. **OBJECTIVE REACHED** — the authorized task endpoint has been reached and required verification is complete;
2. **HUMAN-ONLY BOUNDARY** — continuation requires authentication/credential presentation, physical action, unavailable capability, a reserved human judgment, authority expansion, or another genuinely human-only act;
3. **GOVERNED STOP** — current evidence, safety/privacy/legal/authorization rules, unresolved material contradiction, or failed prerequisite requires STOP, escalation, or a new Gene decision.

Do not treat these as stop conditions:

- a command finished;
- an installer completed;
- a verification substep passed;
- a tool returned output;
- a progress/status message was sent;
- the next step is merely mechanical;
- a different authorized adapter/tool is required;
- the work has taken a long time.

## 3. Human-boundary resumption

When a genuine human-only boundary is reached, state exactly what human action is required and why execution cannot cross that boundary autonomously.

After the boundary is satisfied, resume the already-authorized task automatically from the preserved verified state. Do not require Gene to restate "continue," "go," "next," or equivalent unless the human action materially changed the objective, scope, authority, or evidence state.

## 4. Progress-update behavior

For multi-step work, provide concise progress updates when useful, especially when execution is long-running or a material finding changes the path.

Progress updates must not be phrased or treated as final task completion unless a closure condition in §2 is actually met.

If the interface requires a message while tools continue, use commentary/progress communication and keep executing. Do not convert communication into a conversational handoff.

## 5. Verification and closure

Before declaring completion, verify the resulting state required by the governing task. Apparent success, command exit, UI acknowledgement, or process existence alone remains insufficient.

When a later step fails, preserve verified completed state and reopen only the failed boundary unless evidence invalidates earlier state.

## 6. Correction record

**Evidence / provenance:** Repeated field observations in DACP endpoint-recovery work on 2026-09-15/16, culminating in Gene's explicit 2026-09-16 correction that intermediate "coffee breaks" were forcing unnecessary re-prompts despite known executable next steps.

**Existing rule:** Project Instructions 0.4 states that Gene decides, the AI executes, mechanical work should not be returned to Gene, and execution should resume after a human-only boundary.

**Defect:** The existing rule did not explicitly bind turn closure and progress-report semantics, allowing an intermediate status response to function as an accidental stop.

**Refinement:** Bind conversational closure to objective completion, a genuine human-only boundary, or a governed STOP; explicitly classify progress messages as non-terminal; require automatic resumption after the boundary ends.

**Trigger:** Active DACP task has remaining authorized mechanical work after an intermediate result or progress update.

**Intended scope:** DACP-governed execution and tool-use workflows. It does not create authority outside the user's existing authorization or the project's governing rules.

**Success criterion:** No additional Gene prompt is required merely to continue known authorized mechanical work between substeps. Human input is requested only at a genuine human-only boundary or material decision point.

**Regression test:** In a multi-step task with three executable mechanical substeps and no human-only boundary, the AI must execute all three and verify the endpoint without stopping after substep one or two. In a variant where substep two requires user authentication, the AI must stop at authentication, state the exact required action, and automatically resume substep three after authentication is satisfied without requiring a separate "continue" instruction.

**Regression risks:** Over-continuation after a material scope change; failure to surface a real human-only boundary; excessive progress chatter. Existing authority, safety, privacy, consequence, reversibility, and verification controls remain binding and override continuation when they require STOP or escalation.

**Privacy implications:** None beyond existing controls. Continuation never expands data access, credential handling, connector scope, or disclosure authority.

**Status:** VERIFIED CORRECTION CANDIDATE PENDING CANONICAL READ-BACK AT CREATION; ACTIVE only after canonical persistence and independent read-back verification.
