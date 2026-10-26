# Тренажёр «El islam» (тема 2, часть 2A). Источник: резюме учителя (п. 1–21).
# Пп. 9 (пять столпов) и 19 (город) в резюме даны картинками: здесь — стандартное школьное содержание этих схем.
# Границы — Cliopatria (Seshat Global History Databank, CC BY 4.0), см. islam_geo.py; основа карты — geo_islam.json (Natural Earth).
import json, os
GEO = 'geo_islam.json'
_B = os.path.dirname(os.path.abspath(__file__))
_GG = json.load(open(os.path.join(_B, GEO)))
_G = json.load(open(os.path.join(_B, 'islam_geo.json')))

def _vb(lon0, lat0, lon1, lat1):
    C, K = _GG['C'], _GG['K']
    return [round((lon0 - _GG['LON0']) * C * K, 1), round((_GG['LAT1'] - lat1) * K, 1), round((lon1 - lon0) * C * K, 1), round((lat1 - lat0) * K, 1)]

META = {
 "title": "El islam — preparar la prueba", "h1": "☪️ El islam",
 "sub": "Tema 2 · el islam · aprender → repasar → examen", "lsp": "h2_isl_",
 "footer": "Fuente: resumen del profesor (puntos 1–21); los cinco pilares (punto 9) y las partes de la ciudad (punto 19), que en el resumen están en imágenes, siguen el esquema habitual del libro. Mapas: fronteras de Cliopatria (Seshat Global History Databank, CC BY 4.0; github.com/Seshat-Global-History-Databank/cliopatria); costas y ríos: Natural Earth 1:10m; itinerarios aproximados; fotos: Wikimedia Commons (autor y licencia en cada foto).",
}
TOPICS = {"arabia": "Arabia antes del islam", "mahoma": "Mahoma", "religion": "La religión", "mezquita": "La mezquita",
          "expansion": "Expansión y califas", "gobierno": "Gobierno y sociedad", "ciudad": "La ciudad", "ciencia": "Ciencia", "cultura": "Cultura y arte"}

