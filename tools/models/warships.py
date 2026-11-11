from lib import Model


def pennant(m, x, y, z, h=8):
    m.cube('mast', [x - 0.3, y, z - 0.3], [x + 0.3, y + h, z + 0.3], 'rod'); m.cube('pennant', [x, y + h - 4, z - 10.5], [x, y + h, z - 0.5], 'flag')


def lantern(m, x, y, z):
    m.cube('lantern', [x - 1, y, z - 1], [x + 1, y + 3, z + 1], 'lantern'); m.cube('lantern_cap', [x - 0.5, y + 3, z - 0.5], [x + 0.5, y + 4, z + 0.5], 'brassrod')


def engine(m, x, y0, z0, z1, grp, r=5, prop='fan4', pr=13):
    for sx, tag in ((1, 'a'), (-1, 'b')):
        X = x * sx; g = grp + tag
        m.cube('engine', [X - r, y0, z0], [X + r, y0 + 2 * r, z1], 'tank'); m.cube('stack', [X - 1, y0 + 2 * r, z0 + 3], [X + 1, y0 + 2 * r + 4, z0 + 5], 'gun')
        m.cube('spinner', [X - 1.5, y0 + r - 1.5, z1], [X + 1.5, y0 + r + 1.5, z1 + 2.5], 'brassrod', g)
        m.cube('prop', [X - pr, y0 + r - pr, z1 + 1.5], [X + pr, y0 + r + pr, z1 + 1.5], prop, g); m.gorig[g] = [X, y0 + r, z1 + 1.5]


# ================= GIGANTIA (scale 1.0): six-engine giant biplane, raised bridge, no dummy turrets
m = Model('gigantia')
m.cube('floor', [-18, 10, -48], [18, 13, 48], 'hullw'); m.mir('side', [16, 13, -48], [18, 24, 48], 'hullw'); m.mir('armor', [18, 15, -40], [19, 21, 20], 'panel')
m.cube('front', [-16, 13, 46], [16, 24, 48], 'hullw'); m.rcube('nose', [-13, 10, 48.2], [13, 21, 60], 'hullw', [14, 0, 0], [0, 15, 48.2])
m.cube('dash', [-12, 16, 45.5], [12, 22, 46], 'dash')
m.cube('bulkhead', [-16, 13, 22], [16, 24, 24], 'hullw'); m.rcube('windshield', [-17, 24, 46.5], [17, 35, 47.5], 'window', [-22, 0, 0], [0, 24, 47])
m.cube('rear', [-16, 13, -48], [16, 24, -46], 'hullw'); m.rcube('tailcone', [-12, 11, -76], [12, 22, -48.2], 'hullw', [10, 0, 0], [0, 16, -48.2])
for z in (-8, -22, -36):
    m.chest(-15, 13, z, 'e'); m.chest(1, 13, z, 'e')
m.seat(-8, 15, 34); m.seat(8, 15, 34); m.seat(-8, 15, 12); m.seat(8, 15, 12)
m.mir('wing_low_a', [18, 11, -8], [98, 13, 26], 'sailc'); m.mir('wing_low_b', [98, 11, -6], [168, 13, 24], 'sailc')
m.cube('wing_top_c', [-44, 44, -10], [44, 46, 28], 'sailc'); m.mir('wing_top_m', [44, 44, -10], [130, 46, 28], 'sailc'); m.mir('wing_top_o', [130, 44, -6], [216, 46, 24], 'sailc')
for x in (34, 74, 114, 154):
    m.mir('strut', [x + 7, 13, -4], [x + 8.5, 44, -2.5], 'rod'); m.mir('strut', [x + 7, 13, 20], [x + 8.5, 44, 21.5], 'rod')
m.rmir('tip_strut', [167, 13, 8], [168.5, 58, 9.5], 'rod', [0, 0, -47], [167.75, 13, 8.75])
m.mir('cabane', [16.2, 24, 0], [17.7, 44, 1.5], 'rod'); m.mir('cabane', [16.2, 24, 16], [17.7, 44, 17.5], 'rod')
for i, x in enumerate((34, 74, 114)):
    engine(m, x, 23, 4, 28, 'propellor_%d' % i, r=6, pr=16); m.mir('engine_mount', [x - 1, 13, 10], [x + 1, 23, 22], 'girder')
