# NAS Build Current State

Status date: 2026-10-27

## Objective

Assemble, verify, install, and commission the home NAS without relying on chat-memory continuity. The physical build must be verified before TrueNAS installation; TrueNAS configuration must be verified before application/data migration.

## Current hardware

- Chassis: SilverStone CS383, 8-bay hot-swap NAS chassis.
- Motherboard: MSI MAG X870E TOMAHAWK WIFI.
- CPU: AMD Ryzen 7 8700G.
- CPU cooler: AMD stock cooler supplied for this build.
- Memory: Corsair Vengeance 64 GB DDR5-6000 CL30, two DIMMs.
- PSU: Seasonic FOCUS GX-750.
- HBA: LSI / Broadcom SAS 9207-8i.
- Data drives: eight Seagate IronWolf 12 TB drives.
- Boot SSDs:
  - Crucial MX500 250 GB.
  - Patriot Burst Elite 240 GB.

## Verified physical state

- CPU installed and AM5 retention mechanism latched.
- CPU cooler physically installed.
- Two RAM modules installed in MSI-recommended A2 and B2 slots; latch seating was visually confirmed.
- PSU bench test passed using the Seasonic-supported 24-pin paper-clip method.
- Seasonic modular cable identification verified against Seasonic's compatibility guide: E81-family cables are CPU/EPS 12 V cables; G92-family cables are 6+2-pin PCIe/GPU cables. This NAS has no discrete GPU power requirement, so the two RG92/G92 PCIe cables are not used; the two RE81/E81 CPU cables are the required pair for motherboard CPU power.
- Both RE81/E81 CPU/EPS cables are now connected to adjacent PSU CPU/PCIe modular sockets; both RG92/G92 PCIe/GPU cables remain unused.
- PSU-side modular cabling is now complete for the planned build: motherboard 24-pin cable connected; both RE81/E81 CPU/EPS cables connected; both SATA/peripheral harnesses connected. The only modular cables intentionally left disconnected are the 12V-2x6 / 600 W GPU cable and the two RG92/G92 PCIe/GPU cables.
- PSU cable routing in the chassis: the motherboard 24-pin, both RE81/E81 CPU/EPS leads, and the backplane SATA-power harness route above/around the motherboard area; the second SATA-power harness routes below to the two boot SSDs.
- CS383 rear cable bundle observed on the cable-management side of the motherboard tray, not trapped under the motherboard footprint.
- Motherboard installed in the CS383 on nine matched standoffs; all nine motherboard screws were started by hand and then snugged evenly without over-tightening.
- Front-panel JFP1 wiring completed: HDD LED on pins 1/3, Power LED on 2/4, Reset SW on 5/7, Power SW on 6/8; NIC1/NIC2 LED leads are unused on this motherboard.
- Front HD AUDIO connected to JAUD1.
- Front USB 5 Gbps Type-A cable connected to JUSB3.
- Front USB-C cable connected to JUSBC1.
- Final fan header map: rear case fan on SYS_FAN1; right front drive-cage fan on SYS_FAN5; left front drive-cage fan on SYS_FAN6.
- Rear expansion-slot cover aligned with PCI_E1 removed in preparation for HBA installation.
- Both boot SSDs are physically secured in their final CS383 mounting positions. All eight IronWolf 12 TB drives are installed in the CS383 hot-swap bays and seated without force. The PSU is installed in the CS383 and its mounting screws are snug. HBA retention is now resolved: Gene modified the chassis holder for clearance and reports the LSI 9207-8i is firmly anchored to the frame.
- LSI 9207-8i is fully seated in PCI_E1 and firmly retained by the modified chassis holder. The incompatible silver metal bracket remains removed. Both Cable Matters SFF-8087 forward-breakout cables are connected to the HBA internal ports. The upper HBA cable maps to CS383 SATA 1-4, and the lower HBA cable maps to CS383 SATA 5-8. All eight SATA branch connectors are securely attached to the numbered CS383 backplane data ports.
- Boot SSD connections completed: Crucial MX500 and Patriot Burst Elite are both physically secured, have SATA data connected to SATA_S1/SATA_S2 respectively, and have SATA power connected.
- Motherboard-side PSU power is complete: the 24-pin ATX connector and both CPU/EPS connectors are attached and reported fully seated.
- CS383 backplane power is complete: both backplane PSU power connections are attached.
- Gene performed a final physical check of all wired/LSI connections completed to this point and secured the wire bundles.
- Two Cable Matters 0.5 m / 1.6 ft Internal Mini-SAS SFF-8087-to-4x-SATA forward-breakout cables, model 104016-0.5m, are now physically in hand. They are intended to connect the LSI 9207-8i's J5/J6 ports to the eight CS383 backplane SATA data inputs.
- IronWolf tray numbering and serial inventory from photographed labels:
  - 1: ZZ30N1YX
  - 2: ZZ30PAWE
  - 3: ZZ30PC78
  - 4: ZZ30PBLQ
  - 5: ZZ30N2BG
  - 6: ZZ30N4AC
  - 7: ZZ30N4DB
  - 8: ZZ30PBPL
  - All eight are Seagate IronWolf 12 TB ST12000VN0008, firmware SC60.

