# NAS Transition

## Intended role

The NAS is future private infrastructure, not a new human workflow.

When available it should provide, as justified by evidence and design:

- clone/backup/recovery for the public DACP Git repository;
- protected storage for private/raw data that does not belong in public Git;
- future private telemetry/history/indexes under DACP privacy and retention rules;
- future application services after application implementation is separately authorized.

## Transition gate

Do not make the NAS canonical merely because files were copied to it. Promotion requires defined migration scope, integrity/coverage checks, backup/recovery evidence, access-control verification, and read-back verification.

## Desired result

GitHub can remain the public dissemination/version surface while the NAS becomes the protected operational substrate. Mac, Windows, and Pixel continue to behave as replaceable clients/execution surfaces.
