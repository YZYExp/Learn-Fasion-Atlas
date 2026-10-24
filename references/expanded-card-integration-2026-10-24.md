# Expanded atlas cards: integration checkpoint (2026-10-24)

This checkpoint tracks **19 generated editorial cards** across **17 chapters**.
The original 72 teaching plates remain untouched.

## Status
- The new picture files have been generated in the working session and packaged externally.
- The source PNG files have **not yet been uploaded to this GitHub repository**.
- This commit provides the authoritative mapping and an idempotent integration script.
- Public chapter links will only change once all required PNGs have been transferred and validated.

## Workflow
1. Supply all 19 PNG files listed in `expanded-card-manifest-2026-10-24.json` to a local folder.
2. Run `python scripts/integrate_expanded_cards.py --source /path/to/pngs`.
3. Run `python scripts/integrate_expanded_cards.py --check`.
4. Run the existing book build, PDF export and Pages site checker, then inspect small-screen layouts.
5. Commit the PNG files, updated chapters, generated manuscript and verified outputs together.

## Editorial QA
These composites are **examples rather than exhaustive taxonomies**. Check Chinese and English labels, garment/pose continuity, and category-vs-construction ambiguity. The current drafts are not authoritative for historical Hanfu garment construction, textile composition, or unseen closures. Retain existing verified images and captions; the importer adds supplemental cards rather than replacing their evidence.
