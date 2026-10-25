# Общее для мини-карт раздела «Aprender»: рамка карты по долготе/широте в проекции сайта.
def vb(lon0, lat0, lon1, lat1):
    """x=(lon+14)*C*K, y=(60-lat)*K — та же проекция, что в template.html (prj)"""
    C, K = 0.7193398, 20
    return [round((lon0 + 14) * C * K, 1), round((60 - lat1) * K, 1), round((lon1 - lon0) * C * K, 1), round((lat1 - lat0) * K, 1)]

import json as _json, os as _os
_F = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'fotos.json')))
def photo(key, cap, cap_ru, tall=False):
    """фото из Wikimedia Commons с автором и лицензией (см. fotos.json)"""
    f = _F[key]
    return {"img": "img/" + f["file"], "w": f["w"], "h": f["h"], "cap": cap, "cap_ru": cap_ru, "tall": tall,
            "url": f["commons"], "credit": f"Imagen: {f['author']} · {f['license']} · Wikimedia Commons"}
