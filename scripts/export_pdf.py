#!/usr/bin/env python3
"""Typeset the illustrated atlas from chapter sources, with page-local citations."""
from pathlib import Path
import re, html, json, hashlib, os
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether, Flowable, CondPageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf/fashion-atlas-expanded.pdf'
TMP=ROOT.parent/'tmp/pdfs'
TMP.mkdir(parents=True,exist_ok=True)
font_override=os.environ.get('FASHION_ATLAS_FONT')
font_candidates=([Path(font_override).expanduser()] if font_override else [])+[
 ROOT/'fonts/NotoSansSC-Regular.ttf',
 Path.home()/'.local/share/fonts/NotoSansSC-Regular.ttf',
 Path.home()/'Library/Fonts/NotoSansSC-Regular.ttf',
 Path('/usr/share/fonts/truetype/noto/NotoSansSC-Regular.ttf'),
]
FONT=next((p for p in font_candidates if p.is_file()),None)
if FONT is None:
 raise SystemExit('Chinese font missing: set FASHION_ATLAS_FONT to NotoSansSC-Regular.ttf')
pdfmetrics.registerFont(TTFont('CN',str(FONT)))
pdfmetrics.registerFontFamily('CN',normal='CN',bold='CN',italic='CN',boldItalic='CN')
W,H=595.276,841.89
M=52
BW=W-2*M
TEAL=colors.HexColor('#365e64')
INK=colors.HexColor('#263339')
MUTED=colors.HexColor('#65757a')
S={
 'body':ParagraphStyle('body',fontName='CN',fontSize=10.4,leading=17.3,textColor=INK,spaceAfter=7,wordWrap='CJK',splitLongWords=True,allowWidows=0,allowOrphans=0),
 'h1':ParagraphStyle('h1',fontName='CN',fontSize=21,leading=31,textColor=TEAL,spaceAfter=18,wordWrap='CJK',keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='CN',fontSize=13.2,leading=21,textColor=TEAL,spaceBefore=12,spaceAfter=8,wordWrap='CJK',keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='CN',fontSize=11.3,leading=18.5,textColor=TEAL,spaceBefore=9,spaceAfter=6,wordWrap='CJK',keepWithNext=True),
 'caption':ParagraphStyle('caption',fontName='CN',fontSize=8.2,leading=13,textColor=MUTED,spaceAfter=11,wordWrap='CJK'),
 'cell':ParagraphStyle('cell',fontName='CN',fontSize=8.1,leading=12.7,textColor=INK,wordWrap='CJK',spaceAfter=0),
 'quote':ParagraphStyle('quote',fontName='CN',fontSize=10.1,leading=17,textColor=TEAL,leftIndent=13,borderPadding=8,backColor=colors.HexColor('#f0f5f4'),spaceBefore=5,spaceAfter=10,wordWrap='CJK'),
 'small':ParagraphStyle('small',fontName='CN',fontSize=8.3,leading=13.2,textColor=MUTED,wordWrap='CJK'),
}
BOOK=json.loads((ROOT/'book.json').read_text())
CHAPTERS=[ROOT/c['source'] for c in BOOK['chapters']]
IMAGE_COUNT=len(list((ROOT/'assets/images').glob('*.png')))
FILES=CHAPTERS+sorted((ROOT/'appendices').glob('*.md'))+[ROOT/'references/sources.md']
KEYS={p.name:'section-'+p.stem for p in FILES}
REFS={}
for p in FILES:
 for label,url in re.findall(r'(?<!!)\[([^\]]+)\]\((https?://[^\s)]+)\)',p.read_text()):
  if url not in REFS:REFS[url]={'id':len(REFS)+1,'label':label,'url':url}

def inline(text):
    refs=[]
    tokens={}
    def link(m):
        label,url=m.groups(); key=f'ZZLINK{len(tokens)}ZZ'
        if url.startswith('http'):
            r=REFS[url];refs.append(r['id'])
            out=f'<link href="{html.escape(url,quote=True)}" color="#365e64">{html.escape(label)}</link><super size="6.7">[{r["id"]}]</super>'
        else:
            name=Path(url.split('#')[0]).name
            target=KEYS.get(name)
            out=f'<link href="#{target}" color="#365e64">{html.escape(label)}</link>' if target else html.escape(label)
        tokens[key]=out;return key
    text=re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)',link,text)
    text=html.escape(text)
    text=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',text)
    text=re.sub(r'`([^`]+)`',r'<font color="#365e64">\1</font>',text)
    text=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',text)
    for key,value in tokens.items():text=text.replace(key,value)
    return text,list(dict.fromkeys(refs))

