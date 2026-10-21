import numpy as np,json,pickle,math,cv2
from scipy.ndimage import distance_transform_edt,binary_dilation
from pyproj import Transformer
im=cv2.imread('ign25-1.png');hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
h=hsv[...,0].astype(int)*2;s=hsv[...,1].astype(int);v=hsv[...,2].astype(int)
sea=np.load('ign25_sea.npy')
blue=(h>=185)&(h<=225)&(s>=60)&(~binary_dilation(sea,iterations=6))
dt=distance_transform_edt(~blue)
tr=Transformer.from_crs('EPSG:4326','+proj=lcc +lat_1=37.17806 +lat_2=42.82194 +lat_0=40 +lon_0=-3 +ellps=GRS80',always_xy=True)
P=json.load(open('georef25.json'))['main']
def apply(p,x,y):
  s_,th,tx,ty=p;return tx+s_*(math.cos(th)*x-math.sin(th)*y),ty-s_*(math.sin(th)*x+math.cos(th)*y)
R=pickle.load(open('osm_pick2.pkl','rb'))
H,W=blue.shape;out=[]
for n,g in R.items():
  if g is None:continue
  ls=list(g.geoms) if hasattr(g,'geoms') else [g]
  pts=np.vstack([np.array(l.coords) for l in ls])
  if len(pts)>4000:pts=pts[::len(pts)//4000]
  X,Y=tr.transform(pts[:,0],pts[:,1]);px,py=apply(P,X,Y)
  ok=(px>0)&(px<W-1)&(py>0)&(py<H-1)
  d=dt[py[ok].astype(int),px[ok].astype(int)]
  km=d/0.003279/1000
  out.append((n,round((km<1.5).mean()*100),round(np.median(km),2)))
out.sort(key=lambda a:a[1])
for r in out:print(f"{r[0]:22s} совпадение {r[1]:3d}%  медиана {r[2]} км")
