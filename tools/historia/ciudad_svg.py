# Ilustración de la ciudad islámica (esquema del punto 19 del resumen), en perspectiva sencilla: SVG generado.
import random
R = random.Random(7)
def box(x, y, w, h, d=10, top='#f7f1e3', front='#e3d6bd', side='#cdbb9a', roof=None, sw=.8):
    """caja en perspectiva: base (x,y) esquina inferior izquierda de la fachada, w ancho, h alto, d profundidad"""
    o = f'<path d="M{x},{y} h{w} v{-h} h{-w}z" fill="{front}" stroke="#8d7b5f" stroke-width="{sw}"/>'
    o += f'<path d="M{x + w},{y} l{d},{-d * .6} v{-h} l{-d},{d * .6}z" fill="{side}" stroke="#8d7b5f" stroke-width="{sw}"/>'
    o += f'<path d="M{x},{y - h} l{d},{-d * .6} h{w} l{-d},{d * .6}z" fill="{roof or top}" stroke="#8d7b5f" stroke-width="{sw}"/>'
    return o
def house(x, y, s=1.0):
    w, h, d = R.randint(14, 22) * s, R.randint(9, 15) * s, 9 * s
    roof = R.choice(['#f7f1e3', '#f3ead6', '#e9b98f', '#f7f1e3'])
    o = box(x, y, w, h, d, roof=roof)
    if R.random() < .7: o += f'<rect x="{x + w * .35:.1f}" y="{y - h * .55:.1f}" width="{3 * s:.1f}" height="{4 * s:.1f}" fill="#6d5c45"/>'
    return o
def dome(cx, cy, r, fill='#f7f1e3', holes=False):
    o = f'<path d="M{cx - r},{cy} a{r},{r} 0 0 1 {2 * r},0z" fill="{fill}" stroke="#8d7b5f" stroke-width=".8"/>'
    if holes: o += ''.join(f'<circle cx="{cx + dx}" cy="{cy - r * .45 + dy}" r="1.2" fill="#8d7b5f"/>' for dx, dy in [(-r * .4, 0), (0, -r * .25), (r * .4, 0), (-r * .15, r * .2), (r * .2, r * .2)])
    return o
def tower(x, y, w, h, fill='#e3c79a'):
    o = box(x, y, w, h, 6, top=fill, front=fill, side='#c9a874')
    o += ''.join(f'<rect x="{x + i * w / 4:.1f}" y="{y - h - 4}" width="{w / 8:.1f}" height="4" fill="{fill}" stroke="#8d7b5f" stroke-width=".6"/>' for i in range(4))
    return o
