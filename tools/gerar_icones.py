"""Gera os ícones do app sem bibliotecas externas.

Desenho: fundo grafite com brilho no centro, anel de progresso vermelho (como a
anilha da tela de treino) e um halter branco no meio, com anilhas vermelhas.

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

BG_IN, BG_OUT = (40, 44, 53), (12, 13, 17)
TRACK = (52, 56, 66)
RED, RED_DK = (232, 56, 36), (176, 34, 20)
WHITE, SHADE = (246, 247, 249), (200, 204, 212)

def pixel(u, v, k):
    """u,v em [0,1]; k = escala do desenho (1 normal, menor para ícone 'maskable')."""
    x = (u - .5) / k; y = (v - .5) / k
    d = math.hypot(x, y)
    col = mix(BG_IN, BG_OUT, min(1, (math.hypot(u - .5, v - .42)) / .75))
    # anel de progresso
    R, w = .385, .055
    ring = abs(d - R) - w / 2
    if ring < .004:
        a = (math.atan2(y, x) + math.pi / 2) % (2 * math.pi)
        c = RED if a <= 2 * math.pi * .78 else TRACK
        if a <= 2 * math.pi * .78:
            c = mix(RED, RED_DK, (y + .4) / 1.6)  # leve degradê de cima para baixo
        col = over(col, c, (.004 - ring) / .008)
    # halter
    parts = [
        (WHITE, rrect(x, y, 0, 0, .21, .028, .02)),          # barra
        (RED, rrect(x, y, -.150, 0, .040, .150, .03)),       # anilhas grandes
        (RED, rrect(x, y,  .150, 0, .040, .150, .03)),
        (RED_DK, rrect(x, y, -.215, 0, .028, .100, .022)),   # anilhas menores
        (RED_DK, rrect(x, y,  .215, 0, .028, .100, .022)),
        (SHADE, rrect(x, y, -.262, 0, .022, .034, .012)),    # pontas
        (SHADE, rrect(x, y,  .262, 0, .022, .034, .012)),
    ]
    for c, dist in parts:
        if dist < .004:
            if c is RED:
                c = mix((246, 82, 60), RED_DK, (y + .15) / .3)  # brilho na anilha
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
