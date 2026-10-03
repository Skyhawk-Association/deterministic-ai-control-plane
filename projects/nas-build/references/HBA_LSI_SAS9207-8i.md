# LSI SAS 9207-8i Reference

## Exact hardware identity

The uploaded LSI SAS 9207-8i User Guide identifies the card as an LSI SAS 9207-8i HBA based on the LSI SAS 2308 controller. It provides eight internal 6 Gb/s SAS/SATA ports through two internal x4 mini-SAS SFF-8087 connectors and uses an x8 PCIe host interface.

## Build-relevant hardware facts

- PCIe host interface: x8, PCIe 3.0.
- Storage ports: eight internal 6 Gb/s SAS/SATA lanes.
- Internal connectors: two x4 SFF-8087 mini-SAS connectors, J5 and J6.
- Board size: 167.6 mm x 64.5 mm.
- Nominal power: 9.8 W.
- Worst-case power: 16.0 W.
- Operating temperature: 0 C to 55 C.
- Minimum airflow: 200 linear feet per minute.
- Heartbeat LED: CR1 blinks green to indicate general HBA activity.

## Installation authority

The 2014 User Guide and Quick Installation Guide agree on the material installation sequence:

1. Work ESD-safe and inspect the HBA.
2. Remove system AC power before installation.
3. Use the correct full-height or low-profile bracket for the chassis.
4. Install the HBA in an x8-capable PCIe slot and seat it fully.
5. Secure the bracket to the chassis.
6. Connect the two internal SFF-8087 SAS paths to the backplane / SATA or SAS devices.
7. Restore power only after the card and cabling are secured.

The quick guide specifies a maximum bracket-screw torque of 4.8 +/- 0.5 inch-pounds when changing the HBA mounting bracket.

## Firmware / SAS2Flash caution

The uploaded SAS2Flash Utility Quick Reference Guide is Preliminary Version 1.0 from November 2009. Its listed controller set includes SAS2004, SAS2008, SAS2108, and SAS2116; it does not list the SAS2308 used by the 9207-8i. Therefore:

- treat this PDF as historical syntax/reference material only;
- do not infer 9207-8i firmware compatibility from this guide alone;
- do not erase or flash the HBA until the exact adapter identity, current firmware, target firmware, tool build, and recovery path are verified from current Broadcom material.

The guide also documents destructive erase commands and explicitly states that erase operations cannot be undone. Those commands are outside the normal assembly path and require their own exact-target and recovery evidence.

## Uploaded source copies

| Document | Working filename | SHA-256 | Size |
| --- | --- | --- | ---: |
| LSI SAS 9207-8i User Guide v2.2, Oct 2014 | `LSISAS9207-8i_UG_v2-2.pdf` | `61bb97fd099f10ce07d2489510acdd7f0ee3fefcb63db7c866071d4e05cc4df6` | 193741 |
| LSI SAS 9207-8i Quick Installation Guide, Oct 2014 | `LSI_SAS_9207-8i_QIG.pdf` | `e2b5402d3c3ae32420bec4e8331491d8e4b522550a5fa8b7c82a7d23f1749f04` | 342608 |
| SAS2Flash Utility Quick Reference Guide, Preliminary v1.0, Nov 2009 | `SAS2_Flash_Utility_Software_Ref_Guide.pdf` | `04708a22726274be2ea673940611b332993f367b94f8aaf782311f498182c978` | 298520 |

## Public-repository handling

The public DACP repository keeps source identity, hashes, and build-relevant extracted facts. It does not duplicate these third-party binaries by default. The SAS2Flash PDF in particular carries an explicit proprietary/confidential notice against third-party disclosure, so its binary must not be committed to public Git without a verified redistribution right.
