# Reduce los JSON de osm/: guarda solo id, tipo, nombre y la geometría simplificada (~200 m), suficiente para la escala del mapa.
import json, os, glob
from shapely.geometry import shape, mapping
HERE = os.path.dirname(os.path.abspath(__file__))
def rnd(o):
    if isinstance(o, float): return round(o, 4)
    if isinstance(o, (list, tuple)): return [rnd(x) for x in o]
    if isinstance(o, dict): return {k: rnd(v) for k, v in o.items()}
    return o
for fn in glob.glob(os.path.join(HERE, 'osm', '*.json')):
    if fn.endswith('dem_regions.json'): continue
    d = json.load(open(fn)); res = []
    for r in d.get('res', []):
        g = shape(r['geojson'])
        if g.geom_type != 'Point': g = g.simplify(0.002, preserve_topology=True)
        res.append({'osm_type': r['osm_type'], 'osm_id': r['osm_id'], 'class': r.get('class'), 'type': r.get('type'), 'display_name': r['display_name'], 'geojson': rnd(mapping(g))})
    json.dump({'query': d.get('query'), 'res': res, 'nota': 'Nominatim (OpenStreetMap, ODbL); geometría simplificada a ~200 m'}, open(fn, 'w'), ensure_ascii=False, separators=(',', ':'))