- Historical no-power evidence before outside service: PSU paper-clip test passed in Normal fan mode; +5VSB measured 5.0 VDC at the motherboard-end 24-pin harness; PS_ON was later measured at about 5 V at rest and 0 V when JFP1 pins 6/8 were shorted, showing the motherboard asserted PS_ON.
- Gene reports that an outside tech center diagnosed a failed Ryzen 7 8700G and replaced/handled the CPU. The exact tech-center test method was not recorded, so the causal diagnosis is user-reported rather than independently verified here.
- After service, Gene observed the system POST successfully. MSI Click BIOS X identifies BIOS E7E59AMSI.2AC4 dated 2026-09-02 and detects an AMD Ryzen 7 8700G.
- BIOS reports 64 GB RAM as two 32 GB DIMMs in A2/B2 at 4800 MT/s with EXPO off.
- BIOS idle CPU temperature was observed at about 66 C with CPU voltage about 1.428 V. Gene reports the CPU cooler fan is operating.
- BIOS clock is incorrect, showing approximately 2026-04-06/07; set correct date/time before TrueNAS installation.
- Current front-panel wiring after service: JFP1 HDD LED 1(+)/3(-), Power LED 2(+)/4(-), Reset 5/7, Power SW 6/8.
- Current boot SSD data wiring after service: Crucial MX500 -> SATA_S1 (bottom port of the SATA_S1/S2 stack); Patriot Burst Elite -> SATA_S2 (top port).
- Both SFF-8087 breakout cables remain connected to the LSI 9207-8i. They do not connect to the motherboard.
- EPS cables are intended to route behind the motherboard tray rather than over the CPU cooler.
- CORRECTION 2026-10-13: Gene clarified that the used drive with the "NEMONG COMPUTER" sticker and existing Korean Windows 10 installation is the Patriot Burst Elite 240 GB, not the Crucial MX500. The Patriot is therefore the legacy/used boot device to isolate during initial TrueNAS installation.
- SUPERSEDING EVIDENCE 2026-10-13 (device-reported SMART, see EVIDENCE.md): Crucial MX500 reports 2,019 power-on hours and Percent_Lifetime_Remain 75 (25% of rated life used); Patriot Burst Elite reports 3 power-on hours. The TrueNAS installer also showed a vfat (EFI) partition on the Crucial and none on the Patriot, and the F11 menu showed Windows Boot Manager on the Crucial. The Crucial MX500 is therefore the previously used, heavily written drive; the Patriot is effectively new. The earlier "Patriot is the used drive" correction is contradicted by device evidence.

## 2026-10-13 HBA / video fault state

