TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Sheep docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/sheep.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Sheep — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register or unregister Sheep as a conclusion of this investigation.** Sheep is already in `vanilla_hosts.living_biological`. Registration is participation, not extra biology.

Method (every behavior): existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Mechanic classes used **before** A/B/C: identity | persistent entity state | transient gameplay state | environmental interaction | item/block production | effect application | entity/state transformation | actual biological input consumed by BioCraft.

Closed leaps applied independently: `Animal` parent ≠ clade; wool/shear ≠ Mooshroom ancestry reopen; Host Registry ≠ eligibility science ≠ manifestation; variant/state ≠ BP merely because persistent/heritable; item production ≠ stored biological composition; name/easter egg ≠ genetics. Identity-route `organismKey` / `contributingSourceKey` is **B for that consumer only** — do **not** infer wool Color is represented because the identity route exists. **C** only if a named live consumer needs a missing biological distinction. Do not invent consumers. Do **not** pre-decide wool color is non-biological.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey` (Model A Chestburster/Drone), optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

This organism is investigated independently. Do **not** absorb Mooshroom, Goat, Cow, or Wolf as Sheep biology. Working hypothesis only — prefer disprove **C**.

Default: **NO** new BP field. Live `contributingSourceKey=sheep` is **B** (identity), not **C**. Wool Color is probed as persistent/heritable vanilla state; absence of a BioCraft Color reader is recorded as evidence, not as a claim that Color “isn’t biology.”

---

## Subject

Sheep (`minecraft:sheep`, living Sheep) — identity, `#sheep_food` wheat tempt/breed, same-type lamb, persistent wool **Color** + **Sheared** packed in `DATA_WOOL_ID`, dye mutation of that Color, shear → colored wool items, grass-eat regrowth, color-keyed death loot, `jeb_` fur-layer easter egg, Evoker wololo (blue→red), Host Registry LIVE `living_biological` + `HostType.LIVING_BIOLOGICAL` + `baseline_biological`, and BioCraft gestation `contributingSourceKey` identity routing.

Out of scope as organisms: Mooshroom, Cow, Goat, Wolf. Cited only as **adjacency / negative controls** (shared `IShearable` / farm column ≠ ancestry).

---

## Version

Minecraft Java **1.21.1** only. Mapped NeoForge **21.1.208** sources under `.tmp_mc_sources/` are authoritative. Wiki = orientation/disagreement only; **source wins**. Missing required source → **UNKNOWN** (no wiki/superclass/sibling inference).

Temporary source cache (not SSOT): `.tmp_mc_sources/`.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:sheep` |
| `EntityType` | `EntityType.SHEEP` — `EntityType.java` **585–588**: `register("sheep", Builder.of(Sheep::new, MobCategory.CREATURE).sized(0.9F, 1.3F).eyeHeight(1.235F).passengerAttachments(1.2375F).clientTrackingRange(10))` |
| Fire / lava | **No** `.fireImmune()` on SHEEP. Builder default false |
| Class | `Sheep extends Animal implements Shearable` (`Sheep.java` **64**). Vanilla `Shearable` **extends** Neo `IShearable` (`Shearable.java` **8**) |
| Category | `MobCategory.CREATURE` |
| Summonable | Builder does **not** call `noSummon()` |
| Attributes | `DefaultAttributes` binds `EntityType.SHEEP` → `Sheep.createAttributes()` (`DefaultAttributes.java` **144**). `Sheep.createAttributes` (`Sheep.java` **151–153**): `MAX_HEALTH` **8.0**, `MOVEMENT_SPEED` **0.23F** |
| Dimensions | Adult hitbox **0.9 × 1.3**, eyeHeight **1.235**, passengerAttachments **1.2375F**. **No** Sheep `getDefaultDimensions` override. Baby scale via `LivingEntity.getDefaultDimensions` → `getType().getDimensions().scale(getAgeScale())` with `getAgeScale()` **0.5F** if baby (`LivingEntity.java` **548–549**, **3427–3428**) |
| Host Registry | **REGISTERED.** `hosts.json` `vanilla_hosts.living_biological.mobs` includes `"sheep"` (**6**). `default_dna`: `baseline_biological` (**4**). `variant_mappings` has **no** sheep entry (**47–52**) |
| Suitability | Registered living_biological → currently suitable for xenomorph hosting via `HostEligibilityService` → `MobHostRegistry.isSuitableForXenomorph` because `HostType.LIVING_BIOLOGICAL.isSuitableForXenomorph() == true` (`HostType.java` **17**, **44–45**). Registered ≠ extra biology ≠ BP field |
| Spawn egg | `Items.SHEEP_SPAWN_EGG` (`Items.java` **1471**): colors **15198183**, **16758197** |
| Spawn placement | `SpawnPlacements.java` **135**: `ON_GROUND`, `MOTION_BLOCKING_NO_LEAVES`, `Animal::checkAnimalSpawnRules` |

Independent existence paths (not origin): spawn egg, `/summon` (`canSummon` default true), CREATURE biome spawn (Minecraft-owned; spawn biome ≠ origin), breeding `Sheep.getBreedOffspring` → `EntityType.SHEEP.create`.

```text
Sheep does X
    → Minecraft entity / Animal / item / Evoker / renderer owns X?
    → Sheep biological composition contributes something to X?
    → a live AlienCraft consumer needs that distinction beyond organismKey / contributingSourceKey?
