# DACP Infrastructure Marching Orders 0.1

**Status:** ACTIVE OPERATING ORDERS / GENE DECISION  
**Scope:** Current DACP repository and supporting infrastructure  
**Purpose:** Keep the control system simple, portable, testable, and useful while the NAS comes online.

## 1. Maintain one permanent bootstrap address

`CURRENT.md` is the stable human/AI starting point. `CURRENT.json` is the machine-readable companion. They identify the current specification and the governing files required before consequential DACP work.

The bootstrap location must remain stable even as the active specification path/version changes.

## 2. Enforce a hard public/private boundary

Public Git contains only material intentionally suitable for public inspection and dissemination: specifications, public governance, public tests, public architecture, and sanitized/public evidence.

Secrets, credentials, private user data, raw private chat archives, confidential operational logs, organization secrets, and future application-private data do not belong in this repository.

## 3. Make devices replaceable

Mac, Windows, Pixel, terminals, SSH clients, Git apps, and future machines are execution adapters. No consequential DACP state should exist only because one device has a particular local directory.

Local clones are disposable working copies unless explicitly promoted through the authoritative Git process.

## 4. Make repository integrity self-evident

Material changes must be versioned, attributable, and read back after persistence before success is claimed. The current bootstrap identifies the active spec by repository path plus immutable Git blob identity where available.

A successful command, green UI, local file, or model statement is not proof that canonical state changed.

## 5. Let the NAS enter as infrastructure, not as a redesign

When the NAS is ready, it should clone/backup the public repository and host protected private state and future application services. GitHub may remain the public dissemination/version-control surface.

NAS introduction should not require changing the human/AI operating model or making any endpoint dependent on one physical device.
