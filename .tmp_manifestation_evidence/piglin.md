# TEMPORARY EVIDENCE PACKET — NOT PROJECT SSOT

**Status:** Temporary Piglin investigation artifact. **Not** Biological Profile SSOT. **Not** a canonical manifestation report. **Not** permission to mint Feature IDs, edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or DESIGN-BIO-MANIFEST-004.

**Do not** promote this file into `manifestations/piglin.md` or any living hub without a later authorized pass. **Do not register** `piglin` as a conclusion of this packet.

**Subject lock:** Piglin (`minecraft:piglin`) only. AbstractPiglin is a **Java parent**, not a biological clade. Piglin Brute is **adjacency only** (second conversion source via AbstractPiglin). Do **not** write brute AI, brute spawn, brute equipment, or brute barter-absence as Piglin biology. Hoglin hunting is targeting, not a Hoglin/Piglin clade. Conversion to Zombified Piglin is entity replacement, not inheritance. Do **not** copy `EntityType.ZOMBIFIED_PIGLIN.fireImmune()` onto Piglin. Ghast, Ravager, Witch, Creeper, Bat, Horse are out of scope.

**Isolation:** Authoritative Minecraft Java **1.21.1** mapped sources, live BioCraft, locked context, and this packet’s own reads only. Destination report `manifestations/zombified_piglin.md` was **verified against source**, not copied as authority.

---

## Subject

Piglin (`minecraft:piglin`) — identity, absent fire immunity, AbstractPiglin-owned Overworld/End conversion to Zombified Piglin, bartering, gold/equipment gating, Hoglin hunting, zombified/soul-fire fear, baby state, Nether spawn, tags with named 1.21.1 consumers, Host Registry absence — and whether any of that earns a Biological Profile field or a named BioCraft consumer that needs a missing biological fact.

---

## Version

Minecraft Java **1.21.1** (`minecraft_version_range=[1.21.1,1.22)` in `biocraft-alien/gradle.properties`). Mapped NeoForge **21.1.208** sources jar is authoritative (`biocraft-alien/build/moddev/artifacts/neoforge-21.1.208-sources.jar` and `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar`). Wiki is orientation and disagreement discovery only; **source wins**.

