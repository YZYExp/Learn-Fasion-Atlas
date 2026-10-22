"""Extract homepage panels without stretching the original teaching plates."""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent/'dist/assets'
PANELS={'24-lace-variants':0,'23-slip-variants':1,'35-mamian-modern':0,'31-lolita-variants':1,'25-sport-variants':0,'28-knit-variants':1,'27-blouse-variants':2,'30-jacket-variants':0,'33-song-beizi':0,'32-urban-tailoring':1,'36-cosplay-types':2,'37-xianxia-fantasy':0}
for name,col in PANELS.items():
 im=Image.open(ROOT/(name+'.webp')); w,h=im.size
 # Leave a small inset before panel rules; keep each source panel's ratio.
 rows=1 if name=='33-song-beizi' else 2
 box=(round(w*col/3)+3,0,round(w*(col+1)/3)-3,h//rows-18)
 im.crop(box).save(ROOT/(name+'-thumb.webp'),quality=92)
print('Extracted',len(PANELS),'undistorted panels')

# The male style plate has two columns, unlike the earlier six-panel sheets.
im=Image.open(ROOT/'63-mens-classic-styles.webp');w,h=im.size
im.crop((3,0,w//2-3,h//2-18)).save(ROOT/'63-mens-classic-styles-thumb.webp',quality=92)
