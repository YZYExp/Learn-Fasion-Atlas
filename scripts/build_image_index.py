#!/usr/bin/env python3
"""Build one offline image-review file. Deliberately separate from book/site outputs."""
from __future__ import annotations

import base64
import hashlib
import html
import io
import json
import re
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'review/image-index.html'
IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^\s)]+)\)')


def esc(value):
    return html.escape(str(value), quote=True)


def display(value):
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, indent=2)
    return str(value)


def image_records(value):
    """Accept historic list/nested-object schemas without assuming every JSON is a plan."""
    if isinstance(value, dict):
        if any(isinstance(value.get(k), str) for k in ('prompt', 'review')) and any(
            isinstance(value.get(k), str) and value[k].lower().endswith('.png')
            for k in ('file', 'path', 'asset')
        ):
            yield value
        for child in value.values():
            if isinstance(child, (dict, list)):
                yield from image_records(child)
    elif isinstance(value, list):
        for child in value:
            yield from image_records(child)


def collect_records():
    result = {}
    for path in sorted((ROOT / 'references').glob('*.json')):
        data = json.loads(path.read_text(encoding='utf-8'))
        for record in image_records(data):
            filename = record.get('file') or record.get('path') or record.get('asset')
            key = Path(filename).name
            result.setdefault(key, []).append((path.relative_to(ROOT).as_posix(), record))
    return result


def collect_uses():
    result = {}
    book = json.loads((ROOT / 'book.json').read_text(encoding='utf-8'))
    paths = [ROOT / c['source'] for c in book['chapters']]
    paths += [ROOT / a for a in book['appendices']]
    paths.append(ROOT / 'references/sources.md')
    for path in paths:
        text = path.read_text(encoding='utf-8')
        title = text.splitlines()[0].lstrip('# ')
        for match in IMAGE_RE.finditer(text):
            target = (path.parent / match[2].split('#')[0]).resolve()
            if target.parent != (ROOT / 'assets/images').resolve():
                continue
            after = text[match.end():].lstrip()
            paragraph = after.split('\n\n', 1)[0]
            caption = paragraph.strip('* \n') if paragraph.startswith('*') else ''
            result.setdefault(target.name, []).append({
                'source': path.relative_to(ROOT).as_posix(),
                'line': text.count('\n', 0, match.start()) + 1,
                'title': title,
                'alt': match[1],
                'caption': caption,
            })
    return result


def metadata_block(label, value):
    return f'<div class="field"><dt>{esc(label)}</dt><dd><pre>{esc(display(value))}</pre></dd></div>'