- USER-STATED-EXPLICIT: With the LSI 9207-8i removed, motherboard HDMI video works and BIOS is usable.
- USER-STATED-EXPLICIT: With the LSI 9207-8i installed, motherboard HDMI output is black/no video.
- USER-STATED-EXPLICIT: The same black-screen behavior occurred with the HBA installed in PCI_E1 and in a lower full-length PCIe slot, so the symptom is not unique to one tested slot.
- USER-STATED-EXPLICIT: Gene ruled out the HDMI cable/monitor path based on prior successful use and repeated current testing.
- USER-STATED-EXPLICIT: BIOS graphics settings tested with the HBA present included Initiate Graphic Adapter = IGD and Integrated Graphics = UMA Auto; no change.
- USER-STATED-EXPLICIT: BIOS UEFI/CSM Mode was already UEFI.
- USER-STATED-EXPLICIT: Re-Size BAR and Above 4G were disabled; no change.
- USER-STATED-EXPLICIT: CMOS was cleared once during the 2026-10-12/13 troubleshooting session.
- USER-STATED-EXPLICIT: Both boot SSDs were disconnected during these tests.
- USER-STATED-EXPLICIT: Without the HBA installed, the board reached Digi-Debug A9 / 00 with the green BOOT LED while no bootable device was connected.
- USER-STATED-EXPLICIT: With the HBA installed in the third full-length PCIe slot, both SFF-8087 storage cables disconnected from the HBA, and both boot SSDs disconnected, the board reached Digi-Debug `00` with the green BOOT LED lit but motherboard HDMI remained black/no video. This shows the symptom persists with no downstream SATA/backplane connection and is not unique to PCI_E1.
- UNRESOLVED: Exact HBA firmware version/mode (IT vs IR), option-ROM contents, and whether this specific card works in another machine remain unknown.
- HBA firmware must not be erased or flashed until exact adapter identity/current firmware/tool/target/recovery path are verified from current Broadcom authority.
- USER-STATED-EXPLICIT: Forcing Chipset Gen Switch to Gen3 did not restore HDMI video with the HBA present.
- USER-STATED-EXPLICIT: Changing UEFI/CSM Mode from UEFI to CSM caused the previously working no-HBA firmware-video path to fail/freeze after save/reboot.
- USER-STATED-EXPLICIT: A subsequent Clear CMOS restored normal POST/video with the HBA removed and both boot SSDs disconnected.



- IMAGE-EVIDENCED 2026-10-13: MSI F11 boot menu with the Patriot disconnected shows `Windows Boot Manager (SATA S1: CT250MX500SSD1)` and `UEFI: PNY USB 2.0 FD PMAP, Partition 1`. This proves the Crucial MX500 currently carries a Windows Boot Manager EFI entry; it does not establish where the prior Korean Windows installation's full OS volume resided.

## 2026-10-14 state (CURRENT - read first)

- IMAGE-EVIDENCED 2026-10-14: With the Android phone on cellular (5G, not house Wi-Fi) and connected to Tailscale, `http://<NAS-TAILSCALE-IP>` reached the TrueNAS sign-in page. This verifies end-to-end remote VPN access to the NAS from outside the home LAN. The TrueNAS page warns that HTTP is not HTTPS, but the transport path is inside the encrypted Tailscale tunnel.
- IMAGE-EVIDENCED 2026-10-14: Tailscale app is installed and Running in TrueNAS, and the Tailscale Machines page shows `truenas-scale` online at <NAS-TAILSCALE-IP> under the same tailnet/account as the Envy and Mac. Initial VPN join is therefore verified.
- USER-STATED-EXPLICIT 2026-10-14: Android device `hacker-deux` is now connected to the same tailnet. Gene reports that HTTPS to the NAS Tailscale IP does not work; use of the Tailscale path should therefore be tested with plain HTTP over the encrypted Tailscale tunnel unless/until a matching HTTPS certificate/name is configured.
BASE BUILD COMPLETE.

- Drives: all 8 IronWolf SMART long tests "Completed without error", health PASSED (2026-10-14 04:29).
- Pool `tank`: single 8-wide RAIDZ2 vdev, ONLINE, 0 errors, 61.93 TiB usable. Datasets tank/immich, tank/plex, tank/nextcloud, tank/general (+ TrueNAS tank/.system). Weekly scrub Sundays 00:00. Auto TRIM off (HDD pool).
- Created 08:00 by pool_gate.sh after first attempt failed safely (`midclt call -job` invalid; correct flag `-j`).
- Boot: Patriot (223.57 GiB) could not be attached as a mirror to the Crucial (232.89 GiB) - too small. Gene reinstalled TrueNAS 25.10.7 onto BOTH SSDs (Fresh Install) and restored the saved configuration. boot-pool is now mirror-0 of two SSD partitions, ONLINE, no errors. `tank` re-imported via config restore, ONLINE.
- During the restart before the reinstall, no video and Digi-Debug 80/81 were observed; after the reinstall the system booted with console video normally. Root cause of the intermittent no-video-with-HBA behavior remains unexplained.
- Network: 192.168.20.14 (VLAN 20 Family, UDM Pro port 3, UniFi fixed IP by MAC fc:9d:05:06:49:fe). Time/timezone correct (America/New_York).
- Update profile MISSION_CRITICAL; 25.10.7 "System is up to date".
- Configuration backup: System -> Advanced Settings -> Manage Configuration -> Download File (with Password Secret Seed). Fresh backup taken after mirror/email/alerts were configured; stored off-NAS by Gene.
- Email: Send Mail Method GMail OAuth, From "Home TrueNas" saweba4master1@gmail.com; test mail succeeded. truenas_admin email set via `midclt call user.update` (UI user edit form would not save). Test alert sent successfully via the E-Mail alert service (level Warning).
- SMART schedule: not available in the 25.10 UI; implemented as a root cron job (System -> Advanced Settings -> Cron Jobs) "Monthly SMART long test - IronWolfs", 01:00 on day 1 of each month, command loops `smartctl -t long` over all ST12000VN0008 disks.
- Disk temperatures at idle: IronWolfs 40-49 C; the 60 C dashboard maximum is an SSD. Revisit drive-cage fan curve (SYS_FAN5/SYS_FAN6) if IronWolfs sit in the mid-50s under load.