m.mir('driveshaft', [18, 28, 15], [108, 29.5, 16.5], 'brassrod')
m.mir('boom', [32, 28, -128], [36, 32, -8], 'girder'); m.mir('stab', [0, 32, -134], [70, 34, -112], 'sailc')
m.rmir('fin', [33.5, 34, -136], [34.5, 58, -114], 'sailc', [-12, 0, 0], [34, 34, -118]); m.rcube('rudder', [-0.5, 34, -136], [0.5, 52, -116], 'sailc', [-12, 0, 0], [0, 34, -120], 'rudder')
m.mir('boom_brace', [18, 22, -46], [32, 24, -44], 'girder')
m.mir('stab_up', [0, 54, -140], [60, 56, -120], 'sailc'); m.mir('stab_post', [58, 34, -128], [59.5, 54, -126.5], 'rod')
m.mir('gondola', [40, 3, -6], [50, 11, 24], 'hullw'); m.rmir('gondola_nose', [41, 4, 24.2], [49, 11, 25.2], 'window', [35, 0, 0], [45, 11, 24.7])
m.mir('wheel', [50, 0, 4], [52, 8, 12], 'wheel'); m.mir('wheel', [38, 0, 4], [40, 8, 12], 'wheel')
m.mir('nosewheel', [2, 0, 32], [4, 8, 40], 'wheel'); m.cube('nose_strut', [-2, 4, 35], [2, 10, 37], 'girder'); m.mir('tail_skid', [33.5, 18, -122], [34.5, 28, -121], 'rod')
m.mir('lattice', [84, 13, 8.75], [106, 44, 8.75], 'net'); m.mir('lattice', [124, 13, 8.75], [160, 44, 8.75], 'net'); m.mir('boom_net', [34, 32, -110], [34, 44, -60], 'net')
m.cube('cargo_net', [-15.4, 27.4, -36], [15.4, 27.4, 6], 'net'); m.mir('rail_net', [17, 24, -46], [17, 29, 20], 'net'); m.mir('rail_post', [16.5, 24, -47], [17.5, 29.5, -46], 'rod')
m.mir('wing_light', [213, 46, 8], [215, 48, 10], 'lantern'); lantern(m, 0, 21.2, 56); pennant(m, 0, 52, -124); m.mir('rope_coil', [10, 13, 26], [14, 14.5, 30], 'rope')
m.cube('ladder', [18.4, 3, 30], [18.4, 13, 36], 'net'); m.mir('crate', [20, 13, -4], [28, 19, 4], 'crate')
m.mounts = [dict(ROTATING=[(0, 46, 9)], FRONT=[(-45, 11, 27), (45, 11, 27)], DROP=[(-45, 3, 8), (45, 3, 8)]),
            dict(ROTATING=[(0, 24, -47)], FRONT=[(0, 21, 60)], DROP=[(0, 10, -10)])]
m.build()

# ================= PELICAN (scale 1.0): blunt-nose sea skimmer; two shoulder engines + two tail engines that only run in the air
m = Model('pelican')
m.cube('keel', [-7, 3, -44], [7, 8, 34], 'hullw'); m.cube('floor', [-14, 8, -56], [14, 12, 40], 'hullw'); m.mir('side', [12, 12, -56], [14, 20, 40], 'hullw'); m.mir('armor', [14, 13, -50], [15, 19, -6], 'panel')
m.rcube('nose', [-11.8, 8, 40.2], [11.8, 22, 54], 'hullw', [16, 0, 0], [0, 15, 40.2]); m.cube('front', [-12, 12, 38], [12, 22, 40], 'hullw')
m.cube('dash', [-10, 15, 37.5], [10, 20, 38], 'dash')
m.rcube('windshield', [-13, 22, 38.5], [13, 33, 39.5], 'window', [-30, 0, 0], [0, 22, 39]); m.mir('cab_side', [12, 20, -4], [14, 22, 38], 'hullw')
m.cube('bulkhead', [-12, 12, -6], [12, 22, -4], 'hullw')
m.seat(-6, 14, 23); m.seat(6, 14, 23); m.seat(-6, 14, 6); m.seat(6, 14, 6)
m.cube('rear', [-12, 12, -56], [12, 20, -54], 'hullw'); m.rcube('stern', [-9, 10, -80], [9, 19, -56.2], 'hullw', [14, 0, 0], [0, 14, -56.2])
for z0 in (-19, -32):
    m.mir('crate', [1, 12, z0], [12, 22, z0 + 11], 'crate')
