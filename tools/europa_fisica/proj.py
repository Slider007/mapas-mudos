# Proyección del mapa físico de Europa: acimutal equivalente de Lambert centrada en 20°E 56°N.
import math
LON0, LAT0 = 20.0, 56.0
def laea(lon, lat):
    l, p, l0, p0 = map(math.radians, (lon, lat, LON0, LAT0))
    k = math.sqrt(2 / (1 + math.sin(p0) * math.sin(p) + math.cos(p0) * math.cos(p) * math.cos(l - l0)))
    return k * math.cos(p) * math.sin(l - l0), k * (math.cos(p0) * math.sin(p) - math.sin(p0) * math.cos(p) * math.cos(l - l0))
def inv(x, y):
    p0, l0 = math.radians(LAT0), math.radians(LON0); r = math.hypot(x, y)
    if r < 1e-12: return LON0, LAT0
    c = 2 * math.asin(min(1, r / 2))
    lat = math.asin(math.cos(c) * math.sin(p0) + y * math.sin(c) * math.cos(p0) / r)
    lon = l0 + math.atan2(x * math.sin(c), r * math.cos(p0) * math.cos(c) - y * math.sin(p0) * math.sin(c))
    return math.degrees(lon), math.degrees(lat)
# encuadre: de Islandia a los Urales y Nueva Zembla, del norte de África a Svalbard
_F = [(-25.5, 63.0), (-24.5, 66.8), (-10.5, 35.6), (36.0, 33.8), (52.5, 37.5), (66.5, 67.5), (69.5, 77.2), (28.5, 80.8), (10.0, 80.0)]
_xs, _ys = zip(*[laea(*p) for p in _F])
X0, X1, Y0, Y1 = min(_xs), max(_xs), min(_ys), max(_ys)
_mx, _my = (X1 - X0) * .015, (Y1 - Y0) * .015; X0 -= _mx; X1 += _mx; Y0 -= _my; Y1 += _my
W = 1000.0; S = W / (X1 - X0); H = round((Y1 - Y0) * S, 1)
def prj(lon, lat):
    x, y = laea(lon, lat); return ((x - X0) * S, (Y1 - y) * S)
def unprj(px, py): return inv(px / S + X0, Y1 - py / S)
