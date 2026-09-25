TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent A docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/sniffer.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Sniffer — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register Sniffer as a conclusion of this investigation.** Sniffer is **ABSENT** from `hosts.json`. Host Registry absence is **not** itself evidence for **A** or **B**. Classification rests on whether any **other** live BioCraft consumer requires a biological distinction beyond fail-soft identity.

Method (every behavior): owner → biological input? → existing composition? → named live BioCraft consumer? → **A / B / C**, after the four-way consumer audit.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

**Four-way consumer class** (exactly one per tempting behavior):

| Class | Meaning | Typical A/B/C |
|-------|---------|---------------|
| **1** | No BioCraft consumer exists | usually **A** |
| **2** | Consumer exists but does not consume Biological Profile | usually **A** |
| **3** | Consumer consumes BP and existing composition already represents the fact | **B** |
| **4** | Consumer consumes BP and composition genuinely lacks the fact | only path that can become **C**, and only if the missing input is biological |

Closed leaps applied independently: shared item-production outcome ≠ shared cause (Sheep Color wool vs Sniffer loot-table seeds); `Animal` parent ≠ clade; tag ≠ clade; archaeology encounter ≠ origin; entity/`EntityType.create` ≠ reproduction; renderer/model ≠ anatomy; Minecraft “ancient” flavor ≠ BioCraft composition; egg block ≠ Genome; Host Registry absence ≠ automatic A/B and is **not** a registration order. Do **not** assume Wandering Trader conclusions. Do **not** invent shared biology with Wandering Trader.

Existing BP composition tested first (no invented fields): `organismKey`, fail-soft unregistered key, optional `contributingSourceKey`, sparse `CompiledBiologicalProfile` fields (`HostType`, form key, host-effect id, `behaviorTypeKey`).

**Default: NO new BP field.** C is **not** earned. Do **not** mint `DESIGN-BIO-MANIFEST-004`.

---

## Subject / Version / Target identity

### Subject

Sniffer (`minecraft:sniffer`) — independent 1.21.1 creature: brain-driven sniff/search/dig, gift loot `gameplay/sniffer_digging` (torchflower seeds / pitcher pod), torchflower-seed food/breed, **egg dropped as `Items.SNIFFER_EGG` block-item** rather than a live baby, `SnifferEggBlock` hatch into baby Sniffer, warm-ocean-ruins archaeology egg loot as encounter acquisition, Host Registry **ABSENCE**, and whether any live BioCraft consumer requires a biological fact beyond fail-soft `organismKey=sniffer`.

Out of scope as organisms: Wandering Trader (no shared code/biology with Sniffer), Sheep (contrast only: Color-keyed wool vs world-search loot; Color remains **A** and identity `contributingSourceKey=sheep` remains **B not C** — do **not** smuggle a foraging/wool BP), Turtle egg-block hatch (adjacency of “egg is a block,” not shared lifecycle BP).

### Version

Minecraft Java **1.21.1** only / NeoForge **21.1.208**. `biocraft-alien/gradle.properties`: `minecraft_version=1.21.1`; `minecraft_version_range=[1.21.1,1.22)`; `neo_version=21.1.208`.

Mapped sources extracted this pass from `biocraft-alien/build/moddev/artifacts/neoforge-21.1.208-sources.jar` and `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar` into `.tmp_mc_sources/` (**TEMPORARY, NON-SSOT** — see `.tmp_mc_sources/README_NON_SSOT.txt`). Wiki = orientation / disagreement discovery only; **1.21.1 source wins**.

### Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:sniffer` |
| `EntityType` | `EntityType.SNIFFER` — `EntityType.java` **619–627**: `register("sniffer", Builder.of(Sniffer::new, MobCategory.CREATURE).sized(1.9F, 1.75F).eyeHeight(1.05F).passengerAttachments(2.09375F).nameTagOffset(2.05F).clientTrackingRange(10))` |
| Fire / lava | **No** `.fireImmune()` on SNIFFER. Builder default false |
| Class | `Sniffer extends Animal` (`Sniffer.java` **65**) |
| Category | `MobCategory.CREATURE` |
| Summonable | Builder does **not** call `noSummon()` |
| Attributes | `DefaultAttributes.java` **150**: `EntityType.SNIFFER` → `Sniffer.createAttributes()`. `Sniffer.createAttributes` (**82–84**): `MOVEMENT_SPEED` **0.1F**, `MAX_HEALTH` **14.0** |
| Adult dimensions | Hitbox **1.9 × 1.75**, eyeHeight **1.05**. Baby uses `LivingEntity.getAgeScale()` **0.5F** if baby (`LivingEntity.java` **548–549**) then `getType().getDimensions().scale(getAgeScale())` (**3427–3428**). Sniffer does **not** override `getAgeScale`. Digging pose uses a **state** hitbox: `DIGGING_DIMENSIONS` = width `EntityType.SNIFFER.getWidth()`, height `getHeight() - 0.4F`, eyeHeight **0.81F**, then `.scale(getAgeScale())` (`Sniffer.java` **71–73**, **115–117**) — pose/state, not a second body-plan BP |
| Baby age | `setBaby(true)` → `setAge(-48000)` (`Sniffer.java` **70**, **422–424**). `AgeableMob.BABY_START_AGE` default is **-24000** (`AgeableMob.java` **17**, **161–162**). Twice default baby duration is a vanilla age timer, not a Genome/lifecycle Profile field |
| Spawn egg | `Items.SNIFFER_SPAWN_EGG` (`Items.java` **1485–1486**): colors **8855049**, **2468720** |
| Egg item | `Items.SNIFFER_EGG = registerBlock(Blocks.SNIFFER_EGG)` (`Items.java` **670**). Egg is a **BLOCK item**, not an entity |
| Spawn placement | **ABSENT** from `SpawnPlacements` static register list (**92–174**). `hasPlacement(SNIFFER)` is false. `checkSpawnRules` with null data treats missing placement as vanilla-true (`SpawnPlacements.java` **81–83**) — egg/summon/spawn-egg paths, not biome spawn rules |
| Natural biome spawn | Resources-jar worldgen/biome JSON: **no** `"sniffer"` spawn entries (this-pass scan). Combined with missing `SpawnPlacements` row: Sniffer is **not** a natural biome-spawned CREATURE in 1.21.1 |
| Host Registry | **ABSENT.** `hosts.json` `living_biological.mobs` and all other buckets omit `"sniffer"`. No `variant_mappings` sniffer |
| Suitability | Unregistered → `MobHostRegistry.getHostType("sniffer")` is null (`MobHostRegistry.java` **46–48**) → `isSuitableForXenomorph` false (**68–70**). **Do not register from this packet.** Absence ≠ automatic **A**/**B** |

Independent existence paths (not origin): spawn egg; `/summon` (`canSummon` default true); `SnifferEggBlock.tick` hatch → `EntityType.SNIFFER.create` + `setBaby(true)` (`SnifferEggBlock.java` **71–76**); breeding drops egg **item** then hatch later. Archaeology brush of warm-ocean-ruins suspicious sand yields the egg item — **encounter acquisition**, not organism-native origin.

```text
Sniffer does X
    → Minecraft entity / brain / loot / block / renderer owns X?
    → Sniffer biological composition contributes something to X?
    → a live AlienCraft consumer needs that distinction beyond organismKey / contributingSourceKey?
```

---

## Source-completeness table

Probes began only after `Sniffer.java`, `SnifferAi.java`, and `SnifferEggBlock.java` were present under `.tmp_mc_sources/`. JSON extracted this pass from the 21.1.208 client-extra resources jar.

| Source path | Status | Role in this packet |
|-------------|--------|---------------------|
| `.tmp_mc_sources/.../animal/sniffer/Sniffer.java` | **PRESENT** (copied this pass) | Identity, state, dig loot drop, egg breed, food, baby age, brain tick |
| `.tmp_mc_sources/.../animal/sniffer/SnifferAi.java` | **PRESENT** (copied this pass) | Activities, memories, temptations, digging/sniffing behaviors |
| `.tmp_mc_sources/.../block/SnifferEggBlock.java` | **PRESENT** (copied this pass) | Block hatch, moss boost |
| `.tmp_mc_sources/.../SnifferRenderer.java` + `SnifferModel.java` + `SnifferAnimation.java` | **PRESENT** (copied this pass) | Presentation; not anatomy |
| `.tmp_mc_sources/.../EntityType.java` | **PRESENT** | SNIFFER **619–627** |
| `.tmp_mc_sources/.../DefaultAttributes.java` | **PRESENT** | Bind **150** |
| `.tmp_mc_sources/.../SpawnPlacements.java` | **PRESENT** | **No** SNIFFER row |
| `.tmp_mc_sources/.../MemoryModuleType.java` | **PRESENT** | Sniffer memories **130–133**; `SNIFF_COOLDOWN` **120** |
| `.tmp_mc_sources/.../ItemTags.java` / `BlockTags.java` | **PRESENT** | `SNIFFER_FOOD` **57**; `SNIFFER_DIGGABLE_BLOCK` **182**; `SNIFFER_EGG_HATCH_BOOST` **183** |
| `.tmp_mc_sources/.../BuiltInLootTables.java` | **PRESENT** | `SNIFFER_DIGGING` **114**; `OCEAN_RUIN_WARM_ARCHAEOLOGY` **127** |
| `.tmp_mc_sources/data/minecraft/loot_table/gameplay/sniffer_digging.json` | **PRESENT** (extracted this pass) | Gift: torchflower_seeds / pitcher_pod |
| `.tmp_mc_sources/data/minecraft/loot_table/entities/sniffer.json` | **PRESENT** | Empty entity table |
| `.tmp_mc_sources/data/minecraft/loot_table/blocks/sniffer_egg.json` | **PRESENT** | Block drop → sniffer_egg item |
| `.tmp_mc_sources/data/minecraft/loot_table/archaeology/ocean_ruin_warm.json` | **PRESENT** | **Only** archaeology table containing `sniffer_egg` |
| `.tmp_mc_sources/data/minecraft/loot_table/archaeology/{ocean_ruin_cold,desert_*,trail_ruins_*}.json` | **PRESENT** (extracted this pass) | Negative control: **no** `sniffer_egg` |
| `.tmp_mc_sources/data/minecraft/tags/block/sniffer_diggable_block.json` | **PRESENT** | Dirt/grass/podzol/coarse/rooted/moss/mud/muddy_mangrove_roots |
| `.tmp_mc_sources/data/minecraft/tags/block/sniffer_egg_hatch_boost.json` | **PRESENT** | `moss_block` only |
| `.tmp_mc_sources/data/minecraft/tags/item/sniffer_food.json` | **PRESENT** | `torchflower_seeds` only |
| `.tmp_mc_sources/.../VanillaGiftLoot.java` | **PRESENT** | Digging loot gen **231–238** |
| `.tmp_mc_sources/.../VanillaArchaeologyLoot.java` | **PRESENT** (copied this pass) | Warm ocean ruins egg **120–136** |
| `.tmp_mc_sources/.../VanillaHusbandryAdvancements.java` | **PRESENT** | Egg obtain / feed snifflet / plant seed; `INDIRECTLY_BREEDABLE_ANIMALS` includes SNIFFER (**83**) |
| `.tmp_mc_sources/.../VanillaEntityLoot.java` | **PRESENT** | Empty sniffer death loot **778** |
| `.tmp_mc_sources/.../VanillaItemTagsProvider.java` | **PRESENT** | `#sniffer_food` ← `TORCHFLOWER_SEEDS` **361** |
| `.tmp_mc_sources/.../VanillaBlockTagsProvider.java` | **PRESENT** | Diggable **1754–1764**; hatch boost moss **1765** |
| `.tmp_mc_sources/.../Animal.java` / `AgeableMob.java` / `LivingEntity.java` | **PRESENT** | Breed default vs Sniffer override; baby scale |
| AlienCraft `hosts.json` | **PRESENT** | `"sniffer"` **ABSENT** |
| AlienCraft production Java/resources/tests named `sniffer` | **ABSENT** | Grep this pass under `biocraft-alien/src` and `docs/development` |

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP representation? | Four-way consumer class | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|-----------------------------|-------------------------|--------------------|-------|
| Identity / CREATURE / size 1.9×1.75 / eye 1.05 | `EntityType.SNIFFER` | `EntityType.java` **619–627** | Identity only | Fail-soft `organismKey=sniffer`; HostType/form/effect/behavior empty | **3** — Analyzer/resolver consume `organismKey`; sparse payload already holds the key | **LIVE** generic `BiologicalProfileResolver` + `DnaSampleFromOccupant` encodeId → registryPath; **no** sniffer branch | **B** |
| Attributes health 14 / speed 0.1 | `Sniffer.createAttributes` + `DefaultAttributes` | `Sniffer.java` **82–84**; `DefaultAttributes.java` **150** | Vanilla stats | Not needed | **1** | None | **A** |
| Baby scale vs EntityType dims | `LivingEntity.getAgeScale` 0.5 + EntityType dims; digging pose `DIGGING_DIMENSIONS` | `LivingEntity.java` **548–549**, **3427–3428**; `Sniffer.java` **71–73**, **115–117** | No — age/pose hitbox | Identity sufficient | **1** | None | **A** |
| Baby duration 48000 ticks | `Sniffer.setBaby` | **70**, **422–424** vs `AgeableMob` **-24000** | No — age timer | Not a lifecycle Profile | **1** | None | **A** |
| Synched `DATA_STATE` / `State` enum | `Sniffer` + `EntityDataSerializers.SNIFFER_STATE` | IDLING/FEELING_HAPPY/SCENTING/SNIFFING/SEARCHING/DIGGING/RISING (**74–75**, **488–508**). **No** `addAdditionalSaveData` on Sniffer — state is synched presentation/AI, not NBT-authored composition | Transient/synched AI presentation | Not needed | **1** | None | **A** |
| Brain memories `SNIFFER_EXPLORED_POSITIONS`, `SNIFFER_SNIFFING_TARGET`, `SNIFFER_DIGGING`, `SNIFFER_HAPPY` (+ `SNIFF_COOLDOWN`) | `MemoryModuleType` + `SnifferAi` + `Sniffer.storeExploredPosition` | Memories **130–133** / **120**; `MEMORY_TYPES` `SnifferAi.java` **50–66**; explored list capped at **20** (`Sniffer.java` **315–319**); `SNIFFER_EXPLORED_POSITIONS` has `Codec.list(GlobalPos.CODEC)` so brain **may** persist positions — still **AI state**, not biological composition | No — AI/memory state | Not needed | **1** | None that read Sniffer brain | **A** |
| Sniff / search / scent / happy / panic reset | `SnifferAi` activities + `Sniffer.transitionTo` | `initIdleActivity` / `initSniffingActivity` / `initDigActivity` / `updateActivity` (`SnifferAi.java` **77–167**); `canSniff` (`Sniffer.java` **127–129**) | No — behavior FSM | Identity sufficient | **1** | None | **A** |
| Digging → `gameplay/sniffer_digging` item production | `Sniffer.dropSeed` + `BuiltInLootTables.SNIFFER_DIGGING` | `dropSeed` **267–286**: GIFT loot at head origin; JSON entries `torchflower_seeds` and `pitcher_pod` equal (rolls 1). `VanillaGiftLoot.java` **231–238**. **Adult-only** (`canDig` `!isBaby` **251–259**; `Sniffing.checkExtraStartConditions` `!isBaby` **366–368**) | **No stored composition.** Loot table item production, analogous to (not inherited from) Sheep shear/wool **items**. Sheep **Color** is persistent entity state and is still **A** (unconsumed); it is **not** represented by `contributingSourceKey=sheep`. Sniffer seeds are even further from composition (no entity Color-like field) | Existing identity does **not** encode seed type — and no consumer needs it to | **1** | None. Analyzer does not read digging loot | **A** |
| `#sniffer_diggable_block` | Tag JSON + `Sniffer.canDig(BlockPos)` | Tag: dirt, grass_block, podzol, coarse_dirt, rooted_dirt, moss_block, mud, muddy_mangrove_roots. Consumer: `level.getBlockState(pos).is(BlockTags.SNIFFER_DIGGABLE_BLOCK)` (`Sniffer.java` **261–265**) | Tag membership ≠ clade / diet trait | Not needed | **1** | None in BioCraft | **A** |
| `#sniffer_food` / tempt | Tag JSON + `Sniffer.isFood` + `SnifferAi.getTemptations` + `SensorType.SNIFFER_TEMPTATIONS` | `sniffer_food.json` = `torchflower_seeds` only; `isFood` **453–455**; temptations **73–75**; sensor `SensorType.java` **50** | Breeding/tempt item, not a diet BP | Child/egg remain sniffer identity | **1** | None | **A** |
| Reproduction: food → egg **item**, not entity baby | `Sniffer.spawnChildFromBreeding` override | **339–346**: spawn `ItemStack(Items.SNIFFER_EGG)` + `finalizeSpawnChildFromBreeding(..., null)`. Default `Animal.spawnChildFromBreeding` would `getBreedOffspring` + `setBaby` + add entity (`Animal.java` **214–232**) — **bypassed**. `getBreedOffspring` still `EntityType.SNIFFER.create` (**427–429**) for the abstract contract / spawn-egg clone path; breeding **does not** add that child | Lifecycle/mechanic. Entity creation ≠ reproduction of a live baby. Egg-as-item ≠ Genome | Child key would be `sniffer` if a baby existed; here the product is a block item | **1** | None | **A** |
| `canMate` same-class + state gate | `Sniffer.canMate` | Both must be `Sniffer`; both states in `{IDLING, SCENTING, FEELING_HAPPY}` then `super.canMate` (**435–441**) | Breed AI gate | Not needed | **1** | None | **A** |
| Egg hatch as **BLOCK** | `SnifferEggBlock` | `HATCH` 0→2; regular **24000** ticks / moss-boosted **12000**; per-stage `time/3 + random(300)` (`SnifferEggBlock.java` **28–32**, **64–91**, **99–101**). Hatch: `destroyBlock` then `EntityType.SNIFFER.create` + `setBaby(true)` (**69–76**) | Minecraft block hatch. Distinguish from entity-baby breed. `#sniffer_egg_hatch_boost` = moss_block only — environment timer, not origin | Not a Genome / lifecycle Profile | **1** | None | **A** |
| Archaeology egg loot | `VanillaArchaeologyLoot` + `archaeology/ocean_ruin_warm.json` + `OceanRuinPieces` warm suspicious sand | Egg **only** in warm ocean-ruins archaeology (**120–136** / JSON). Cold ocean ruins, desert well/pyramid, trail ruins: **no** `sniffer_egg` (this-pass extract). Structure: `OceanRuinPieces.java` **57** binds warm suspicious sand → `OCEAN_RUIN_WARM_ARCHAEOLOGY` | **Encounter acquisition**, not organism-native origin | Not an origin field | **1** | None | **A** |
| Death loot | `VanillaEntityLoot` / `entities/sniffer.json` | Empty loot table (**778**) | Drops ≠ anatomy | Not needed | **1** | None | **A** |
| Natural spawn | Missing `SpawnPlacements` + no biome JSON sniffer | `SpawnPlacements.java` **92–174**; resources worldgen scan **NONE** | Spawn encounter ≠ origin (and here natural spawn is absent) | Identity sufficient for egg/summon paths | **1** | None | **A** |
| Renderer / model | `SnifferRenderer` / `SnifferModel` / `SnifferAnimation` | Single texture `textures/entity/sniffer/sniffer.png` (`SnifferRenderer.java` **12–20**). `AgeableHierarchicalModel` baby **0.5F** (`SnifferModel.java` **16–24**). `setupAnim` drives walk/search/dig/sniff/happy/scent animations (**108–125**). Nose/beak/ears are **ModelPart** names | Presentation ≠ anatomy schema (`system.md` §G) | Not needed | **1** | None | **A** |
| Capture / admission | `CaptureEligibilityPolicy` + snapshot NBT | `canCapture` = alive && !player (`CaptureEligibilityPolicy.java` **19–20**) — **not** Host Registry, **not** BP. Opaque entity NBT may keep brain memories; strip list does not interpret them | Capture policy is gameplay eligibility | Type id via encodeId after capture | **2** for capture rule (does not consume BP); identity observation after capture is **3** | **LIVE** generic capture; **LIVE** `DnaSampleFromOccupant` identity | **A** (capture) / **B** (identity if analyzed) |
| Host eligibility / gestation contribution | `HostEligibilityService` + `MobHostRegistry` + `GestationManager.writeContributingSource` | Unregistered → `isSuitableForXenomorph("sniffer")` false. `writeContributingSource` only runs after chestburster spawn from a gestating host (**164–175**). Sniffer never becomes that host on the live registry | Participation gap, not a missing biological field. If a sniffer were hypothetically registered later, contribution would still be **identity key only** (Sheep precedent: `contributingSourceKey=sheep` is **B not C**) | Fail-soft `organismKey` already represents identity; empty HostType/effect is correct for unregistered | **2** for eligibility (reads Host Registry, not BP). **1** for sniffer contribution writer (never reached). **3** for Analyzer identity | Eligibility **LIVE** generic, **does not consume BP**. No live `contributingSourceKey=sniffer` | **B** (fail-soft identity after four-way audit — **not** because absence is automatic B). Do **not** register |
| Analyzer / DNA page projection | `BiologicalProfileDnaAnalysisPort` + `DnaAnalysisReport.fromCompiled` | Projects organismKey + optional contributing source + empty HostType/form/effect/behavior for unknown keys (`BiologicalProfileResolver.java` **41–56**; report **71–80**). `Genome` stays `unknown()` | Identity observation | Fail-soft key **is** the 001 payload for unregistered organisms | **3** | **LIVE** (Analyzer FEATURE-DNA-003; Pen/Pod FEATURE-DNA-UI-002). Does **not** read digging, egg, memories, or tags | **B** |

**No row is C.** Class **4** was not reached.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"sniffer"` | **ABSENT** | Not in `living_biological` / `undead` / `unsuitable` / `modded` / `variant_mappings` | Do **not** register. Absence ≠ automatic A/B; no other live consumer needs a bio distinction → identity remains fail-soft **B** |
| `BiologicalProfileResolver` sniffer branch | **ABSENT** | Generic unknown-key path (`BiologicalProfileResolver.java` **23–24**, **41–56**); test `unknownKeyPreservesOrganismKeyWithEmptyOptionals` (`BiologicalProfileResolverTest.java` **47–55**) | **LIVE** fail-soft. **TEST** covers unknown keys, not sniffer by name |
| Analyzer / `DnaSampleFromOccupant` | **LIVE** generic | encodeId → `sniffer`; contributing source only if `ContributingSourcePort.supports` (Chestburster/Drone) | Identity **B**. Genome unknown. Does not earn digging/egg fields |
| `HostEligibilityService` | **LIVE** but **does not consume BP** | Host Registry lookup | Four-way **2**. Unregistered sniffer ineligible. Not a missing BP fact |
| Gestation `writeContributingSource` | **LIVE** generic; **DEAD** for sniffer | Never reached: sniffer is not a suitable host | No live `contributingSourceKey=sniffer` |
| Xenomorph / mob-based JSON named sniffer | **ABSENT** | `biocraft-alien/src/main/resources` grep this pass | PARSE-ONLY/catalog not applicable |
| Inventory row `sniffer` | **PLANNING** | `vanilla_organism_inventory.md` **163**: bio-organic, unregistered, manifestation pending | Docs ≠ live consumer. This packet does **not** edit inventory |
| BACKLOG / SPRINT / ROADMAP sniffer | **ABSENT** | `docs/development` grep this pass | **PLANNING** silence |
| Vials / Analyzer UI / lifecycle / AI / rendering sniffer specials | **ABSENT** | Production Java grep | Do not invent consumers |
| `data/biocraft_alien/dna/` | Empty / not live SSOT | `dna.md` / `system.md` | **DEAD** as biology authority |

Classification of BioCraft surfaces for sniffer:

| Surface | Class |
|---------|-------|
| `BiologicalProfileResolver` / `CompiledBiologicalProfile` | **LIVE** generic fail-soft |
| Analyzer / DNA page (`DnaAnalysisPort`) | **LIVE** generic identity projection |
| `DnaSampleFromOccupant` / vial observation | **LIVE** generic encodeId |
| `HostEligibilityService` / `hosts.json` | **LIVE** participation; sniffer **unregistered** |
| Gestation contribution | **LIVE** machinery; **DEAD** for this organism |
| Xenomorph JSON / `behavior_type` | **ABSENT** / not a sniffer consumer |
| Inventory planning row | **PLANNING** |
| Resolver unknown-key unit test | **TEST** (generic, not sniffer-named) |
| Stubs claiming sniffer biology | **ABSENT** — do not promote |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails |
|----------------|--------------|
| “Sniffer can dig” is a BP foraging/capability field | Behavior + loot-table item production (`dropSeed` + `sniffer_digging`). Four-way **1**. Sheep Color contrast does **not** authorize a wool/foraging BP: Color is unconsumed persistent state (**A**); Sniffer has **no** analogous stored composition field at all |
| Digging seeds are stored biological composition like Sheep Color | Color is packed NBT/`DATA_WOOL_ID`. Sniffer seed **type** is rolled from a GIFT loot table at dig time. Item production ≠ stored composition |
| Brain memories (`SNIFFER_*`) are biological state / Genome | AI memories. Explored-position codec persistence is still AI state. Instruction: “Sniffer has memories” is not a BP fact |
| Scenting / “smells ancient seeds” is a chemoreception BP | `State.SCENTING` + animation + wiki flavor. No BioCraft consumer. Rejected: scent-as-BP |
| Sniffer is an ancient-origin clade because archaeology yields eggs | Warm-ocean-ruins loot is **encounter acquisition**. Spawn ≠ origin. Closed leap |
| Egg is Genome / lifecycle Profile / Ovomorph analogue | `Items.SNIFFER_EGG` is a block item; hatch is `SnifferEggBlock` creating a baby entity. Minecraft block hatch ≠ BioCraft Genome. Rejected: egg-as-Genome |
| Shared `Animal` or CREATURE category is a livestock/bio-organic clade with Sheep | Inventory label is planning only. Independent investigation. Shared parent ≠ clade |
| `#sniffer_diggable_block` / `#sniffer_food` are clades or diet traits | Tags are vanilla consumers of blocks/items. Tag ≠ clade |
| Renderer nose/beak/six legs are anatomy Profile | ModelPart presentation (`system.md` §G). First gameplay consumer of semantic anatomy has not appeared |
| Baby 48000 ticks / moss hatch boost are developmental biology fields | Vanilla timers. `#sniffer_egg_hatch_boost` is a block-below check |
| `getBreedOffspring` returning `SNIFFER.create` means live baby reproduction | Breeding override drops an egg item and passes **null** child into `finalizeSpawnChildFromBreeding`. Factory method exists for the `AgeableMob` contract / spawn-egg path |
| Host Registry absence earns **C** (must register) | Absence is participation. No named live consumer demands missing bio facts. Fail-soft identity is **B**. Do **not** register |
| Absence earns automatic **B** | Ruled out: classify from other consumers. Other distinguishing consumers: **none** → residual identity **B**, not “absence ⇒ B” |
| Analyzer exists + interesting Minecraft mechanic earns a BP field | Consumer-boundary test failed: Analyzer reads identity references, not digging/egg/memories |
| Classification forest (mammal/reptile/ancient) | Gated; not earned; reject |
| Must share biology with Wandering Trader because both are last pending inventory rows | Evidence-management pairing only. **Zero** shared 1.21.1 owners. Do not invent shared biology |
| Register because interesting / inventory-pending | Registration is participation, out of freeze, not a manifestation conclusion |

---

## Potential biological relationships

| Relationship | Owner | Biological input? | Existing composition | Named consumer | Result |
|--------------|-------|-------------------|----------------------|----------------|--------|
| Identity without Host Registry | `EntityType.SNIFFER` + fail-soft resolver | Registry key only | `organismKey=sniffer` | **LIVE** generic Analyzer/resolver | **B** |
| World-search item production vs Sheep Color-keyed wool | `Sniffer.dropSeed` / loot table vs `Sheep` Color + shear | Shared **outcome class** (items appear) ≠ shared **cause**. Sheep Color is persistent/heritable vanilla state (**A**, unconsumed). Sniffer has no Color analogue | Identity does not encode either Color or seed rolls | None for Color; none for seeds | **A** both; do **not** mint a foraging/wool field from the contrast |
| Torchflower food vs digging torchflower seeds | `#sniffer_food` vs `sniffer_digging` loot | Food tag is breed/tempt; loot is gift production. Same item id appearing in two vanilla tables is **not** a stored composition loop BioCraft must model | Identity sufficient | None | **A** |
| Egg item → block hatch → baby entity | `spawnChildFromBreeding` + `SnifferEggBlock` | Minecraft lifecycle/mechanic. Distinct from Turtle `TurtleEggBlock` world-placed eggs (adjacency only; do not import Turtle BP) | Not Genome | None | **A** |
| Archaeology warm ocean ruins | `OCEAN_RUIN_WARM_ARCHAEOLOGY` | Encounter ≠ origin | Not an origin field | None | **A** |
| Wandering Trader | **None** in Sniffer sources | **No** shared Java parent, loot, tags, memories, or egg path | Do not compose together | None | **No relationship.** Do not assume Trader conclusions |
| Host contribution if later registered | Hypothetical Host Registry + `writeContributingSource` | Would still be **identity key only** (Sheep `contributingSourceKey=sheep` is **B not C**) | Fail-soft already covers identity today | No live writer now | Do **not** register; not **C** |

**C is not earned.** No class-**4** consumer.

---

## Wiki orientation disagreements

| Common orientation | 1.21.1 authority | Conclusion |
|--------------------|------------------|------------|
| Sniffer is “ancient”; tracks “ancient seeds” | No origin/genome field. Dig loot is `torchflower_seeds` / `pitcher_pod`. Archaeology is structure loot | Flavor ≠ BP. Encounter ≠ origin |
| Digs in “dirt, grass, and moss” | `#sniffer_diggable_block` also podzol, coarse_dirt, rooted_dirt, mud, muddy_mangrove_roots | Source tag wins; wiki intro understates |
| 6.7% egg from warm ruins | Warm archaeology pool total weight **15**; `sniffer_egg` weight **1** → 1/15 | Matches; still encounter loot |
| Hatch 10 min moss / 20 min else | `BOOSTED_HATCH_TIME_TICKS=12000`, `REGULAR=24000` | Matches |
| Baby 40 minutes / two in-game days | `SNIFFER_BABY_AGE_TICKS=48000` | Matches; still an age timer |
| “Snifflet” as a creature type | `setBaby(true)` on `EntityType.SNIFFER` | UX name, not a second organismKey |
| Bedrock: heal on feed; full-health breed gate | **Absent** from Java `Sniffer.java` | Java 1.21.1 source wins; Bedrock is out of scope |
| Later-wiki pale moss / golden dandelions | Not in 1.21.1 mapped sources (`sniffer_egg_hatch_boost` = moss_block only) | Out of `minecraft_version_range`; ignore |
| Natural spawn | No `SpawnPlacements` row; no biome spawn JSON | Wiki “cannot spawn naturally” **agrees** with source |

---

## Final evidence conclusion

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** (fail-soft `organismKey=sniffer`; empty HostType / form / host-effect / behavior / contributingSource) |
| Named consumer exists | **YES** for generic identity (LIVE Analyzer / resolver / occupant sample). **NO** named consumer of digging, egg, memories, tags, or archaeology as Biological Profile data |
| Architectural escalation required | **NO** |

C threshold: no concrete currently live BioCraft consumer whose correct behavior cannot be represented by existing composition, and whose required input is genuinely biological. Class **4** not reached. Analyzer + interesting Minecraft mechanic does **not** earn a BP fact.

**Overall A/B/C: B** (identity fail-soft) with pervasive **A** ownership of dig/loot/memories/tags/egg-hatch/archaeology/renderer. **C not earned.** Do not register. Do not mint `DESIGN-BIO-MANIFEST-004`. Do not invent Wandering Trader shared biology.

---

## UNKNOWN list

| Item | Why UNKNOWN |
|------|-------------|
| Whether a future Host Registry registration of `sniffer` would use `LIVING_BIOLOGICAL` / `baseline_biological` | Out of freeze; do not register; absence is not a HostType conclusion |
| Full brain NBT round-trip of `SNIFFER_EXPLORED_POSITIONS` in capture snapshot | Codec exists; BioCraft does not interpret it; not required to classify memories as **A** |
| Exact client animation timing vs `DATA_DROP_SEED_AT_TICK` 120-tick offset | Presentation; loot still owned by `dropSeed` |
| Playtest of Analyzer UI string for an unregistered sniffer occupant | Source path is generic fail-soft; live UI not run this pass |
