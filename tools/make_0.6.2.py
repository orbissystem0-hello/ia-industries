#!/usr/bin/env python3
"""ia_upgraded 0.2.0 (proj) -> 0.3.0 (proj3): new models, open cockpits, fuel, powered gyrodynes, pelican rear engines, hawk weapons."""
import json, os, re, shutil, subprocess
from PIL import Image

SRC = '/home/claude/build/proj'; OUT = '/home/claude/build/proj8'; M2 = '/home/claude/build/m2'; MO = M2 + '/out'
NS = 'ia_upgraded'; VERSION = '0.6.2'
if os.path.exists(OUT): shutil.rmtree(OUT)
shutil.copytree(SRC + '/resources', OUT + '/resources'); shutil.copytree(SRC + '/src', OUT + '/src')
res = OUT + '/resources'; ent = OUT + '/src/kr/aerosky/iaupgraded/entity'; cli = OUT + '/src/kr/aerosky/iaupgraded/client'
os.makedirs(OUT + '/models_src'); [shutil.copy(M2 + '/' + f, OUT + '/models_src/') for f in ('lib.py', 'oldlib.py', 'cargo.py', 'warships.py', 'render.js')]

AIR = ['cargo_copter', 'cargo_gyrodyne', 'cargo_biplane', 'cargo_seaplane', 'gigantia', 'pelican', 'hawk', 'dragonfly']
ICON = {'cargo_copter': (30, 0, 16, -12), 'cargo_gyrodyne': (34, 0, 18, -10), 'cargo_biplane': (46, 0, 16, -6), 'cargo_seaplane': (52, 0, 18, -10),
        'gigantia': (150, 0, 28, -30), 'pelican': (70, 0, 30, -14), 'hawk': (50, 0, 28, -14), 'dragonfly': (64, 0, 38, -16)}

# ---- models, textures, icons ----
for n in AIR + ['hawk_ballista', 'hawk_autocannon']:
    shutil.copy('%s/%s.bbmodel' % (MO, n), '%s/assets/%s/objects/%s.bbmodel' % (res, NS, n))
    shutil.copy('%s/%s.png' % (MO, n), '%s/assets/%s/textures/entity/%s.png' % (res, NS, n))
for n in AIR:
    subprocess.run(['node', M2 + '/render.js', n, *map(str, ICON[n]), 'icon'], cwd=MO, check=True)
    im = Image.open('%s/%s_icon.png' % (MO, n)).convert('RGBA'); bb = im.getbbox(); im = im.crop(bb)
    side = max(im.size); sq = Image.new('RGBA', (side, side), (0, 0, 0, 0)); sq.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    sq.resize((32, 32), Image.LANCZOS).save('%s/assets/%s/textures/item/%s.png' % (res, NS, n))