```

---

## Source-completeness table

Probes began only after `Sheep.java` and directly referenced helper/goal/state/factory classes were present under `.tmp_mc_sources/`. Missing color loot tables were extracted this pass from `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar`. `ShearsItem` extracted from `neoforge-21.1.208-sources.jar`.

| Source path | Status | Role in this packet |
|-------------|--------|---------------------|
| `.tmp_mc_sources/.../animal/Sheep.java` | **PRESENT** | Goals, Color/Sheared packing, shear, NBT, offspring, ate(), finalizeSpawn |
| `.tmp_mc_sources/.../animal/Animal.java` | **PRESENT** | Love/food interact, `canMate` same class, `spawnChildFromBreeding` |
| `.tmp_mc_sources/.../AgeableMob.java` | **PRESENT** | `setBaby` → age **−24000**; `ageUp` |
| `.tmp_mc_sources/.../EatBlockGoal.java` | **PRESENT** | Grass / short-grass eat → `mob.ate()` |
| `.tmp_mc_sources/.../BreedGoal.java` | **PRESENT** | Same-class love partner |
| `.tmp_mc_sources/.../TemptGoal.java` | **PRESENT** | `#sheep_food` predicate |
| Float / Panic / FollowParent / WaterAvoidingRandomStroll / LookAtPlayer / RandomLookAround | **PRESENT** | Generic goals; no Sheep-specific subclasses |
| `.tmp_mc_sources/.../Shearable.java` + `IShearable.java` | **PRESENT** | Shear contract; Neo default `onSheared` captures `Shearable.shear` drops |
| `.tmp_mc_sources/.../item/ShearsItem.java` | **PRESENT** (extracted this pass) | `interactLivingEntity` → `IShearable` |
| `.tmp_mc_sources/.../item/DyeItem.java` | **PRESENT** | Living-entity dye → `sheep.setColor` |
| `.tmp_mc_sources/.../item/DyeColor.java` | **PRESENT** | 16 ids 0–15; `byId` |
| `.tmp_mc_sources/.../EntityType.java` | **PRESENT** | `SHEEP` **585–588** |
| `.tmp_mc_sources/.../DefaultAttributes.java` | **PRESENT** | Sheep bind **144** |
| `.tmp_mc_sources/.../BuiltInLootTables.java` | **PRESENT** | `SHEEP_WHITE`…`SHEEP_BLACK` **80–95** |
| `.tmp_mc_sources/data/minecraft/loot_table/entities/sheep.json` | **PRESENT** | Mutton + smelt-on-fire + looting |
| `.tmp_mc_sources/data/minecraft/loot_table/entities/sheep/{16 colors}.json` | **PRESENT** (14 extracted this pass; white/black already cached) | 1× `{color}_wool` + nested `entities/sheep` |
| `.tmp_mc_sources/data/minecraft/tags/item/sheep_food.json` | **PRESENT** | `minecraft:wheat` only |
| `.tmp_mc_sources/.../ItemTags.java` | **PRESENT** | `SHEEP_FOOD` **62** |
| `.tmp_mc_sources/.../VanillaItemTagsProvider.java` | **PRESENT** | `#sheep_food` ← `Items.WHEAT` **455** |
| `.tmp_mc_sources/.../SpawnPlacements.java` | **PRESENT** | Sheep **135** |
| `.tmp_mc_sources/.../layers/SheepFurLayer.java` | **PRESENT** | `jeb_` rainbow lerp; else `Sheep.getColor(livingEntity.getColor())` |
| `.tmp_mc_sources/.../SheepRenderer.java` | **PRESENT** | Body texture; adds `SheepFurLayer` |
| `.tmp_mc_sources/.../monster/Evoker.java` | **PRESENT** | Wololo reads/writes Sheep Color |
| `.tmp_mc_sources/data/minecraft/recipe/gray_dye.json`, `purple_dye.json`, `lime_dye.json`, `cyan_dye.json`, `magenta_dye_from_purple_and_pink.json` | **PRESENT** | Two-dye shapeless mixes used by `getOffspringColor` recipe lookup |
| AlienCraft `hosts.json` | **PRESENT** | `"sheep"` living_biological |
| AlienCraft `GestationManager.java` | **PRESENT** | `writeContributingSource` **164–175** |
| AlienCraft `BiologicalProfileResolver.java` | **PRESENT** | Sparse profile; no sheep/Color branch |
| AlienCraft `HostEligibilityService.java` | **PRESENT** | Generic encodeId → registryPath |
| AlienCraft `CapturedEntitySnapshot.java` | **PRESENT** | Opaque NBT snapshot; does not strip `Color`/`Sheared` |
| Sheep-named xenomorph entity JSON | **ABSENT** under `biocraft-alien/src/main/resources` (search this pass) | No Sheep production catalog |
| `jeb_` outside `SheepFurLayer.java` | **ABSENT** in `.tmp_mc_sources` grep | Rendering-only in this version’s mapped sources |

---

## Sheep wool phenotype probe (mandatory)

### Ownership of Color

