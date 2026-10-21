import rasterio,numpy as np
from PIL import Image,ImageFilter
def shade(z,res,lat0,lat1,zf=2.5):
  h,w=z.shape
  lat=np.linspace(lat1,lat0,h)[:,None]
  dx=res*111320*np.cos(np.radians(lat));dy=res*110574
  dzdx=np.gradient(z,axis=1)/dx*zf
  dzdy=-np.gradient(z,axis=0)/dy*zf
  nz=1/np.sqrt(dzdx**2+dzdy**2+1)
  out=np.zeros_like(z)
  for az,wgt in [(315,.55),(270,.15),(0,.2),(225,.1)]:
    a=np.radians(az);al=np.radians(40)
    L=(np.sin(a)*np.cos(al),np.cos(a)*np.cos(al),np.sin(al))
    out+=wgt*np.clip((-dzdx*L[0]-dzdy*L[1]+L[2])*nz,0,1)
  flat=np.sin(np.radians(40))
  return np.clip(out/flat*0.75,0,1.3)
BANDS=[200,400,700,1000,1500,2000,2500,3000]
BCOL=[(0xc6,0xe9,0xb7),(0xe2,0xf3,0xc6),(0xff,0xfc,0xc6),(0xfc,0xd8,0xbb),(0xfa,0xc5,0xa6),(0xd7,0xbe,0xa8),(0xd8,0xd0,0xec),(0xd9,0xf3,0xfc),(0xff,0xff,0xff)]
def tint(z):
  idx=np.digitize(z,BANDS);pal=np.array(BCOL,float);return pal[idx]
def build(src,box,size,tag):
  with rasterio.open(src) as r:
    z=r.read(1).astype(float);res=r.res[0];b=r.bounds
  sea=z<-1000;z[sea]=0
  hs=shade(z,res,b.bottom,b.top)
  hs[sea]=hs[~sea].mean() if (~sea).any() else .7
  # colour: tint * (0.55+0.6*hs) soft
  rgb=tint(z)*(0.50+0.55*hs)[...,None];rgb=np.clip(rgb,0,255).astype(np.uint8)
  gray=(186+67*np.clip((hs-0.3)/0.8,0,1)**0.9).astype(np.uint8)
  # crop exact box (lon0,lat0,lon1,lat1)
  def crop(img):
    im=Image.fromarray(img)
    x0=(box[0]-b.left)/res;x1=(box[2]-b.left)/res;y0=(b.top-box[3])/res;y1=(b.top-box[1])/res
    im=im.crop((round(x0),round(y0),round(x1),round(y1)))
    return im.resize(size,Image.LANCZOS)
  c=crop(rgb).filter(ImageFilter.UnsharpMask(1.0,40,2));c.save(f'dem_{tag}_c.jpg',quality=84,optimize=True,progressive=True)
  g=crop(gray).filter(ImageFilter.UnsharpMask(1.4,110,1));g.save(f'dem_{tag}_g.jpg',quality=84,optimize=True,progressive=True)
  print(tag,c.size)
build('/mnt/user-data/uploads/main.tif',(-10.9,33.4,5.6,44.6),(2750,1867),'main')
build('/mnt/user-data/uploads/can.tif',(-18.4,27.5,-13.2,29.5),(1100,423),'can')
