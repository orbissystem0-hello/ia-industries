#!/usr/bin/env python3
"""ia_fleet 0.1.0 -> ia_upgraded 0.2.0: 이름 변경, Create 의존, 제작법 전면 교체."""
import json, os, re, shutil, sys

OLD_JAR = '/home/claude/ia_fleet_src/jar'
OUT = '/home/claude/build/proj'
OLD, NEW = 'ia_fleet', 'ia_upgraded'
VERSION = '0.2.0'

if os.path.exists(OUT):
    shutil.rmtree(OUT)
res = os.path.join(OUT, 'resources')
src = os.path.join(OUT, 'src')

# ---- 1. 리소스 복사 (네임스페이스 변경) ----
for top in ('assets', 'data'):
    shutil.copytree(os.path.join(OLD_JAR, top, OLD), os.path.join(res, top, NEW))
for f in ('pack.mcmeta', 'LICENSE.txt'):
    shutil.copy(os.path.join(OLD_JAR, f), os.path.join(res, f))
shutil.rmtree(os.path.join(res, 'data', NEW, 'recipe'))
for root, _, files in os.walk(res):
    for f in files:
        if f.endswith(('.json', '.mcmeta')):
            p = os.path.join(root, f)
            t = open(p, encoding='utf-8').read()
            if OLD in t:
                open(p, 'w', encoding='utf-8').write(t.replace(OLD, NEW))

# ---- 2. 소스 (패키지·ID 변경) ----
for root, _, files in os.walk(os.path.join(OLD_JAR, 'sources', 'kr')):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), os.path.join(OLD_JAR, 'sources'))
        rel = rel.replace('iafleet', 'iaupgraded').replace('IAFleet', 'IAUpgraded').replace('FleetRenderer', 'UpgradedRenderer')
        t = open(os.path.join(root, f), encoding='utf-8').read()
        t = (t.replace('kr.aerosky.iafleet', 'kr.aerosky.iaupgraded').replace('IAFleet', 'IAUpgraded')
              .replace('FleetRenderer', 'UpgradedRenderer').replace('"ia_fleet"', '"ia_upgraded"')
              .replace('TABS.register("fleet"', 'TABS.register("aircraft"').replace('+ ".fleet")', '+ ".aircraft")'))
        os.makedirs(os.path.dirname(os.path.join(src, rel)), exist_ok=True)
        open(os.path.join(src, rel), 'w', encoding='utf-8').write(t)
shutil.copytree(os.path.join(OLD_JAR, 'sources', 'models'), os.path.join(OUT, 'models_src'))

# ---- 3. 언어 파일 ----
TAB = {'en_us': 'Create: Immersive Aircraft Upgraded', 'ko_kr': 'Create: 이머시브 에어크래프트 업그레이디드',
       'ja_jp': 'Create: イマーシブ・エアクラフト アップグレーデッド'}
for lang, name in TAB.items():
    p = os.path.join(res, 'assets', NEW, 'lang', lang + '.json')
    d = json.load(open(p, encoding='utf-8'))
    d = {k: v for k, v in d.items() if not k.startswith('itemGroup.')}
    d = {'itemGroup.%s.aircraft' % NEW: name, **d}
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# ---- 4. mods.toml ----
toml = open(os.path.join(OLD_JAR, 'META-INF', 'neoforge.mods.toml'), encoding='utf-8').read()
toml = toml.replace(OLD, NEW).replace('version = "0.1.0"', 'version = "%s"' % VERSION)
toml = toml.replace('displayName = "Immersive Aircraft: Fleet"', 'displayName = "Create: Immersive Aircraft Upgraded"')
toml = re.sub(r"description = '''.*?'''", "description = '''\nUpgrade paths for the Immersive Aircraft vehicles: every base aircraft can be upgraded into a cargo variant and then into a warship-class variant. All Immersive Aircraft recipes are replaced with Create recipes.\n'''", toml, flags=re.S)
toml += '''
[[dependencies.%s]]
modId = "create"
type = "required"
versionRange = "[6.0.0,)"
ordering = "AFTER"
side = "BOTH"
''' % NEW
os.makedirs(os.path.join(res, 'META-INF'))
open(os.path.join(res, 'META-INF', 'neoforge.mods.toml'), 'w', encoding='utf-8').write(toml)

# ---- 5. 제작법 ----
IA, CR, MC = 'immersive_aircraft:', 'create:', 'minecraft:'
count = {'ia': 0, 'own': 0}

def ing(x):
    return {'tag': x[1:]} if x.startswith('#') else {'item': x}