Packed in synched `DATA_WOOL_ID` (`EntityDataSerializers.BYTE`, default `(byte)0`) (`Sheep.java` **66**, **156–158**).

| Bits | Meaning | Accessors |
|------|---------|-----------|
| Low 4 (`& 15`) | `DyeColor` id 0–15 | `getColor()` / `setColor()` (**298–307**) |
| Bit 4 (`& 16`) | Sheared | `isSheared()` / `setSheared()` (**310–323**) |

NBT: `"Color"` byte = `getColor().getId()`; `"Sheared"` boolean (`addAdditionalSaveData` / `readAdditionalSaveData` **262–275**). Color is **persistent entity state**, not a render-only tint.

`setColor` preserves the sheared nibble (`b0 & 240 | dyeColor.getId() & 15`). `setSheared` preserves the color nibble.

### Persistent?

**Yes.** Synched entity data + NBT. Survives save/load. Capture Net `entity.saveWithoutId` keeps `Color`/`Sheared` because `EntitySnapshotWorldIdentity.STRIP_KEYS` does **not** list them (`EntitySnapshotWorldIdentity.java` **13–25**; `CapturedEntitySnapshot.write` **55–57**). That is opaque specimen NBT, **not** a BioCraft Color reader.

### Initial assignment / randomization

`finalizeSpawn` always `setColor(getRandomSheepColor(level.getRandom()))` then `super.finalizeSpawn` (`Sheep.java` **362–364**).

`getRandomSheepColor` (`326–338`): `nextInt(100)` → **BLACK** if `<5`; **GRAY** if `<10`; **LIGHT_GRAY** if `<15`; **BROWN** if `<18`; else `nextInt(500)==0` → **PINK** else **WHITE**. Default packed `0` is WHITE until this runs.

Breeding does **not** use this table (see offspring).

### Breeding inheritance / offspring color

`getBreedOffspring` (`342–348`): `EntityType.SHEEP.create(level)` then `sheep.setColor(this.getOffspringColor(this, (Sheep)otherParent))`. Offspring **EntityType** is `SHEEP`. Color is copied/mixed **before** add; `Animal.spawnChildFromBreeding` then `setBaby(true)` (`Animal.java` **214–231**).

`getOffspringColor` (`370–382`): builds a 2×1 `CraftingInput` of the two parents’ `DyeItem.byColor` stacks (`makeCraftInput` **385–387**); asks `RecipeType.CRAFTING`; if the result item is a `DyeItem`, uses that `DyeColor`; else `random.nextBoolean() ? fatherColor : motherColor`.

This is **Minecraft crafting-recipe mixing of dye items**, not a BioCraft genome. Two-dye shapeless recipes exist (examples extracted): gray = black+white; purple = blue+red; lime = green+white; cyan = blue+green; magenta = purple+pink (`magenta_dye_from_purple_and_pink.json`). Same-color parents with no matching mix recipe fall through to random parent. **Persistent Color is heritable in vanilla.** Heritable ≠ BP field by itself (closed leap).

BioCraft consumption of inherited Color: **none found**.

### Dye changes the same persistent state?

**Yes.** `DyeItem.interactLivingEntity` (`DyeItem.java` **30–38**): target `instanceof Sheep`, alive, **not sheared**, `getColor() != this.dyeColor` → server `sheep.setColor(this.dyeColor)` and shrink dye. Same `setColor` as spawn/breed/NBT/Evoker. Sheep `mobInteract` does **not** handle dye; it falls through to `Animal.mobInteract` (food/love) after a **disabled** shears branch (`if (false && itemstack.is(Items.SHEARS))` — Neo comment: shear via `IShearable`) (`Sheep.java` **219–232**).

### Shearing relationship to color

Shear does **not** clear Color. `shear` (`236–254`): `setSheared(true)` then spawn `1 + random.nextInt(3)` items from `ITEM_BY_DYE.get(this.getColor())` (wool **blocks** keyed by current Color, **67–84**). Color nibble remains. `readyForShearing`: alive && !sheared && **!isBaby()** (**257–258**).

Owner path: `ShearsItem.interactLivingEntity` → `IShearable.isShearable` / `onSheared` (`ShearsItem.java` **65–88**). Default `IShearable.onSheared` captures drops from vanilla `Shearable.shear` (`IShearable.java` **66–74**). `IShearable.spawnShearedDrop` default branch comments “rules invented by Sheep#shear” and has a **separate** `MushroomCow` branch (**93–110**). Shared shear interface + drop physics ≠ Mooshroom ancestry (closed leap).

### Regrowth

`EatBlockGoal` eats `SHORT_GRASS` at feet or `GRASS_BLOCK` below → `mob.ate()` (`EatBlockGoal.java` **68–87**). `Sheep.ate` (`352–357`): `super.ate()` (`Mob.ate` = `GameEvent.EAT`, `Mob.java` **261–263**) then **`setSheared(false)`**; if baby, `ageUp(60)`. Color unchanged. Regrowth restores wool **presence**, not a new Color roll.

### Does Color affect anything beyond rendering / item production?