SECTIONS = [
 {"id": "arabia", "t": "1. La península arábiga en el siglo VII", "tr": "Аравийский полуостров в VII веке",
  "pts": [
   "En el siglo VII la península arábiga estaba rodeada por dos imperios poderosos: el <b>Imperio persa</b> y el <b>Imperio bizantino</b>.",
   "Era un territorio <b>árido y desértico</b> entre el <b>mar Rojo</b>, el <b>golfo Pérsico</b> y el mar Mediterráneo.",
   "La habitaban pueblos <b>nómadas</b> y <b>pastores</b>, organizados en <b>tribus</b>. Eran <b>politeístas</b> (creían en muchos dioses).",
   "Las ciudades más importantes, como <b>La Meca</b> y <b>Medina</b>, estaban a orillas del mar Rojo."],
  "ru": "В VII в. Аравию окружали две могущественные империи — Персидская и Византийская. Это засушливый пустынный край между Красным морем, Персидским заливом и Средиземным морем. Жили там кочевники и пастухи, объединённые в племена; они были многобожниками. Главные города — Мекка и Медина — у Красного моря.",
  "key": "rodeada por los imperios persa y bizantino · árida y desértica · mar Rojo, golfo Pérsico · nómadas y pastores en tribus · politeístas · La Meca y Medina"},
 {"id": "economia", "topic": "arabia", "t": "2. ¿De qué vivían los árabes?", "tr": "Чем жили арабы",
  "pts": [
   "<b>Agricultura:</b> a orillas del mar Rojo y en los <b>oasis</b>: cereales, hortalizas, legumbres, <b>arroz</b>, frutales, plantas aromáticas, <b>moreras</b> (para criar gusanos de seda), plantas textiles (algodón, lino) y medicinales. Como había sequía, usaban el <b>regadío</b>: la <b>noria</b> (agua de los pozos), la <b>rueda hidráulica</b> (agua de los ríos), las <b>acequias</b> (canales de riego) y los <b>aljibes</b> (depósitos). Las casas de campo se llamaban <b>alquerías</b>.",
   "<b>Ganadería:</b> nómada, con pastores de <b>camellos</b>, cabras y ovejas.",
   "<b>Comercio:</b> los <b>beduinos</b> (árabes nómadas) hacían el comercio de <b>caravanas</b> por el desierto. En las ciudades se comerciaba en el <b>zoco</b>. Comercio internacional: de <b>Europa</b> llegaban metales y madera; de <b>África</b>, esclavos, oro y marfil; de <b>Oriente</b>, productos de lujo y especias.",
   "Monedas: <b>dinar</b> de oro, <b>dírham</b> de plata y <b>felús</b> de cobre. Los árabes controlaban las rutas del Próximo Oriente y las marítimas del Índico y el Mediterráneo (barcos de <b>vela triangular</b>).",
   "El comercio facilitó la <b>expansión del islam</b>, la aparición de nuevos puertos y rutas y el crecimiento de ciudades con escuelas, bibliotecas y centros de traductores, que llevaron a Europa el saber antiguo y oriental.",
   "<b>Artesanía:</b> los <b>gremios</b> se agrupaban en barrios según su actividad: cuero, metales, tejidos y cerámica."],
  "ru": "Земледелие — у Красного моря и в оазисах: зерно, овощи, бобовые, рис, фрукты, пряности, шелковица (для шелкопряда), хлопок, лён, лекарственные растения. Из-за засухи — орошение: нория (вода из колодцев), водяное колесо (из рек), арыки-асекии (каналы), альхибы (цистерны). Сельские дома — алькерии. Скотоводство кочевое: верблюды, козы, овцы. Торговля: бедуины водили караваны через пустыню; в городах — рынок-сук. Из Европы — металлы и дерево, из Африки — рабы, золото, слоновая кость, с Востока — роскошь и пряности. Монеты: золотой динар, серебряный дирхам, медный фельс. Арабы контролировали пути Ближнего Востока, Индийского океана и Средиземноморья (корабли с треугольным парусом). Торговля помогла распространению ислама, росту портов и городов со школами и библиотеками. Ремесленники объединялись в цеха по кварталам: кожа, металл, ткани, керамика.",
  "key": "regadío: noria, rueda hidráulica, acequias, aljibes · alquerías · camellos · beduinos y caravanas · zoco · dinar, dírham, felús · vela triangular · gremios por barrios"},
 {"id": "mahoma", "t": "3. Mahoma y el origen del islam", "tr": "Мухаммед и рождение ислама",
  "pts": [
   "<b>Mahoma</b> nació en el <b>570</b> en <b>La Meca</b>, en una familia acomodada. Era <b>comerciante</b>.",
   "En el <b>610</b>, meditando en una cueva, se le apareció el <b>arcángel Gabriel</b>: le dijo que era el elegido por el dios <b>Alá</b> para predicar una nueva religión <b>monoteísta</b>, el <b>islam</b>.",
   "Los habitantes de La Meca no le creyeron y en el <b>622</b> huyó a <b>Medina</b>: es la <b>Hégira</b>, que marca el <b>inicio del calendario musulmán</b>.",
   "Tras convertir a los habitantes de Medina, reunió un ejército, <b>conquistó La Meca</b> y acabó con el politeísmo. Desde allí extendió la nueva religión por toda <b>Arabia</b>.",
   "Cuando murió en el <b>632</b>, gran parte de Arabia era musulmana."],
  "ru": "Мухаммед родился в 570 г. в Мекке в зажиточной семье, был купцом. В 610 г., размышляя в пещере, он увидел архангела Джибрила (Гавриила): тот сказал, что Аллах избрал его проповедовать новую единобожную религию — ислам. Мекканцы не поверили, и в 622 г. он бежал в Медину — это хиджра, начало мусульманского летоисчисления. Обратив жителей Медины, он собрал войско, взял Мекку и покончил с многобожием, затем распространил ислам по Аравии. Когда он умер (632), большая часть Аравии была мусульманской.",
  "key": "570 nace en La Meca · comerciante · 610 arcángel Gabriel · Alá, islam monoteísta · 622 Hégira a Medina = inicio del calendario · conquista La Meca · 632 muere"},
 {"id": "religion", "t": "4. La religión islámica", "tr": "Исламская религия",
  "pts": [
   "El islam predica que existe <b>un solo dios, Alá</b>, y considera a Mahoma un <b>profeta</b>, igual que Abraham, Moisés o Jesús.",
   "El <b>Corán</b> es el libro sagrado: tiene <b>114 suras</b> (capítulos) escritas en <b>árabe</b> con las normas del islam, de la vida privada y las obligaciones de la <b>umma</b> (la comunidad islámica).",
   "La <b>Sunna</b> recoge las costumbres del profeta. El Corán y la Sunna forman la <b>sharía</b>, la ley sagrada.",
   "El <b>califa</b> es el jefe religioso y político; los califas son los herederos de Mahoma.",
   "<b>Los cinco pilares del islam:</b> 1) la <b>profesión de fe</b> («No hay más dios que Alá y Mahoma es su profeta»); 2) la <b>oración</b> cinco veces al día, mirando hacia La Meca; 3) la <b>limosna</b> a los pobres; 4) el <b>ayuno</b> durante el mes de <b>Ramadán</b>; 5) la <b>peregrinación a La Meca</b> al menos una vez en la vida.",
   "<b>Prohibiciones:</b> comer <b>cerdo</b>, beber <b>alcohol</b> y los juegos de azar. Se permite la <b>poligamia</b> (como máximo <b>4 mujeres</b>).",
   "En el islam <b>no hay sacerdotes</b>, pero hay <b>imanes</b> (dirigen la oración), <b>ulemas</b> (interpretan los textos sagrados) y <b>cadíes</b> (jueces elegidos entre los creyentes más devotos, que aplican la justicia según el Corán).",
   "Hay dos corrientes: los <b>sunitas o suníes</b> (el <b>90 %</b>; siguen el Corán y la Sunna; el califa debía ser elegido entre los mejores creyentes) y los <b>chiitas o chiíes</b> (se separaron cuando los omeyas llegaron al poder; siguen a sus líderes, los <b>ayatolás</b>; el califa debía ser <b>descendiente de Mahoma</b>)."],
  "ru": "Ислам учит, что Бог один — Аллах, а Мухаммед — пророк, как Авраам, Моисей или Иисус. Священная книга — Коран: 114 сур (глав) на арабском с нормами веры, частной жизни и обязанностями уммы (общины). Сунна — обычаи пророка; Коран и Сунна вместе — шариат (священный закон). Халиф — религиозный и политический глава, наследник Мухаммеда. Пять столпов: исповедание веры («Нет бога, кроме Аллаха, и Мухаммед — пророк его»), молитва пять раз в день лицом к Мекке, милостыня бедным, пост в месяц Рамадан, паломничество в Мекку хотя бы раз в жизни. Запреты: свинина, алкоголь, азартные игры. Многожёнство разрешено (до 4 жён). Священников нет, но есть имамы (ведут молитву), улемы (толкуют тексты) и кади (судьи). Два течения: сунниты (90 %, Коран и Сунна, халифа выбирают) и шииты (отделились при Омейядах, слушают аятолл, халиф — потомок Мухаммеда).",
  "key": "un solo dios, Alá · Mahoma profeta · Corán (114 suras) · Sunna · sharía · umma · cinco pilares: fe, oración, limosna, ayuno (Ramadán), peregrinación a La Meca · sin cerdo ni alcohol · imán, ulema, cadí · sunitas (90 %) y chiitas (ayatolás)"},
 {"id": "mezquita", "t": "5. La mezquita y la Kaaba", "tr": "Мечеть и Кааба",
  "pts": [
   "La <b>mezquita</b> es el lugar de culto de los musulmanes, pero también era <b>escuela</b> y lugar donde se difundían las noticias.",
   "<b>Patio</b> rodeado de columnas, con la <b>fuente de abluciones</b>, donde los fieles se purificaban antes de rezar.",
   "<b>Sala de oración</b> cubierta. En ella está el <b>muro de la quibla</b>, orientado hacia <b>La Meca</b>; en él hay un nicho vacío, el <b>mihrab</b>, donde suele estar el Corán. Cerca del mihrab suele haber un púlpito, el <b>mimbar</b>.",
   "<b>Minarete o alminar:</b> torre desde donde el <b>almuecín o almuédano</b> llama a los fieles a la oración con un cántico.",
   "La mezquita está inspirada en la <b>casa de Mahoma en Medina</b>. Su forma cúbica recuerda la <b>Kaaba</b> de La Meca, el lugar de peregrinación más importante.",
   "La <b>Piedra Negra</b> es una reliquia de la Kaaba: un meteorito que el arcángel Gabriel dio a <b>Abraham</b>. Era blanca, pero los pecados de los hijos de Adán la volvieron negra. Abraham y su hijo <b>Ismael</b> la colocaron en la esquina oriental de la Kaaba."],
  "ru": "Мечеть — место молитвы, а также школа и место, где узнавали новости. Части: двор с колоннами и фонтаном для омовений; крытый молитвенный зал с михрабом в стене киблы (обращённой к Мекке) — пустой нишей, где обычно лежит Коран, рядом — кафедра-минбар; минарет, с которого муэдзин пением созывает на молитву. Мечеть повторяет дом Мухаммеда в Медине, а её кубическая форма напоминает Каабу в Мекке — главное место паломничества. Чёрный камень — реликвия Каабы: метеорит, который архангел Джибрил дал Аврааму; он был белым, но почернел от грехов людей. Авраам и его сын Исмаил вставили его в восточный угол Каабы.",
  "key": "mezquita = culto, escuela, noticias · patio con fuente de abluciones · sala de oración · muro de la quibla (hacia La Meca) · mihrab · mimbar · alminar y almuecín · Kaaba y Piedra Negra"},
 {"id": "expansion", "t": "6. La expansión del islam y los califas", "tr": "Распространение ислама и халифы",
  "pts": [
   "Al morir Mahoma (<b>632</b>), sus sucesores, los <b>califas</b>, conquistaron un gran imperio, <b>desde la península ibérica hasta la India</b> (<b>yihad</b> o guerra santa). Se enfrentaron con el Imperio bizantino, los francos…",
   "<b>1ª etapa: califas ortodoxos (632–661):</b> cuatro califas, familiares o amigos de Mahoma, <b>elegidos</b>. El califa tenía <b>poder absoluto</b>: máxima autoridad religiosa, juez supremo, general de los ejércitos y nombraba los cargos públicos.",
   "<b>2ª etapa: dinastía omeya (661–750):</b> procedía de Siria; capital en <b>Damasco</b>. Fue la etapa de <b>mayor expansión</b>. El cargo se hizo <b>hereditario</b> y el imperio se dividió en provincias o <b>emiratos</b>. La familia omeya fue asesinada, salvo el príncipe <b>Abderramán</b>, que huyó a la península ibérica.",
   "<b>3ª etapa: dinastía abasí (750–1258):</b> capital en <b>Bagdad</b>. Fue el período de <b>mayor esplendor económico y cultural</b>. Desde el siglo X el imperio se dividió en califatos independientes (como en la península ibérica). Terminó cuando los <b>mongoles</b> saquearon Bagdad (<b>1258</b>).",
   "Después ganaron fuerza los <b>turcos otomanos</b> (musulmanes), que en <b>1453</b> conquistaron <b>Constantinopla</b> y la llamaron <b>Estambul</b>.",
   "<b>¿Por qué fue tan rápida la expansión?</b> Por la motivación de difundir y defender la fe (se prometía el <b>paraíso</b> a quien muriera luchando contra los infieles); por la <b>debilidad</b> de los imperios vecinos (persa y bizantino), y por los <b>pactos</b> con la población: se respetaban su fe y sus propiedades. Cristianos y judíos, monoteístas con la Biblia, eran una <b>minoría protegida</b>: conservaban religión, leyes y costumbres a cambio de pagar <b>tributos</b>."],
  "ru": "После смерти Мухаммеда (632) халифы создали огромную империю — от Испании до Индии (джихад, священная война), воевали с Византией, франками. 1) Праведные халифы (632–661): четверо родственников или друзей Мухаммеда, их выбирали; власть халифа абсолютна (религия, суд, войско, назначения). 2) Омейяды (661–750): из Сирии, столица — Дамаск; наибольшее расширение; власть стала наследственной, империя делилась на провинции-эмираты; Омейядов перебили, спасся только Абд ар-Рахман, бежавший в Испанию. 3) Аббасиды (750–1258): столица — Багдад; наивысший экономический и культурный расцвет; с X в. распад на независимые халифаты; конец — разграбление Багдада монголами (1258). Позже усилились турки-османы и в 1453 г. взяли Константинополь (Стамбул). Причины быстрого расширения: вера (рай погибшим в бою), слабость Персии и Византии, договоры с местными жителями: христиане и иудеи сохраняли веру и законы, платя дань.",
  "key": "632 muere Mahoma · de la península ibérica a la India · ortodoxos (632–661, elegidos) · omeyas (661–750, Damasco, mayor expansión, hereditario) · abasíes (750–1258, Bagdad, esplendor) · 1258 mongoles · 1453 otomanos: Estambul · fe, debilidad de los vecinos, pactos y tributos"},
 {"id": "gobierno", "t": "7. Gobierno y sociedad del Imperio islámico", "tr": "Управление и общество",
  "pts": [
   "<b>Califa:</b> máxima autoridad política y religiosa; dirigía el ejército, hacía las leyes y era juez supremo. <b>Visires:</b> consejeros del califa (primer ministro). <b>Cadíes:</b> aplicaban la justicia según el Corán y enseñaban sus doctrinas. <b>Valíes:</b> gobernaban las provincias. <b>Emires:</b> príncipes o nobles, familiares del califa, que actuaban como valí de una provincia y tenían poder militar. <b>Diwán:</b> tesorero real.",
   "Los musulmanes eran <b>tolerantes</b> con otras religiones, pero difundieron el islam y la cultura árabe. El <b>árabe</b> fue la lengua oficial. Las <b>ventajas económicas y sociales</b> de ser musulmán hicieron que la mayoría de la población se islamizara.",
   "La sociedad era muy <b>heterogénea</b>: distintas religiones (musulmanes, judíos, cristianos) y etnias (árabes, bereberes…). Se dividía según la <b>riqueza</b>:",
   "1º <b>Aristocracia árabe:</b> pocos, con poder político y económico; grandes propietarios y gobernantes.",
   "2º <b>Notables:</b> vivían bien pero sin cargos políticos: comerciantes, artesanos con taller propio y pequeños propietarios.",
   "3º <b>La mayoría de la población, pobre:</b> campesinos sin tierras, artesanos sin taller, vendedores ambulantes y criados.",
   "Las <b>mujeres</b> estaban bajo la autoridad del padre o del marido; cuidaban la casa y los hijos y <b>no podían estudiar</b>."],
  "ru": "Халиф — высшая политическая и религиозная власть (войско, законы, суд). Визири — советники (первый министр). Кади — судьи по Корану. Вали — правители провинций. Эмиры — родственники халифа во главе провинций, с военной властью. Диван — казначейство. Мусульмане терпимо относились к другим религиям, но распространяли ислам и арабскую культуру; арабский — официальный язык. Быть мусульманином было выгодно, поэтому большинство приняло ислам. Общество разнородное и делилось по богатству: 1) арабская аристократия — немногие, власть и земли; 2) знатные горожане — купцы, ремесленники со своей мастерской, мелкие землевладельцы; 3) большинство — бедные: безземельные крестьяне, ремесленники без мастерской, разносчики, слуги. Женщины подчинялись отцу или мужу, вели дом и не могли учиться.",
  "key": "califa · visires · cadíes · valíes · emires · diwán · árabe lengua oficial · islamización por ventajas · 1º aristocracia árabe, 2º notables, 3º mayoría pobre · mujeres sin estudios"},
 {"id": "ciudad", "t": "8. La ciudad islámica", "tr": "Исламский город",
  "pts": [
   "La <b>medina</b> era el centro de la ciudad, rodeada por una <b>muralla</b> con puertas. Sus calles eran estrechas y tortuosas, a veces sin salida (adarves).",
   "En el centro estaba la <b>mezquita mayor</b> y, a su alrededor, el <b>zoco</b> (mercado) con tiendas agrupadas por oficios y la <b>alcaicería</b> (mercado de productos de lujo, como la seda).",
   "<b>Alhóndiga:</b> almacenes donde los comerciantes guardaban las mercancías (y donde se alojaban). <b>Madrasa:</b> escuela. <b>Baños</b> públicos (hammam).",
   "La <b>alcazaba</b> era la fortaleza, residencia del gobernador. Fuera de la muralla estaban los <b>arrabales</b> (barrios nuevos), los <b>cementerios</b> y las huertas.",
   "Las <b>casas</b> eran pequeñas, de <b>ladrillo</b> y de <b>dos pisos</b>: la planta baja para recibir a las visitas y la alta con las habitaciones privadas. Había <b>pocos muebles</b>."],
  "ru": "Центр города — медина, окружённая стеной с воротами; улицы узкие и извилистые, порой тупики. В центре — главная (соборная) мечеть, вокруг — рынок-сук с лавками по ремёслам и алькайсерия (рынок предметов роскоши, шёлка). Альондига — склады купцов (и постоялый двор). Медресе — школа. Общественные бани (хаммам). Алькасаба — крепость, резиденция правителя. За стеной — пригороды (арраббали), кладбища, огороды. Дома маленькие, кирпичные, в два этажа: внизу принимали гостей, наверху — личные комнаты; мебели мало.",
  "key": "medina amurallada · mezquita mayor · zoco · alcaicería · alhóndiga = almacenes · madrasa = escuela · baños · alcazaba · arrabales · casas de ladrillo, dos pisos, pocos muebles"},
 {"id": "ciencia", "t": "9. Los avances científicos", "tr": "Научные достижения",
  "pts": [
   "Los musulmanes trajeron de <b>India y China</b> el <b>papel</b>, la <b>pólvora</b> e instrumentos de navegación como la <b>brújula</b> y el <b>astrolabio</b>.",
   "<b>Agricultura:</b> la <b>noria</b> y el <b>molino de agua</b>, el regadío por <b>acequias</b> y canales, y nuevos cultivos como el <b>arroz</b>, la <b>naranja</b> o el <b>azafrán</b>.",
   "<b>Astronomía:</b> catálogos de astros y observatorios.",
   "<b>Matemáticas:</b> difundieron el uso del <b>cero</b>, inventaron el <b>álgebra</b> y perfeccionaron la aritmética y la trigonometría.",
   "<b>Medicina:</b> técnicas avanzadas de <b>cirugía</b> y <b>anestesia</b>. Destacan <b>Avicena</b> y <b>Averroes</b>.",
   "<b>Química:</b> descubrieron el <b>ácido sulfúrico</b> y el <b>ácido nítrico</b> y desarrollaron los primeros métodos de <b>destilación</b> del alcohol."],
  "ru": "Мусульмане принесли из Индии и Китая бумагу, порох, компас и астролябию. Земледелие: нория и водяная мельница, орошение арыками и каналами, новые культуры — рис, апельсин, шафран. Астрономия: каталоги звёзд, обсерватории. Математика: распространили ноль, придумали алгебру, развили арифметику и тригонометрию. Медицина: хирургия и обезболивание; Авиценна и Аверроэс. Химия: серная и азотная кислоты, первые способы перегонки спирта.",
  "key": "papel, pólvora, brújula, astrolabio (de India y China) · noria, molino de agua · arroz, naranja, azafrán · cero y álgebra · cirugía y anestesia: Avicena, Averroes · ácidos, destilación"},
 {"id": "cultura", "t": "10. La cultura y el arte islámico", "tr": "Культура и искусство",
  "pts": [
   "La expansión puso a los musulmanes en contacto con otras lenguas, formas de vida y creencias. El <b>árabe</b> (la lengua del Corán) fue el vehículo de comunicación; muchas <b>palabras árabes</b> han llegado hasta hoy.",
   "<b>Tradujeron al árabe</b> muchas obras griegas y romanas y escribieron libros de viajes, historia y geografía. Destacan las fábulas, los cuentos cortos como <b>Las mil y una noches</b> y la poesía. Las <b>bibliotecas</b> guardaban todo el saber.",
   "<b>Arquitectura:</b> <b>materiales pobres</b> (ladrillo, yeso…); mezquitas, palacios, madrasas; columnas y pilares; arcos (de medio punto peraltado, <b>polilobulado</b>, de <b>herradura</b>, entrecruzado…); <b>cúpulas</b> (gallonada) y bóvedas; techos planos de madera.",
   "<b>Decoración:</b> motivos geométricos (<b>lacería</b>), vegetales (<b>ataurique</b>), <b>inscripciones</b> de libros sagrados y poemas, celosías, vidrieras, <b>azulejos</b>, <b>mocárabes</b>…",
   "El <b>agua</b> era un elemento decorativo: su sonido, su reflejo y su simbología (la vida en medio del desierto).",
   "También destacaron en <b>cerámica</b>, vidrio esmaltado, <b>marfil</b> y <b>cuero</b>."],
  "ru": "Завоевания познакомили мусульман с другими языками и культурами. Арабский язык Корана стал общим языком; многие арабские слова дошли до наших дней. Перевели на арабский многие греческие и римские книги, писали о путешествиях, истории, географии; басни, сказки («Тысяча и одна ночь»), поэзия; библиотеки хранили знания. Архитектура: бедные материалы (кирпич, гипс); мечети, дворцы, медресе; колонны, разные арки (подковообразная, многолопастная, перекрещивающаяся), купола, деревянные потолки. Декор: геометрический (ласерия), растительный (атаурике), надписи, решётки, витражи, изразцы (асулехос), сталактиты (мукарны). Вода — часть декора: звук, отражение, символ жизни в пустыне. Также керамика, эмалированное стекло, слоновая кость, кожа.",
  "key": "árabe y palabras árabes · traducciones de obras griegas y romanas · Las mil y una noches · bibliotecas · materiales pobres · arco de herradura y polilobulado · cúpulas · lacería, ataurique, inscripciones, azulejos, mocárabes · agua"},
]

