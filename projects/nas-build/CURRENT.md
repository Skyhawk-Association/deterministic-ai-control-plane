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
- CS383 rear cable bundle observed on the cable-management side of the motherboard tray, not trapped under the motherboard footprint.
- Motherboard installed in the CS383 on nine matched standoffs; all nine motherboard screws were started by hand and then snugged evenly without over-tightening.
- HBA, boot SSDs, eight data drives, and PSU have not yet been installed into their final chassis positions.
- HBA installation is currently blocked: the metal bracket attached to the LSI 9207-8i interfered with proper seating in the CS383 slot opening. Gene removed that bracket. The HBA is therefore not yet verified as securely retained and must not be treated as installation-complete or powered in an unsecured state.

## Software / installer state

- TrueNAS Community Edition target: 25.10.7.
- Windows PowerShell reported `RESULT=TRUENAS_ISO_VERIFIED`.
- Installer USB has not yet been written from the verified ISO.
- The intended installer USB must be re-identified by physical device identity immediately before writing; do not target a drive letter alone.

## Known corrections to older planning material

- Current data-drive count is eight, not six.
- The MSI motherboard has an integrated rear I/O shield; do not perform a separate loose-I/O-shield installation step.
- Case cable-management wiring visible behind the motherboard tray is not an obstruction under the motherboard.
- Manufacturer documentation controls standoff placement, PSU sequence/orientation, connector use, and HBA installation when it conflicts with the planning guides.

## Next hardware sequence

1. Lay the CS383 for motherboard installation and inspect the motherboard tray.
2. Match chassis standoffs to actual MSI motherboard mounting holes. Remove or relocate any standoff that would sit under solid PCB.
3. Lower the assembled motherboard onto only the matched standoffs, align integrated rear I/O, start all board screws loosely, then secure evenly without over-tightening.
4. Before access becomes restricted, connect case front-panel, front USB, front audio, required fan headers, and motherboard-side SATA/data connections.
5. Install the LSI SAS 9207-8i in the motherboard slot selected from the MSI slot topology; verify full seating and bracket retention.
6. Route the two internal mini-SAS data paths from the HBA toward the CS383 backplane without sharp bends or fan interference.
7. Install the two boot SSDs in the CS383-supported 2.5-inch locations and connect their SATA data paths.
8. Outside the case, attach the exact required Seasonic modular cables: motherboard 24-pin pair at the PSU, required CPU/EPS cable(s), and required SATA/peripheral power leads.
9. Install the PSU in the chassis only after required modular cables are attached and PSU orientation is verified against both the CS383 airflow geometry and Seasonic guidance.
10. Complete motherboard, boot-SSD, and backplane power connections.
11. Install and map the eight IronWolf drives by bay.
12. Perform a no-AC pre-power inspection.
13. First POST with monitor/keyboard; verify CPU, 64 GB RAM, sane CPU temperature/fan behavior, boot devices, and HBA visibility before TrueNAS installation.
14. Flash and verify the TrueNAS installer USB, then install only after destination boot devices are unambiguously identified.

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
