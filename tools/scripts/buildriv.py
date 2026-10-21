import pickle,math,json,re
from shapely.geometry import LineString,MultiLineString
P=pickle.load(open('osm_pick2.pkl','rb'));B=pickle.load(open('osm_bank.pkl','rb'))
exec(open('osmriv2.py').read().split('OUT={}')[0].split('def clusters')[0])
LON0,LAT1,K=-10.9,44.6,100;C=math.cos(math.radians(40))
pm=lambda lon,lat:[round((lon-LON0)*K*C,1),round((LAT1-lat)*K,1)]
L=[ # name, ru, cat
 ('Miño','Миньо','r_gal'),('Sil','Силь','r_gal'),('Ulla','Улья','r_gal'),('Tambre','Тамбре','r_gal'),('Eo','Эо','r_gal'),
 ('Navia','Навия','r_can'),('Nalón','Налон','r_can'),('Narcea','Нарсеа','r_can'),('Besaya','Бесайя','r_can'),('Nervión','Нервьон','r_can'),('Bidasoa','Бидасоа','r_can'),
 ('Duero','Дуэро','r_duero'),('Pisuerga','Писуэрга','r_duero'),('Arlanzón','Арлансон','r_duero'),('Carrión','Каррион','r_duero'),('Esla','Эсла','r_duero'),('Bernesga','Бернесга','r_duero'),('Eresma','Эресма','r_duero'),('Adaja','Адаха','r_duero'),('Tormes','Тормес','r_duero'),
 ('Tajo','Тахо','r_tajo'),('Jarama','Харама','r_tajo'),('Henares','Энарес','r_tajo'),('Alberche','Альберче','r_tajo'),('Tiétar','Тьетар','r_tajo'),('Alagón','Алагон','r_tajo'),('Almonte','Альмонте','r_tajo'),('Salor','Салор','r_tajo'),
 ('Guadiana','Гвадиана','r_guadiana'),('Záncara','Санкара','r_guadiana'),('Cigüela','Сигуэла','r_guadiana'),('Jabalón','Хабалон','r_guadiana'),('Zújar','Сухар','r_guadiana'),('Matachel','Матачель','r_guadiana'),
 ('Guadalquivir','Гвадалквивир','r_gq'),('Guadalimar','Гвадалимар','r_gq'),('Jándula','Хандула','r_gq'),('Guadalmellato','Гвадальмельято','r_gq'),('Guadiato','Гвадиато','r_gq'),('Bembézar','Бембесар','r_gq'),('Viar','Виар','r_gq'),('Guadiana Menor','Гвадиана-Менор','r_gq'),('Guadalbullón','Гвадальбульон','r_gq'),('Genil','Хениль','r_gq'),
 ('Odiel','Одьель','r_and'),('Tinto','Тинто','r_and'),('Guadalete','Гвадалете','r_and'),('Barbate','Барбате','r_and'),
 ('Ter','Тер','r_med'),
 ('Ebro','Эбро','r_ebro'),('Jalón','Халон','r_ebro'),('Jiloca','Хилока','r_ebro'),('Huerva','Уэрва','r_ebro'),('Guadalope','Гвадалопе','r_ebro'),('Arga','Арга','r_ebro'),('Aragón','Арагон','r_ebro'),('Gállego','Гальего','r_ebro'),('Cinca','Синка','r_ebro'),('Noguera Pallaresa','Ногера-Пальяреса','r_ebro'),('Noguera Ribagorzana','Ногера-Рибагорсана','r_ebro'),('Segre','Сегре','r_ebro'),
 ('Mijares','Михарес','r_med'),('Turia','Турия','r_med'),('Júcar','Хукар','r_med'),('Cabriel','Кабриэль','r_med'),('Segura','Сегура','r_med'),('Almanzora','Альмансора','r_med'),('Andarax','Андаракс','r_med'),('Adra','Адра','r_med'),('Guadalfeo','Гвадальфео','r_med'),('Guadalhorce','Гвадальорсе','r_med'),('Guadiaro','Гвадьяро','r_med')]
slug=lambda n:re.sub(r'[^a-z]','',n.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u').replace('ñ','n'))
ids={n:slug(n) for n,_,_ in L}
out=[];src={}
for n,ru,cat in L:
  g=P[n].simplify(0.003)
  ls=[l for l in (g.geoms if hasattr(g,'geoms') else [g]) if l.length>0.005]
  lines=[[pm(*c) for c in l.coords] for l in ls]
  main=max(ls,key=lambda l:l.length);lp=main.interpolate(0.5,normalized=True)
  o=dict(id=ids[n],name='Río '+n,short=n,cat=cat,kind='line',ru=ru,xy=[pm(lp.x,lp.y)],lines=lines)
  s='OpenStreetMap (Overpass, waterway=river)'
  if n in B:
    main_,bank,chain=B[n];o['parent']=ids[main_];o['bank']=bank
    if REC[n]!=main_:o['recv']=ids[REC[n]]
    s+=f'; впадение проверено по геометрии; берег относительно {main_} вычислен и совпал со списком'
  elif n in REC:o['parent']=ids[REC[n]];s+=f'; впадение в {REC[n]} проверено по геометрии'
  if n=='Segre':s+='; верхнее течение дополнено Natural Earth'
  if n in('Duero','Tajo'):s+='; в Португалии (Дору / Тежу) участок из Natural Earth'
  src[o['id']]=s;out.append(o)
json.dump({'objs':out,'src':src},open('riv_osm.json','w'),ensure_ascii=False)
print(len(out),len(json.dumps(out))//1024,'KB')
