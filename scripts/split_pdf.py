#!/usr/bin/env python3
"""Extract chapter PDFs from the validated full book, preserving page-local sources."""
from pathlib import Path
from pypdf import PdfReader, PdfWriter
ROOT=Path(__file__).resolve().parents[1]
def main():
 source=ROOT/'output/pdf/fashion-atlas-expanded.pdf'
 r=PdfReader(source)
 dest=ROOT/'output/pdf/chapters';dest.mkdir(parents=True,exist_ok=True)
 sections=[(d.title,r.get_destination_page_number(d)) for d in r.outline if not isinstance(d,list)]
 chapters=sorted((ROOT/'chapters').glob('*.md'))
 for idx,p in enumerate(chapters):
  start=sections[idx][1];end=sections[idx+1][1] if idx+1<len(sections) else len(r.pages)
  w=PdfWriter()
  for pg in r.pages[start:end]:w.add_page(pg)
  w.add_metadata({'/Title':sections[idx][0],'/Author':'衣着有名'})
  w.add_outline_item(sections[idx][0],0)
  with (dest/(p.stem+'.pdf')).open('wb') as f:w.write(f)
 print(f'Exported {len(chapters)} chapter PDFs to {dest}')
if __name__=='__main__':main()
