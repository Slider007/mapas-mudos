import json,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import content as C
D={'sections':C.SECTIONS,'timeline':C.TIMELINE,'tlcore':C.TL_CORE,'pyramid':C.PYRAMID,'cities':C.CITIES,'cards':C.CARDS,
   'quiz':[{'q':q[0],'a':q[1],'w':q[2],'e':q[3],'topic':q[4]} for q in C.QUIZ],'tf':C.TF,'open':C.OPEN}
base=os.path.dirname(os.path.abspath(__file__))
G=open(os.path.join(base,'geo.json')).read()
t=open(os.path.join(base,'template.html'),encoding='utf8').read()
t=t.replace('__DATA__',json.dumps(D,ensure_ascii=False).replace('</','<\\/')).replace('__GEO__',G)
out=sys.argv[1];os.makedirs(os.path.dirname(out),exist_ok=True)
open(out,'w',encoding='utf8').write(t);print(out,len(t),'cards',len(C.CARDS),'quiz',len(C.QUIZ),'tf',len(C.TF),'open',len(C.OPEN))
