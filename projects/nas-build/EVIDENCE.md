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

This establishes purchase-source provenance and a current missing-cable condition; it does not by itself prove what accessories the seller's product page promised at checkout.

## HBA document intake

Three HBA-related PDFs were supplied directly in the working session and hashed before canonical indexing:

- `LSISAS9207-8i_UG_v2-2.pdf` — SHA-256 `61bb97fd099f10ce07d2489510acdd7f0ee3fefcb63db7c866071d4e05cc4df6`.
- `LSI_SAS_9207-8i_QIG.pdf` — SHA-256 `e2b5402d3c3ae32420bec4e8331491d8e4b522550a5fa8b7c82a7d23f1749f04`.
- `SAS2_Flash_Utility_Software_Ref_Guide.pdf` — SHA-256 `04708a22726274be2ea673940611b332993f367b94f8aaf782311f498182c978`.

The exact binaries remain outside public Git under the project binary-document policy. Their identities, hashes, official source links, and build-relevant facts are persisted in `REFERENCES.md` and `references/HBA_LSI_SAS9207-8i.md`.