TIMELINE = [
 [570, "Nace Mahoma en La Meca", "Рождение Мухаммеда в Мекке"],
 [610, "El arcángel Gabriel se aparece a Mahoma", "Явление архангела Джибрила"],
 [622, "Hégira: Mahoma huye a Medina; empieza el calendario musulmán", "Хиджра: бегство в Медину"],
 [630, "Mahoma conquista La Meca", "Мухаммед берёт Мекку"],
 [632, "Muere Mahoma; califas ortodoxos (632–661)", "Смерть Мухаммеда; праведные халифы"],
 [661, "Dinastía omeya, capital Damasco (661–750)", "Омейяды, столица Дамаск"],
 [711, "Los musulmanes llegan a la península ibérica", "Мусульмане в Испании"],
 [732, "Batalla de Poitiers: los francos frenan a los musulmanes", "Битва при Пуатье"],
 [750, "Dinastía abasí, capital Bagdad (750–1258)", "Аббасиды, столица Багдад"],
 [1258, "Los mongoles saquean Bagdad: fin de los abasíes", "Монголы грабят Багдад"],
 [1453, "Los turcos otomanos conquistan Constantinopla (Estambul)", "Османы берут Константинополь"],
]
TL_CORE = [570, 610, 622, 632, 661, 750, 1258, 1453]

PYRAMID = {
 "title": "La sociedad islámica", "apex": "Califa",
 "note": "La división social se basaba en la riqueza (resumen del profesor, punto 18).", "src": "Resumen del profesor, punto 18.",
 "levels": ["1º · Arriba", "2º · En medio", "3º · Abajo"],
 "items": [["Aristocracia árabe", 0], ["Grandes propietarios y gobernantes", 0],
           ["Notables", 1], ["Comerciantes y artesanos con taller propio", 1], ["Pequeños propietarios de tierras", 1],
           ["Campesinos sin tierras", 2], ["Artesanos sin taller y vendedores ambulantes", 2], ["Criados", 2]],
}

CARDS = [
 ["Península arábiga", "Territorio árido y desértico entre el mar Rojo, el golfo Pérsico y el Mediterráneo.", "Аравийский полуостров"],
 ["Politeísmo", "Creencia en muchos dioses; así eran los árabes antes del islam.", "Многобожие"],
 ["Beduinos", "Árabes nómadas que hacían el comercio de caravanas por el desierto.", "Бедуины"],
 ["Caravana", "Grupo de cientos de camellos que transportaban mercancías por el desierto.", "Караван"],
 ["Oasis", "Lugar con agua y vegetación en medio del desierto.", "Оазис"],
 ["Noria", "Máquina para sacar agua de los pozos.", "Нория"],
 ["Rueda hidráulica", "Rueda para sacar agua de los ríos.", "Водяное колесо"],
 ["Acequia", "Canal de riego.", "Асекия (арык)"],
 ["Aljibe", "Depósito para almacenar el agua.", "Альхибе (цистерна)"],
 ["Alquería", "Casa de campo.", "Алькерия"],
 ["Zoco", "Mercado principal de la ciudad.", "Сук (рынок)"],
 ["Dinar, dírham y felús", "Monedas de oro, plata y cobre.", "Динар, дирхам, фельс"],
 ["Gremio", "Asociación de artesanos de un mismo oficio, agrupados por barrios.", "Цех"],
 ["Mahoma", "Profeta del islam, nacido en La Meca en el 570; murió en el 632.", "Мухаммед"],
 ["La Meca", "Ciudad natal de Mahoma, donde está la Kaaba.", "Мекка"],
 ["Medina", "Ciudad a la que huyó Mahoma en el 622.", "Медина"],
 ["Arcángel Gabriel", "Se apareció a Mahoma en el 610 en una cueva.", "Архангел Джибрил (Гавриил)"],
 ["Alá", "El dios único del islam.", "Аллах"],
 ["Islam", "Religión monoteísta predicada por Mahoma.", "Ислам"],
 ["Hégira", "Huida de Mahoma de La Meca a Medina (622); inicio del calendario musulmán.", "Хиджра"],
 ["Corán", "Libro sagrado del islam: 114 suras en árabe.", "Коран"],
 ["Sura", "Capítulo del Corán.", "Сура"],
 ["Sunna", "Libro con las costumbres del profeta.", "Сунна"],
 ["Sharía", "Ley sagrada islámica: el Corán y la Sunna.", "Шариат"],
 ["Umma", "La comunidad islámica.", "Умма"],
 ["Califa", "Jefe religioso y político, heredero de Mahoma.", "Халиф"],
 ["Cinco pilares", "Profesión de fe, oración, limosna, ayuno en Ramadán y peregrinación a La Meca.", "Пять столпов ислама"],
 ["Ramadán", "Mes en que los musulmanes ayunan.", "Рамадан"],
 ["Imán", "Dirige la oración.", "Имам"],
 ["Ulema", "Interpreta los textos sagrados.", "Улем"],
 ["Cadí", "Juez que aplica la justicia según el Corán.", "Кади"],
 ["Mezquita", "Lugar de culto; también escuela y lugar de noticias.", "Мечеть"],
 ["Fuente de abluciones", "Fuente del patio donde los fieles se purifican antes de rezar.", "Фонтан для омовений"],
 ["Muro de la quibla", "Muro de la sala de oración orientado hacia La Meca.", "Стена киблы"],
 ["Mihrab", "Nicho vacío en el muro de la quibla, donde suele estar el Corán.", "Михраб"],
 ["Mimbar", "Púlpito cerca del mihrab.", "Минбар"],
 ["Alminar o minarete", "Torre desde donde se llama a la oración.", "Минарет"],
 ["Almuecín o almuédano", "Hombre que llama a los fieles a la oración desde el alminar.", "Муэдзин"],
 ["Kaaba", "Santuario de La Meca, el lugar de peregrinación más importante.", "Кааба"],
 ["Piedra Negra", "Reliquia de la Kaaba: meteorito que Gabriel dio a Abraham.", "Чёрный камень"],
 ["Sunitas", "El 90 % de los musulmanes; siguen el Corán y la Sunna; califa elegido.", "Сунниты"],
 ["Chiitas", "Siguen a los ayatolás; el califa debía ser descendiente de Mahoma.", "Шииты"],
 ["Ayatolá", "Líder religioso de los chiitas.", "Аятолла"],
 ["Yihad", "Guerra santa para extender el islam.", "Джихад"],
 ["Califas ortodoxos", "Los cuatro primeros califas (632–661), elegidos.", "Праведные халифы"],
 ["Omeyas", "Dinastía de califas (661–750), capital Damasco; mayor expansión.", "Омейяды"],
 ["Damasco", "Capital del califato omeya.", "Дамаск"],
 ["Abasíes", "Dinastía de califas (750–1258), capital Bagdad; mayor esplendor.", "Аббасиды"],
 ["Bagdad", "Capital del califato abasí; saqueada por los mongoles en 1258.", "Багдад"],
 ["Turcos otomanos", "Musulmanes que conquistaron Constantinopla en 1453 (Estambul).", "Турки-османы"],
 ["Visir", "Consejero del califa, primer ministro.", "Визирь"],
 ["Valí", "Gobernador de una provincia.", "Вали"],
 ["Emir", "Príncipe, familiar del califa, que gobierna una provincia con poder militar.", "Эмир"],
 ["Diwán", "Tesorero real.", "Диван (казна)"],
 ["Aristocracia árabe", "Pocos, con poder político y económico: grandes propietarios y gobernantes.", "Арабская аристократия"],
 ["Notables", "Comerciantes, artesanos con taller y pequeños propietarios, sin cargos políticos.", "Знатные горожане"],
 ["Medina (parte de la ciudad)", "Centro amurallado de la ciudad islámica.", "Медина (центр города)"],
 ["Alcaicería", "Mercado de productos de lujo, como la seda.", "Алькайсерия"],
 ["Alhóndiga", "Almacenes donde los comerciantes guardaban las mercancías.", "Альондига (склад)"],
 ["Madrasa", "Escuela.", "Медресе"],
 ["Alcazaba", "Fortaleza de la ciudad, residencia del gobernador.", "Алькасаба"],
 ["Arrabal", "Barrio fuera de la muralla.", "Пригород (арраббаль)"],
 ["Astrolabio", "Instrumento de navegación para medir la altura de los astros.", "Астролябия"],
 ["Álgebra", "Parte de las matemáticas inventada por los musulmanes.", "Алгебра"],
 ["Avicena", "Médico y filósofo musulmán.", "Авиценна"],
 ["Las mil y una noches", "Colección de cuentos árabes.", "«Тысяча и одна ночь»"],
 ["Lacería", "Decoración con motivos geométricos.", "Ласерия (геометрический узор)"],
 ["Ataurique", "Decoración con motivos vegetales.", "Атаурике (растительный узор)"],
 ["Mocárabes", "Decoración de techos y arcos con prismas que cuelgan, como estalactitas.", "Мукарны (сталактиты)"],
 ["Azulejo", "Pieza de cerámica vidriada para decorar paredes.", "Изразец (асулехо)"],
]