**Yes, in Minecraft:** `Evoker.EvokerWololoSpellGoal` targeting selector requires `((Sheep)…).getColor() == DyeColor.BLUE` (`Evoker.java` **302–304**); `performSpellCasting` `sheep.setColor(DyeColor.RED)` (**340–344**). Same persistent Color field. Owner = Evoker spell, not Sheep biology dossier.

Rendering: `SheepFurLayer` skips fur when `isSheared()`; otherwise tints with `Sheep.getColor(livingEntity.getColor())` **unless** `jeb_` (below) (`SheepFurLayer.java` **43–68**). Body texture is uncolored `sheep.png` (`SheepRenderer.java` **13–24**).

Item production: shear wool blocks; unsheared death loot table selected by `getDefaultLootTable` switch on `getColor()` (`Sheep.java` **162–184**) → `entities/sheep/{color}.json` = 1× `{color}_wool` + nested mutton table. Sheared death uses `getType().getDefaultLootTable()` = `entities/sheep.json` (mutton only, **no wool**).

### Live BioCraft consumer of Color?

Production Java/JSON search for `sheep` under `biocraft-alien/src/main` hits **`hosts.json` only** (plus this packet’s identity path). No `DyeColor`, `getColor`, wool, or `jeb_` reader. Resolver/Analyzer/gestation use organism-definition keys, not Color.

**Probe conclusion:** Color is persistent, dyeable, heritable, loot/shear-relevant, and Evoker-relevant. It is **not** currently an actual biological input consumed by BioCraft. Identity B does **not** represent Color. **C is not earned** — no named live consumer needs a missing Color distinction. Do not mint a wool-color BP field from interesting vanilla state.

### `jeb_` (easter-egg rendering / item-state mechanism)

Sole mapped-source hit: `SheepFurLayer.java` **56–65**. Gate: `hasCustomName() && "jeb_".equals(getName().getString())`. Then rainbow **lerp** of `Sheep.getColor(DyeColor.byId(i1))` / `byId(j1)` from `tickCount` and `entityId` (period 25 ticks). **Does not call `setColor`.** Custom name is entity name state; rainbow is **transient client render**.

Shear, loot, dye, breed, Evoker all use persistent `getColor()`, not the rainbow. **No** `jeb_` item-drop override found in 1.21.1 mapped sources (record absence; do not import wiki drop claims). Treat as name-triggered **rendering** easter egg sitting on top of unchanged Color — not genetics, and not a hidden Color genotype.

---

## Reproduction / lifecycle (minimum)

| Question | 1.21.1 evidence | BioCraft consumption |
|----------|-----------------|----------------------|
| Can breed? | **Yes.** `BreedGoal` + `Animal` love via `#sheep_food` / `isFood` (`Sheep.java` **119–120**, **132–134**; `Animal.mobInteract` **136–158**). `canMate` requires same Java class (`Animal.java` **206–211**) | **None** |
| Offspring EntityType | `EntityType.SHEEP.create` (`Sheep.java` **343**) | Child identity still `sheep` if later sampled; no breed trait consumer |
| Age | `spawnChildFromBreeding` → `setBaby(true)` → age **−24000** (`AgeableMob.java` **161–162**). Grass `ate()` `ageUp(60)` if baby. Adult feeding uses Animal baby speed-up, not Sheep-specific | AgeableMob flag; not a BP field |
| Inherited / persistent state | **Color** via `getOffspringColor` (recipe mix or random parent). **Sheared** not copied in `getBreedOffspring` (fresh entity default unsheared). Custom name not copied here | Color inheritance **not** read by BioCraft |
| Food tag | `#minecraft:sheep_food` = wheat only (`sheep_food.json`; datagen **455**) | **None.** Tag ≠ diet trait |

Absence of BioCraft breed/Color/age consumers is **evidence**, not a gap to fill.

---

## Behavior ownership table

