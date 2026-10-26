# Busca en OpenStreetMap (Nominatim) los elementos que antes estaban dibujados a mano y guarda las respuestas en osm/<id>.json.
# Uso: python3 osm_fetch.py   (respeta el límite de Nominatim: 1 petición por segundo)
import json, os, sys, time, urllib.request, urllib.parse
UA = 'MapasMudosSchoolSite/1.0 (https://slider007.github.io/mapas-mudos/; educational, non-commercial)'
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'osm'); os.makedirs(OUT, exist_ok=True)
Q = {  # id: lista de búsquedas (se prueba en orden); tipos OSM aceptados
 'g_valencia': ['Golf de València', 'Golfo de Valencia'], 'g_genova': ['Golfo di Genova', 'Mar Ligure Golfo di Genova'], 'g_venecia': ['Golfo di Venezia'],
 'g_tarento': ['Golfo di Taranto'], 'g_corinto': ['Κορινθιακός Κόλπος', 'Gulf of Corinth'], 'g_salonica': ['Θερμαϊκός Κόλπος', 'Thermaic Gulf'], 'g_cadiz': ['Golfo de Cádiz'],
 'cantabrico': ['Mar Cantábrico'],
 'e_gibraltar': ['Estrecho de Gibraltar'], 'e_bonifacio': ['Bouches de Bonifacio', 'Strait of Bonifacio'], 'e_mesina': ['Stretto di Messina'], 'e_otranto': ["Canale d'Otranto", 'Strait of Otranto'],
 'e_dardanelos': ['Çanakkale Boğazı', 'Dardanelles'], 'e_bosforo': ['İstanbul Boğazı', 'Bosphorus'], 'e_kerch': ['Керченский пролив', 'Kerch Strait'], 'e_calais': ['Pas de Calais strait', 'Strait of Dover'],
 'e_sund': ['Øresund'], 'e_granbelt': ['Storebælt'], 'e_pequenobelt': ['Lillebælt'], 'k_norte': ['North Channel'], 'k_sanjorge': ["St George's Channel"],
 'c_gata': ['Cabo de Gata cape'], 'c_palos': ['Cabo de Palos'], 'c_nao': ['Cap de la Nau', 'Cabo de la Nao'], 'c_creus': ['Cap de Creus'], 'c_corcega': ['Capu Grossu', 'Cap Corse'],
 'c_spartivento': ['Capo Spartivento Calabria', 'Capo Spartivento Brancaleone'], 'c_passaro': ['Capo Passero'], 'c_leuca': ['Punta Meliso', 'Capo Santa Maria di Leuca'],
 'c_matapan': ['Ακρωτήριο Ταίναρο', 'Cape Matapan'], 'c_sanvicente': ['Cabo de São Vicente'], 'c_roca': ['Cabo da Roca'], 'c_finisterre': ['Cabo Fisterra'],
 'c_sanmateo': ['Pointe Saint-Mathieu'], 'c_landsend': ["Land's End"], 'c_lindesnes': ['Lindesnes fyr', 'Lindesnes'], 'c_skagen': ['Grenen'], 'c_norte': ['Nordkapp Magerøya', 'North Cape Norway', 'Nordkappen'],
 'm_beticas': ['Sistema Bético', 'Cordillera Bética', 'Cordilleras Béticas'], 'm_meseta': ['Meseta Central', 'Meseta Central Ibérica'], 'm_bohemia': ['Český masiv', 'Bohemian Massif'],
 'b_iberico': ['Sistema Ibérico'], 'b_cantabrica': ['Cordillera Cantábrica'], 'b_morena': ['Sierra Morena'], 'b_leon': ['Montes de León'],
 'll_europea': ['Great European Plain', 'Osteuropäische Ebene'], 'p_italica': ['Penisola italiana', 'Italian Peninsula'],
}
OK = {'bay', 'strait', 'cape', 'mountain_range', 'peninsula', 'sea', 'plateau', 'plain', 'point', 'water', 'ridge', 'massif', 'valley', 'lighthouse', 'locality'}
def get(q):
    u = 'https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode({'q': q, 'format': 'json', 'polygon_geojson': 1, 'limit': 6, 'accept-language': 'es'})
    for k in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=60))
        except Exception as e: print('  retry', e, file=sys.stderr); time.sleep(5)
    return []
only = sys.argv[1:]
for oid, qs in Q.items():
    if only and oid not in only: continue
    fn = os.path.join(OUT, oid + '.json')
    if os.path.exists(fn) and not only: continue
    best = None
    for qq in qs:
        res = get(qq); time.sleep(1.3)
        cand = [r for r in res if r.get('type') in OK or r.get('class') in ('natural',)]
        if cand: best = {'query': qq, 'res': cand}; break
    json.dump(best or {'query': qs, 'res': []}, open(fn, 'w'), ensure_ascii=False)
    print(oid, '→', [(r['osm_type'], r['osm_id'], r['class'], r['type'], r['geojson']['type'], r['display_name'][:50]) for r in (best or {'res': []})['res']][:3], flush=True)