m.chest(-7, 12, -48, 'e')
m.mir('pylon', [14, 26, 6], [19, 29, 18], 'girder')
engine(m, 25, 24, 2, 26, 'propellor_0', r=6, pr=15)
for sx, g in ((1, 'rear_a'), (-1, 'rear_b')):
    X = 25 * sx
    m.cube('engine_aft', [X - 6, 24, -26], [X + 6, 36, -2], 'tank'); m.cube('stack', [X - 1, 36, -9], [X + 1, 40, -7], 'gun'); m.cube('engine_link', [X - 2, 27, -2], [X + 2, 33, 2], 'girder')
    m.cube('spinner', [X - 1.5, 28.5, -28.5], [X + 1.5, 31.5, -26], 'brassrod', g); m.cube('prop', [X - 15, 15, -27.5], [X + 15, 45, -27.5], 'fan4b', g); m.gorig[g] = [X, 30, -27.5]
m.mir('pylon_aft', [14, 26, -20], [19, 29, -8], 'girder')
m.rmir('wing', [14, 20, -34], [75, 23, 14], 'sailc', [0, 0, -13], [14, 21.5, -10])
m.mir('pontoon', [66, 1, -40], [78, 10, 22], 'hullw'); m.rmir('pontoon_bow', [66.2, 1, 21], [77.8, 8, 34], 'hullw', [-26, 0, 0], [72, 1, 21]); m.mir('pontoon_cap', [67, 10, -36], [77, 11, 18], 'panel')
m.rmir('tip', [78, 7, -24], [96, 9, 6], 'sailc', [0, 0, 24], [78, 8, -9])
m.rmir('strake', [14, 14, -52], [32, 16, -38], 'sailc', [0, 0, -18], [14, 15, -45])
m.rmir('fin', [5, 22, -66], [7, 64, -42], 'sailc', [0, 0, -28], [6, 22, -54])
m.cube('stab_c', [-30, 58, -70], [30, 60, -44], 'sailc'); m.mir('stab_o', [30, 58, -68], [72, 60, -46], 'sailc'); m.mir('stab_tip', [72, 56, -68], [74, 62, -46], 'panel')
m.cube('radar', [-3, 60, -60], [3, 64, -54], 'panel'); m.cube('radar_dish', [-5, 64, -62], [5, 65, -52], 'sailc')
m.mir('rail_net', [13, 20, -54], [13, 26, -8], 'net'); m.mir('rail_post', [12.5, 20, -55], [13.5, 26.5, -54], 'rod'); m.mir('rail_post', [12.5, 20, -8], [13.5, 26.5, -7], 'rod')
m.cube('cargo_net', [0.6, 22.4, -33], [12.4, 22.4, -7], 'net'); m.cube('cargo_net', [-12.4, 22.4, -33], [-0.6, 22.4, -7], 'net'); m.mir('rope_coil', [-11, 12, -53], [-7, 13.5, -49], 'rope')
m.mir('bow_light', [71, 10, 26], [73, 12, 28], 'lantern'); pennant(m, 0, 65, -57, 9); m.mir('fender', [78.3, 3, -20], [78.3, 8, 0], 'net')
m.mounts = [dict(ROTATING=[(0, 22, -5)], FRONT=[(-25, 36, 14), (25, 36, 14)], DROP=[(-72, 1, 0), (72, 1, 0)]),
            dict(ROTATING=[(0, 65, -57)], FRONT=[(-72, 11, 10), (72, 11, 10)], DROP=[(0, 8, -32)])]
m.build()

