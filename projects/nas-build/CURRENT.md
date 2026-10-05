# NAS Build Current State

Status date: 2026-10-03

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
- CS383 rear cable bundle observed on the cable-management side of the motherboard tray, not trapped under the motherboard footprint.
- Motherboard installed in the CS383 on nine matched standoffs; all nine motherboard screws were started by hand and then snugged evenly without over-tightening.
- Front-panel JFP1 wiring completed: HDD LED on pins 1/3, Power LED on 2/4, Reset SW on 5/7, Power SW on 6/8; NIC1/NIC2 LED leads are unused on this motherboard.
- Front HD AUDIO connected to JAUD1.
- Front USB 5 Gbps Type-A cable connected to JUSB3.
- Front USB-C cable connected to JUSBC1.
- Final fan header map: rear case fan on SYS_FAN1; right front drive-cage fan on SYS_FAN5; left front drive-cage fan on SYS_FAN6.
- Rear expansion-slot cover aligned with PCI_E1 removed in preparation for HBA installation.
- Both boot SSDs are physically secured in their final CS383 mounting positions. All eight IronWolf 12 TB drives are installed in the CS383 hot-swap bays and seated without force. The HBA retention and PSU installation remain incomplete.
- LSI 9207-8i is now fully seated in PCI_E1 with its incompatible silver metal bracket removed. Full seating is based on Gene's direct physical report. Chassis retention remains unresolved, so the HBA is not yet installation-complete and the system must not be powered with the HBA unsecured.
- Boot SSD connections completed: Crucial MX500 and Patriot Burst Elite are both physically secured, have SATA data connected to SATA_S1/SATA_S2 respectively, and have SATA power connected.
- Two Cable Matters 0.5 m / 1.6 ft SFF-8087-to-4x-SATA forward-breakout cables were ordered from Amazon on 2026-10-04, with estimated delivery 2026-10-05; these are intended to connect the LSI 9207-8i's J5/J6 ports to the eight CS383 backplane SATA data inputs.
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

## Software / installer state

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

1. Lay the CS383 for motherboard installation and inspect the motherboard tray.
2. Match chassis standoffs to actual MSI motherboard mounting holes. Remove or relocate any standoff that would sit under solid PCB.
3. Lower the assembled motherboard onto only the matched standoffs, align integrated rear I/O, start all board screws loosely, then secure evenly without over-tightening.
4. Case front-panel, front USB, front audio, and the two drive-cage PWM fan leads are connected to the motherboard as recorded above.
5. Resolve the LSI SAS 9207-8i bracket/chassis mismatch. Do not power the system with the HBA unsecured. After the correct retention method is established, install the HBA in PCI_E1, verify full seating and chassis retention, then route the two internal SFF-8087 paths without sharp bends or fan interference.
6. Boot SSD SATA data and power connections are complete.
8. Outside the case, attach the exact required Seasonic modular cables: motherboard 24-pin pair at the PSU, required CPU/EPS cable(s), and required SATA/peripheral power leads.
9. Install the PSU in the chassis only after required modular cables are attached and PSU orientation is verified against both the CS383 airflow geometry and Seasonic guidance.
10. Complete motherboard, boot-SSD, and backplane power connections.
11. Eight IronWolf drives are installed; verify physical bay numbering against the recorded tray serial inventory before first power.
12. Perform a no-AC pre-power inspection.
13. First POST with monitor/keyboard; verify CPU, 64 GB RAM, sane CPU temperature/fan behavior, boot devices, and HBA visibility before TrueNAS installation.
14. Use the already-created TrueNAS installer USB only after destination boot devices are unambiguously identified.

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
