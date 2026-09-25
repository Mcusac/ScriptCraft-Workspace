TEMPORARY EVIDENCE — NOT PROJECT SSOT

Do not treat this file as canonical design documentation.
Do not promote into manifestations/polar_bear.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Polar Bear — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register or unregister Polar Bear as a conclusion of this investigation.** Polar Bear is already in `vanilla_hosts.living_biological`. Registration is participation, not extra biology. Host Registry presence ≠ automatic A (and ≠ C).

**Isolation:** Minecraft Java **1.21.1** / NeoForge **21.1.208** mapped sources under `.tmp_mc_sources/`, live BioCraft under `biocraft-alien/src`, and this packet’s own reads only. Sibling packets were **not** absorbed as evidence.

Method (every behavior): existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied independently: `Animal` parent ≠ clade; cold/frozen spawn biome ≠ origin/adaptation; Host Registry ≠ eligibility science ≠ manifestation completeness; `DATA_STANDING_ID` / anger persistence ≠ BP merely because persistent; fish loot ≠ diet composition; `#freeze_immune_entity_types` membership ≠ automatic BP field; `EntityType.immuneTo(POWDER_SNOW)` ≠ walk-on-powder-snow; live `contributingSourceKey=polar_bear` is **B**, not **C**. Cold was **not** pre-classified as non-biological: freeze/`immuneTo` facts were traced to owners and consumers first.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey` (Model A Chestburster/Drone), optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

**Default: NO new BP field.**

---

## Subject

Polar Bear (`minecraft:polar_bear`) — living Polar Bear identity on Minecraft Java **1.21.1**. Scope: EntityType registration (incl. powder-snow `immuneTo`); adult/baby age; protective / anger / targeting AI; swimming vs land movement; melee + standing warning; player proximity; breeding/offspring (incl. food and `BreedGoal` absence); spawn conditions (biome + ice alternate); freeze / powder-snow tags and EntityType flags; loot (cod/salmon); Host Registry `living_biological`; BioCraft identity routing; mob-catalog / xenomorph-variant stub audit.

Out of scope as organisms: Fox (prey/avoid adjacency only). Freeze-immune tag co-members (Stray, Snow Golem, Wither) are **not** absorbed.

---

## Version

Minecraft Java **1.21.1** / NeoForge **21.1.208**.

- `biocraft-alien/gradle.properties`: `minecraft_version=1.21.1`; `neo_version=21.1.208` (project gate).
- Temporary source cache (not SSOT): `.tmp_mc_sources/` extracted from `biocraft-alien/build/moddev/artifacts/neoforge-21.1.208-sources.jar` and `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar`.
- This pass extracted missing helpers `RandomStrollGoal.java`, `TimeUtil.java`, `UniformInt.java`, plus biome JSON `frozen_ocean.json` / `deep_frozen_ocean.json` / `ice_spikes.json`.
- Wiki = orientation only; **source wins**. Missing required source → **UNKNOWN** (no wiki/superclass/sibling inference).

---

## Phase 1 gate

| Required probe source | Status |
|-----------------------|--------|
| `.tmp_mc_sources/.../animal/PolarBear.java` | **PRESENT** |
| Inner goals (`PolarBearMeleeAttackGoal`, `PolarBearHurtByTargetGoal`, `PolarBearAttackPlayersGoal`) | **PRESENT** (nested in `PolarBear.java`) |
| `NeutralMob.java` | **PRESENT** |
| `Animal.java` / `AgeableMob.java` | **PRESENT** |
| `FloatGoal` / `FollowParentGoal` / `LookAtPlayerGoal` / `MeleeAttackGoal` / `PanicGoal` / `RandomLookAroundGoal` / `RandomStrollGoal` | **PRESENT** (`RandomStrollGoal` extracted this pass) |
| `HurtByTargetGoal` / `NearestAttackableTargetGoal` / `ResetUniversalAngerTargetGoal` | **PRESENT** |
| `Fox.java` (prey type referenced by Polar Bear) | **PRESENT** |
| `EntityType.java` (`POLAR_BEAR` builder) | **PRESENT** |
| `DefaultAttributes.java` | **PRESENT** |
| `SpawnPlacements.java` | **PRESENT** |
| `Entity.java` (`canFreeze`) | **PRESENT** |
| `LivingEntity.java` (`getWaterSlowDown`) | **PRESENT** |
| `PowderSnowBlock.java` | **PRESENT** |
| `EntityTypeTags.java` / freeze + powder-snow tags JSON | **PRESENT** |
| Spawn alternate biome/block tags + loot JSON | **PRESENT** |
| `TimeUtil.java` / `UniformInt.java` (anger timer factory) | **PRESENT** (extracted this pass) |
| `PolarBearRenderer.java` / `PolarBearModel.java` | **PRESENT** (presentation) |
| BioCraft `hosts.json`, `mob_catalog.json`, xenomorph `polar_bear.json`, resolver / gestation / Analyzer path | **PRESENT** under `biocraft-alien/` |

Gate **PASS** — probes below are source-backed (not UNKNOWN from missing class).

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:polar_bear` |
| `EntityType` | `EntityType.POLAR_BEAR` — `EntityType.java` **563–564**: `register("polar_bear", Builder.of(PolarBear::new, MobCategory.CREATURE).immuneTo(Blocks.POWDER_SNOW).sized(1.4F, 1.4F).clientTrackingRange(10))` |
| Fire / lava | Builder does **not** call `.fireImmune()` |
| Powder snow (EntityType) | **`.immuneTo(Blocks.POWDER_SNOW)`** — `EntityType.isBlockDangerous` returns false when block ∈ `immuneTo` (**1117–1119**) |
| Class | `PolarBear extends Animal implements NeutralMob` (`PolarBear.java` **53**) |
| Category | `MobCategory.CREATURE` |
| Dimensions | Adult **1.4 × 1.4**; client standing scales height via `getDefaultDimensions` (**217–224**) |
| Default attributes | `DefaultAttributes.java` **139** → `PolarBear.createAttributes()`: health **30**, follow **20**, movement **0.25**, attack **6** (`PolarBear.java` **100–106**) |
| Host Registry | **REGISTERED.** `hosts.json` `vanilla_hosts.living_biological.mobs` includes `"polar_bear"` (**8**). `default_dna`: `baseline_biological` (**4**). `variant_mappings` has **no** polar_bear entry (**47–52**) |
| Suitability | Registered `LIVING_BIOLOGICAL` → `HostType.isSuitableForXenomorph() == true` (`HostType.java` **17**). `MobHostRegistry.isSuitableForXenomorph("polar_bear")` **true**. Registered ≠ extra biology ≠ BP field |
| Inventory baseline | `vanilla_organism_inventory.md` **155**: bio-organic, registered, `LIVING_BIOLOGICAL`, manifestation **pending** (planning pointer only) |