QUIZ = [
 ["¿Qué dos imperios rodeaban la península arábiga en el siglo VII?", "El persa y el bizantino", ["El romano y el carolingio", "El mongol y el chino", "El franco y el visigodo"], "Persia al este y Bizancio al norte.", "arabia"],
 ["¿Cómo era la península arábiga?", "Árida y desértica", ["Húmeda y boscosa", "Montañosa y nevada", "Un gran llano verde"], "Entre el mar Rojo, el golfo Pérsico y el Mediterráneo.", "arabia"],
 ["¿Qué religión tenían los árabes antes del islam?", "Eran politeístas", ["Eran cristianos", "Eran monoteístas", "No tenían religión"], "Creían en muchos dioses.", "arabia"],
 ["¿Dónde estaban La Meca y Medina?", "A orillas del mar Rojo", ["En el golfo Pérsico", "Junto al Mediterráneo", "En el río Nilo"], "Allí estaban las ciudades más importantes.", "arabia"],
 ["¿Para qué servía la noria?", "Para sacar agua de los pozos", ["Para moler trigo", "Para navegar", "Para guardar el agua"], "La rueda hidráulica sacaba agua de los ríos.", "arabia"],
 ["¿Qué es un aljibe?", "Un depósito para almacenar agua", ["Un canal de riego", "Una casa de campo", "Un mercado"], "La acequia es el canal.", "arabia"],
 ["¿Cómo se llamaban las casas de campo?", "Alquerías", ["Alcazabas", "Alhóndigas", "Madrasas"], "Alquería = casa de campo.", "arabia"],
 ["¿Quiénes eran los beduinos?", "Árabes nómadas que comerciaban con caravanas", ["Jueces del Corán", "Soldados del califa", "Monjes cristianos"], "Cruzaban el desierto con camellos.", "arabia"],
 ["¿Qué llegaba de África?", "Esclavos, oro y marfil", ["Metales y madera", "Especias y lujo", "Papel y pólvora"], "De Europa, metales y madera; de Oriente, lujo y especias.", "arabia"],
 ["¿Cuál era la moneda de cobre?", "El felús", ["El dinar", "El dírham", "El sólido"], "Dinar de oro, dírham de plata.", "arabia"],
 ["¿Cómo se organizaban los artesanos?", "En gremios agrupados por barrios", ["En monasterios", "En feudos", "En tribus nómadas"], "Cuero, metales, tejidos, cerámica.", "arabia"],
 ["¿Dónde y cuándo nació Mahoma?", "En La Meca, en el 570", ["En Medina, en el 622", "En Damasco, en el 661", "En Bagdad, en el 750"], "En una familia acomodada.", "mahoma"],
 ["¿A qué se dedicaba Mahoma?", "Era comerciante", ["Era pastor", "Era soldado", "Era sacerdote"], "Comerciante de La Meca.", "mahoma"],
 ["¿Quién se apareció a Mahoma en el 610?", "El arcángel Gabriel", ["Abraham", "Moisés", "El califa"], "En una cueva, mientras meditaba.", "mahoma"],
 ["¿Qué es la Hégira?", "La huida de Mahoma de La Meca a Medina (622)", ["La conquista de La Meca", "La peregrinación a La Meca", "El libro sagrado"], "Marca el inicio del calendario musulmán.", "mahoma"],
 ["¿Qué marca la Hégira?", "El inicio del calendario musulmán", ["El fin del islam", "La muerte de Mahoma", "La llegada a la península"], "Año 622.", "mahoma"],
 ["¿Cuándo murió Mahoma?", "En el 632", ["En el 570", "En el 711", "En el 1258"], "Gran parte de Arabia ya era musulmana.", "mahoma"],
 ["¿Qué predica el islam?", "Que hay un solo dios, Alá", ["Que hay muchos dioses", "Que Mahoma es dios", "Que no hay dios"], "Mahoma es un profeta.", "religion"],
 ["¿Cuántas suras tiene el Corán?", "114", ["5", "33", "1001"], "Escritas en árabe.", "religion"],
 ["¿Qué es la umma?", "La comunidad islámica", ["El libro sagrado", "Un tipo de mezquita", "La ley sagrada"], "Comunidad de creyentes.", "religion"],
 ["¿Qué forman el Corán y la Sunna?", "La sharía o ley sagrada", ["La umma", "El califato", "La Hégira"], "La Sunna recoge las costumbres del profeta.", "religion"],
 ["¿Cuál NO es un pilar del islam?", "Ir a la guerra cada año", ["La oración", "La limosna", "El ayuno en Ramadán"], "Los cinco: fe, oración, limosna, ayuno, peregrinación.", "religion"],
 ["¿Cuántas veces al día rezan los musulmanes?", "Cinco", ["Una", "Tres", "Siete"], "Mirando hacia La Meca.", "religion"],
 ["¿En qué mes ayunan los musulmanes?", "En Ramadán", ["En Sabbat", "En Navidad", "En Hégira"], "Es el cuarto pilar.", "religion"],
 ["¿Qué tienen prohibido los musulmanes?", "Comer cerdo y beber alcohol", ["Comer pan", "Tener una casa", "Comerciar"], "También los juegos de azar.", "religion"],
 ["¿Cuántas esposas permite el islam como máximo?", "Cuatro", ["Una", "Dos", "Ninguna"], "Se permite la poligamia hasta 4 mujeres.", "religion"],
 ["¿Quién dirige la oración?", "El imán", ["El cadí", "El ulema", "El valí"], "En el islam no hay sacerdotes.", "religion"],
 ["¿Quién interpreta los textos sagrados?", "El ulema", ["El imán", "El almuecín", "El visir"], "Ulema = intérprete.", "religion"],
 ["¿Qué porcentaje de los musulmanes son sunitas?", "El 90 %", ["El 10 %", "El 50 %", "El 30 %"], "Los chiitas son minoría.", "religion"],
 ["Según los chiitas, ¿quién debía ser califa?", "Un descendiente de Mahoma", ["El mejor creyente elegido", "El emperador bizantino", "Un ayatolá cualquiera"], "Los sunitas querían elegirlo.", "religion"],
 ["¿Hacia dónde está orientado el muro de la quibla?", "Hacia La Meca", ["Hacia Jerusalén", "Hacia el norte", "Hacia Medina"], "Los musulmanes rezan mirando a La Meca.", "mezquita"],
 ["¿Qué es el mihrab?", "Un nicho vacío en el muro de la quibla", ["Una torre", "Una fuente", "Un púlpito"], "Suele contener el Corán.", "mezquita"],
 ["¿Qué es el mimbar?", "Un púlpito cerca del mihrab", ["Una torre", "Un patio", "Un libro"], "Desde él se predica.", "mezquita"],
 ["¿Para qué sirve el alminar?", "Para llamar a la oración", ["Para guardar el Corán", "Para purificarse", "Para vigilar la ciudad"], "El almuecín canta desde allí.", "mezquita"],
 ["¿Dónde se purificaban los fieles antes de rezar?", "En la fuente de abluciones del patio", ["En el mihrab", "En el alminar", "En el zoco"], "El patio estaba rodeado de columnas.", "mezquita"],
 ["¿En qué está inspirada la mezquita?", "En la casa de Mahoma en Medina", ["En las iglesias bizantinas", "En los templos romanos", "En los castillos"], "Y su forma cúbica recuerda la Kaaba.", "mezquita"],
 ["¿Qué es la Piedra Negra?", "Una reliquia de la Kaaba: un meteorito", ["La primera piedra de Medina", "Una moneda", "Un tipo de arco"], "Gabriel la dio a Abraham.", "mezquita"],
 ["¿Qué funciones tenía la mezquita además del culto?", "Escuela y lugar de noticias", ["Mercado y almacén", "Cárcel", "Cuartel"], "Así lo dice el resumen (punto 10).", "mezquita"],
 ["¿Hasta dónde llegó el imperio de los califas?", "De la península ibérica a la India", ["De Francia a Rusia", "Solo Arabia", "De Egipto a Grecia"], "Mediante la yihad o guerra santa.", "expansion"],
 ["¿Cómo llegaban al poder los califas ortodoxos?", "Eran elegidos", ["Por herencia", "Por sorteo", "Los nombraba el papa"], "Eran familiares o amigos de Mahoma.", "expansion"],
 ["¿Cuál fue la capital de los omeyas?", "Damasco", ["Bagdad", "La Meca", "Córdoba"], "Procedían de Siria.", "expansion"],
 ["¿Qué etapa fue la de mayor expansión del islam?", "La omeya", ["La de los ortodoxos", "La abasí", "La otomana"], "661–750.", "expansion"],
 ["¿Qué cambió con los omeyas?", "El cargo de califa se hizo hereditario", ["Se eligieron por votación", "Desapareció el califa", "La capital pasó a Medina"], "Y el imperio se dividió en emiratos.", "expansion"],
 ["¿Quién huyó a la península ibérica?", "El príncipe omeya Abderramán", ["Mahoma", "El último califa abasí", "Un ayatolá"], "Fue el único omeya que se salvó.", "expansion"],
 ["¿Cuál fue la capital de los abasíes?", "Bagdad", ["Damasco", "Estambul", "El Cairo"], "750–1258.", "expansion"],
 ["¿Qué etapa fue la de mayor esplendor económico y cultural?", "La abasí", ["La omeya", "La de los ortodoxos", "La mongola"], "Con capital en Bagdad.", "expansion"],
 ["¿Quiénes acabaron con los abasíes en 1258?", "Los mongoles", ["Los turcos", "Los francos", "Los bizantinos"], "Saquearon Bagdad.", "expansion"],
 ["¿Qué pasó en 1453?", "Los turcos otomanos conquistaron Constantinopla", ["Murió Mahoma", "Cayó Bagdad", "Empezó la Hégira"], "La llamaron Estambul.", "expansion"],
 ["¿Por qué se expandió tan rápido el islam?", "Por la fe, la debilidad de los vecinos y los pactos", ["Porque nadie vivía allí", "Por la ayuda de los francos", "Porque tenían cañones"], "Tres causas del punto 15.", "expansion"],
 ["¿Qué tenían que hacer cristianos y judíos para conservar su religión?", "Pagar tributos", ["Hacerse musulmanes", "Irse del imperio", "Servir en el ejército"], "Eran una minoría protegida.", "expansion"],
 ["¿Quiénes eran los visires?", "Consejeros del califa (primer ministro)", ["Gobernadores de provincias", "Jueces", "Tesoreros"], "Ayudaban al califa.", "gobierno"],
 ["¿Quién gobernaba una provincia?", "El valí", ["El visir", "El cadí", "El diwán"], "El emir también podía actuar como valí.", "gobierno"],
 ["¿Qué era el diwán?", "El tesorero real", ["Un juez", "Un libro", "Un tipo de casa"], "Se ocupaba del tesoro.", "gobierno"],
 ["¿Cuál era la lengua oficial del Imperio islámico?", "El árabe", ["El latín", "El griego", "El persa"], "La lengua del Corán.", "gobierno"],
 ["¿Por qué se islamizó la mayoría de la población?", "Por las ventajas económicas y sociales", ["Porque los obligaban siempre", "Porque no había otras religiones", "Por miedo a los mongoles"], "Los musulmanes eran tolerantes.", "gobierno"],
 ["¿En qué se basaba la división social?", "En la riqueza", ["En la religión", "En la edad", "En la estatura"], "Criterio económico.", "gobierno"],
 ["¿Quiénes eran los notables?", "Comerciantes, artesanos con taller y pequeños propietarios", ["Los gobernantes", "Los esclavos", "Los campesinos sin tierra"], "Vivían bien pero sin cargos políticos.", "gobierno"],
 ["¿Podían estudiar las mujeres?", "No: su lugar era la casa", ["Sí, en la madrasa", "Solo medicina", "Solo las ricas"], "Estaban bajo la autoridad del padre o marido.", "gobierno"],
 ["¿Qué era la alhóndiga?", "Almacenes de los comerciantes", ["Una escuela", "Un baño", "Una fortaleza"], "Allí guardaban las mercancías.", "ciudad"],
 ["¿Qué era la madrasa?", "Una escuela", ["Un mercado", "Una torre", "Un almacén"], "Madrasa = escuela.", "ciudad"],
 ["¿Qué había en el centro de la medina?", "La mezquita mayor y el zoco", ["El cementerio", "Las huertas", "Los arrabales"], "Alrededor de la mezquita estaba el mercado.", "ciudad"],
 ["¿Cómo eran las casas?", "Pequeñas, de ladrillo y de dos pisos", ["Grandes y de piedra", "De madera y de un piso", "Tiendas de campaña"], "Con pocos muebles.", "ciudad"],
 ["¿Qué trajeron los musulmanes de India y China?", "Papel, pólvora, brújula y astrolabio", ["Trigo y vino", "La imprenta", "El hierro"], "Los difundieron por su imperio.", "ciencia"],
 ["¿Qué nuevos cultivos introdujeron?", "Arroz, naranja y azafrán", ["Patata y tomate", "Maíz y cacao", "Trigo y olivo"], "La patata y el maíz vinieron de América más tarde.", "ciencia"],
 ["¿Qué inventaron los musulmanes en matemáticas?", "El álgebra", ["La geometría de Euclides", "El ábaco romano", "Los números romanos"], "Y difundieron el uso del cero.", "ciencia"],
 ["¿Qué descubrieron en química?", "El ácido sulfúrico y el nítrico", ["El oxígeno", "La electricidad", "El petróleo"], "Y métodos de destilación del alcohol.", "ciencia"],
 ["¿Qué médicos destacan?", "Avicena y Averroes", ["Hipócrates y Galeno", "Alcuino y Beda", "Tariq y Muza"], "Usaban cirugía y anestesia.", "ciencia"],
 ["¿Qué obra famosa de cuentos escribieron?", "Las mil y una noches", ["La Ilíada", "El Cantar de mio Cid", "Las Etimologías"], "Destacan fábulas y cuentos cortos.", "cultura"],
 ["¿Qué tradujeron al árabe?", "Obras griegas y romanas", ["La Biblia de Gutenberg", "Libros chinos de pólvora", "Nada"], "Así conservaron el saber antiguo.", "cultura"],
 ["¿Qué es la lacería?", "Decoración geométrica", ["Decoración vegetal", "Un tipo de arco", "Una torre"], "El ataurique es la vegetal.", "cultura"],
 ["¿Qué es el ataurique?", "Decoración con motivos vegetales", ["Decoración geométrica", "Una cúpula", "Un azulejo"], "Hojas y tallos.", "cultura"],
 ["¿Qué simbolizaba el agua en el arte islámico?", "La vida en medio del desierto", ["La guerra", "La muerte", "La riqueza del califa"], "Se usaba su sonido y su reflejo.", "cultura"],
]

