TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Strider docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/strider.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Strider — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register Strider as a conclusion of this investigation.**

Leftover `.tmp_manifestation_evidence/strider.md` was **orientation only**. Every owner below was re-read independently from `.tmp_mc_sources/` and live `biocraft-alien/` for this rewrite. Leftover conclusions are **not** SSOT.

Method (every behavior): existing gameplay → actual owner → manifestation class → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**. Prefer disprove **C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied independently: shared parent ≠ clade; tag ≠ clade; conversion ≠ inheritance; spawn biome ≠ origin; equipment ≠ capability; Host Registry ≠ eligibility; Host Registry absence ≠ consumer absence; interesting behavior ≠ consumer; `fireImmune` ≠ lava-walk ≠ warm-state; shared warped-fungus **item/block name** ≠ shared fungus trait with Hoglin; `ItemSteerable`/`Saddleable` ≠ rideable clade with Horse/Pig; Strider ≠ Ghast flight / Nether-column anatomy.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey` (Model A Chestburster/Drone), optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

This organism is investigated independently. No architectural decision is shared with Hoglin, Piglin, Horse, Pig, or Ghast.

---

## Subject

Strider (`minecraft:strider`) — identity; **thermal warm/cold** (`DATA_SUFFOCATING` / `isSuffocating` / `setSuffocating`) vs lava environment / `#strider_warm_blocks` vs `fireImmune` vs lava standing; reproduction (food / breed / offspring / age); warped-fungus food vs tempt vs stick vs Hoglin `#hoglin_repellents`; saddle / `ItemSteerable`; zombified-piglin jockey; spawn/biome JSON; loot; tags with named consumers; Host Registry **absence**; live BioCraft consumer search despite that absence.

Out of scope as organisms: Hoglin, Piglin, Piglin Brute, Horse, Pig, Ghast, Magma Cube, Blaze (cited only where owners contrast).

---

## Version

Minecraft Java **1.21.1** / NeoForge **21.1.208**.

