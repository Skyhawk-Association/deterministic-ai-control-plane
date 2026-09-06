# DACP Public Test Surface

Real use is the primary adversarial test surface for the active heuristic specification.

This directory is for public regression/adversarial test descriptions and later machine-executable tests when implementation is separately authorized.

Current required regression themes include:

- instruction/data separation;
- authority spoofing/replay;
- verifier independence and stale verification;
- delegated privilege composition;
- mutable-target / TOCTOU protection;
- privacy and retention boundaries;
- rule conflict and poisoned telemetry;
- provider-neutral history/inert archival content;
- human/AI role allocation under H-017, including recursive testing and cross-platform execution without avoidable human mechanical handoff.

Passing a specification-level test does not prove an application implementation is secure or correct.