| Behavior | Manifestation class | Actual owner | 1.21.1 evidence | Biological input? | Existing BP representation? | BioCraft consumer? | A/B/C |
|----------|---------------------|--------------|-----------------|-------------------|----------------------------|--------------------|-------|
| Identity / dimensions / CREATURE | identity | `EntityType.SHEEP` | `EntityType.java` **585–588**: `"sheep"`, `CREATURE`, `0.9F×1.3F`, eyeHeight `1.235F` | Identity only | `organismKey = sheep` | Resolver / Analyzer / host lookup | **B** |
| Goals / panic / stroll | transient gameplay state | `Sheep.registerGoals` | Float, Panic **1.25**, Breed **1.0**, Tempt **1.1** `#sheep_food`, FollowParent **1.1**, EatBlock, WaterAvoidingRandomStroll **1.0**, LookAtPlayer **6.0F**, RandomLookAround (`Sheep.java` **114–125**) | **No.** Entity AI | Identity sufficient | None | **A** |
| Food / tempt | environmental interaction | `Sheep.isFood` + `TemptGoal` | `stack.is(ItemTags.SHEEP_FOOD)` (`Sheep.java` **120**, **132–134**); tag = wheat | **No.** Item tag. Tag ≠ diet trait | Not needed | None | **A** |
| Attributes / sounds | identity (vanilla stats/SFX) | `Sheep.createAttributes` + sound overrides | Health **8**, speed **0.23F** (**151–153**). Ambient/hurt/death/step (**278–295**) | **No** | Not needed | None | **A** |
| Grass eat | environmental interaction | `EatBlockGoal` | Short grass or grass block → `ate()` (`EatBlockGoal.java` **37–87**) | **No.** World block eat | Not needed | None | **A** |
| Eat animation | transient gameplay state | `eatAnimationTick` + entity event **10** | Client countdown (`Sheep.java` **88**, **137–148**, **191–216**). Not NBT | **No** | Not needed | None | **A** |
| **Wool Color** | persistent entity state | `DATA_WOOL_ID` low nibble + NBT `"Color"` | `getColor`/`setColor` (**298–307**, **262–275**). Used by render, dye, shear drops, death loot switch, breed mix, Evoker | Vanilla persistent/heritable state. **Not** consumed by BioCraft | `organismKey` does **not** encode Color | **None** live Color reader | **A** |
| Color init | persistent entity state (assignment) | `finalizeSpawn` + `getRandomSheepColor` | **362–364**, **326–338** | Spawn roll, not origin | Not needed | None | **A** |
| Dye Color | persistent entity state (mutation) | `DyeItem.interactLivingEntity` | Same `setColor`; requires unsheared + different color (`DyeItem.java` **30–38**) | Item interact mutating vanilla Color | Not needed | None | **A** |
| **Sheared** flag | persistent entity state | `DATA_WOOL_ID` bit 4 + NBT `"Sheared"` | **310–323**, **264** | Wool-present flag, not composition | Not needed | None | **A** |
| Shear → wool items | item/block production | `ShearsItem` + `Sheep.shear` | 1–3 wool **blocks** of current Color; `setSheared(true)`; babies ineligible (**236–258**; `ShearsItem.java` **65–88**) | Item production ≠ stored biological composition | Not needed | None | **A** |
| Wool regrowth | persistent entity state + age | `Sheep.ate` | `setSheared(false)`; baby `ageUp(60)` (**352–357**) | Grass-eat restores presence, not Color | Not needed | None | **A** |
| Death loot | item/block production | `getDefaultLootTable` + JSON | Sheared → mutton table; else `entities/sheep/{color}` = 1 wool + mutton (**162–184**; color JSON files) | Loot ≠ BP | Not needed | None | **A** |
| **Breeding / lamb** | identity (vanilla reproduction) | `BreedGoal` + `getBreedOffspring` + `Animal.spawnChildFromBreeding` | Offspring `EntityType.SHEEP` (**342–348**). Same-type vanilla AgeableMob path | Vanilla same-type reproduction. Not xenomorph contribution | Child is still `sheep` | None that needs a breed trait | **A** |
| Offspring Color mix | persistent entity state (inherited) | `getOffspringColor` + crafting recipes | Dye-item recipe or random parent (**370–382**) | Heritable vanilla Color. Closed leap: heritable ≠ BP | Not represented; **no consumer** | None | **A** |
| Baby age / scale | persistent entity state | `AgeableMob` + `LivingEntity.getAgeScale` | `setBaby` **−24000**; scale **0.5F** | Age/pose presentation | Entity baby flag | None | **A** |
| **`jeb_` fur** | transient gameplay state (name-gated render) | `SheepFurLayer` | CustomName `"jeb_"` rainbow lerp (**56–65**). Does not mutate Color | Easter-egg rendering. Name ≠ genetics | Not needed | None | **A** |
| Evoker wololo | entity/state transformation | `EvokerWololoSpellGoal` | Target blue Sheep; set Color red (`Evoker.java` **301–344**) | Evoker spell, not Sheep BP | Not needed | None | **A** |
| Spawn / summon / egg | identity (existence paths) | `EntityType` + items + `SpawnPlacements` | CREATURE; egg **1471**; placement **135**. Spawn biome ≠ origin | **No** | Not an origin field | None | **A** |
| Java parent `Animal` | identity (implementation sharing) | Class inheritance | Shared with many creatures | Shared parent ≠ clade | Distinct key `sheep` | None | **A** |
| `IShearable` / Mooshroom drop helper | item/block production (shared API) | `IShearable.spawnShearedDrop` | Default physics cited as Sheep#shear; **separate** `MushroomCow` branch (`IShearable.java` **86–110**) | Wool/shear ≠ Mooshroom ancestry | Distinct keys | None | **A** |
| Capture Net / snapshot | identity + opaque persistent NBT | `CaptureEligibilityPolicy` + `CapturedEntitySnapshot` | `canCapture` = alive && !player (`CaptureEligibilityPolicy.java` **19–20**). Snapshot saves full entity NBT minus world-identity keys | Carrier does not interpret Color. Playtest fixture ≠ Color consumer | Type id `minecraft:sheep` already identity | Generic LIVE capture; **TEST/PLAYTEST** docs name sheep as first target | **A** |
| **Live host → contributingSourceKey** | actual biological input consumed by BioCraft = **organism-definition key only** | Host Registry + gestation + Analyzer | `hosts.json` `"sheep"`; `GestationManager.writeContributingSource` encodeId → registryPath → `setContributingSourceKey` (**164–175**) | Source **identity** only. Not Color, not wool, not wheat | Existing `organismKey` / optional `contributingSourceKey` | **LIVE** eligibility, gestation copy, Analyzer. Tests assert host refs | **B** |