- `biocraft-alien/gradle.properties`: `minecraft_version=1.21.1` (**15**); `minecraft_version_range=[1.21.1,1.22)` (**19**); `neo_version=21.1.208` (**21**).
- Temporary source cache (not SSOT): `.tmp_mc_sources/`.
- Wiki = orientation / disagreement discovery only. **Source wins.** Missing source → **UNKNOWN**; no wiki / superclass / sibling inference.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:strider` |
| `EntityType` | `EntityType.STRIDER` — `EntityType.java` **659–661**: `register("strider", Builder.of(Strider::new, MobCategory.CREATURE).fireImmune().sized(0.9F, 1.7F).clientTrackingRange(10))` |
| Fire / lava HP flag | **Yes** `.fireImmune()` on builder (**660**). Builder default `fireImmune` false (**1254**); setter **1344–1346**. Runtime: `Entity.fireImmune()` **1212–1213** → `getType().fireImmune()` **1038–1039**. `Entity.lavaHurt()` **530–536** no-ops when `fireImmune()`. `isInvulnerableTo` treats `IS_FIRE` as invulnerable when `fireImmune()` (**2684**). **EntityType registration flag — not warm-state, not lava-walk anatomy, not Nether-origin** |
| Class | `Strider extends Animal implements ItemSteerable, Saddleable` (`Strider.java` **74**). Package `entity.monster`; category **CREATURE**. Package/parent mix ≠ clade |
| Category | `MobCategory.CREATURE` |
| Summonable | Builder does **not** call `noSummon()`; summon defaults true (`EntityType.Builder` **1253**); `canSummon()` **1034–1036** |
| Spawn egg | `Items.STRIDER_SPAWN_EGG` (`Items.java` **1494–1496**) |
| Attributes | `DefaultAttributes.java` **155**: `EntityType.STRIDER` → `Strider.createAttributes()`. Stats (`Strider.java` **356–358**): movement **0.175**, follow range **16.0**. Max health not overridden on Strider (living default path via `Mob.createMobAttributes`) |
| Dimensions | Hitbox **0.9 × 1.7** |
| Host Registry | **UNREGISTERED.** `hosts.json` (`biocraft-alien/src/main/resources/data/biocraft_alien/systems/hosts.json` **1–53**): no `"strider"` in `living_biological`, `undead`, `unsuitable.{construct,inorganic,elemental,spiritual}`, `modded_hosts`, or `variant_mappings`. `MobHostRegistry.getHostType("strider")` → **null** (**46–48**). `isSuitableForXenomorph("strider")` → **false** because `hostType == null` (**68–71**) |
| Inventory row | Planning inventory mentions `strider` / bio-organic / unregistered / pending (`vanilla_organism_inventory.md`). Inventory ≠ HostType ≠ biology. This packet does **not** edit it |

Independent existence paths (not origin): spawn egg, `/summon` (`canSummon` true), natural lava-column spawn in all five 1.21.1 Nether biome JSONs, breeding offspring `Strider.getBreedOffspring`.

---

## Source-completeness table

| Source / owner | Present in `.tmp_mc_sources` / live tree? | Used for |
|----------------|-------------------------------------------|----------|
| `Strider.java` | **YES** | Thermal, AI, food, tempt, saddle, jockey, spawn rules, water, fire presentation |
| `StriderRenderer.java` | **YES** | Cold texture / shake from `isSuffocating` |
| `ItemBasedSteering.java` / `ItemSteerable.java` / `Saddleable.java` | **YES** | Saddle NBT `"Saddle"`; boost; interface contracts |
| `FoodOnAStickItem.java` + `Items.java` STRIDER/PIG bindings | **YES** | Stick steer EntityType binding |
| `Animal.java` / `AgeableMob.java` | **YES** | Love, growth, mate, baby spawn chance, offspring setBaby |
| `EntityType.java` STRIDER + `fireImmune` | **YES** | Identity / flag |
| `Entity.java` lavaHurt / fireImmune / dismountsUnderwater | **YES** | Flag runtime vs presentation |
| `LivingEntity.java` freeze ×5 / water sensitivity | **YES** | Tag consumers |
| `SpawnPlacements.java` + `SpawnPlacementTypes.IN_LAVA` | **YES** | Encounter placement |
| `#strider_warm_blocks` / `#strider_food` / `#strider_tempt_items` JSON | **YES** | Warm / food / tempt |
| `#hoglin_repellents` + `HoglinSpecificSensor` | **YES** | Reject shared fungus trait |
| `#hoglin_food` | **YES** | Hoglin food = crimson only |
| Loot / recipe / advancements / biome JSON | **YES** | Drops, stick craft, ride checklists, spawners |
| `#freeze_hurts_extra_types` / `#dismounts_underwater` | **YES** | Named vanilla tag consumers |
| Live `biocraft-alien` `strider` / `Strider` string | **ABSENT** (grep zero under `src`) | Consumer search |
| Live `hosts.json` `"strider"` | **ABSENT** | Registry participation |
| DefaultAttributes STRIDER bind | **YES** | Attribute wiring |
| Wiki-only claims (golden dandelion food, shears unequip, `can_equip_saddle` tag) | **Not in 1.21.1 Strider owners** | Excluded / **UNKNOWN** as JE 1.21.1 fact |
| Client `StriderModel` beyond renderer hooks | Present but not required for classification | Presentation detail only |

---

## Dedicated probe 1 — Thermal warm/cold

### Ownership chain (re-verified)