Independent existence paths (not origin): spawn egg / `/summon`; CREATURE biome spawn (`snowy_plains.json`, `ice_spikes.json` via `BiomeDefaultFeatures.snowySpawns`; `frozen_ocean.json` / `deep_frozen_ocean.json` via `OverworldBiomes.frozenOcean`); ice / frosted-ice `isValidSpawn` allowing only `POLAR_BEAR`.

---

## Mechanic classification (pre A/B/C)

| Mechanic | Class |
|----------|-------|
| Registry id / EntityType / Host Registry key | **identity** |
| Age / baby (`AgeableMob`) | **persistent entity state** |
| Persistent anger UUID + remaining time (`NeutralMob` NBT) | **persistent entity state** (combat, not biological subtype) |
| Synched standing flag + client stand animation | **transient gameplay state** |
| Warning sound tick counter | **transient gameplay state** |
| Protective targeting / melee / fox hunt / panic / look | **transient gameplay state** (AI) |
| Spawn biome lists / alternate ice spawn rules / ice block `isValidSpawn` | **environmental interaction** (encounter placement) |
| `#freeze_immune_entity_types` → `Entity.canFreeze()` | **environmental interaction** (damage rule keyed by EntityType tag) |
| `EntityType.immuneTo(POWDER_SNOW)` → `isBlockDangerous` | **environmental interaction** (path/danger rule on EntityType) |
| Not in `#powder_snow_walkable_mobs` | **environmental interaction** (collision/walk rule — Polar Bear **absent**) |
| `getWaterSlowDown() == 0.98F` | **transient gameplay state** / movement (numeric travel factor) |
| Death loot cod/salmon | **item/block production** |
| No food item / no `BreedGoal` | **absence** (reproduction input / AI) |
| `getBreedOffspring` → `EntityType.POLAR_BEAR` | **entity/state transformation** (same-type factory when breeding fires) |
| Host / gestation / Analyzer `organismKey` / `contributingSourceKey` | **actual biological input consumed by BioCraft** (identity only) |

