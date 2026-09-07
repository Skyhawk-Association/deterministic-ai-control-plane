# DACP broker v0

A deliberately tiny experiment to remove Gene from the mechanical relay path between OpenAI and Anthropic while preserving deterministic commitment rules.

## What it does

- Sends the exact same task/evidence string to OpenAI and Anthropic.
- Dispatches both initial calls before consuming either result, so neither provider sees the other's first answer.
- Performs **no automatic retries**.
- Writes a local append-only JSONL audit record. The input itself is not logged, only its SHA-256 hash.
- Can deterministically verify a known exact answer with `--expect-exact`.
- Treats model agreement without an objective verifier as `SUPPORTED_AGREEMENT`, never as proof.
- Optionally performs exactly one bounded peer-challenge round with `--peer-challenge`.
- Makes no consequential external actions.

## Bounded peer challenge

`--peer-challenge` is deliberately narrow and requires `--expect-exact`.

1. Both providers answer independently and those answers are fixed and logged.
2. Only after both initial calls succeed, each provider receives the other's initial answer exactly once.
3. The deterministic oracle is never disclosed to either provider.
4. Each provider may keep or revise its answer once. There is no second challenge round and no automatic retry.
5. The audit preserves initial and final provider results plus deterministic flags for rescue, degradation, and same-wrong-answer convergence.

Peer output is serialized inside a controller-generated challenge prompt and explicitly marked as untrusted data, not authority. Instructions embedded in a peer answer do not acquire control authority merely because another model reads them.

## Terminal states

- `VERIFIED_MATCH` - both providers match an objective expected string.
- `SUPPORTED_AGREEMENT` - both independently return the same text, but there is no objective verifier.
- `DISAGREEMENT` - successful provider outputs differ, or one/both fail an exact-answer verifier.
- `UNRESOLVED` - a provider call failed or has an uncertain/PENDING outcome.

With peer challenge enabled, the terminal state is based on final answers. The audit also preserves the pre-challenge state and per-provider initial/final verifier results, so a correct-to-wrong flip cannot be hidden by the final classification.

## Cost discipline

Defaults are intentionally cost-sensitive and output is capped at 300 tokens:

- OpenAI: `gpt-5.6-luna`
- Anthropic: `claude-haiku-4-5-20251001`

Override with `OPENAI_MODEL`, `ANTHROPIC_MODEL`, or CLI flags. Provider pricing changes over time; the broker controls token ceilings rather than pretending a stale hard-coded dollar estimate is authoritative.

## Credentials

Set credentials in the environment. Never put keys in Git or the audit log.

```sh
export OPENAI_API_KEY='...'
export ANTHROPIC_API_KEY='...'
```

## Blinded exact-answer experiment

```sh
python3 dacp_broker.py \
  --prompt 'Return exactly: DACP-BROKER-V0-TEST' \
  --expect-exact 'DACP-BROKER-V0-TEST' \
  --max-output-tokens 50
```

## One-round peer-challenge experiment

```sh
python3 dacp_broker.py \
  --prompt 'Solve the objectively checkable task and return only the final answer.' \
  --expect-exact 'KNOWN-ANSWER' \
  --peer-challenge \
  --max-output-tokens 50
```

Before spending API credit, the transport/audit path can be exercised without network calls:

```sh
python3 dacp_broker.py --prompt 'synthetic test' --dry-run
```

## Tests

No third-party packages are required.

```sh
python3 -m unittest -v test_dacp_broker.py
```

## Explicit non-goals for v0

No agent framework, vector database, message bus, recursive debate, multi-round consensus loop, automatic heuristic promotion, autonomous repair, external side effects, or dashboard. The peer-challenge option is one bounded reveal round, not a permission slip for the models to form a parliament.
