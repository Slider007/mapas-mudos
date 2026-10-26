# Cuencas hidrográficas a partir de la rejilla de altitudes (relleno de depresiones «priority flood» + dirección D8).
import heapq, numpy as np
D8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
def flow(E, land, y0, y1, x0, x1):
    """devuelve (receptor[y,x] como índice plano, subrejilla) dentro de la ventana; el mar es sumidero"""
    e = E[y0:y1, x0:x1].astype(np.float64); L = land[y0:y1, x0:x1]; h, w = e.shape
    filled = np.where(L, np.inf, e); done = ~L.copy(); pq = []
    # semillas: mar contiguo a tierra y borde de la ventana
    for y in range(h):
        for x in range(w):
            if L[y, x] and (y in (0, h - 1) or x in (0, w - 1) or any(0 <= y + dy < h and 0 <= x + dx < w and not L[y + dy, x + dx] for dy, dx in D8)):
                filled[y, x] = e[y, x]; heapq.heappush(pq, (e[y, x], y, x)); done[y, x] = True
    rec = -np.ones((h, w), np.int64)
    while pq:
        z, y, x = heapq.heappop(pq)
        for dy, dx in D8:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not done[ny, nx]:
                done[ny, nx] = True; filled[ny, nx] = max(e[ny, nx], z + 1e-3); rec[ny, nx] = y * w + x
                heapq.heappush(pq, (filled[ny, nx], ny, nx))
    return rec, (h, w)
def upstream(rec, shape, seeds):
    """celdas que drenan hacia alguna de las celdas semilla"""
    h, w = shape; kids = [[] for _ in range(h * w)]
    for i, r in enumerate(rec.ravel()):
        if r >= 0: kids[r].append(i)
    out = np.zeros(h * w, bool); st = [s for s in seeds]
    for s in st: out[s] = True
    while st:
        i = st.pop()
        for k in kids[i]:
            if not out[k]: out[k] = True; st.append(k)
    return out.reshape(h, w)