1. **Synched data:** `DATA_SUFFOCATING` (`EntityDataSerializers.BOOLEAN`) defined `Strider.java` **82**, registered in `defineSynchedData` **122** (default `false`). Accessors: `setSuffocating` **173–183**, `isSuffocating` **185–187**.
2. **Tick recalculation (server AI path):** `tick` **309–328** when `!isNoAi()`:
   - `flag` (warm environment) = feet block **or** legacy on-block is `BlockTags.STRIDER_WARM_BLOCKS` **or** `getFluidHeight(FluidTags.LAVA) > 0`.
   - `flag1` (forced cold) = vehicle is a `Strider` that `isSuffocating()`.
   - `setSuffocating(!flag || flag1)`.
3. **Warm block tag:** `data/minecraft/tags/block/strider_warm_blocks.json` values = **only** `minecraft:lava`. Bind `BlockTags.STRIDER_WARM_BLOCKS` (`BlockTags.java` **107**).
4. **Speed side effect:** `setSuffocating(true)` adds **transient** attribute modifier `SUFFOCATING_MODIFIER` id `minecraft:suffocating`, −0.34 `ADD_MULTIPLIED_BASE` (**75–78**, **177–181**); false removes it. Ridden speed (`getRiddenSpeed` **272–273**) multiplies movement by **0.35** if suffocating else **0.55**, times boost factor.
5. **AI relationship:** `StriderGoToLavaGoal` (**499–533**) seeks `Blocks.LAVA` when not in lava — environmental pathing, separate from `DATA_SUFFOCATING` write. Panic/tempt/breed goals do not write suffocation.
6. **Damage:** Suffocation state does **not** apply HP damage in `Strider.tick`. Water/rain damage is separate (`isSensitiveToWater` **381–383** → `LivingEntity` **2850–2851**). Freeze-extra is tag-driven (`LivingEntity` **1178–1179**), not warm-state.
7. **Rendering:** `StriderRenderer.getTextureLocation` **32–33** cold texture when `isSuffocating()`; `isShaking` **46–48** also when suffocating. Saddle layer is equipment presentation, not thermal.
8. **Breeding/food:** No branch on `isSuffocating` in `isFood` / `mobInteract` / `getBreedOffspring`.
9. **Passenger/steering:** Control requires saddle + holding warped fungus on a stick (`getControllingPassenger` **209–212**). Suffocation only changes ridden speed multiplier, not control eligibility.
10. **Outside lava:** Without `#strider_warm_blocks` / lava fluid height (and not forced by a cold parent vehicle), `setSuffocating(true)` every tick → cold texture, shake, slower movement / ride. Entity can still exist (egg/summon/Overworld lava-ride advancement).

### Persistence vs environment vs intrinsic

| Layer | What it is | Evidence |
|-------|------------|----------|
| Environmental condition | Standing on / in warm blocks or lava fluid height | Tag + fluid height checks in `tick` |
| Transient gameplay / synced entity state | `DATA_SUFFOCATING` + transient attribute modifier | Synched boolean; modifier `addOrUpdateTransientModifier` / `removeModifier` |
| Persistent entity state (NBT) | **Not** for warm/cold | `addAdditionalSaveData` / `readAdditionalSaveData` **127–139** save **only** `steering` (saddle). **No** `"Suffocating"` (or equivalent) NBT key. Reload → state re-derived next tick |
| Intrinsic organism property | **No** | Recomputed from world + optional vehicle; not a breed-inherited or type-constant biology field |

### Do **not** collapse these three

| Mechanism | Owner | Class |
|-----------|-------|-------|
| `fireImmune` | `EntityType` builder flag + `Entity.lavaHurt` / fire invuln | Identity / type flag — **not** warm-state |
| Lava walking / path / float | `canStandOnFluid(LAVA)`, path malus, `floatStrider`, `StriderPathNavigation`, `StriderGoToLavaGoal` | Environmental interaction / navigation |
| Warm vs cold (`DATA_SUFFOCATING`) | Tick + tag + fluid height → synched state → speed/render | Transient synced state driven by environment |

Minecraft **does** expose a distinct physiological-*looking* cold/suffocating state (cold skin + shake + speed). That is still **vanilla entity state**, not a BP fact.

