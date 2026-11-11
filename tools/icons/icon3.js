// node render.js <name> <K> <cx> <cy> <cz> [icon]   (run from the folder holding <name>.scene.json)
const { chromium } = require('playwright'); const fs = require('fs');
const [, , name, kk, cx, cy, cz, mode] = process.argv; const SCENE_DIR = process.env.SCENE_DIR || '.'; const CAMV = (process.env.CAM || '62,40,70').split(',').map(Number); const K = +kk, CEN = [+cx, +cy, +cz]; const ICON = mode === 'icon';
const W = 512, H = 512;
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
  await p.setContent('<body style="margin:0;background:' + (ICON ? 'transparent' : 'linear-gradient(#9fc4e8,#e6eef5)') + '"><canvas id=c></canvas></body>');
  await p.addScriptTag({ path: '/home/claude/tools/node_modules/three/build/three.min.js' });
  const scene = JSON.parse(fs.readFileSync(SCENE_DIR + '/' + name + '.scene.json'));
  const views = ICON ? [['icon', CAMV]] : [['v1', [62, 40, 70]], ['v2', [-70, 34, -58]], ['v3', [95, 6, 2]], ['v4', [2, 95, 6]]];
  for (const [vn, cam] of views) {
    await p.evaluate(async ({ S, cam, K, CEN, W, H, ICON }) => {
      const T = THREE, r = new T.WebGLRenderer({ canvas: document.getElementById('c'), antialias: true, alpha: true, preserveDrawingBuffer: true });
      r.setPixelRatio(2); r.setSize(W, H); r.shadowMap.enabled = true;
      const sc = new T.Scene();
      const tex = await new T.TextureLoader().loadAsync(S.tex); tex.magFilter = T.NearestFilter; tex.minFilter = T.NearestFilter; tex.colorSpace = T.SRGBColorSpace; tex.flipY = false;
      const mat = new T.MeshLambertMaterial({ map: tex, alphaTest: 0.5, side: T.DoubleSide });
      const N = { north: [0, 0, -1], south: [0, 0, 1], east: [1, 0, 0], west: [-1, 0, 0], up: [0, 1, 0], down: [0, -1, 0] };
      for (const c of S.cubes) {
        if (ICON && ['skin', 'shirt', 'pants'].includes(c.mat)) continue;
        const [x0, y0, z0] = c.f, [x1, y1, z1] = c.t;
        const Q = { north: [[x1, y1, z0], [x0, y1, z0], [x0, y0, z0], [x1, y0, z0]], south: [[x0, y1, z1], [x1, y1, z1], [x1, y0, z1], [x0, y0, z1]], east: [[x1, y1, z1], [x1, y1, z0], [x1, y0, z0], [x1, y0, z1]], west: [[x0, y1, z0], [x0, y1, z1], [x0, y0, z1], [x0, y0, z0]], up: [[x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]], down: [[x0, y0, z1], [x1, y0, z1], [x1, y0, z0], [x0, y0, z0]] };
        const pos = [], uv = [], nor = [], idx = [];
        for (const f in c.uv) {
          const [u0, v0, u1, v1] = c.uv[f]; const q = Q[f]; const n = pos.length / 3;
          if ((y0 == y1 && f == 'down') || (z0 == z1 && f == 'north') || (x0 == x1 && f == 'west')) continue;
          q.forEach(v => { pos.push(...v); nor.push(...N[f]) });
          uv.push(u0 / S.tw, v0 / S.th, u1 / S.tw, v0 / S.th, u1 / S.tw, v1 / S.th, u0 / S.tw, v1 / S.th); idx.push(n, n + 2, n + 1, n, n + 3, n + 2);
        }
        const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new T.Float32BufferAttribute(uv, 2)); g.setAttribute('normal', new T.Float32BufferAttribute(nor, 3)); g.setIndex(idx);
        let o = new T.Mesh(g, mat); o.castShadow = true; o.receiveShadow = !(x0 == x1 || y0 == y1 || z0 == z1);
        for (const [rot, org] of (c.chain || [])) {
          const piv = new T.Group(); piv.position.set(...org); const inner = new T.Group(); inner.position.set(-org[0], -org[1], -org[2]); inner.add(o); piv.add(inner);
          piv.rotation.set(...rot.map(d => d * Math.PI / 180), 'ZYX'); o = piv;
        }
        sc.add(o);
      }
      sc.add(new T.HemisphereLight(0xffffff, 0x8a8f99, 1.5));
      const d = new T.DirectionalLight(0xfff2dd, 2.0); d.position.set(40, 90, 50); d.castShadow = true; d.shadow.mapSize.set(2048, 2048);
      Object.assign(d.shadow.camera, { left: -260, right: 260, top: 260, bottom: -260, near: 1, far: 600 }); sc.add(d);
      if (!ICON && cam[1] > 0 && cam[1] < 90) { const gp = new T.Mesh(new T.PlaneGeometry(1200, 1200), new T.ShadowMaterial({ opacity: 0.22 })); gp.rotation.x = -Math.PI / 2; gp.receiveShadow = true; sc.add(gp); }
      const a = W / H; const camO = new T.OrthographicCamera(-K * a, K * a, K, -K, -1500, 1500);
      camO.position.set(cam[0] + CEN[0], cam[1] + CEN[1], cam[2] + CEN[2]); if (cam[1] >= 90) camO.up.set(0, 0, 1); camO.lookAt(...CEN); r.render(sc, camO);
    }, { S: scene, cam, K, CEN, W, H, ICON });
    await p.screenshot({ path: 'iso_' + name + '.png', omitBackground: ICON });
  }
  await b.close();
})();