- USER-VERIFIED 2026-10-14: Immich preflight completed on TrueNAS 25.10.7. Catalog reports Immich community 1.14.50 / v3.3.1_1.14.50, not installed. `tank/immich/data` and `tank/immich/pgData` exist at `/mnt/tank/immich/data` and `/mnt/tank/immich/pgData`. `data` is owned by apps:apps mode 770; `pgData` is root:root mode 770 pending Immich PostgreSQL automatic-permissions handling. AMD Phoenix1 GPU is visible at PCI 0000:78:00.0 and available to host; initial Immich install will use CPU/default ML first and GPU enablement will be a later verified change.

- USER-SUPPLIED COMMAND OUTPUT 2026-10-14: Immich install via supported TrueNAS `app.create` completed successfully. `app.query` reports `immich` state `RUNNING`, version `1.14.50` / human version `v3.3.1_1.14.50`, server published on host port <IMMICH-PORT>, and server/Postgres/machine-learning/Redis containers running. Data bind mount is `/mnt/tank/immich/data`; PostgreSQL bind mount is `/mnt/tank/immich/pgData`. Post-install permissions are `apps:apps 770` for data and `netdata:docker 770` for pgData, confirming PostgreSQL automatic-permissions handling completed. Initial install uses default CPU machine-learning image; AMD GPU enablement remains a later controlled change.

- USER-SUPPLIED COMMAND OUTPUT 2026-10-14: Immich is RUNNING on TrueNAS, version 1.14.50 / v3.3.1_1.14.50, published on host port <IMMICH-PORT>. Server, PostgreSQL, machine-learning, and Redis services are running. Data uses /mnt/tank/immich/data and PostgreSQL uses /mnt/tank/immich/pgData. Post-install permissions are apps:apps 770 for data and netdata:docker 770 for pgData. Initial deployment uses the default CPU machine-learning image; AMD GPU enablement remains a later controlled change.

- USER-DIRECTED 2026-10-14: Immich is to become the canonical photo/video source after the existing Mac archive is bulk-uploaded and verified. Ongoing phone photos should flow into Immich. The Mac and Envy are intended to hold independent local backup copies sourced one-way from Immich/NAS rather than act as peer canonical stores. Do not use bidirectional sync or have one backup computer be the only source for the other. Backup design must include both Immich asset files and Immich database dumps; at least one offsite copy remains separately required because NAS, Mac, and Envy are co-located.

- USER-SUPPLIED COMMAND OUTPUT 2026-10-14: Plex stable app 1.3.15 / Plex Media Server 1.43.4.10903-e5521bd8c installed successfully and is now RUNNING on host port 32400. Persistent bind mounts are /mnt/tank/plex/config -> /config and /mnt/tank/plex/data -> /data; both child datasets were created under tank/plex and set to apps:apps (UID/GID 568), mode 770, ACL disabled before install. TrueNAS app notes confirm AMD GPU devices /dev/dri and /dev/kfd are passed read/write into the Plex container. This proves device exposure, not successful hardware transcoding; that must still be verified from an actual Plex transcode session after account/server setup.

- USER-SUPPLIED COMMAND OUTPUT 2026-10-14: Nextcloud stable app 2.3.78 / Nextcloud 35.0.1 installed successfully on host port 30027. The install output shows persistent bind mounts `/mnt/tank/nextcloud/html` -> `/var/www/html`, `/mnt/tank/nextcloud/data` -> `/var/www/html/data`, and `/mnt/tank/nextcloud/postgres_data` -> `/var/lib/postgresql`. Post-install verification reported `RESULT=NEXTCLOUD_RUNNING`, version 35.0.1, maintenance mode false, no pending database upgrade, PostgreSQL UID/GID 999/999, and script exit 0. Base Nextcloud installation is therefore verified; remote-access/trusted-domain validation is now complete; remaining commissioning includes user accounts/quotas and snapshot protection before substantial user data.