### BioCraft consumer test for thermal distinction

Live tree grep `strider` / `Strider` / warm / `SUFFOCAT` under `biocraft-alien/src`: **zero** matches. Generic Analyzer / resolver / gestation do not read warm/cold. **No named live consumer needs the warm/cold distinction.** → classification **transient gameplay state** / **environmental interaction** → **A**.

---

## Dedicated probe 2 — Reproduction

| Step | Owner | 1.21.1 evidence |
|------|-------|-----------------|
| Breeding item / food | `Strider.isFood` + `#strider_food` | `isFood` **413–415**: `stack.is(ItemTags.STRIDER_FOOD)`. JSON: **only** `minecraft:warped_fungus`. Bind `ItemTags.STRIDER_FOOD` (**79**) |
| Tempt (superset, not food) | `TemptGoal` + `#strider_tempt_items` | Goal **163–164**. JSON: `#minecraft:strider_food` **and** `minecraft:warped_fungus_on_a_stick`. Stick tempts; stick is **not** in food tag |
| Love / adult feed | `Animal.mobInteract` via `super` | `Strider.mobInteract` **435** → `Animal` **136–157**: adult age 0 + `canFallInLove` → `setInLove`; baby → `ageUp` |
| Mate eligibility | `Animal.canMate` | **206–211**: same class, both in love |
| Offspring creation | `Strider.getBreedOffspring` | **405–407**: `EntityType.STRIDER.create(level)` — fresh STRIDER; **no** variant/copy of parent warm/saddle |
| Age transition | `AgeableMob` | Breeding sets baby (`Animal.spawnChildFromBreeding` path); spawn group baby via `AgeableMobGroupData(0.5F)` non-jockey path **485**; baby age −24000 jockey passenger **481**. Baby **not** saddleable (**147–149**) |
| Variant / state inheritance | **None found** | No Strider variant data; warm-state not NBT; offspring not copied from parents' suffocation |
| BioCraft consumers | **None Strider-named** | Zero `strider` in live `src`. Diet/breed not projected into BP |

**Classification:** food/tempt = item-tag environmental interaction; breeding = AgeableMob/Animal gameplay; offspring = identity `strider`. **Not** actual biological input consumed by BioCraft. → **A** (identity of child still **B** via `organismKey`).

### Warped fungus vs Hoglin (distinct consumers — reject shared fungus trait)

| Role | Tag / item | Consumer | Overlap? |
|------|------------|----------|----------|
| Strider **food** | `#strider_food` item = warped fungus | `Strider.isFood` | — |
| Strider **tempt** | `#strider_tempt_items` = food + stick | `TemptGoal` | — |
| Strider **steer** | `WARPED_FUNGUS_ON_A_STICK` (`FoodOnAStickItem` × `EntityType.STRIDER`, damage 1) | `getControllingPassenger` + `FoodOnAStickItem.use` **33–37**; recipe fishing rod + warped fungus | — |
| Hoglin **food** | `#hoglin_food` = **crimson** fungus only | Hoglin (not Strider) | **No** shared food item |
| Hoglin **repellent** | `#hoglin_repellents` **block** tag includes warped fungus / potted / portal / respawn anchor | `HoglinSpecificSensor.findNearestRepellent` **61–62** | Same **name** `warped_fungus`, **block** tag, **flee** — opposite of Strider attract. **Not** a shared fungus trait |

---

## Behavior ownership table

Classification column **before** A/B/C.

