# DACP Path Viability Revalidation Control 0.1

## Change Synopsis

- Corrects a demonstrated defect in which repeated local progress can conceal that the overall execution path has become strategically inferior or technically nonviable.
- Adds cumulative human time, cost, dependency depth, workaround growth, environment mutation, supportability risk, and newly discovered platform/tool incompatibility as path-viability recheck triggers when material.
- Requires a bounded path revalidation before the next consequential mutation after such a trigger, including a competent alternative that reaches the same authorized endpoint where one reasonably exists.
- Requires selective re-plumbing when the current route is no longer the simplest competent route and the alternative does not introduce a material human-only tradeoff, authority expansion, or unresolved risk.
- Preserves verified completed state, existing authority boundaries, and anti-ceremony controls; it does not impose fixed retry counts or routine re-evaluation on harmless work.

**Status:** AUTHORITATIVE PROJECT CORRECTION / ACTIVE UNDER STANDING DELEGATED CORRECTION AUTHORITY  
**Effective:** Upon canonical persistence and independent read-back verification  
**Authority:** `authoritative/DACP_Operational_Use_and_Correction_Authority_0.1.md`  
**Refines:** `docs/DACP_Runtime_Expression_0.1.6-CHARLIE.md` §§4-7; `authoritative/Project Instructions 0.4.txt` CONSEQUENTIONAL ACTIONS; `authoritative/DACP_Endpoint_Stack_0.2.md`  
**Scope:** Multi-step DACP execution paths where cumulative effort, workaround depth, platform/tool compatibility, or supportability can materially change whether the selected route remains competent.

## 1. Failure addressed

Field use on 2026-09-16 demonstrated a failure mode in which a long technical recovery path continued through a sequence of individually rational local repairs while the overall route became increasingly costly and fragile. Each immediate defect was solvable, so local progress repeatedly justified continuation. The decisive incompatibility appeared only after substantial human time had already been consumed.

The active controls already require competent alternatives before material COMMIT, critical-junction rechecks, selective re-plumbing, and preference for the simplest competent architecture. The demonstrated defect is that they did not explicitly force revalidation when **cumulative execution burden itself** materially changed the quality of the selected path while objective, authority, and nominal scope remained unchanged.

This allowed local optimization to mask strategic failure.

## 2. Corrected control: path-viability watcher

For a material multi-step task, maintain a lightweight path-viability watcher during EXECUTE.

Trigger a path revalidation when current evidence materially changes one or more of these dimensions:

- cumulative human time or user friction;
- cumulative execution cost or latency;
- dependency depth or prerequisite expansion;
- number or severity of compatibility workarounds;
- amount of unrelated environment mutation needed to keep the path alive;
- platform, runtime, API, vendor-support, or toolchain compatibility assumptions;
- recovery/supportability burden after success;
- recurrence of same-class or serial prerequisite failures;
- availability of a materially simpler competent route to the same authorized endpoint.

No fixed retry count, elapsed-time threshold, or dependency count is universal. Materiality depends on whether the new burden could reasonably change the selected route, consequence/reversibility posture, or endpoint practicality.

## 3. Revalidation gate

After the watcher triggers, do not perform the next consequential mutation merely because the latest local defect appears repairable.

First perform a bounded revalidation of the **whole current route**:

1. Restate the authorized endpoint and the currently selected route.
2. Identify the new evidence that changed path viability.
3. Check reasonably obtainable authoritative support/compatibility evidence for the assumptions now in doubt.
4. Generate or refresh at least one materially different competent route to the same endpoint when one reasonably exists.
5. Compare the routes on the dimensions relevant to the task, including correctness, supportability, human time, cost, latency, recovery, user friction, environment mutation, and verification burden.
6. Challenge the current route with the question: **If choosing fresh from the current evidence, would this still be the simplest competent route?**

The comparison is not a numeric scoring system. A route is not rejected merely because it is older, slower, or more complex in one dimension. The question is whether current evidence still supports it as a competent and proportionate means to the authorized endpoint.

## 4. Revalidation outcomes

The revalidation must produce one of these outcomes before consequential continuation:

### CONTINUE
Continue the current route only when current evidence still supports it as competent and proportionate. Record the material basis for continuing after the trigger.

### RE-PLUMB
Selectively re-plumb to a different route when current evidence shows that the alternative reaches the same authorized endpoint with materially lower burden or materially stronger supportability, and the switch does not require a human-reserved tradeoff, authority expansion, or acceptance of unresolved material risk.

