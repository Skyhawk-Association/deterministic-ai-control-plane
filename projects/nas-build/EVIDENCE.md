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
