# Funciones comunes para las fronteras de Cliopatria: suavizado con topología común y paso a anillos para la web.
from shapely.geometry import Polygon
from shapely.ops import unary_union

def chaikin(coords, n=3):
    pts = list(coords)[:-1]
    for _ in range(n):
        q = []
        for i in range(len(pts)):
            (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
            q += [(0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1), (0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1)]
        pts = q
    return pts + [pts[0]]
def smooth(groups, tol=0.07):
    """fronteras suaves y comunes: coverage_simplify (bordes compartidos iguales) + Chaikin; quita los escalones de los datos"""
    from shapely import coverage_simplify
    from shapely.geometry import Polygon, MultiPolygon
    keys = [k for k in groups if not groups[k].is_empty]
    simp = coverage_simplify([groups[k].buffer(0) for k in keys], tol)
    out = dict(groups)
    for k, g in zip(keys, simp):
        ps = [Polygon(chaikin(p.exterior.coords), [chaikin(r.coords) for r in p.interiors]) for p in polys(g) if len(p.exterior.coords) > 3]
        out[k] = unary_union([p.buffer(0) for p in ps if p.area > 0]) if ps else g
    return out
def polys(g): return [p for p in (list(g.geoms) if hasattr(g, 'geoms') else [g]) if p.geom_type == 'Polygon']
def rings(g, tol=0.006, mina=0.004):
    g = g.buffer(0).simplify(tol, preserve_topology=True); out = []
    for p in polys(g):
        if p.area < mina: continue
        r = [[round(x, 2), round(y, 2)] for x, y in p.exterior.coords]
        out.append([r[0]] + [q for i, q in enumerate(r[1:], 1) if q != r[i - 1]])
    return out

