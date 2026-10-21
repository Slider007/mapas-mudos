# tools: как собран урок «España física»

[Русский](#tools-как-собран-урок-españa-física) · [Español](#español) · [English](#english)

Здесь скрипты и промежуточные данные, из которых собран `espana-fisica/`. Они нужны, чтобы собрать следующий урок (административное деление, Европа) или обновить этот. Скрипты рабочие, но писались по ходу работы: пути в них указывают на временные папки (`/mnt/user-data/...`, `/home/claude/...`), при запуске на своём компьютере их нужно заменить.

## Исходные данные (скачиваются отдельно, в репозитории их нет)
| Что | Откуда |
|---|---|
| Страны, моря, изобаты, регионы | Natural Earth 1:10M, `github.com/nvkelso/natural-earth-vector` (geojson) |
| Береговая линия и провинции Испании | `github.com/AlexGPlay/SpainLayers`, файл `provinces/0.geojson` (данные IGN) |
| Реки, вершины, хребты | OpenStreetMap через Overpass API (`overpass-api.de`), запросы по названиям из списка учителя |
| Рельеф | Copernicus DEM GLO-90, тайлы `copernicus-dem-90m.s3.amazonaws.com` (сборка через GDAL, см. ниже) |
| Подложка IGN | «Mapa físico de España 1:3 000 000», edición 2025, PDF с `ign.es` / CNIG |

## Порядок сборки
1. **Контур Испании**: `topo.py` и `build2.py` (границы провинций → контур, острова, соседние страны, проекция).
2. **Рельеф**: `dem2img.py` строит цветную и серую отмывку из `main.tif` и `can.tif` (палитра IGN). Файлы `main.tif`, `can.tif`:
   ```bash
   gdalwarp -te -10.9 33.4 5.6 44.6 -tr 0.003 0.003 -r average dem.vrt main.tif
   gdalwarp -te -18.4 27.5 -13.2 29.5 -tr 0.002 0.002 -r average dem.vrt can.tif
   ```
3. **Реки**: `osmriv.py`, `osmriv2.py`, `osmriv3.py` (сборка рек из OSM), `osmbank.py` (проверка берега притоков), `mouths.py` (достройка устьев по DEM), `buildriv.py` (в формат приложения).
4. **Рельеф, хребты и вершины**: `buildrel.py`.
5. **Заливы**: `gulfs.py` (области от мыса до мыса).
6. **Подложка IGN**: `geo25c.py` + `sea25.py` (привязка листа IGN по береговой линии, проекция Ламберта с параллелями 37°10′41″ и 42°49′19″), `warp25h.py` (перенос в проекцию приложения).
7. **PDF для печати**: `mkpdf.py`.
8. **Сборка страницы**: `src/espana-fisica.template.html` с метками `__GEO__`, `__HYPM__` и др. подставляется данными и картинками.

## Проверки
`verify.py`, `logic.py`, `rcheck.py`, `rivcmp.py`: положение объектов, впадение рек, берег притоков, сверка рек с картой IGN.

## Проекция приложения
Простая сетка градусов: `x = (lon + 10.9) * 100 * cos(40°)`, `y = (44.6 - lat) * 100`. Канары во врезке: `x = 14 + (lon + 18.4) * 100 * cos(28.5°)`.


---

## Español

# tools: cómo se construyó la lección «España física»

Aquí están los scripts y los datos intermedios con los que se construyó `espana-fisica/`. Sirven para construir las próximas lecciones (división administrativa, Europa) o para actualizar ésta. Los scripts funcionan, pero se escribieron sobre la marcha: las rutas apuntan a carpetas temporales (`/mnt/user-data/...`, `/home/claude/...`) y hay que cambiarlas al ejecutarlos en otro equipo.

### Datos de origen (se descargan aparte, no están en el repositorio)
| Qué | De dónde |
|---|---|
| Países, mares, isobatas, regiones | Natural Earth 1:10M, `github.com/nvkelso/natural-earth-vector` (geojson) |
| Costa y provincias de España | `github.com/AlexGPlay/SpainLayers`, archivo `provinces/0.geojson` (datos del IGN) |
| Ríos, cumbres, cordilleras | OpenStreetMap vía Overpass API (`overpass-api.de`), consultas por los nombres de la lista del profesor |
| Relieve | Copernicus DEM GLO-90, teselas de `copernicus-dem-90m.s3.amazonaws.com` (se ensambla con GDAL, véase abajo) |
| Fondo del IGN | «Mapa físico de España 1:3 000 000», edición 2025, PDF de `ign.es` / CNIG |

### Orden de construcción
1. **Contorno de España**: `topo.py` y `build2.py` (límites provinciales → contorno, islas, países vecinos, proyección).
2. **Relieve**: `dem2img.py` genera el sombreado en color y en gris a partir de `main.tif` y `can.tif` (paleta del IGN). Los archivos `main.tif`, `can.tif`:
   ```bash
   gdalwarp -te -10.9 33.4 5.6 44.6 -tr 0.003 0.003 -r average dem.vrt main.tif
   gdalwarp -te -18.4 27.5 -13.2 29.5 -tr 0.002 0.002 -r average dem.vrt can.tif
   ```
3. **Ríos**: `osmriv.py`, `osmriv2.py`, `osmriv3.py` (ensamblado de ríos desde OSM), `osmbank.py` (comprobación de la margen de los afluentes), `mouths.py` (completa las desembocaduras con el DEM), `buildriv.py` (al formato de la aplicación).
4. **Relieve, cordilleras y cumbres**: `buildrel.py`.
5. **Golfos**: `gulfs.py` (áreas de cabo a cabo).
6. **Fondo del IGN**: `geo25c.py` + `sea25.py` (georreferenciación de la hoja del IGN con la línea de costa, proyección de Lambert con paralelos 37°10′41″ y 42°49′19″), `warp25h.py` (paso a la proyección de la aplicación).
7. **PDF para imprimir**: `mkpdf.py`.
8. **Ensamblado de la página**: `src/espana-fisica.template.html` con las marcas `__GEO__`, `__HYPM__`, etc., que se sustituyen por datos e imágenes.

### Comprobaciones
`verify.py`, `logic.py`, `rcheck.py`, `rivcmp.py`: posición de los objetos, desembocadura de los ríos, margen de los afluentes, comparación de los ríos con el mapa del IGN.

### Proyección de la aplicación
Cuadrícula simple de grados: `x = (lon + 10.9) * 100 * cos(40°)`, `y = (44.6 - lat) * 100`. Canarias en el recuadro: `x = 14 + (lon + 18.4) * 100 * cos(28.5°)`.

---

## English

# tools: how the "España física" lesson was built

These are the scripts and intermediate data used to build `espana-fisica/`. They are needed to build the next lessons (administrative divisions, Europe) or to update this one. The scripts work but were written along the way: paths point to temporary folders (`/mnt/user-data/...`, `/home/claude/...`) and must be changed when running on another machine.

### Source data (downloaded separately, not in the repository)
| What | Where from |
|---|---|
| Countries, seas, isobaths, regions | Natural Earth 1:10M, `github.com/nvkelso/natural-earth-vector` (geojson) |
| Spain's coastline and provinces | `github.com/AlexGPlay/SpainLayers`, file `provinces/0.geojson` (IGN data) |
| Rivers, peaks, mountain ranges | OpenStreetMap via Overpass API (`overpass-api.de`), queried by the names on the teacher's list |
| Relief | Copernicus DEM GLO-90, tiles from `copernicus-dem-90m.s3.amazonaws.com` (mosaicked with GDAL, see below) |
| IGN base map | "Mapa físico de España 1:3 000 000", 2025 edition, PDF from `ign.es` / CNIG |

### Build order
1. **Spain outline**: `topo.py` and `build2.py` (province borders → outline, islands, neighbouring countries, projection).
2. **Relief**: `dem2img.py` renders colour and grey hillshade from `main.tif` and `can.tif` (IGN palette). Creating `main.tif`, `can.tif`:
   ```bash
   gdalwarp -te -10.9 33.4 5.6 44.6 -tr 0.003 0.003 -r average dem.vrt main.tif
   gdalwarp -te -18.4 27.5 -13.2 29.5 -tr 0.002 0.002 -r average dem.vrt can.tif
   ```
3. **Rivers**: `osmriv.py`, `osmriv2.py`, `osmriv3.py` (assembling rivers from OSM), `osmbank.py` (tributary bank check), `mouths.py` (completing river mouths from the DEM), `buildriv.py` (to the app format).
4. **Relief, ranges and peaks**: `buildrel.py`.
5. **Gulfs**: `gulfs.py` (areas from cape to cape).
6. **IGN base map**: `geo25c.py` + `sea25.py` (georeferencing the IGN sheet against the coastline, Lambert projection with parallels 37°10′41″ and 42°49′19″), `warp25h.py` (transfer to the app projection).
7. **Printable PDFs**: `mkpdf.py`.
8. **Page assembly**: `src/espana-fisica.template.html` with markers `__GEO__`, `__HYPM__`, etc. is filled in with data and images.

### Checks
`verify.py`, `logic.py`, `rcheck.py`, `rivcmp.py`: object positions, river confluences, tributary banks, comparison of rivers with the IGN map.

### App projection
A plain degree grid: `x = (lon + 10.9) * 100 * cos(40°)`, `y = (44.6 - lat) * 100`. Canary Islands inset: `x = 14 + (lon + 18.4) * 100 * cos(28.5°)`.