# ---- aircraft data ----
PROPS = {
    'cargo_copter':   dict(fuel=1.0, engineSpeed=0.0285, verticalSpeed=0.029),   # 1.0.0: ~88% of the Quadrocopter's speed (was 62%), burns twice its fuel
    'cargo_gyrodyne': dict(fuel=1.0, engineSpeed=0.042, verticalSpeed=0.03, pitchSpeed=3.5, stabilizer=0.3),
    'cargo_biplane':  dict(fuel=1.7, engineSpeed=0.0255),
    'cargo_seaplane': dict(fuel=2.0, engineSpeed=0.0235, waterFriction=0.95),
    'gigantia':       dict(fuel=1.6),
    'pelican':        dict(fuel=2.2, engineSpeed=0.022, lift=0.2, waterFriction=0.97),
    'hawk':           dict(fuel=1.2, engineSpeed=0.085),
    'dragonfly':      dict(fuel=1.4, engineSpeed=0.044, verticalSpeed=0.035),
}
GYRO_SLOTS = {
    'cargo_gyrodyne': [dict(type='boiler', x=17, y=32), dict(type='weapon', x=50, y=24), dict(type='upgrade', x=72, y=24), dict(type='upgrade', x=50, y=46), dict(type='upgrade', x=72, y=46),
                       dict(type='inventory', x=98, y=18, cols=4, rows=4), dict(type='inventory', x=-62, y=8, cols=3, rows=7, boxed=True)],
    'dragonfly': [dict(type='boiler', x=17, y=32), dict(type='weapon', x=50, y=24), dict(type='upgrade', x=72, y=24), dict(type='upgrade', x=50, y=46), dict(type='upgrade', x=72, y=46),
                  dict(type='inventory', x=98, y=18, cols=4, rows=4), dict(type='inventory', x=-62, y=8, cols=3, rows=10, boxed=True), dict(type='inventory', x=-124, y=8, cols=3, rows=10, boxed=True),
                  dict(type='inventory', x=186, y=8, cols=3, rows=10, boxed=True), dict(type='inventory', x=248, y=8, cols=3, rows=9, boxed=True)],
}
summary = {}
for n in AIR:
    p = '%s/data/%s/aircraft/%s.json' % (res, NS, n); d = json.load(open(p)); meta = json.load(open('%s/%s.meta.json' % (MO, n)))
    for k in ('pushSpeed',):
        if n in GYRO_SLOTS: d['properties'].pop(k, None)
    for bad in ('wasterFriction', 'fraction'): d['properties'].pop(bad, None)
    d['properties'].update(PROPS[n])
    if n in GYRO_SLOTS: d['inventorySlots'] = GYRO_SLOTS[n]
    seats = meta['seats']; d['passengerPositions'] = [seats[:i + 1] for i in range(len(seats))]
    nslots = sum(1 for s in d['inventorySlots'] if s['type'] == 'weapon')
    assert nslots == len(meta['mounts']), (n, nslots, len(meta['mounts']))
    d['weaponMounts'] = meta['mounts']
    json.dump(d, open(p, 'w'), indent=2)
    summary[n] = dict(scale=meta['scale'], seats=len(seats), slots=sum(s.get('cols', 0) * s.get('rows', 0) for s in d['inventorySlots']), fuel=d['properties'].get('fuel'),
                      engineSpeed=d['properties'].get('engineSpeed'), extent=meta['extent_blocks'])
json.dump(summary, open(OUT + '/summary.json', 'w'), indent=1)

# ---- java ----
W = lambda path, text: open(path, 'w', encoding='utf-8').write(text)
HEAD = '''package kr.aerosky.iaupgraded.entity;

import immersive_aircraft.entity.AircraftEntity;
import kr.aerosky.iaupgraded.IAUpgraded;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.Level;
'''


def simple(cls, base, baseimport, item, zoom):
    W('%s/%s.java' % (ent, cls), HEAD + ('import %s;\n' % baseimport if baseimport else '') + '''
public class %s extends %s {
    public %s(EntityType<? extends AircraftEntity> type, Level level) {
        super(type, level);
    }

    @Override
    public Item asItem() {
        return IAUpgraded.%s.get();
    }

    /** extra third-person camera distance in blocks */
    @Override
    public double getZoom() {
        return %s;
    }
}
''' % (cls, base, cls, item, zoom))


simple('CargoCopterEntity', 'QuadrocopterEntity', 'immersive_aircraft.entity.QuadrocopterEntity', 'CARGO_COPTER_ITEM', '4.0')
simple('HawkEntity', 'QuadrocopterEntity', 'immersive_aircraft.entity.QuadrocopterEntity', 'HAWK_ITEM', '7.0')
simple('CargoBiplaneEntity', 'BiplaneEntity', 'immersive_aircraft.entity.BiplaneEntity', 'CARGO_BIPLANE_ITEM', '6.0')
simple('GigantiaEntity', 'BiplaneEntity', 'immersive_aircraft.entity.BiplaneEntity', 'GIGANTIA_ITEM', '18.0')
simple('CargoSeaplaneEntity', 'BambooHopperEntity', 'immersive_aircraft.entity.BambooHopperEntity', 'CARGO_SEAPLANE_ITEM', '7.0')
simple('CargoGyrodyneEntity', 'PoweredGyrodyneEntity', None, 'CARGO_GYRODYNE_ITEM', '5.0')
simple('DragonflyEntity', 'PoweredGyrodyneEntity', None, 'DRAGONFLY_ITEM', '9.0')