---

## Behavior ownership table

Method: **owner → biological input? → existing composition? → named live BioCraft consumer? → A/B/C**

| Behavior | Actual owner | Manifestation class | Biological input? | Existing composition? | Named live BioCraft consumer? | A/B/C |
|----------|--------------|---------------------|-------------------|----------------------|-------------------------------|-------|
| Identity / CREATURE / dims / tracking | `EntityType.POLAR_BEAR` | identity | Identity only | `organismKey=polar_bear` | Resolver / Analyzer / host lookup | **B** |
| Host participation / suitability | `hosts.json` + `MobHostRegistry` + `HostEligibilityService` | identity / BioCraft route | Participation key only | `HostType.LIVING_BIOLOGICAL` + `baseline_biological` | **LIVE** eligibility | **B** |
| Live host → `contributingSourceKey` | `GestationManager.writeContributingSource` | BioCraft-consumed identity | `encodeId` → registry path `"polar_bear"` | optional `contributingSourceKey` | **LIVE** gestation writer + Analyzer report lines | **B** |
| Attributes / attack damage | `PolarBear.createAttributes` | identity stats | **No.** Vanilla numbers | Not needed | None | **A** |
| Adult vs baby age | `AgeableMob` age / `DATA_BABY_ID` | persistent entity state | Vanilla age | Not needed | None | **A** |
| Natural group baby chance | `PolarBear.finalizeSpawn` → `AgeableMobGroupData(1.0F)` then `AgeableMob.finalizeSpawn` | persistent entity state at spawn | Spawn group data: baby chance **1.0** when `groupSize > 0` (`PolarBear.java` **245–250**; `AgeableMob.java` **28–41**, **183–185**) | Not needed | None | **A** |
| Food / player breeding feed | `PolarBear.isFood` → **always `false`** | absence | **No** breed item; `Animal.mobInteract` food path never starts | Not needed | None | **A** |
| Breed AI | Polar Bear `registerGoals` | absence | **No** `BreedGoal`; `Mob.registerGoals` empty; `Animal` does not add one | Not needed | None | **A** |
| Offspring factory (if breeding occurs) | `getBreedOffspring` | entity transformation | Same type `EntityType.POLAR_BEAR.create` (**70–72**); `Animal.spawnChildFromBreeding` sets baby | Child key remains `polar_bear` | None needing breed trait | **A** |
| Inherited biological state on offspring | (none beyond Animal age machinery) | — | **No** PolarBear-owned variant/NBT copied in `getBreedOffspring` | Identity sufficient | None | **A** |
| Float / surface in water | `FloatGoal` priority 0 | transient AI | Jump-in-fluid when water/lava above threshold | Not needed | None | **A** |
| Water travel slowdown | `PolarBear.getWaterSlowDown` → **0.98F** (vs `LivingEntity` default **0.8F**) | transient movement | Numeric travel | Not needed | None | **A** |
| Land stroll / look | `RandomStrollGoal` 1.0 / `LookAtPlayerGoal` 6.0F / `RandomLookAroundGoal` | transient AI | Movement / player look | Not needed | None | **A** |
| Follow parent (baby) | `FollowParentGoal` 1.25 | transient AI | Age-gated AI | Not needed | None | **A** |
| Panic | `PanicGoal` — baby uses `PANIC_CAUSES`; adult `PANIC_ENVIRONMENTAL_CAUSES` | transient AI | Damage-tag gate | Not needed | None | **A** |
| Melee + standing warning | `PolarBearMeleeAttackGoal` + `DATA_STANDING_ID` | transient combat / presentation | Synched standing **not** NBT-saved in PolarBear add/read (only anger via NeutralMob) | Not needed | Client model/renderer only | **A** |
| Hurt-by + alert adults | `PolarBearHurtByTargetGoal` | transient AI | Baby hurt → `alertOthers` then stop; `alertOther` only adult `PolarBear` | Not needed | None | **A** |
| Protect cubs → attack players | `PolarBearAttackPlayersGoal` | transient AI | Adult only; requires baby Polar Bear in inflate **8×4×8**; follow distance ×0.5 (**253–279**) | Not needed | None | **A** |
| Anger at players (universal anger) | `NearestAttackableTargetGoal` + `NeutralMob.isAngryAt` | persistent/transient anger | Timer `TimeUtil.rangeOfSeconds(20, 39)` → **400–780** ticks; NBT `AngerTime`/`AngryAt` | Not needed | None | **A** |
| Hunt Fox | `NearestAttackableTargetGoal<>(…, Fox.class, …)` | transient AI | Hardcoded prey type | Not needed | None | **A** |
| Reset anger | `ResetUniversalAngerTargetGoal` | transient AI | NeutralMob machinery; Polar Bear passes `alertOthersOfSameType=false` | Not needed | None | **A** |
| **Freeze immunity** | `#minecraft:freeze_immune_entity_types` ⊇ `polar_bear` → `Entity.canFreeze()` **false** | environmental interaction | Tag membership on EntityType | **Not** a BP field without consumer | **None** in BioCraft reading this tag | **A** |
| **Powder-snow block danger immunity** | `EntityType` builder `.immuneTo(POWDER_SNOW)` → `isBlockDangerous` false | environmental interaction | EntityType `immuneTo` set | Not needed | **None** BioCraft | **A** |
| Powder-snow **walk** | `#powder_snow_walkable_mobs` | environmental interaction | Polar Bear **NOT** a member (rabbit/endermite/silverfish/fox only) → sinks unless boots | Not needed | None | **A** |
| Natural spawn (snowy plains / ice spikes) | `BiomeDefaultFeatures.snowySpawns` + biome JSON | environmental encounter | Weight 1, count 1–2 | Spawn ≠ origin | None | **A** |
| Natural spawn (frozen ocean) | `OverworldBiomes.frozenOcean` + `frozen_ocean.json` / `deep_frozen_ocean.json` | environmental encounter | Same weight/count | Spawn ≠ origin | None | **A** |
| Alternate spawn floor (ice biomes) | `checkPolarBearSpawnRules` + biome tag + block tag | environmental encounter | If biome ∈ `#polar_bears_spawn_on_alternate_blocks` (`frozen_ocean`, `deep_frozen_ocean`) → bright enough + below ∈ `#polar_bears_spawnable_on_alternate` (`ice`); else default animal rules (`PolarBear.java` **108–115**) | Encounter | None | **A** |
| Ice / frosted ice valid spawn | `Blocks.ICE` / `Blocks.FROSTED_ICE` `isValidSpawn` → only `EntityType.POLAR_BEAR` | environmental encounter | Block property, not organism NBT | Encounter | None | **A** |
| Placement registration | `SpawnPlacements` ON_GROUND + `PolarBear::checkPolarBearSpawnRules` | environmental encounter | Placement API | None | None | **A** |
| Entity loot | `loot_table/entities/polar_bear.json` | item production | Cod (weight 3) / salmon; smelt-on-fire; looting | Loot ≠ diet BP | None | **A** |
| Client texture / scale / stand pose | `PolarBearRenderer` single texture `textures/entity/bear/polarbear.png`; scale **1.2**; `PolarBearModel.setupAnim` uses standing scale | presentation | One skin; no variant | Not needed | None | **A** |
| Mob-catalog deep matrix row | `mob_catalog.json` `deep_mob_configs.neutral.mobs` includes `"polar_bear"` | PLANNING config text | **Not loaded** at init | N/A | **Not** a live loader input | **A** (planning only; not consumer) |
| Xenomorph variant JSON on disk | `entity/xenomorph/mob-based/neutral/organic/polar_bear.json` | STUB / DEAD file | `variant_id=polar_bear`, multipliers **1.0**, description says stub | N/A | **Not** in `bootstrap_entries` → `MobEntityConfigLoader` **never loads** it | **A** (dead stub ≠ C) |