def main():
    records = collect_records()
    uses = collect_uses()
    atlas = {x['id']: x for x in json.loads((ROOT / 'web/atlas.json').read_text(encoding='utf-8'))}
    audience_names = {'mens': '男装示例', 'womens': '女装示例', 'mixed': '中性／混合示例'}
    sources = sorted((ROOT / 'assets/images').glob('*.png'))
    cards = []
    total_bytes = 0
    derivative_count = 0
    referenced = 0
    for path in sources:
        raw = path.read_bytes()
        total_bytes += len(raw)
        digest = hashlib.sha256(raw).hexdigest()
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(raw)))
        im.load()
        width, height = im.size
        if im.mode not in ('RGB', 'RGBA'):
            im = im.convert('RGBA' if 'transparency' in im.info else 'RGB')
        im.thumbnail((1536, 1536), Image.Resampling.LANCZOS)
        buffer = io.BytesIO()
        im.save(buffer, 'WEBP', quality=85, method=6)
        preview = base64.b64encode(buffer.getvalue()).decode('ascii')
        source_path = path.relative_to(ROOT).as_posix()
        use_list = uses.get(path.name, [])
        in_book = bool(use_list)
        referenced += in_book
        plan_records = records.get(path.name, [])
        info = atlas.get(path.stem, {})
        title = info.get('title') or next((r.get('title') for _, r in plan_records if r.get('title')), None)
        title = title or (use_list[0]['alt'] if use_list else path.stem)
        audience = info.get('audience', 'unknown')
        audience_label = audience_names.get(audience, '未分类／方法图')
        derivatives = sorted((ROOT / 'web/dist/assets').glob(path.stem + '*.webp'))
        derivative_count += len(derivatives)
        # Do not infer a review verdict where old records contain no verdict.
        details = metadata_block('源文件', source_path)
        details += metadata_block('尺寸／文件大小', f'{width} × {height} px · {len(raw):,} bytes')
        details += metadata_block('SHA-256', digest)
        for use in use_list:
            details += metadata_block('书稿引用', f"{use['title']}\n{use['source']}:{use['line']}")
            details += metadata_block('替代文字', use['alt'])
            details += metadata_block('当前图注', use['caption'] or '该图片后未找到独立斜体图注')
        if not use_list:
            details += metadata_block('书稿引用', '未在 book.json 所列章节、附录或书末资料中引用')
        details += metadata_block('网页衍生资源', '\n'.join(
            f'{p.relative_to(ROOT).as_posix()} · {p.stat().st_size:,} bytes' for p in derivatives
        ) or '暂无匹配衍生文件')
        for record_path, record in plan_records:
            details += metadata_block('制作记录来源', record_path)
            for key, label in [('panels', '分格记录'), ('review', '审图记录'),
                               ('limitations', '已知限制'), ('notes', '补充说明'),
                               ('status', '制作状态')]:
                if record.get(key) not in (None, '', [], {}):
                    details += metadata_block(label, record[key])
            details += '<details class="prompt"><summary>查看原始提示词</summary>'
            details += f'<pre>{esc(record.get("prompt", "用户提供图片；原始提示词未提供。"))}</pre></details>'
            for key in ('edit_prompt', 'revision_prompt', 'revision_prompts'):
                if record.get(key):
                    details += metadata_block('定向修订提示词', record[key])
        if not plan_records:
            details += metadata_block('制作记录', '未匹配到图像生成记录；几何示意等程序绘图可能没有生成提示词')
        search = ' '.join([path.stem, title, source_path, audience_label] + [
            u['title'] + ' ' + u['source'] + ' ' + u['caption'] for u in use_list
        ])
        status = '已入书' if in_book else '未入书'
        cards.append(f'''<article class="card" data-status="{'used' if in_book else 'unused'}" data-audience="{esc(audience)}" data-search="{esc(search.lower())}">
<div class="card-head"><span class="number">{esc(path.stem.split('-')[0])}</span><h2>{esc(title)}</h2><span class="badge {'used' if in_book else 'unused'}">{status}</span></div>
<button class="image-button" aria-label="放大图 {esc(path.stem)}"><img src="data:image/webp;base64,{preview}" width="{width}" height="{height}" alt="{esc(title)}，完整图板" loading="lazy" decoding="async"><span>放大完整图板 ↗</span></button>
<p class="filename">{esc(path.name)}</p><p class="small">{esc(audience_label)} · {width} × {height} · {len(raw) / 1024 / 1024:.2f} MiB 原图</p>
<details class="metadata"><summary>章节、图注与审图记录</summary><dl>{details}</dl></details></article>''')
    header = f'''<header><p class="eyebrow">FASHION ATLAS · IMAGE REVIEW</p><h1>所有图片审查索引</h1><p class="notice">审查用，不进入书籍或在线阅读目录。</p><p>共 <strong>{len(sources)}</strong> 张源 PNG；其中 <strong>{referenced}</strong> 张已入书、<strong>{len(sources) - referenced}</strong> 张未入书。网页 WebP／缩略图共 <strong>{derivative_count}</strong> 个，归在对应原图项下，不重复计图。</p><p class="small">本文件内嵌保留全图比例的 WebP 预览，可离线搜索和放大。预览最长边不超过 1536 px，采用有损压缩；精确像素审查请用列出的工程内 PNG 原图和 SHA-256。路径是工程定位信息，单独下载本文件不需要携带图片文件夹。</p><p class="small">“已入书”按 book.json 的章节、附录和书末资料中的实际图片引用计算；制作记录与图注据现有文件摘录，不自动判定服饰结构正确。</p></header>'''
    controls = '''<section class="toolbar" aria-label="索引筛选"><label>搜索图号、文件名或章节<input id="search" type="search" placeholder="例如 67、吊带、35-mens…"></label><label>引用状态<select id="status"><option value="all">全部</option><option value="used">已入书</option><option value="unused">未入书</option></select></label><label>展示方向<select id="audience"><option value="all">全部</option><option value="mens">男装示例</option><option value="womens">女装示例</option><option value="mixed">中性／混合示例</option><option value="unknown">未分类／方法图</option></select></label><button id="reset" type="button">清空筛选</button><p id="count" role="status" aria-live="polite"></p></section>'''
    css = '''*{box-sizing:border-box}body{margin:0;background:#f5f3ed;color:#25383c;font:15px/1.65 system-ui,-apple-system,"Segoe UI","Noto Sans CJK SC",sans-serif}main{max-width:1500px;margin:auto;padding:34px 24px}header{max-width:1000px;margin-bottom:26px}h1{font-size:32px;margin:0 0 12px;font-weight:600}.eyebrow{font-size:11px;letter-spacing:.15em;color:#6d7c7d}.notice{display:inline-block;background:#e1ebe6;padding:6px 12px;margin:0 0 8px}.small{font-size:12px;color:#617174}.toolbar{display:flex;flex-wrap:wrap;align-items:end;gap:14px;padding:18px 0;border-block:1px solid #cfd7d4;margin-bottom:24px;position:relative}.toolbar label{display:grid;gap:5px;font-size:12px}.toolbar label:first-child{flex:1;min-width:220px}input,select,button{font:inherit}input,select{border:1px solid #aebdba;border-radius:4px;background:#fff;padding:9px 10px;color:inherit}button{cursor:pointer}#reset{background:#e5ece8;border:1px solid #b7c3bf;padding:9px 14px;border-radius:4px}#count{font-size:12px;flex-basis:100%;margin:0}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}.card{min-width:0;background:#fff;border:1px solid #d7ddda;border-radius:7px;padding:14px;align-self:start}.card[hidden]{display:none}.card-head{display:flex;align-items:start;gap:9px;margin:0 0 12px}.number{font-size:12px;color:#657b79;padding-top:3px}h2{font-size:16px;line-height:1.4;margin:0;flex:1;min-width:0}.badge{font-size:10px;white-space:nowrap;padding:2px 6px;border-radius:3px;background:#e7efeb}.unused{background:#fff0d9}.image-button{display:block;width:100%;padding:0;border:0;background:#f0eeea;position:relative;border-radius:3px}.image-button img{display:block;width:100%;height:auto;max-height:490px;object-fit:contain}.image-button>span{display:block;font-size:11px;padding:4px 9px;background:#e6ebe7;text-align:right}.filename{font:12px/1.5 ui-monospace,monospace;overflow-wrap:anywhere;margin:12px 0 3px}.card>.small{margin:0 0 12px}.metadata>summary,.prompt>summary{font-size:12px;cursor:pointer;padding:7px 0}.field{border-top:1px solid #edf0ed;padding-top:8px;margin-top:8px}dt{font-size:11px;color:#657572}dd{margin:3px 0 0}pre{font-family:inherit;font-size:12px;line-height:1.65;white-space:pre-wrap;overflow-wrap:anywhere;margin:0;color:#344b4f}.prompt{border-top:1px solid #edf0ed;margin-top:10px}.empty{padding:30px 0;color:#667976}dialog{max-width:min(96vw,1300px);max-height:96vh;padding:20px;border:1px solid #c7d2cb;border-radius:6px;background:#f8f7f2}dialog::backdrop{background:#102024c9}.dialog-head{display:flex;gap:15px;justify-content:space-between;align-items:start;margin-bottom:12px}.dialog-head h2{font-size:17px}.dialog-head button{font-size:22px;background:none;border:1px solid #b9c4bf;line-height:1;padding:4px 8px}dialog img{display:block;width:auto;height:auto;max-width:100%;margin:auto}button:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid #427a84;outline-offset:3px}footer{font-size:11px;color:#6d7b79;border-top:1px solid #ccd7d0;margin-top:30px;padding-top:12px}@media(max-width:1050px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:650px){main{padding:22px 14px}.grid{grid-template-columns:1fr}.toolbar{gap:10px}.toolbar label:first-child{flex-basis:100%}h1{font-size:26px}.image-button img{max-height:none}.badge{font-size:9px}dialog{padding:10px}}@media print{.toolbar,dialog,.image-button>span{display:none}.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.card{break-inside:avoid}}'''
    script = ''''use strict';
const cards=[...document.querySelectorAll('.card')],search=document.getElementById('search'),status=document.getElementById('status'),audience=document.getElementById('audience'),count=document.getElementById('count');
function filter(){const q=search.value.trim().toLowerCase();let n=0;for(const card of cards){const show=(!q||card.dataset.search.includes(q))&&(status.value==='all'||status.value===card.dataset.status)&&(audience.value==='all'||audience.value===card.dataset.audience);card.hidden=!show;if(show)n++;}count.textContent=`显示 ${n} / ${cards.length} 张源图`;document.getElementById('empty').hidden=n!==0;}
search.addEventListener('input',filter);status.addEventListener('change',filter);audience.addEventListener('change',filter);document.getElementById('reset').addEventListener('click',()=>{search.value='';status.value='all';audience.value='all';filter();});
const dialog=document.getElementById('zoom'),zoomImage=document.getElementById('zoom-image');
for(const card of cards){card.querySelector('.image-button').addEventListener('click',()=>{const img=card.querySelector('img');document.getElementById('zoom-title').textContent=card.querySelector('h2').textContent+' · '+card.querySelector('.filename').textContent;zoomImage.src=img.src;zoomImage.alt=img.alt;dialog.showModal();dialog.scrollTop=0;});}
document.getElementById('close').addEventListener('click',()=>dialog.close());dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});filter();'''
    page = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>衣着有名 · 所有图片审查索引</title><style>' + css + '</style></head><body><main>' + header + controls + '<section class="grid" aria-label="所有源图片">' + '\n'.join(cards) + '</section><p id="empty" class="empty" hidden>没有匹配图片，清空筛选后重试。</p><footer>独立审查文件 · 由 scripts/build_image_index.py 从当前工程生成 · 源图总计 ' + f'{total_bytes:,}' + ' bytes · 不加入 book.json、合并书稿或 web/dist。</footer></main><dialog id="zoom" aria-labelledby="zoom-title"><div class="dialog-head"><h2 id="zoom-title"></h2><button id="close" type="button" aria-label="关闭放大图">×</button></div><img id="zoom-image" alt=""></dialog><script>' + script + '</script></body></html>\n'
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(page, encoding='utf-8')
    print(json.dumps({'output': str(OUTPUT), 'source_images': len(sources), 'in_book': referenced, 'derivatives': derivative_count, 'bytes': OUTPUT.stat().st_size}, ensure_ascii=False))


if __name__ == '__main__':
    main()