TF = [
 ["En el siglo VII Arabia estaba rodeada por los imperios persa y bizantino.", True, "Persia al este, Bizancio al norte."],
 ["Los árabes eran monoteístas antes de Mahoma.", False, "Eran politeístas."],
 ["La Meca y Medina estaban a orillas del mar Rojo.", True, "Allí estaban las ciudades más importantes."],
 ["La acequia es un depósito para guardar agua.", False, "La acequia es un canal; el depósito es el aljibe."],
 ["Los beduinos eran árabes nómadas que comerciaban con caravanas.", True, "Por el desierto."],
 ["El dírham era una moneda de oro.", False, "Era de plata; el dinar, de oro; el felús, de cobre."],
 ["Mahoma nació en Medina en el 622.", False, "Nació en La Meca en el 570; en el 622 huyó a Medina."],
 ["La Hégira marca el inicio del calendario musulmán.", True, "Año 622."],
 ["El arcángel Gabriel se apareció a Mahoma en el 610.", True, "En una cueva."],
 ["El islam considera a Mahoma un dios.", False, "Es un profeta; el único dios es Alá."],
 ["El Corán tiene 114 suras escritas en árabe.", True, "Sura = capítulo."],
 ["La sharía está formada por el Corán y la Sunna.", True, "Es la ley sagrada."],
 ["En el islam hay sacerdotes, como en el cristianismo.", False, "No hay sacerdotes; hay imanes, ulemas y cadíes."],
 ["El cadí es un juez.", True, "Aplica la justicia según el Corán."],
 ["El ayuno se hace durante el mes de Ramadán.", True, "Es uno de los cinco pilares."],
 ["Los chiitas son el 90 % de los musulmanes.", False, "El 90 % son sunitas."],
 ["El mihrab está en el muro de la quibla.", True, "Orientado hacia La Meca."],
 ["El almuecín llama a la oración desde el mimbar.", False, "Desde el alminar; el mimbar es el púlpito."],
 ["La Kaaba está en Medina.", False, "Está en La Meca."],
 ["Los califas ortodoxos eran elegidos.", True, "632–661."],
 ["Con los omeyas el cargo de califa se hizo hereditario.", True, "Capital en Damasco."],
 ["La capital de los abasíes fue Damasco.", False, "Fue Bagdad."],
 ["Los mongoles saquearon Bagdad en 1258.", True, "Fin de los abasíes."],
 ["Los turcos otomanos conquistaron Constantinopla en 1453.", True, "La llamaron Estambul."],
 ["Cristianos y judíos tenían que convertirse al islam por obligación.", False, "Podían conservar su religión pagando tributos."],
 ["El árabe fue la lengua oficial del imperio.", True, "La lengua del Corán."],
 ["Los notables tenían cargos políticos importantes.", False, "Vivían bien pero no tenían cargos políticos."],
 ["La madrasa era una escuela.", True, "La alhóndiga, el almacén."],
 ["Los musulmanes inventaron el álgebra.", True, "Y difundieron el cero."],
 ["La arquitectura islámica usaba materiales pobres como ladrillo y yeso.", True, "Cubiertos con mucha decoración."],
]