**No row is C.** Live `contributingSourceKey=polar_bear` is identity already Model **B**. Freeze/powder-snow distinctions are **real Minecraft-stored EntityType/tag facts**, but no named live BioCraft consumer needs them beyond identity.

---

## Polar Bear cold / behavior probe (mandatory)

### Adult / baby
- Age via `AgeableMob` (`setAge(-24000)` baby path).
- Goals: babies panic on broader damage tags; babies do not use `PolarBearAttackPlayersGoal` (`isBaby()` → `canUse` false); baby hurt alerts adults then that baby’s hurt-by goal stops; `FollowParentGoal` present.
- Ambient sound baby vs adult (`POLAR_BEAR_AMBIENT_BABY` vs `POLAR_BEAR_AMBIENT`).
- Spawn: `finalizeSpawn` installs `AgeableMobGroupData(1.0F)` → **100%** baby chance for subsequent group members (`groupSize > 0`).

### Protective behavior / anger / targeting / player proximity
- Cub protection: adult scans for baby Polar Bear in AABB inflate 8/4/8; then targets player (`PolarBearAttackPlayersGoal`).
- Hurt-by: baby alerts adult Polar Bears only (`alertOther` instanceof PolarBear && !baby).
- Persistent anger: `NeutralMob` fields + NBT via `readPersistentAngerSaveData` / `addPersistentAngerSaveData`; timer sample 20–39 seconds (400–780 ticks); server `updatePersistentAnger` each tick.
- Additional player target when `isAngryAt`; fox always targetable (nearest goal, `mustReach=true`).
- `LookAtPlayerGoal` range **6.0F** — look AI, not attack.