# ================= HAWK (scale 1.3): tandem open cockpit gunship, two huge engines canted outward, each driving a rotor
m = Model('hawk', scale=1.3)
m.cube('floor', [-8, 6, -30], [8, 9, 34], 'hullw'); m.mir('side_low', [7, 9, -30], [8, 13, 34], 'panel'); m.mir('side_up', [7, 22, -30], [8, 26, -6], 'panel')
m.rcube('nose', [-6, 5, 34.2], [6, 13, 46], 'hullw', [18, 0, 0], [0, 9, 34.2])
m.rcube('gunner_glass', [-7, 13, 33], [7, 20, 34], 'window', [-25, 0, 0], [0, 13, 33.5]); m.mir('gunner_side', [7, 13, 20], [8, 17, 31], 'window')
m.cube('gunner_dash', [-5, 10, 33.5], [5, 13, 34], 'dash')
m.cube('step', [-7, 9, 16], [7, 19, 18], 'hullw'); m.cube('pilot_floor', [-7, 9, -4], [7, 13, 16], 'hullw'); m.cube('pilot_dash', [-5, 14, 15.5], [5, 18, 16], 'dash')
m.rcube('pilot_glass', [-7, 19, 16.5], [7, 25, 17.5], 'window', [-30, 0, 0], [0, 19, 17]); m.mir('pilot_rim', [7, 13, -4], [8, 19, 18], 'panel')
m.cube('mid', [-7, 9, -6], [7, 26, -4], 'hullw'); m.cube('roof', [-8, 26, -30], [8, 28, -4], 'panel'); m.cube('rear', [-7, 9, -30], [7, 26, -28], 'hullw')
m.seat(0, 15, 4); m.seat(0, 11, 24)
m.chest(-7, 9, -20, 'e'); m.cube('crate', [-6, 9, -27.5], [6, 17, -20.5], 'crate')
for sx, tex, grp in ((1, 'heli2', 'propellor_0'), (-1, 'heli2b', 'propellor_1')):
    o = [9 * sx, 27, -13]; rz = -16 * sx; tg = 'tilt_r' if sx > 0 else 'tilt_l'
    m.gdef[tg] = dict(origin=o, rotation=[0, 0, rz]); m.gdef[grp] = dict(origin=[11 * sx, 54, -13], parent=tg)
    X = lambda a, b: (a, b) if sx > 0 else (-b, -a)
    x0, x1 = X(5, 19); m.cube('engine', [x0, 26, -28], [x1, 40, 2], 'tank', tg)
    x0, x1 = X(8, 16); m.cube('engine_cap', [x0, 40, -21], [x1, 43, -5], 'panel', tg)
    x0, x1 = X(10, 12); m.cube('mast', [x0, 43, -14], [x1, 54.5, -12], 'rod', tg)
    x0, x1 = X(8.5, 13.5); m.cube('hub', [x0, 52, -15.5], [x1, 53.5, -10.5], 'brassrod', grp)
    x0, x1 = X(11 - 52, 11 + 52); m.cube('rotor', [x0, 54, -65], [x1, 54, 39], tex, grp)
    x0, x1 = X(10, 14); m.cube('exhaust', [x0, 30, -38], [x1, 34, -28], 'gun', tg)
m.cube('gear_bridge', [-4.5, 28, -19], [4.5, 32, -7], 'girder')
m.rmir('stub', [8, 14, -10], [34, 16, 8], 'panel', [0, 0, -8], [8, 15, -2]); m.rmir('stub_tip', [34, 13.5, -11], [35.5, 16.5, 9], 'brassrod', [0, 0, -8], [8, 15, -2])
m.rcube('boom', [-3, 18, -78], [3, 25, -30.2], 'hullw', [7, 0, 0], [0, 21, -30.2])
m.rmir('vfin', [0.2, 26, -84], [1.2, 46, -68], 'sailc', [0, 0, -32], [0.7, 26, -76])
m.mir('wheel', [10, 0, 10], [12, 7, 17], 'wheel'); m.mir('leg', [10.5, 7, 13], [11.5, 13, 14], 'rod'); m.mir('axle', [8, 3, 13], [10, 4, 14], 'rod'); m.rcube('tail_skid', [-0.5, 12, -72], [0.5, 22, -70], 'rod', [25, 0, 0], [0, 22, -71])
m.cube('antenna', [-0.5, 28, -27], [0.5, 40, -26], 'rod'); m.cube('pennant', [0, 36, -37], [0, 40, -27], 'flag')
m.mir('ammo_box', [1.5, 28, -27.5], [6.5, 31, -22], 'crate'); lantern(m, 0, 13.2, 44); m.cube('tail_light', [-1, 25, -79], [1, 27, -77], 'lantern')
m.mounts = [dict(ROTATING=[(-27.7, 6.2, 0), (27.7, 6.2, 0)], FRONT=[(0, 1.8, 28)], DROP=[(0, 5, 6)]),
            dict(ROTATING=[(-16.9, 7.8, 0), (16.9, 7.8, 0)], FRONT=[(0, 1.8, -14)], DROP=[(0, 5, -22)])]
