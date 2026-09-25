```text
TEMPORARY EVIDENCE — NOT PROJECT SSOT
Minecraft Java 1.21.1 mapped-source investigation
Do not treat this file as canonical design documentation.
```

**Status:** Temporary Agent Phantom evidence packet. **Not** a canonical manifestation report. **Not** DESIGN-BIO-MANIFEST-004. **Not** permission to add flight, nocturnal, insomnia, membrane, undead-flying, or other Biological Profile fields.

**Authoritative source:** Minecraft Java **1.21.1** mapped NeoForge 21.1.208 sources (`neoforge-21.1.208-sources.jar` + `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar`). Cache: `.tmp_mc_sources/` (not project SSOT).

**Wiki:** orientation / disagreement check only. Where wiki and 1.21.1 source disagree, **1.21.1 source wins**.

**Closed leaps used throughout:** shared outcome ≠ shared biological cause; shared Java parent ≠ clade; shared tag ≠ clade; same HostType ≠ same biology; Host Registry membership ≠ eligibility ≠ manifestation; spawn encounter ≠ organism origin; world/dimension association ≠ organism-native origin; renderer/model ≠ anatomical composition; Minecraft taxonomy ≠ BioCraft biological composition.

Phantom is **not** part of a zombie-family cluster and is **not** investigated as a biological group with Zombie Horse or Camel Husk.

---

## Subject

Phantom

## Version

Minecraft Java 1.21.1 (`minecraft_version_range=[1.21.1,1.22)`, NeoForge 21.1.208)

## Target identity

| Fact | 1.21.1 evidence |
|------|-----------------|
| Registry name | `"phantom"` |
| Registry object | `EntityType.PHANTOM` |
| Class | `net.minecraft.world.entity.monster.Phantom` |
| Hierarchy | `Entity` → `LivingEntity` → `Mob` → `FlyingMob` → `Phantom implements Enemy` |
| **Not** a `Monster` subclass | `Phantom extends FlyingMob implements Enemy` (`Phantom.java:42`). `Enemy` is a marker/XP-constant interface only (`Enemy.java`). |
| Mob category | `MobCategory.MONSTER` (`EntityType.java:524-532`) |
| Default dimensions | `sized(0.9F, 0.5F)`, `eyeHeight(0.175F)`, `passengerAttachments(0.3375F)`, `ridingOffset(-0.125F)`, `clientTrackingRange(8)` |
| Fire immune? | Builder does **not** call `immuneToFire()`. Default false. |
| Attributes | `DefaultAttributes` maps `EntityType.PHANTOM` → `Monster.createMonsterAttributes().build()` (`DefaultAttributes.java:133`). That is `Mob.createMobAttributes().add(Attributes.ATTACK_DAMAGE)` (`Monster.java:127-128`) plus living defaults (`MAX_HEALTH` default **20.0**, `ATTACK_DAMAGE` default **2.0** then overwritten by size). |
| Spawn placement (generic registry) | `SpawnPlacementTypes.NO_RESTRICTIONS`, `Heightmap.Types.MOTION_BLOCKING_NO_LEAVES`, `Mob::checkMobSpawnRules` (`SpawnPlacements.java:167`) |
| Natural spawn owner | **Not** biome spawn lists. Overworld **custom spawner** `PhantomSpawner` installed only on the Overworld `ServerLevel` (`MinecraftServer.createLevels` `ImmutableList.of(new PhantomSpawner(), …)` at `MinecraftServer.java:363-368`). |
| Renderer | `EntityRenderers.register(EntityType.PHANTOM, PhantomRenderer::new)` |
| Model layer | `ModelLayers.PHANTOM` |
| Items | `Items.PHANTOM_SPAWN_EGG`, `Items.PHANTOM_MEMBRANE` |

```524:532:.tmp_mc_sources/net/minecraft/world/entity/EntityType.java
    public static final EntityType<Phantom> PHANTOM = register(
        "phantom",
        EntityType.Builder.of(Phantom::new, MobCategory.MONSTER)
            .sized(0.9F, 0.5F)
            .eyeHeight(0.175F)
            .passengerAttachments(0.3375F)
            .ridingOffset(-0.125F)
            .clientTrackingRange(8)
    );
```

