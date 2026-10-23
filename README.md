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

Cada lección es una carpeta con `index.html`, `img/` y `pdf/` (mapa mudo para imprimir y mapa físico del IGN). La página `index.html` de la raíz enumera las lecciones. La carpeta `tools/` contiene los scripts, datos y la plantilla con que se construyó la lección 2 (véase `tools/README.md`).

### Fuentes de datos
- Costa e islas de España: IGN / CNIG (Líneas Límite), a través de AlexGPlay/SpainLayers
- Ríos, cumbres, cordilleras: © OpenStreetMap contributors (ODbL)
- Países vecinos, batimetría, nombres de mares: Natural Earth (dominio público)
- Relieve: Copernicus DEM GLO-90 (ESA)
- Fondo «Mapa físico de España 1:3 000 000», PDF: © Instituto Geográfico Nacional / CNIG
- Fronteras históricas de `historia-tema1/`: [aourednik/historical-basemaps](https://github.com/aourednik/historical-basemaps), licencia GPL-3.0 (fronteras aproximadas)

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

Каждый урок это папка с `index.html`, `img/` и `pdf/` (контурная карта для печати и физическая карта IGN). Корневой `index.html` содержит список уроков. В `tools/` лежат скрипты, данные и шаблон, из которых собран урок 2 (см. `tools/README.md`).

### Источники данных
- Береговая линия и острова Испании: IGN / CNIG (Líneas Límite), через репозиторий AlexGPlay/SpainLayers
- Реки, вершины, хребты: © OpenStreetMap contributors (ODbL)
- Соседние страны, глубины моря, названия акваторий: Natural Earth (public domain)
- Рельеф: Copernicus DEM GLO-90 (ESA)
- Подложка «Mapa físico de España 1:3 000 000», PDF: © Instituto Geográfico Nacional / CNIG
- Исторические границы в `historia-tema1/`: [aourednik/historical-basemaps](https://github.com/aourednik/historical-basemaps), лицензия GPL-3.0 (границы приблизительные)

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

Each lesson is a folder with `index.html`, `img/` and `pdf/` (printable blank map and the IGN physical map). The root `index.html` lists the lessons. `tools/` holds the scripts, data and template used to build lesson 2 (see `tools/README.md`).

### Data sources
- Spain's coastline and islands: IGN / CNIG (Líneas Límite), via AlexGPlay/SpainLayers
- Rivers, peaks, mountain ranges: © OpenStreetMap contributors (ODbL)
- Neighbouring countries, sea depths, sea names: Natural Earth (public domain)
- Relief: Copernicus DEM GLO-90 (ESA)
- Base map "Mapa físico de España 1:3 000 000", PDF: © Instituto Geográfico Nacional / CNIG
- Historical borders in `historia-tema1/`: [aourednik/historical-basemaps](https://github.com/aourednik/historical-basemaps), GPL-3.0 licence (borders are approximate)

### License
- Code (`tools/`, HTML/JS): **MIT**, see [`LICENSE`](LICENSE).
- Content (maps, images, PDFs, data): **CC BY-SA 4.0**, see [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md). Third-party data keeps its own terms; attribution is required.