Temporary source cache (not SSOT): `.tmp_mc_sources/`.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:piglin` |
| `EntityType` | `EntityType.PIGLIN` — `EntityType.java` 536–544: `Builder.of(Piglin::new, MobCategory.MONSTER).sized(0.6F, 1.95F).eyeHeight(1.79F).passengerAttachments(2.0125F).ridingOffset(-0.7F).clientTrackingRange(8)` |
| `fireImmune` | **ABSENT** on Piglin. Builder default `fireImmune = false` (`EntityType.Builder` 1254). Contrast: `EntityType.ZOMBIFIED_PIGLIN` **calls** `.fireImmune()` (`EntityType.java` 793–801). Do **not** copy destination fire immunity onto Piglin |
| Class | `Piglin extends AbstractPiglin implements CrossbowAttackMob, InventoryCarrier` (`Piglin.java` 57). `AbstractPiglin extends Monster` (`AbstractPiglin.java` 22) |
| AbstractPiglin | Java parent + conversion owner. **Not** a clade. Second subclass is Piglin Brute (adjacency only) |
| Category | `MobCategory.MONSTER` |
| Summonable | PIGLIN builder does **not** call `noSummon()`; `canSummon()` follows Builder default `summon = true` (`EntityType.java` 1034–1036, 1253) |
| Attributes | `DefaultAttributes` → `Piglin.createAttributes()` (`DefaultAttributes.java` 135): max health **16**, movement **0.35F**, attack damage **5.0** (`Piglin.java` 65–67, 192–194). Constructor `xpReward = 5` (122) |
| Baby dimensions | `BABY_DIMENSIONS = EntityType.PIGLIN.getDimensions().scale(0.5F).withEyeHeight(0.97F)` (`Piglin.java` 71). Adult uses EntityType size |
| Spawn placement | `SpawnPlacements.register(EntityType.PIGLIN, ON_GROUND, MOTION_BLOCKING_NO_LEAVES, Piglin::checkPiglinSpawnRules)` (`SpawnPlacements.java` 129) |
| Spawn egg | `Items.PIGLIN_SPAWN_EGG` (`Items.java` 1453) |
| Death loot JSON | `data/minecraft/loot_table/entities/piglin.json` is **empty of pools** (type entity + `random_sequence` only). Extra drops are Java: 8-slot inventory + charged-creeper `PIGLIN_HEAD` (`Piglin.dropCustomDeathLoot` 157–166) |
| Host Registry | **UNREGISTERED.** `hosts.json` has no `"piglin"`, `"piglin_brute"`, or `"zombified_piglin"`. `MobHostRegistry.getHostType("piglin")` → `null`. `isSuitableForXenomorph("piglin")` → **false** (`MobHostRegistry.java` 46–48, 68–71) |
| Inventory row | Planning inventory: `piglin` / bio-organic / unregistered / pending / undetermined. Inventory category ≠ HostType ≠ biology. This packet does **not** update that row |
| Suitability | Unregistered → not suitable. Unregistered ≠ ineligible-as-biology ≠ BP field |

Adjacent vanilla types (identity / conversion adjacency only; **not** investigated here as organisms):

| Type | 1.21.1 fact | This packet’s use |
|------|-------------|-------------------|
| `EntityType.PIGLIN_BRUTE` | Same size/eyeHeight; **no** `fireImmune()` (`EntityType.java` 545–553). `PiglinBrute extends AbstractPiglin`. `canHunt() == false`. Does **not** override `finishConversion` | Second AbstractPiglin conversion source. **Do not** write brute AI/spawn as Piglin biology |
| `EntityType.ZOMBIFIED_PIGLIN` | `fireImmune()`, `ZombifiedPiglin extends Zombie`. Destination of AbstractPiglin `convertTo` | Conversion destination identity. Destination `fireImmune` is **gained**, not Piglin |
| `EntityType.HOGLIN` | Separate type. `Hoglin.canBeHunted()` = adult && !CannotBeHunted. Parallel `!piglinSafe` conversion to Zoglin is Hoglin-owned | Hunt **target**, not clade |
| `EntityType.ZOGLIN` | `PiglinAi.isZombified` includes ZOGLIN **or** ZOMBIFIED_PIGLIN | Fear predicate operand, not Piglin biology |

---

## Behavior ownership table

Method: existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

A = Minecraft owns it, no biological input required.
B = `organismKey` / `contributingSourceKey` already sufficient.
C = named consumer needs a missing biological fact — STOP, document minimum, do not design.

Closed leaps applied: shared parent ≠ clade; tag ≠ clade; conversion ≠ inheritance; spawn biome ≠ origin; equipment ≠ capability; Host Registry ≠ eligibility; interesting behavior ≠ consumer.

Existing BP composition: `organismKey`, optional `contributingSourceKey` (Model A Chestburster/Drone), optional HostType, xenomorphFormKey, hostEffectProfileId, behaviorTypeKey.

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP representation? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|-----------------------------|--------------------|-------|
| Identity / MONSTER / size 0.6×1.95 / eyeHeight 1.79 | `EntityType.PIGLIN` | `EntityType.java` 536–544 | Identity only | `organismKey = piglin` (fail-soft if unregistered) | Generic `BiologicalProfileResolver` + `DnaSampleFromOccupant` encode-id path if a sample exists | **B** |
| `fireImmune` **absent** | Piglin EntityType builder (default false) | No `.fireImmune()` on PIGLIN. ZP **has** it (`EntityType.java` 796). Magma `isValidSpawn` requires `entityType.fireImmune()` (`Blocks.java` 4943) | EntityType flag, not tissue | Distinct keys already separate Piglin from ZP | None for a fire-immunity field | **A** / identity **B** |
| Java parent `AbstractPiglin` | Shared Minecraft class | `Piglin extends AbstractPiglin`; `PiglinBrute extends AbstractPiglin` | Implementation reuse. **Closed leap:** shared parent ≠ clade | Distinct registry ids `piglin` / `piglin_brute` | None for clade | **A** |
| Conversion trigger / replace | `AbstractPiglin.customServerAiStep` / `finishConversion` | `isConverting()` = `!dimensionType().piglinSafe()` && !immune && !noAI (`AbstractPiglin.java` 94–96). `timeInOverworld > 300` then `convertTo(ZOMBIFIED_PIGLIN, true)` (88–104). Nether `piglin_safe: true`; Overworld/End `false` (`dimension_type/*.json`) | Replacement, not genetics. Conversion ≠ inheritance | Distinct keys `piglin` vs `zombified_piglin`. Optional `contributingSourceKey` could name source **if** a later Model A consumer existed | **None** live needing a conversion trait | **A/B** |
| Piglin inventory drop before convert | `Piglin.finishConversion` then `super` | Cancel admire; `inventory.removeAllItems().forEach(this::spawnAtLocation)` then `AbstractPiglin.finishConversion` (`Piglin.java` 323–327). 8-slot `SimpleContainer` (73) | Entity container dump, not composition | Not needed | None | **A** |
| Transferred on `convertTo(..., true)` | `Mob.convertTo` | Copies position, baby, no-AI, name, persistence, invulnerability, loot-pickup, equipment stacks + drop chances; then `discard()` source (`Mob.java` 1330–1371). Confusion 200 ticks on **new** ZP (`AbstractPiglin.java` 101) | Entity/item state | Destination key already | None | **A/B** |
| Reverse conversion | **Absent** | No ZP→Piglin `convertTo` in this Java | N/A | Distinct keys | None | **A** |
| Bartering | `PiglinAi` + loot table | Currency: `BARTERING_ITEM = GOLD_INGOT` (`PiglinAi.java` 79); `IItemExtension.isPiglinCurrency` default is that item (120–121). Adult-only `canAdmire` (553–555). Admire 119 ticks (~6s) (83, 798–799). `getBarterResponseItems` reads `BuiltInLootTables.PIGLIN_BARTERING` → `data/minecraft/loot_table/gameplay/piglin_bartering.json` (443–450). Player use: `Piglin.mobInteract` → `PiglinAi.mobInteract` (262–271, 540–550) | Vanilla trade AI + loot. **Not** Villager trading. Equipment ≠ capability | Identity sufficient | None | **A** |
| Loved gold items / pickup | `PiglinAi.isLovedItem` / `wantsToPickup` / `pickUpItem` | Tag `#minecraft:piglin_loved` (`ItemTags.java` 54; `data/minecraft/tags/item/piglin_loved.json`). Pickup gated by `EventHooks.canEntityGrief` (`Piglin.wantsToPickUp` 414–416) | Item tags + AI | Identity sufficient | None | **A** |
| Gold armor neutrality | `PiglinAi.isWearingGold` | Iterates armor; `ItemStack.makesPiglinsNeutral` → `IItemExtension` default: `ArmorItem` with `ArmorMaterials.GOLD` (`PiglinAi.java` 641–650; `IItemExtension.java` 132–133). Sensor fills `NEAREST_TARGETABLE_PLAYER_NOT_WEARING_GOLD` (`PiglinSpecificSensor.java` 87–88, 116) | Equipment gating, **not** a gold-metabolism capability | Identity sufficient | None | **A** |
| Crossbow / melee combat | `Piglin` as `CrossbowAttackMob` + `PiglinAi.initFightActivity` | `canFireProjectileWeapon` only `Items.CROSSBOW` (`Piglin.java` 396–398). Fight activity: `CrossbowAttack`, `MeleeAttack`, `BackUpIfTooClose` if holding crossbow (`PiglinAi.java` 168–179). Spawn weapon 50% crossbow / golden sword if adult and **not** STRUCTURE (`Piglin.java` 206–211, 329–331). Adult gold armor 10% per slot (231–244) | Spawn/combat equipment. Equipment ≠ organism capability field | Identity sufficient | None | **A** |
| Hoglin hunting | `StartHuntingHoglin` + `PiglinAi` + sensor | Idle: `BehaviorBuilder.triggerIf(Piglin::canHunt, StartHuntingHoglin.create())` (`PiglinAi.java` 158). Hunt memory: visible **adult huntable** Hoglin (`PiglinSpecificSensor.java` 70–74; `Hoglin.canBeHunted` adult && !CannotBeHunted). Broadcast anger to nearby adult AbstractPiglins that `canHunt` (`PiglinAi.java` 667–672). Retreat if hoglins outnumber piglins (759–762). 10% dance is **after Hoglin kill**, not hunt start (`wantsToDance` 453–455) | Targeting `EntityType.HOGLIN`. **Closed leap:** hunt ≠ clade | Distinct keys already | None | **A** |
| `CannotHunt` | Piglin NBT / `canHunt()` | Field `cannotHunt`; written/read as `CannotHunt` (`Piglin.java` 74, 132–147, 299–306). Java **never assigns** it except NBT. `finalizeSpawn` STRUCTURE skips baby/weapon but does **not** set the flag (204–217). Wiki bastion-worldgen claim is **unconfirmed in this Java**; do not invent | Spawn/AI gate | Identity sufficient | None | **A** |
| Zombified / Zoglin fear | `PiglinAi.isZombified` + core `avoidZombified` | `isZombified` = `ZOMBIFIED_PIGLIN \|\| ZOGLIN` (`PiglinAi.java` 846–848). Sensor `NEAREST_VISIBLE_ZOMBIFIED` (95–97, 115). Avoid copy to `AVOID_TARGET` for 5–7s (292–296). Fight erases attack target if near zombified (179). Desired distance 6 (102, 492–496) | Piglin AI predicate. **Not** a zombification trait on Piglin or ZP | Identity already distinguishes types | None | **A** |
| Soul-fire / repellent fear | `PiglinSpecificSensor.findNearestRepellent` + `avoidRepellent` | Block tag `#minecraft:piglin_repellents`: soul_fire, soul_torch, soul_lantern, soul_wall_torch, soul_campfire (`data/minecraft/tags/block/piglin_repellents.json`). Soul campfire only if lit (`PiglinSpecificSensor.java` 128–132). Walk away from `NEAREST_REPELLENT` (`PiglinAi.java` 284–286). Item tag `#minecraft:piglin_repellents` blocks pickup (soul_torch/lantern/campfire only) (`PiglinAi.java` 460–461; item JSON) | Block/item tags + pathing. Path malus `DANGER_FIRE` 16 / `DAMAGE_FIRE` -1 on AbstractPiglin ctor (33–34) is fire pathing, **not** `fireImmune` | Identity sufficient | None | **A** |
| Baby piglin | `Piglin` synched `DATA_BABY_ID` | Not `AgeableMob`. `setBaby` / `isBaby` (`Piglin.java` 283–297). 20% baby if spawnType ≠ STRUCTURE (206–208). Baby speed modifier +0.2 multiplied base (61–64, 286–290). Babies flee on hurt 100 ticks; adults retaliate (`PiglinAi.wasHurtBy` 576–585). Babies do **not** barter (`canAdmire` requires `isAdult`). Baby ride baby Hoglin up to 3 passengers (`Piglin.startRiding` 451–456; `MAX_PASSENGERS_ON_ONE_HOGLIN = 3`). Leather ignored by babies (`ItemTags.IGNORED_BY_PIGLIN_BABIES`) | Persistent NBT flag + AI branches. **Not** growth/genetics. Babies do not age in this Java | Identity + entity baby state already | None | **A** |
| Nether biome spawn | Biome JSON + `Piglin.checkPiglinSpawnRules` | Nether Wastes monster weight **15** min/max 4 (`nether_wastes.json` 100–105). Crimson Forest weight **5** min 3 max 4 (`crimson_forest.json` 94–98). **Warped Forest / Soul Sand Valley / Basalt Deltas: no piglin** in spawners. Predicate: block below is **not** `NETHER_WART_BLOCK` (`Piglin.java` 196–200). Magma excluded because magma `isValidSpawn` requires `fireImmune()` and Piglin is not. Spawn biome ≠ origin | Encounter lists | Identity sufficient | None | **A** |
| Bastion structure placement | Template pools / structure pieces | `data/minecraft/worldgen/template_pool/bastion/mobs/piglin.json` (melee/sword/crossbow/empty weights). Structure NBT under `data/minecraft/structure/bastion/mobs/*piglin*.nbt`. Encounter placement ≠ origin | Structure spawn | Identity sufficient | None | **A** |
| Open doors | `AbstractPiglin.applyOpenDoorsAbility` | GroundPathNavigation `setCanOpenDoors(true)` (`AbstractPiglin.java` 37–41). Shared parent helper, not Villager clade | AI navigation | Identity sufficient | None | **A** |
| Peaceful persistence | `Piglin.shouldDespawnInPeaceful` | Returns **false** (`Piglin.java` 221–223) vs `Monster` default **true** (`Monster.java` 55–57). Natural monster category still gated by server `spawnMonsters`. Not a biology field | Vanilla despawn | Identity sufficient | None | **A** |
| Guarded-block anger | `Block.playerWillDestroy` + container opens | If broken block is `#minecraft:guarded_by_piglins`, `PiglinAi.angerNearbyPiglins(player, false)` (`Block.java` 467–471; tag JSON gold/chests/ores/shulkers). Named openers: Barrel, EnderChest, ShulkerBox, MinecartChest, ChestBoat, ContainerEntity | Block/container gameplay | Identity sufficient | None | **A** |
| Creeper charged head | `Piglin.dropCustomDeathLoot` | `Items.PIGLIN_HEAD` if charged creeper (`Piglin.java` 157–163) | Loot special-case | Identity sufficient | None | **A** |
| Entity-type tags | **Piglin is not a member** of 1.21.1 `data/minecraft/tags/entity_type/*.json` | Jar scan: the only entity-type JSON containing the substring `piglin` is `#minecraft:zombies` listing **`zombified_piglin`**, not `piglin`. `#illager` / `#raiders` / `#undead` do **not** include piglin (`illager.json`, `raiders.json`, `undead.json`) | Tag ≠ clade. No piglin-specific entity-type tag exists | Identity sufficient | None | **A** |
| Item/block piglin tags | Tag JSON + named vanilla readers | `#piglin_loved`, `#piglin_food` (porkchop/cooked), `#piglin_repellents` (item+block), `#ignored_by_piglin_babies` (leather), `#guarded_by_piglins`. Consumers: `PiglinAi`, `PiglinSpecificSensor`, `Block.playerWillDestroy`, nether `distract_piglin` advancement (loved items) | Gameplay tags | Identity sufficient | None | **A** |
| Host Registry row | **ABSENT** | `hosts.json` living_biological / undead / unsuitable lists have no piglin | Participation missing | Fail-soft `organismKey = piglin` still representable | Eligibility false via null HostType. **Not** a missing-fact consumer | **B** |
| Gold / Nether-origin / Piglin-family / conversion Profile | No BioCraft owner | Would be new facts. Default is **no new field** | Existing identity already distinguishes Piglin | **None** | not **C** |

**No row is C.**

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` key `"piglin"` | **UNREGISTERED / ABSENT** | Not in `vanilla_hosts.living_biological`, `undead`, or `unsuitable.*` (`hosts.json` 1–53) | Participation missing. Do **not** register in this pass. Host Registry ≠ eligibility ≠ manifestation |
| `hosts.json` keys `"piglin_brute"` / `"zombified_piglin"` | **UNREGISTERED** | Same file. ZP destination report independently recorded the same absence | Narrow adjacency check only. Do not infer HostType from Minecraft tags or conversion |
| HostType / suitability for piglin | **N/A via registry** | `getHostType("piglin") == null` → `isSuitableForXenomorph` false (`MobHostRegistry.java` 46–71) | Unregistered ≠ biology. Inventory label `bio-organic` is **not** HostType `LIVING_BIOLOGICAL` |
| `HostConfigParser` | **LIVE** generic | Forbids biology keys in hosts.json (`HostConfigParser.java` 35–49) | Cannot smuggle gold/barter/conversion into Host Registry |
| `BiologicalProfileResolver` | **LIVE** generic | Unknown keys **fail-soft**: preserve `organismKey`, empty HostType / form / pack / source (`BiologicalProfileResolver.java` 35–56; test `unknownKeyPreservesOrganismKeyWithEmptyOptionals`) | `organismKey = piglin` is representable **without** registration |
| Resolver / registry unit test for key `piglin` | **TEST** absent | `MobHostRegistryTest` / `BiologicalProfileResolverTest` have pig, cow, unknown-key; **zero** `"piglin"` assertions under `src/test` | Generic path live; no Piglin-specific test |
| `DnaSampleFromOccupant` | **LIVE** generic | `minecraft:piglin` → `piglin` via `HostRegistryPaths.registryPath` even if unregistered (`DnaSampleFromOccupant.java` 50–59; `HostRegistryPaths.java` 16–21) | Identity/source transport only. Not a barter/gold/conversion consumer |
| `contributingSourceKey` production from this host | **LIVE machinery, origin blocked** | Model A optional source key exists on `CompiledBiologicalProfile`. Gestation/eligibility uses `HostEligibilityService` → null HostType fails (`HostEligibilityService.java` 19–31, 47–49) | Representation exists; origin production does not. Do not treat Piglin as a conversion-source clade with Hoglin/Villager |
| `HostEligibilityService` | **LIVE** generic | Null HostType → not suitable | Not a Piglin consumer |
| Piglin / AbstractPiglin / barter / gold entity JSON / AI / DNA under BioCraft | **ABSENT** | `biocraft-alien/src` Java+JSON: **no** `piglin` matches. Docs-only hits in dna.md / inventory / SPRINT (ZP/Zoglin context) | Vanilla remains behavior owner. Docs mentions are **PLANNING** inventory, not live consumers |
| `vanilla_compatibility.md` | **PLANNING** | Mentions ZP investigation only, not a Piglin consumer | Not a live Piglin manifestation consumer |
| DESIGN-BIO-MANIFEST-004 / Piglin / Gold / Nether / conversion Profile | **PLANNING / RESERVED** | Locked: 004 remains reserved. No such profile | Do not mint. Do not register this key |

---

## Tempting but rejected interpretations

| Tempting claim | Why rejected |
|----------------|--------------|
| AbstractPiglin is a biological clade | Shared Java parent. Piglin barters/hunts/babies; Brute `canHunt()==false`, golden axe, different brain (`PiglinBruteAi`). Shared parent ≠ clade |
| Piglin + Hoglin + Villager are a conversion-source clade | Conversion owners differ (AbstractPiglin vs Hoglin vs Zombie/Villager). Hunt/target/door-opening are separate AI. Conversion ≠ inheritance. Do **not** treat this as a conversion-source clade |
| Piglin Brute is the same organism / absorb brute AI | Distinct `EntityType.PIGLIN_BRUTE`. Adjacency is conversion only |
| Copy ZP `fireImmune` onto Piglin | Piglin builder has no `fireImmune()`. Magma spawn uses that flag. Destination-gained flag |
| Gold love / barter is a Biological Profile gold trait | `PiglinAi` + item tags + loot table. Equipment/currency ≠ capability field. No named BioCraft consumer |
| Gold armor neutrality is innate piglin biology | `makesPiglinsNeutral` is **item** default for gold `ArmorItem`. Player equipment gating |
| Crossbow is a Piglin biological ranged capability | `CrossbowAttackMob` + held item. Pillager also implements crossbow combat. Equipment ≠ capability |
| Hoglin hunting proves Piglin–Hoglin ancestry | `StartHuntingHoglin` targets `EntityType.HOGLIN`. Hunt ≠ clade |
| `#minecraft:zombies` / undead / zombified name proves Piglin is undead | Piglin is **not** in `#zombies` or `#undead`. ZP is. Tag ≠ clade |
| `#minecraft:illager` / raid faction | Piglin **absent** from `#illager` and `#raiders` |
| Nether spawn = Nether biological origin | Biome/structure encounter lists. Spawn biome ≠ origin. Warped/SSV/basalt have **no** piglin spawners |
| Host Registry absence = biological ineligibility field | Participation missing. Fail-soft identity still works. Unregistered ≠ BP field |
| Inventory `bio-organic` = HostType `LIVING_BIOLOGICAL` | Planning label only (`vanilla_organism_inventory.md` methodology). Not earned here |
| Baby piglin is a growth/AgeableMob lifecycle | Synched boolean; no aging. Not genetics |
| Conversion preserves Piglin biology on ZP | Brain/barter/inventory discarded; `fireImmune` gained; replacement via `convertTo` |
| Interesting Piglin AI earns C | Interesting behavior ≠ consumer. No named live BioCraft consumer needs a missing fact |
| Wiki “inventory items disappear on zombify” | Java **drops** the 8-slot inventory into the world before `super.finishConversion` |

---

## Potential biological relationships

For each: relationship / owner / biological input / existing composition / named consumer / result.

### 1. Piglin → Zombified Piglin conversion

- **Relationship:** Real 1.21.1 entity **replacement** when `!piglinSafe` for >300 ticks.
- **Owner:** `AbstractPiglin.customServerAiStep` / `finishConversion`; Piglin drops inventory first.
- **Biological input?** No. Replacement + copied entity/equipment state. Conversion ≠ inheritance.
- **Existing composition:** `organismKey=piglin` (source) and `organismKey=zombified_piglin` (destination). Optional `contributingSourceKey` is already the Model A slot if a later live host-contribution consumer existed.
- **Named consumer:** None live. Hosting/origin blocked for both keys (unregistered).
- **Result:** **A/B**. Not a conversion-source clade.

### 2. Shared AbstractPiglin with Piglin Brute

- **Relationship:** Java sibling; second conversion source to the same ZP type.
- **Owner:** `AbstractPiglin.finishConversion` (Brute does not override). Brute `playConvertedSound` is brute-specific (`PiglinBrute.java` 164–166).
- **Biological input?** No. Shared parent ≠ clade. Do not absorb brute AI/spawn.
- **Existing composition:** Distinct keys already.
- **Named consumer:** None.
- **Result:** **A**. Adjacency only.

### 3. Hoglin as hunt target / baby mount

- **Relationship:** Adult huntable Hoglin as attack target; baby Hoglin as ride vehicle.
- **Owner:** `StartHuntingHoglin`, `PiglinSpecificSensor`, `Piglin.startRiding`.
- **Biological input?** No. Targeting / passenger stack. Hoglin’s own `!piglinSafe` → Zoglin path is Hoglin-owned, not Piglin biology.
- **Existing composition:** Distinct `hoglin` key already (inventory unregistered; not this report).
- **Named consumer:** None.
- **Result:** **A**. Not a Hoglin/Piglin clade.

### 4. Fear of Zombified Piglin and Zoglin

- **Relationship:** Same Piglin predicate `isZombified` lists both types.
- **Owner:** `PiglinAi.isZombified` / `avoidZombified`.
- **Biological input?** No. AI grouping of two destination types. Not a shared undead/zombification trait on Piglin.
- **Existing composition:** Identity keys already distinguish all three.
- **Named consumer:** None.
- **Result:** **A**.

### 5. Villager-like doors / “trading”

- **Relationship:** Superficial: open doors; exchange items.
- **Owner:** AbstractPiglin door nav; PiglinAi barter loot table. Villager is a different type/profession system.
- **Biological input?** No. Closed leap.
- **Existing composition:** Distinct keys (`villager` is registered living; piglin is not).
- **Named consumer:** None for a trader clade.
- **Result:** **A**. Rejected as relationship.

### 6. Illager / raider / gold-crossbow kinship with Pillager

- **Relationship:** Both can hold crossbows; similar hitbox.
- **Owner:** Separate types. Piglin **not** in `#illager` / `#raiders`. Pillager is `CrossbowAttackMob` independently.
- **Biological input?** No.
- **Existing composition:** Distinct keys.
- **Named consumer:** None.
- **Result:** **A**. Out of illager scope except as negative control.

### 7. Host Registry / Model A contribution

- **Relationship:** If Piglin were a live host, Model A could use `organismKey` + optional `contributingSourceKey`.
- **Owner:** `hosts.json` / `BiologicalProfileResolver` / `HostEligibilityService`.
- **Biological input?** Participation is missing. No extra fact is required for fail-soft identity.
- **Existing composition:** Sufficient for identity projection.
- **Named consumer:** Generic resolver **LIVE**; origin **blocked**. No consumer asking for gold/barter/conversion fields.
- **Result:** **B** for identity; **not C**.

---

## Wiki orientation disagreements

Source: [minecraft.wiki/w/Piglin](https://minecraft.wiki/w/Piglin) (version-aggregated page, fetched 2026-09-11). Wiki is orientation only; **1.21.1 source wins**.

| Wiki orientation | 1.21.1 authority | Conclusion |
|------------------|------------------|------------|
| Spawn at light level 11 or less (Java) | `Piglin.checkPiglinSpawnRules` only rejects `NETHER_WART_BLOCK` below (`Piglin.java` 196–200). It does **not** call `Monster.isDarkEnoughToSpawn` / `checkMonsterSpawnRules`. Nether `monster_spawn_light_level` is **7** in `dimension_type/the_nether.json`, and that test is used by `Monster.isDarkEnoughToSpawn` (`Monster.java` 92–104) which Piglin’s registered predicate does not invoke | **Source.** Wiki light-11 is not this spawn predicate |
| Cannot spawn on magma (and nether wart) | Nether wart: explicit Piglin predicate. Magma: `Blocks.MAGMA_BLOCK` `isValidSpawn` iff `entityType.fireImmune()` (`Blocks.java` 4943); `SpawnPlacementTypes.ON_GROUND` requires `isValidSpawn` (31–32). Piglin is not fireImmune | **Mechanism matches magma**, via fireImmune flag, not a Piglin-only magma check |
| 15 s Overworld/End conversion | `CONVERSION_TIME = 300` ticks (`AbstractPiglin.java` 26, 88–90). `piglin_safe` false in overworld.json / the_end.json | **Matches** |
| Inventory items “disappear” on convert except equipped | `Piglin.finishConversion` **spawns** inventory contents in-world, then `convertTo(..., true)` copies equipment (`Piglin.java` 323–327; `Mob.convertTo` 1351–1360) | **Source: drop, not vanish** |
| Hunt start ~10% per piglin that sees a hoglin `[verify]` | Hunt start is `StartHuntingHoglin` (visible huntable adult Hoglin, not angry, not `HUNTED_RECENTLY`, adult, nearby adults also not recently hunted). **10% is victory dance** after Hoglin kill (`wantsToDance` 0.1F) | **Source.** Wiki hunt-chance is unverified and does not match this Java |
| Hunts baby hoglins (some secondary wikis) | Sensor huntable list is **adult** `canBeHunted()` Hoglin. Babies are `NEAREST_VISIBLE_BABY_HOGLIN` for riding | **Source: adults hunted; babies ridden** |
| Bastion-generated piglins `CannotHunt` | Flag exists as NBT. Java does not set it in `finalizeSpawn`. STRUCTURE path only skips baby/weapon randomization. This packet did not decode bastion `.nbt` entity data | **Unconfirmed in Java.** Do not invent. Hunt gate owner is still Piglin NBT/`canHunt()` |
| Peaceful: “stuck in eternal transformation” (Java) | Piglin `shouldDespawnInPeaceful()==false`. Conversion still the AbstractPiglin timer + `canLivingConvert` event (default not canceled). No Peaceful special-case in `Piglin.java` / `AbstractPiglin.java` | **Orientation.** Do not encode as a BP Peaceful trait |
| Not immune to fire/lava unlike ZP | Matches EntityType: Piglin no `fireImmune`; ZP has it | **Matches** |
| Babies never grow up | Not `AgeableMob`; baby is a boolean; no aging tick | **Matches** |
| Barter: gold ingot, ~6 s examine (Java) | `BARTERING_ITEM` gold ingot; `ADMIRE_DURATION = 119` ticks | **Matches** |
| Soul fire / ZP / Zoglin fear | Block tag + `isZombified` ZP\|\|Zoglin | **Matches** (soul campfire must be lit) |
| Open wooden doors like villagers | `setCanOpenDoors(true)` on AbstractPiglin | Superficial similarity; **not** Villager relationship |
| Later-version Peaceful natural spawn (wiki 26.2) | Out of `minecraft_version_range=[1.21.1,1.22)` | **Exclude** |
| Dried ghast in barter (wiki 1.21.6+) | 1.21.1 `piglin_bartering.json` has no dried ghast (soul_speed book/boots, fire res potions, iron/ender/string/quartz/etc.) | **Exclude later loot** |

---

## Final evidence conclusion

Piglin is a vanilla-owned Nether monster with barter/gold/hunt/fear/baby/conversion AI. Conversion is AbstractPiglin-owned replacement to a **different** EntityType that **gains** `fireImmune`. AbstractPiglin and Hoglin targeting are not clades. Piglin is **unregistered** in Host Registry. Fail-soft `organismKey=piglin` already represents identity. No named live BioCraft consumer needs a missing biological fact.

**Do not register Piglin as a conclusion of this investigation.** Generic fail-soft identity is **B**, not a missing-fact consumer.

New BP field earned: **NO**
Existing composition sufficient: **YES**
Named consumer exists: **NO**
Architectural escalation required: **NO**
