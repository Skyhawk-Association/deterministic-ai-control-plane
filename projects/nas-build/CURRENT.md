# NAS Build Current State

Status date: 2026-10-31

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

## 2026-10-16 Pixel -> Immich uploader (SUPERSEDED 2026-10-31: DEFECTIVE, see "2026-10-31 Pixel -> Immich" below)

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
## 2026-10-31 Pixel -> Immich: uploader defect found, switched to the Immich app (ACHIEVED 2026-10-31 16:09 ET)

Sanitized per C-10 (no addresses).

- TOOL-VERIFIED 2026-10-27 15:19 ET (read-only Termux audit, Immich bulk-upload-check by SHA-1 against the uploader API key's account): Pixel media under shared storage (excluding Android/ and dot-dirs) = 6,497 files; in Immich 2,158; MISSING 4,339 (DCIM/Camera 1,827 missing; Screenshots 1,598; ChatGPT 534; others smaller). Unreadable 0.
- ROOT CAUSE (INFERRED, strong): the Termux uploader decides "already uploaded" from its own preloaded SHA-256 list, never by asking Immich. First run hashed 4,407 files and uploaded 5. Its "0 failed / no duplicates" reports were true of its own list and meaningless for Immich. The 2026-10-16 "ACHIEVED" status above was therefore wrong.
- 2026-10-27: a corrective Termux bulk upload (pixel-upload-missing.py, server-side checksum dedupe) uploaded 47 files ("created") before Android killed Termux after its wake lock was released. Termux upload route abandoned.
- USER-DIRECTED 2026-10-27: switch to the native Immich mobile app (reverses the 2026-10-19 keep-Termux direction). Earlier WATCH against app backup is withdrawn: Immich deduplicates per account by checksum, so files already uploaded are not stored twice.
- USER-DIRECTED 2026-10-27: Immich account used is the existing admin account (storage label "admin", the geneatwell login). No other Immich account exists; logins with Gene's primary email fail. Immich password changed by Gene 2026-10-27 (an earlier screenshot exposed the old one).
- APP CONFIG, USER-SUPPLIED SCREENSHOTS 2026-10-31: Immich app 3.3.4, server 3.3.1 (3.3.5 available, not applied). Backup Albums: all device albums selected (Camera, Screenshots, ChatGPT, WhatsApp Images/Video/Animated Gifs, DCIM, Download, Pictures and subfolders, Internal Storage, others). Backup Options: cellular OFF for photos and videos (source-verified: uploads then require Wi-Fi), Charging OFF (Gene decision pending), Sync albums OFF. Networking: Automatic URL switching ON; local = home Wi-Fi "Atwell" + LAN endpoint; external = Tailscale endpoint, validated (green check). Away from home Tailscale must be on; at home it is not needed.
- 2026-10-31 15:02 ET: Enable Backup ON and uploading (Backup 3,089 -> 3,188, Remainder 6,858 -> 6,759 within one minute; Total 9,947). App total exceeds the audit's 6,497 because it also includes folders the Termux scan skipped (e.g. WhatsApp under Android/media) - INFERRED.
- UNVERIFIED: that the 3,034 pre-existing "Backup" count includes the Termux uploads (consistent, not proven per file).
- ACCEPTANCE, TOOL-VERIFIED 2026-10-31 16:02-16:09 ET: Immich app Backup 9,949 / Total 9,950 (one upload error). Independent read-only audit (pixel-audit.py, Immich bulk-upload-check by SHA-1): IN_IMMICH 6,530, MISSING 2. Missing #1: a screenshot taken 16:00 that day - re-check returned "duplicate" (already uploaded by the app). Missing #2: DCIM/Camera/PXL_20260120_160011755.mp4 is a 0-byte file (empty recording) - nothing to upload; this is the app's one "upload error". Result: every non-empty photo and video on the Pixel is in Immich, no duplicates (server checksum dedupe).
- RESOLVES: the 2026-10-16 49-asset discrepancy and folder-coverage WATCH items are superseded by this per-file audit.
- SOURCE-VERIFIED (Immich mobile source): the app stops uploading when sent to the background (handleAppPause -> stopForegroundBackup); background mode is a short-burst worker for new media after the trigger delay. Large backlogs require the app open on screen. New photos are picked up by the background worker.
- NEXT: when Remainder = 0, run the read-only audit (~/.local/bin/pixel-audit.py) - acceptance = MISSING: 0 against the same account. Then retire pixel-nas-new-only and pixel-upload-missing.py (Gene decides on deletion); keep pixel-audit.py.
- OPEN: Charging decision; confirm Immich password change by fresh login; credential storage for the Immich login (Chrome did not offer to save); other three users wait until the Pixel passes.
- LESSONS (candidate, not yet filed): success must be verified at the destination, never from the tool's own log; UI steps must come from vendor docs or source, not memory.

## 2026-10-31 evening: snapshots, old Synology, HTPC backup scan

Sanitized per C-10.

- TOOL-VERIFIED 2026-10-31 18:43 ET: a periodic snapshot task for tank/immich ALREADY EXISTED (task id 1): recursive, retention 3 WEEK, daily 03:10, enabled. Snapshots present for tank/immich, /data, /import, /library, /pgData (03:10 today) plus a manual run 18:42. Next-sequence item 4 is therefore DONE for tank/immich. USER-DIRECTED: leave retention at 3 weeks; do not modify the task.
- USER-DIRECTED: SSH service enabled on TrueNAS 2026-10-31 (key-only; password authentication off; Envy key on truenas_admin). Temporary - to be switched off when the Synology work is finished.
- USER-DIRECTED: the Mac and Envy cannot hold the NAS contents; the one-way-copy-to-Mac/Envy design is withdrawn. Second-copy target to be the old Synology (as a plain SMB target, no Synology apps), then off-site separately.
- TOOL-VERIFIED (read-only, DSM API): old Synology DS416play - 4x Seagate IronWolf 8 TB (SMART normal), SHR-1 Btrfs volume 23.0 TB total / 15.5 TB used; CPU ~100%, load ~13-18 on 4 cores, media re-indexing in progress. Two USB WD My Book drives (3.76 TB each, ~full) contain only a Hyper Backup target (Synology_1.hbk). Shares include Movies (785 files, 1.02 TB), TV (242 files, 60 GB), HTPC Backup (78,503 files, 6.78 TB), Computer Room Backup, Computer Room Time Machine, photo, homes, ActiveBackupforBusiness, Plex (not readable by Gene's account).
- CHANGE 2026-10-31 (Claude via DSM API, Gene-directed "stop the indexing"): stopped Media Server, Synology Photos, Video Station; stop sent to Universal Search and Audio Station (status unconfirmed). System media re-indexing still running.
- USER-DIRECTED: save Movies, TV and HTPC Backup to the NAS (Movies/TV -> tank/plex/data; HTPC Backup -> tank/general/htpc-backup), then wipe the rest. HOLD: Gene has said the old backups may contain photos lost in the earlier mass deletion; the Synology must not be wiped until its backups are searched (HTPC Backup, Computer Room Backup, Time Machine, photo/homes, Active Backup, Hyper Backup).
- IN PROGRESS: read-only scan on the NAS of the HTPC Backup share (mounted read-only via CIFS at /tmp/syno): 24,550 Windows Backup ZIPs (table-of-contents read only) plus File History plain files and a 205.8 GB WindowsImageBackup VHDX of the HTPC system drive (2024-06-09). Copy job prepared but not started.

## 2026-10-31 night: Immich 3.3.5, family users, Tailscale access rules

Sanitized per C-10 (no emails or addresses).

- TOOL-VERIFIED 2026-10-31 ~19:15 ET: Immich upgraded on TrueNAS via app.upgrade (snapshot_hostpaths true) from v3.3.1 to v3.3.5; web UI shows "Server Online v3.3.5". Phone app reconnected.
- TOOL-VERIFIED: Immich nightly DB dumps exist in the Immich data backups folder (daily 02:00, ~466 MB each), covered by the tank/immich snapshot task.
- USER-ACTION 2026-10-31: four family Immich accounts created by Gene (photo quota 3072 GiB each; son has admin rights per Gene). Welcome emails were NOT sent (SMTP not configured at creation; Immich sends the welcome only at creation - source-verified, no resend). Credentials delivered by Gene via WhatsApp.
- USER-ACTION: Immich email notifications configured (Gmail SMTP, app password, SMTPS on port 465); test email sent successfully.
- USER-DIRECTED: quotas recalibrated - photos (Immich) are the bulk at 3 TB per person as a ceiling; Nextcloud is for small files only (~250 GB proposed, not yet set). Supersedes the earlier "Nextcloud ~3 TB per user" plan. Computer (Time Machine / Windows image) backups: not yet designed; Gene's priority is his own photos, music, and whatever is needed to restore the M4 and the Envy.
- TOOL-VERIFIED 2026-10-31 19:40 ET: Tailscale access policy replaced (Gene saved; backup of the default policy kept by Gene). Structure: group:trusted (Gene, son) -> all destinations; group:family (three others) -> NAS Immich port only, plus autogroup:internet (exit node use). Default "ssh autogroup:self check" rule kept. Post-change test from the Envy: NAS Immich, NAS web, NAS SSH and Pi SSH all reachable over Tailscale.
- USER-ACTION 2026-10-31 ~20:35 ET: four Tailscale invite links (role Member, one per person) and the app instructions sent by Gene via WhatsApp. Free plan allows 6 users (5 in use).
- OPEN: verify family-group restriction from the first joined family phone (Immich reachable, NAS admin page not); confirm each invitee signs in with the email listed in the policy groups; set Immich External domain for future welcome links; switch NAS SSH off after the Synology work.

## 2026-10-31 late: old-Synology photo search - findings and copy in progress

- TOOL-VERIFIED (read-only scans on the NAS over read-only CIFS mounts at /tmp/syno): HTPC Backup share is NOT a photo source. Windows Backup sets 2019-2024 hold ~430 images over 200 KB, all application data (Plex artwork, app packages); the large video counts are the movie library (also present in the Movies share). Decision basis: HTPC Backup (6.78 TB) need not be saved; the Movies+TV save remains (~1.1 TB).
- TOOL-VERIFIED: the Synology "photo" share holds 47,950 images over 200 KB (94.6 GB; 47,001 .jpg), file dates 1980-01-05 .. 2017-09-07, including personal folders (e.g. Pictures/My Pictures/..., an iPhoto Library). Strong candidate for photos lost in the earlier mass deletion; overlap with Immich and the Mac archive NOT yet checked.
- IN PROGRESS 2026-10-31 21:36 ET (Gene approved): rsync of the photo share to /mnt/tank/general/synology-photo (detached on the NAS; log /tmp/photo-copy.log). Next: verify copy file-by-file vs source, snapshot tank/general (no snapshot task covers it yet), then fingerprint-compare against Immich.
- IN PROGRESS: read-only scan of the homes and Computer Room Backup shares (/tmp/scan3.txt).
- HOLD stands: no wipe of the Synology until all shares are searched (remaining: Computer Room Time Machine on the Mac, Active Backup, Hyper Backup on the USB drives).
- NOTE: /tmp/syno mounts do not survive a NAS reboot; NAS SSH remains enabled (key-only) until the Synology work is done.

## 2026-11-02: Live snapshot-task correction (USER-SUPPLIED COMMAND OUTPUT)

- Read-only TrueNAS command `sudo midclt call pool.snapshottask.query` returned three existing, enabled, recursive daily snapshot tasks. All report state FINISHED with a named snapshot dated 2026-11-02:
  - `tank/immich`: id 1, daily 03:10, 3 WEEK retention, `tank/immich@auto-2026-11-02_03-10`.
  - `tank/nextcloud`: id 2, daily 03:20, 3 WEEK retention, `tank/nextcloud@auto-2026-11-02_03-20`.
  - `tank/general`: id 3, daily 03:30, 3 WEEK retention, `tank/general@auto-2026-11-02_03-30`.
- CORRECTION: Earlier 2026-10-31/11-01 status entries calling general and nextcloud snapshot tasks OPEN are stale. No duplicate tasks needed; no snapshot settings were changed in this session.
- Plex migration: user-supplied pilot output on 2026-11-02 shows 20 TV video files and one movie copied from read-only Synology mounts to `/mnt/tank/plex/data/{TV,Movies}`; 21/21 SHA-256 comparisons passed, no deletions. Full ~1.075 TB transfer scripted and syntax/launch-tool checked; NOT STARTED, pending Gene's later go-ahead.

## 2026-11-01: Synology homes search, Drupal 6 dump recovery, launch-method correction

- TOOL-VERIFIED 07:00 ET: Synology photo-share copy complete - rsync dry-run against /mnt/tank/general/synology-photo shows 71,102 files, 190.2 GB, 0 files left to transfer.
- TOOL-VERIFIED (size2, 07:24-10:39 ET): Synology Drive backups in homes/geneatwell/Drive/Backup - Computer-Room-IMAC.local ~/Downloads 10,452,194 files / 12,964 GB (most of the Synology's 15.5 TB used), ~/Pictures 100,578 / 192.3 GB, ~/Music 35,811 / 176.6 GB, ~/Movies 444 / 64.1 GB, 31 recup_dir.* folders (PhotoRec output, ~15,000 files / ~80 GB); DESKTOP-FEAHE8A 52,816 / 233.2 GB; Hacker.local 199,762 / 252.9 GB. A 2014 Time Machine set inside the iMac backup holds one complete snapshot (13 GB) and is NOT the duplication source. Downloads contains ~55 daily full copies of the skyhawk.org drupalbeta tree (2021); website photos are out of scope (USER-DIRECTED).
- USER-DIRECTED: Skyhawk Association photos/documents on the Synology are out of scope; old Drupal databases are in scope (the Drupal 6 -> 8 migration dropped the photo research data). Detail and status in projects/skyhawk/LOST-D.md, 2026-11-01 section.
- TOOL-VERIFIED (drupalfind, 10:40-16:57 ET): 340 database dumps found (all in homes and CRB; none in photo or HTPC); no raw MySQL data folders anywhere. Copied (dumps only, all dates, plus the drupal638 code folder without sites/*/files) to /mnt/tank/general/skyhawk-d6-recovery: 18.00 GB, rsync verify 0 left, 2,227 SHA-256 hashes in SHA256SUMS. Site-file tarballs excluded (USER-STATED: files only, no databases).
- CORRECTION (launch method): background jobs started as `sudo nohup ... &` (or `sudo bash -c '... &'`) die or fail once the SSH session ends; children that outlive sudo get "Function not implemented" for every external command. Reliable method: `sudo systemd-run --collect --unit=<name> <command>`; check with `systemctl is-active <name>` (a finished --collect unit reports "could not be found"/inactive).
- TEMPORARY: Docker container `d6db` (mariadb:10.11, --network none, empty root password because unreachable, data in skyhawk-d6-recovery/db-scratch) holds the 2016-04-09 Drupal 6 database. Gene: KEEP until the live-site comparison is done; remove afterwards.
- OPEN: the 2014 Time Machine set inside the iMac backup includes usr/local/mysql that the geneatwell CIFS account cannot read (not needed so far).

## 2026-11-02 Gene decisions

- USER-STATED: no further time on the old Synology. The journal content scan (container pdfscan) was terminated by Gene. Not copied and left on the Synology: Movies/TV, iMac/old-Envy/Hacker.local Drive backups, CRB Envy and Time Machine, family home folders. The no-wipe HOLD stands by default (nothing is deleted unless Gene decides).
- USER-STATED: off-site / second NAS copy dropped (item 7).

## 2026-11-03 Photo consolidation into Immich: plan approved (Gene: "let it happen", 14:38 ET)

- Endpoint: all of Gene's photos in Immich (Immich is the master from here on), Skyhawk Association website copies excluded, Gene's own aircraft photos kept.
- C-18 bulk ingestion terms: owner = Gene's Immich account (geneatwell@gmail.com); destination mode = upload into Immich-managed storage (tank/immich, nightly snapshots), NOT an External Library and NOT an intermediate NAS mirror (Gene: no two-step merge); sources = Mac ArchiveSSD PicturesBackup (98,451 media files, 47,763 distinct) + the 13,240 Synology-copy files not on the Mac; duplicate policy = exact duplicates skipped by fingerprint (Immich uploader checks the server first), near-duplicates reviewed afterwards with Immich's duplicate tool, nothing deleted at any source; website exclusion = exact fingerprint match against the Mac's live-site mirror (/Volumes/SkyhawkBackup/skyhawk-vps-files/current), not file-name patterns; reconciliation = count to-upload vs uploaded vs skipped per source, recorded in Git.
- Tool: official Immich command-line uploader, run where the files are (Mac; NAS for the Synology set), API key entered by Gene at a hidden prompt. Albums per source for review.
- Sequence: (1) fingerprint the site mirror on the Mac + export Immich fingerprints (read-only); (2) final counts; (3) uploader install + API key; (4) 50-photo pilot; (5) overnight run.
- 2026-11-03 progress: exact counts (Mac 34,652 / Synology 13,238 not in Immich and not exact site copies). Gene: exclude all of Subject Collections (1,581 more; sample of 20 all website material). Uploader installed on the Mac, existing key "Mac Bulk Import 2026-10-14" reused; pilot of 50 into album "Mac archive" uploaded OK.
- Gene's pilot review: 3 Skyhawk Association photos, 1 junk icon, 2 1980s scans dated 2013 (their embedded date is wrong). Added content filters (Mac, read-only): visual dHash match (<=4/64 bits) against the live-site mirror's images, and longer side < 200 px = excluded. EXIF-date split dropped (Gene: yes), because it flagged 45% while missing the wrongly dated scans.
- USER-STATED-EXPLICIT rule (Gene 15:57 ET): "if it's a standard whatapp/pixel/mac named photo, it's a photo to keep. Most of the photos on the website that I helped to upload were coded with author/date of upload/other easy to discern names." Applied: camera/phone-pattern names are rescued from the look-alike exclusion (329 rescued); sample of 20 remaining exclusions all had descriptive website names matching site files.
- Final Mac list: 30,873 files (dacp-work\mac-final-all.lst), excluded 2,091 website look-alikes + 107 tiny + Subject Collections. Synology 13,238 still to be filtered the same way before upload.
- 2026-11-03 17:48 ET: Synology set filtered on the NAS (python:3.12-slim container, Synology copy read-only): 13,238 -> upload 12,600, excluded 638 (347 website look-alike, 291 tiny), 98 rescued by the camera-name rule. Gene confirmed the 20-sample of look-alike exclusions are website photos (including "Blade 83 Mike Wells"); Claude's suggestion to override them was WRONG and withdrawn. Files: /mnt/tank/general/immich-audit/{synology-final.lst (NUL-separated, /import/... paths), synology-excluded.tsv, synology-classify-summary.txt}.
- STATUS: nothing beyond the 50-file pilot uploaded yet. Tonight (Gene's choice, off-peak): (1) Mac run: /tmp/immich-full.sh on the Mac, xargs -0 immich upload --no-progress -A "Mac archive" < /tmp/mac-final-all.lst (list in dacp-work; block given in session, not yet run); (2) Synology run on the NAS after the Mac run: ghcr.io/immich-app/immich-cli:latest, /mnt/tank/general/synology-photo mounted at /import read-only, list /mnt/tank/general/immich-audit/synology-final.lst, album "Synology recovered", key via root-only env file deleted after the run, launched with systemd-run (delayed ~4 h) -- block NOT yet written against synology-final.lst.
- **2026-11-03 19:04 ET onward, USER-STATED-EXPLICIT + TOOL-VERIFIED component progress:** Gene started the Mac upload from `/tmp/immich-full.sh`. A live read-only Mac process check via Desktop Commander at approximately 19:11 ET found the `immich upload` process still running and the manifest containing 30,873 NUL-separated paths; the log showed `Received 5000 files`, `Found 4988 new files and 12 duplicates`, `Uploading 4988 assets`. This proves an active upload, not completed reconciliation. Leave the running Mac job untouched.
- **2026-11-03 approximately 19:23 ET, USER-STATED-EXPLICIT (PowerShell/TrueNAS output):** The first NAS Synology launcher failed when the container returned `immich: not found` after its built-in entrypoint was overridden; no timer was created. A corrected v2 launcher used the image's entrypoint and printed `PREFLIGHT PASS: 12600 distinct present files`, manifest SHA-256 `2fac247215b801978f931753c71141ecd8fe29b6265735325128bb3f1b676e66`, `3.3.5`, `CLI AUTH: PASS`, `CLI SAMPLE DRY RUN: PASS`, and `SCHEDULED`. The one-time `immichsyno.timer` is reported for **2026-11-03 23:23:22 EST**, activating `immichsyno.service`; expected log `/mnt/tank/general/immich-audit/synology-upload.log`. Source files remain read-only; Mac job was not restarted. **Component status: scheduled, not yet uploaded.** Reported timer output does not prove future execution or successful ingest.
- **Remaining acceptance:** after both jobs finish, verify service/runner exit results and reconcile per-source expected file sets against Immich asset records. Do not claim bulk ingestion COMPLETE from timer creation or a CLI dry run.
- Morning reconciliation: compare upload logs and Immich fingerprints against both final lists.

## 2026-11-03 evening: Gene's Immich closeout target for 2026-11-04

- **USER-STATED-EXPLICIT (Gene, 2026-11-03 evening):** "3 I can verify is working properly. All photos/ whatapp/etc have uploaded once I use tailscale on a wifi connection. we will reverify." This concerns ongoing native Immich Pixel backup (the earlier closeout item 3), not the still-running Mac bulk import or the NAS Synology upload.
- **USER-STATED-EXPLICIT (Gene, 2026-11-03 evening):** "I want all finished tomorrow asap to include amd gpu acceleration. good night." Target date: **2026-11-04**. AMD Radeon 780M iGPU acceleration for Immich machine learning is now **in scope for the next Immich closeout**, superseding the earlier optional/deferred categorization. No GPU configuration change has yet been executed or proven; check TrueNAS/Immich support and available device access, preserve CPU fallback, and verify actual GPU usage under a test workload before claiming acceleration.
- **Next closeout:** confirm both 30,873-file Mac manifest and 12,600-file Synology manifest upload outcomes with destination-side reconciliation; verify usability/indexing; reverify automatic Pixel Wi-Fi+Tailscale uploads (reported working by Gene); verify snapshots, database dumps and recovery; complete authorized housekeeping; configure and test Immich AMD GPU acceleration where supported without disrupting the functioning service.
- **Limits:** This entry is a target and user report, not proof that overnight jobs completed, GPU acceleration works, or the full Immich endpoint is complete. No family rollout, new backup destination, destructive cleanup, or unattended new action is authorized by this note.

## 2026-11-03 TrueNAS configuration backup

- USER-STATED (18:20 ET): config backup run "finished" (tar of /data/freenas-v1.db + /data/pwenc_secret, copied to the Envy C:\Users\genea\Documents\TrueNAS-config\ with SHA-256 compare; NAS temp copy removed on match). USER-STATED 18:57 ET: the run printed VERIFIED (SHA-256 match). Contains secrets: never in Git.
- CORRECTION (Claude): the first backup block captured `ssh -t` output in a PowerShell variable, which hid the sudo prompt; Gene waited over an hour. Rule: never capture or redirect the output of a command that prompts for a password; write results to a file on the remote side and fetch it separately.

## 2026-11-03 Plex media copied from the Synology (COMPLETE, verified)

- TOOL-VERIFIED (user-supplied log, 08:02 ET): systemd unit plexcopy ran ChatGPT's plex-full-transfer.sh (rsync --ignore-existing from read-only /tmp/syno/{Movies,TV} to /mnt/tank/plex/data/{Movies,TV}, then rsync -c checksum verify). Log: VERIFY PASS Movies, VERIFY PASS TV, COMPLETE 2026-11-03T12:54:18Z. Expected scope from preflight: Movies 785 files / 1.02 TB, TV 242 files / 60 GB. Nothing deleted; Synology sources untouched. Log: /mnt/tank/general/plex-migration/full-transfer.log.
- TOOL-VERIFIED 08:09 ET: container ix-plex-plex-1 healthy; /mnt/tank/plex/data is /data inside Plex; server "TrueNAS Plex" claimed to Plex account geneatwell; NO libraries existed (why nothing showed in Plex).
- DONE 08:11 ET (Gene ran, Claude verified): libraries created via the local server API (HTTP 201 each): "Movies" -> /data/Movies (type movie), "TV Shows" -> /data/TV (type show); scan started automatically.
- VERIFIED 08:19 ET: Plex Web at http://192.168.20.14:32400/web shows both libraries with metadata.
- Phone away from home (5G + Tailscale): "TrueNAS Plex is Currently Unavailable". Evidence: plex.tv lists only https 172.16.2.2:32400 (container bridge address) and lastSeenAt 2026-11-03T06:42:13Z does not advance.
- Changes made 08:36-08:44 ET (all reversible): customConnections = http://192.168.20.14:32400,http://100.97.199.3:32400; LanNetworksBandwidth = 192.168.20.0/24,100.64.0.0/10; Plex app network.host_network false -> true (app.update). Result: plex.tv listing UNCHANGED (still 172.16.2.2, lastSeen 06:42Z). Remote Access (PublishServerOnPlexOnlineKey) = 0.
- Plex policy (support.plex.tv): remote playback of personal video needs Plex Pass (server owner) or Remote Watch Pass; VPN connections may count as remote.
- OPEN, Gene decision: enable Plex Remote Access publishing vs replace Plex with Jellyfin (direct connection over Tailscale, no plex.tv broker, no remote fee).

## 2026-11-03 Plex Tailscale-only remote playback: Gene-confirmed success

This is the latest Plex outcome and supersedes the earlier failed-remote-playback / public-Remote-Access-versus-Jellyfin OPEN line above. Historical troubleshooting evidence remains unchanged.

- **USER-STATED-EXPLICIT (2026-11-03):** Gene confirmed native Plex playback on his Pixel by saying "Working" after testing with phone Wi-Fi off, cellular on, and Tailscale connected. **Endpoint 1: PASSED, USER-STATED-EXPLICIT.** This is Gene's report of the actual end-to-end playback test, not independent application telemetry.
- **VERIFIED from uploaded diagnostic log (2026-11-03, 08:41-09:02 ET):** Plex connection-registration PUT requests containing a raw Tailscale 100.x address received repeated HTTP 403 responses and backed off; the older Plex cloud connection listing remained stale. Other Plex cloud requests returned HTTP 200, so account authentication alone was not the failure.
- **VERIFIED from uploaded diagnostic log (09:18:15 ET):** Replacing the raw Tailscale custom access URL with the NAS MagicDNS hostname using HTTP resulted in HTTP 200 for the Plex server connection-registration PUT. This fixed registration at component level but did not by itself satisfy the native Android playback endpoint.
- **VERIFIED from Gene's TrueNAS Tailscale-app shell output (2026-11-03):** Existing tailnet-only HTTPS Serve mapping on port 443 to Nextcloud's local backend was preserved; a separate tailnet-only HTTPS Serve mapping on port 8443 to Plex's local backend was added. Pre/post status output confirmed the existing Nextcloud handler remained unchanged. No Funnel or router port forwarding was enabled.
- **VERIFIED from Gene's Plex Network settings screenshot (2026-11-03):** Custom server access URLs was saved as the NAS's MagicDNS HTTPS endpoint on port 8443. Plex local-network bandwidth policy was left as previously configured. The subsequent Pixel app playback is the actual acceptance evidence.
- **VERIFIED from Gene's TrueNAS installed-app screenshot (2026-11-03):** Updated Plex app shows Plex Media Server version `1.43.6.11085-d1e52e169`, TrueNAS chart version `1.3.24`, with rollback available. This screenshot proves the installed version. **USER-STATED-EXPLICIT (2026-11-03, subsequent confirmation):** Gene reports that native Plex playback on his Pixel works after this server upgrade. **Post-upgrade Pixel playback: PASSED (Gene's direct acceptance report).** This does not constitute a second independent device-level test by ChatGPT.
- **USER-STATED-EXPLICIT:** Gene is **not ready to distribute Plex access to family**. Family access/permissions/invitations remain ON HOLD; no family rollout is authorized. Existing family tailnet rules do not yet grant the Plex HTTPS port; any later expansion is a separate Gene decision.
- **UNRESOLVED:** Plex transcoding under actual transcoding conditions. A public Plex Remote Access configuration is not part of the accepted Tailscale-only design.

**DACP handoff guard:** Do not re-open the solved raw-IP registration issue or propose public port forwarding. Native Pixel playback was confirmed by Gene both before and after the Plex server upgrade. Family rollout remains held until Gene explicitly authorizes it; do not relabel the post-upgrade Pixel endpoint OPEN without newer contradictory evidence.

## 2026-11-02 photo backup scope rule (Gene, verbatim)

- USER-STATED-EXPLICIT 20:56 ET: "i only want the myriad backups of the skyhawk association downloaded over the years to NOT be included in the backup to the NAS. we are already backing up the live site to the mac and that is fine for what we are doing with the skyhawk association. my own photos taken of any aircraft are to be saved to the NAS."
- Applied as: exclude copies of the Skyhawk website (downloaded site backups, site file trees, files identical to live-site files); keep every personal photo, including aircraft photos. File-name patterns (BuNo, squadron) are NOT used to exclude, because they would catch Gene's own aircraft photos.
- 2026-11-02 comparison (exact bytes): 13,240 distinct Synology photo-share files (24.1 GB) are not in the Mac archive; list in dacp-private evidence/photo-compare-20261102. Site copies not yet removed from that count.

## 2026-11-02 evening: family SMB shares (ChatGPT build, Claude diagnosis)

- Built by ChatGPT (handoff 2026-11-02, scripts/results in the Envy dacp-work folder): dataset tank/general/family-smb (NFSv4 ACL), group family_smb (GID 3000), SMB users jake, jennie, philip, jo-anne, shares FamilyShared (browsable) and <user>Private (not browsable) for each, SMB1 off, guest off (restrict anonymous = 2).
- TOOL-VERIFIED (Claude, read-only, 18:40 ET): middleware cifs RUNNING and enabled; smbd/nmbd/winbind active; 445/139 listening; all five shares loaded; all four users in the Samba passdb with normal flags. The earlier interrupted service-start job did complete.
- ROOT CAUSE (TOOL-VERIFIED): Windows logins failed because Samba itself rejected the passwords (smbclient on the NAS: NT_STATUS_LOGON_FAILURE). Gene reset each password in the TrueNAS UI; afterwards all four users pass on the NAS (smbclient //127.0.0.1): FamilyShared OK, own Private OK, another user's Private NT_STATUS_ACCESS_DENIED (isolation holds). Listing tests only, no files written.
- TOOL-VERIFIED 18:56 ET: Windows 11 (Envy) over Tailscale to \\100.97.199.3 as jake: net use FamilyShared exit 0, write OK (test file smb-test-jake.txt left in FamilyShared), jakePrivate listed, connections removed afterwards. The Envy is in group:trusted, so this proves the NAS side over Tailscale, not the family restriction.
- USER-DIRECTED 2026-11-02: family members are never at home and need the shares away from home. Change given to Gene: family grant ip ["tcp:30041","tcp:445"] (dst nas only). USER-SUPPLIED policy text 19:02 ET shows the family grant as ["tcp:30041", "tcp:445"] to "nas"; trusted, exit-node and ssh sections unchanged.
- OPEN: proof from a family device away from home (SMB reachable, own private share only); Mac test; which device types the family uses (Windows / Mac / iPhone / Android).

## Next sequence - status as of 2026-10-31 22:20 ET

| # | Item | Status |
|---|---|---|
| 1 | Physical closeout and final placement | DONE (before the Spain trip; USER-STATED) |
| 2 | Tailscale remote access | DONE; access policy now group-based (2026-10-31 night section) |
| 3 | App commissioning | Immich DONE (v3.3.5, Pixel backup verified, 4 family accounts). Plex transcoding test OPEN. Nextcloud users OPEN (quota now ~250 GB/person for small files, not 3 TB). Immich GPU ML deferred. |
| 4 | Snapshot tasks | tank/immich DONE (pre-existing task, 3 weeks daily 03:10). tank/general and tank/nextcloud OPEN - tank/general now receives the Synology photo copy. |
| 5 | SMB shares + non-admin user for Envy/Mac | OPEN; to be designed with music, Time Machine and Windows backup targets |
| 6 | Migration from the Synology / HTPC | REDEFINED 2026-10-31: HTPC Backup not needed (no photos). Photo share COPIED and verified 2026-11-01. Drupal dumps COPIED 2026-11-01. Movies+TV (~1.1 TB) not started. homes Drive backups measured, copy undecided. Search remaining shares before any wipe |
| 7 | Second / off-site copy | OPEN; old Synology to be a plain SMB target after it is searched and wiped; off-site still required |
| 8 | UPS | SUPERSEDED: three UPS units plus whole-house generator (USER-STATED 2026-10-27) |
| 9 | Housekeeping | OPEN (config backup after today's changes recommended) |
| 10 | HBA firmware / no-video fault | OPEN, only if it recurs |

Additional OPEN items: Immich External domain setting; family-group Tailscale restriction to be proven from the first family phone; NAS SSH to be switched off after the Synology work; Mac archive into Immich (External Library proposed); music location and sizes.

## Next sequence (2026-10-14) - original list, kept for history

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