```42:54:.tmp_mc_sources/net/minecraft/world/entity/monster/Phantom.java
public class Phantom extends FlyingMob implements Enemy {
    public static final float FLAP_DEGREES_PER_TICK = 7.448451F;
    public static final int TICKS_PER_FLAP = Mth.ceil(24.166098F);
    private static final EntityDataAccessor<Integer> ID_SIZE = SynchedEntityData.defineId(Phantom.class, EntityDataSerializers.INT);
    Vec3 moveTargetPoint = Vec3.ZERO;
    BlockPos anchorPoint = BlockPos.ZERO;
    Phantom.AttackPhase attackPhase = Phantom.AttackPhase.CIRCLE;

    public Phantom(EntityType<? extends Phantom> entityType, Level level) {
        super(entityType, level);
        this.xpReward = 5;
        this.moveControl = new Phantom.PhantomMoveControl(this);
        this.lookControl = new Phantom.PhantomLookControl(this);
    }
```

**Required distinction:** `MobCategory.MONSTER` and `implements Enemy` are Minecraft spawn/taxonomy/XP markers. They are **not** BioCraft biological composition and do **not** establish an “undead flying” category.

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP representation? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|-----------------------------|--------------------|-------|
| Registry identity `minecraft:phantom` | `EntityType.PHANTOM` | `EntityType.java:524-532` | Identity only | `organismKey` `"phantom"` via Host Registry path | Generic resolver / DNA sample identity (LIVE, not Phantom-specific) | **B** |
| Class hierarchy / `FlyingMob` parent | Java type graph | `Phantom extends FlyingMob`; 1.21.1 `FlyingMob` subclasses are **Phantom and Ghast only** | No. Shared parent ≠ clade | None needed | None | **A** |
| Generic aerial travel physics | `FlyingMob.travel` / empty `checkFallDamage` / `onClimbable()==false` | `FlyingMob.java:13-53` | No. Shared movement helper, not a flight trait | None | None | **A** |
| Phantom-specific flight / steering | `Phantom.PhantomMoveControl` (replaces default `MoveControl`) | Constructor sets `this.moveControl = new Phantom.PhantomMoveControl(this)`; inner class `PhantomMoveControl.tick` (`Phantom.java:50-54`, `401-446`) | No. Gameplay steering | None | None | **A** |
| Generic `FlyingMoveControl` | **Not used by Phantom** | `FlyingMoveControl` is a separate `MoveControl` used by other flyers (e.g. Wither). Phantom never constructs it | No | None | None | **A** |
| Circle / swoop attack AI | Phantom inner goals | `registerGoals`: `PhantomAttackStrategyGoal`, `PhantomSweepAttackGoal`, `PhantomCircleAroundAnchorGoal`, `PhantomAttackPlayerTargetGoal` (`Phantom.java:68-73`). Phases `CIRCLE` / `SWOOP` (`229-232`) | No. Phantom-owned combat AI | None | None | **A** |
| Inherited generic combat | `Mob.doHurtTarget` | Sweep goal calls `Phantom.this.doHurtTarget(livingentity)` (`Phantom.java:517`) | No. Melee hit is Mob infrastructure | None | None | **A** |
| Attack damage vs size | `Phantom.updatePhantomSizeInfo` | `ATTACK_DAMAGE` base = `6 + getPhantomSize()` (`Phantom.java:85-88`) | No. Entity stat | None | None | **A** |
| Targeting | `PhantomAttackPlayerTargetGoal` | Nearby **players** in inflated AABB `(16, 64, 16)`, combat range 64, sorted by Y descending (`Phantom.java:234-267`). Not a general predator-of-mobs AI | No | None | None | **A** |
| Cat scare during swoop | `PhantomSweepAttackGoal` + `Cat.hiss()` | Searches `Cat` in inflate(16); if any alive cat, `isScaredOfCat` and swoop stops (`Phantom.java:459-498`) | No. Vanilla encounter rule | None | None | **A** |
| Natural spawn | `PhantomSpawner` as Overworld `CustomSpawner` | `MinecraftServer.java:363-368`; `PhantomSpawner.tick` (`PhantomSpawner.java:21-83`) | **No.** Player/world spawn condition, not organism origin | None | None | **A** |
| Gamerule toggle | `GameRules.RULE_DOINSOMNIA` `"doInsomnia"` | Default true, category `SPAWNING` (`GameRules.java:126-128`). Spawner returns 0 if false (`PhantomSpawner.java:28-29`) | No. Spawn gamerule | None | None | **A** |
| Player inactivity / insomnia | `Stats.TIME_SINCE_REST` | Incremented while not sleeping (`Player.java:303-308`). Reset on `startSleeping` (`ServerPlayer.java:1043-1045`) and on death (`ServerPlayer.java:739`, `Player.java:686`). Spawner: `random.nextInt(j) >= 72000` (`PhantomSpawner.java:51-53`) | **No.** Player statistic as spawn gate. **Insomnia ≠ Phantom biological origin** | None | None | **A** |
| Sky / night / sea-level spawn gates | `PhantomSpawner` + `PlayerSpawnPhantomsEvent.shouldSpawnPhantoms` | `getSkyDarken() < 5 && hasSkyLight()` abort (`PhantomSpawner.java:37-38`). Default result requires no skylight **or** `Y >= seaLevel && canSeeSky` (`PlayerSpawnPhantomsEvent.java:74-78`, `87-100`). Difficulty random gate (`PhantomSpawner.java:48-49`) | No. World/player spawn filters | None | None | **A** |
| Spawn count | NeoForge hook wrapping vanilla random | `1 + random.nextInt(difficulty.getId() + 1)` (`EventHooks.firePlayerSpawnPhantoms` `EventHooks.java:367-371`) | No | None | None | **A** |
| Spawn placement block check | `NaturalSpawner.isValidEmptySpawnBlock(..., EntityType.PHANTOM)` | `PhantomSpawner.java:59` | No | None | None | **A** |
| Natural spawn size | `Phantom.finalizeSpawn` | `setPhantomSize(0)` always (`Phantom.java:156-159`) | No | None | None | **A** |
| Size NBT / scaling | Phantom synched `ID_SIZE` 0–64 | `setPhantomSize` clamps 0–64 (`81-83`); `getDefaultDimensions` scales `1.0F + 0.15F * size` (`223-227`); renderer `scale` same formula (`PhantomRenderer.java:29-34`). **No 1.21.1 tick/attack increment of size** | No. Gameplay/presentation scale, not anatomy profile | None | None | **A** |
| Sunlight burning | `Phantom.aiStep` + `Mob.isSunBurnTick` | If alive and `isSunBurnTick()` then `igniteForSeconds(8.0F)` (`Phantom.java:142-148`). **Not** driven by `#minecraft:undead` | No. Per-class vanilla sunlight rule | None | None | **A** |
| Peaceful despawn | `Phantom.shouldDespawnInPeaceful` | Returns true (`Phantom.java:108-110`) | No | None | None | **A** |
| XP | Phantom field | `xpReward = 5` (`Phantom.java:52`) = `Enemy.XP_REWARD_MEDIUM` constant, not a biological yield | No | None | None | **A** |
| Sounds | Phantom + `SoundEvents` + level event 1039 | Ambient/hurt/death/flap/swoop on Phantom; bite via `levelEvent(1039)` → `LevelRenderer` plays `PHANTOM_BITE` (`Phantom.java:198-210`, `519-521`; `LevelRenderer.java:2994-2995`) | No | None | None | **A** |
| Wing particles | Client `Phantom.tick` | `ParticleTypes.MYCELIUM` at wing tips (`Phantom.java:132-137`) | No. Cosmetic. Not mycelium biology | None | None | **A** |
| Rendering / model | `PhantomRenderer`, `PhantomModel`, `PhantomEyesLayer` | Eyes overlay; wing/tail cubes; size scale in renderer | No. Model ≠ anatomy composition | None | None | **A** |
| Fall-damage immunity | Tag `#minecraft:fall_damage_immune` includes `minecraft:phantom` | Tag JSON + `LivingEntity.calculateFallDamage` / `Entity.isInvulnerableTo` IS_FALL | No. Shared tag with Bat, Bee, Ghast, Chicken, etc. Tag ≠ clade | None | None | **A** |
| Undead tag membership | `#minecraft:undead` includes `minecraft:phantom` plus `#skeletons`, `#zombies`, Wither | `undead.json`; `EntityTypeTagsProvider.java:40` | Minecraft taxonomy, **not** BioCraft composition | `HostType.UNDEAD` already on this registry key | Host Registry / resolver identity only | **B** (identity) / **A** (tag gameplay) |
| Tag-driven undead effects | Vanilla tag consumers | `CAN_BREATHE_UNDER_WATER`, `IGNORES_POISON_AND_REGEN`, `INVERTED_HEALING_AND_HARM`, `WITHER_FRIENDS`, `SENSITIVE_TO_SMITE` all **include `#minecraft:undead`** | No. Named vanilla consumers (LivingEntity, Enchantments.SMITE, WitherBoss targeting/hurt, Armadillo scare) | Do not encode as BP undead-tissue | None that need a new field | **A** |
| Phantom membrane drop | Loot table `entities/phantom.json` / `VanillaEntityLoot` | 0–1 `phantom_membrane` when killed by player; looting extra | No. Loot SSOT | None | None | **A** |
| Membrane uses | Item / brewing / repair | Awkward + membrane → Slow Falling (`PotionBrewing.java:224`); Elytra anvil repair (`ElytraItem.isValidRepairItem` `ElytraItem.java:27-28`). Cat morning gift can also drop membrane (`VanillaGiftLoot.java:34`) | No. Item recipes. Membrane ≠ anatomy field | None | None | **A** |
| Beds / sleep blocking | `ServerPlayer` sleep check queries **`Monster.class`** | `getEntitiesOfClass(Monster.class, …, Monster::isPreventingPlayerRest)` (`ServerPlayer.java:999-1011`). Phantom **is not** a `Monster` subclass, so nearby Phantoms do **not** emit `NOT_SAFE` via this path | No | None | None | **A** |
| Sleep resetting spawn gate | `ServerPlayer.startSleeping` | Resets `TIME_SINCE_REST` (`ServerPlayer.java:1043-1045`). Entering a bed is enough; night skip is not required by this reset | No. Player action | None | None | **A** |
| Advancements | Vanilla advancement JSON | `kill_a_mob` / `kill_all_mobs` include `minecraft:phantom`; `two_birds_one_arrow` requires two Phantom crossbow victims | No | None | None | **A** |
| Host Registry row | `hosts.json` `vanilla_hosts.undead.mobs` includes `"phantom"` | `default_dna: "undead"` → `HostType.UNDEAD` | Participation / DNA **routing**, not biology dossier | `organismKey` + `hostType` + `hostEffectProfileId` | LIVE registry; eligibility false | **B** |
| Xenomorph eligibility | `HostType.UNDEAD.isSuitableForXenomorph() == false` | `HostType.java:20`; `MobHostRegistry.isSuitableForXenomorph` | Locked project suitability, **not** reopened | Existing HostType | LIVE rejection | **B** |
| Flight / insomnia / membrane as BP fields | No live BioCraft consumer | Searched AlienCraft Java/tests: no Phantom-specific AI, config, transformation, lifecycle, or Analyzer field | Not earned | Existing identity sufficient | None named | **A/B** |

