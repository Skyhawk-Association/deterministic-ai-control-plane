# DACP Required Pipe Qualification 0.1

## Change Synopsis

- Establishes an end-to-end qualification rule for any required persistence, evidence, state, or handoff pipe.
- A pipe is not operational merely because an executor can write to it or read from it separately.
- Requires write -> persist -> consumer read-back -> verification by the intended executor path before the pipe may be relied on.
- Requires a pre-proven alternate authorized route when an adapter can fail independently of the underlying capability.
- Prohibits shifting machine-retrievable transport work to Gene merely because one adapter failed.
- Adds explicit regression coverage for write-only/read-only half-pipes and adapter failover.

**Status:** AUTHORITATIVE PROJECT CONTROL / ACTIVE / GENE DECISION  
**Effective:** upon canonical persistence and independent read-back verification  
**Decision record:** authoritative/DACP_Decision_Record_2026-09-27_Required_Pipe_Qualification.md

## 1. Failure addressed

Field use repeatedly exposed a false-pipe pattern:

1. an executor was required to persist or hand off state;
2. one adapter could write but the executor could not reliably consume the resulting state, or the reverse;
3. the adapter failure was treated as loss of the underlying capability;
4. Gene was asked to carry, paste, restate, or otherwise transport machine-retrievable information;
5. work became stranded or state drifted between executors.

The defect is not lack of storage. The defect is accepting a partial route as an operational pipe.

## 2. Required-pipe definition

A required pipe is any storage, evidence, state, handoff, or coordination route that DACP depends on for continued execution.

A required pipe is QUALIFIED only when the intended executor can prove the complete route:

PRODUCE -> WRITE -> PERSIST -> CONSUMER READ -> VERIFY -> CONTINUE

The write and read sides may use different authorized adapters, but the full route must be proven for the executor that depends on it.

## 3. Qualification rule

Before designating a pipe required, bind and test:

- producer/executor identity;
- primary write adapter;
- persistence owner;
- consumer/read adapter;
- exact object identity or immutable content token/hash;
- success endpoint;
- authorized fallback adapter or route when one exists;
- stop condition when no competent route remains.

PASS requires:
- the producer writes the test object;
- persistence is independently observable;
- the intended consumer retrieves the persisted object without Gene transporting it;
- exact expected content, identity, generation, hash, or token is verified;
- the executor continues from that retrieved state.

A write acknowledgement alone is not PASS.
A read capability without proven write persistence is not PASS.
Two separately functioning components do not prove the pipe.

## 4. Adapter failure is not capability failure

An adapter is only one route to a capability.

When a required-pipe adapter fails:
1. classify the failure as adapter, authentication, execution-context, remote-endpoint, persistence-owner, or capability failure;
2. preserve verified completed state;
3. automatically resolve and use a pre-authorized competent alternate surface when available;
4. re-run the failed pipe segment and read-back verification;
5. declare the capability unavailable only after competent authorized alternatives are exhausted or evidence requires STOP.

Do not ask Gene to carry machine-retrievable payloads merely because the first adapter failed.

## 5. Executor-specific routes

Different executors may use different adapters to the same canonical owner.

A required pipe must therefore record the executor-specific proven route rather than assume equivalent behavior from tools with similar product labels.

For Git, a machine-native local clone plus push plus independent canonical read-back may qualify even when a direct connector write adapter is unavailable.

For locally synchronized private state, a filesystem route may qualify independently of a semantic connector route if authority and privacy constraints permit it.

## 6. Requalification triggers

Requalify a required pipe when:
- credentials or account context change;
- executor or execution surface changes;
- adapter behavior changes;
- storage owner or path changes;
- a previously passing write/read-back fails;
- a user is asked to transport machine-retrievable state;
- evidence shows stale, divergent, or unreadable persisted state.

Until requalified, the affected pipe is DEGRADED or FAILED, not silently assumed operational.

## 7. Success evidence

Required-pipe success must include evidence of both persistence and consumer read-back.

For Git, qualifying evidence may include:
- local commit SHA;
- successful push;
- remote main HEAD;
- independent fetch/read of the exact file/blob/content expected.

For other stores, use the equivalent durable identity and read-back evidence.

## 8. Field evidence

On 2026-09-27, a direct ChatGPT GitHub connector write was blocked after an earlier connector write had succeeded. The repository capability itself remained available.

ChatGPT then used the authorized Windows execution surface through Desktop Commander:
- local clone: C:\Users\genea\dacp-work\dacp;
- Git write/push test commit: cad7d174f415c19d704187ad1026220244430f7d;
- independent GitHub read-back retrieved the exact test token;
- the previously blocked LOST-D update was then committed through the same route as d8255d12a18228f797a506f851b64f63e7591f92;
- independent GitHub read-back confirmed the resulting LOST-D state.

Gene transported no payload between producer and consumer.

## 9. Regression requirements

A conforming runtime must fail any required-pipe plan that:
- proves only write or only read;
- treats one adapter failure as capability failure while an authorized alternate exists;
- asks Gene to paste or carry machine-retrievable output;
- claims persistence without read-back verification;
- assumes two executors share equivalent adapters without executor-specific proof.

The regression matrix carries the executable pass/fail fixtures.

## 10. Privacy and scope

Pipe qualification does not expand authority, credentials, repository scope, privacy scope, or data classification.

The test payload must use the minimum non-sensitive content necessary to prove the route.
