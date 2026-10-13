# NAS Build Evidence Index

This file records evidence that materially affects build decisions. It is not a substitute for the current-state file.

## Verified observations

- AM5 CPU was visually observed seated and then latched by the retention mechanism.
- AMD stock cooler was physically installed.
- Corsair DIMMs were visually confirmed in DIMMA2 and DIMMB2.
- Seasonic FOCUS GX-750 passed a bench power-on test using the paper-clip method described by Seasonic.
- CS383 interior photos established that the pre-routed case cable bundle is behind the motherboard tray on the cable-management side.
- Windows PowerShell produced `RESULT=TRUENAS_ISO_VERIFIED` for the TrueNAS 25.10.7 installer image.

## Useful photo set

The following photo classes are useful enough to retain as public project evidence if cropped to hardware-only content and stripped of unnecessary serial/background information:

1. Motherboard assembly showing installed CPU cooler and A2/B2 memory population.
2. CS383 motherboard-tray / rear cable-management view establishing routing and standoff area.
3. CS383 interior overview showing motherboard area, drive/backplane area, and PSU bay relationship.
4. Seasonic modular connector panel showing the actual PSU connector layout used for this build.

Photos whose primary value is only transient troubleshooting should not be retained.

## Current persistence status

The useful photos exist in the active ChatGPT session but have not yet been persisted as Git objects through the currently qualified GitHub text-write path. They are therefore **not canonical evidence yet**.

When a binary-capable Git write path is available, place selected, privacy-safe images under:

`projects/nas-build/evidence/photos/`

Use descriptive names rather than chat-upload IDs, for example:

- `2026-10-03-motherboard-cpu-cooler-ram.jpg`
- `2026-10-03-cs383-motherboard-tray-rear-routing.jpg`
- `2026-10-03-cs383-interior-layout.jpg`
- `2026-10-03-seasonic-modular-panel.jpg`

After each binary write, independently read back the Git object/path before treating the image as shared evidence.

## HBA purchase provenance

Gene supplied the original shopping-cart text on 2026-10-04. It identifies the HBA purchase listing as:

- Newegg Marketplace.
- Seller: Fastparts.
- Product description: `DELL / LSI 6GB/S HOST BUS ADAPTER HBA PCI-E 3.0 X8 LSI00301 -US SAS9207-8i`.
- Listed price: $57.49.
- The supplied cart text does not list any SFF-8087-to-SATA breakout cables as separate purchased items or included accessories.
- On 2026-10-05, Gene supplied photographic evidence of two Cable Matters boxes labeled `Internal Mini-SAS to SATA Forward Breakout Cable - 1.6ft / 0.5m [SFF-8087 to 4x SATA]`, model `104016-0.5m`. The required pair is therefore physically in hand.
- Both breakout cables were then connected to the LSI 9207-8i, and all eight breakout SATA branch connectors were reported securely attached to the CS383 numbered backplane ports.

This establishes purchase-source provenance and documents that the required breakout-cable pair was later received; it does not by itself prove what accessories the seller's product page promised at checkout.

## HBA document intake

Three HBA-related PDFs were supplied directly in the working session and hashed before canonical indexing:

- `LSISAS9207-8i_UG_v2-2.pdf` — SHA-256 `61bb97fd099f10ce07d2489510acdd7f0ee3fefcb63db7c866071d4e05cc4df6`.
- `LSI_SAS_9207-8i_QIG.pdf` — SHA-256 `e2b5402d3c3ae32420bec4e8331491d8e4b522550a5fa8b7c82a7d23f1749f04`.
- `SAS2_Flash_Utility_Software_Ref_Guide.pdf` — SHA-256 `04708a22726274be2ea673940611b332993f367b94f8aaf782311f498182c978`.

The exact binaries remain outside public Git under the project binary-document policy. Their identities, hashes, official source links, and build-relevant facts are persisted in `REFERENCES.md` and `references/HBA_LSI_SAS9207-8i.md`.

