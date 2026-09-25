```text
TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Hoglin docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/hoglin.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.
```

# Hoglin — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register Hoglin as a conclusion of this investigation.**

Method (every behavior): existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied independently: shared parent ≠ clade; tag ≠ clade; conversion ≠ inheritance; spawn biome ≠ origin; equipment ≠ capability; Host Registry ≠ eligibility; interesting behavior ≠ consumer; `HoglinBase` shared with Zoglin ≠ Hoglin genetics; Piglin/Villager conversion parallelism ≠ Hoglin clade.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey` (Model A Chestburster/Drone), optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

---

## Subject

Hoglin (`minecraft:hoglin`) — identity, conversion owner to Zoglin, breeding/food, warped-fungus repellents, knockback helper vs transferred state, Piglin-hunt social / `CannotBeHunted`, baby vs adult, crimson-forest spawn, fire vulnerability, loot, tags with named 1.21.1 consumers, Host Registry absence, and BioCraft consumer classification.

This packet does **not** investigate Piglin Brute, Ghast, Ravager, Witch, Creeper, Bat, or Horse as organisms. Piglin is cited only as a **named owner** of hunt/ride AI that targets Hoglin.

---

## Version

Minecraft Java **1.21.1** (`minecraft_version_range=[1.21.1,1.22)` in `biocraft-alien/gradle.properties`). Mapped NeoForge **21.1.208** sources jar is authoritative (`biocraft-alien/build/moddev/artifacts/neoforge-21.1.208-sources.jar` and `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar`). Wiki is orientation and disagreement discovery only; **source wins**.

Temporary source cache (not SSOT): `.tmp_mc_sources/`.

Prior destination report `implementations/minecraft/AlienCraft/docs/design/biological/manifestations/zoglin.md` was used only as a Hoglin-side owner checklist. Every Hoglin owner below was re-read from 1.21.1 mapped sources; destination conclusions were not copied as Hoglin facts.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:hoglin` |
| `EntityType` | `EntityType.HOGLIN` — `EntityType.java` **412–414**: `register("hoglin", Builder.of(Hoglin::new, MobCategory.MONSTER).sized(1.3964844F, 1.4F).passengerAttachments(1.49375F).clientTrackingRange(8))` |
| Fire / lava | **No** `.fireImmune()` on HOGLIN. Builder `fireImmune` defaults **false** (`EntityType.Builder` field **1254**; setter **1344–1346**). Contrast: `EntityType.ZOGLIN` **does** call `.fireImmune()` (`EntityType.java` **763–765**). Runtime: `Entity.fireImmune()` **1212–1213** → `getType().fireImmune()` **1038–1039** |
| Class | `Hoglin extends Animal implements Enemy, HoglinBase` (`Hoglin.java` **49**) |
| Category | `MobCategory.MONSTER` |
| Summonable | Builder does **not** call `noSummon()`; `summon` defaults true (`EntityType.Builder` **1253**); `canSummon()` **1034–1036** |
| Spawn egg | `Items.HOGLIN_SPAWN_EGG` (`Items.java` **1432**) — `SpawnEggItem(EntityType.HOGLIN, 13004373, 6251620, …)` |
| Attributes | `DefaultAttributes` binds `EntityType.HOGLIN` → `Hoglin.createAttributes()` (`DefaultAttributes.java` **121**). Stats (`Hoglin.java` **98–104**): max health 40, movement 0.3, knockback resistance 0.6, attack knockback 1.0, attack damage 6.0. Constructor `xpReward = 5` (**88–91**) |
| Dimensions | Hitbox **1.3964844 × 1.4**. Same numeric size literals appear on ZOGLIN builder; that is registration duplication, not copied instance genetics |
| Host Registry | **UNREGISTERED.** `hosts.json` `vanilla_hosts` / `modded_hosts` / `variant_mappings` contain no `"hoglin"`. `MobHostRegistry.getHostType("hoglin")` → **null** (`MobHostRegistry.java` **46–48**). `isSuitableForXenomorph("hoglin")` → **false** because `hostType == null` (**68–71**) |
| Inventory row | Planning inventory lists `hoglin` / bio-organic / unregistered / pending / undetermined. Inventory category ≠ HostType ≠ biology. This packet does **not** update that row |
| Suitability | Unregistered → not suitable. Unregistered ≠ ineligible-as-biology ≠ BP field |