OPEN = [
 {"q": "¿Cómo era la península arábiga antes del islam y de qué vivían sus habitantes?",
  "a": "En el siglo VII la península arábiga estaba rodeada por los imperios persa y bizantino. Era un territorio árido y desértico entre el mar Rojo, el golfo Pérsico y el Mediterráneo, habitado por pueblos nómadas y pastores organizados en tribus y politeístas; las principales ciudades, La Meca y Medina, estaban junto al mar Rojo. Vivían de la agricultura de regadío junto al mar Rojo y en los oasis (norias, ruedas hidráulicas, acequias, aljibes); de la ganadería nómada de camellos, cabras y ovejas; del comercio de caravanas de los beduinos y de los zocos, con un gran comercio internacional (metales y madera de Europa; esclavos, oro y marfil de África; lujo y especias de Oriente) y monedas como el dinar, el dírham y el felús; y de la artesanía organizada en gremios.",
  "k": ["imperios persa y bizantino", "árida, desértica; tribus nómadas politeístas", "La Meca y Medina", "agricultura de regadío", "ganadería y caravanas de beduinos", "comercio internacional, monedas; gremios"]},
 {"q": "¿Quién fue Mahoma? Explica el origen del islam.",
  "a": "Mahoma nació en La Meca en el 570 en una familia acomodada y era comerciante. En el 610, meditando en una cueva, se le apareció el arcángel Gabriel y le dijo que Alá lo había elegido para predicar una nueva religión monoteísta, el islam. Los habitantes de La Meca no le creyeron y en el 622 huyó a Medina (Hégira), lo que marca el inicio del calendario musulmán. Después de convertir a los habitantes de Medina, reunió un ejército, conquistó La Meca y acabó con el politeísmo; desde allí extendió el islam por Arabia. Murió en el 632.",
  "k": ["570, La Meca, comerciante", "610, arcángel Gabriel", "Alá, islam monoteísta", "622 Hégira a Medina", "calendario musulmán", "conquista La Meca; 632"]},
 {"q": "¿Qué predica el islam? Explica sus libros sagrados y los cinco pilares.",
  "a": "El islam predica que existe un solo dios, Alá, y considera a Mahoma un profeta como Abraham, Moisés o Jesús. Su libro sagrado es el Corán, con 114 suras en árabe que recogen las normas del islam, de la vida privada y las obligaciones de la umma. La Sunna recoge las costumbres del profeta; el Corán y la Sunna forman la sharía. Los cinco pilares son la profesión de fe, la oración cinco veces al día mirando a La Meca, la limosna, el ayuno en el mes de Ramadán y la peregrinación a La Meca. Está prohibido comer cerdo, beber alcohol y los juegos de azar, y se permite la poligamia hasta cuatro mujeres.",
  "k": ["un solo dios, Alá; Mahoma profeta", "Corán: 114 suras", "Sunna y sharía", "fe, oración, limosna", "ayuno (Ramadán), peregrinación", "prohibiciones y poligamia"]},
 {"q": "Describe una mezquita y sus partes con sus funciones.",
  "a": "La mezquita es el lugar de culto de los musulmanes, pero también escuela y lugar de noticias. Tiene un patio rodeado de columnas con la fuente de abluciones, donde los fieles se purifican antes de rezar; una sala de oración cubierta con el muro de la quibla orientado hacia La Meca, en el que hay un nicho vacío, el mihrab, donde suele estar el Corán, y cerca un púlpito o mimbar; y el alminar o minarete, la torre desde donde el almuecín llama a la oración. Está inspirada en la casa de Mahoma en Medina y su forma cúbica recuerda la Kaaba de La Meca.",
  "k": ["culto, escuela, noticias", "patio y fuente de abluciones", "sala de oración", "muro de la quibla, mihrab", "mimbar", "alminar y almuecín"]},
 {"q": "Explica las etapas de los sucesores de Mahoma.",
  "a": "1) Califas ortodoxos (632–661): cuatro califas, familiares o amigos de Mahoma, elegidos, con poder absoluto (autoridad religiosa, juez supremo, general y nombraba los cargos). 2) Dinastía omeya (661–750): de Siria, con capital en Damasco; fue la etapa de mayor expansión, el cargo se hizo hereditario y el imperio se dividió en emiratos; la familia fue asesinada salvo Abderramán, que huyó a la península ibérica. 3) Dinastía abasí (750–1258): capital en Bagdad; época de mayor esplendor económico y cultural; desde el siglo X el imperio se dividió en califatos independientes; terminó cuando los mongoles saquearon Bagdad (1258). Después los turcos otomanos conquistaron Constantinopla en 1453.",
  "k": ["ortodoxos (632–661), elegidos", "omeyas (661–750), Damasco", "mayor expansión, hereditario, emiratos", "Abderramán huye", "abasíes (750–1258), Bagdad, esplendor", "1258 mongoles; 1453 otomanos"]},
 {"q": "¿Por qué se expandió tan rápido el islam tras la muerte de Mahoma?",
  "a": "Por tres motivos: la motivación de los musulmanes por difundir el islam y defender la fe, ya que se prometía el paraíso a quien muriera luchando contra los infieles; la debilidad de los imperios vecinos, el persa y el bizantino; y los pactos con la población: se respetaban su fe y sus propiedades. Cristianos y judíos, monoteístas con la Biblia, eran una minoría protegida que podía conservar su religión, leyes y costumbres a cambio de pagar tributos.",
  "k": ["difundir y defender la fe", "promesa del paraíso", "debilidad de persas y bizantinos", "pactos con la población", "cristianos y judíos protegidos", "tributos"]},
 {"q": "Cita los cargos políticos del Imperio islámico y explica la sociedad.",
  "a": "El califa era la máxima autoridad política y religiosa (ejército, leyes, juez supremo); los visires eran sus consejeros; los cadíes aplicaban la justicia según el Corán; los valíes gobernaban las provincias; los emires eran familiares del califa que gobernaban provincias con poder militar, y el diwán era el tesorero. La sociedad era heterogénea (religiones y etnias distintas) y se dividía según la riqueza: arriba la aristocracia árabe (grandes propietarios y gobernantes); en medio los notables (comerciantes, artesanos con taller y pequeños propietarios), y abajo la mayoría pobre (campesinos sin tierras, artesanos sin taller, vendedores ambulantes y criados). Las mujeres estaban bajo la autoridad del padre o del marido y no podían estudiar.",
  "k": ["califa, visires, cadíes", "valíes, emires, diwán", "sociedad heterogénea, según la riqueza", "aristocracia árabe", "notables", "mayoría pobre; mujeres"]},
 {"q": "¿Cómo era la ciudad islámica?",
  "a": "El centro era la medina, rodeada por una muralla con puertas y con calles estrechas y tortuosas. En el centro estaba la mezquita mayor y a su alrededor el zoco, con tiendas por oficios, y la alcaicería. Había alhóndigas (almacenes de los comerciantes), madrasas (escuelas) y baños. La alcazaba era la fortaleza del gobernador. Fuera de la muralla estaban los arrabales, los cementerios y las huertas. Las casas eran pequeñas, de ladrillo y de dos pisos: abajo se recibía a las visitas y arriba estaban las habitaciones privadas; tenían pocos muebles.",
  "k": ["medina amurallada", "mezquita mayor y zoco", "alhóndiga y madrasa", "alcazaba", "arrabales fuera", "casas de ladrillo, dos pisos"]},
 {"q": "Cita los avances científicos islámicos.",
  "a": "Trajeron de India y China el papel, la pólvora, la brújula y el astrolabio. En agricultura introdujeron la noria y el molino de agua, el regadío por acequias y canales y cultivos como el arroz, la naranja o el azafrán. En astronomía hicieron catálogos de astros y observatorios. En matemáticas difundieron el cero, inventaron el álgebra y perfeccionaron la aritmética y la trigonometría. En medicina usaron técnicas avanzadas de cirugía y anestesia (Avicena, Averroes). En química descubrieron los ácidos sulfúrico y nítrico y la destilación del alcohol.",
  "k": ["papel, pólvora, brújula, astrolabio", "noria, molino, acequias; arroz, naranja, azafrán", "astronomía", "cero y álgebra", "cirugía y anestesia", "química: ácidos, destilación"]},
 {"q": "¿Qué importancia tuvo la cultura y el arte en el Imperio islámico?",
  "a": "La expansión puso a los musulmanes en contacto con otras lenguas y culturas; el árabe fue la lengua común y muchas palabras árabes han llegado hasta hoy. Tradujeron obras griegas y romanas, escribieron libros de viajes, historia y geografía, fábulas, cuentos como Las mil y una noches y poesía, y las bibliotecas guardaban el saber. En arquitectura usaron materiales pobres (ladrillo, yeso) en mezquitas, palacios y madrasas, con arcos de herradura, polilobulados y entrecruzados, cúpulas y techos de madera; decoraban con lacería, ataurique, inscripciones, celosías, azulejos y mocárabes, y usaban el agua como elemento decorativo. También destacaron en cerámica, vidrio, marfil y cuero.",
  "k": ["árabe, palabras árabes", "traducciones griegas y romanas", "Las mil y una noches, bibliotecas", "materiales pobres, arcos, cúpulas", "lacería, ataurique, azulejos, mocárabes", "agua; cerámica, marfil, cuero"]},
]

# ---------- mapas ----------
BYZ, PER, ARA = "#efa94a", "#d9b8e6", "#9ccc65"
SEAS = [["Mar Mediterráneo", 18.0, 34.6], ["Mar Rojo", 38.2, 20.5, 62, 9], ["Golfo Pérsico", 51.3, 27.6, 32, 8.5], ["Mar Arábigo", 63.0, 16.0],
        ["Océano Atlántico", -10.0, 33.0, -70, 9], ["Mar Negro", 34.5, 43.2], ["Mar Caspio", 51.0, 42.0, -75, 8]]
MAPS = [
 {"id": "arabia", "tab": "🗺 1 · Arabia y Mahoma (s. VII)", "title": "La península arábiga en tiempos de Mahoma", "sub": "Fronteras hacia el 630.",
  "vb": _vb(18, 10, 66, 44),
  "layers": [["arab", "Península arábiga", ARA], ["byz600", "Imperio bizantino", BYZ], ["per600", "Imperio persa (sasánida)", PER],
             ["hegira", "La Hégira (622): de La Meca a Medina", "#c62828", "route"]],
  "regions": {**{k: _G[k] for k in ["arab", "byz600", "per600"]}, "hegira": [{"pts": [[39.83, 21.42], [39.3, 23.0], [39.61, 24.47]], "label": "Hégira (622)", "lab": [37.2, 23.4]}]},
  "klabels": [["PENÍNSULA ARÁBIGA", 45.0, 22.5, {"path": [[42.5, 18.6], [47.0, 21.6], [52.5, 20.2]], "fs": 12}],
              ["IMPERIO BIZANTINO", 33.0, 38.6, {"path": [[27.0, 38.4], [32.5, 39.4], [37.5, 38.6]], "fs": 11}],
              ["IMPERIO PERSA", 54.0, 33.0, {"path": [[48.0, 33.6], [54.0, 34.4], [60.0, 33.2]], "fs": 12}]],
  "seas": [["Mar Mediterráneo", 26.0, 34.0]] + SEAS[1:], "rivl": [["Río Nilo", 31.3, 26.0, 75], ["Río Éufrates", 41.0, 34.6, 30], ["Río Tigris", 44.6, 35.4, 50]], "isles": [], "legnote": "",
  "cities": {"La Meca": [39.83, 21.42, "ciudad natal de Mahoma; la Kaaba"], "Medina": [39.61, 24.47, "Mahoma huyó aquí en el 622 (Hégira)"],
             "Jerusalén": [35.23, 31.78, "ciudad santa, en el Imperio bizantino"], "Damasco": [36.29, 33.51, "ciudad bizantina; después capital de los omeyas"],
             "Constantinopla": [28.98, 41.01, "capital del Imperio bizantino"], "Ctesifonte": [44.58, 33.09, "capital del Imperio persa"],
             "Alejandría": [29.92, 31.2, "gran ciudad bizantina de Egipto"]},
  "terrq": [
   {"q": "Toca la península arábiga", "in": ["arab"], "a": "verde: entre el mar Rojo y el golfo Pérsico"},
   {"q": "Toca el Imperio bizantino", "in": ["byz600"], "a": "naranja: al noroeste (Anatolia, Siria, Egipto)"},
   {"q": "Toca el Imperio persa", "in": ["per600"], "a": "malva: al noreste (Irak e Irán)"},
  ],
  "info": "En el siglo VII la <b>península arábiga</b> (verde), árida y desértica, estaba rodeada por el <b>Imperio bizantino</b> (naranja) y el <b>Imperio persa</b> (malva). Las ciudades más importantes, <b>La Meca</b> y <b>Medina</b>, estaban junto al <b>mar Rojo</b>. En el <b>622</b> Mahoma huyó de La Meca a Medina: la <b>Hégira</b>.",
  "ru": "В VII в. Аравийский полуостров (зелёный), засушливый и пустынный, окружали Византийская (оранжевый) и Персидская (сиреневый) империи. Главные города — Мекка и Медина — у Красного моря. В 622 г. Мухаммед бежал из Мекки в Медину — хиджра.",
  "how": "<p>Fronteras de <a href='https://github.com/Seshat-Global-History-Databank/cliopatria' target='_blank' rel='noopener'>Cliopatria</a> (Seshat Global History Databank, licencia CC BY 4.0) para 630–632: Imperio romano de Oriente (bizantino) e Imperio sasánida (persa); la península arábiga es el resto de la península. Cliopatria incluye el Yemen y la costa del golfo en el Imperio persa, que los dominaba en esos años. Fronteras suavizadas sin cambiar su recorrido general; costas y ríos de Natural Earth 1:10m. La línea de la Hégira es aproximada.</p>",
  "how_ru": "<p>Границы — <a href='https://github.com/Seshat-Global-History-Databank/cliopatria' target='_blank' rel='noopener'>Cliopatria</a> (Seshat Global History Databank, CC BY 4.0) на 630–632 гг.: Восточная Римская (Византийская) и Сасанидская (Персидская) империи; Аравия — остальная часть полуострова. Cliopatria относит Йемен и побережье залива к Персии, которая тогда ими владела. Границы сглажены без изменения общего хода; берега и реки — Natural Earth 1:10m. Линия хиджры приблизительная.</p>"},
 {"id": "expansion", "tab": "🗺 2 · La expansión del islam", "title": "La expansión del islam (632–750)", "sub": "De Arabia a la península ibérica y la India.",
  "vb": _vb(-11, 12, 80, 49),
  "layers": [["e632", "A la muerte de Mahoma (632)", "#2e7d32"], ["e661", "Conquistas de los califas ortodoxos (632–661)", "#7cb342"],
             ["e750", "Conquistas de los omeyas (661–750)", "#c5e1a5"], ["byz720", "Imperio bizantino", BYZ], ["fra720", "Reino de los francos", "#f2c9de"],
             ["frenos", "Batallas que frenaron el avance", "#b71c1c", "route"]],
  "regions": {**{k: _G[k] for k in ["e632", "e661", "e750", "byz720", "fra720", "all750"]},
   "frenos": [{"pts": [[-1.0, 44.2], [0.0, 45.6], [0.34, 46.5]], "label": "732", "lab": [-1.9, 45.2]},
              {"pts": [[31.5, 39.8], [30.0, 40.6], [29.1, 40.95]], "label": "717–718", "lab": [31.6, 38.9]}]},
  "klabels": [["ARABIA", 48.0, 21.0, {"fs": 11}], ["OMEYAS", 10.0, 30.0, {"path": [[-2.0, 30.3], [8.0, 31.6], [18.0, 29.8]], "fs": 13}]],
  "seas": SEAS, "rivl": [["Río Indo", 69.0, 27.5, -60], ["Río Nilo", 31.3, 26.0, 75]], "isles": [], "legnote": "",
  "cities": {"La Meca": [39.83, 21.42, "origen del islam"], "Medina": [39.61, 24.47, "ciudad de la Hégira"], "Damasco": [36.29, 33.51, "capital de los omeyas (661–750)"],
             "Bagdad": [44.36, 33.31, "capital de los abasíes (desde el 750)"], "Jerusalén": [35.23, 31.78, "ciudad santa"], "Córdoba": [-4.78, 37.89, "capital de al-Ándalus"],
             "Kairuán": [10.1, 35.68, "gran ciudad musulmana del norte de África"], "El Cairo": [31.24, 30.04, "ciudad de Egipto"], "Samarcanda": [66.97, 39.65, "ciudad de Asia central, en la frontera oriental de los omeyas"],
             "Constantinopla": [28.98, 41.01, "capital bizantina; resistió a los musulmanes; turca desde 1453 (Estambul)"], "Poitiers": [0.34, 46.58, "batalla del 732"]},
  "terrq": [
   {"q": "Toca el territorio musulmán a la muerte de Mahoma (632)", "in": ["e632"], "a": "verde oscuro: la península arábiga"},
   {"q": "Toca una conquista de los califas ortodoxos (632–661)", "in": ["e661"], "a": "verde medio: Siria, Egipto, Irak e Irán"},
   {"q": "Toca una conquista de los omeyas (661–750)", "in": ["e750"], "a": "verde claro: norte de África, península ibérica, Asia central e Indo"},
   {"q": "Toca el imperio que resistió en Constantinopla", "in": ["byz720"], "a": "naranja: el Imperio bizantino"},
   {"q": "Toca el reino que frenó a los musulmanes en Poitiers", "in": ["fra720"], "a": "rosa: el reino de los francos"},
  ],
  "info": "A la <b>muerte de Mahoma (632)</b> gran parte de Arabia era musulmana (verde oscuro). Los <b>califas ortodoxos (632–661)</b> conquistaron Siria, Egipto, Irak e Irán (verde medio). Los <b>omeyas (661–750)</b>, con capital en <b>Damasco</b>, llegaron al norte de África, la <b>península ibérica</b> (711), Asia central y el <b>Indo</b> (verde claro). Los frenaron los bizantinos en <b>Constantinopla</b> y los francos en <b>Poitiers (732)</b>. Desde el 750 los <b>abasíes</b> gobernaron desde <b>Bagdad</b>.",
  "ru": "К смерти Мухаммеда (632) большая часть Аравии была мусульманской (тёмно-зелёный). Праведные халифы (632–661) завоевали Сирию, Египет, Ирак и Иран (средне-зелёный). Омейяды (661–750, столица Дамаск) дошли до Северной Африки, Испании (711), Средней Азии и Инда (светло-зелёный). Их остановили византийцы у Константинополя и франки при Пуатье (732). С 750 г. Аббасиды правили из Багдада.",
  "how": "<p>Fronteras de <a href='https://github.com/Seshat-Global-History-Databank/cliopatria' target='_blank' rel='noopener'>Cliopatria</a> (CC BY 4.0): califato Rashidun en 633 (≈ la Arabia de 632) y en 656–660, califato omeya en 718–723 (su máxima extensión, sin una franja de Anatolia que solo eran incursiones), Imperio bizantino y reino de los francos en 718–723. Fronteras suavizadas; costas y ríos de Natural Earth 1:10m.</p>",
  "how_ru": "<p>Границы — <a href='https://github.com/Seshat-Global-History-Databank/cliopatria' target='_blank' rel='noopener'>Cliopatria</a> (CC BY 4.0): Праведный халифат в 633 г. (≈ Аравия 632 г.) и в 656–660 гг., Омейядский халифат в 718–723 гг. (наибольшая площадь, без полосы в Анатолии — это были лишь набеги), Византия и королевство франков в 718–723 гг. Границы сглажены; берега и реки — Natural Earth 1:10m.</p>"},
]

