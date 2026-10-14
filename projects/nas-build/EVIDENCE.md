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

## 2026-10-13 installation, network, and drive-health evidence

- TOOL-VERIFIED (PowerShell on Envy): official TrueNAS 25.10.7 SHA-256 `54ce9441ce66966a392e28f63604ca3c2c083d0bec4db7bb5af2f74f7a007c8e`; `TrueNAS-SCALE-25.10.7-VERIFIED.iso` MATCH; `TrueNAS-SCALE-25.10.7.iso` (b0d5c3dd...) and `.fresh.iso` (3723959c...) NO_MATCH. PNY USB 2.0 FD (serial 087E013260C0) written and read back with matching hash: `RESULT=TRUENAS_USB_WRITTEN_VERIFIED`.
- TOOL-VERIFIED: write to 7.5 GB "Generic Flash Disk" failed at ~1,024 MB with "The device is not ready."
- IMAGE-EVIDENCED: TrueNAS installer and first boot with HBA installed; `mpt2sas_cm0` loaded; eight `ST12000VN0008-3M SC60` direct-access devices at scsi 0:0:0-0:0:7.
- IMAGE-EVIDENCED: installer showed `vfat` on CT250MX500SSD1 and no filesystem on Patriot Burst Elite; erase warning listed only the Crucial.
- TOOL-VERIFIED (`ip -br link/addr`): `enp6s0` NO-CARRIER on UDM port 3 before VLAN change; link UP on switch; DHCP initially missed after slow link-up; re-applied via console interface Save -> address 192.168.40.14 (IoT); after UDM port 3 set to VLAN 20 -> 192.168.20.14.
- CLAUDE-OBSERVED (UniFi web UI): UDM Pro port 3 native VLAN set to Family Network (20) and re-read as saved; client `truenas` (fc:9d:05:06:49:fe) fixed IP 192.168.20.14 with Virtual Network Override off, re-read after page reload. An accidental Virtual Network Override (IoT) tick during editing was found and cleared before final save.
- TOOL-VERIFIED (`smartctl -H -A`): sdi CT250MX500SSD1 PASSED, Power_On_Hours 2019, Percent_Lifetime_Remain normalized 075 (raw 25 used), Reallocate_NAND_Blk_Cnt 0, Reported_Uncorrect 0, Current_Pending_ECC_Cnt 0. sdj Patriot PASSED, Power_On_Hours 3, Reallocated_Sector_Ct 0, Reported_Uncorrect 0.
- TOOL-VERIFIED (`smartctl -t long`): long tests started on sda-sdh; reported completion times Wed 2026-10-14 04:13:45-06:06:45 EDT.
- TOOL-VERIFIED: `pool-gate.service` started; log shows `START pool_gate (pool=tank model=ST12000VN0008 expect=8)` and `WAIT 8 drive(s) still testing` at 2026-10-13 14:58:43 EDT.
- USER-STATED-EXPLICIT: Amazon accepted return of the original defective 8700G.

## 2026-10-14 evidence

- TOOL-VERIFIED (gate log): 04:29:07 ALL 8 LONG TESTS PASSED; `midclt call -job` rejected ("unrecognized arguments: -ob"), RESULT=FAILED_POOL_CREATE, nothing created. 08:00:38 CREATE tank RAIDZ2 sda..sdh; 08:00:47-48 DATASET immich/plex/nextcloud/general; 08:00:49 RESULT=SUCCESS.
- TOOL-VERIFIED (audit 08:06): boot-pool 232G ONLINE (single disk, pre-reinstall); tank 87.3T raw ONLINE, raidz2-0 8 members, 0/0/0 errors; avail 61.9T; sda-sdh PASSED + Extended offline Completed without error; enp6s0 192.168.20.14/24; version 25.10.7.
- IMAGE-EVIDENCED: System -> Update 25.10.7 "System is up to date", profile MISSION_CRITICAL.
- USER-STATED-EXPLICIT 11:14-11:19: restart before reinstall showed no video, disk activity, LSI LED flashing, Digi-Debug 80/81. 11:41: Gene shut down, reinstalled to both SSDs, uploaded config; console then showed web UI address normally.
- IMAGE-EVIDENCED 11:45: Boot Pool Status boot-pool ONLINE, mirror-0 with sde3 and sdj3 ONLINE, 0 errors. Storage Dashboard: tank 1 x RAIDZ2 8 wide 10.91 TiB, usable 61.93 TiB, "Online, no errors", scheduled scrub Sundays 00:00, Auto TRIM off.
- IMAGE-EVIDENCED 11:51: disk temperature reports, IronWolf maxima 43-49 C over the prior hour.
- IMAGE-EVIDENCED/USER-STATED: GMail OAuth applied (From Home TrueNas saweba4master1@gmail.com); test mail worked; test alert worked; fresh config backup downloaded; cron job "Monthly SMART long test" at 01:00 day 1, user root, enabled.