m.build()

# ================= DRAGONFLY (scale 1.2): twin outrigger rotors, vault slung under the belly, fuel tank on the spine
m = Model('dragonfly', scale=1.2)
m.cube('floor', [-11, 22, -40], [11, 25, 36], 'hullw'); m.mir('side', [9, 25, -40], [11, 34, 36], 'hullw'); m.mir('armor', [11, 27, -34], [12, 32, 8], 'panel')
m.rcube('nose_low', [-9, 22, 36.2], [9, 30, 46], 'hullw', [-18, 0, 0], [0, 22, 36.2])
m.rcube('nose_glass', [-10, 30, 35], [10, 42, 36], 'window', [-28, 0, 0], [0, 30, 35.5])
m.cube('dash', [-8, 27, 34], [8, 31, 34.5], 'dash')
m.cube('bulkhead', [-9, 25, 10], [9, 34, 12], 'hullw'); m.mir('frame_post', [9, 34, 10], [11, 48, 12], 'girder'); m.mir('frame_post', [9, 34, -32], [11, 48, -30], 'girder'); m.cube('frame_beam', [-11, 48, -32], [11, 50, -30], 'girder'); m.mir('frame_beam_f', [4, 48, 10], [11, 50, 12], 'girder'); m.mir('frame_rail', [9, 48, -30], [11, 50, 10], 'girder')
m.seat(-4.5, 27, 22); m.seat(4.5, 27, 22)
m.cube('rear', [-9, 25, -40], [9, 34, -38], 'hullw'); m.chest(-9, 25, -8, 'e'); m.chest(-5, 25, -22, 'w'); m.chest(-9, 25, -36, 'e')
m.cube('spine', [-4, 48, -30], [4, 52, 14], 'girder'); m.cube('fuel_tank', [-3, 52, -28], [3, 58, -10], 'tank')
m.rmir('outrigger', [4, 47, -6], [70, 52, 6], 'girder', [0, 0, 9], [4, 49.5, 0]); m.rmir('brace', [11.2, 26, -1], [12.7, 76, 0.5], 'rod', [0, 0, -63], [11.95, 26, -0.25])
for sgn, grp, tex in ((1, 'propeller_left', 'heli3'), (-1, 'propeller_right', 'heli3b')):
    x = 68 * sgn; side = 'left' if sgn > 0 else 'right'
    m.cube('nacelle', [x - 7, 52, -14], [x + 7, 66, 12], 'tank'); m.cube('nacelle_cap', [x - 5, 66, -8], [x + 5, 69, 8], 'panel')
    m.cube('shaft', [x - 1, 69, -1], [x + 1, 76.5, 1], 'rod'); m.cube('hub', [x - 2.5, 74, -2.5], [x + 2.5, 75.5, 2.5], 'brassrod', grp)
    m.cube('rotor', [x - 44, 76, -44], [x + 44, 76, 44], tex, grp); m.gorig[grp] = [x, 76, 0]
    m.cube('thrust', [x - 12, 47, 13.5], [x + 12, 71, 13.5], 'fan4', 'propellor_' + side); m.gorig['propellor_' + side] = [x, 59, 13.5]
    m.cube('stack', [x - 1, 66, -13], [x + 1, 72, -11], 'gun')