# ---------- mini-mapas ----------
_AR = _vb(30, 12, 62, 38)
MINIMAPS = {
 "arabia": {"vb": _vb(20, 10, 64, 44),
  "regs": [[_G["arab"], ARA, .85], [_G["byz600"], BYZ, .8], [_G["per600"], PER, .85]],
  "labels": [["IMPERIO BIZANTINO", 31.5, 39.0, "big"], ["IMPERIO PERSA", 54.0, 33.5, "big"], ["ARABIA", 45.0, 23.0, "big"], ["mar Rojo", 38.3, 20.2, "sea", 62], ["golfo Pérsico", 51.4, 27.5, "sea", 32]],
  "pts": [["La Meca", 39.83, 21.42, "w"], ["Medina", 39.61, 24.47, "w"]],
  "leg": [[ARA, "Península arábiga"], [BYZ, "Imperio bizantino"], [PER, "Imperio persa"]],
  "cap": "Arabia, árida y desértica, entre el <b>mar Rojo</b> y el <b>golfo Pérsico</b>, rodeada por los imperios <b>bizantino</b> y <b>persa</b>.",
  "cap_ru": "Аравия — пустыня между Красным морем и Персидским заливом, окружённая Византийской и Персидской империями."},
 "economia": {"vb": _vb(-6, 0, 80, 47),
  "regs": [[_G["arab"], ARA, .85]],
  "lines": [{"pts": [[12.0, 44.0], [25.0, 38.0], [34.0, 31.5], [38.5, 26.0]], "col": "#5d4037", "label": "metales, madera", "lab": [13.0, 41.0]},
            {"pts": [[30.0, 8.0], [36.0, 14.0], [39.0, 19.0]], "col": "#795548", "label": "esclavos, oro, marfil", "lab": [26.0, 11.0]},
            {"pts": [[76.0, 14.0], [66.0, 18.0], [58.0, 20.0], [52.0, 22.0]], "col": "#e65100", "label": "lujo y especias", "lab": [70.0, 20.5]}],
  "labels": [["ARABIA", 45.0, 23.0, "big"], ["caravanas", 45.0, 26.8, "note"]],
  "pts": [["La Meca", 39.83, 21.42, "w"]],
  "cap": "Rutas del comercio árabe: de <b>Europa</b> llegaban metales y madera; de <b>África</b>, esclavos, oro y marfil; de <b>Oriente</b>, productos de lujo y especias.",
  "cap_ru": "Торговые пути арабов: из Европы — металлы и дерево, из Африки — рабы, золото, слоновая кость, с Востока — роскошь и пряности."},
 "mahoma": {"vb": _vb(31, 18.5, 50, 26.5),
  "regs": [[_G["arab"], ARA, .6]],
  "lines": [{"pts": [[39.83, 21.42], [39.25, 23.0], [39.61, 24.47]], "col": "#c62828", "label": "Hégira (622)", "lab": [37.6, 23.1]},
            {"pts": [[40.0, 24.3], [40.6, 23.0], [40.05, 21.6]], "col": "#1565c0", "label": "conquista de La Meca", "lab": [42.6, 22.8], "dash": 1}],
  "pts": [["La Meca (570, 610)", 39.83, 21.42], ["Medina", 39.61, 24.47]],
  "labels": [["mar Rojo", 37.5, 21.0, "sea", 62]],
  "cap": "Mahoma nació en <b>La Meca</b>; en el <b>622</b> huyó a <b>Medina</b> (Hégira) y después volvió para conquistar La Meca.",
  "cap_ru": "Мухаммед родился в Мекке, в 622 г. бежал в Медину (хиджра), а затем вернулся и взял Мекку."},
 "expansion": {"vb": _vb(-11, 12, 78, 49),
  "regs": [[_G["e632"], "#2e7d32", .9], [_G["e661"], "#7cb342", .9], [_G["e750"], "#c5e1a5", .95]],
  "pts": [["Damasco", 36.29, 33.51, "w"], ["Bagdad", 44.36, 33.31], ["Córdoba", -4.78, 37.89, "s"]],
  "labels": [["632", 45.0, 22.5, "big"], ["632–661", 50.0, 33.0, "big"], ["661–750", 5.0, 30.5, "big"], ["661–750", 66.0, 33.0, "big"]],
  "leg": [["#2e7d32", "Hasta el 632 (Mahoma)"], ["#7cb342", "Califas ortodoxos (632–661)"], ["#c5e1a5", "Omeyas (661–750)"]],
  "cap": "En un siglo el islam se extendió <b>desde la península ibérica hasta la India</b>. Capitales: <b>Damasco</b> (omeyas) y <b>Bagdad</b> (abasíes).",
  "cap_ru": "За сто лет ислам распространился от Испании до Индии. Столицы: Дамаск (Омейяды) и Багдад (Аббасиды)."},
 "gobierno": {"vb": _vb(-11, 12, 78, 49),
  "regs": [[_G["abb800"], "#7cb342", .85], [_G["ind800"], "#dce775", .9], [_G["byz800"], BYZ, .7]],
  "pts": [["Bagdad", 44.36, 33.31], ["Córdoba", -4.78, 37.89, "s"]],
  "labels": [["CALIFATO ABASÍ (hacia el 800)", 50.0, 37.5, "big"], ["independientes", -1.0, 33.5, "note"]],
  "leg": [["#7cb342", "Califato abasí"], ["#dce775", "Territorios ya independientes (al-Ándalus, norte de África)"]],
  "cap": "Hacia el 800 el califa abasí gobernaba desde <b>Bagdad</b> con visires, cadíes, valíes y emires; al-Ándalus y parte del norte de África ya eran <b>independientes</b>.",
  "cap_ru": "Около 800 г. халиф Аббасидов правил из Багдада с визирями, кади, вали и эмирами; аль-Андалус и часть Северной Африки уже были независимы."},
}
for _s in SECTIONS:
    if _s["id"] in MINIMAPS: _s["map"] = MINIMAPS[_s["id"]]