Independent existence paths (not origin): spawn egg, `/summon` (`canSummon` true), crimson-forest natural spawn, bastion structure entity `data/minecraft/structure/bastion/mobs/hoglin.nbt`, breeding offspring `Hoglin.getBreedOffspring`.

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP representation? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|-----------------------------|--------------------|-------|
| Identity / registration / size / category | `EntityType.HOGLIN` | `EntityType.java` **412–414**: id `"hoglin"`, `MONSTER`, sized 1.3964844×1.4, no `fireImmune()` | Identity only | `organismKey = hoglin` (fail-soft; unregistered) | Generic resolver / Analyzer identity if a sample is named `hoglin`. **No** Hoglin-specific branch | **B** |
| Java type (`Animal` + `Enemy` + `HoglinBase`) | `Hoglin` class declaration | `Hoglin.java` **49**. Does **not** extend `Pig`, `Piglin`, `Monster`, or `Zoglin` | Implementation mix. Hostile animal, not a clade | Distinct key already | None for ancestry | **A/B** |
| Fire vulnerability | `EntityType` flag (absent) | HOGLIN builder omits `fireImmune()`; ZOGLIN sets it (`EntityType.java` **765**). `Entity.fireImmune()` delegates to type | **No.** Destination/source EntityType flags. Hoglin burns | Identity distinguishes Hoglin from Zoglin | None | **A** |
| Conversion Hoglin → Zoglin | **`Hoglin`** + `Mob.convertTo` | `customServerAiStep` **165–173**: if `isConverting()` increment `timeInOverworld`; if `> 300` and `EventHooks.canLivingConvert(this, ZOGLIN, …)` then sound + `finishConversion`. `isConverting` **322–324**: `!dimensionType().piglinSafe() && !isImmuneToZombification() && !isNoAi()`. `finishConversion` **264–269**: `convertTo(EntityType.ZOGLIN, true)` then Confusion 200 on **new** entity. `CONVERSION_TIME = 300` (**58**) | **Replacement, not genetics.** Source state happens to be Hoglin | Distinct keys `hoglin` / `zoglin` already represent source vs destination | None named for conversion biology | **A/B** |
| Conversion gate vs NBT name | Dimension `piglin_safe` + Hoglin NBT | Nether `piglin_safe: true` (`dimension_type/the_nether.json` **17**). Overworld **false** (`overworld.json` **20**). End **false** (`the_end.json` **21**). NBT field is still `"TimeInOverworld"` (`Hoglin.java` **297**, **310**) | **No.** Dimension monster-settings flag. End also converts. Name is misaligned with the gate | Not a Nether-origin field | None | **A** |
| Immune NBT | Hoglin synched data | `DATA_IMMUNE_TO_ZOMBIFICATION` **50**, **285–287**, **314–320**. Saved as `"IsImmuneToZombification"` **293–295**. Default false | **No.** Per-instance conversion suppress flag | Entity NBT, not BP | None | **A** |
| `convertTo` transferred vs discarded | `Mob.convertTo` | `Mob.java` **1330–1371**: create destination, copy position, baby, no-AI, name, persistence, invulnerability, optional equipment, ride vehicle, **discard source**. Hoglin NBT (`TimeInOverworld`, immune, `CannotBeHunted`), brain, breeding/love, health, Hoglin XP field are **not** copied. Zoglin constructor sets its own `xpReward = 5` | Copied baby/name/equipment = entity state, not genetics | Optional `contributingSourceKey` could name `hoglin` on a xenomorph later; conversion itself needs no field | Gestation `contributingSourceKey` is Chestburster/Drone Model A, **not** vanilla convertTo | **A/B** |
| Knockback fling | `HoglinBase` static helpers | `Hoglin.doHurtTarget` **108–117** → `HoglinBase.hurtAndThrowTarget`. Adult-only throw (`HoglinBase.java` **31–32**, **39–52**). Shield-block throw if adult (`Hoglin.java` **121–124**). **Zoglin** independently implements `HoglinBase` and calls the same statics (`Zoglin.java` **48**, **173–180**, **190–193**) | **No.** Combat helper interface. Not transferred state. Shared parent/interface ≠ clade | Not a knockback BP field | None | **A** |
| Breeding / food | `Hoglin` + `Animal` + item tag | `isFood` **276–278**: `stack.is(ItemTags.HOGLIN_FOOD)`. Tag JSON `data/minecraft/tags/item/hoglin_food.json`: **only** `minecraft:crimson_fungus`. `ItemTags.HOGLIN_FOOD` bind (`ItemTags.java` **72**). Love uses `Animal.mobInteract` **136–157**. `canFallInLove` **346–348**: `!HoglinAi.isPacified(this) && super.canFallInLove()`. Offspring `getBreedOffspring` **336–342**: `EntityType.HOGLIN.create` + `setPersistenceRequired()`. Brain: `AnimalMakeLove(EntityType.HOGLIN, 0.6F, 2)` in idle and fight (`HoglinAi.java` **78**, **95**) | Food tag + AgeableMob breeding. **Not** a Hoglin food trait for BP | Identity sufficient | None | **A** |
| Warped-fungus / portal / anchor repellents | `HoglinSpecificSensor` + `HoglinAi` + block tag | Tag `data/minecraft/tags/block/hoglin_repellents.json`: warped_fungus, potted_warped_fungus, nether_portal, respawn_anchor. `BlockTags.HOGLIN_REPELLENTS` (`BlockTags.java` **105**). Sensor `findNearestRepellent` **61–63**: `BlockPos.findClosestMatch(..., 8, 4, state.is(HOGLIN_REPELLENTS))`. Ranges: horizontal 8, vertical 4 (`HoglinAi.java` **41–42**). Pacify 200 ticks (`BecomePassiveIfMemoryPresent` **77**, **94**). Walk away from `NEAREST_REPELLENT` (**79**). `getWalkTargetValue` **218–223**: −1 near repellent; +10 on crimson nylium | **No.** Block-tag AI. Spawn-floor preference ≠ origin | Identity sufficient | None | **A** |
| Piglin hunt / `CannotBeHunted` | **Piglin AI** (not Hoglin genetics) + Hoglin NBT flag | Hoglin `canBeHunted()` **330–332**: adult and `!cannotBeHunted`. NBT `"CannotBeHunted"` **298–300**, **311**. Bastion template `data/minecraft/structure/bastion/mobs/hoglin.nbt` contains `CannotBeHunted` (gzip NBT string present). Piglin idle: `StartHuntingHoglin.create()` gated on `Piglin::canHunt` (`PiglinAi.java` **158**). `StartHuntingHoglin.java` **12–38**: requires `NEAREST_VISIBLE_HUNTABLE_HOGLIN`, absent `ANGRY_AT` / `HUNTED_RECENTLY`. Sensor fills huntable hoglin only if `hoglin.canBeHunted()` (`PiglinSpecificSensor.java` **72–73**). PiglinBrute `canHunt()` **returns false** (`PiglinBrute.java` **98–100**) — out of organism scope; cited only as hunt-gate owner | **No.** Social/combat AI + structure NBT. Hunt is Piglin-owned | Identity already distinguishes Hoglin | None in BioCraft | **A** |
| Baby piglin riding baby hoglin | `Piglin` | `Piglin.startRiding` **451–454**: if baby and vehicle type HOGLIN, stack via `getTopPassenger(..., 3)` (`MAX_PASSENGERS_ON_ONE_HOGLIN = 3`). `PiglinAi.babySometimesRideBabyHoglin` **657–664** copies `NEAREST_VISIBLE_BABY_HOGLIN` → `RIDE_TARGET` | **No.** Piglin baby ride AI. Hoglin is the vehicle type | Identity sufficient | None | **A** |
| Hoglin idle hostility (players) | `HoglinAi` | `findNearestValidAttackTarget` **166–169**: only `NEAREST_VISIBLE_ATTACKABLE_PLAYER` unless pacified/breeding. **Does not** hunt Piglin on sight. Retaliation `wasHurtBy` / `maybeRetaliate` **191–212** (not other Hoglins). Adult melee interval 40; baby 15 (`HoglinAi.java` **47–48**, **97–98**) | **No.** Brain targeting | Identity sufficient | None | **A** |
| Baby vs adult | `AgeableMob` + Hoglin overrides | `finalizeSpawn` **205–207**: 0.2F baby chance. `ageBoundaryReached` **186–193**: baby XP 3 / attack 0.5; adult XP 5 / attack 6.0. `isAdult()` **280–282** = `!isBaby()`. Babies: no knockback throw (`HoglinBase`); flee when hurt (`HoglinAi.wasHurtBy` **195–196**); `canBeHunted` false | Age state. Not a baby-hoglin BP field | Entity baby flag already copied by `convertTo` | None | **A** |
| Crimson-forest / bastion spawn | Worldgen + `SpawnPlacements` | `SpawnPlacements.java` **128**: `ON_GROUND`, `MOTION_BLOCKING_NO_LEAVES`, `Hoglin::checkHoglinSpawnRules`. Rules **196–200**: reject if block below is `NETHER_WART_BLOCK` only (no shroomlight check in JE). Biome JSON `worldgen/biome/crimson_forest.json` **89–93**: monster hoglin weight 9, min 3, max 4. Datagen `NetherBiomes.crimsonForest` **171**. Bastion pool `worldgen/template_pool/bastion/mobs/hoglin.json` + structure NBT. **No other 1.21.1 biome JSON** lists hoglin | **No.** Encounter placement. Spawn biome ≠ organism-native origin | Not an origin field | None | **A** |
| Loot | Vanilla loot table | `data/minecraft/loot_table/entities/hoglin.json`: porkchop 2–4 (furnace_smelt if this entity on fire or attacker has `#smelts_loot`); leather 0–1; looting increase. `random_sequence` `minecraft:entities/hoglin` | **No.** Drops ≠ anatomy | Not needed | None | **A** |
| Leash despite `Enemy` | Hoglin override | `Mob.canBeLeashed` **1405–1406** is `!(this instanceof Enemy)`. Hoglin **overrides** to `true` (`Hoglin.java` **94–96`). Same override on Zoglin (`Zoglin.java` **185–187`) | **No.** Explicit leash exception | Identity sufficient | None | **A** |
| Sleep / bed safety | `ServerPlayer` queries **`Monster.class`** | `ServerPlayer.java` **999–1011**: `getEntitiesOfClass(Monster.class, …, Monster::isPreventingPlayerRest)`. Hoglin extends **Animal**, not Monster → **does not** block sleep. `Enemy` is not the sleep query | **No.** Java type filter | Identity sufficient | None | **A** |
| Iron Golem / Snow Golem hostility | Golem target goals | `IronGolem` / `SnowGolem` target `instanceof Enemy`. Hoglin implements `Enemy` | **No.** Marker interface | Identity sufficient | None | **A** |
| Parrot imitate | `Parrot.MOB_SOUND_MAP` | `Parrot.java` **91**: `EntityType.HOGLIN → SoundEvents.PARROT_IMITATE_HOGLIN`. Presentation map, not a tag | **No.** Sound table | Identity sufficient | None | **A** |
| Entity-type tags | **Absent from extracted 1.21.1 entity_type tags** | Jar `tags/entity_type/*.json`: hoglin is **not** in `#undead`, `#zombies` (zoglin **is** in zombies), `#fall_damage_immune`, `#sensitive_to_smite` (aliases `#undead`), `#raiders`, etc. Item/block tags `hoglin_food` / `hoglin_repellents` are **about** hoglin gameplay, not entity-type clade membership | Tag ≠ clade. Hoglin is **not** undead/zombie by 1.21.1 entity tags | Distinct key vs zoglin | Vanilla tag consumers do not list hoglin | **A** |
| Advancements | Kill-mob lists | `advancement/adventure/kill_a_mob.json` / `kill_all_mobs.json` include `minecraft:hoglin` | UX checklist | Identity sufficient | None | **A** |
| Host Registry participation | **ABSENT** | `hosts.json` has no hoglin. Resolver `hostType == null` | Participation missing. Unregistered ≠ biology | Fail-soft `organismKey`; HostType empty | `HostEligibilityService.isSuitableForXenomorph("hoglin")` false via null HostType. Eligibility undetermined as biology, blocked as current origin | **B** |

