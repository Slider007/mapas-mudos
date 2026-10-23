# Сборка тренажёра: python3 build.py <тема> <выход.html>   (тема = имя файла с содержанием: bizancio, visigodos, …)
import json, sys, os, importlib
base = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, base)
C = importlib.import_module(sys.argv[1]); out = sys.argv[2]
D = {'sections': C.SECTIONS, 'timeline': C.TIMELINE, 'tlcore': C.TL_CORE, 'pyramid': C.PYRAMID, 'maps': C.MAPS, 'cards': C.CARDS, 'topics': C.TOPICS,
     'quiz': [{'q': q[0], 'a': q[1], 'w': q[2], 'e': q[3], 'topic': q[4]} for q in C.QUIZ], 'tf': C.TF, 'open': C.OPEN}
G = open(os.path.join(base, 'geo.json')).read()
t = open(os.path.join(base, 'template.html'), encoding='utf8').read()
for k, v in [('__TITLE__', C.META['title']), ('__H1__', C.META['h1']), ('__SUB__', C.META['sub']), ('__FOOTER__', C.META['footer']), ('__LSP__', C.META['lsp'])]:
    t = t.replace(k, v)
t = t.replace('__DATA__', json.dumps(D, ensure_ascii=False).replace('</', '<\\/')).replace('__GEO__', G)
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
open(out, 'w', encoding='utf8').write(t)
print(out, len(t), 'cards', len(C.CARDS), 'quiz', len(C.QUIZ), 'tf', len(C.TF), 'open', len(C.OPEN), 'maps', len(C.MAPS))
