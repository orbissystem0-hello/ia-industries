from lib import Model
S = 1.3


def pennant(m, x, y, z, h=6):
    m.cube('mast', [x - 0.3, y, z - 0.3], [x + 0.3, y + h, z + 0.3], 'rod'); m.cube('pennant', [x, y + h - 3, z - 7.5], [x, y + h, z - 0.5], 'flag')


def lantern(m, x, y, z):
    m.cube('lantern', [x - 1, y, z - 1], [x + 1, y + 3, z + 1], 'lantern'); m.cube('lantern_cap', [x - 0.5, y + 3, z - 0.5], [x + 0.5, y + 4, z + 0.5], 'brassrod')


def stick(m, z, y):
    m.rcube('stick', [-0.5, y, z], [0.5, y + 5, z + 1], 'rod', [20, 0, 0], [0, y, z + 0.5])
    m.cube('stick_knob', [-1, y + 4.6, z + 1.4], [1, y + 6.2, z + 3], 'brassrod')


# ============ cargo copter: coaxial utility heli, open cockpit, twin booms, hollow rear with two chests
m = Model('cargo_copter', scale=S)
m.cube('cab_floor', [-7, 5, 6], [7, 8, 20], 'wood'); m.cube('cab_front', [-7, 8, 18], [7, 12, 20], 'casing'); m.mir('cab_side', [5, 8, 6], [7, 12, 18], 'wood')
m.cube('dash', [-5, 9, 17.5], [5, 12, 18], 'dash'); m.rcube('windshield', [-7, 12, 19], [7, 18, 20], 'window', [-22, 0, 0], [0, 12, 19.5])
m.cube('cab_back', [-7, 5, 4], [7, 20, 6], 'casing'); m.seat(0, 10, 10); stick(m, 14.5, 8)
m.cube('hull_top', [-8, 20, -26], [8, 21, 4], 'sail'); m.mir('hull_side', [7, 16, -26], [8, 20, 4], 'sail'); m.cube('deck', [-7, 3, -26], [7, 5, 4], 'wood')
m.chest(-7, 5, -10, 'e'); m.chest(-7, 5, -24, 'w')
m.cube('gearbox', [-3, 21, -9], [3, 28, -1], 'casing'); m.mir('engine', [3, 21, -10], [9, 27, 0], 'engine'); m.mir('stack', [5, 27, -9], [7, 31, -7], 'gun')
m.cube('shaft', [-1, 28, -6], [1, 37, -4], 'rod'); m.cube('cog', [-6, 29.5, -11], [6, 29.5, 1], 'cog', 'propellor_0')
m.cube('rotor', [-26, 33, -31], [26, 33, 21], 'prop2', 'propellor_0'); m.cube('rotor', [-26, 36.5, -31], [26, 36.5, 21], 'prop2', 'propellor_1', rot=[0, 90, 0], origin=[0, 36.5, -5])
m.gorig = {'propellor_0': [0, 33, -5], 'propellor_1': [0, 36.5, -5]}
m.mir('boom', [5, 18, -50], [7, 20, -26], 'wood'); m.cube('stab', [-13, 20, -52], [13, 21, -45], 'sail'); m.rmir('fin', [13, 14, -53], [14, 28, -45], 'sail', [-10, 0, 0], [13.5, 20, -49])
m.rmir('brace', [5.5, 6, -27], [6.5, 20, -26.2], 'rod', [-38, 0, 0], [6, 6, -26.6])
m.mir('leg_f', [8, 2, 12], [9, 8, 13], 'rod'); m.mir('wheel', [9, 0, 10], [11, 5, 15], 'wheel')
m.mir('leg_r', [8, 2, -20], [9, 16, -19], 'rod'); m.mir('wheel', [9, 0, -22], [11, 5, -17], 'wheel')
m.mir('cargo_net', [7.4, 5, -25], [7.4, 16, 3], 'net'); m.cube('tool_crate', [-7, 21, -25], [-2, 25, -19], 'crate'); m.cube('rope_coil', [2, 21, -24], [6, 22.5, -20], 'rope')
pennant(m, 13.5, 27, -49)
m.mounts = [dict(ROTATING=[(0, 21, -15)], FRONT=[(0, 8, 21)], DROP=[(0, 3, -10)])]
m.build()