**No row is C.**

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` key `hoglin` | **UNREGISTERED** | Absent from `vanilla_hosts.living_biological`, `undead`, `unsuitable.*`, `modded_hosts`, `variant_mappings` (`systems/hosts.json`) | Do **not** register in this pass. Participation ≠ eligibility ≠ manifestation |
| `BiologicalProfileResolver` | **LIVE** generic | `BiologicalProfileResolver.java` **35–56**: lookup lowercased `organismKey`; `MobHostRegistry.getHostType`; unknown keys fail-soft (comment **23–24**; port contract `BiologicalProfilePort.java` **22–24**) | `hoglin` is representable as identity without registration. No Hoglin branch |
| `CompiledBiologicalProfile` | **LIVE** composition type | Fields: organismKey, HostType, xenomorphFormKey, hostEffectProfileId, behaviorTypeKey, contributingSourceKey (`CompiledBiologicalProfile.java` **23–28**, **71–124**) | Sparse identity + refs. Not a Hoglin dossier. No new field used or earned |
| Analyzer / `BiologicalProfileDnaAnalysisPort` | **LIVE** generic | Port **39–41**: `profiles.resolve(BiologicalProfileRef.of(organismKey), sample.contributingSourceKey())`. `DnaAnalysisReport.fromCompiled` copies those refs. Screen reads synced report only (`DnaAnalyzerProjectionOwnershipTest`) | If a vial/occupant were keyed `hoglin`, Analyzer would project fail-soft identity. **No** Hoglin-specific analysis |
| `DnaSampleFromOccupant` | **LIVE** generic | `organismKey` from xenomorph form **or** encode-id path (`DnaSampleFromOccupant.java` **51–59** via `HostRegistryPaths`). Contributing source only if `ContributingSourcePort.supports` (Chestburster/Drone carriers) | A captured Hoglin occupant would sample as `hoglin` identity. Vanilla Hoglin is **not** a contributing-source carrier |
| Gestation `contributingSourceKey` | **LIVE machinery, origin blocked** | `GestationManager.writeContributingSource` **164–175**: encode host id → `setContributingSourceKey` on Chestburster. `HostEligibilityService.isValidFacehuggerHost` **33–44** requires `isSuitableForXenomorph` → registry HostType. Hoglin HostType **null** → suitability **false** | Representation exists for Model A xenomorphs. Hoglin cannot originate a production contribution through the current Host Registry path. Do not treat that as a missing Hoglin BP field |
| Chestburster / Drone carriers | **LIVE** Model A | `ChestbursterEntity` / `DroneEntity` `contributingSourceKey` field + NBT persistence. Tests distinguish cow vs human on **chestburster**, not hoglin | Hoglin is not a xenomorph form. Do not mint Hoglin contribution |
| Hoglin entity JSON / AI config | **ABSENT** | Zero `hoglin` matches under `biocraft-alien/src/main` Java/JSON (shell search). Inventory markdown is planning-only | Vanilla remains owner of Hoglin gameplay |
| Tests | **TEST** generic; **no Hoglin fixture** | `BiologicalProfileResolverTest.unknownKeyPreservesOrganismKeyWithEmptyOptionals` **47–55**. Zero `hoglin` in `src/test` | Fail-soft is proven for unknown keys. Hoglin is expected UNREGISTERED and untested as a named key |
| Inventory / dna.md mentions | **PLANNING / PARSE-ONLY** | Inventory row pending. `dna.md` mentions Hoglin only as conversion source in the Zoglin investigation bullet | Docs are not live consumers. Do not treat planning labels as biology |

Consumer classification for this organism:

| Candidate | Classification |
|-----------|----------------|
| `BiologicalProfileResolver` | **LIVE** generic fail-soft (not Hoglin-specific) |
| `CompiledBiologicalProfile` | **LIVE** generic composition |
| Analyzer / `BiologicalProfileDnaAnalysisPort` / `DnaAnalysisReport` | **LIVE** generic projection |
| Gestation `contributingSourceKey` | **LIVE** xenomorph machinery; Hoglin **origin blocked** |
| `HostEligibilityService` | **LIVE** registry gate; Hoglin ineligible via null HostType |
| `hosts.json` hoglin row | **DEAD / ABSENT** (unregistered) |
| Hoglin production JSON | **ABSENT** |
| Inventory `hoglin` row | **PLANNING** |
| JUnit hoglin cases | **ABSENT** (generic unknown-key **TEST** only) |
| Hoglin as registered conclusion | **Do not register** |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails on 1.21.1 evidence |
|----------------|--------------------------------|
| Hoglin + Zoglin share `HoglinBase` ⇒ Hoglin genetics / knockback trait | Interface is a **static combat helper**. Zoglin **reimplements** it on a new class. `convertTo` does not copy methods. Shared helper ≠ clade |
| Hoglin → Zoglin conversion ⇒ Hoglin ancestry / zombified Hoglin BP | Owner is `Hoglin.finishConversion` + `Mob.convertTo` **replace**. Discarded: health, brain, Hoglin NBT, breeding, sensors. Surviving baby/name/equipment are entity state. Conversion ≠ inheritance |
| Parallel `piglinSafe` timer with AbstractPiglin ⇒ Piglin/Villager conversion clade | Same **dimension flag** and 300-tick pattern; **different owners** (`Hoglin` vs `AbstractPiglin`) and **different destinations** (`ZOGLIN` vs `ZOMBIFIED_PIGLIN`). Parallel helper ≠ clade. Piglin/Villager conversion-source grouping is **out of scope and rejected** |
| Crimson forest / Nether spawn ⇒ organism-native origin | Encounter worldgen. `SpawnPlacements` + biome JSON + bastion NBT. Independent egg/summon/breeding also exist. Spawn biome ≠ origin |
| `#hoglin_food` / crimson fungus ⇒ Hoglin diet trait for BP | `Animal.isFood` + item tag. Vanilla breeding owner. No BioCraft consumer |
| Warped fungus fear ⇒ Nether-fungus biology / Hoglin vs Strider/Piglin repellent clade | Hoglin reads `#hoglin_repellents`. Piglin sensor reads `#piglin_repellents` (different tag, includes soul campfire). Shared “fungus fear” is **not** a named shared trait owner |
| Piglin hunt / baby ride ⇒ Hoglin–Piglin social genetics | `StartHuntingHoglin`, `PiglinSpecificSensor`, `Piglin.startRiding` are **Piglin-owned**. Hoglin `CannotBeHunted` is an NBT hunt **exemption**, not a capability |
| Porkchop/leather loot ⇒ Pig relationship | Loot table only. `Hoglin` does not extend `Pig`. Closed leap |
| `Enemy` + `MONSTER` category ⇒ Monster clade with Zoglin | Zoglin **extends Monster**. Hoglin **extends Animal**. Sleep query is `Monster.class`, so Hoglin does not block beds. Category/interface ≠ clade |
| Host Registry absence ⇒ biological ineligibility | Unregistered means participation missing. `organismKey` still fail-softs. Do not infer ineligibility-as-biology |
| Interesting Nether hostile breedable animal ⇒ needs a Hoglin Profile | Interesting ≠ consumer. No named live consumer needs a missing fact |
| Wiki “zombification” / `TimeInOverworld` ⇒ Overworld-only undead process | Gate is `!piglinSafe()` (Overworld **and** End). Destination is Zoglin EntityType, not a Hoglin undead flag |
| Golden dandelion baby freeze (wiki usable items) | **Not** in 1.21.1 `hoglin_food` (crimson fungus only). Not in `Hoglin.isFood`. Later-version / wiki extra — exclude |
| Register Hoglin because Zoglin investigation existed | Destination report does not authorize Hoglin registration. This packet independently finds unregistered + A/B sufficient |

