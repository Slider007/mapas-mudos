# Construye europa-fisica/index.html: python3 build.py ../../europa-fisica/index.html  (las imágenes van en europa-fisica/img/, ver relief.py)
import json, sys, os
base = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, base)
from datos import O, CATS, SECS, SEQ
t = open(os.path.join(base, 'template.html'), encoding='utf8').read()
D = {'O': [[o[0], o[1], o[2], o[3], None, o[5]] for o in O], 'CATS': CATS, 'SECS': SECS, 'SEQ': SEQ}
t = t.replace('__CSS__', open(os.path.join(base, 'base.css')).read())
t = t.replace('__GEO__', open(os.path.join(base, 'geo.json')).read()).replace('__DATA__', json.dumps(D, ensure_ascii=False))
os.makedirs(os.path.dirname(os.path.abspath(sys.argv[1])), exist_ok=True); open(sys.argv[1], 'w', encoding='utf8').write(t)
print(sys.argv[1], len(t))