| Behavior | Actual owner | Manifestation class | Biological input? | Existing BP? | Named live BioCraft consumer? | A/B/C |
|----------|--------------|---------------------|-------------------|--------------|-------------------------------|-------|
| Identity / size / CREATURE / `.fireImmune()` | `EntityType.STRIDER` **659–661** | identity (+ type flag) | Identity only; flag ≠ origin | `organismKey=strider` (fail-soft) | Generic resolver / Analyzer if key named; **no** Strider branch | **B** |
| Java type mix (`Animal`+`ItemSteerable`+`Saddleable` in `monster`) | Class **74** | identity / implementation | Shared interfaces ≠ clade | Distinct key | None for ancestry | **A** |
| `fireImmune` runtime (no lava/fire HP) | `Entity` lavaHurt **530–536** + invuln **2684**; Strider `isOnFire()` always false **386–388** | identity / presentation override | No | Identity | None | **A** |
| Warm/cold `DATA_SUFFOCATING` | `tick` + tag + fluid; synched; **not** NBT | transient gameplay state ← environmental | No | Identity sufficient | **None** (searched) | **A** |
| `#strider_warm_blocks` = lava | Block tag JSON | environmental interaction | No | — | Vanilla Strider only | **A** |
| Lava stand / path / GoToLava / float | `canStandOnFluid`, malus, nav, goal, `floatStrider` | environmental interaction | No | Identity | None | **A** |
| Food / breeding / offspring | `#strider_food` + `Animal` + `getBreedOffspring` | environmental + entity transformation (baby) | No diet BP | Child identity | None | **A** / child **B** |
| Tempt | `#strider_tempt_items` | transient AI / item interaction | No | Identity | None | **A** |
| Warped fungus on a stick steer | `FoodOnAStickItem(STRIDER)` + holding check | item interaction + transient boost | No | Identity | None | **A** |
| Saddle / `ItemBasedSteering` NBT `"Saddle"` | `Saddleable` + steering save **54–59** | persistent entity state (equipment) | Equipment ≠ capability | Identity | None | **A** |
| Zombified piglin jockey | `finalizeSpawn` **466–489** | entity spawn kit (rider) | Rider ≠ genetics | Distinct keys | None | **A** |
| Baby rider / group baby chance | `finalizeSpawn` + `AgeableMob` | transient/persistent age state | No | Entity baby flag | None | **A** |
| Lava-column spawn rules | `SpawnPlacements` **145** + `IN_LAVA` **21–23** + `checkStriderSpawnRules` **97–107** | environmental / encounter | Spawn ≠ origin | Not origin field | None | **A** |
| Nether biome spawners | All five biome JSONs weight 60 min1 max2 | environmental / encounter | Spawn biome ≠ origin | Not origin | None | **A** |
| Water/rain damage | `isSensitiveToWater` | environmental damage hook | No | Identity | None | **A** |
| Freeze ×5 | `#freeze_hurts_extra_types` | environmental / tag | Tag ≠ clade | Identity | Vanilla `LivingEntity` | **A** |
| Dismount underwater | `#dismounts_underwater` | vehicle tag | Shared with Horse ≠ clade | Identity | `Entity.dismountsUnderwater` **2335–2336** | **A** |
| Loot string 2–5 | `entities/strider.json` | item/block production (drops) | Drops ≠ anatomy | Not needed | None | **A** |
| Advancements ride / Overworld lava ride | nether advancement JSON | UX checklist | Not origin | Identity | None | **A** |
| Host Registry participation | **ABSENT** `"strider"` | (registry gap) | Participation missing ≠ biology field | Fail-soft key; HostType empty | Eligibility false via null HostType; **not** a missing BP fact consumer | **B** |