---

## Potential biological relationships

For each candidate: relationship / owner / biological input / existing composition / named consumer / result.

### 1. Hoglin as conversion source of Zoglin

- **Relationship:** Real **entity replacement** when `!piglinSafe` for >300 ticks (unless immune / no-AI).
- **Owner:** `Hoglin.customServerAiStep` / `finishConversion`; `Mob.convertTo(ZOGLIN, true)`.
- **Biological input?** No. Environmental/dimension replacement. Source organism happens to be Hoglin.
- **Existing composition:** `organismKey=hoglin` (source identity) and `organismKey=zoglin` (destination). Optional Model A `contributingSourceKey` is a **xenomorph** composition slot, not vanilla convertTo.
- **Named consumer?** None that needs a conversion trait, zombification field, or Hoglin genetics.
- **Result:** **A/B**. Do not treat as Hoglin DNA. Do not treat as conversion-source clade with Piglin/Villager.

### 2. HoglinBase shared with Zoglin

- **Relationship:** Both implement `HoglinBase` and call `hurtAndThrowTarget` / `throwTarget`.
- **Owner:** Interface statics; each class wires `doHurtTarget` itself.
- **Biological input?** No. Combat helper reuse.
- **Existing composition:** Distinct keys already.
- **Named consumer?** None for knockback-as-anatomy.
- **Result:** **A**. Shared interface ≠ Hoglin genetics.

