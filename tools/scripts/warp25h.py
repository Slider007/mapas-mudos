import numpy as np,json,math,cv2
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
from pyproj import Transformer
tr=Transformer.from_crs('EPSG:4326','+proj=lcc +lat_1=37.17806 +lat_2=42.82194 +lat_0=40 +lon_0=-3 +ellps=GRS80',always_xy=True)
P0=json.load(open('georef25.json'));K=400/250
P={k:[v[0]*K,v[1],v[2]*K,v[3]*K] for k,v in P0.items()}
src=cv2.cvtColor(cv2.imread('ign400-1.png'),cv2.COLOR_BGR2RGB);H,W,_=src.shape
def apply(p,x,y):
  s,th,tx,ty=p;return tx+s*(math.cos(th)*x-math.sin(th)*y),ty-s*(math.sin(th)*x+math.cos(th)*y)
def warp(p,box,size,okfn,fallback,out):
  w,h=size;lon=np.linspace(box[0],box[2],w);lat=np.linspace(box[3],box[1],h);LO,LA=np.meshgrid(lon,lat)
  X,Y=tr.transform(LO,LA);px,py=apply(p,X,Y)
  img=cv2.remap(src,px.astype(np.float32),py.astype(np.float32),cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT,borderValue=(255,255,255))
  ok=okfn(px,py)
  fb=np.asarray(Image.open(fallback).convert('RGB').resize((w,h)))
  img[~ok]=fb[~ok]
  Image.fromarray(img).save(out,quality=84,optimize=True,progressive=True);print(out,ok.mean())
f=lambda a,b:(a/1064*W,b/788*H)
def main_ok(px,py):
  x0,y0=f(46,63);x1,y1=f(1017,717);ix,iy=f(366,571);lx0,ly0=f(46,260);lx1,ly1=f(212,474)
  return (px>x0)&(px<x1)&(py>y0)&(py<y1)&~((px<ix)&(py>iy))&~((px>lx0)&(px<lx1)&(py>ly0)&(py<ly1))
def can_ok(px,py):
  x0,y0=f(47,579);x1,y1=f(363,716);return (px>x0)&(px<x1)&(py>y0)&(py<y1)
warp(P['main'],(-10.9,33.4,5.6,44.6),(4400,2987),main_ok,'dem_main_c.jpg','ign25h_main.jpg')
warp(P['can'],(-18.4,27.5,-13.2,29.5),(1800,692),can_ok,'dem_can_c.jpg','ign25h_can.jpg')