W(ent + '/PoweredGyrodyneEntity.java', '''package kr.aerosky.iaupgraded.entity;

import immersive_aircraft.entity.AircraftEntity;
import immersive_aircraft.entity.Rotorcraft;
import immersive_aircraft.item.upgrade.VehicleStat;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.Level;
import org.joml.Vector3f;

/**
 * Engine driven gyrodyne (cargo gyrodyne, dragonfly): burns boiler fuel instead of the pilot's hunger,
 * lifts off vertically, and builds up forward thrust slowly once the pilot pushes forward.
 */
public abstract class PoweredGyrodyneEntity extends Rotorcraft {
    /** share of the gap to the wanted forward thrust closed per tick (0.02 = about 3 seconds to 80%) */
    public static final float SPOOL_RATE = 0.02f;
    /** reverse thrust relative to forward thrust */
    public static final float REVERSE = 0.4f;
    private float forwardSpool;

    public PoweredGyrodyneEntity(EntityType<? extends AircraftEntity> type, Level level) {
        super(type, level, true);
    }

    @Override
    protected double getDefaultGravity() {
        return (double) (1.0f - this.getEnginePower()) * super.getDefaultGravity();
    }

    @Override
    protected void updateController() {
        super.updateController();
        if (this.canTurnOnEngine(this.getControllingPassenger())) {
            this.setEngineTarget(1.0f);
        }
        float power = this.getEnginePower();
        double up = power * this.getProperties().get(VehicleStat.VERTICAL_SPEED) * this.pressingInterpolatedY.getSmooth();
        float want = this.pressingInterpolatedZ.getSmooth();
        if (want < 0.0f) want *= REVERSE;
        this.forwardSpool += (want - this.forwardSpool) * SPOOL_RATE;
        float thrust = power * power * this.getProperties().get(VehicleStat.ENGINE_SPEED) * this.forwardSpool;
        Vector3f f = this.getForwardDirection().mul(thrust);
        this.setDeltaMovement(this.getDeltaMovement().add(f.x(), up + f.y(), f.z()));
    }
}
''')

