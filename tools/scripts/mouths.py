import pickle,math,json,heapq,rasterio,numpy as np
from shapely.geometry import Point,LineString,MultiLineString
from shapely.ops import unary_union
P=pickle.load(open('osm_pick2.pkl','rb'))
src=rasterio.open('/mnt/user-data/uploads/main.tif');Z=src.read(1).astype(float);T=src.transform
from rasterio.features import rasterize
from shapely.geometry import shape
es=pickle.load(open('es_hr.pkl','rb'))
oth=[shape(f['geometry']) for f in json.load(open('c10.geojson'))['features'] if f['properties']['ADM0_A3'] in ('PRT','FRA','MAR')]
landm=rasterize([(es,1)]+[(g,1) for g in oth],out_shape=Z.shape,transform=T,fill=0,dtype='uint8')
sea=(landm==0)|(Z<-1000)
def rc(lon,lat):c,r=~T*(lon,lat);return int(r),int(c)
def ll(r,c):x,y=T*(c+.5,r+.5);return x,y
ext={}
for n,end in [('Eo',(-7.057,43.472)),('Besaya',(-4.061,43.356)),('Nervión',(-2.877,43.240)),('Tinto',(-6.940,37.207)),('Ebro',(0.864,40.721))]:
  r0,c0=rc(*end);W=120
  dist={(r0,c0):0};prev={};pq=[(0,r0,c0)];goal=None
  while pq:
    d,r,c=heapq.heappop(pq)
    if d>dist.get((r,c),1e18):continue
    if sea[r,c]:goal=(r,c);break
    for dr in(-1,0,1):
      for dc in(-1,0,1):
        if not dr and not dc:continue
        rr,cc=r+dr,c+dc
        if abs(rr-r0)>W or abs(cc-c0)>W:continue
        z=0 if sea[rr,cc] else max(Z[rr,cc],0)
        nd=d+math.hypot(dr,dc)*(1+z/4)
        if nd<dist.get((rr,cc),1e18):dist[(rr,cc)]=nd;prev[(rr,cc)]=(r,c);heapq.heappush(pq,(nd,rr,cc))
  path=[goal];
  while path[-1]!=(r0,c0):path.append(prev[path[-1]])
  pts=[end]+[ll(r,c) for r,c in reversed(path)][1:]
  # smooth
  for _ in range(3):pts=[pts[0]]+[((pts[i-1][0]+2*pts[i][0]+pts[i+1][0])/4,(pts[i-1][1]+2*pts[i][1]+pts[i+1][1])/4) for i in range(1,len(pts)-1)]+[pts[-1]]
  L=LineString(pts);km=L.length*111*.75
  print(n,'extension',round(km,1),'km, max elev along path',int(max(max(Z[r,c],0) for r,c in path)),'m')
  ext[n]=L
pickle.dump(ext,open('mouth_ext.pkl','wb'))
