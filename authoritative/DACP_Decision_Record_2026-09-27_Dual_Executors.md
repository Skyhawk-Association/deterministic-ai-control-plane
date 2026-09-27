# DACP Decision Record 2026-09-27 — Dual Executors and Git Passdown

**Status:** AUTHORITATIVE PROJECT DECISION / GENE DECISION
**Decided:** 2026-09-27 (Gene)
**Effective:** upon canonical persistence and independent read-back
**Supersedes:** 0.5's retirement of ChatGPT and the Executor Transfer decision record of 2026-09-23 (both kept as provenance)

## Decisions

1. **Two executors.** Claude and ChatGPT are both authorized executors, used one at a time as Gene chooses. Each may plan, code and change the projects it is used on. No mutual agreement is required; the tunnel (one AI checking the other) happens only when Gene asks.
2. **Shared passdown in Git.** LOST-D lives at projects/skyhawk/LOST-D.md in this public repository. Every session starts by reading it and projects/skyhawk/RULES.md. Every verified consequential step updates LOST-D in the same run as the change.
3. **Governing references readable without login.** The Skyhawk Working Rules and the Drupal Environment Reference moved to projects/skyhawk/RULES.md and projects/skyhawk/ENVIRONMENT.md (sanitized). Their Drupal pages (nodes 49418, 49461) and the Drupal LOST-D page (2479) are pointers.
4. **No secrets in public files:** no passwords, keys, token links, member personal data, backup contents or server addresses.

## Evidence

Claude sessions hit hard context limits, so work must be able to change hands mid-stream. From 2026-09-23 to 2026-09-27 both AIs repeatedly worked around established rules and references that existed only behind the site login or in chat history. Publishing the state and rules where either AI can read them directly removes that dependency.

Commits: cb10015 (LOST-D to Git), f9ef29d (Rules to Git), 86ce6d8 (Drupal pointers), 7cacabe (Environment Reference to Git), 69fa3b1 (LOST-D freshness note).

## Known limitation

Public raw GitHub URLs can lag a few minutes behind a push. Right after a push, verify with git (clone or ls-remote).
