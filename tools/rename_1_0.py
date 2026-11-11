"""Rename ia_upgraded (0.6.2) -> ia_industries (1.0.0): mod id, package, classes, display name, version."""
import os, shutil, re, sys
SRC, OUT, VERSION = 'proj8', 'proj10', '1.0.0'
if os.path.exists(OUT): shutil.rmtree(OUT)
shutil.copytree(SRC, OUT)
REPL = [('ia_upgraded', 'ia_industries'), ('kr.aerosky.iaupgraded', 'kr.aerosky.iaindustries'), ('kr/aerosky/iaupgraded', 'kr/aerosky/iaindustries'),
        ('IAUpgraded', 'IAIndustries'), ('UpgradedRenderer', 'IndustriesRenderer'),
        ('Create: Immersive Aircraft Upgraded', 'Create: Immersive Aircraft Industries')]
TEXT = ('.java', '.json', '.toml', '.py', '.js', '.mcmeta', '.txt', '.lang')
for root, dirs, files in os.walk(OUT):
    for f in files:
        if f.endswith(TEXT):
            p = os.path.join(root, f); t = open(p, encoding='utf-8').read(); n = t
            for a, b in REPL: n = n.replace(a, b)
            if n != t: open(p, 'w', encoding='utf-8').write(n)
for root, dirs, files in os.walk(OUT, topdown=False):
    for nm in files + dirs:
        new = nm.replace('IAUpgraded', 'IAIndustries').replace('UpgradedRenderer', 'IndustriesRenderer').replace('ia_upgraded', 'ia_industries').replace('iaupgraded', 'iaindustries')
        if new != nm: os.rename(os.path.join(root, nm), os.path.join(root, new))
res = OUT + '/resources'
p = res + '/META-INF/neoforge.mods.toml'; t = open(p).read()
t = t.replace('version = "0.6.2"', 'version = "%s"' % VERSION)
t = re.sub(r"description = '''.*?'''", "description = '''\nCargo and warship-class variants for every Immersive Aircraft vehicle, with all Immersive Aircraft recipes rebuilt around Create (mechanical crafting). Requires Immersive Aircraft and Create.\n'''", t, flags=re.S)
open(p, 'w').write(t)
open(res + '/pack.mcmeta', 'w').write('{"pack": {"description": "Create: Immersive Aircraft Industries", "pack_format": 34}}')