No row is **C**. Live `contributingSourceKey=sheep` is identity already represented — not C. Wool Color is documented persistent/heritable vanilla state with **no** named BioCraft reader — A, not C.

---

## Configuration audit

Statuses used: **LIVE** / **STUB** / **PARSE-ONLY** / **DEAD** / **PLANNING** / **TEST** / **UNKNOWN**.

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` key `"sheep"` under `vanilla_hosts.living_biological` | **LIVE** | `hosts.json` **6**; group `default_dna: baseline_biological` (**4**) | Registered participation. Can originate production contribution. **Not** a Color/wool/breed field |
| `hosts.json` `variant_mappings` sheep | **ABSENT** | No `"sheep"` under `variant_mappings` (**47–52**) | No aggressive/neutral override |
| `HostEligibilityService` | **LIVE** generic | `isSuitableForXenomorph` / `isValidFacehuggerHost` (**19–45**): encodeId → `HostRegistryPaths.registryPath` (`minecraft:sheep` → `sheep`) → `MobHostRegistry` | Named live gate. Sheep passes because registered `LIVING_BIOLOGICAL`. Not Color science |
| `GestationManager.writeContributingSource` | **LIVE** | `GestationManager.java` **147–175** | **Production writer.** Gestated Sheep host yields `contributingSourceKey="sheep"` on Model A carriers. Identity only. **Not C** |
| `BiologicalProfileResolver` | **LIVE** generic | `resolve` (**35–57**): HostType + dna profile id from registry; no sheep/Color branch. Unknown keys fail soft | Sparse projection. Sheep test expects `LIVING_BIOLOGICAL` + `baseline_biological`, empty form/behavior/source unless supplied |
| Analyzer / `DnaAnalysisReportLines` | **LIVE** generic | Projects `organismKey`, optional `contributingSourceKey`, optional `behaviorTypeKey` (`DnaAnalysisReportLines.java` **32–38**) | Does not project Color/Sheared/jeb_ |
| Capture Net | **LIVE** generic | `CaptureNetCapture` + `CaptureEligibilityAdapter`; snapshot NBT | Sheep is a valid living non-player target. First **playtest** target in docs is **PLANNING/TEST**, not a Color consumer |
| `BiologicalProfileResolverTest.sheepResolvesLivingBiologicalHostReferences` | **TEST** | `BiologicalProfileResolverTest.java` **63–65**, `assertLivingHost("sheep")` **126–133** | Identity/host-type contract. Does not assert Color |
| `AdmissionTransactionTest` `"minecraft:sheep"` | **TEST** | Fixture blueprint + `SpecimenExtents(0.9, 0.9)` (**44**) | **Identity string only.** Extents **0.9×0.9** do **not** match `EntityType.SHEEP` **0.9×1.3** — test fake, not dimension SSOT |
| `ContainmentOccupancyServiceTest` variable `sheep` | **TEST** | `LivingEntityRef` occupancy identity (**87–92**) | Variable name only; occupancy is entity-id based, not species/Color |
| Sheep entity JSON / DNA / behavior_type in BioCraft | **ABSENT** | Not in `mob_catalog.json` `bootstrap_entries` (**3–7**). `deep_mob_configs.passive.mobs` is `cow, pig, chicken` only (**19–21**) — **sheep absent even from that planning matrix** | Vanilla remains behavior owner |
| Inventory / manifestation row | **PLANNING** | `vanilla_organism_inventory.md` sheep row manifestation **pending** | Docs are not live consumers. This packet does not edit inventory |
| S3F / BACKLOG Capture Net “first target: sheep” | **PLANNING** + **TEST/PLAYTEST** | `S3F_PLAYTEST_CHECKLIST.md`; `BACKLOG.md` FEATURE-NET-002 | Playtest fixture. Not a wool-color consumer |

Consumer classification for this organism:

| Candidate | Classification |
|-----------|----------------|
| `BiologicalProfileResolver` / compiled profile | **LIVE** generic (not Sheep-specific; TEST asserts `"sheep"` host refs) |
| Analyzer / DNA-page projection | **LIVE** generic projection of keys |
| Gestation `contributingSourceKey` | **LIVE** xenomorph machinery; Sheep **origin allowed** (registered + suitable) |
| `HostEligibilityService` | **LIVE** registry gate; Sheep eligible via `LIVING_BIOLOGICAL` |
| `hosts.json` sheep row | **LIVE** participation |
| Capture Net | **LIVE** generic `LivingEntity`; sheep is a legal target |
| Capture/lab playtest checklists naming sheep | **PLANNING** / **TEST/PLAYTEST** (identity fixture) |
| Sheep production JSON / xenomorph catalog | **ABSENT** |
| Inventory `sheep` row | **PLANNING** |
| Any Color / Sheared / `jeb_` / wool-item BioCraft reader | **ABSENT** (searched production `src/main`) |
| Mooshroom as Sheep ancestry via shear | **REJECTED** (closed leap; not a consumer) |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails on 1.21.1 evidence |
|----------------|--------------------------------|
| Live `contributingSourceKey=sheep` earns C / a new BP field | Named consumers already take the organism-definition key. Identity B for **that** consumer does not represent Color. **B, not C** |
| Wool Color is heritable + persistent → must be a BP / genetics field | Closed leap: variant/state ≠ BP merely because persistent/heritable. No named live consumer reads Color. **A** |
| Identity route means wool is already represented | Explicitly forbidden. `organismKey=sheep` does not encode Color. Color remains unrepresented **and** unconsumed | 
| Dye / shear / loot wool is stored biological composition | Item/block production and item interact. Production ≠ composition. **A** |
| `jeb_` is a genetic rainbow allele / hidden Color | Fur-layer name gate + tick lerp. Does not `setColor`. Shear/loot/Evoker use persistent Color. Easter-egg rendering. Name ≠ genetics | 
| `jeb_` changes shear/loot items in this version | **No** mapped-source item path found. Recorded **ABSENT**. Do not import wiki |
| Shearing is Mooshroom-related biology | Shared `IShearable`; Mooshroom has its own drop-spawn branch. Wool/shear ≠ Mooshroom ancestry reopen | 
| `Animal` parent / farm animals = clade | Shared parent ≠ clade. Distinct `EntityType.SHEEP` | 
| Host Registry registration = extra eligibility science or a Sheep dossier | Registration enables the existing host path. Suitability is `HostType.LIVING_BIOLOGICAL`. Not a Color field | 
| Evoker blue→red means BioCraft needs Color | Minecraft Evoker spell owner. No BioCraft Evoker/Color consumer | 
| Capture snapshot preserving Color means BioCraft consumes Color | Opaque NBT reconstitution. Strip list omits Color; no code interprets it. **A** |
| Wheat food is a diet trait | `#sheep_food` tag. Tag ≠ diet trait. **A** |
| CREATURE spawn biomes are organism origin | Encounter placement. Egg/summon/breed also exist. Spawn biome ≠ origin. **A** |
| Inventory pending / playtest sheep fixture is a live Color consumer | **PLANNING** / **TEST**. Docs and fixtures are not production Color readers | 
| Interesting wool phenotype earns C | Interesting ≠ consumer. C requires a **named live** consumer of a **missing** fact |