W(ent + '/PelicanEntity.java', '''package kr.aerosky.iaupgraded.entity;

import immersive_aircraft.entity.AircraftEntity;
import immersive_aircraft.entity.BambooHopperEntity;
import kr.aerosky.iaupgraded.IAUpgraded;
import net.minecraft.core.BlockPos;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import org.joml.Vector3f;

/**
 * Sea skimmer (a wing-in-ground craft that can also fly): fast on the water where all four engines run,
 * slower and clumsier in the air. It stays on the water until the pilot deliberately pulls up.
 */
public class PelicanEntity extends BambooHopperEntity {
    /** forward push per tick from the two tail engines at full power (water only) */
    public static final double WATER_THRUST = 0.035;
    /** speed (blocks per second) at which the tail engines stop adding thrust */
    public static final double WATER_MAX_SPEED = 19.0;
    /** extra top speed (blocks per second) at full rain + thunder */
    public static final double STORM_SPEED = 1.5;
    /** fuel use in the air relative to the water (tail engines off) */
    public static final float AIR_FUEL = 0.6f;
    /** how far back the pitch control must be held before the hull is allowed to leave the water */
    public static final float PULL_UP = -0.35f;
    /** turn and pitch rate in the air relative to the water */
    public static final float AIR_YAW = 0.55f;
    public static final float AIR_PITCH = 0.75f;
    /** water within this many blocks below still counts as skimming */
    public static final int SKIM_HEIGHT = 2;

    /** 0..1, how far the tail engines have spun up */
    public float rearPower;
    public float rearRotation;
    public float prevRearRotation;
    private boolean overWater;

    public PelicanEntity(EntityType<? extends AircraftEntity> type, Level level) {
        super(type, level);
    }

    @Override
    public Item asItem() {
        return IAUpgraded.PELICAN_ITEM.get();
    }

    @Override
    public double getZoom() {
        return 10.0;
    }

    private boolean checkOverWater() {
        if (this.wasTouchingWater) return true;
        BlockPos pos = this.blockPosition();
        for (int i = 0; i <= SKIM_HEIGHT; i++) {
            if (!this.level().getFluidState(pos.below(i)).isEmpty()) return true;
        }
        return false;
    }

    public boolean isPullingUp() {
        return this.pressingInterpolatedZ.getSmooth() < PULL_UP;
    }

    /** on or just above the water with the pilot not pulling up: wings give no lift, the hull stays down */
    public boolean isSkimming() {
        return this.overWater && !this.isPullingUp();
    }

    @Override
    protected double getDefaultGravity() {
        double gravity = super.getDefaultGravity();
        if (gravity >= 0.0 && this.isSkimming()) return 0.04;
        return gravity;
    }

    @Override
    protected void updateController() {
        float yaw = this.getYRot();
        float pitch = this.getXRot();
        super.updateController();
        if (!this.overWater && !this.onGround()) {
            this.setYRot(yaw + (this.getYRot() - yaw) * AIR_YAW);
            this.setXRot(pitch + (this.getXRot() - pitch) * AIR_PITCH);
        }
    }

    @Override
    public float getFuelConsumption() {
        return super.getFuelConsumption() * (AIR_FUEL + (1.0f - AIR_FUEL) * this.rearPower);
    }

    @Override
    public void tick() {
        this.overWater = this.checkOverWater();
        super.tick();
        float power = this.getEnginePower();
        float target = this.wasTouchingWater && power > 0.05f ? power : 0.0f;
        this.rearPower += (target - this.rearPower) * 0.08f;
        if (this.level().isClientSide) {
            if (this.rearRotation > 1000.0f) this.rearRotation -= 1000.0f;
            this.prevRearRotation = this.rearRotation;
            this.rearRotation += this.rearPower;
        }
        if (this.getControllingPassenger() == null || !this.isControlledByLocalInstance()) return;
        Vec3 v = this.getDeltaMovement();
        if (this.isSkimming() && v.y > 0.0) {
            v = new Vec3(v.x, v.y * 0.5, v.z);
        }
        if (this.rearPower >= 0.01f && this.wasTouchingWater) {
            Vector3f d = this.getForwardDirection();
            double speed = Math.max(0.0, v.x * d.x() + v.z * d.z()) * 20.0;
            double storm = this.level().getRainLevel(1.0f) + this.level().getThunderLevel(1.0f);
            double max = WATER_MAX_SPEED + storm * STORM_SPEED;
            double k = WATER_THRUST * this.rearPower * this.rearPower * Mth.clamp((1.0 - speed / max) / 0.25, 0.0, 1.0);
            v = v.add(d.x() * k, 0.0, d.z() * k);
        }
        this.setDeltaMovement(v);
    }
}
''')


W(cli + '/UpgradedRenderer.java', '''package kr.aerosky.iaupgraded.client;

import immersive_aircraft.client.render.entity.renderer.AircraftEntityRenderer;
import immersive_aircraft.client.render.entity.renderer.utils.ModelPartRenderHandler;
import immersive_aircraft.entity.AircraftEntity;
import kr.aerosky.iaupgraded.IAUpgraded;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.resources.ResourceLocation;

/** One renderer for every aircraft of this mod: the model and its propeller animation live in the .bbmodel file. */
public class UpgradedRenderer<T extends AircraftEntity> extends AircraftEntityRenderer<T> {
    private final ResourceLocation modelId;
    private final ModelPartRenderHandler<T> model;

    public UpgradedRenderer(EntityRendererProvider.Context context, String name, float shadow) {
        this(context, name, shadow, new ModelPartRenderHandler<>());
    }

    public UpgradedRenderer(EntityRendererProvider.Context context, String name, float shadow, ModelPartRenderHandler<T> handler) {
        super(context);
        this.modelId = ResourceLocation.fromNamespaceAndPath(IAUpgraded.ID, name);
        this.shadowRadius = shadow;
        this.model = handler;
    }

    @Override
    protected ResourceLocation getModelId() {
        return this.modelId;
    }

    @Override
    protected ModelPartRenderHandler<T> getModel(AircraftEntity entity) {
        return this.model;
    }
}
''')

