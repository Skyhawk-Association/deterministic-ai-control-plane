# DACP broker v0

A deliberately tiny experiment to remove Gene from the mechanical relay path between OpenAI and Anthropic while preserving model independence.

## What it does

- Sends the exact same task/evidence string to OpenAI and Anthropic.
- Dispatches both calls before consuming either result, so neither provider sees the other's answer.
- Performs **no automatic retries**.
- Writes a local append-only JSONL audit record. The input itself is not logged, only its SHA-256 hash.
- Can deterministically verify a known exact answer with `--expect-exact`.
- Treats model agreement without an objective verifier as `SUPPORTED_AGREEMENT`, never as proof.
- Makes no consequential external actions.

## Terminal states

- `VERIFIED_MATCH` - both providers match an objective expected string.
- `SUPPORTED_AGREEMENT` - both independently return the same text, but there is no objective verifier.
- `DISAGREEMENT` - successful provider outputs differ, or one/both fail an exact-answer verifier.
- `UNRESOLVED` - a provider call failed or has an uncertain/PENDING outcome.

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

## First live experiment

Use a synthetic exact-answer task first:

```sh
python3 dacp_broker.py \
  --prompt 'Return exactly: DACP-BROKER-V0-TEST' \
  --expect-exact 'DACP-BROKER-V0-TEST' \
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

No agent framework, vector database, message bus, recursive debate, automatic heuristic promotion, autonomous repair, external side effects, or dashboard. This is a broker experiment, not a startup pitch wearing a trench coat.