### Methodology notes (selected)

**Flight**

```
Existing gameplay: Phantom flies and swoops
  → Owner: Phantom.PhantomMoveControl + inner goals; generic aerial physics on FlyingMob
  → Biological input? No. This is vanilla movement/AI
  → Existing composition? Identity key already distinguishes Phantom from Bee/Ghast/Bat
  → Named BioCraft consumer needing biological flight? None found
  → A
```

**Insomnia spawn**

```
Existing gameplay: Phantoms appear after long time-since-rest
  → Owner: PhantomSpawner + Stats.TIME_SINCE_REST + doInsomnia + player sleep/death reset
  → Biological input? No. Player/world spawn condition
  → Existing composition? Not an organism-origin fact
  → Named consumer? None
  → A
```

**Membrane**

```
Existing gameplay: kill Phantom (player kill) → phantom_membrane
  → Owner: loot table
  → Biological input? No
  → Named BioCraft consumer of membrane-as-anatomy? None
  → A
```

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"phantom"` under `vanilla_hosts.undead` | **LIVE** | `hosts.json` lines 13–18: `"phantom"` in undead `mobs`; `default_dna: "undead"` | Host Registry **participation**. Registration ≠ eligibility ≠ manifestation. |
| `HostType.UNDEAD` | **LIVE** | `HostType.java`; `HostConfigParser.parseGroup(..., "undead", HostType.UNDEAD, ...)` | Current project taxonomy / suitability bucket. `isSuitableForXenomorph() == false` is a **locked prior**. Do not reopen. |
| `MobHostRegistry.getHostType("phantom")` / `getDnaProfileId("phantom")` | **LIVE** | Parser writes every mob string into `hostTypeMap` + `dnaProfileIdByMob` | Would resolve `UNDEAD` + `"undead"`. No Phantom-specific override (`dna_overrides` absent for phantom). |
| `HostEligibilityService` | **LIVE** | Delegates to `MobHostRegistry.isSuitableForXenomorph` | Phantom is registered but **not** currently a xenomorph host. |
| Host-effect pack `undead.json` | **LIVE** (attachment-effect pack) | `parasite/host_effects/undead.json`: immobilization + vanilla potion-like visual/movement effects. Description: “reserved for future undead-compatible parasites” | Host-effect gameplay routing. **Not** genetics, **not** anatomy, **not** Phantom-specific biology. `CompiledBiologicalProfile.hostEffectProfileId()` explicitly must not be inferred as genetics. |
| `BiologicalProfileResolver` | **LIVE** (generic) | Resolves any Host Registry key to sparse `CompiledBiologicalProfile` | `resolve("phantom")` would yield `organismKey=phantom`, `hostType=UNDEAD`, `hostEffectProfileId=undead`, empty form/behavior/contributing source. That is **identity composition already**. No Phantom test names this key. |
| `BiologicalProfilePort` / `CompiledBiologicalProfile` | **LIVE** | Domain boundary; sparse payload only | No flight/insomnia/membrane field exists or is earned. |
| `contributingSourceKey` / Model A | **LIVE** (xenomorph carriers) | Chestburster/Drone carry optional contributing source; Analyzer projects it | If a **later separately authorized** eligibility decision permitted Phantom as a host, existing Model A could store `contributingSourceKey="phantom"` without a new BP field. That is **not** current eligibility and is **not** a Phantom manifestation requirement. |
| `DnaSampleFromOccupant` | **LIVE** (generic) | Non-xenomorph → `encodeId` → `HostRegistryPaths.registryPath` → organismKey | Sampling a Phantom entity would produce identity `"phantom"`. Analyzer would display identity, not a new biological dimension. |
| `variant_mappings` | **DEAD-UNUSED for Phantom** | `hosts.json` maps spider/creeper/wolf/enderman only | Phantom has no temperament mapping. |
| `mob_catalog.json` | **PARSE-ONLY / PLANNING matrix** | `deep_mob_configs` hostile mobs list does **not** include `phantom`. Live bootstrap is spider/creeper/wolf/enderman | Catalog is not a Phantom consumer and does not load a Phantom xenomorph variant. |
| `entity/xenomorph/mob-based/**` | **DEAD-UNUSED for Phantom** | No phantom xenomorph JSON | No mob-based xenomorph variant. |
| Entity / AI / transformation / lifecycle config named phantom | **DEAD-UNUSED** | Ripgrep of `biocraft-alien/src` Java/tests: **no** `phantom` symbol except `hosts.json` | No Phantom AI, renderer, or lifecycle fork. |
| `HostEffectProfileConfigLoadTest.everyRegisteredMobHasKnownHostEffectProfile` | **TEST ONLY** (generic) | Iterates `getAllRegisteredMobs()`; does not name phantom | Covers Phantom only as “a registered mob has some pack id”. |
| `BiologicalProfileResolverTest` | **TEST ONLY** | Names skeleton/husk/drowned as undead examples; **does not** name phantom | Phantom would follow the same `assertUndeadHost` pattern if added; that would still be identity, not a new field. |
| Inventory row `phantom` | **PLANNING ONLY** | `vanilla_organism_inventory.md` category `undead`, registered, manifestation pending, eligibility undetermined | Accounting label. Not SSOT for biology or eligibility. |
| `vanilla_compatibility.md` “Flight capability” row listing phantom | **PLANNING ONLY** | Compatibility sketch; Bat is the named eventual candidate | Must **not** be treated as a live consumer of biological flight. Interesting ≠ earned. |
| ROADMAP / BACKLOG / SPRINT sequence mentioning Phantom | **PLANNING ONLY** | Investigation order text | Do not mint Feature IDs from this packet. |
| `HostType.UNDEAD` comment “reserved for future specialized xenomorph lifecycles” | **LIVE comment / PLANNING remainder** | `HostType.java:19-20` | Suitability false today. This packet does not design that future. |

**Hard Phantom gate:** `#minecraft:undead` membership and `HostType.UNDEAD` must **not** reopen or establish a broader “undead flying” category. Those are taxonomy / routing. Vanilla tag consumers (Smite, poison/regen ignore, inverted heal/harm, Wither friends, armadillo scare, aquatic breathing) are **named 1.21.1 gameplay consumers of a tag**, not BioCraft biological composition.

---

## Tempting but rejected interpretations

The evidence does **not** support:

1. **A Biological Profile “flight” field** because Phantom flies. Flight is vanilla-owned (`FlyingMob` physics + `PhantomMoveControl` + Phantom goals). No named BioCraft consumer needs biological flight information. Conclude **A/B**.
2. **Generic biological flight shared with Bat / Bee / Ghast / Wither / Ender Dragon.** Shared aerial outcome ≠ shared cause. Bat/Bee do not extend `FlyingMob`. Ghast shares `FlyingMob` — that is a Java parent, **not** a clade. Wither uses `FlyingMoveControl`, which Phantom does **not**. Do not generalize Phantom → Bat/Ghast.
3. **An “undead flying” category** from Phantom + Wither (or Ghast). Phantom classification must not reopen that category even though Phantom is in `#minecraft:undead` and Wither is too. Tag/HostType sharing ≠ flying-undead biology.
4. **Sleep-deprivation biology / insomnia adaptation / nocturnal trait.** `TIME_SINCE_REST` and `doInsomnia` are **spawn conditions on the player/world**. They are not Phantom tissue, origin, or adaptation. `player insomnia as a spawn condition ≠ Phantom biological origin`.
5. **Overworld-native organism origin** because the custom spawner is installed on Overworld. Dimension association of a spawner ≠ organism-native origin.
6. **A membrane / anatomy profile** because the loot table drops `phantom_membrane`. Loot and item uses (Slow Falling brew, Elytra repair, rare cat gift) are vanilla item SSOTs. No BioCraft consumer reads membrane as anatomy.
7. **Size as anatomical composition.** Size is a synched 0–64 scale affecting hitbox, attack damage, and renderer. Natural spawn forces size 0. 1.21.1 `Phantom.java` contains **no** growth-on-attack loop.
8. **Mycelium / fungal biology** from `ParticleTypes.MYCELIUM`. Cosmetic client particles.
9. **Undead-as-composition** from `#minecraft:undead` or `HostType.UNDEAD`. Those are Minecraft taxonomy and AlienCraft routing. Named tag consumers are vanilla combat/effect/AI rules.
10. **Sunlight burning as proof of undead composition.** Sunburn is `Phantom.aiStep` calling `Mob.isSunBurnTick`, **not** a `#undead` tag effect. Other undead classes implement similar rules independently. Shared outcome ≠ shared BP field.
11. **Phantom prevents bed use** as a Phantom-owned rest-biology. 1.21.1 bed `NOT_SAFE` scans `Monster.class`. Phantom is not a `Monster`.
12. **Host Registry membership as eligibility or manifestation.** `"phantom"` is registered `UNDEAD`; `isSuitableForXenomorph() == false` remains locked. This packet does not change that.
13. **`hostEffectProfileId = "undead"` as genetics or Phantom traits.** Resolver comment and `CompiledBiologicalProfile` forbid that inference.
14. **A named BioCraft consumer invented because spawn is unusual.** Unusual spawn is still vanilla spawn ownership.
15. **Current-wiki / later-version / Bedrock behavior as 1.21.1 evidence** (see disagreements below).
16. **Zombie-family grouping.** Phantom is not in `#minecraft:zombies`. This investigation is not a zombie-cluster pass.

---

## Wiki vs 1.21.1 source disagreements

Orientation only. **Source wins.**

| Topic | Current wiki / later-version claim | 1.21.1 mapped source | Winner |
|-------|-----------------------------------|----------------------|--------|
| Gamerule name | Wiki currently attributes Java `spawn_phantoms` and Bedrock `doInsomnia` | Java 1.21.1 registers **`doInsomnia`** (`GameRules.RULE_DOINSOMNIA`) | **1.21.1 source** |
| Straw beds | Wiki marks straw beds as upcoming 2026 | Not present in this 1.21.1 extract | **1.21.1 source** (ignore upcoming) |
| Bedrock spawn | Surface monster-cap spawn, ocelot scare | Out of scope. Java 1.21.1 uses `PhantomSpawner` + **Cat** only | Do not import Bedrock |
| Particles | “Gray smoke” | `ParticleTypes.MYCELIUM` | **1.21.1 source** |
| Entity components such as `burn_in_daylight` | Later data-driven component lists | 1.21.1 burns via `Phantom.aiStep` + `isSunBurnTick` | **1.21.1 source** |
| Size growth while hunting | Older community/wiki memory of size increasing on successful attacks | 1.21.1 `Phantom.java` never increments size; `finalizeSpawn` sets 0; NBT can store Size if summoned | **1.21.1 source** (no growth loop) |
| Sea level Y=64 | Wiki often hardcodes 64 | `level.getSeaLevel()` | **1.21.1 source** |
| Natural size 0, HP 20, damage 6+size | Wiki NBT notes | Agrees with `finalizeSpawn` size 0, `MAX_HEALTH` default 20, `ATTACK_DAMAGE` set to `6+size` | Agree |
| 72000 tick insomnia gate | Wiki | `random.nextInt(j) >= 72000` with `j = TIME_SINCE_REST` | Agree (spawn condition, not biology) |

Do **not** silently merge wiki into 1.21.1 evidence.

---

## Potential biological relationships

| Candidate | Relationship | Owner | Biological input? | Existing composition | Named consumer | Result |
|-----------|--------------|-------|-------------------|----------------------|----------------|--------|
| Phantom ↔ Ghast | Both `extends FlyingMob` | Java parent `FlyingMob` | No. Shared parent ≠ clade | Host Registry already splits them (`phantom` UNDEAD vs `ghast` ELEMENTAL) | None needing a shared flight trait | **Reject clade.** Do not generalize Phantom → Ghast |
| Phantom ↔ Bat / Bee / Parrot | Some shared `#fall_damage_immune`; all can be “flying” in speech | Distinct classes / AI / spawn | No | Identity keys already differ | Compatibility doc lists flight as eventual Bat-centric sketch only (PLANNING) | **Reject** shared aerial-predator / flight trait |
| Phantom ↔ Wither / other `#undead` | Tag + HostType UNDEAD | Vanilla tags; WitherBoss `WITHER_FRIENDS`; Smite; LivingEntity effect inversion | Tag gameplay, not composition | `HostType.UNDEAD` already groups registry routing | Vanilla consumers only; BioCraft uses HostType for suitability routing | **Reject** undead-flying category. **Do not reopen** |
| Phantom ↔ `#minecraft:zombies` / Zombie Horse | None in 1.21.1 tags | Phantom is listed on `UNDEAD` **beside** `#zombies`, not inside it | No | Separate organismKey | None | **Reject** zombie-family grouping |
| Phantom ↔ player insomnia | Spawn gate uses player `TIME_SINCE_REST` | `PhantomSpawner` + Player stats + beds | No. Spawn ≠ origin | None | None | **Reject** insomnia-adaptation biology |
| Phantom ↔ Overworld | Custom spawner installed on Overworld only | `MinecraftServer.createLevels` | No. World hook ≠ native origin | None | None | **Reject** dimension-as-origin |
| Phantom ↔ membrane / Elytra / Slow Falling | Loot item consumed by brewing and anvil | Loot table, `PotionBrewing`, `ElytraItem` | No | None | None | **Reject** membrane anatomy |
| Phantom ↔ Cat | Swoop abort + hiss | Phantom goal + `Cat.hiss()` | No | None | None | **A** encounter rule |
| Phantom as future `contributingSourceKey` | Identity key already exists | Model A / resolver | Only identity of a contributing organism definition | `organismKey` / contributing source already distinguish organisms | Analyzer displays contributing source when present | **B** if ever eligible; **not earned now**; eligibility locked false |

---

## AlienCraft consumer classification (Phantom-specific)

| Location | Classification | Notes |
|----------|----------------|-------|
| `hosts.json` `"phantom"` | **LIVE** | Participation + `default_dna` routing |
| `HostConfigParser` / `MobHostRegistry` / `HostConfigLoader` | **LIVE** | Generic loaders; Phantom is one string among undead mobs |
| `HostType.UNDEAD` / `HostEligibilityService` | **LIVE** | Suitability false; locked |
| `host_effects/undead.json` | **LIVE** | Shared undead attachment pack, not Phantom-specific |
| `BiologicalProfileResolver` / `BiologicalProfilePort` / `CompiledBiologicalProfile` | **LIVE** | Generic identity resolve; would distinguish Phantom by `organismKey` |
| DNA Analyzer / vials / `DnaSampleFromOccupant` | **LIVE** | Generic identity projection; no Phantom field |
| Chestburster/Drone `contributingSourceKey` | **LIVE** | Generic Model A; no Phantom authoring |
| `mob_catalog.json` | **PARSE-ONLY / PLANNING** | Phantom absent from live bootstrap and from the deep matrix mob list |
| Manifestation / inventory / compatibility / ROADMAP mentions | **PLANNING ONLY** | Must not be treated as consumers |
| JUnit | **TEST ONLY** | No test names `"phantom"`; generic registered-mob coverage only |
| Phantom entity/AI/renderer/lifecycle Java | **DEAD-UNUSED** | Does not exist in AlienCraft |
| Unknown remaining hooks | **UNKNOWN** — none found after Java/JSON/test search | |

---

## Final evidence conclusion

```
New BP field earned: NO
Existing composition sufficient: YES
Named consumer exists: NO
Architectural escalation required: NO
```

**Read of those four lines:**

- **New BP field earned: NO** — every investigated Phantom behavior has a vanilla or existing-identity owner. Flight, swoop, insomnia spawn, sunlight, tags, loot, model, and size are **A**. Registry identity is already **B**.
- **Existing composition sufficient: YES** — `organismKey="phantom"` plus existing Host Registry `HostType.UNDEAD` / `hostEffectProfileId="undead"` already distinguish Phantom from other organisms. No missing biological fact is required by a live consumer.
- **Named consumer exists: NO** — no named live BioCraft consumer needs a Phantom-specific biological distinction (flight trait, insomnia biology, membrane anatomy, undead-flying clade). Generic identity consumers already work without new fields. Planning matrices and compatibility sketches are not consumers.
- **Architectural escalation required: NO** — nothing to document as a BP-boundary gap.

**Hard gates held:**

```text
Phantom-specific gameplay rules  ≠  generic biological flight
player insomnia as a spawn condition  ≠  Phantom biological origin
#minecraft:undead / HostType.UNDEAD  ≠  undead-flying biological category
FlyingMob parent  ≠  clade with Ghast
```

Do **not** mint DESIGN-BIO-MANIFEST-004, Feature IDs, BP fields, traits, profiles, or Host Registry edits from this packet.