**No row is C.**

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` key `strider` | **UNREGISTERED** | Absent all groups (**1–53**) | Do **not** register here. Absence ≠ consumer absence (searched separately) |
| Live `biocraft-alien` `strider`/`Strider` | **ABSENT** | Grep zero under `src` (main+test) | No Strider-specific production code |
| `BiologicalProfileResolver` | **LIVE** generic | **35–56**: lowercased key; `MobHostRegistry.getHostType`; unknown keys fail-soft | `strider` representable as identity without registration |
| `CompiledBiologicalProfile` | **LIVE** composition | Fields organismKey, HostType, xenomorphFormKey, hostEffectProfileId, behaviorTypeKey, contributingSourceKey | Sparse; no warm/diet field |
| Analyzer `BiologicalProfileDnaAnalysisPort` | **LIVE** generic | **39–41** resolve + `fromCompiled` | Would project fail-soft `strider` if sampled; **no** thermal/diet projection |
| `DnaSampleFromOccupant` | **LIVE** generic | organismKey from form or encode-id (**51–59**) | Captured Strider would sample as `strider`; not a contributing-source carrier |
| Gestation `writeContributingSource` | **LIVE** xenomorph-side | `GestationManager` **164–175**; requires eligible host | Strider suitability **false** (null HostType) → cannot originate live contribution today. Block is registry gate, not missing Strider BP field |
| `HostEligibilityService` | **LIVE** registry gate | **19–21**, **33–44** | Unregistered → ineligible path |
| Strider entity JSON / AI config | **ABSENT** | No production Strider config | Vanilla owns gameplay |
| JUnit named `strider` | **ABSENT** | Generic unknown-key test only (`BiologicalProfileResolverTest` **47–55**) | Fail-soft proven for unknown keys |
| Inventory / dna.md mentions | **PLANNING** | Docs only | Not live consumers |

Consumer classification:

| Candidate | Classification |
|-----------|----------------|
| Resolver / Compiled BP / Analyzer / DnaSample | **LIVE** generic — not Strider-specific; no missing-fact demand |
| Gestation contributing source | **LIVE** xenomorph machinery; Strider **origin blocked** by null HostType |
| `HostEligibilityService` | **LIVE** gate; false via absence |
| `hosts.json` strider row | **DEAD / ABSENT** |
| Strider production JSON / tests | **ABSENT** |
| Inventory row | **PLANNING** |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails on 1.21.1 evidence |
|----------------|--------------------------------|
| Nether spawn ⇒ organism-native Nether origin | Encounter: `IN_LAVA` + lava-air column + five biome JSONs. Egg/summon/breeding/Overworld lava-ride advancement also exist. Spawn biome ≠ origin |
| Collapse `fireImmune` + lava walk + warm-state into one trait | Three owners: EntityType flag; fluid/path; synched `DATA_SUFFOCATING` from tag/fluid. Do not mint one “lava physiology” field |
| Warm/cold is persistent biology / BP | Synched + transient modifier; **not** in NBT; re-derived each tick |
| Shared fungus trait with Hoglin | Strider item food/tempt/stick vs Hoglin **block** `#hoglin_repellents` flee; Hoglin food is crimson. Attract ≠ flee |
| Rideable clade via `ItemSteerable`/`Saddleable` with Horse/Pig | Horse = `AbstractHorse` + jump interfaces; Pig = separate `FoodOnAStickItem(PIG)`. Helpers ≠ clade |
| Strider → Ghast flight / Nether column anatomy | No Strider flight owner; spawn column ≠ anatomy. Ghast out of scope |
| Host Registry absence ⇒ no BioCraft consumers / proves ineligibility-as-biology | Absence ≠ consumer absence. Live search found **generic** plumbing only; suitability false is registry participation, not a missing BP field (**B**, not **C**) |
| Interesting cold texture ⇒ Profile field | Interesting ≠ named consumer. Consumer test failed |
| Wiki golden dandelion / shears unequip / `can_equip_saddle` | Not in 1.21.1 `Strider.isFood` / `mobInteract` / `EntityTypeTags` extract — exclude |

---

## Potential biological relationships

### 1. Warm/cold physiological-looking state

- **Owner:** environment → `DATA_SUFFOCATING` → speed/render.
- **Class:** transient synced state / environmental — **not** persistent, **not** intrinsic.
- **Biological input for BioCraft?** No named consumer.
- **Result:** **A**. Do not collapse with `fireImmune` / lava-walk.

### 2. Warped fungus food/tempt/stick vs Hoglin repellent

