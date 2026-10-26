# Mapas mudos

🌐 **Sitio / Сайт / Site:** https://slider007.github.io/mapas-mudos/

[Español](#español) · [Русский](#русский) · [English](#english)

---

## Español

Mapas mudos interactivos para las clases de geografía: localizar, nombrar, repetir y hacer un «examen». Son sitios estáticos (sin servidor, sin dependencias, sin compilación) que funcionan en GitHub Pages. El progreso del alumno se guarda solo en el navegador (`localStorage`, claves `mme_*`); no se envía ningún dato.

| Lección | Carpeta | Tema | Estado |
|---|---|---|---|
| 1 | `espana-administrativa/` | División administrativa de España | en preparación |
| 2 | `espana-fisica/` | España física: costa, ríos, relieve (178 objetos) | listo |
| 3 | `europa-politica/` | Europa política: países y capitales (prueba 4 nov) | listo |
| 4 | `europa-fisica/` | Europa física: costas, ríos, lagos y relieve (prueba 25 nov) | listo |
| Historia T1 | `historia-tema1/` | Fin de la Edad Antigua e inicio de la Edad Media: germanos y visigodos, bizantinos, carolingios (3 pruebas) | listo |
| Historia T1 · parte 1 | `historia-visigodos/` | Entrenador: pueblos germanos y visigodos (teoría, fechas, 3 mapas del libro, pirámide, tarjetas, test, examen) | listo |
| Historia T1 · parte 2 | `historia-bizancio/` | Entrenador: el Imperio bizantino (teoría, fechas, mapa del libro, pirámide, tarjetas, test, examen) | listo |
| Historia T1 · parte 3 | `historia-carolingios/` | Entrenador: los carolingios (prueba 30 oct) | listo |
| Historia T1 · recursos | `historia-recursos/` | PDF para imprimir: mapas mudos, línea del tiempo, plantillas del cuaderno y de trabajos | listo |
| Historia T2 · al-Ándalus | `historia-al-andalus/` | Entrenador: al-Ándalus (teoría, fechas, 5 mapas, pirámide social, tarjetas, test, examen) | listo |
| Historia T2 · el islam | `historia-islam/` | Entrenador: el islam (teoría, fechas, 2 mapas, esquemas de la mezquita y la ciudad, pirámide, tarjetas, test, examen) | listo |

Cada lección es una carpeta con `index.html`, `img/` y `pdf/` (mapa mudo para imprimir y mapa físico del IGN). La página `index.html` de la raíz enumera las lecciones. La carpeta `tools/` contiene los scripts, datos y la plantilla con que se construyó la lección 2 (véase `tools/README.md`).

### Fuentes de datos
- Costa e islas de España: IGN / CNIG (Líneas Límite), a través de AlexGPlay/SpainLayers
- Ríos, cumbres, cordilleras: © OpenStreetMap contributors (ODbL)
- Países vecinos, batimetría, nombres de mares: Natural Earth (dominio público)
- Relieve: Copernicus DEM GLO-90 (ESA)
- Fondo «Mapa físico de España 1:3 000 000», PDF: © Instituto Geográfico Nacional / CNIG
- Costas, lagos y ríos de los entrenadores de historia: Natural Earth 1:10m (github.com/nvkelso/natural-earth-vector)
- Fronteras históricas de `historia-tema1/`: [aourednik/historical-basemaps](https://github.com/aourednik/historical-basemaps), licencia GPL-3.0 (fronteras aproximadas)
- Mapa de Bizancio (527 y conquistas de Justiniano): [Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria), Seshat Global History Databank, licencia CC BY 4.0; 1025, 1204 y 1453: según el mapa 18 del libro de texto
- Mapas de los carolingios (reino franco en 768, Imperio en 814, Tratado de Verdún): [Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria), CC BY 4.0, organizados como los mapas 12 y 14 del libro; marcas aproximadas
- Mapas de al-Ándalus (conquista hacia 720, califato hacia 1000, taifas hacia 1050, almohades hacia 1200, reino nazarí hacia 1400): [Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria), CC BY 4.0, recortado a la península con Natural Earth; se genera con `tools/historia/andalus_geo.py`
- Mapas del islam (Arabia hacia 630, expansión 632–750, abasíes hacia 800): Cliopatria, CC BY 4.0; base de costas y ríos de Natural Earth 1:10m en otra proyección (`tools/historia/geo_islam.py`, `islam_geo.py`)
- Fotos de los entrenadores de historia: Wikimedia Commons (dominio público, CC0, CC BY o CC BY-SA); autor y licencia bajo cada foto y en `tools/historia/fotos.json`
- Europa política y física: Natural Earth 1:10m (países desde el punto de vista de España; Kosovo de la versión general). Relieve de Europa: Mapzen/AWS Terrain Tiles (SRTM, GMTED, ETOPO). Golfos, estrechos, cabos y península Itálica: © OpenStreetMap contributors (Nominatim, ODbL). Meseta, Béticas, Bohemia y Gran Llanura Europea: calculadas a partir de las altitudes (cuencas y alturas, `regions_dem.py`). Scripts en `tools/europa/` y `tools/europa_fisica/`
- Fondos 🗺 en Europa física y Europa política: «Mapa físico de Europa» y «Mapa político de Europa» (Atlas Nacional de España, 2025), © Instituto Geográfico Nacional / CNIG; georreferenciados (cónica de Lambert ajustada a 32 capitales del mapa político; los dos mapas tienen la misma maquetación) y reproyectados con `tools/ign/ign_warp.py`; solo se muestran en «Estudiar» porque llevan los nombres

### Licencia
- Código (`tools/`, HTML/JS): **MIT**, véase [`LICENSE`](LICENSE).
- Contenido (mapas, imágenes, PDF, datos): **CC BY-SA 4.0**, véase [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md). Los datos de terceros conservan sus condiciones; hay que citar las fuentes.

---

## Русский

Интерактивные контурные карты для школьных уроков географии: найти, назвать, повторить, сдать «экзамен». Статические сайты (без сервера, зависимостей и сборки), работают на GitHub Pages. Прогресс ученика хранится только в браузере (`localStorage`, ключи `mme_*`), никакие данные никуда не отправляются.

| Урок | Папка | Тема | Статус |
|---|---|---|---|
| 1 | `espana-administrativa/` | Административное деление Испании | в работе |
| 2 | `espana-fisica/` | Физическая карта Испании: побережье, реки, рельеф (178 объектов) | готово |
| 3 | `europa-politica/` | Политическая карта Европы: страны и столицы (проверочная 4 нояб) | готов |
| 4 | `europa-fisica/` | Физическая карта Европы: берега, реки, озёра, рельеф (проверочная 25 нояб) | готов |
| История, тема 1 | `historia-tema1/` | Конец Античности и начало Средневековья: германцы и вестготы, Византия, Каролинги (3 проверочные) | готово |
| История, тема 1 · часть 1 | `historia-visigodos/` | Тренажёр: германцы и вестготы (материал, даты, 3 карты из учебника, пирамида, карточки, тест, экзамен) | готово |
| История, тема 1 · часть 2 | `historia-bizancio/` | Тренажёр: Византия (материал, даты, карта из учебника, пирамида, карточки, тест, экзамен) | готово |
| История, тема 1 · часть 3 | `historia-carolingios/` | Тренажёр: Каролинги (проверочная 30 окт) | готов |
| История, тема 1 · материалы | `historia-recursos/` | PDF для печати: контурные карты, линия времени, шаблоны тетради и работы | готово |
| История, тема 2 · аль-Андалус | `historia-al-andalus/` | Тренажёр: аль-Андалус (материал, даты, 5 карт, пирамида общества, карточки, тест, экзамен) | готов |
| История, тема 2 · ислам | `historia-islam/` | Тренажёр: ислам (материал, даты, 2 карты, схемы мечети и города, пирамида, карточки, тест, экзамен) | готов |

Каждый урок это папка с `index.html`, `img/` и `pdf/` (контурная карта для печати и физическая карта IGN). Корневой `index.html` содержит список уроков. В `tools/` лежат скрипты, данные и шаблон, из которых собран урок 2 (см. `tools/README.md`).

### Источники данных
- Береговая линия и острова Испании: IGN / CNIG (Líneas Límite), через репозиторий AlexGPlay/SpainLayers
- Реки, вершины, хребты: © OpenStreetMap contributors (ODbL)
- Соседние страны, глубины моря, названия акваторий: Natural Earth (public domain)
- Рельеф: Copernicus DEM GLO-90 (ESA)
- Подложка «Mapa físico de España 1:3 000 000», PDF: © Instituto Geográfico Nacional / CNIG
- Берега, озёра и реки в тренажёрах по истории: Natural Earth 1:10m (github.com/nvkelso/natural-earth-vector)
- Исторические границы в `historia-tema1/`: [aourednik/historical-basemaps](https://github.com/aourednik/historical-basemaps), лицензия GPL-3.0 (границы приблизительные)
- Карта Византии (527 г. и завоевания Юстиниана): [Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria), Seshat Global History Databank, лицензия CC BY 4.0; 1025, 1204 и 1453 гг. — по карте 18 учебника
- Карты Каролингов (королевство франков в 768 г., империя в 814 г., Верденский договор): [Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria), CC BY 4.0, устроены как карты 12 и 14 учебника; марки приблизительные
- Карты аль-Андалуса (завоевание ок. 720, халифат ок. 1000, тайфы ок. 1050, альмохады ок. 1200, Насриды ок. 1400): [Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria), CC BY 4.0, обрезка по полуострову — Natural Earth; собирается `tools/historia/andalus_geo.py`
- Карты ислама (Аравия ок. 630, расширение 632–750, Аббасиды ок. 800): Cliopatria, CC BY 4.0; основа (берега, реки) — Natural Earth 1:10m в своей проекции (`tools/historia/geo_islam.py`, `islam_geo.py`)
- Фото в тренажёрах по истории: Wikimedia Commons (общественное достояние, CC0, CC BY или CC BY-SA); автор и лицензия под каждым фото и в `tools/historia/fotos.json`
- Политическая и физическая карта Европы: Natural Earth 1:10m (страны с точки зрения Испании; Косово из общей версии). Рельеф Европы: Mapzen/AWS Terrain Tiles (SRTM, GMTED, ETOPO). Заливы, проливы, мысы и Апеннинский полуостров: © OpenStreetMap contributors (Nominatim, ODbL). Месета, Бетские горы, Богемия и Великая Европейская равнина рассчитаны по данным высот (бассейны рек и высоты, `regions_dem.py`). Скрипты в `tools/europa/` и `tools/europa_fisica/`
- Подложки 🗺 в «Europa física» и «Europa política»: «Mapa físico de Europa» и «Mapa político de Europa» (Национальный атлас Испании, 2025), © Instituto Geográfico Nacional / CNIG; привязаны (коническая Ламберта по 32 столицам политического листа; оба листа свёрстаны одинаково) и перепроецированы `tools/ign/ign_warp.py`; видны только в «Estudiar», потому что на них подписаны названия

### Лицензия
- Код (`tools/`, HTML/JS): **MIT**, см. [`LICENSE`](LICENSE).
- Контент (карты, изображения, PDF, данные): **CC BY-SA 4.0**, см. [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md). Данные третьих лиц сохраняют свои условия; источники нужно указывать.

---

## English

Interactive blank (outline) maps for school geography lessons: locate, name, review and take a quiz. Static sites (no server, no dependencies, no build step) hosted on GitHub Pages. Student progress is stored only in the browser (`localStorage`, keys `mme_*`); no data is sent anywhere.

| Lesson | Folder | Topic | Status |
|---|---|---|---|
| 1 | `espana-administrativa/` | Administrative divisions of Spain | in progress |
| 2 | `espana-fisica/` | Physical map of Spain: coast, rivers, relief (178 objects) | ready |
| 3 | `europa-politica/` | Political map of Europe: countries and capitals (quiz 4 Nov) | ready |
| 4 | `europa-fisica/` | Physical map of Europe: coasts, rivers, lakes and relief (quiz 25 Nov) | ready |
| History, topic 1 | `historia-tema1/` | End of Antiquity and start of the Middle Ages: Germanic peoples and Visigoths, Byzantium, Carolingians (3 quizzes) | ready |
| History T1 · part 1 | `historia-visigodos/` | Trainer: Germanic peoples and Visigoths (theory, dates, 3 textbook maps, pyramid, flashcards, test, exam) | ready |
| History T1 · part 2 | `historia-bizancio/` | Trainer: the Byzantine Empire (theory, dates, textbook map, pyramid, flashcards, test, exam) | ready |
| History T1 · part 3 | `historia-carolingios/` | Trainer: the Carolingians (quiz 30 Oct) | ready |
| History T1 · resources | `historia-recursos/` | Printable PDFs: blank maps, timeline, notebook and project templates | ready |
| History T2 · al-Andalus | `historia-al-andalus/` | Trainer: al-Andalus (theory, dates, 5 maps, social pyramid, flashcards, test, exam) | ready |
| History T2 · Islam | `historia-islam/` | Trainer: Islam (theory, dates, 2 maps, mosque and city diagrams, pyramid, flashcards, test, exam) | ready |

Each lesson is a folder with `index.html`, `img/` and `pdf/` (printable blank map and the IGN physical map). The root `index.html` lists the lessons. `tools/` holds the scripts, data and template used to build lesson 2 (see `tools/README.md`).

### Data sources
- Spain's coastline and islands: IGN / CNIG (Líneas Límite), via AlexGPlay/SpainLayers
- Rivers, peaks, mountain ranges: © OpenStreetMap contributors (ODbL)
- Neighbouring countries, sea depths, sea names: Natural Earth (public domain)
- Relief: Copernicus DEM GLO-90 (ESA)
- Base map "Mapa físico de España 1:3 000 000", PDF: © Instituto Geográfico Nacional / CNIG
- Coasts, lakes and rivers in the history trainers: Natural Earth 1:10m (github.com/nvkelso/natural-earth-vector)
- Historical borders in `historia-tema1/`: [aourednik/historical-basemaps](https://github.com/aourednik/historical-basemaps), GPL-3.0 licence (borders are approximate)
- Byzantium map (527 and Justinian's conquests): [Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria), Seshat Global History Databank, CC BY 4.0 licence; 1025, 1204 and 1453 follow map 18 of the textbook
- Carolingian maps (Frankish kingdom in 768, Empire in 814, Treaty of Verdun): [Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria), CC BY 4.0, laid out like maps 12 and 14 of the textbook; marches are approximate
- Al-Andalus maps (conquest c. 720, caliphate c. 1000, taifas c. 1050, Almohads c. 1200, Nasrid kingdom c. 1400): [Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria), CC BY 4.0, clipped to the peninsula with Natural Earth; built by `tools/historia/andalus_geo.py`
- Islam maps (Arabia c. 630, expansion 632–750, Abbasids c. 800): Cliopatria, CC BY 4.0; coast and river base from Natural Earth 1:10m in its own projection (`tools/historia/geo_islam.py`, `islam_geo.py`)
- Photos in the history trainers: Wikimedia Commons (public domain, CC0, CC BY or CC BY-SA); author and licence under each photo and in `tools/historia/fotos.json`
- Political and physical maps of Europe: Natural Earth 1:10m (countries from Spain's point of view; Kosovo from the general version). Europe relief: Mapzen/AWS Terrain Tiles (SRTM, GMTED, ETOPO). Gulfs, straits, capes and the Italian peninsula: © OpenStreetMap contributors (Nominatim, ODbL). Meseta, Baetic ranges, Bohemia and the Great European Plain: computed from elevation data (river basins and heights, `regions_dem.py`). Scripts in `tools/europa/` and `tools/europa_fisica/`
- 🗺 bases in Europa física and Europa política: "Mapa físico de Europa" and "Mapa político de Europa" (Spanish National Atlas, 2025), © Instituto Geográfico Nacional / CNIG; georeferenced (Lambert conic fitted to 32 capitals of the political sheet; both sheets share the layout) and reprojected with `tools/ign/ign_warp.py`; shown only in "Estudiar" because they carry the names

### License
- Code (`tools/`, HTML/JS): **MIT**, see [`LICENSE`](LICENSE).
- Content (maps, images, PDFs, data): **CC BY-SA 4.0**, see [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md). Third-party data keeps its own terms; attribution is required.