- NEXTCLOUD SECURE ACCESS VERIFIED 2026-10-14: Tailscale HTTPS certificates were enabled for the tailnet after Gene explicitly accepted Certificate Transparency disclosure for the node hostname. Nextcloud now trusts `truenas-scale.tail6e87d7.ts.net` and is configured with `overwriteprotocol=https`, `overwritehost=truenas-scale.tail6e87d7.ts.net`, and `overwrite.cli.url=https://truenas-scale.tail6e87d7.ts.net`. USER-SUPPLIED COMMAND OUTPUT: `tailscale serve status` reports `https://truenas-scale.tail6e87d7.ts.net (tailnet only)` with `/` proxied to `http://127.0.0.1:30027`; `tailscale funnel status` also reports the route as `(tailnet only)`, with no public Funnel endpoint reported. TOOL-VERIFIED FROM ENVY: the Tailscale hostname resolves to `<NAS-TAILSCALE-IP>`; Tailscale ping succeeds; HTTPS certificate validation succeeds and the secure URL returns the normal Nextcloud redirect path; direct LAN `http://192.168.20.14:30027/` returns HTTP 302 with `Location: https://truenas-scale.tail6e87d7.ts.net/login`. USER-STATED-EXPLICIT: Gene is logged into Nextcloud successfully in the Envy browser and Pixel browser over the secure route. Tailscale itself remains in host-network mode; do not redesign it merely to attach to Nextcloud's private Docker network because that could disrupt remote TrueNAS host access.

## 2026-10-16 Pixel -> Immich uploader (ACHIEVED)

