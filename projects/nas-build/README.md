# NAS Build Project

## Purpose

This directory is the durable public working package for the home NAS build. It exists so multiple authorized AI executors can resume the same build from Git instead of depending on chat history, copied summaries, or model recollection.

Root `CURRENT.md` remains the canonical bootstrap for DACP governance. This directory governs only the current NAS-build project state.

## Start here

1. `CURRENT.md` — verified build state, unresolved gates, and next sequence.
2. `REFERENCES.md` — manufacturer / TrueNAS source set and source hierarchy.
3. `EVIDENCE.md` — observed evidence and selected-photo policy.

## Source hierarchy

For this project:

1. live physical state and verified test results;
2. current manufacturer documentation for the exact component;
3. current TrueNAS documentation for the exact software version;
4. project build/setup guides as secondary planning material only.

The project build guides are not allowed to override manufacturer documentation or verified physical reality. They currently contain at least one known stale assumption: six 12 TB data drives rather than the current eight-drive build.

## Public/private boundary

This repository is public. Do not place credentials, private network information, private operational logs, unnecessary serial numbers, or identifying household/background imagery here.

Selected hardware photos may be kept as evidence when they materially reduce ambiguity. Crop or exclude irrelevant personal/background material before public persistence.

## Persistence rule

A source, photo, or state claim is not considered shared merely because it exists in a ChatGPT or Claude conversation. Shared project material must be persisted to Git and independently read back before another executor may treat it as durable state.