def recipe(ns, name, kind, pattern, key, result=None):
    """kind: 'mech' = Create 기계식 조합기, 'table' = 작업대"""
    w = max(len(r) for r in pattern)
    assert all(len(r) == w for r in pattern), name
    used = set(''.join(pattern)) - {' '}
    assert used == set(key), (name, used, set(key))
    if kind == 'table':
        assert len(pattern) <= 3 and w <= 3, name
    r = {'type': 'create:mechanical_crafting' if kind == 'mech' else 'minecraft:crafting_shaped', 'category': 'misc',
         'key': {k: ing(v) for k, v in key.items()}, 'pattern': pattern,
         'result': {'count': 1, 'id': result or (IA if ns == 'immersive_aircraft' else NEW + ':') + name}}
    if kind == 'mech':
        r['accept_mirrored'] = False
        r['show_notification'] = False
    d = os.path.join(res, 'data', ns, 'recipe')
    os.makedirs(d, exist_ok=True)
    json.dump(r, open(os.path.join(d, name + '.json'), 'w'), indent=2)
    count['ia' if ns == 'immersive_aircraft' else 'own'] += 1

ia = lambda *a: recipe('immersive_aircraft', *a)
own = lambda *a: recipe(NEW, *a)

# 부품 5종
ia('hull', 'table', ['PPP', 'AAA', 'PPP'], {'P': '#minecraft:planks', 'A': CR + 'andesite_alloy'})
ia('sail', 'table', ['WWS', 'WWS'], {'W': CR + 'white_sail', 'S': MC + 'string'})
ia('propeller', 'table', ['I I', ' P ', 'I I'], {'I': CR + 'iron_sheet', 'P': CR + 'propeller'})
ia('boiler', 'table', ['CCC', 'CTC', 'CFC'], {'C': CR + 'copper_sheet', 'T': CR + 'fluid_tank', 'F': MC + 'furnace'})
ia('engine', 'mech', [' S ', 'PBP', 'CMC'], {'S': CR + 'shaft', 'P': MC + 'piston', 'B': IA + 'boiler', 'C': CR + 'copper_casing', 'M': CR + 'precision_mechanism'})
# 업그레이드·무기 15종
ia('eco_engine', 'mech', ['SGS', 'GEG', 'BBB'], {'S': MC + 'slime_ball', 'G': CR + 'golden_sheet', 'E': IA + 'engine', 'B': MC + 'brick'})
ia('nether_engine', 'mech', ['MNM', 'BEB', 'SSS'], {'M': MC + 'magma_cream', 'N': MC + 'netherite_ingot', 'B': CR + 'blaze_burner', 'E': IA + 'engine', 'S': CR + 'sturdy_sheet'})
ia('enhanced_propeller', 'table', ['BB ', ' P ', ' BB'], {'B': CR + 'brass_sheet', 'P': IA + 'propeller'})
ia('gyroscope', 'table', ['RCR', ' P '], {'R': CR + 'electron_tube', 'C': MC + 'compass', 'P': CR + 'precision_mechanism'})
ia('gyroscope_dials', 'table', [' C ', 'SGT'], {'C': MC + 'clock', 'S': CR + 'speedometer', 'G': IA + 'gyroscope', 'T': CR + 'stressometer'})
ia('gyroscope_hud', 'table', ['NPN', 'TLT', ' G '], {'N': CR + 'brass_nugget', 'P': MC + 'glass_pane', 'T': CR + 'electron_tube', 'L': CR + 'nixie_tube', 'G': IA + 'gyroscope'})
ia('heavy_crossbow', 'table', ['CH', 'AS'], {'C': MC + 'crossbow', 'H': MC + 'tripwire_hook', 'A': CR + 'andesite_casing', 'S': CR + 'shaft'})
ia('hull_reinforcement', 'table', ['III', 'HHH', 'III'], {'I': CR + 'iron_sheet', 'H': IA + 'hull'})
ia('improved_landing_gear', 'table', [' II', 'BBI', 'BB '], {'I': CR + 'iron_sheet', 'B': CR + 'belt_connector'})
ia('industrial_gears', 'table', [' II', 'CLI', 'CC '], {'I': CR + 'iron_sheet', 'C': CR + 'cogwheel', 'L': CR + 'large_cogwheel'})
ia('rotary_cannon', 'mech', ['FFF', 'DGM'], {'F': CR + 'fluid_pipe', 'D': MC + 'dispenser', 'G': IA + 'industrial_gears', 'M': CR + 'precision_mechanism'})
ia('steel_boiler', 'table', ['III', 'IBI', 'IFI'], {'I': CR + 'iron_sheet', 'B': IA + 'boiler', 'F': MC + 'blast_furnace'})
ia('sturdy_pipes', 'table', ['  P', 'IPI', 'P  '], {'P': CR + 'fluid_pipe', 'I': CR + 'iron_sheet'})
ia('telescope', 'table', ['T', 'B', 'C'], {'T': MC + 'spyglass', 'B': CR + 'brass_sheet', 'C': CR + 'copper_sheet'})
ia('bomb_bay', 'table', ['ITI', 'ICI'], {'I': CR + 'iron_sheet', 'T': MC + 'tnt', 'C': CR + 'chute'})
# 기본 기체 7종 (기계식 조합기)
ia('gyrodyne', 'mech', [' S ', 'XPX', 'AHA'], {'S': IA + 'sail', 'X': CR + 'shaft', 'P': IA + 'propeller', 'A': CR + 'andesite_alloy', 'H': IA + 'hull'})
ia('biplane', 'mech', ['IHI', 'PEM', 'IHI'], {'I': CR + 'iron_sheet', 'H': IA + 'hull', 'P': IA + 'propeller', 'E': IA + 'engine', 'M': CR + 'precision_mechanism'})
ia('quadrocopter', 'mech', ['PBP', 'BEB', 'PMP'], {'P': IA + 'propeller', 'B': MC + 'bamboo', 'E': IA + 'engine', 'M': CR + 'precision_mechanism'})
ia('bamboo_hopper', 'mech', ['BHB', 'BAB', 'SES'], {'B': MC + 'bamboo_block', 'H': IA + 'hull', 'A': IA + 'biplane', 'S': IA + 'sail', 'E': IA + 'engine'})
ia('airship', 'mech', ['SSS', 'SSS', 'HME'], {'S': IA + 'sail', 'H': IA + 'hull', 'M': CR + 'precision_mechanism', 'E': IA + 'engine'})
ia('cargo_airship', 'mech', ['CAC', 'KHK'], {'C': MC + 'chest', 'A': IA + 'airship', 'K': CR + 'andesite_casing', 'H': IA + 'hull'})
ia('warship', 'mech', ['SHS', 'EAE', 'HGH', 'BMB'], {'S': IA + 'sail', 'H': IA + 'hull', 'E': IA + 'engine', 'A': IA + 'cargo_airship', 'G': IA + 'industrial_gears', 'B': CR + 'brass_casing', 'M': CR + 'precision_mechanism'})
# 화물 4종: 기본 기체 + 상자 2 + 안산암 케이스 2 + 선체 (+ 계열 부품)
own('cargo_copter', 'mech', ['CAC', 'KHK'], {'C': MC + 'chest', 'A': IA + 'quadrocopter', 'K': CR + 'andesite_casing', 'H': IA + 'hull'})
own('cargo_gyrodyne', 'mech', ['CAC', 'KHK', ' X '], {'C': MC + 'chest', 'A': IA + 'gyrodyne', 'K': CR + 'andesite_casing', 'H': IA + 'hull', 'X': IA + 'propeller'})
own('cargo_biplane', 'mech', ['CAC', 'KHK', ' X '], {'C': MC + 'chest', 'A': IA + 'biplane', 'K': CR + 'andesite_casing', 'H': IA + 'hull', 'X': IA + 'engine'})
own('cargo_seaplane', 'mech', ['CAC', 'KHK', ' X '], {'C': MC + 'chest', 'A': IA + 'bamboo_hopper', 'K': CR + 'andesite_casing', 'H': IA + 'hull', 'X': IA + 'sail'})
# 워십급 4종: 화물 기체에서 업그레이드
U = NEW + ':'
own('gigantia', 'mech', ['SSSSS', 'EEAEE', 'HBMBH'], {'S': IA + 'sail', 'E': IA + 'engine', 'A': U + 'cargo_biplane', 'H': IA + 'hull', 'B': CR + 'brass_casing', 'M': CR + 'precision_mechanism'})
own('pelican', 'mech', ['SHS', 'EAE', 'HGH', 'BMB'], {'S': IA + 'sail', 'H': IA + 'hull', 'E': IA + 'engine', 'A': U + 'cargo_seaplane', 'G': IA + 'industrial_gears', 'B': CR + 'brass_casing', 'M': CR + 'precision_mechanism'})
own('hawk', 'mech', ['P P', 'EAE', 'TMT'], {'P': IA + 'enhanced_propeller', 'E': IA + 'engine', 'A': U + 'cargo_copter', 'T': CR + 'sturdy_sheet', 'M': CR + 'precision_mechanism'})
own('dragonfly', 'mech', ['PSP', 'EAE', 'BVB'], {'P': IA + 'propeller', 'S': IA + 'sail', 'E': IA + 'engine', 'A': U + 'cargo_gyrodyne', 'B': CR + 'brass_casing', 'V': CR + 'item_vault'})

print('recipes:', count)