- Goal: manual run on the Pixel (Termux) over Wi-Fi with mobile data off; upload all photos/videos to Immich with no duplicates.
- Immich API: `http://<NAS-TAILSCALE-IP>:<IMMICH-PORT>/api` over Tailscale.
- Script: `~/.local/bin/pixel-nas-new-only` (all-directories version), SHA-256 `bfabe08ab39be52a91529814d210cb5fe1a5f0345b544e2f89a278506becfd68`. Prior camera-only version kept at `~/.local/bin/pixel-nas-new-only.bak` (copy also at `Download/pixel-nas-new-only.txt`).
- Behavior: scans `/storage/emulated/0` excluding `Android/` and dot-directories; matches by SHA-256 against `known-sha256.txt` + `hash-cache.tsv`; records Immich "duplicate" responses; verifies each new upload by SHA-1; refuses to run unless on `wlan0`.
- API key: `~/.config/pixel-nas/immich-key` (mode 600). Never print or expose it. Log: `~/.local/share/pixel-nas/new-only.log`.
- USER-SUPPLIED COMMAND OUTPUT 2026-10-15/16: first full run `uploaded=5 already_on_server=0 failed=0 (newly hashed 4407)`.
- USER-SUPPLIED COMMAND OUTPUT 2026-10-16: run from hotel Wi-Fi in New Jersey `uploaded=5 already_on_server=0 failed=0 (newly hashed 5)`; log shows these 5 VERIFIED_NEW paths are distinct from the first run's 5. Immediate re-run `uploaded=0 already_on_server=0 failed=0 (newly hashed 0)` - no-duplicate behavior verified. Remote use over non-home Wi-Fi verified.
- USER-SUPPLIED COMMAND OUTPUT 2026-10-16: old termux-job-scheduler job 44110 no longer exists; `--pending` reports no pending jobs. No automatic schedule remains; uploader is manual by design.
- Daily use: Wi-Fi on, mobile data off, Tailscale on -> `bash ~/.local/bin/pixel-nas-new-only`.
- WATCH: Do NOT enable Immich mobile-app backup on the Pixel (risk of duplicating the uploader's assets).
- WATCH: 49-asset count discrepancy in Immich, not yet investigated.
- USER-SUPPLIED COMMAND OUTPUT 2026-10-18 (hotel Wi-Fi, Spain): first run refused to upload: `curl: (28) Connection timed out after 8003 milliseconds` / `NAS not reachable (Tailscale on?)`. Script exited safely with no upload.

- USER-SUPPLIED COMMAND OUTPUT 2026-10-18: next run `DONE: uploaded=258 already_on_server=0 failed=0 (newly hashed 258)`. Immediate repeat `DONE: uploaded=0 already_on_server=0 failed=0 (newly hashed 0)` - no-duplicate behavior reproduced. Completion level: component (upload run). Coverage of every Pixel folder and the Immich-side asset count were NOT checked.

- USER-DIRECTED 2026-10-19: keep the Termux uploader for now. Eventual direction: move to native Immich app backup because other users will need the same capability. NOT authorized yet: any switch requires Gene's approval after duplicate handling, folder coverage and a safe transition are established. WATCH about enabling app backup on the Pixel still stands until then.

- OPEN: 49-asset discrepancy; Pixel folder coverage check; Immich total vs +258 (Gene: later).

## 2026-10-27 Remote operability and network hardening

Sanitized per C-10: no addresses, MACs, tailnet names or serials. Detailed inventory belongs in dacp-private (not yet written).

- USER-STATED-EXPLICIT: NAS physical closeout (step 1 below) was completed before the Spain trip: panels on, final location, continuous uptime since.
- USER-STATED-EXPLICIT: Whole-house natural-gas generator (about 10 s transfer); gateway, switch, both NASes, Envy, Mac mini and iMac are on three UPS units. Gene accepts generator-failure risk; UPS signalling and auto-power-on are out of scope. The earlier "add a UPS" item is superseded.
- TOOL-VERIFIED 2026-10-27 (Claude, Gene's UniFi session, read-only): both UniFi sites (Pennsylvania home, Delaware) inventoried, plus the unmanaged EdgeSwitch web UI. UPnP off and gateway SSH off at both sites; automatic backups on; IPS on in notify-and-block with region blocking.
- CHANGES 2026-10-27 (Gene clicked; Claude read back each one):
  - Pennsylvania gateway: all four inbound port forwards PAUSED (HTPC media server, a legacy port-80 forward aimed at an unused address, Pi SSH, Pi WireGuard). No inbound forwards are active. IPS had logged external intrusion attempts against the Pi via those forwards.
  - Pennsylvania IPS: outgoing detection exclusion added for the skyhawk.org server only. Cause: outbound SSH from the Mac mini and Envy to that server was blocked 14 times on 2026-10-25 under the "Scanning Activity" policy.
  - Basement Pi (Raspberry Pi 4) rebuilt on a new 128 GB card. Old card (Raspbian 10, end of life; half-upgraded Pi-hole; nightly backups to a missing host with remote rm -rf) removed intact, labelled, kept as the rollback. New: Raspberry Pi OS Lite 64-bit (Debian 13), key-only SSH (password authentication off, verified), Pi-hole v6 (core 6.5, web 6.6.1, FTL 6.8) migrated from the old config, listening mode changed from local to ALL. The old "local" mode refused queries from the Family VLAN, so ad blocking was ineffective for user devices. Verified from the Family VLAN: ad domain blocked, normal domain resolves.
  - Tailscale on the Pi as an approved exit node (accept-dns off). Verified 2026-10-27 about 12:02 ET: Pixel on cellular with the Pi as exit node showed the home WAN address.
  - Tailscale key expiry disabled on the Pi, Envy, Mac mini and TrueNAS. Pixel keeps expiry (Gene).
- USER-DIRECTED: exit node None at home; select the Pi when travelling; Allow LAN access off.
- CORRECTIONS: the temperature controller is NOT PoE-powered (its switch port draws 0 W), so it cannot be power-cycled from the switch. The Basement Pi IS PoE-powered, so it can be power-cycled from the EdgeSwitch UI. The Mac is an M4. The basement iMac exists on the Family VLAN; its switch port is unresolved (port labels are stale).
- OPEN:
  - C-10: this file already contains LAN addresses, a MAC, a tailnet name and drive serials. Redaction decision pending (Gene). Whether C-10 also applies to dacp-private is pending (Gene).
  - Proton VPN clients (5, disabled) and a "Full Tunnel" policy route with kill switch remain. Deletion not executed.
  - Delaware: switch uplink to the gateway negotiates 100 Mbps (cable or port fault); WAN packet-loss event 2026-10-26.
  - EdgeSwitch: factory admin username, old firmware, about 285 days uptime.
  - Stale Pennsylvania firewall objects (camera address list, rules for a removed network, a nonexistent subnet in the local list).
  - Both sites auto-update OS and apps daily (unattended gateway restarts). Gene decision pending.
  - No independent remote path to the EdgeSwitch yet (needed to power-cycle the Pi if the Pi hangs): Tailscale subnet route from the NAS proposed.
  - Optional: tailnet DNS pointed at Pi-hole for ad blocking while travelling; Pi UDP GRO tuning.
  - Pixel uploader: the 2026-10-19 run was cut off (no PASS_COMPLETE); a stale lock left by the killed run blocked the next start. Self-clearing lock proposed, not built.
  - Envy, Mac and iMac unattended-recovery items (auto-login, sleep, independent remote access) not yet inventoried.
## Next sequence (2026-10-14)

1. Physical closeout and final placement: cleanly shut down TrueNAS, reinstall the CS383 panels, move the NAS to its final storage location, reconnect Ethernet and power, boot, and verify the normal web UI at https://192.168.20.14 before continuing.
2. Tailscale remote access is verified. Nextcloud now uses tailnet-only HTTPS at `https://truenas-scale.tail6e87d7.ts.net`; no public Funnel endpoint is reported.
3. Base app installation is complete for Immich, Plex, and Nextcloud. Remaining app commissioning: validate Immich CPU fallback if AMD iGPU acceleration is unavailable; verify whether Plex Radeon 780M hardware transcoding actually works from a real transcode session; configure Nextcloud for the planned 5 users with approximately 3 TB quotas; its intended Tailscale HTTPS access path is now validated.
4. Periodic snapshot tasks on tank/immich, tank/nextcloud, and tank/general, with a practical initial retention target of roughly 2-4 weeks. Have snapshot protection in place before substantial real user data lands.
5. SMB share(s) plus a non-admin NAS user for the Envy and Mac, using tank/general for ordinary file access.
6. Data migration from the Synology (VLAN 50) and the HTPC recovery set. Verify file counts and checksums before retiring or deleting any source copy.
7. Establish a second/off-site copy for irreplaceable data (especially photos and documents), either via TrueNAS Cloud Sync to a suitable provider or replication to the old Synology if it is retained as a backup target. RAIDZ2 is not a backup.
8. Add a UPS and configure the TrueNAS UPS service for clean shutdown on power loss.
9. Housekeeping: download a fresh configuration backup with secret seed after each major configuration change; continue watching IronWolf temperatures under load and raise SYS_FAN5/SYS_FAN6 if needed; consider disabling Usage collection & UI error reporting if desired for privacy.
10. Verify LSI 9207-8i firmware/mode before any firmware action; investigate intermittent no-video-with-HBA only if it recurs.

- USER-DIRECTED 2026-10-14: Gene wants the chassis closed up and moved to its final storage location before the remaining commissioning work. Routine TrueNAS configuration should then be performed through the web UI from the Envy; the local downstairs console is reserved primarily for boot/network/recovery situations when the web UI is unavailable.


## 2026-10-13 TrueNAS installation and commissioning state

- TOOL-VERIFIED: PNY USB 2.0 FD 14.4 GB (serial 087E013260C0) rewritten on the Envy at ~09:44 EDT from `TrueNAS-SCALE-25.10.7-VERIFIED.iso`; ISO SHA-256 `54ce9441ce66966a392e28f63604ca3c2c083d0bec4db7bb5af2f74f7a007c8e` matched the official TrueNAS .sha256, and a raw read-back of the USB matched the same hash. The two other local ISO copies (`TrueNAS-SCALE-25.10.7.iso`, `.fresh.iso`) do NOT match the official hash and must not be used. An earlier write to a 7.5 GB "Generic Flash Disk" failed mid-write ("device not ready") and that stick is not usable as installer media.
- IMAGE-EVIDENCED: The rewritten PNY booted the TrueNAS 25.10.7 installer with the LSI 9207-8i installed and video working. The earlier HBA black-screen symptom did not recur in this boot; its root cause remains unexplained.
- IMAGE-EVIDENCED: Installer disk list showed all eight ST12000VN0008 (10.91 TiB) plus CT250MX500SSD1 (232.89 GiB) and Patriot Burst Elite (223.57 GiB). TrueNAS was installed to the Crucial MX500 ONLY; the erase warning named only that disk. Install succeeded. Boot pool = `boot-pool` on the Crucial. Patriot remains unused (planned boot-pool mirror).
- IMAGE-EVIDENCED: First boot loaded `mpt2sas` and enumerated all eight IronWolfs behind the HBA. TrueNAS Disks page lists serials ZZ30N1YX, ZZ30PAWE, ZZ30PC78, ZZ30PBLQ, ZZ30N2BG, ZZ30N4AC, ZZ30N4DB, ZZ30PBPL at 10.91 TiB, no pool.
- Network: onboard 5G NIC `enp6s0`, MAC `fc:9d:05:06:49:fe`. Link negotiates slowly after boot; if DHCP is missed, console option 1 -> Save -> `a` re-applies DHCP. UDM Pro (UDMP Pennsylvania) port 3 changed by Claude, with Gene approval, from native Default (1) to Family Network (VLAN 20); NAS cable moved to UDM port 3. UniFi fixed IP reservation 192.168.20.14 (Virtual Network Override OFF, verified after reload). Web UI: https://192.168.20.14, admin user `truenas_admin`.
- UniFi network map (UDMP Pennsylvania, CLAUDE-OBSERVED): Default 1 192.168.1.0/24; Family Network 20 192.168.20.0/24 (house computers); Camera 30; IoT 40 192.168.40.0/24; Server 50 192.168.50.0/24 (Synology); Guest 99. ES-24-500W EdgeSwitch (unadopted, 192.168.1.3) on UDM port 8.
- Timezone America/New_York; clock verified correct in TrueNAS.
- SSD SMART (TOOL-VERIFIED via smartctl): Crucial MX500 PASSED, 2,019 POH, 25% life used, 0 reallocated/pending/uncorrectable. Patriot PASSED, 3 POH, 0 reallocated/uncorrectable.
- SMART LONG tests started 2026-10-13 ~12:55 EDT on all eight IronWolfs; estimated completion 04:14-06:07 EDT 2026-10-14 (sdc last).
- A TrueNAS update is pending; Gene decision: do not apply until the long tests finish (reboot would abort them).
- Gene decisions: NAS on VLAN 20; pool `tank` = 8-wide RAIDZ2 (unencrypted); datasets tank/immich, tank/plex, tank/nextcloud, tank/general per NAS_Software_Setup_Guide.pdf (that guide's 6-drive/~48 TB Stage 3 is stale; 8-wide RAIDZ2 expected ~58 TiB usable).
- Unattended gate armed: `/home/truenas_admin/pool_gate.sh` (SHA-256 `0f5a2baae9dc4a221e4f6ca0d7254e3de8352f90717673cb16b2166d84fc8212`) running as systemd unit `pool-gate.service`, log `/home/truenas_admin/pool_gate.log`. It creates the pool and datasets only if all eight long tests report "Completed without error" with health PASSED, exactly eight ST12000VN0008 are present, no pool `tank` exists, and no data disk has partitions; otherwise it logs `RESULT=ABORT_*` and does nothing. Deadline 2026-10-14 14:00 EDT.
- Original defective Ryzen 7 8700G (OPN 100-100001236SBX, S/N 9MQ4290R50085) returned to Amazon; no AMD RMA filed.

## Software / installer state

- IMAGE-EVIDENCED 2026-10-13: Selecting `UEFI: PNY USB 2.0 FD PMAP, Partition 1` from the MSI F11 boot menu returned immediately to the same boot-device menu instead of starting the TrueNAS installer. This narrows the current blocker to the installer-media/UEFI boot path rather than the Windows Boot Manager entry on the Crucial SSD.

- TrueNAS Community Edition target: 25.10.7.
- Windows PowerShell reported `RESULT=TRUENAS_ISO_VERIFIED`.
- TrueNAS 25.10.7 is installed and running (see 2026-10-13 installation section above).

## Known corrections to older planning material

- Current data-drive count is eight, not six.
- The MSI motherboard has an integrated rear I/O shield; do not perform a separate loose-I/O-shield installation step.
- Case cable-management wiring visible behind the motherboard tray is not an obstruction under the motherboard.
- Manufacturer documentation controls standoff placement, PSU sequence/orientation, connector use, and HBA installation when it conflicts with the planning guides.

## Superseded 2026-10-13 next sequence

Superseded by "Next sequence (2026-10-14)" above.

## Hard stop conditions

Stop rather than force or improvise if any of the following occurs:

- a motherboard standoff does not correspond to an actual motherboard mounting hole;
- a keyed power/data connector requires abnormal force;
- HBA slot/cable identity is ambiguous;
- modular PSU cable provenance/compatibility is uncertain;
- installer USB identity is ambiguous;
- TrueNAS install destination cannot be distinguished unambiguously from the eight data drives;
- observed physical state contradicts this file or a manufacturer reference.

Verified reality supersedes this file. Correct this file when reality changes.