### Swimming / land / attack
- `FloatGoal(0)`; water slowdown **0.98F** (less damping than default **0.8F**). **No** `canBreatheUnderwater` override in `PolarBear.java`.
- Land: stroll 1.0; melee speed 1.25; standing synched during wind-up; warning sound (40-tick cooldown).
- Attack damage attribute **6.0**.

### Breeding / offspring / food
- `isFood` **always false** → Animal food-interact love path never starts from items.
- **No** `BreedGoal` registered (Polar Bear goals only; `Mob.registerGoals` empty).
- `getBreedOffspring` still returns `EntityType.POLAR_BEAR.create` (same-type factory) if love/breeding is forced by other means — **no** PolarBear-specific inherited variant.
- **Absence recorded:** no breed item tag; no PolarBear-owned heritable cold/variant NBT; no BreedGoal.

### Spawn conditions
- Snowy plains / ice spikes datapack JSON: CREATURE polar_bear weight 1, min 1, max 2 (matches `snowySpawns`).
- Frozen ocean / deep frozen ocean datapack JSON: same CREATURE entry (matches `OverworldBiomes.frozenOcean`).
- Frozen ocean biomes also use alternate ice floor rules via biome/block tags.
- Ice & frosted ice blocks: `isValidSpawn` exclusive to Polar Bear.
- **Encounter ≠ origin.**

### Persistent variant / state
- **No** cold variant enum, **no** snow/ice NBT flag on Polar Bear.
- Synched: `DATA_STANDING_ID` (attack presentation) — not written in PolarBear NBT overrides.
- Persistent: NeutralMob anger UUID/time only (+ AgeableMob age / Animal InLove from parents).

### Effects / item production
- Loot: cod (weight 3) / salmon; furnace-smelt if burning / smelts_loot. **Item production ≠ composition.**
- No PolarBear-applied potion effects found in class.

### Freeze / powder-snow — encounter vs stored distinction

| Fact Minecraft stores | Owner | Consequence | BioCraft consumes? |
|-----------------------|-------|-------------|--------------------|
| Biome spawn in snowy plains / ice spikes / frozen ocean | Worldgen / spawn lists | Encounter placement | **No** |
| Alternate spawn on `ice` in frozen oceans | `checkPolarBearSpawnRules` + tags | Encounter floor rule | **No** |
| Ice / frosted ice `isValidSpawn` exclusive | Block property | Encounter | **No** |
| `#freeze_immune_entity_types` includes `polar_bear` | `Entity.canFreeze` | No freeze damage ticks from freeze path | **No** |
| `EntityType.immuneTo(POWDER_SNOW)` | `EntityType.isBlockDangerous` | Powder snow not “dangerous block” for this type | **No** |
| Not in `#powder_snow_walkable_mobs` | `PowderSnowBlock.canEntityWalkOnPowderSnow` | Does **not** walk on powder snow via tag | **No** |

