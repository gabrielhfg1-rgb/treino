"""Gera os ícones do app sem bibliotecas externas.

Desenho: fundo espacial com grade, anel de progresso neon (ciano → violeta → rosa)
e um halter branco com anilhas neon no meio.

Uso:  python tools/gerar_icones.py
"""
import zlib, struct, os, math

def mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))

def over(dst, src, alpha):
    return mix(dst, src, max(0.0, min(1.0, alpha)))

def rrect(px, py, cx, cy, hw, hh, r):
    # distância (negativa = dentro) até um retângulo de cantos arredondados
    qx = abs(px - cx) - (hw - r); qy = abs(py - cy) - (hh - r)
    return math.hypot(max(qx, 0), max(qy, 0)) + min(max(qx, qy), 0) - r

BG_IN, BG_OUT = (34, 22, 70), (4, 5, 14)
TRACK = (34, 38, 70)
CYAN, VIOLET, PINK = (34, 211, 238), (139, 92, 246), (236, 72, 153)
WHITE, SHADE = (240, 244, 255), (176, 186, 230)

def grad3(t):
    t = max(0.0, min(1.0, t))
    return mix(CYAN, VIOLET, t / .55) if t < .55 else mix(VIOLET, PINK, (t - .55) / .45)

def pixel(u, v, k):
    """u,v em [0,1]; k = escala do desenho (1 normal, menor para ícone 'maskable')."""
    x = (u - .5) / k; y = (v - .5) / k
    d = math.hypot(x, y)
    col = mix(BG_IN, BG_OUT, min(1, math.hypot(u - .5, v - .38) / .72))
    # grade sutil
    gx = (u * 12) % 1; gy = (v * 12) % 1
    if min(gx, 1 - gx) < .03 or min(gy, 1 - gy) < .03:
        col = over(col, (70, 80, 150), .18 * max(0, 1 - d * 1.6))
    R, w = .385, .05
    a = (math.atan2(y, x) + math.pi / 2) % (2 * math.pi)
    frac = a / (2 * math.pi)
    on = frac <= .80
    # brilho em volta do anel aceso
    ring = abs(d - R) - w / 2
    if on and ring < .06:
        col = over(col, grad3(frac / .8), .35 * (1 - max(0, ring) / .06) ** 2)
    if ring < .004:
        c = grad3(frac / .8) if on else TRACK
        col = over(col, c, (.004 - ring) / .008)
    # halter
    parts = [
        ('bar', rrect(x, y, 0, 0, .21, .026, .02)),
        ('big', rrect(x, y, -.150, 0, .040, .150, .03)),
        ('big', rrect(x, y,  .150, 0, .040, .150, .03)),
        ('small', rrect(x, y, -.215, 0, .028, .100, .022)),
        ('small', rrect(x, y,  .215, 0, .028, .100, .022)),
        ('end', rrect(x, y, -.262, 0, .022, .034, .012)),
        ('end', rrect(x, y,  .262, 0, .022, .034, .012)),
    ]
    for kind, dist in parts:
        if kind in ('big', 'small') and dist < .03:
            col = over(col, CYAN if kind == 'big' else VIOLET, .25 * (1 - max(0, dist) / .03))
        if dist < .004:
            if kind == 'bar': c = WHITE
            elif kind == 'end': c = SHADE
            elif kind == 'big': c = mix(CYAN, VIOLET, (y + .15) / .3)
            else: c = mix(VIOLET, PINK, (y + .1) / .2)
            col = over(col, c, (.004 - dist) / .008)
    return col

def png(path, size, k=1.0, ss=3):
    rows = []
    for j in range(size):
        row = bytearray([0])
        for i in range(size):
            acc = [0.0, 0.0, 0.0]
            for sj in range(ss):
                for si in range(ss):
                    c = pixel((i + (si + .5) / ss) / size, (j + (sj + .5) / ss) / size, k)
                    acc[0] += c[0]; acc[1] += c[1]; acc[2] += c[2]
            n = ss * ss
            row += bytes(int(round(a / n)) for a in acc)
        rows.append(bytes(row))
    def chunk(t, d): return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    data = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(b''.join(rows), 9)) + chunk(b'IEND', b''))
    open(path, 'wb').write(data)

out = os.path.join(os.path.dirname(__file__), '..', 'icons')
os.makedirs(out, exist_ok=True)
png(os.path.join(out, 'icon-192.png'), 192)
png(os.path.join(out, 'icon-512.png'), 512, ss=2)
png(os.path.join(out, 'icon-512-maskable.png'), 512, k=.78, ss=2)
png(os.path.join(out, 'apple-touch-icon.png'), 180)
png(os.path.join(out, 'favicon-32.png'), 32, ss=4)
print('ícones gerados em', os.path.abspath(out))
