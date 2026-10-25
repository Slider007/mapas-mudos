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
| 3 | `europa-politica/` | Europa política | en preparación |
| 4 | `europa-fisica/` | Europa física | en preparación |
| Historia T1 | `historia-tema1/` | Fin de la Edad Antigua e inicio de la Edad Media: germanos y visigodos, bizantinos, carolingios (3 pruebas) | listo |
| Historia T1 · parte 1 | `historia-visigodos/` | Entrenador: pueblos germanos y visigodos (teoría, fechas, 3 mapas del libro, pirámide, tarjetas, test, examen) | listo |
| Historia T1 · parte 2 | `historia-bizancio/` | Entrenador: el Imperio bizantino (teoría, fechas, mapa del libro, pirámide, tarjetas, test, examen) | listo |
| Historia T1 · parte 3 | `historia-carolingios/` | Entrenador: los carolingios (prueba 30 oct) | listo |
| Historia T1 · recursos | `historia-recursos/` | PDF para imprimir: mapas mudos, línea del tiempo, plantillas del cuaderno y de trabajos | listo |
| Historia T2 | — | El islam y al-Ándalus | en preparación |

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
- Fotos de los entrenadores de historia: Wikimedia Commons (dominio público, CC0, CC BY o CC BY-SA); autor y licencia bajo cada foto y en `tools/historia/fotos.json`

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
| 3 | `europa-politica/` | Политическая карта Европы | в работе |
| 4 | `europa-fisica/` | Физическая карта Европы | в работе |
| История, тема 1 | `historia-tema1/` | Конец Античности и начало Средневековья: германцы и вестготы, Византия, Каролинги (3 проверочные) | готово |
| История, тема 1 · часть 1 | `historia-visigodos/` | Тренажёр: германцы и вестготы (материал, даты, 3 карты из учебника, пирамида, карточки, тест, экзамен) | готово |
| История, тема 1 · часть 2 | `historia-bizancio/` | Тренажёр: Византия (материал, даты, карта из учебника, пирамида, карточки, тест, экзамен) | готово |
| История, тема 1 · часть 3 | `historia-carolingios/` | Тренажёр: Каролинги (проверочная 30 окт) | готов |
| История, тема 1 · материалы | `historia-recursos/` | PDF для печати: контурные карты, линия времени, шаблоны тетради и работы | готово |
| История, тема 2 | — | Ислам и Аль-Андалус | в работе |

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
- Фото в тренажёрах по истории: Wikimedia Commons (общественное достояние, CC0, CC BY или CC BY-SA); автор и лицензия под каждым фото и в `tools/historia/fotos.json`

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
| 3 | `europa-politica/` | Political map of Europe | in progress |
| 4 | `europa-fisica/` | Physical map of Europe | in progress |
| History, topic 1 | `historia-tema1/` | End of Antiquity and start of the Middle Ages: Germanic peoples and Visigoths, Byzantium, Carolingians (3 quizzes) | ready |
| History T1 · part 1 | `historia-visigodos/` | Trainer: Germanic peoples and Visigoths (theory, dates, 3 textbook maps, pyramid, flashcards, test, exam) | ready |
| History T1 · part 2 | `historia-bizancio/` | Trainer: the Byzantine Empire (theory, dates, textbook map, pyramid, flashcards, test, exam) | ready |
| History T1 · part 3 | `historia-carolingios/` | Trainer: the Carolingians (quiz 30 Oct) | ready |
| History T1 · resources | `historia-recursos/` | Printable PDFs: blank maps, timeline, notebook and project templates | ready |
| History T2 | — | Islam and al-Andalus | in progress |

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
- Photos in the history trainers: Wikimedia Commons (public domain, CC0, CC BY or CC BY-SA); author and licence under each photo and in `tools/historia/fotos.json`

### License
- Code (`tools/`, HTML/JS): **MIT**, see [`LICENSE`](LICENSE).
- Content (maps, images, PDFs, data): **CC BY-SA 4.0**, see [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md). Third-party data keeps its own terms; attribution is required.