---

## Potential biological relationships

### 1. Sheep as live xenomorph host / Model A contributing source

- **Relationship:** Facehugger/ovomorph may select Sheep; gestation copies host registry path onto Chestburster/Drone; Analyzer displays the key; resolver TEST asserts living-biological host refs for `"sheep"`.
- **Owner:** `hosts.json` + `HostEligibilityService` + `GestationManager.writeContributingSource` + Analyzer projection.
- **Biological input?** Only the organism-definition key `"sheep"`.
- **Existing composition:** `organismKey` on a Sheep sample; optional `contributingSourceKey="sheep"` on Model A offspring. `HostType.LIVING_BIOLOGICAL` + `hostEffectProfileId=baseline_biological` already resolve.
- **Named consumer:** **LIVE** — eligibility, gestation writer, Analyzer. Tests = **TEST** identity/host contract.
- **Result:** **B**. Not C.

### 2. Wool Color (persistent / dyeable / heritable phenotype-like state)

- **Relationship:** Packed Color nibble; spawn roll; dye; breed mix via dye recipes; shear/loot keyed by Color; Evoker wololo mutates it; fur layer tints from it (unless `jeb_`).
- **Owner:** `Sheep` + `DyeItem` + crafting recipes + loot tables + `SheepFurLayer` + `Evoker`.
- **Biological input consumed by BioCraft?** **No** named live reader.
- **Existing composition:** Does **not** include Color. That missingness is **not** C without a consumer.
- **Named consumer:** **None**.
- **Result:** **A**. Do not pre-label “non-biological”; do not mint a field.

### 3. Sheared flag / shear / grass regrowth

- **Relationship:** Bit flag + wool item drops + `ate()` restore; babies cannot shear; dye refused while sheared.
- **Owner:** `Sheep` + `ShearsItem`/`IShearable` + `EatBlockGoal`.
- **Biological input?** Item production + persistent wool-present flag.
- **Named consumer:** None.
- **Result:** **A**.

### 4. Breeding / lamb

- **Relationship:** Love + wheat; offspring Sheep; Color mix; baby age.
- **Owner:** `BreedGoal` + `Sheep.getBreedOffspring` + `Animal`.
- **Biological input?** Vanilla same-type reproduction + vanilla Color inheritance.
- **Existing composition:** Child key remains `sheep`.
- **Named consumer:** None that needs a breed or Color-inheritance trait.
- **Result:** **A**.

### 5. `jeb_` name easter egg

- **Relationship:** CustomName `"jeb_"` drives fur-layer rainbow; persistent Color unchanged.
- **Owner:** `SheepFurLayer`.
- **Biological input?** No. Rendering easter egg.
- **Named consumer:** None.
- **Result:** **A**.

### 6. Capture / lab fixture

- **Relationship:** Docs and tests use sheep as a generic LivingEntity / `minecraft:sheep` string.
- **Owner:** Capture eligibility (alive, not player) + admission/containment generics.
- **Biological input?** Type identity at most; NBT snapshot is opaque.
- **Named consumer:** LIVE generic capture; TEST/PLANNING fixtures. Not Color.
- **Result:** **A** (fixture/generic). Identity of a captured sheep sample still **B** if later resolved as `organismKey=sheep`.

