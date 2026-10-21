import numpy as np,json,pickle,math
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
from scipy.ndimage import binary_opening,binary_erosion,distance_transform_edt,zoom
from scipy.optimize import minimize
from pyproj import Transformer
im=np.asarray(Image.open('ign25-1.png').convert('RGB')).astype(int);H,W,_=im.shape
sea=np.load('ign25_sea.npy')

f=lambda a,b:(a/1064*W,b/788*H)
tr=Transformer.from_crs('EPSG:4326','+proj=lcc +lat_1=37.17806 +lat_2=42.82194 +lat_0=40 +lon_0=-3 +ellps=GRS80',always_xy=True)
es=pickle.load(open('es_hr.pkl','rb'))
def apply(p,x,y):
  s,th,tx,ty=p;return tx+s*(math.cos(th)*x-math.sin(th)*y),ty-s*(math.sin(th)*x+math.cos(th)*y)
from shapely.geometry import shape as _sh,Point as _P
from shapely.ops import unary_union as _uu
from shapely.prepared import prep
_nb=prep(_uu([_sh(f['geometry']) for f in json.load(open('c10.geojson'))['features'] if f['properties']['ADM0_A3'] in ('PRT','FRA','AND','GIB')]).buffer(0.03))
def pts(canary):
  xs=[];ys=[]
  for g in es.geoms:
    if g.area<0.01 or (g.centroid.x<-12.5)!=canary:continue
    c=np.array(g.exterior.coords)[::3];c=np.array([q for q in c if not _nb.contains(_P(q))]);
    if len(c):xs+=list(c[:,0]);ys+=list(c[:,1])
  return tr.transform(np.array(xs),np.array(ys))
edge=sea&~binary_erosion(sea,iterations=1)
dt=distance_transform_edt(~edge)
def fit(p0,canary,region,trans=500,step=25):
  X,Y=pts(canary)
  def f_(p):
    px,py=apply(p,X,Y);ok=(px>=0)&(px<W-1)&(py>=0)&(py<H-1)&region(px,py)
    if ok.mean()<0.4:return 1e6
    d=np.minimum(dt[py[ok].astype(int),px[ok].astype(int)],150);return d.mean()+(1-ok.mean())*200
  best=None
  for sf in np.linspace(0.94,1.06,7):
    for dx in range(-trans,trans+1,step):
      for dy in range(-trans,trans+1,step):
        p=[p0[0]*sf,p0[1],p0[2]+dx,p0[3]+dy];v=f_(p)
        if best is None or v<best[0]:best=(v,p)
  print('grid',best[0])
  p1=best[1]
  g=lambda q:f_([p1[0]*(1+q[0]*0.01),p1[1]+q[1]*0.01,p1[2]+q[2]*10,p1[3]+q[3]*10])
  r=minimize(g,np.zeros(4),method='Powell',options={'maxiter':4000,'xtol':1e-3,'ftol':1e-4})
  q=r.x;p=[p1[0]*(1+q[0]*0.01),p1[1]+q[1]*0.01,p1[2]+q[2]*10,p1[3]+q[3]*10];print('fit',r.fun,p);return p
Pm=json.load(open('georef.json'))
k=W/5079
# initial: scale mudo params by width ratio and per-degree ratio
s0=Pm['main'][0]*265/244*(W/5321)
x0,y0=f(45,62);x1,y1=f(1018,718)
def main_region(px,py):
  lx0,ly0=f(48,262);lx1,ly1=f(210,472);cx1,cy0=f(365,572)
  return (px>x0)&(px<x1)&(py>y0)&(py<y1)&~((px>lx0)&(px<lx1)&(py>ly0)&(py<ly1))&~((px<cx1)&(py>cy0))
# initial translation: map Lambert origin (-3,40) to approx image location of Madrid area: preview (~560,330)
mx,my=f(560,338)
p0=[s0,Pm['main'][1],mx,my]
pm=fit(p0,False,main_region,trans=400,step=20)
def can_region(px,py):
  a0,b0=f(48,580);a1,b1=f(362,714);return (px>a0)&(px<a1)&(py>b0)&(py<b1)
# canaries init: Tenerife centre (-16.6,28.27) at preview (~150,640)
X0,Y0=tr.transform(-16.6,28.27);sc=Pm['can'][0]*265/244*(W/5321)
th=Pm['can'][1];tx=f(150,640)[0]-sc*(math.cos(th)*X0-math.sin(th)*Y0);ty=f(150,640)[1]+sc*(math.sin(th)*X0+math.cos(th)*Y0)
pc=fit([sc,th,tx,ty],True,can_region,trans=300,step=15)
json.dump({'main':pm,'can':pc},open('georef25.json','w'))