W(cli + '/HawkWeaponRenderer.java', '''package kr.aerosky.iaupgraded.client;

import com.mojang.blaze3d.vertex.PoseStack;
import immersive_aircraft.client.render.entity.weaponRenderer.WeaponRenderer;
import immersive_aircraft.entity.VehicleEntity;
import immersive_aircraft.entity.weapon.Weapon;
import kr.aerosky.iaupgraded.entity.HawkEntity;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.resources.ResourceLocation;

/** Draws the normal weapon model everywhere, and the Hawk's own model when the weapon is mounted on a Hawk. */
public class HawkWeaponRenderer extends WeaponRenderer<Weapon> {
    private final ResourceLocation normal;
    private final ResourceLocation onHawk;
    private ResourceLocation current;

    public HawkWeaponRenderer(ResourceLocation normal, ResourceLocation onHawk) {
        this.normal = normal;
        this.onHawk = onHawk;
        this.current = normal;
    }

    @Override
    public <T extends VehicleEntity> void render(T entity, Weapon weapon, PoseStack matrixStack, MultiBufferSource buffers, int light, float time) {
        this.current = entity instanceof HawkEntity ? this.onHawk : this.normal;
        super.render(entity, weapon, matrixStack, buffers, light, time);
    }

    @Override
    protected ResourceLocation getModelId() {
        return this.current;
    }
}
''')

W(cli + '/ClientSetup.java', '''package kr.aerosky.iaupgraded.client;

import com.mojang.math.Axis;
import immersive_aircraft.Main;
import immersive_aircraft.WeaponRendererRegistry;
import immersive_aircraft.client.render.entity.renderer.utils.ModelPartRenderHandler;
import kr.aerosky.iaupgraded.IAUpgraded;
import kr.aerosky.iaupgraded.entity.PelicanEntity;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

public final class ClientSetup {
    private ClientSetup() {}

    public static void init(IEventBus modBus) {
        modBus.addListener(ClientSetup::registerRenderers);
        modBus.addListener(ClientSetup::clientSetup);
    }

    private static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath(IAUpgraded.ID, path);
    }

    /** Hawk shows its own ballista / twin autocannon instead of the standard weapon models. */
    private static void clientSetup(FMLClientSetupEvent e) {
        e.enqueueWork(() -> {
            WeaponRendererRegistry.register(Main.locate("heavy_crossbow"), new HawkWeaponRenderer(Main.locate("heavy_crossbow"), id("hawk_ballista")));
            WeaponRendererRegistry.register(Main.locate("rotary_cannon"), new HawkWeaponRenderer(Main.locate("rotary_cannon"), id("hawk_autocannon")));
        });
    }

    /** tail propellers of the pelican: spin only while the tail engines run (on the water) */
    private static void spinRear(PelicanEntity entity, float yaw, float time, com.mojang.blaze3d.vertex.PoseStack pose, float dir) {
        float partial = (time * 20.0f) % 1.0f;
        pose.mulPose(Axis.ZP.rotationDegrees(Mth.lerp(partial, entity.prevRearRotation, entity.rearRotation) * 150.0f * dir));
    }

    private static void registerRenderers(EntityRenderersEvent.RegisterRenderers e) {
        e.registerEntityRenderer(IAUpgraded.CARGO_COPTER.get(), c -> new UpgradedRenderer<>(c, "cargo_copter", 1.2f));
        e.registerEntityRenderer(IAUpgraded.HAWK.get(), c -> new UpgradedRenderer<>(c, "hawk", 2.0f));
        e.registerEntityRenderer(IAUpgraded.CARGO_GYRODYNE.get(), c -> new UpgradedRenderer<>(c, "cargo_gyrodyne", 1.3f));
        e.registerEntityRenderer(IAUpgraded.DRAGONFLY.get(), c -> new UpgradedRenderer<>(c, "dragonfly", 2.6f));
        e.registerEntityRenderer(IAUpgraded.CARGO_BIPLANE.get(), c -> new UpgradedRenderer<>(c, "cargo_biplane", 1.5f));
        e.registerEntityRenderer(IAUpgraded.GIGANTIA.get(), c -> new UpgradedRenderer<>(c, "gigantia", 3.5f));
        e.registerEntityRenderer(IAUpgraded.CARGO_SEAPLANE.get(), c -> new UpgradedRenderer<>(c, "cargo_seaplane", 1.8f));
        e.registerEntityRenderer(IAUpgraded.PELICAN.get(), c -> new UpgradedRenderer<>(c, "pelican", 2.6f,
                new ModelPartRenderHandler<PelicanEntity>()
                        .add("rear_a", (entity, yaw, time, pose) -> spinRear(entity, yaw, time, pose, 1.0f))
                        .add("rear_b", (entity, yaw, time, pose) -> spinRear(entity, yaw, time, pose, -1.0f))));
    }
}
''')

