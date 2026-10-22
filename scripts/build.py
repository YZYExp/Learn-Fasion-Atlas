#!/usr/bin/env python3
"""Validate local Markdown links and assemble the reading manuscript; no HTML."""
from pathlib import Path
import argparse
import json
import re
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'(!?\[[^\]]*\]\()([^\s)]+)(\))')

def local_target(source, url):
    if url.startswith('#') or urlparse(url).scheme:
        return None
    return (source.parent / unquote(url.split('#')[0])).resolve()

def validate():
    errors = []
    manifest = json.loads((ROOT / 'book.json').read_text())
    files = [ROOT / c['source'] for c in manifest['chapters']]
    actual = set((ROOT / 'chapters').glob('*.md'))
    if set(files) != actual:
        errors.append('Chapter manifest does not match source files')
    for source in [*files, *sorted((ROOT / 'appendices').glob('*.md')), ROOT / 'README.md']:
        text = source.read_text(encoding='utf-8')
        if len(text) < 500:
            errors.append(f'Too little text: {source.name}')
        for match in LINK.finditer(text):
            target = local_target(source, match.group(2))
            if target and not target.is_file():
                if source.name == 'README.md' and target.name in ('book.md', 'garment-details.md'):
                    continue
                errors.append(f'Missing local target: {source.name}: {match.group(2)}')
        if re.search(r'\bTODO\b|待生成|占位图', text):
            errors.append(f'Unfinished content: {source.name}')
    image_records = []
    for manifest in ('images.json', 'detail-plan.json', 'variation-plan.json', 'hanfu-cosplay-images.json', 'expansion-images-a.json', 'expansion-images-b.json'):
        image_records.extend(json.loads((ROOT / 'references' / manifest).read_text(encoding='utf-8')))
    for image in image_records:
        if not (ROOT / image['file']).is_file() or not image.get('prompt'):
            errors.append(f'Incomplete image record: {image.get("id")}')
    if errors:
        raise SystemExit('\n'.join(errors))
    return files

def rebase(source, text):
    def sub(match):
        url = match.group(2)
        target = local_target(source, url)
        if target is None:
            return match.group(0)
        new_url = target.relative_to(ROOT).as_posix()
        if '#' in url:
            new_url += '#' + url.split('#', 1)[1]
        return match.group(1) + new_url + match.group(3)
    return LINK.sub(sub, text)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    chapters = validate()
    sources = [*chapters, *sorted((ROOT / 'appendices').glob('*.md')), ROOT / 'references/sources.md']
    if not args.check:
        heading = '# 衣着有名：从风格识别到单品描述\n\n中文图解兴趣读本 · 扩充版 · 2026-10-22\n\n'
        toc = '\n'.join(f'- [{p.read_text(encoding="utf-8").splitlines()[0].lstrip("# ")}]({p.relative_to(ROOT).as_posix()})' for p in sources)
        content = '\n\n---\n\n'.join(rebase(p, p.read_text(encoding='utf-8')) for p in sources)
        (ROOT / 'book.md').write_text(heading + toc + '\n\n---\n\n' + content, encoding='utf-8')
        detail_sources = [p for p in chapters if int(p.name[:2]) >= 13]
        detail_sources.append(ROOT / 'appendices/03-garment-words.md')
        detail_heading = '# 衣着有名：人物衣着与单品细节分册\n\n从连衣裙、蕾丝与领袖开始，学会说清人物穿着。\n\n'
        detail_toc = '\n'.join(f'- [{p.read_text(encoding="utf-8").splitlines()[0].lstrip("# ")}]({p.relative_to(ROOT).as_posix()})' for p in detail_sources)
        detail_content = '\n\n---\n\n'.join(rebase(p, p.read_text(encoding='utf-8')) for p in detail_sources)
        (ROOT / 'garment-details.md').write_text(detail_heading + detail_toc + '\n\n---\n\n' + detail_content, encoding='utf-8')
    print(f'Checked {len(chapters)} chapter files, {len(sources)-len(chapters)-1} appendices and all local references.')

if __name__ == '__main__':
    main()
