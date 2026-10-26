# Construye europa-politica/index.html: python3 build.py ../../europa-politica/index.html
import json, sys, os
base = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, base)
from paises import P, REG, NOTE
t = open(os.path.join(base, 'template.html'), encoding='utf8').read()
D = {'P': P, 'REG': REG, 'NOTE': NOTE}
t = t.replace('__GEO__', open(os.path.join(base, 'geo.json')).read()).replace('__DATA__', json.dumps(D, ensure_ascii=False))
os.makedirs(os.path.dirname(os.path.abspath(sys.argv[1])), exist_ok=True); open(sys.argv[1], 'w', encoding='utf8').write(t)
print(sys.argv[1], len(t))
