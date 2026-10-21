# Входные файлы скриптов

Скрипты в `scripts/` ждут свои входные файлы в рабочей папке (имена без пути). Часть мелких промежуточных файлов лежит в `data/`, крупные исходные данные скачиваются отдельно.

## Уже в репозитории (`data/`)
| Файл | Для чего |
|---|---|
| `geo2.json` | контур Испании, острова, соседние страны в проекции приложения |
| `grayp_main.png`, `grayp_can.png` | серая отмывка для листов PDF (полуостров и Канары) |
| `es_hr.pkl` | контур Испании из IGN (shapely, pickle) |
| `osm_pick2.pkl`, `osm_bank.pkl`, `rivers_ne.pkl`, `mouth_ext.pkl` | итоговая геометрия рек, берега притоков, реки Natural Earth, устья |
| `georef.json`, `gulfs.json`, `objs.json`, `bath.json`, `gulf_lbl.json`, `syslbl.json`, `objs3.json`, `rel_osm.json`, `riv_osm.json` | привязка, заливы, объекты, глубины, подписи |
| `overpass/*.ql` | запросы к Overpass API для рек, вершин, хребтов |

Pickle-файлы привязаны к версии shapely; если не открываются, пересоберите их скриптами `osmriv*.py`.

## Скачивать отдельно
| Файл | Откуда |
|---|---|
| `c10.geojson` | Natural Earth `ne_10m_admin_0_countries.geojson` |
| `ne_10m_geography_marine_polys.geojson`, `ne_10m_geography_regions_polys.geojson`, `ne_10m_bathymetry_*.geojson` | Natural Earth, `github.com/nvkelso/natural-earth-vector/tree/master/geojson` |
| `osm/rivers.json` | Overpass API: `curl --data-urlencode data@data/overpass/rivers.ql https://overpass-api.de/api/interpreter` (нужен заголовок `-A`, иначе ошибка 406) |
| `sel.json`, `llob.json`, пики и хребты | те же запросы `p1.ql`, `p2.ql`, `rg.ql`, `lb.ql`, `sel.ql` |
| `main.tif`, `can.tif` | Copernicus DEM GLO-90, команды `gdalwarp` в `README.md` |
| `ign25-1.png`, `ign400-1.png` | PDF IGN 2025: `pdftoppm -r 250 -png -f 1 -l 1 <pdf> ign25` и `-r 400` для `ign400` |

## Сборка только PDF для печати
Ничего скачивать не нужно: `python3 tools/scripts/mkpdf.py` из любого места собирает `espana-fisica/pdf/mapa-mudo-espana-fisica.pdf` (нужен только `reportlab`).