### 3. Hoglin ↔ Piglin hunt / ride / numeric standoff

- **Relationship:** Piglins hunt huntable adult hoglins; hoglins retreat if piglins outnumber; baby piglins ride baby hoglins (max 3).
- **Owner:** `PiglinAi`, `StartHuntingHoglin`, `PiglinSpecificSensor`, `HoglinAi.piglinsOutnumberHoglins`, `Hoglin.canBeHunted`, bastion `CannotBeHunted` NBT.
- **Biological input?** No. Cross-type AI + structure flag.
- **Existing composition:** Identity of each type already.
- **Named consumer?** None in BioCraft. Piglin Brute is out of organism scope; `canHunt()==false` is a PiglinBrute owner fact only.
- **Result:** **A**. Not a Hoglin–Piglin clade.

### 4. Crimson forest / crimson nylium preference / crimson fungus food

- **Relationship:** Natural spawn in crimson forest; walk-target bonus on crimson nylium; breed with crimson fungus.
- **Owner:** biome JSON / `NetherBiomes`; `Hoglin.getWalkTargetValue`; `#hoglin_food`.
- **Biological input?** No. Encounter + AI + item tag. **Spawn biome ≠ origin.**
- **Existing composition:** Not needed as origin.
- **Named consumer?** None.
- **Result:** **A**.

