from pathlib import Path
import json,re,html,shutil,os,io,hashlib
from PIL import Image
SOURCE=Path(os.environ.get('FASHION_ATLAS_SOURCE',str(Path(__file__).resolve().parent.parent)))
DIST=Path(__file__).parent/'dist';(DIST/'assets').mkdir(exist_ok=True)
cache_path=Path(__file__).parent/'image-cache.json'
cache=json.loads(cache_path.read_text()) if cache_path.exists() else {}
new_cache={}
for p in (SOURCE/'assets/images').glob('*.png'):
 target=DIST/'assets'/(p.stem+'.webp');digest=hashlib.sha256(p.read_bytes()).hexdigest();new_cache[p.name]=digest
 if cache.get(p.name)==digest and target.is_file() and target.stat().st_size>0:continue
 im=Image.open(p).convert('RGB');buffer=io.BytesIO();im.save(buffer,'WEBP',quality=88,method=6)
 data=buffer.getvalue();Image.open(io.BytesIO(data)).verify();target.write_bytes(data)
cache_path.write_text(json.dumps(new_cache,indent=2)+'\n')
shutil.copy2(SOURCE/'output/pdf/fashion-atlas-expanded.pdf',DIST/'fashion-atlas.pdf')
shutil.copy2(SOURCE/'output/pdf/menswear-atlas.pdf',DIST/'menswear-atlas.pdf')
book=json.loads((SOURCE/'book.json').read_text());chapters=[SOURCE/c['source'] for c in book['chapters']];appendices=[SOURCE/p for p in book['appendices']]
files=chapters+appendices+[SOURCE/'references/sources.md'];ids={p.name:p.stem for p in files}
def urlfix(u):
 if u.startswith(('http://','https://','#')):return u
 if 'assets/images/' in u:return 'assets/'+Path(u).stem+'.webp'
 n=Path(u.split('#')[0]).name
 if n in ids:return 'read.html?chapter='+ids[n]
 return u

def inline(s):
 stash=[]
 def link(m):
  label,u=m.groups();u=urlfix(u);external=u.startswith('http');v='<a href="'+html.escape(u,quote=True)+'"'+(' target="_blank" rel="noopener noreferrer"' if external else '')+'>'+html.escape(label)+'</a>';stash.append(v);return f'ZZT{len(stash)-1}ZZ'
 s=re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)',link,s);s=html.escape(s)
 s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s);s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s);s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<em>\1</em>',s)
 for i,v in enumerate(stash):s=s.replace(f'ZZT{i}ZZ',v)
 return s

