#!/usr/bin/env python3
"""Integrate reviewed atlas cards without replacing historical teaching plates.

Usage:
  python scripts/integrate_expanded_cards.py --source /path/to/generated/pngs
  python scripts/integrate_expanded_cards.py --check

The source directory contains the original generated image filenames listed in
references/expanded-card-manifest-2026-10-24.json.
"""
from __future__ import annotations
import argparse, json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references/expanded-card-manifest-2026-10-24.json"
ASSET_ROOT = ROOT / "assets/images"

def integrate(source: Path | None = None, check: bool = False) -> None:
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = []
    edited = []
    for entry in entries:
        dst = ROOT / entry["asset"]
        original = source / entry["source"] if source else None
        if original and not dst.exists():
            if not original.is_file():
                errors.append(f"Missing source: {original}")
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, dst)
        if not dst.is_file():
            errors.append(f"Card unavailable: {dst}")
            continue
        magic = dst.read_bytes()[:8]
        if magic != b"\x89PNG\r\n\x1a\n":
            errors.append(f"Not a PNG: {dst}")
            continue
        chapter = ROOT / entry["chapter"]
        body = chapter.read_text(encoding="utf-8")
        marker = f"![{entry['alt']}](../{entry['asset']})"
        if marker in body:
            continue
        if check:
            errors.append(f"Card not embedded: {entry['chapter']}: {entry['asset']}")
            continue
        old_image = re.search(r"!\[[^\]]*\]\(\.\./" + re.escape(entry["anchor"]) + r"\)", body)
        if not old_image:
            errors.append(f"Anchor missing: {entry['chapter']}: {entry['anchor']}")
            continue
        # Insert after the original image caption, preserving its 6-panel-specific claims.
        after = body[old_image.end():]
        caption = re.match(r"\s*\n\*[^\n]*\*\s*\n", after)
        insert_at = old_image.end() + (caption.end() if caption else 0)
        snippet = (
            "\n\n" + marker + "\n\n"
            + "*扩展观察图卡（AI 教学示意）："
            + entry["caption"] + "。图中例子不是完整分类；细部判断请结合本章原图和正文。*\n"
        )
        if not check:
            body = body[:insert_at] + snippet + body[insert_at:]
            chapter.write_text(body, encoding="utf-8")
        edited.append(entry["chapter"])
    if errors:
        raise SystemExit("\n".join(errors))
    if not check:
        print("Updated chapters:", len(set(edited)), "; regenerate book.md and PDFs using project build scripts.")
    else:
        print("Validated", len(entries), "PNG cards and chapter anchors.")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, help="Directory containing generated PNG files")
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    integrate(args.source, args.check)
