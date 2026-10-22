"""Check published assets and chapter routes before deployment."""
import json, re
from pathlib import Path
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
    if path and not (root / path).is_file():
        errors.append(f'{source}: missing {path}')
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
app = (root / 'app.js').read_text()
for name in re.findall(r"\{id:'([^']+)'", app):
    for suffix in ('.webp', '-thumb.webp'):
        check_url('assets/' + name + suffix, name)
assert len(ids) == len(chapters), 'Duplicate chapter IDs'
assert (root / 'fashion-atlas.pdf').read_bytes().startswith(b'%PDF-'), 'Missing or invalid PDF'
assert not errors, '\n'.join(errors)
print(f'Validated {len(chapters)} reading entries, local assets and PDF.')
