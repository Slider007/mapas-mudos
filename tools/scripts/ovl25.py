import numpy as np,json,pickle,math,sys
from PIL import Image,ImageDraw
Image.MAX_IMAGE_PIXELS=None
from pyproj import Transformer
tr=Transformer.from_crs('EPSG:4326','+proj=lcc +lat_1=37.17806 +lat_2=42.82194 +lat_0=40 +lon_0=-3 +ellps=GRS80',always_xy=True)
P=json.load(open('georef25.json'))
def apply(p,x,y):
  s,th,tx,ty=p;return tx+s*(math.cos(th)*x-math.sin(th)*y),ty-s*(math.sin(th)*x+math.cos(th)*y)
es=pickle.load(open('es_hr.pkl','rb'))
im=Image.open('ign25-1.png').convert('RGB');d=ImageDraw.Draw(im)
for g in es.geoms:
  xs,ys=g.exterior.coords.xy
  if g.area<0.002:continue
  p=P['can'] if g.centroid.x<-12.5 else P['main']
  X,Y=tr.transform(np.array(xs),np.array(ys));px,py=apply(p,X,Y)
  d.line(list(zip(px,py)),fill=(255,0,0),width=4)
im.save('o25_full.jpg',quality=70)
w,h=im.size
for n,b in {'nw':(.25,.08,.45,.30),'s':(.40,.62,.62,.85),'e':(.70,.15,.92,.45),'can':(.04,.72,.36,.92)}.items():
  im.crop((int(w*b[0]),int(h*b[1]),int(w*b[2]),int(h*b[3]))).save(f'o25_{n}.jpg',quality=80)