- **Owner:** four distinct vanilla consumers (food, tempt, stick, Hoglin block flee).
- **Result:** **A**. Shared fungus trait **rejected**.

### 3. Saddle / stick vs Horse / Pig

- **Owner:** Strider `Saddleable` + `ItemBasedSteering` + `FoodOnAStickItem(STRIDER)`.
- **Result:** **A**. No rideable clade.

### 4. Zombified piglin jockey

- **Owner:** `finalizeSpawn` creates rider + saddle + stick kit.
- **Result:** **A**. Not inheritance/conversion.

### 5. Nether biome / lava-column encounter

- **Owner:** biome JSON + `IN_LAVA` + air-above-lava rules.
- **Result:** **A**. Spawn ≠ origin.

### 6. Strider as BioCraft host / contributing source

- **Owner:** Host Registry + eligibility + gestation write path.
- **Participation:** missing (unregistered).
- **Composition:** fail-soft `organismKey=strider` already (**B**).
- **Named consumer of a missing Strider biological fact?** No — gate is null HostType.
- **Result:** **B**; do not register; do not invent contribution field. **C not earned.**

---

## Final evidence conclusion — YES/NO gates

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** (`organismKey` fail-soft; optional xenomorph `contributingSourceKey` already exists and is not a Strider field) |
| Named consumer of a **missing** Strider biological fact | **NO** (generic identity plumbing ≠ Strider-specific missing-fact consumer; thermal distinction unused) |
| Architectural escalation / DESIGN-BIO-MANIFEST-004 | **NO** |
| Register `strider` from this packet | **NO** |

**Stop.** Prefer disprove C: **C = 0**.

### A/B/C counts

- **A:** ~18 behavior rows — `fireImmune` runtime; warm/cold + `#strider_warm_blocks`; lava stand/path/GoToLava; food/breed mechanics; tempt; stick steer; saddle equipment; jockeys; spawn rules; biome tables; water sensitivity; freeze-extra; dismounts-underwater; loot; advancements; class-mix/ancestry rejection; fungus-split / rideable-clade rejections.
- **B:** 2 — registry identity `organismKey=strider` (fail-soft unregistered); Host Registry participation gap / eligibility false without minting a new BP field (optional Model A `contributingSourceKey` already exists on xenomorphs).
- **C:** **0**.

### Thermal-state ownership/persistence (summary)

Environmental warm check (`#strider_warm_blocks` / lava fluid / cold parent vehicle) drives **transient synched** `DATA_SUFFOCATING` + transient speed modifier + client cold/shake. **Not** NBT-persistent. **Not** intrinsic. **Distinct** from `fireImmune` and lava-walking. Live BioCraft does **not** consume the distinction.

### Reproduction (summary)

Food = warped fungus item tag only; tempt adds stick; offspring = new `STRIDER` with no warm/variant inheritance; age via AgeableMob. No BioCraft diet/breed consumer.

### Live consumer search despite Host Registry absence

`hosts.json` has no `strider`. Independent live-tree search: **zero** `strider`/`Strider` under `biocraft-alien/src`. Generic resolver/Analyzer/gestation/eligibility exist but need **no** missing Strider biological fact. Host Registry absence does **not** prove consumer absence; search still found no Strider-specific consumer and **no C**.

### UNKNOWNs

- Wiki-era shears unequip / golden dandelion / `can_equip_saddle` / `followable_friendly_mobs`: **not** evidenced in 1.21.1 extracted Strider/EntityTypeTags owners → treated as **non-1.21.1 / UNKNOWN** for this packet (excluded, not inferred).
- Exact default max-health numeric if not overridden: Strider does not set `MAX_HEALTH` in `createAttributes`; full LivingEntity default chain not re-expanded here beyond movement/follow (**UNKNOWN** as a Strider-specific override — none found).

### Path

`.tmp_manifestation_evidence/strider.md`