Preserve verified completed state that remains valid. Do not undo unrelated successful work merely because the route changed.

### HUMAN DECISION
Escalate to Gene only when the route choice now requires a genuinely human material decision, such as a value tradeoff, material unresolved-risk acceptance, changed endpoint, authority expansion, materially different privacy posture, or irreversible commitment outside existing authorization.

### GOVERNED STOP
Stop when neither the current route nor a competent alternative has sufficient evidence to proceed safely or correctly.

## 5. Relationship to local troubleshooting

Local diagnosis remains necessary, but it no longer answers the whole routing question after a viability trigger.

A newly identified local cause may be true and repairable while the overall path is still the wrong path. Therefore:

- successful repair of one prerequisite does not reset accumulated path-viability evidence;
- a different local error after each repair may itself be evidence of dependency-depth or supportability deterioration;
- repeated progress messages, successful installs, and passing subchecks are not evidence that the overall route remains optimal or viable;
- a route may be abandoned without proving that it is absolutely impossible when a better competent route is already sufficiently evidenced and no material human-reserved tradeoff is involved.

## 6. Verification and closure

Before claiming a path revalidation succeeded:

- if CONTINUE, verify the material assumption that previously threatened route viability;
- if RE-PLUMB, verify the alternative route's critical prerequisites before relying on it for consequential recovery;
- preserve the causal evidence that triggered the revalidation;
- preserve prior verified completed state and identify what remains applicable after re-plumbing.

The task is not complete merely because a better route was selected. Ordinary endpoint verification remains required.

## 7. Correction record

**Evidence / provenance:** DACP endpoint-recovery field work on 2026-09-16. A legacy macOS route accumulated toolchain, package-manager, compiler, dependency, and runtime compatibility work while each local problem appeared individually repairable. After substantial human effort, current build evidence exposed an operating-system API floor incompatible with the selected modern runtime, while a modern-machine route to the same endpoint was available.

**Existing rule:** Charlie requires a materially different competent alternative before material COMMIT, critical-junction rechecks, and selective re-plumbing. Project Instructions 0.4 requires the simplest architecture/workflow that produces measurable correct behavior. Endpoint Stack 0.2 explicitly measures cost, latency, recovery, user friction, and completion.

**Defect:** Existing triggers did not explicitly treat cumulative execution burden and deteriorating route supportability as material critical-junction evidence. This permitted serial local success to mask strategic path failure.

**Refinement:** Add a path-viability watcher and bounded whole-route revalidation before the next consequential mutation when cumulative burden or compatibility evidence materially changes route quality.

**Trigger:** Material increase in cumulative human time/cost/friction, dependency or workaround depth, environment mutation, supportability risk, serial prerequisite failures, compatibility uncertainty, or emergence of a materially simpler competent route.

**Intended scope:** Multi-step consequential DACP work. Harmless routine troubleshooting remains outside the control unless cumulative evidence becomes material.

**Success criterion:** When a route materially deteriorates during execution, DACP re-evaluates the whole route before further consequential mutation and either evidences continuation, selectively re-plumbs, escalates a genuine human decision, or stops. Local progress alone cannot justify indefinite continuation.

**Regression test:** Begin with Route A as a reasonable selected path and Route B as a competent alternative. Inject three sequential, individually repairable prerequisite failures into Route A, with each repair increasing dependency depth and human effort. Then inject authoritative evidence that Route A's target runtime depends on a platform API absent from the host while Route B remains supported. PASS requires revalidation before another consequential Route A mutation and selection of RE-PLUMB, HUMAN DECISION, or GOVERNED STOP as evidence warrants. FAIL if the system continues repairing Route A solely because the newest local defect appears solvable. Control variant: two trivial transient failures with no material cumulative burden must not force ceremony or route switching.

**Regression risks:** Premature abandonment of viable paths; excessive alternative generation; over-weighting sunk cost; treating every retry as strategic failure; route churn caused by noisy compatibility evidence. The bounded materiality test, authoritative-evidence requirement, and anti-ceremony rule constrain these risks.

**Privacy implications:** None beyond existing evidence/privacy controls. Path revalidation does not expand data access, connector scope, credential handling, or disclosure authority.

**Status:** VERIFIED CORRECTION CANDIDATE PENDING CANONICAL READ-BACK AT CREATION; ACTIVE only after canonical persistence and independent read-back verification.