class CiteP(Paragraph):
 def __init__(self,text,style,refs=None,**kw):
  super().__init__(text,style,**kw);self.source_ids=refs or []
 def split(self,aW,aH):
  parts=super().split(aW,aH)
  for p in parts:p.source_ids=self.source_ids
  return parts

def para(text,style='body',track=True):
 x,r=inline(text)
 return CiteP(x,S[style],r if track else [])

def img(path):
 source=PILImage.open(path).convert('RGB')
 source.thumbnail((1280,1280),PILImage.Resampling.LANCZOS)
 maxw=491;maxh=420  # Leave room for chapter heading, introduction and the attached caption.
 fac=min(maxw/source.width,maxh/source.height)
 target=TMP/(hashlib.sha256(str(path).encode()).hexdigest()[:12]+'.jpg')
 source.save(target,quality=int(os.environ.get('FASHION_ATLAS_JPEG_QUALITY','75')),subsampling=2,optimize=True)
 return Image(str(target),width=source.width*fac,height=source.height*fac,hAlign='CENTER')

class Cover(Flowable):
 def __init__(self):super().__init__();self.width=BW;self.height=640
 def draw(self):
  c=self.canv
  c.setFillColor(TEAL);c.rect(0,608,42,5,fill=1,stroke=0)
  c.setFont('CN',35);c.drawString(0,552,'衣着有名')
  c.setFont('CN',18);c.drawString(0,517,'服饰风格、单品与穿着知识')
  c.setFillColor(MUTED);c.setFont('CN',10.5)
  c.drawString(0,483,'认识风格 · 理解结构 · 了解现实穿着')
  c.setFont('CN',10);c.drawString(0,448,f'{len(CHAPTERS)-1} 章正文 / {IMAGE_COUNT} 张教学配图')
  dw=173
  for x,name in [(BW-2*dw-12,'13-dresses.png'),(BW-dw,'63-mens-classic-styles.png')]:
   picture=img(ROOT/'assets/images'/name)
   dh=dw*picture.imageHeight/picture.imageWidth
   c.drawImage(picture.filename,x,55,width=dw,height=dh,mask='auto')
  c.setFillColor(TEAL);c.setFont('CN',13)
  for i,line in enumerate(['风格与衣橱','女装与男装','衣型与比例','面料与装饰','综合辨识与穿着']):c.drawString(0,338-i*29,line)
  c.setFillColor(MUTED);c.setFont('CN',9);c.drawString(0,28,'中文图解兴趣读本')
  c.drawString(0,9,'服饰知识修订版 · 2026 年 10 月')

class Doc(BaseDocTemplate):
 def __init__(self,*a,**k):
  super().__init__(*a,**k);self.heading='';self.page_sources=set();self.citation_pages={}
 def beforePage(self):self.page_sources=set()
 def afterFlowable(self,f):
  if hasattr(f,'source_ids'):self.page_sources.update(f.source_ids)
  if hasattr(f,'toc_key'):
   self.heading=f.getPlainText()
   self.canv.bookmarkPage(f.toc_key)
   self.canv.addOutlineEntry(self.heading,f.toc_key,level=0,closed=False)
   self.notify('TOCEntry',(0,self.heading,self.page,f.toc_key))

def footer(c,d):
 if d.page==1:return
 c.saveState();c.setStrokeColor(colors.HexColor('#dce4e2'));c.line(M,103,W-M,103)
 c.setFillColor(MUTED);c.setFont('CN',7)
 head=d.heading
 if len(head)>43:head=head[:43]+'…'
 c.drawString(M,H-34,head)
 c.setFont('CN',8);c.drawRightString(W-M,24,str(d.page))
 c.drawString(M,24,'衣着有名 / 扩充版')
 sources=sorted(d.page_sources)
 d.citation_pages[d.page]=sources
 if len(sources)>7:raise ValueError(f'Too many sources on page {d.page}: {len(sources)}')
 rev={r['id']:r for r in REFS.values()}
 y=88
 for num in sources:
  r=rev[num];label=re.sub(r'^(资料与真实.*?：|真实.*?：|资料：|原始资料：|术语旁读：|旁读：)','',r['label'])
  text=f'[{num}] {label}'
  while pdfmetrics.stringWidth(text,'CN',6.6)>BW-6:text=text[:-2]+'…'
  c.setFillColor(TEAL);c.setFont('CN',6.6);c.drawString(M,y,text)
  c.linkURL(r['url'],(M,y-1,W-M,y+8),relative=0,thickness=0)
  y-=9.4
 c.restoreState()