**Conclusion of probe:** Minecraft **does** store cold-adjacent **EntityType/tag** distinctions (freeze immune + powder-snow `immuneTo`), distinct from mere cold biome spawn. Those are vanilla environmental/damage owners, not per-instance biological NBT and not a Polar Bear variant. BioCraft does **not** consume them. Therefore they remain **A**, not a BP field and **not C**. Do **not** infer “cold adaptation” biology from spawn alone; do **not** invent a cold-adaptation consumer. Cold was evaluated as a possible biological distinction and **failed C** for lack of a named live consumer, not because cold was assumed non-biological.

---

## BioCraft consumer audit

Search (`rg polar_bear|PolarBear` under `biocraft-alien`, excluding `build/` / `.gradle/`): JSON/resources only; **no Java**; **no tests**.

| Artifact | Path / symbol | Classification | Consumes `organismKey` / `contributingSourceKey`? |
|----------|---------------|----------------|---------------------------------------------------|
| Host Registry | `hosts.json` `"polar_bear"` in `living_biological` | **LIVE** | Key → `HostType` / DNA profile id / suitability |
| Eligibility | `HostEligibilityService` → `MobHostRegistry.isSuitableForXenomorph` | **LIVE** | Mob name string (= organism key path) |
| Gestation copy | `GestationManager.writeContributingSource` | **LIVE** | Writes host registry path onto Chestburster |
| Biological Profile resolve | `BiologicalProfileResolver.resolve(ref, contributingSourceKey)` | **LIVE** | Assembles sparse profile from key + optional contributing source; **no** freeze/powder fields (`CompiledBiologicalProfile` identity refs only) |
| Analyzer UI | `DnaAnalysisReportLines` / vial helpers | **LIVE** | Displays organism + contributing source |
| `variant_mappings` | `hosts.json` | **Absent** for polar_bear | `MobHostRegistry.getVariant("polar_bear")` → null |
| `SpecializedXenomorphManager.getSpecializedVariant` | wraps `getVariant` | **DEAD** API | **No callers** besides the method definition |
| `mob_catalog.json` `bootstrap_entries` | loads spider/creeper/wolf/enderman only | **LIVE** loader list — **polar_bear not listed** | N/A |
| `mob_catalog.json` `deep_mob_configs.neutral` | includes `"polar_bear"` | **PLANNING** (comment: content planning; bootstrap is what loads) | **Not consumed** by `MobEntityConfigLoader` |
| `…/neutral/organic/polar_bear.json` | on-disk variant stub | **STUB / DEAD** (file exists; multipliers 1.0; **not** bootstrap-loaded) | Would parse `variant_id` **if** loaded — currently **not** |
| Texture `…/neutral/organic/polar_bear.png` | on-disk asset | **STUB** | Unused while variant JSON is not loaded |
| Java sources under `biocraft-alien` | `rg polar_bear` / `PolarBear` | **No Java references** | — |
| Tests | same search | **No polar_bear tests** | — |
| Freeze / powder-snow tags | vanilla only | **No BioCraft consumer** | — |

**Existing-consumer hypothesis verified:** hosts / resolver / gestation / Analyzer **do** consume organism identity (`organismKey` / registry path → `contributingSourceKey`). That earns **B for identity only**. It does **not** prove freeze immunity, protective AI, or spawn ecology are represented in composition. **C not earned** — no named live consumer needs a missing biological distinction.

---

## Configuration audit