### 5. Hoglin as BioCraft host / contributing source

- **Relationship:** Could a Hoglin host contribute `contributingSourceKey=hoglin`?
- **Owner:** Host Registry + `HostEligibilityService` + `GestationManager.writeContributingSource`.
- **Biological input?** Participation is **missing** (unregistered). Machinery would accept a path string if eligibility passed; it does not today.
- **Existing composition:** Fail-soft `organismKey=hoglin` already. Model A contributing source is xenomorph-side, blocked at eligibility.
- **Named consumer?** Generic LIVE gestation/Analyzer; **no** consumer asking for a Hoglin-specific missing fact. Block is null HostType, not a missing BP field.
- **Result:** **B** for identity; origin **blocked**. Do not register. Do not invent a Hoglin contribution field.

### 6. Hoglin ↔ Pig via porkchop

- **Relationship:** Both drop porkchop.
- **Owner:** Separate loot tables.
- **Biological input?** No.
- **Existing composition:** Distinct keys.
- **Named consumer?** None.
- **Result:** **A**. Rejected clade.

**C is not earned for any relationship.**

---

## Wiki orientation disagreements

Source: [minecraft.wiki Hoglin](https://minecraft.wiki/w/Hoglin) (orientation only). **1.21.1 mapped source wins.**

| Wiki orientation | 1.21.1 authority | Conclusion |
|------------------|------------------|------------|
| Transform after 15 seconds in Overworld/End | `CONVERSION_TIME = 300` ticks; gate `!piglinSafe()` (`Hoglin.java` **58**, **165–173**, **322–324**). Nether `piglin_safe: true`; Overworld and End `false` | **Agrees** on 15s and End-included conversion. Source for the actual gate name |
| NBT `TimeInOverworld` = ticks in the Overworld | Counter increments whenever `isConverting()` is true, including **the End** | **Disagreement / misname.** Source: dimension flag, not Overworld-only |
| “Zombification” / converts to Zoglin | `convertTo(EntityType.ZOGLIN, true)` replace; sound `HOGLIN_CONVERTED_TO_ZOMBIFIED`; immune NBT `IsImmuneToZombification` | Gameplay wording. **Not** genetics, not `#undead` membership (hoglin **absent** from `#undead` / `#zombies`) |
| Avoid warped fungi etc. within **7** blocks | Sensor match range **8** horizontal, **4** vertical (`HoglinSpecificSensor.java` **62**; `HoglinAi.java` **41–42**). `isPosNearNearestRepellent` uses `closerThan(pos, 8.0)` | **Source wins: 8 / 4**, not 7 |
| Usable items include **Golden Dandelion** (baby freeze) | `#hoglin_food` = crimson fungus **only**. `Hoglin.isFood` is that tag. No golden-dandelion branch on Hoglin | **Exclude.** Not 1.21.1 JE Hoglin food |
| Shroomlight spawn exclusion | Wiki marks **Bedrock only**. JE `checkHoglinSpawnRules` rejects **nether wart block** only | **Source:** JE wart-block only |
| Baby spawn 20% JE | `PROBABILITY_OF_SPAWNING_AS_BABY = 0.2F` (`Hoglin.java` **51**, **205–207**) | **Agrees** |
| Groups 3–4 in crimson forest, weight 9 | `crimson_forest.json` min 3 max 4 weight 9; `NetherBiomes.java` **171** | **Agrees** |
| Bastion hoglins `CannotBeHunted` | NBT key present on `structure/bastion/mobs/hoglin.nbt`; Java only reads/writes the flag (`Hoglin.java` **298–332**) | **Agrees** that the flag exists and is structure-associated. Owner is NBT + Piglin hunt AI |
| Attacks players; piglin fight is standoff/retaliate | Idle attack target is **player only** (`HoglinAi.findNearestValidAttackTarget`). Piglin hunt is Piglin-owned | **Agrees** with official wiki hostility section. Third-party “attacks piglins on sight” pages are **wrong** for 1.21.1 JE idle targeting |
| Does not prevent sleeping | `ServerPlayer` rest check is `Monster.class` (`ServerPlayer.java` **1003–1008**). Hoglin is `Animal` | **Agrees.** Type filter, not a Hoglin sleep trait |
| Fire vulnerable; Zoglin fire immune | HOGLIN no `fireImmune()`; ZOGLIN has it | **Agrees.** Destination EntityType flag, not Hoglin fire biology |
| Leashable despite hostile | `Hoglin.canBeLeashed()` override **true** | **Agrees** |
| Adult attack ~6 / baby 0.5 | Attributes attack 6.0; baby `ageBoundaryReached` sets 0.5 | **Agrees** with Java literals (difficulty scaling is vanilla damage pipeline) |

---

## Final evidence conclusion

Hoglin is a 1.21.1 `Animal`+`Enemy` monster identity. Minecraft owns conversion, breeding, repellents, knockback helpers, spawn, loot, and Piglin-facing hunt flags. BioCraft already fail-softs `organismKey=hoglin` without registration. No named consumer needs a missing biological fact.

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** |
| Named consumer exists | **NO** (no named consumer of a missing Hoglin biological fact; generic identity plumbing is not a Hoglin-specific consumer) |
| Architectural escalation required | **NO** |

**Stop.** A = vanilla ownership; B = existing identity/composition; C = not earned. Do **not** register `hoglin`. Do **not** mint a Hoglin/Nether/zombification/knockback Profile. Do **not** treat Hoglin as a conversion-source clade with Piglin/Villager. Do **not** treat `HoglinBase` as genetics. Do **not** treat crimson/Nether spawn as origin.

### A/B/C summary

- **A:** conversion timer/gate, immune NBT, knockback helpers, food/breeding, repellents, Piglin hunt/ride, baby/adult numbers, crimson/bastion spawn, fire flag, loot, tags, leash override, sleep non-block, parrot imitate.
- **B:** registry identity `organismKey=hoglin` (fail-soft unregistered); HostType empty; optional Model A `contributingSourceKey` already exists on xenomorphs and is **not** required as a new Hoglin field.
- **C:** none.

### 1.21.1 authority anchors (Hoglin-side)

- `.tmp_mc_sources/net/minecraft/world/entity/monster/hoglin/Hoglin.java` — class, conversion, food, NBT, baby, spawn rules, leash
- `.tmp_mc_sources/net/minecraft/world/entity/monster/hoglin/HoglinAi.java` — brain, love, pacify, player target, piglin standoff
- `.tmp_mc_sources/net/minecraft/world/entity/monster/hoglin/HoglinBase.java` — knockback statics
- `.tmp_mc_sources/net/minecraft/world/entity/ai/sensing/HoglinSpecificSensor.java` — repellents + piglin/hoglin counts
- `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` **412–414**, **763–765**, **1038–1039**, **1254**, **1344–1346**
- `.tmp_mc_sources/net/minecraft/world/entity/Mob.java` **1330–1371** — `convertTo`
- `.tmp_mc_sources/net/minecraft/world/entity/SpawnPlacements.java` **128**
- `.tmp_mc_sources/net/minecraft/world/entity/monster/piglin/StartHuntingHoglin.java`, `PiglinAi.java`, `PiglinSpecificSensor.java`
- JSON: `data/minecraft/tags/item/hoglin_food.json`, `tags/block/hoglin_repellents.json`, `loot_table/entities/hoglin.json`, `worldgen/biome/crimson_forest.json`, `dimension_type/{overworld,the_nether,the_end}.json`, `structure/bastion/mobs/hoglin.nbt`
- AlienCraft: `hosts.json` (no hoglin); `BiologicalProfileResolver.java`; `CompiledBiologicalProfile.java`; `BiologicalProfileDnaAnalysisPort.java`; `HostEligibilityService.java`; `GestationManager.java`; `DnaSampleFromOccupant.java`; `BiologicalProfileResolverTest.java`
