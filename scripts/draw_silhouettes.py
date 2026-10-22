#!/usr/bin/env python3
"""Draw an exact, abstract silhouette comparison; not an AI image or pattern."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
canvas = Image.new('RGB', (1500, 620), '#f7f4ef')
d = ImageDraw.Draw(canvas)
font_path = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
def font(size):
    return ImageFont.truetype(str(font_path), size) if font_path.exists() else ImageFont.load_default()
shapes = [
    ('H', [(150,100),(330,100),(330,470),(150,470)], 'Straight body'),
    ('A', [(675,100),(805,100),(885,470),(595,470)], 'Widening hem'),
    ('X', [(1135,100),(1345,100),(1290,280),(1375,470),(1105,470),(1190,280)], 'Defined waist'),
]
for i, (label, points, subtitle) in enumerate(shapes):
    if i:
        d.line((i*500,45,i*500,575), fill='#d4cec4', width=2)
    d.polygon(points, fill='#44636b', outline='#263f47', width=4)
    cx = 240+i*500
    d.line((cx-170,280,cx+170,280), fill='#c79a61', width=3)
    d.text((cx,495),label,font=font(52),fill='#263f47',anchor='mt')
    d.text((cx,560),subtitle,font=font(23),fill='#55504a',anchor='mt')
canvas.save(root/'assets/images/12-silhouettes.png')
print('assets/images/12-silhouettes.png')