### 7. Sheep ↔ Mooshroom (adjacency only)

- **Relationship:** Both shearable; `IShearable` default drop helper mentions Sheep physics and special-cases Mooshroom.
- **Owner:** Neo shear API + `MushroomCow` (not investigated as organism here).
- **Biological input?** Shared interface ≠ ancestry. Wool/shear ≠ Mooshroom reopen.
- **Named consumer:** None.
- **Result:** **A**. Do not absorb Mooshroom.

**C is not earned for any relationship.**

---

## Wiki orientation disagreements

Wiki not fetched this pass. Orientation only; **1.21.1 mapped source wins**.

| Common orientation | 1.21.1 authority | Conclusion |
|--------------------|------------------|------------|
| Sheep wool colors are “genetics” | Persistent `Color` nibble + dye-recipe offspring mix + dye mutation | Vanilla persistent/heritable **state**. Not BioCraft genetics. **A** unless a live consumer appears |
| `jeb_` sheep drop random/rainbow wool | `jeb_` only in `SheepFurLayer`; `shear`/`getDefaultLootTable` use `getColor()` | Rendering easter egg in this source set. Item-state `jeb_` **ABSENT** |
| Health 8 | `Sheep.createAttributes` `MAX_HEALTH` **8.0** | **Agrees** |
| Wheat breeding | `#sheep_food` = wheat | **Agrees** |
| Pink sheep rare on spawn | `getRandomSheepColor` 1/500 after the 18% non-white-gray-brown-black band | Spawn table **A**; not a BP rarity field |
| Evoker dyes blue sheep red | `EvokerWololoSpellGoal` | **Agrees**; Minecraft other-entity owner |

---

## Final evidence conclusion

Sheep is a 1.21.1 `Animal` creature identity (`minecraft:sheep`, 0.9×1.3, eyeHeight 1.235, not fire-immune). Minecraft owns wheat tempt/breed, same-type lambs, packed Color/Sheared state, dye, shear, grass regrowth, color-keyed loot, `jeb_` fur rendering, and Evoker wololo. Color is persistent and heritable in vanilla and is **not** read by any live BioCraft consumer. Identity B does not stand in for Color.

BioCraft already registers `sheep` as `LIVING_BIOLOGICAL` / `baseline_biological` and can write `contributingSourceKey=sheep` on Model A carriers. That consumer asks only for the existing organism-definition key.

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** (for identity / host / Model A source consumers). Color remains unrepresented and **unconsumed** |
| Named consumer exists | **YES** (live host/gestation/Analyzer identity-source path). **NO** named consumer of a **missing** Sheep biological fact (including Color) |
| Architectural escalation required | **NO** |

**Stop.** A = vanilla ownership (Color/Sheared/dye/shear/loot/breed/`jeb_`/Evoker/goals/food/spawn/capture snapshot); B = existing identity/composition including live Model A source identity; C = **not earned**. Do **not** change Host Registry. Do **not** mint a Sheep/wool/Color/jeb_ Profile. Do **not** absorb Mooshroom. Do **not** treat registration or live `contributingSourceKey=sheep` as C. Do **not** mint `DESIGN-BIO-MANIFEST-004`.

### A/B/C summary

- **A count: 21** — goals, `#sheep_food`/tempt, attributes/sounds, grass eat, eat animation, wool Color state, Color spawn roll, dye mutation, Sheared flag, shear item drops, regrowth, death loot, breeding/lamb EntityType, offspring Color mix, baby age/scale, `jeb_` render, Evoker wololo, spawn/summon/egg, `Animal` parent, `IShearable`/Mooshroom shear adjacency, Capture Net generic+opaque NBT.
- **B count: 2** — registry identity `organismKey=sheep`; live host path (`HostType.LIVING_BIOLOGICAL`, `hostEffectProfileId=baseline_biological`, optional Model A `contributingSourceKey=sheep`) including Analyzer projection of those keys.
- **C count: 0.** C was **not** earned.

### 1.21.1 authority anchors

- `.tmp_mc_sources/net/minecraft/world/entity/animal/Sheep.java` — class, goals, Color/Sheared, shear, NBT, offspring mix, ate(), finalizeSpawn
- `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` **585–588** (`SHEEP`)
- `.tmp_mc_sources/net/minecraft/world/item/DyeItem.java` **30–38**
- `.tmp_mc_sources/net/minecraft/world/item/ShearsItem.java` **65–88**
- `.tmp_mc_sources/net/minecraft/client/renderer/entity/layers/SheepFurLayer.java` **43–68** (`jeb_`)
- `.tmp_mc_sources/net/minecraft/world/entity/monster/Evoker.java` **301–344**
- `.tmp_mc_sources/data/minecraft/loot_table/entities/sheep.json` + `entities/sheep/{16 colors}.json`
- `.tmp_mc_sources/data/minecraft/tags/item/sheep_food.json`
- AlienCraft: `hosts.json`; `HostEligibilityService.java`; `GestationManager.java` `writeContributingSource` **164–175**; `BiologicalProfileResolver.java`; `CapturedEntitySnapshot.java`