def parse(p):
 lines=p.read_text().splitlines();story=[];i=0;track=p.parent.name not in ('appendices','references')
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line.startswith('# '):
   title=line[2:];h=para(title,'h1',track=False);h.toc_key=KEYS[p.name];story.extend([h]);i+=1;continue
  if line.startswith('### '):story.append(para(line[4:],'h3',track));i+=1;continue
  if line.startswith('## '):
   heading=para(line[3:],'h2',track)
   j=i+1
   while j<len(lines) and not lines[j].strip():j+=1
   if j<len(lines) and lines[j].strip().startswith('|'):
    heading.keepWithNext=0
    story.append(CondPageBreak(100))
   story.append(heading);i+=1;continue
  m=re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)',line)
  if m:
   image=img((p.parent/m.group(2)).resolve());i+=1
   while i<len(lines) and not lines[i].strip():i+=1
   cap=None
   if i<len(lines) and lines[i].strip().startswith('*') and not lines[i].strip().startswith('**'):
    cap=para(lines[i].strip().strip('*'),'caption',track);i+=1
   group=[Spacer(1,5),image,Spacer(1,7)]
   if story and getattr(getattr(story[-1],'style',None),'name','')=='h2':group.insert(0,story.pop())
   if cap:group.append(cap)
   story.append(KeepTogether(group));continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    row=[t.strip() for t in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r':?-+:?',x) for x in row):rows.append(row)
    i+=1
   n=max(map(len,rows));ratios=([.12,.24,.20,.27,.17] if n==5 else [.19,.41,.40] if n==3 else [.25]*4 if n==4 else [1/n]*n)
   if len(ratios)!=n:ratios=[1/n]*n
   values=[[para(c,'cell',track=False) for c in row]+[para('','cell')]*(n-len(row)) for row in rows]
   t=Table(values,colWidths=[BW*r for r in ratios],repeatRows=1,hAlign='LEFT',splitByRow=1)
   t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6efed')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f7f6')]),('LINEBELOW',(0,0),(-1,0),.6,TEAL),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
   t.spaceAfter=10
   story.append(t);continue
  if line.startswith('```'):
   block=[];i+=1
   while i<len(lines) and not lines[i].strip().startswith('```'):block.append(lines[i]);i+=1
   story.append(para('<br/>'.join(block),'small',track));i+=1;continue
  style='quote' if line.startswith('>') else 'body'
  if style=='quote':line=line.lstrip('> ')
  if line.startswith('- '):line='• '+line[2:]
  block=[line];i+=1
  while i<len(lines) and lines[i].strip() and not re.match(r'^(#|!\[|\||>|```|- |\d+\. )',lines[i].strip()):
   block.append(lines[i].strip());i+=1
  story.append(para(' '.join(block),style,track))
 return story

def main():
 OUT.parent.mkdir(parents=True,exist_ok=True)
 d=Doc(str(OUT),pagesize=(W,H),leftMargin=M,rightMargin=M,topMargin=58,bottomMargin=112,title=BOOK['title'],author='衣着有名',pageCompression=1)
 d.addPageTemplates(PageTemplate('main',[Frame(M,112,BW,H-170,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPageEnd=footer))
 toc=TableOfContents();toc.levelStyles=[ParagraphStyle('toc',fontName='CN',fontSize=9.3,leading=16.5,textColor=INK,spaceBefore=5,wordWrap='CJK',rightIndent=25)]
 story=[Cover(),PageBreak(),para('目录','h1'),para('点选目录或 PDF 书签即可跳转。第 13 章起为单品细节；来源编号在对应页下方可点击。','small'),Spacer(1,14),toc]
 for p in FILES:story.extend([PageBreak(),*parse(p)])
 d.multiBuild(story,maxPasses=4)
 (TMP/'pdf-citations.json').write_text(json.dumps(d.citation_pages,indent=2))
 (ROOT/'output/pdf/metadata.json').write_text(json.dumps({'pages':d.page,'chapters':len(CHAPTERS)-1,'images':IMAGE_COUNT},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'output':str(OUT),'pages':d.page,'sources':len(REFS),'images':IMAGE_COUNT},ensure_ascii=False))

if __name__=='__main__':main()