# ============ cargo gyrodyne: compound gyroplane, open cockpit, high stub wings with tip engines, roof fuel tank
m = Model('cargo_gyrodyne', scale=S)
m.cube('floor', [-9, 3, -24], [9, 6, 24], 'wood'); m.mir('cab_side', [7, 6, 8], [9, 12, 22], 'wood'); m.cube('cab_front', [-9, 6, 22], [9, 12, 24], 'casing')
m.rcube('nose', [-6, 4, 24], [6, 10, 29], 'casing', [20, 0, 0], [0, 7, 24])
m.cube('dash', [-6, 7, 21.5], [6, 11, 22], 'dash'); m.rcube('windshield', [-8, 12, 22.5], [8, 18, 23.5], 'window', [-20, 0, 0], [0, 12, 23])
m.cube('bulkhead', [-9, 6, 6], [9, 22, 8], 'casing'); m.seat(0, 8, 13); stick(m, 17.5, 6)
m.cube('roof', [-9, 22, -24], [9, 23, 8], 'sail'); m.mir('post', [8, 6, -24], [9, 22, -23], 'rod'); m.mir('rail', [8, 6, -22], [9, 9, 6], 'wood')
m.chest(-7, 6, -8, 'e'); m.chest(-7, 6, -22, 'w')
m.mir('wing', [9, 21, -10], [36, 22, 4], 'sail'); m.mir('pod', [30, 18, -9], [38, 26, 5], 'engine'); m.mir('stack', [33, 26, -7], [35, 29, -5], 'gun')
m.cube('prop', [24, 12, 6.5], [44, 32, 6.5], 'prop4', 'propellor_left'); m.cube('prop', [-44, 12, 6.5], [-24, 32, 6.5], 'prop4', 'propellor_right')
m.rmir('wing_brace', [8.5, 8, -4], [9.5, 30, -3], 'rod', [0, 0, -58], [9, 8, -3.5])
m.cube('pylon', [-4, 23, -11], [4, 29, -1], 'casing'); m.cube('gearbox', [-3, 29, -9], [3, 33, -3], 'engine'); m.cube('shaft', [-1, 33, -7], [1, 38, -5], 'rod')
m.cube('fuel_tank', [-4, 23, -22], [4, 30, -12], 'tank'); m.cube('fuel_pipe', [-0.5, 27, -12], [0.5, 28, -11], 'brassrod')
m.cube('cog', [-6, 34.5, -12], [6, 34.5, 0], 'cog', 'propeller'); m.cube('rotor', [-32, 37, -38], [32, 37, 26], 'heli4', 'propeller')
m.gorig = {'propeller': [0, 37, -6], 'propellor_left': [34, 22, 6.5], 'propellor_right': [-34, 22, 6.5]}
m.rcube('boom', [-3, 16, -46], [3, 21, -24], 'wood', [8, 0, 0], [0, 18.5, -24])
m.cube('stab', [-17, 23, -50], [17, 24, -42], 'sail'); m.rmir('fin', [17, 17, -51], [18, 33, -42], 'sail', [-12, 0, 0], [17.5, 23, -46])
m.mir('wheel', [9, 0, 10], [11, 5, 15], 'wheel'); m.mir('wheel', [9, 0, -16], [11, 5, -11], 'wheel')
m.mir('cargo_net', [9.4, 9, -22], [9.4, 22, 6], 'net'); m.mir('wing_light', [35, 22, -4], [37, 24, -2], 'lantern')
pennant(m, 17.5, 32, -46); m.cube('rope_coil', [-7, 23, 1], [-3, 24.5, 5], 'rope')
m.mounts = [dict(ROTATING=[(0, 23, 3)], FRONT=[(0, 10.5, 29)], DROP=[(12, 3, 0), (-12, 3, 0)])]
m.build()

# ============ cargo biplane: twin-engine transport, open cockpit under a raised top wing
m = Model('cargo_biplane', scale=S)
m.cube('floor', [-7, 4, -24], [7, 7, 26], 'wood'); m.mir('side', [5, 7, 8], [7, 13, 26], 'wood')
m.cube('nose', [-6, 5, 26], [6, 12, 31], 'casing'); m.rcube('nose_tip', [-5, 5, 30], [5, 10, 37], 'casing', [16, 0, 0], [0, 8, 30])
m.cube('dash', [-5, 8, 25.5], [5, 12, 26], 'dash'); m.rcube('windshield', [-7, 13, 24.5], [7, 19, 25.5], 'window', [-32, 0, 0], [0, 13, 25])
m.cube('bulkhead', [-7, 7, 6], [7, 20, 8], 'casing'); m.seat(0, 9, 14); stick(m, 18.5, 7)
m.cube('rear', [-5, 7, -24], [5, 13, -22], 'casing')
m.chest(-7, 7, -8, 'e'); m.chest(-7, 7, -22, 'w')
m.cube('wing_top', [-64, 26, 0], [64, 27, 18], 'sail'); m.mir('wing_low', [7, 5, 2], [34, 6, 16], 'sail')
m.rmir('strut', [33, 6, 5], [34, 34, 6], 'rod', [0, 0, -45], [33.5, 6, 5.5]); m.rmir('strut', [33, 6, 12], [34, 34, 13], 'rod', [0, 0, -45], [33.5, 6, 12.5])
m.mir('cabane', [7, 7, 1], [8, 26, 2], 'rod'); m.mir('cabane', [7, 7, -6], [8, 26, -5], 'rod')
m.mir('pod', [22, 18, 2], [30, 26, 18], 'engine'); m.cube('prop', [16, 12, 19.5], [36, 32, 19.5], 'prop4', 'propellor_left'); m.cube('prop', [-36, 12, 19.5], [-16, 32, 19.5], 'prop4', 'propellor_right')
m.gorig = {'propellor_left': [26, 22, 19.5], 'propellor_right': [-26, 22, 19.5], 'rudder': [0, 20, -44]}
m.rcube('tail', [-4, 6, -48], [4, 12, -24.2], 'wood', [9, 0, 0], [0, 9, -24.2])
m.cube('stab', [-18, 13, -52], [18, 14, -42], 'sail'); m.rcube('fin', [-0.5, 14, -53], [0.5, 30, -43], 'sail', [-18, 0, 0], [0, 14, -45], 'rudder')
m.mir('wheel', [9, 0, 8], [11, 5, 13], 'wheel'); m.cube('axle', [-9, 2, 10], [9, 3, 11], 'rod'); m.mir('gear', [5, 3, 10], [6, 4, 11], 'rod'); m.cube('nosewheel', [-1, 0, 26], [1, 5, 31], 'wheel')
m.mir('cargo_net', [7.4, 7, -22], [7.4, 21, 6], 'net'); m.cube('cargo_net_top', [-7, 21.4, -22], [7, 21.4, 6], 'net')
m.mir('wing_wire', [44, 6, 9], [44, 26, 9], 'rod'); m.mir('wing_light', [62, 27, 8], [64, 29, 10], 'lantern'); pennant(m, 0, 27, -50, 5)
m.mounts = [dict(ROTATING=[(0, 20, 7)], FRONT=[(-30, 6, 9), (30, 6, 9)], DROP=[(-20, 4, 9), (20, 4, 9)])]
m.build()