# ---------- esquemas ----------
_MZ = """<svg viewBox="0 0 420 250" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,sans-serif" font-size="11">
<rect x="10" y="30" width="400" height="200" fill="#f5efe3" stroke="#8d6e63" stroke-width="2"/>
<rect x="10" y="30" width="170" height="200" fill="#fdf9f0" stroke="#8d6e63" stroke-width="2"/>
<g fill="#a1887f">""" + ''.join(f'<circle cx="{x}" cy="{y}" r="2.6"/>' for x in range(22, 175, 16) for y in (42, 218)) + ''.join(f'<circle cx="{x}" cy="{y}" r="2.6"/>' for x in (22, 168) for y in range(58, 210, 16)) + """</g>
<g fill="#8d6e63">""" + ''.join(f'<circle cx="{x}" cy="{y}" r="3"/>' for x in range(200, 395, 22) for y in range(48, 220, 22)) + """</g>
<circle cx="95" cy="130" r="16" fill="#90caf9" stroke="#1e88e5" stroke-width="2"/>
<rect x="404" y="30" width="6" height="200" fill="#6d4c41"/>
<path d="M404 115 h-14 a8 8 0 0 0 0 30 h14z" fill="#ffcc80" stroke="#e65100" stroke-width="1.5"/>
<path d="M388 155 l-14 0 l0 14 l14 0z" fill="#bcaaa4" stroke="#5d4037"/>
<rect x="0" y="0" width="36" height="36" fill="#d7ccc8" stroke="#5d4037" stroke-width="2"/>
<g font-weight="800" fill="#fff">
<circle cx="95" cy="80" r="10" fill="#5e35b1"/><text x="95" y="84" text-anchor="middle">1</text>
<circle cx="95" cy="160" r="10" fill="#5e35b1"/><text x="95" y="164" text-anchor="middle">2</text>
<circle cx="290" cy="20" r="10" fill="#5e35b1"/><text x="290" y="24" text-anchor="middle">3</text>
<circle cx="398" cy="244" r="0"/><circle cx="380" cy="100" r="10" fill="#5e35b1"/><text x="380" y="104" text-anchor="middle">4</text>
<circle cx="372" cy="130" r="10" fill="#5e35b1"/><text x="372" y="134" text-anchor="middle">5</text>
<circle cx="360" cy="180" r="10" fill="#5e35b1"/><text x="360" y="184" text-anchor="middle">6</text>
<circle cx="18" cy="18" r="10" fill="#5e35b1"/><text x="18" y="22" text-anchor="middle">7</text>
</g>
<text x="300" y="246" text-anchor="middle" fill="#6d4c41" font-weight="700">sala de oración</text>
<text x="95" y="246" text-anchor="middle" fill="#6d4c41" font-weight="700">patio</text>
<text x="412" y="22" text-anchor="end" fill="#c62828" font-weight="800">La Meca →</text>
</svg>"""
_CI = """<svg viewBox="0 0 420 270" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,sans-serif" font-size="11">
<rect width="420" height="270" fill="#eef3e2"/>
<path d="M70 60 Q150 25 250 40 Q340 50 360 120 Q370 200 290 230 Q190 255 110 225 Q50 195 55 130 Z" fill="#f6eedd" stroke="#6d4c41" stroke-width="5"/>
<path d="M120 80 L160 150 L230 120 L300 170 M100 170 L160 150 L190 220 M230 120 L250 60" stroke="#d7ccc8" stroke-width="5" fill="none"/>
<rect x="175" y="120" width="44" height="34" fill="#c5e1a5" stroke="#33691e" stroke-width="2"/><rect x="214" y="112" width="7" height="12" fill="#33691e"/>
<rect x="150" y="160" width="80" height="14" fill="#ffe082" stroke="#ff8f00"/>
<rect x="230" y="135" width="30" height="20" fill="#ffccbc" stroke="#d84315"/>
<rect x="120" y="110" width="32" height="22" fill="#b3e5fc" stroke="#0277bd"/>
<rect x="250" y="180" width="34" height="22" fill="#d1c4e9" stroke="#4527a0"/>
<rect x="130" y="185" width="30" height="20" fill="#b2dfdb" stroke="#00695c"/>
<path d="M300 60 h50 v45 h-50z" fill="#bcaaa4" stroke="#3e2723" stroke-width="3"/>
<g fill="#e0d6c4" stroke="#8d6e63">""" + ''.join(f'<rect x="{x}" y="{y}" width="16" height="12"/>' for x, y in [(20, 120), (22, 140), (24, 160), (380, 150), (378, 170), (382, 190)]) + """</g>
<g fill="#9e9e9e">""" + ''.join(f'<path d="M{x} {y} v-8 m-3 3 h6"/>'.replace('fill', 'x') for x, y in []) + """</g>
<g stroke="#757575" stroke-width="1.5">""" + ''.join(f'<path d="M{x} {y} v-9 M{x-3} {y-6} h6"/>' for x, y in [(160, 262), (175, 262), (190, 262), (205, 262)]) + """</g>
<g font-weight="800" fill="#fff">
<circle cx="200" cy="100" r="10" fill="#5e35b1"/><text x="200" y="104" text-anchor="middle">1</text>
<circle cx="190" cy="167" r="10" fill="#5e35b1"/><text x="190" y="171" text-anchor="middle">2</text>
<circle cx="245" cy="145" r="10" fill="#5e35b1"/><text x="245" y="149" text-anchor="middle">3</text>
<circle cx="136" cy="121" r="10" fill="#5e35b1"/><text x="136" y="125" text-anchor="middle">4</text>
<circle cx="267" cy="191" r="10" fill="#5e35b1"/><text x="267" y="195" text-anchor="middle">5</text>
<circle cx="145" cy="195" r="10" fill="#5e35b1"/><text x="145" y="199" text-anchor="middle">6</text>
<circle cx="325" cy="82" r="10" fill="#5e35b1"/><text x="325" y="86" text-anchor="middle">7</text>
<circle cx="80" cy="44" r="10" fill="#5e35b1"/><text x="80" y="48" text-anchor="middle">8</text>
<circle cx="32" cy="104" r="10" fill="#5e35b1"/><text x="32" y="108" text-anchor="middle">9</text>
<circle cx="230" cy="256" r="10" fill="#5e35b1"/><text x="230" y="260" text-anchor="middle">10</text>
</g></svg>"""
MEDIA = {
 "religion": [{"dia": "org", "title": ["Los cinco pilares del islam", "Пять столпов ислама"],
   "rows": [[["1 · Profesión de fe", "1 · Исповедание веры"], ["2 · Oración (5 veces al día)", "2 · Молитва (5 раз в день)"], ["3 · Limosna", "3 · Милостыня"],
             ["4 · Ayuno en Ramadán", "4 · Пост в Рамадан"], ["5 · Peregrinación a La Meca", "5 · Паломничество в Мекку"]]],
   "note": ["Prohibido: cerdo, alcohol y juegos de azar. Se permite la poligamia (máximo 4 mujeres).", "Запрещено: свинина, алкоголь, азартные игры. Многожёнство — до 4 жён."]}],
 "mezquita": [{"dia": "svg", "title": ["Las partes de la mezquita (planta)", "Части мечети (план)"], "svg": _MZ,
   "items": [["Patio con columnas", "Двор с колоннами"], ["Fuente de abluciones: purificarse antes de rezar", "Фонтан для омовений"],
             ["Sala de oración cubierta", "Молитвенный зал"], ["Muro de la quibla, hacia La Meca", "Стена киблы — к Мекке"],
             ["Mihrab: nicho vacío (el Corán)", "Михраб: пустая ниша (Коран)"], ["Mimbar: púlpito", "Минбар: кафедра"],
             ["Alminar: el almuecín llama a la oración", "Минарет: муэдзин зовёт на молитву"]]}],
 "expansion": [{"dia": "phases", "title": ["Los califas después de Mahoma", "Халифы после Мухаммеда"], "from": 632, "to": 1258,
   "items": [[["Ort.", "Пр."], 632, 661, "#2e7d32"], [["Omeyas (Damasco)", "Омейяды (Дамаск)"], 661, 750, "#7cb342"], [["Abasíes (Bagdad)", "Аббасиды (Багдад)"], 750, 1258, "#aed581"]],
   "marks": [[632, "632"], [700, "661"], [750, "750"], [1258, "1258"]],
   "note": ["Ort. = califas ortodoxos (632–661), elegidos.", "Пр. — праведные халифы (632–661), выборные."]}],
 "gobierno": [{"dia": "pyr", "title": ["La sociedad islámica (según la riqueza)", "Исламское общество (по богатству)"], "apex": ["Califa", "Халиф"],
   "levels": [["1º Aristocracia árabe: gobernantes y grandes propietarios", "1) Арабская аристократия"], ["2º Notables: comerciantes, artesanos con taller, pequeños propietarios", "2) Знатные горожане"],
              ["3º Mayoría pobre: campesinos sin tierra, artesanos sin taller, vendedores, criados", "3) Бедное большинство"]]}],
 "ciudad": [{"dia": "svg", "title": ["La ciudad islámica (esquema)", "Исламский город (схема)"], "svg": _CI,
   "items": [["Mezquita mayor", "Главная мечеть"], ["Zoco: tiendas por oficios", "Сук: лавки по ремёслам"], ["Alcaicería: productos de lujo", "Алькайсерия: роскошь"],
             ["Madrasa: escuela", "Медресе: школа"], ["Alhóndiga: almacenes", "Альондига: склады"], ["Baños públicos", "Бани"],
             ["Alcazaba: fortaleza", "Алькасаба: крепость"], ["Muralla de la medina", "Стена медины"], ["Arrabales (fuera de la muralla)", "Пригороды за стеной"], ["Cementerio", "Кладбище"]],
   "note": ["Esquema general, como el del libro.", "Общая схема, как в учебнике."]}],
}
from mm import photo as _ph
MEDIA["religion"].insert(0, _ph("isl/coran-azul", "Página del <b>Corán azul</b> (siglos IX–X), escrito en <b>árabe</b> con letras de oro.", "Страница «Синего Корана» (IX–X вв.), арабский текст золотом."))
MEDIA["mezquita"] += [_ph("isl/kaaba", "La <b>Kaaba</b> de La Meca durante la peregrinación: el lugar más sagrado del islam.", "Кааба в Мекке во время паломничества — главная святыня ислама."),
                      _ph("isl/mihrab", "<b>Mihrab</b> de la Mezquita de Córdoba, en el muro de la quibla.", "Михраб Кордовской мечети в стене киблы."),
                      _ph("isl/kairuan", "<b>Alminar</b> de la Gran Mezquita de Kairuán (Túnez), uno de los más antiguos.", "Минарет Большой мечети Кайруана (Тунис), один из древнейших.")]
MEDIA["expansion"].append(_ph("isl/cupula-roca", "<b>Cúpula de la Roca</b> en Jerusalén, construida por los <b>omeyas</b> (691).", "Купол Скалы в Иерусалиме, построен Омейядами (691)."))
MEDIA["ciencia"] = [_ph("isl/astrolabio", "<b>Astrolabio</b> de latón: medía la altura de los astros para orientarse.", "Латунная астролябия: измеряла высоту светил для ориентирования.", tall=True),
                    _ph("isl/noria", "<b>Noria</b> de la Albolafia (Córdoba), junto al Guadalquivir.", "Нория Альболафия (Кордова) на Гвадалквивире.", tall=True)]
MEDIA["cultura"] = [_ph("and/mezquita", "Arcos de <b>herradura</b> de la Mezquita de Córdoba, de ladrillo y piedra.", "Подковообразные арки Кордовской мечети."),
                    _ph("and/alhambra-cupula", "<b>Mocárabes</b> de yeso en un techo de la Alhambra.", "Гипсовые мукарны на потолке Альгамбры.")]
for _s in SECTIONS:
    if _s["id"] in MEDIA: _s["media"] = MEDIA[_s["id"]]