# hitboxes follow the new model scale
main = OUT + '/src/kr/aerosky/iaupgraded/IAUpgraded.java'; t = open(main).read()
SIZES = {'CargoCopterEntity': ('1.5f, 1.4f', '2.0f, 1.8f'), 'HawkEntity': ('2.5f, 2.2f', '3.2f, 2.8f'), 'CargoGyrodyneEntity': ('1.5f, 1.6f', '2.0f, 2.0f'),
         'DragonflyEntity': ('3.0f, 3.2f', '3.6f, 3.8f'), 'CargoBiplaneEntity': ('2.0f, 1.5f', '2.6f, 1.9f'), 'CargoSeaplaneEntity': ('2.5f, 1.4f', '3.2f, 1.8f')}
for cls, (a, b) in SIZES.items():
    old = '%s::new, MobCategory.MISC).sized(%s)' % (cls, a); assert old in t, cls
    t = t.replace(old, '%s::new, MobCategory.MISC).sized(%s)' % (cls, b))
open(main, 'w').write(t)

# metadata + language
p = res + '/META-INF/neoforge.mods.toml'; t = open(p).read(); assert 'version = "0.2.0"' in t; open(p, 'w').write(t.replace('version = "0.2.0"', 'version = "%s"' % VERSION))
DESC = {
 'ko_kr': {'cargo_gyrodyne': '화물칸과 엔진을 단 자이로다인. 연료로 수직 이륙하며, 전진 속도가 붙는 데 시간이 걸립니다.',
           'dragonfly': '양옆 붐에 로터 두 개, 배 아래에는 금고. 연료로 수직 이륙하며 천천히 가속합니다.',
           'pelican': '물 위에서는 앞뒤 엔진 네 기로 가장 빠르게 달립니다. 기수를 확실히 당겨야 떠오르고, 공중에서는 느리고 둔합니다.',
           'hawk': '바람을 무시하는 무장 헬기. 동체 아래 발리스타는 데미지 2배, 날개 아래 자동포 두 문은 연사와 데미지 1.5배.'},
 'en_us': {'cargo_gyrodyne': 'A gyrodyne with a cargo bay and an engine. Burns fuel, lifts off vertically and takes a while to pick up forward speed.',
           'dragonfly': 'Two rotors on side booms and a vault slung under the belly. Burns fuel, lifts off vertically and accelerates slowly.',
           'pelican': 'Fastest across the water, where all four engines run. It only leaves the water when you pull up firmly, and it is slow and clumsy in the air.',
           'hawk': 'A gunship that ignores wind. The belly ballista deals double damage; the two underwing autocannons fire and hit 1.5 times as hard.'},
 'ja_jp': {'cargo_gyrodyne': '貨物室とエンジンを備えたジャイロダイン。燃料で垂直離陸し、前進速度が上がるまで時間がかかります。',
           'dragonfly': '左右のブームにローター2基、腹の下には金庫。燃料で垂直離陸し、ゆっくり加速します。',
           'pelican': '水上ではエンジン4基で最速。機首をしっかり引かないと浮かび上がらず、空中では遅く鈍重です。',
           'hawk': '風を無視する武装ヘリ。胴体下のバリスタはダメージ2倍、翼下の機関砲2門は連射とダメージが1.5倍。'},
}
for lang, dd in DESC.items():
    p = '%s/assets/%s/lang/%s.json' % (res, NS, lang); d = json.load(open(p, encoding='utf-8'))
    for k, v in dd.items():
        key = 'item.%s.%s.description' % (NS, k); assert key in d, key; d[key] = v
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(json.dumps(summary, indent=0))