# ============ cargo seaplane: parasol-wing flying boat, open bow cockpit, wing floats
m = Model('cargo_seaplane', scale=S)
m.cube('keel', [-5, 0, -22], [5, 3, 30], 'wood'); m.cube('floor', [-10, 3, -28], [10, 6, 32], 'wood'); m.mir('side', [8, 6, -28], [10, 13, 32], 'wood')
m.rcube('bow', [-9, 3, 31], [9, 10, 42], 'wood', [-24, 0, 0], [0, 3, 31]); m.cube('bow_wall', [-8, 6, 32], [8, 13, 34], 'casing')
m.cube('dash', [-6, 8, 31.5], [6, 12, 32], 'dash'); m.rcube('windshield', [-8, 13, 32.5], [8, 19, 33.5], 'window', [-24, 0, 0], [0, 13, 33])
m.cube('bulkhead', [-8, 6, 12], [8, 20, 14], 'casing'); m.seat(0, 8, 20); stick(m, 24.5, 6)
m.cube('rear', [-8, 6, -28], [8, 13, -26], 'casing')
m.chest(-7, 6, -4, 'e'); m.chest(-7, 6, -18, 'w')
m.cube('wing', [-72, 32, -6], [72, 33, 14], 'sail')
m.mir('pylon', [9, 13, 10], [10, 32, 11], 'rod'); m.mir('pylon', [9, 13, -4], [10, 32, -3], 'rod')
m.rmir('brace', [9.5, 13, 3], [10.5, 49, 4], 'rod', [0, 0, -57.5], [10, 13, 3.5])
m.mir('pod', [20, 24, -2], [28, 32, 15], 'engine'); m.cube('prop', [12, 16, 16.5], [36, 40, 16.5], 'prop4', 'propellor_left'); m.cube('prop', [-36, 16, 16.5], [-12, 40, 16.5], 'prop4', 'propellor_right')
m.gorig = {'propellor_left': [24, 28, 16.5], 'propellor_right': [-24, 28, 16.5]}
m.mir('float', [54, 8, -4], [60, 13, 12], 'wood'); m.rmir('float_bow', [54.2, 8, 11], [59.8, 12, 17], 'wood', [-28, 0, 0], [57, 8, 11]); m.mir('float_strut', [56, 13, -1], [57, 32, 0], 'rod'); m.mir('float_strut', [56, 13, 8], [57, 32, 9], 'rod')
m.rcube('stern', [-6, 5, -54], [6, 11, -28.2], 'wood', [11, 0, 0], [0, 8, -28.2])
m.rcube('fin', [-0.5, 13, -60], [0.5, 32, -48], 'sail', [-14, 0, 0], [0, 13, -50]); m.cube('stab', [-20, 25, -62], [20, 26, -52], 'sail')
m.cube('cargo_net_top', [-7.6, 20.4, -18], [7.6, 20.4, 10], 'net'); m.mir('rail_net', [9.6, 13, -27], [9.6, 18, -6], 'net'); m.mir('rail_post', [9, 13, -28], [10, 18.5, -27], 'rod')
m.cube('rope_coil', [-4, 6, 26.5], [0, 7.5, 30.5], 'rope'); m.mir('wing_light', [70, 33, 3], [72, 35, 5], 'lantern'); pennant(m, 0, 31, -57, 5)
m.mounts = [dict(ROTATING=[(0, 20, 13)], FRONT=[(-40, 33, 6), (40, 33, 6)], DROP=[(-40, 31, 4), (40, 31, 4)]),
            dict(ROTATING=[(0, 13, -27)], FRONT=[(-57, 13, 10), (57, 13, 10)], DROP=[(-57, 8, 0), (57, 8, 0)])]
m.build()
