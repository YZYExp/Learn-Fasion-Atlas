"""Check published assets and chapter routes before deployment."""
import hashlib, json, re
from pathlib import Path
from PIL import Image
from urllib.parse import urlsplit, parse_qs, unquote

root = Path(__file__).resolve().parent / 'dist'
chapters = json.loads((root / 'content.json').read_text())
ids = {c['id'] for c in chapters}
errors = []
def check_url(url, source):
    if url.startswith(('http:', 'https:', 'mailto:', 'data:', '#')):
        return
    parsed = urlsplit(url)
    path = unquote(parsed.path)
    if path.startswith('review/') or path.endswith('image-index.html'):
        errors.append(f'{source}: internal review link leaked into reading site')
    if path and not (root / path).is_file():
        errors.append(f'{source}: missing {path}')
    version = parse_qs(parsed.query).get('v', [None])[0]
    if version and path and (root / path).is_file():
        actual = hashlib.sha256((root / path).read_bytes()).hexdigest()[:12]
        if version != actual:
            errors.append(f'{source}: stale version for {path}')
    if path == 'read.html':
        chapter = parse_qs(parsed.query).get('chapter', [''])[0]
        if chapter and chapter not in ids:
            errors.append(f'{source}: unknown chapter {chapter}')
for c in chapters:
    for url in re.findall(r'(?:src|href)="([^"]+)"', c['html']):
        check_url(url, c['id'])
for file in root.glob('*.html'):
    for url in re.findall(r'(?:src|href)="([^"]+)"', file.read_text()):
        check_url(url, file.name)
    for url in re.findall(r"url\('([^']+)'\)", file.read_text()):
        check_url(url, file.name)
for file in [root/'app.js',root/'reader.js']:
    for url in re.findall(r"fetch\('([^']+)'\)",file.read_text()):
        check_url(url,file.name)
atlas=json.loads((root / 'atlas.json').read_text())
for board in atlas:
    check_url('assets/'+board['id']+'.webp',board['id'])
    assert board['chapter'] in ids, f"Unknown atlas chapter: {board['id']}"
    assert board.get('audience') in {'mens','womens','mixed'}, f"Missing audience: {board['id']}"
    assert board['width']>0 and board['height']>0
expected={p.stem for p in (root/'assets').glob('*.webp') if not p.stem.endswith('-thumb') and p.stem!='12-silhouettes'}
assert {b['id'] for b in atlas} == expected, 'Gallery does not cover all photographic plates'
meta=json.loads((root/'book-meta.json').read_text())
assert set().union(*(set(g['ids']) for g in meta['groups'])) == ids, 'Reading groups omit chapters'
for image in (root / 'assets').glob('*.webp'):
    Image.open(image).verify()
assert len(ids) == len(chapters), 'Duplicate chapter IDs'
for name in ['fashion-atlas.pdf','menswear-atlas.pdf']:
    assert (root / name).read_bytes().startswith(b'%PDF-'), f'Missing or invalid PDF: {name}'
assert not (root/'review').exists() and not (root/'image-index.html').exists(), 'Internal review file in published bundle'
assert not errors, '\n'.join(errors)
print(f'Validated {len(chapters)} reading entries, local assets and PDF.')
