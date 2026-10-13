# NAS Build Current State

Status date: 2026-10-12

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

## Software / installer state

- IMAGE-EVIDENCED 2026-10-13: Selecting `UEFI: PNY USB 2.0 FD PMAP, Partition 1` from the MSI F11 boot menu returned immediately to the same boot-device menu instead of starting the TrueNAS installer. This narrows the current blocker to the installer-media/UEFI boot path rather than the Windows Boot Manager entry on the Crucial SSD.

- TrueNAS Community Edition target: 25.10.7.
- Windows PowerShell reported `RESULT=TRUENAS_ISO_VERIFIED`.
- TrueNAS installer USB has already been created and is standing by for installation.
- Monitor and keyboard are standing by for first POST/BIOS and TrueNAS installation.

## Known corrections to older planning material

- Current data-drive count is eight, not six.
- The MSI motherboard has an integrated rear I/O shield; do not perform a separate loose-I/O-shield installation step.
- Case cable-management wiring visible behind the motherboard tray is not an obstruction under the motherboard.
- Manufacturer documentation controls standoff placement, PSU sequence/orientation, connector use, and HBA installation when it conflicts with the planning guides.

## Next hardware sequence

1. Enter BIOS setup or the F11 boot menu using a rear motherboard USB keyboard connection.
2. Set the correct BIOS date/time before installing TrueNAS.
3. Confirm both boot SSDs are visible in BIOS Storage as SATA_S1 / SATA_S2.
4. Confirm drive-cage fan RPM visibility; prior BIOS observation showed SYS Fan 1 as N/A and should not be assumed resolved.
5. Boot the already-created TrueNAS Community Edition 25.10.7 installer USB.
6. For the initial TrueNAS installation, use the 250 GB Crucial MX500 as the sole connected internal boot target and keep the used Patriot Burst Elite 240 GB disconnected. After TrueNAS is proven booting from the Crucial, reconnect the Patriot only for deliberate erase/attachment as the boot-pool mirror. Do not select any of the eight 12 TB IronWolf data drives.
7. After installation, check MX500 SMART wear and verify the LSI 9207-8i operating mode/firmware identity before considering any firmware action.

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