def svg():
    o = ['<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,sans-serif">',
         '<rect width="900" height="600" fill="#e9e4c9"/>',
         # huertas y río
         '<path d="M0,540 C200,515 380,580 560,548 C700,523 800,560 900,540 V600 H0z" fill="#9ccbe0"/>',
         ''.join(f'<rect x="{x}" y="{y}" width="46" height="24" fill="{c}" stroke="#b8b48a" stroke-width=".6" transform="skewX(-20)"/>' for x, y, c in [(120, 470, '#c5d99a'), (180, 488, '#d7e2a6'), (760, 470, '#c5d99a'), (820, 492, '#d7e2a6'), (60, 120, '#d7e2a6'), (110, 96, '#c5d99a')]),
         # colina de la alcazaba
         '<path d="M560,250 C600,120 720,70 860,95 L900,110 V300 C800,300 650,300 560,250z" fill="#d9cfa8" stroke="#b7a978" stroke-width="1"/>']
    # arrabales (fuera de la muralla)
    arr = [(x + R.uniform(-4, 4), y + R.uniform(-3, 3)) for x in range(18, 120, 22) for y in range(300, 470, 20) if R.random() < .8] + \
          [(x + R.uniform(-4, 4), y) for x in range(250, 600, 24) for y in (518, 532) if R.random() < .75]
    for x0, y0 in sorted(arr, key=lambda t: t[1]): o.append(house(x0, y0, .8))
    # muralla de la medina (polígono con almenas) y puertas
    wall = [(140, 230), (330, 165), (560, 190), (620, 300), (600, 460), (420, 500), (210, 480), (130, 380)]
    pts = ' '.join(f'{x},{y}' for x, y in wall)
    o.append(f'<polygon points="{pts}" fill="#f2ead2" stroke="#9c7f55" stroke-width="9" stroke-linejoin="round"/>')
    o.append(f'<polygon points="{pts}" fill="none" stroke="#c9a874" stroke-width="4" stroke-dasharray="5 4" stroke-linejoin="round"/>')
    for x, y in wall: o.append(tower(x - 9, y + 8, 18, 22))
    for x, y in [(235, 197), (608, 380), (315, 490), (135, 305)]:  # puertas
        o.append(f'<path d="M{x - 11},{y + 10} v-14 a11,11 0 0 1 22,0 v14z" fill="#5d4630" stroke="#3e2d1d" stroke-width="1.5"/>')
    # calles irregulares
    o.append('<path d="M235,205 C260,260 300,280 330,300 C360,320 420,315 470,345 C520,375 560,380 600,380 M330,300 C320,360 330,420 315,488 M330,300 C270,300 200,300 140,305" fill="none" stroke="#d8c9a6" stroke-width="7" stroke-linecap="round"/>')
    # casas de la medina
    # medina densa: casas en una rejilla irregular dentro de la muralla, sin tapar los edificios numerados
    from shapely.geometry import Polygon, Point, box as sbox
    inner = Polygon(wall).buffer(-16)
    keep_out = [sbox(275, 280, 470, 372), sbox(425, 270, 540, 360), sbox(180, 285, 262, 335), sbox(225, 380, 300, 425), sbox(465, 410, 560, 460),
                sbox(230, 190, 250, 215), sbox(590, 360, 625, 395), sbox(300, 470, 330, 500), sbox(125, 290, 150, 320)]
    pts_h = []
    for gy in range(205, 495, 21):
        for gx in range(140, 620, 25):
            x, y = gx + R.uniform(-6, 6), gy + R.uniform(-4, 4)
            if inner.contains(Point(x + 9, y - 6)) and not any(k.intersects(sbox(x - 2, y - 18, x + 26, y + 2)) for k in keep_out) and R.random() < .86:
                pts_h.append((x, y))
    for x, y in sorted(pts_h, key=lambda t: t[1]): o.append(house(x, y, .85))
    # 1 mezquita aljama: patio con naranjos + sala de oración + alminar
    o.append(box(300, 360, 120, 8, 40, top='#cfe3b0', front='#e3d6bd'))
    o.append(''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="#6aa55a"/>' for x in (325, 345, 365, 385) for y in (342, 330)))
    o.append(box(300, 335, 120, 24, 24, roof='#d9b98a'))
    o.append(''.join(f'<path d="M{300 + i * 12},{311} l12,-8 l12,8" fill="none" stroke="#b08850" stroke-width="1"/>' for i in range(10)))
    o.append(tower(280, 362, 18, 70, fill='#efd9ae'))
    # 2 zoco: puestos con toldos de colores
    for i, c in enumerate(['#e57373', '#ffb74d', '#81c784', '#64b5f6', '#ba68c8', '#ffd54f']):
        x = 430 + i * 22; o.append(box(x, 352, 18, 8, 6)); o.append(f'<path d="M{x - 2},{344} h22 l-3,-7 h-16z" fill="{c}" stroke="#8d7b5f" stroke-width=".6"/>')
    # 3 alcaicería: recinto cerrado con puertas
    o.append(box(440, 300, 70, 14, 22, top='#f3e5c8', front='#e0c9a0'))
    o.append(''.join(f'<rect x="{445 + i * 13}" y="292" width="6" height="8" fill="#6d5c45"/>' for i in range(5)))
    # 4 madrasa: patio + cúpula
    o.append(box(185, 330, 52, 20, 22, top='#e8f0f5')); o.append(dome(222, 296, 9, fill='#c8dbe8'))
    # 5 alhóndiga: patio central
    o.append(box(470, 455, 60, 22, 26)); o.append('<path d="M482,433 l9,-5 h28 l-9,5z" fill="#cdbb9a"/>')
    # 6 hammam: cúpulas con lucernarios
    o.append(box(230, 420, 56, 12, 20)); o.append(dome(246, 396, 8, holes=True) + dome(266, 394, 10, holes=True) + dome(284, 398, 7, holes=True))
    # 7 alcazaba (ciudad alta, fortificada) y 10 alcázar (palacio)
    o.append('<polygon points="640,200 760,120 860,140 870,240 760,270 650,250" fill="#efe3c3" stroke="#9c7f55" stroke-width="8" stroke-linejoin="round"/>')
    for x, y in [(640, 200), (760, 120), (860, 140), (870, 240), (760, 270), (650, 250)]: o.append(tower(x - 10, y + 10, 20, 28))
    o.append(tower(690, 225, 26, 46))
    o.append(box(760, 240, 80, 26, 30, roof='#e9b98f', front='#f3e5c8'))
    o.append('<rect x="772" y="196" width="48" height="10" fill="#7ec3e0" stroke="#5aa0bf" transform="skewX(-30)" />')
    o.append(''.join(f'<path d="M{770 + i * 14},240 v-14 a6,6 0 0 1 12,0 v14" fill="#d9c49a" stroke="#8d7b5f" stroke-width=".7"/>' for i in range(5)))
    # números
    nums = [(1, 360, 275), (2, 495, 368), (3, 470, 262), (4, 195, 280), (5, 545, 470), (6, 258, 372), (7, 770, 105), (8, 330, 140), (9, 60, 282), (10, 860, 215)]
    for n, x, y in nums:
        o.append(f'<g><circle cx="{x}" cy="{y}" r="17" fill="#5e35b1" stroke="#fff" stroke-width="3"/><text x="{x}" y="{y + 7}" text-anchor="middle" font-size="19" font-weight="800" fill="#fff">{n}</text></g>')
    o.append('<text x="890" y="590" text-anchor="end" font-size="13" fill="#5b6b5a" font-style="italic">río</text>')
    o.append('</svg>')
    return ''.join(o)
