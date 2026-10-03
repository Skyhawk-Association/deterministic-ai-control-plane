# NAS Build References

## Primary hardware references

### MSI MAG X870E TOMAHAWK WIFI

- Role: motherboard authority.
- Official user guide:
  https://download.msi.com/archive/mnu_exe/mb/MAGX870ETOMAHAWKWIFI_English.pdf
- Working-session copy name: `MAGX870ETOMAHAWKWIFI_English.pdf`
- Use for: standoffs/mounting-hole pattern, DIMM population, PCIe slots, SATA headers, front-panel headers, power connectors, fan headers, BIOS/POST.

### SilverStone CS383

- Role: chassis / hot-swap backplane authority.
- Working-session copy name: `Multi-CS383-Manual.pdf`
- The manufacturer manual already supplied for this build remains the primary case reference.
- Use for: motherboard standoff placement, chassis install sequence, drive/backplane wiring, PSU location/orientation constraints, internal 2.5-inch mounting points, cable routing.

### Seasonic FOCUS GX-750

- Role: PSU and modular-cable authority.
- Official installation guide:
  https://seasonic.com/wp-content/uploads/2024/09/QIG-PSU.pdf
- Official general user manual:
  https://seasonic.com/wp-content/uploads/2024/04/Manual-PSU-multilingual.pdf
- Official pinout / family chart:
  https://seasonic.com/wp-content/uploads/2024/09/Pinouts-V2.pdf
- Working-session copy names:
  - `QIG-PSU.pdf`
  - `Manual-PSU-multilingual.pdf`
  - `Pinouts-V2.pdf`
- Safety rule: use only modular cables supplied for / verified compatible with this Seasonic PSU. Do not infer modular-cable interchangeability from connector fit.

### Broadcom / LSI SAS 9207-8i

- Role: HBA authority for the eight data-drive path.
- Detailed local reference summary: [`references/HBA_LSI_SAS9207-8i.md`](references/HBA_LSI_SAS9207-8i.md)
- LSI SAS 9207-8i User Guide, version 2.2:
  https://docs.broadcom.com/doc/12353331
  - uploaded working copy: `LSISAS9207-8i_UG_v2-2.pdf`
  - SHA-256: `61bb97fd099f10ce07d2489510acdd7f0ee3fefcb63db7c866071d4e05cc4df6`
  - size: 193741 bytes
- LSI SAS 9207-8i Quick Installation Guide:
  https://docs.broadcom.com/doc/12352384
  - uploaded working copy: `LSI_SAS_9207-8i_QIG.pdf`
  - SHA-256: `e2b5402d3c3ae32420bec4e8331491d8e4b522550a5fa8b7c82a7d23f1749f04`
  - size: 342608 bytes
- SAS2Flash Utility Reference Guide:
  https://docs.broadcom.com/doc/12353205
  - uploaded working copy: `SAS2_Flash_Utility_Software_Ref_Guide.pdf`
  - SHA-256: `04708a22726274be2ea673940611b332993f367b94f8aaf782311f498182c978`
  - size: 298520 bytes
  - classification: historical SAS2Flash command reference, Preliminary v1.0 (November 2009); it predates the SAS2308-based 9207-8i and does not by itself authorize a firmware operation on this card.
  - public-repo restriction: the uploaded document itself states that it is proprietary/confidential and not to be disclosed to third parties without permission, so the binary is intentionally not committed to this public repository.
- Broadcom firmware-flashing knowledge base:
  https://www.broadcom.com/support/knowledgebase/1211161501344/flashing-firmware-and-bios-on-lsi-sas-hbas
- Broadcom support downloads search:
  https://www.broadcom.com/support/download-search

Before flashing firmware, identify the exact current HBA firmware/mode and bind the action to the exact card. Do not flash merely because a later package exists.

## Primary software references

### TrueNAS Community Edition 25.10

- Version root:
  https://www.truenas.com/docs/scale/25.10/
- 25.10 installation section:
  https://www.truenas.com/docs/scale/25.10/gettingstarted/install/
- Installing TrueNAS:
  https://www.truenas.com/docs/scale/25.10/gettingstarted/install/installingscale/
- 25.10 hardware guide:
  https://www.truenas.com/docs/scale/25.10/gettingstarted/scalehardwareguide/
- 25.10 version notes:
  https://www.truenas.com/docs/scale/25.10/gettingstarted/scalereleasenotes/

Current install media checkpoint for this project: TrueNAS 25.10.7 ISO has been verified locally before USB flashing. Preserve the exact checksum evidence when the installer-media step resumes.

## Secondary project guides

Working-session planning guides:

- `NAS_Build_Guide.pdf`
- `NAS_Software_Setup_Guide.pdf`

These are useful procedural/planning references, not primary authorities. Known stale content includes the original six-drive RAIDZ2 plan; the current hardware build has eight 12 TB IronWolf drives. Any other conflict with manufacturer documentation, current TrueNAS documentation, or verified physical state must be resolved in favor of the higher source.

## Binary-document policy

This public DACP repository should normally store durable links, source identity, version, and checksums rather than duplicate third-party copyrighted PDFs without a specific need and redistribution basis. User-created build evidence may be stored when useful and privacy-safe.