def render(text):
 lines=text.splitlines();o=[];i=0
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line=='---':o.append('<hr>');i+=1;continue
  if line.startswith('```'):
   b=[];i+=1
   while i<len(lines) and not lines[i].startswith('```'):b.append(lines[i]);i+=1
   o.append('<pre><code>'+html.escape('\n'.join(b))+'</code></pre>');i+=1;continue
  m=re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)',line)
  if m:o.append('<figure><img loading="lazy" src="'+urlfix(m[2])+'" alt="'+html.escape(m[1],quote=True)+'"></figure>');i+=1;continue
  if line.startswith('#'):
   m=re.match(r'(#+)\s+(.*)',line);n=min(len(m[1]),4);o.append(f'<h{n}>'+inline(m[2])+f'</h{n}>');i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r':?-+:?',c) for c in cells):rows.append(cells)
    i+=1
   o.append('<div class="table-scroll"><table><thead><tr>'+''.join('<th>'+inline(c)+'</th>' for c in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>');continue
  if line.startswith('>'):
   b=[]
   while i<len(lines) and lines[i].strip().startswith('>'):b.append(lines[i].strip()[1:].strip());i+=1
   o.append('<blockquote>'+inline(' '.join(b))+'</blockquote>');continue
  if line.startswith('- '):
   b=[]
   while i<len(lines) and lines[i].strip().startswith('- '):b.append(lines[i].strip()[2:]);i+=1
   o.append('<ul>'+''.join('<li>'+inline(c)+'</li>' for c in b)+'</ul>');continue
  if re.match(r'\d+\. ',line):
   b=[]
   while i<len(lines) and re.match(r'\d+\. ',lines[i].strip()):b.append(re.sub(r'^\d+\. ','',lines[i].strip()));i+=1
   o.append('<ol>'+''.join('<li>'+inline(c)+'</li>' for c in b)+'</ol>');continue
  b=[line];i+=1
  while i<len(lines) and lines[i].strip() and not re.match(r'^(#|!\[|\||>|```|- |\d+\. )',lines[i].strip()):b.append(lines[i].strip());i+=1
  css=' class="figure-caption"' if line.startswith('*') and not line.startswith('**') else ''
  o.append('<p'+css+'>'+inline(' '.join(b))+'</p>')
 return '\n'.join(o)
out=[]
for p in files:
 text=p.read_text();title=text.splitlines()[0].lstrip('# ');out.append({'id':p.stem,'title':title,'number':int(p.stem[:2]) if p in chapters else None,'kind':'chapter' if p in chapters else 'appendix','html':render(text)})
(DIST/'content.json').write_text(json.dumps(out,ensure_ascii=False))
print({'chapters':len(chapters),'appendices':len(appendices),'images':len(list((SOURCE/'assets/images').glob('*.png')))})

# Update displayed counts from the completed PDF instead of hard-coded values.
meta=json.loads((SOURCE/'output/pdf/metadata.json').read_text())
p=DIST/'index.html';s=p.read_text()
s=re.sub(r'探索\d+章正文、\d+张配图',f"探索{meta['chapters']}章正文、{meta['images']}张配图",s)
s=re.sub(r'<b>\d+</b>章正文',f"<b>{meta['chapters']}</b>章正文",s)
s=re.sub(r'<b>\d+</b>张配图',f"<b>{meta['images']}</b>张配图",s)
s=re.sub(r'<b>\d+</b>页读本',f"<b>{meta['pages']}</b>页读本",s)
s=re.sub(r'完整图解读本 · \d+ 页',f"完整图解读本 · {meta['pages']} 页",s)
s=re.sub(r'PDF 约 [\d.]+ MB',f"PDF 约 {(DIST/'fashion-atlas.pdf').stat().st_size/1000000:.1f} MB",s)
p.write_text(s)

shutil.copy2(Path(__file__).parent/'atlas.json',DIST/'atlas.json')
groups=[{'n':g['id'],'title':g['title'],'ids':[c['id'] for c in book['chapters'] if c['group']==g['id']]} for g in book['sections']]
groups.append({'n':['I','II','III','IV','V','VI','VII','VIII','IX','X'][len(book['sections'])],'title':'查词、辨析与描述路线','ids':[c['id'] for c in out if c['kind']=='appendix']})
(DIST/'book-meta.json').write_text(json.dumps({'title':book['title'],'groups':groups,'stats':meta},ensure_ascii=False,indent=2)+'\n')

# Content fingerprints keep browsers from mixing old scripts/data with a new edition.
def versioned(name):
 return name+'?v='+hashlib.sha256((DIST/name).read_bytes()).hexdigest()[:12]
for name in ['app.js','reader.js']:
 p=DIST/name;s=p.read_text()
 for data in ['content.json','atlas.json','book-meta.json']:
  s=re.sub(r"fetch\('"+re.escape(data)+r"(?:\?v=[a-f0-9]+)?'\)",lambda m: "fetch('"+versioned(data)+"')",s)
 p.write_text(s)
for p in DIST.glob('*.html'):
 s=p.read_text()
 for name in ['app.js','reader.js','style.css','fashion-atlas.pdf','menswear-atlas.pdf']:
  s=re.sub(r'((?:src|href)=")'+re.escape(name)+r'(?:\?v=[a-f0-9]+)?"',lambda m: m[1]+versioned(name)+'"',s)
 p.write_text(s)
