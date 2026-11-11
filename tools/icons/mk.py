"""64x64 item icons: the real model in a front 3/4 view (low camera so belly weapons, floats, engines show), crisp downsample + dark outline."""
import json, subprocess, os, numpy as np
from PIL import Image
OUT = '/home/claude/build/m2/out'; NAMES = ['cargo_copter', 'cargo_gyrodyne', 'cargo_biplane', 'cargo_seaplane', 'gigantia', 'pelican', 'hawk', 'dragonfly']
CAMS = dict(gigantia='96,34,34', cargo_biplane='82,28,56', cargo_seaplane='82,28,56', pelican='80,28,60', dragonfly='70,30,72'); CAM = '62,26,78'; SZ = int(os.environ.get('SZ', 48)); DIL = float(os.environ.get('DIL', 1.1)); SAT = 1.3; CON = 1.18; NCOL = 22
def render(n):
    s = json.load(open(f'{OUT}/{n}.scene.json')); cs = [c for c in s['cubes'] if c['mat'] not in ('skin', 'shirt', 'pants')]
    mn = [min(c['f'][i] for c in cs) for i in range(3)]; mx = [max(c['t'][i] for c in cs) for i in range(3)]
    cen = [(mn[i] + mx[i]) / 2 for i in range(3)]; K = 0.62 * max(mx[0] - mn[0], mx[2] - mn[2], mx[1] - mn[1])
    subprocess.run(['node', 'icon3.js', n, str(K), *map(str, cen), 'icon'], env=dict(os.environ, SCENE_DIR=OUT, CAM=CAMS.get(n, CAM)), check=True)
def sprite(n):
    from PIL import ImageFilter
    im = Image.open(f'iso_{n}.png').convert('RGBA'); im = im.crop(im.getbbox()); inner = SZ - 2
    a = np.asarray(im).astype('float32'); al = a[..., 3]
    # thicken thin parts (rotor blades, struts, rails) BEFORE shrinking so they stay connected at low resolution
    px = max(im.size) / inner                                               # hi-res pixels per icon pixel
    r = (int(px * DIL) | 1); k = (int(px * 0.9) | 1)
    solid = Image.fromarray((al > 40).astype('uint8') * 255, 'L')
    opened = solid.filter(ImageFilter.MinFilter(k)).filter(ImageFilter.MaxFilter(k))          # bodies survive an opening, thin parts do not
    thin = np.asarray(solid).astype(bool) & ~np.asarray(opened).astype(bool)
    thick = Image.fromarray(thin.astype('uint8') * 255, 'L').filter(ImageFilter.MaxFilter(r))   # only the thin parts (rotor blades, struts, rails) get thickened
    A = np.maximum(np.asarray(solid), np.asarray(thick)).astype('float32') / 255
    pre = a[..., :3] * (al[..., None] > 40); blur = lambda x, k: np.stack([np.asarray(Image.fromarray(x[..., c].astype('uint8'), 'L').filter(ImageFilter.GaussianBlur(k))) for c in range(3)], -1)
    wa = np.asarray(Image.fromarray(((al > 40) * 255).astype('uint8'), 'L').filter(ImageFilter.GaussianBlur(r))).astype('float32') / 255
    fill = blur(pre.astype('float32'), r) / np.maximum(wa[..., None], 1e-3)
    rgb = np.where((al > 40)[..., None], a[..., :3], fill)                 # keep real colours, borrow neighbours' colours for the added rim
    big = np.concatenate([rgb, (A * 255)[..., None]], -1).astype('uint8'); im = Image.fromarray(big, 'RGBA')
    sc = min(inner / im.width, inner / im.height); w, h = max(1, round(im.width * sc)), max(1, round(im.height * sc))
    pm = np.concatenate([big[..., :3] * (big[..., 3:4] / 255.0), big[..., 3:4]], -1).astype('uint8')
    P = Image.fromarray(pm, 'RGBA').resize((w, h), Image.BOX); b = np.asarray(P).astype('float32'); alp = b[..., 3] / 255
    rgb = b[..., :3] / np.maximum(alp[..., None], 1e-3); g = rgb.mean(-1, keepdims=True); rgb = np.clip(g + (rgb - g) * SAT, 0, 255); rgb = np.clip((rgb - 128) * CON + 128, 0, 255)
    m = alp > 0.30
    q = Image.fromarray(np.where(m[..., None], rgb, 0).astype('uint8'), 'RGB').quantize(NCOL, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB'); rgb = np.asarray(q).astype('float32')
    o = np.zeros((SZ, SZ, 4), 'uint8'); ox, oy = (SZ - w) // 2, (SZ - h) // 2
    M = np.zeros((SZ, SZ), bool); R = np.zeros((SZ, SZ, 3), 'float32'); M[oy:oy + h, ox:ox + w] = m; R[oy:oy + h, ox:ox + w] = rgb
    O = M.copy()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)): O |= np.roll(np.roll(M, dy, 0), dx, 1)
    edge = O & ~M; o[..., :3] = np.where(M[..., None], R, 0).astype('uint8'); o[edge, :3] = (30, 20, 18); o[..., 3] = np.where(O, 255, 0)
    Image.fromarray(o, 'RGBA').save(f'icons/{n}.png')
if __name__ == '__main__':
    os.makedirs('icons', exist_ok=True)
    for n in NAMES: render(n); sprite(n)
    sh = Image.new('RGBA', (4 * 260, 2 * 260 + 80), (92, 92, 104, 255))
    for k, n in enumerate(NAMES):
        i = Image.open(f'icons/{n}.png'); big = i.resize((256, 256), Image.NEAREST); sh.paste(big, ((k % 4) * 260, (k // 4) * 260), big)
        sm = i.resize((32, 32), Image.NEAREST); sh.paste(sm, (k * 100 + 10, 2 * 260 + 20), sm); sm2 = i.resize((16, 16), Image.BOX); sh.paste(sm2, (k * 100 + 60, 2 * 260 + 28), sm2)   # slot-size (32) and tiny check
    sh.save('sheet.png')