| Config | Polar Bear fact |
|--------|-----------------|
| `hosts.json` living_biological | **Present** `"polar_bear"` |
| `hosts.json` variant_mappings | **Absent** |
| `mob_catalog.json` bootstrap_entries | **Absent** (not loaded) |
| `mob_catalog.json` deep_mob_configs | **Listed** under neutral/organic planning matrix |
| Xenomorph mob-based JSON | **File present**, stub multipliers; **DEAD** to runtime loader |
| DNA default | `baseline_biological` via living_biological group |
| Inventory row | pending manifestation (orientation only) |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails on 1.21.1 evidence |
|----------------|----------------------------------|
| Cold biome spawn ⇒ cold-adaptation BP | Spawn/worldgen encounter only; no organism cold NBT/variant |
| `#freeze_immune` ⇒ must mint freeze/cold BP field | Tag has vanilla owner (`Entity.canFreeze`); **no** BioCraft consumer → **A**. Not rejected because “cold cannot be biological.” |
| `immuneTo(POWDER_SNOW)` ⇒ powder-snow walk / adaptation trait | Separate from walkable tag; Polar Bear **not** walkable; danger immunity only; no BioCraft consumer |
| Shared freeze-immune set with Snow Golem/Stray/Wither ⇒ clade | Tag co-membership ≠ clade |
| `extends Animal` ⇒ livestock/mammal clade | Parent ≠ clade |
| Protective cub AI ⇒ maternal biology field | Goal/AI owner; no consumer |
| Better water slowdown ⇒ aquatic adaptation field | Numeric `getWaterSlowDown`; no consumer |
| Cod/salmon loot ⇒ piscivore composition | Loot table ≠ diet BP |
| Host Registry registered ⇒ every manifestation represented / C | Participation route only; identity **B** |
| On-disk `polar_bear.json` xenomorph stub ⇒ live specialized consumer / C | Not in `bootstrap_entries`; loader never reads it → **DEAD/STUB** |
| `deep_mob_configs` listing ⇒ live | Explicitly planning matrix; bootstrap is SSOT for load |
| Standing synched flag ⇒ persistent biological posture | Transient attack presentation; not PolarBear NBT |
| Anger UUID persistence ⇒ biological aggression subtype | NeutralMob combat state |
| Baby spawn chance 1.0 ⇒ developmental BP | Vanilla `AgeableMobGroupData` spawn rule |
| Fox avoid Polar Bear ⇒ shared biology | Fox AI adjacency only |

---

## Potential biological relationships

| Relationship | Evidence stance |
|--------------|-----------------|
| Polar Bear ↔ Fox | Polar Bear hunts Fox; Fox `AvoidEntityGoal` Polar Bear **8.0F** — combat AI only, **not** ancestry/clade |
| Polar Bear ↔ freeze-immune tag peers | Shared **damage rule** tag — **not** clade |
| Polar Bear ↔ ice blocks | Spawn validity / alternate floor — **encounter** |
| Polar Bear as Model A host | Live `contributingSourceKey=polar_bear` identity **B** |
| Polar Bear specialized xenomorph variant | Planning/stub only until bootstrap lists it — **not** proven live biology need |

Do **not** absorb Fox, Snow Golem, Stray, or Wither into this organism’s composition from this packet.

---

## Reproduction / lifecycle minimum

| Question | 1.21.1 finding |
|----------|----------------|
| Player breeding via food? | **No** — `isFood` always false |
| BreedGoal present? | **No** |
| Offspring EntityType? | `minecraft:polar_bear` via `EntityType.POLAR_BEAR.create` |
| Age on offspring? | Standard AgeableMob baby age when breeding path runs (`spawnChildFromBreeding` → `setBaby(true)`); natural spawn group uses **1.0F** baby chance after first |
| Inherited PolarBear-specific persistent state? | **None** in `getBreedOffspring` (no variant/cold flag) |
| BioCraft consumption of breed/cold traits? | **None** — only host identity if gestated |

Absence of food breeding / BreedGoal is **evidence**, not a gap to fill with a BP field.

---

## Final evidence conclusion

| Question | Answer |
|----------|--------|
| New BP field? | **NO** |
| Existing composition sufficient? | **YES** (`organismKey` / optional `contributingSourceKey` + HostType/DNA profile ids already used) |
| Named live consumer? | **YES** — Host Registry / eligibility / gestation contributing-source writer / BiologicalProfileResolver / Analyzer (identity only). Freeze/powder-snow/protective AI: **no** named BioCraft consumer |
| Architectural escalation? | **NO** |
| **C earned?** | **NO** |

### A/B/C counts (behavior ownership rows)

| Result | Count |
|--------|------:|
| **A** | **30** |
| **B** | **3** (identity EntityType; Host eligibility; gestation/Analyzer contributing-source identity) |
| **C** | **0** |

**C was not earned.** Cold-adjacent EntityType/tag facts are proven as vanilla owners without BioCraft consumption; identity participation is **B**.