m.cube('vault', [-9, 3, -26], [9, 21, 22], 'vault'); m.mir('strap', [9, 2, -16], [10, 22, -13], 'brassrod'); m.mir('strap', [9, 2, 9], [10, 22, 12], 'brassrod')
m.cube('strap_top', [-9, 21, -16], [9, 22, -13], 'brassrod'); m.cube('strap_top', [-9, 21, 9], [9, 22, 12], 'brassrod')
m.rmir('leg', [12.2, 3, 26], [14.2, 26, 28], 'girder', [0, 0, 22], [13.2, 24, 27]); m.rmir('leg', [12.2, 3, -32], [14.2, 26, -30], 'girder', [0, 0, 22], [13.2, 24, -31])
m.mir('wheel', [20, 0, 23], [22, 8, 31], 'wheel'); m.mir('wheel', [20, 0, -35], [22, 8, -27], 'wheel')
m.rcube('boom', [-4, 26, -84], [4, 33, -40.2], 'hullw', [8, 0, 0], [0, 29, -40.2]); m.rcube('fin', [-0.5, 36, -92], [0.5, 58, -76], 'sailc', [-14, 0, 0], [0, 36, -80]); m.mir('stab', [0.5, 52, -98], [24, 54, -84], 'sailc')
m.mir('vault_net', [10.4, 3, -26], [10.4, 21, 22], 'net'); m.cube('vault_net', [-9, 3, 22.4], [9, 21, 22.4], 'net'); m.cube('cargo_net', [-9, 39.4, -36], [9, 39.4, 6], 'net')
m.mir('rail_net', [10, 34, -30], [10, 40, 10], 'net'); pennant(m, 0, 57, -84, 7)
for sgn in (1, -1):
    lantern(m, 68 * sgn, 48, -6) if False else m.cube('nav_light', [68 * sgn - 1, 49, -16], [68 * sgn + 1, 51, -14], 'lantern')
m.cube('rope_coil', [-8, 25, 13], [-4, 26.5, 17], 'rope'); m.cube('hook_chain', [-0.5, 0, -2], [0.5, 3, -1], 'brassrod')
m.mounts = [dict(ROTATING=[(0, 52, 8)], FRONT=[(-16, 54, 0), (16, 54, 0)], DROP=[(-15, 22, -20), (15, 22, -20)])]
m.build()

# ================= HAWK weapons (drawn only when the weapon sits on a Hawk)
m = Model('hawk_ballista', TW=64)       # origin = mount point under the belly; the bracket reaches up to the hull
m.cube('bracket', [-1, 5, -3], [1, 5.6, 3], 'girder'); m.cube('stock', [-1.5, 0, -11], [1.5, 3, 12], 'wood'); m.cube('rail', [-0.5, 3, -9], [0.5, 4, 12], 'gun')
m.rmir('arm', [1.5, 0.5, 7], [14, 2.5, 9], 'wood', [0, 22, 0], [1.5, 1.5, 8]); m.rmir('arm_tip', [13, 0.2, 6.8], [15, 2.8, 9.2], 'brassrod', [0, 22, 0], [1.5, 1.5, 8])
m.rmir('string', [0, 1.3, -6.3], [15.5, 1.7, -5.7], 'rod', [0, -38, 0], [0, 1.5, -6])
m.cube('bolt', [-0.5, 4, -6], [0.5, 5, 17], 'gun'); m.cube('bolt_head', [-1, 3.5, 17], [1, 5.5, 20], 'brassrod'); m.cube('winch', [-3, 0.5, -11.5], [3, 2.5, -10], 'brassrod')
m.build()

m = Model('hawk_autocannon', TW=64)     # origin = gun axis; the pylon reaches up to the wing
m.cube('plate', [-3, 5.6, -3], [3, 6.6, 3], 'panel'); m.cube('pylon', [-1, 2.5, -1.5], [1, 5.6, 1.5], 'girder')
m.gdef = {'yaw': dict(origin=[0, 0, 0]), 'pitch': dict(origin=[0, 0, 0], parent='yaw'), 'roll': dict(origin=[0, 0, 0], parent='pitch')}
m.anim = {'yaw': {'y': '-variable.yaw'}, 'pitch': {'x': 'variable.pitch'}, 'roll': {'z': '-variable.roll'}}
m.cube('breech', [-2.5, -2.5, -7], [2.5, 2.5, 3], 'panel', 'pitch'); m.cube('ammo', [2.5, -2, -5], [5, 2, 1], 'hullw', 'pitch'); m.cube('feed', [1.2, 2.5, -2], [2.2, 3.2, 0], 'brassrod', 'pitch')
for dx, dy in ((-0.9, -0.9), (0.9, -0.9), (-0.9, 0.9), (0.9, 0.9)):
    m.cube('barrel', [dx - 0.5, dy - 0.5, 3], [dx + 0.5, dy + 0.5, 18], 'gun', 'roll')
m.cube('muzzle', [-1.7, -1.7, 15], [1.7, 1.7, 16], 'brassrod', 'roll'); m.cube('collar', [-1.9, -1.9, 3.2], [1.9, 1.9, 4.5], 'brassrod', 'roll')
m.build()