## 2026-10-12 POST recovery evidence

- USER-STATED-EXPLICIT: Gene reports an outside tech center diagnosed a failed Ryzen 7 8700G and replaced/handled the CPU. The exact diagnostic method used by the tech center was not recorded, so the failed-CPU causal diagnosis is not independently verified in this project evidence.
- USER-STATED-EXPLICIT: After service, Gene observed successful POST and MSI Click BIOS X.
- USER-STATED-EXPLICIT: BIOS string observed: E7E59AMSI.2AC4, dated 2026-09-02.
- USER-STATED-EXPLICIT: BIOS detected Ryzen 7 8700G and 64 GB RAM as 2x32 GB in A2/B2 at 4800 MT/s with EXPO off.
- USER-STATED-EXPLICIT: BIOS idle CPU temperature observed around 66 C at about 1.428 V; Gene reports the CPU cooler fan is operating.
- USER-STATED-EXPLICIT: BIOS clock observed incorrect at approximately 2026-04-06/07.
- CORRECTION / USER-STATED-EXPLICIT 2026-10-13: Gene clarified that the Patriot Burst Elite 240 GB, not the Crucial MX500, has the "NEMONG COMPUTER" sticker and booted the existing Korean Windows 10 installation while offline.
- Historical electrical evidence before service: PSU paper-clip test passed in Normal fan mode; +5VSB measured 5.0 VDC; PS_ON was measured about 5 V at rest and 0 V when JFP1 6/8 were shorted, showing the board asserted PS_ON.


- IMAGE-EVIDENCED 2026-10-13: MSI F11 boot menu shows `Windows Boot Manager (SATA S1: CT250MX500SSD1)` and `UEFI: PNY USB 2.0 FD PMAP, Partition 1` while the Patriot is disconnected. Therefore the Crucial MX500 is not presently a blank/clean disk from the firmware's perspective; it contains or exposes a Windows EFI boot entry. This does not by itself contradict Gene's correction that the Patriot was the used Korean SSD, because the image does not identify the location of the full Windows installation.

- IMAGE-EVIDENCED 2026-10-13: After Gene selected `UEFI: PNY USB 2.0 FD PMAP, Partition 1` in the MSI F11 menu and pressed Enter, the firmware returned to the same boot-device menu instead of launching the TrueNAS installer. The PNY device is enumerated by UEFI, but the current media does not successfully hand off into the installer on this machine.

## 2026-10-13 HBA / video troubleshooting evidence

- USER-STATED-EXPLICIT: Motherboard HDMI video works and BIOS is usable with the LSI 9207-8i removed.
- USER-STATED-EXPLICIT: Installing the LSI 9207-8i causes black/no motherboard HDMI video in both PCI_E1 and a lower full-length PCIe slot.
- USER-STATED-EXPLICIT: IGD/UMA graphics settings, UEFI mode, disabling Re-Size BAR, disabling Above 4G, and one CMOS clear did not restore video with the HBA installed.
- USER-STATED-EXPLICIT: Both boot SSDs were disconnected for these tests.
- USER-STATED-EXPLICIT: With the HBA removed and no boot SSD connected, the board reached A9 / 00 and the green BOOT LED, consistent with reaching setup / no bootable device.
- USER-STATED-EXPLICIT: With the HBA in the third full-length PCIe slot, no SFF-8087 storage cables attached to the HBA, and both boot SSDs disconnected, the board displayed `00` with the green BOOT LED and still produced no motherboard HDMI video.
- UNRESOLVED: HBA firmware/mode and option-ROM state are not identified.
- USER-STATED-EXPLICIT: Setting Chipset Gen Switch to Gen3 did not restore motherboard HDMI video with the HBA installed.
- USER-STATED-EXPLICIT: Switching firmware mode from UEFI to CSM caused loss of the previously working no-HBA video/POST path after save/reboot.
- USER-STATED-EXPLICIT: Clearing CMOS afterward restored normal POST/video with the HBA removed and both boot SSDs disconnected.

