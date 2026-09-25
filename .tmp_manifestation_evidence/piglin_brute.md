TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Piglin Brute docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/piglin_brute.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.
Do not copy manifestations/piglin.md as brute biology.

# Piglin Brute — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register Piglin Brute as a conclusion of this investigation.**

**Subject lock:** Piglin Brute (`minecraft:piglin_brute`) only. `AbstractPiglin` is a **Java parent**, not a biological clade. Conversion to Zombified Piglin is entity **replacement**, not inheritance. Gold axe is spawn/pickup **equipment**, not a capability field. Bastion remnant placement is encounter, **not** organism-native origin. Adjacent `manifestations/piglin.md` was **verified** for shared-parent / conversion adjacency only; brute AI, spawn, equipment, and sensor set were **not** copied from that report.

Method (every behavior): existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied independently: shared parent ≠ clade; tag ≠ clade; conversion ≠ inheritance; spawn biome / bastion ≠ origin; gold axe ≠ capability; Host Registry ≠ eligibility; interesting behavior ≠ consumer.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey` (Model A Chestburster/Drone), optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`. **Default: no new BP field.**

---

## Subject

Piglin Brute (`minecraft:piglin_brute`) — identity, absent fire immunity, `AbstractPiglin`-owned Overworld/End conversion to Zombified Piglin, `canHunt()==false`, golden-axe equipment/pickup, HOME stationing, melee/nemesis targeting, Host Registry **absence**, and whether any of that earns a Biological Profile field or a named BioCraft consumer that needs a missing biological fact.

This packet does **not** investigate Piglin, Hoglin, Villager, Ghast, Ravager, Witch, Creeper, Bat, or Horse as organisms. Piglin is cited only as Java sibling / idle-interact type / conversion adjacency.

---

## Version

Minecraft Java **1.21.1** (`minecraft_version_range=[1.21.1,1.22)` in `biocraft-alien/gradle.properties`; `minecraft_version=1.21.1`). Mapped sources under `.tmp_mc_sources/` are authoritative for this packet. Wiki is orientation and disagreement discovery only; **source wins**.

Prior adjacency report `implementations/minecraft/AlienCraft/docs/design/biological/manifestations/piglin.md` was used only as a sibling-owner checklist. Every brute owner below was re-read from 1.21.1 mapped sources; Piglin conclusions were not copied as brute biology.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:piglin_brute` |
| `EntityType` | `EntityType.PIGLIN_BRUTE` — `EntityType.java` **545–553**: `register("piglin_brute", Builder.of(PiglinBrute::new, MobCategory.MONSTER).sized(0.6F, 1.95F).eyeHeight(1.79F).passengerAttachments(2.0125F).ridingOffset(-0.7F).clientTrackingRange(8))` |
| `fireImmune` | **ABSENT.** Builder does **not** call `.fireImmune()`. Builder field defaults `fireImmune = false` (`EntityType.Builder` **1254**; setter **1344–1346**). Same numeric size/eyeHeight as `EntityType.PIGLIN` (**536–544**) is registration duplication, not copied genetics |
| Class | `PiglinBrute extends AbstractPiglin` (`PiglinBrute.java` **31**). Does **not** implement `CrossbowAttackMob` or `InventoryCarrier` (those are Piglin). `AbstractPiglin extends Monster` (`AbstractPiglin.java` **22**) |
| Category | `MobCategory.MONSTER` |
| Summonable | Builder does **not** call `noSummon()`; `summon` defaults true (`EntityType.Builder` **1253**) |
| Spawn egg | `Items.PIGLIN_BRUTE_SPAWN_EGG` (`Items.java` **1454–1456**) — colors 5843472 / 16380836 |
| Attributes | `DefaultAttributes` binds `EntityType.PIGLIN_BRUTE` → `PiglinBrute.createAttributes()` (`DefaultAttributes.java` **136**). Stats (`PiglinBrute.java` **32–34, 65–67**): max health **50**, movement **0.35F**, attack damage **7.0**. Constructor `xpReward = 20` (**62**) |
| Spawn placement | **ABSENT.** `SpawnPlacements.java` registers `PIGLIN` (**129**) then `PILLAGER` (**130–132**). No `PIGLIN_BRUTE` row |
| Death loot JSON | `data/minecraft/loot_table/entities/piglin_brute.json` is **empty of pools** (type entity + `random_sequence` only). Datagen `VanillaEntityLoot.java` **1122**: `LootTable.lootTable()` empty |
| Host Registry | **UNREGISTERED / ABSENT as expected.** `hosts.json` `vanilla_hosts.living_biological` / `undead` / `unsuitable.*`, `modded_hosts`, `variant_mappings` contain no `"piglin_brute"` (file **1–53**). `MobHostRegistry.getHostType("piglin_brute")` → **null** (**46–48**). `isSuitableForXenomorph("piglin_brute")` → **false** because `hostType == null` (**68–71**) |
| Suitability | Unregistered → not suitable. Unregistered ≠ ineligible-as-biology ≠ BP field |

Adjacent vanilla types (identity / conversion adjacency only; **not** investigated here as organisms):

| Type | 1.21.1 fact | This packet’s use |
|------|-------------|-------------------|
| `EntityType.PIGLIN` | Same size/eyeHeight; no `fireImmune()`. `Piglin extends AbstractPiglin implements CrossbowAttackMob, InventoryCarrier`. `canHunt()` is Piglin-owned | Java sibling. Idle look/interact type. **Do not** copy barter/gold/hunt/baby as brute biology |
| `EntityType.ZOMBIFIED_PIGLIN` | Destination of `AbstractPiglin.convertTo`. Has `.fireImmune()` | Conversion destination identity. Destination `fireImmune` is **gained**, not brute |
| `EntityType.HOGLIN` | Hunt target of **Piglin**, not brute | Brute `canHunt()` returns **false** |

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP representation? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|-----------------------------|--------------------|-------|
| Identity / MONSTER / size 0.6×1.95 / eyeHeight 1.79 / no `fireImmune` | `EntityType.PIGLIN_BRUTE` | `EntityType.java` **545–553** | Identity only | `organismKey = piglin_brute` (fail-soft if unregistered) | Generic `BiologicalProfileResolver` | **B** |
| Java parent `AbstractPiglin` | class hierarchy | `PiglinBrute extends AbstractPiglin` (`PiglinBrute.java` **31**). Sibling `Piglin` also extends it. Parent owns conversion, door-opening, fire path malus (`AbstractPiglin.java` **33–34, 37–41, 80–104**) | Implementation reuse. **Closed leap:** AbstractPiglin ≠ clade | Distinct registry ids `piglin` / `piglin_brute` | None for clade | **A** |
| `canHunt() == false` | `PiglinBrute` override | `PiglinBrute.java` **97–100**. Piglin hunt broadcast skips adults that `!canHunt()` (`PiglinAi.broadcastAngerTarget` **667–672**) | Hunt-gate override, not Hoglin ancestry | Distinct key already | None | **A** |
| Conversion trigger / replace | `AbstractPiglin.customServerAiStep` / `finishConversion` | `isConverting()` = `!dimensionType().piglinSafe()` && !immune && !noAI (`AbstractPiglin.java` **94–96**). `CONVERSION_TIME = 300` (**26**). `timeInOverworld > 300` then `convertTo(ZOMBIFIED_PIGLIN, true)` (**88–104**). Nether `piglin_safe: true` (`the_nether.json` **17**); Overworld/End **false** (`overworld.json` **20**; `the_end.json` **21**). Brute does **not** override `finishConversion` | Replacement, not genetics. **Closed leap:** conversion ≠ inheritance | Distinct keys `piglin_brute` vs `zombified_piglin` | **None** live needing a conversion trait | **A/B** |
| Converted sound | `PiglinBrute.playConvertedSound` | `SoundEvents.PIGLIN_BRUTE_CONVERTED_TO_ZOMBIFIED` (`PiglinBrute.java` **163–166**) | Presentation | Identity sufficient | None | **A** |
| `convertTo` transferred vs discarded | `Mob.convertTo` | `Mob.java` **1330–1371**: copy position, baby, no-AI, name, persistence, invulnerability, optional equipment; **discard** source. Confusion 200 on **new** ZP (`AbstractPiglin.java` **101**). Brute has no 8-slot Piglin inventory to dump | Copied equipment = entity state | Optional `contributingSourceKey` is Model A, **not** vanilla convertTo | Gestation source write is Chestburster/Drone, not this replacement | **A/B** |
| Immune-to-zombification NBT | `AbstractPiglin` synched data | `DATA_IMMUNE_TO_ZOMBIFICATION` default **false** (`AbstractPiglin.java` **23–25, 45–57**). Saved `"IsImmuneToZombification"` / `"TimeInOverworld"` (**60–77**) | Per-instance suppress flag | Entity NBT, not BP | None | **A** |
| Reverse conversion | **Absent** | No ZP→brute `convertTo` in this Java | N/A | Distinct keys | None | **A** |
| Default golden axe | `populateDefaultEquipmentSlots` | Always `Items.GOLDEN_AXE` in MAINHAND (`PiglinBrute.java` **77–80**). Called from `finalizeSpawn` (**71–74**) | Spawn equipment. **Closed leap:** gold axe ≠ capability | Identity sufficient | None | **A** |
| Pickup restriction | `wantsToPickUp` | Only `Items.GOLDEN_AXE` then `super.wantsToPickUp`; all other stacks **false** (`PiglinBrute.java` **102–105**). Parent `setCanPickUpLoot(true)` (`AbstractPiglin.java` **31**) | Item filter, not gold metabolism | Identity sufficient | None | **A** |
| Brain / activities | `PiglinBruteAi` | CORE / IDLE / FIGHT only (`PiglinBruteAi.java` **45–92**). No admire, barter, celebrate, hunt, avoid-repellent, or avoid-zombified activities | Vanilla brain owner | Identity sufficient | None | **A** |
| Targeting | `PiglinBruteAi.findNearestValidAttackTarget` | Order: `ANGRY_AT` (if attackable ignoring LOS) → `NEAREST_VISIBLE_ATTACKABLE_PLAYER` within **12.0** → `NEAREST_VISIBLE_NEMESIS` (`PiglinBruteAi.java` **135–147**). Anger duration **600** ticks (**34, 155–157**). Melee cooldown **20** (`MeleeAttack.create(20)` **88**) | Combat AI. Player targeting is **not** gold-gated (no `NEAREST_TARGETABLE_PLAYER_NOT_WEARING_GOLD` memory on this brain) | Identity sufficient | None | **A** |
| Nemesis (Wither / Wither Skeleton) | `PiglinBruteSpecificSensor` | Closest visible `WitherSkeleton \|\| WitherBoss` → `NEAREST_VISIBLE_NEMESIS` (`PiglinBruteSpecificSensor.java` **33–42**). Sensor registered `SensorType.PIGLIN_BRUTE_SPECIFIC_SENSOR` (`SensorType.java` **34–36**; `PiglinBrute.java` **35–36**) | Sensor targeting. Brute is **not** in `#wither_friends` (`wither_friends.json` is `#undead` only) | Identity sufficient | None | **A** |
| Hurt retaliation | `PiglinBruteAi.wasHurtBy` → `PiglinAi.maybeRetaliate` | If attacker is **not** `AbstractPiglin`, call `PiglinAi.maybeRetaliate` (`PiglinBruteAi.java` **149–153**; `PiglinAi.java` **590–604**) | Shared helper on `AbstractPiglin` argument, not clade | Distinct keys | None | **A** |
| HOME stationing | `PiglinBruteAi.initMemories` | On `finalizeSpawn`, `HOME = GlobalPos` of spawn block (`PiglinBruteAi.java` **55–58**; `PiglinBrute.java` **71–72**). Idle: `StrollToPoi` HOME 0.6F, close 2, too-far 100; `StrollAroundPoi` radius 5 (**41–43, 112–113**) | Structure/spawn stationing. **Closed leap:** bastion ≠ origin | Not an origin field | None | **A** |
| Idle social look/interact | `PiglinBruteAi` idle RunOne | Look at PLAYER / PIGLIN / PIGLIN_BRUTE / any; `InteractWith` PIGLIN and PIGLIN_BRUTE (`PiglinBruteAi.java` **94–116**) | Idle AI type filters. Shared look ≠ clade | Distinct keys already | None | **A** |
| Open doors / fire path malus | `AbstractPiglin` ctor | `setCanOpenDoors(true)` (**37–41**). `DANGER_FIRE` 16 / `DAMAGE_FIRE` -1 (**33–34**) | Navigation helpers. Path malus ≠ `fireImmune` | Identity sufficient | None | **A** |
| Arm pose | `getArmPose` | Melee attacking pose iff aggressive **and** holding `TieredItem` (`PiglinBrute.java` **117–120**; `AbstractPiglin.isHoldingMeleeWeapon` **118–120**) | Presentation | Identity sufficient | None | **A** |
| Sounds | brute-specific events | Ambient/hurt/death/step/angry/converted (`PiglinBrute.java` **139–166**; `SoundEvents.java` **1092–1097**) | Presentation | Identity sufficient | None | **A** |
| Natural biome spawn | **ABSENT** from extracted biome spawners | `crimson_forest.json` monster list: ZP, hoglin, **piglin** — no brute (**81–99**). `nether_wastes.json` has **piglin** weight 15 — no brute (**100–105**). `SpawnPlacements` has no brute row | Encounter lists. Spawn biome ≠ origin | Not needed | None | **A** |
| Bastion structure placement | Structure NBT | Extracted `data/minecraft/structure/bastion/mobs/melee_piglin.nbt` contains `piglin_brute`. Template pools `bastion/mobs/piglin.json` / `piglin_melee.json` name `melee_piglin` pieces, not a brute-typed pool element | Structure encounter. **Closed leap:** bastion ≠ origin | Not an origin field | None | **A** |
| Entity loot | empty table | `entities/piglin_brute.json` empty pools; equipment still drops via `Mob.convertTo` / vanilla equipment | Drops ≠ anatomy | Not needed | None | **A** |
| Piglin-head visibility | `LivingEntity` | `PIGLIN_BRUTE` looking entity + worn `PIGLIN_HEAD` halves visibility like Piglin (`LivingEntity.java` **886–890**). Cosmetic; brute does **not** drop a brute head in this Java | Presentation | Identity sufficient | None | **A** |
| Parrot imitate | `Parrot.MOB_SOUND_MAP` | `EntityType.PIGLIN_BRUTE → PARROT_IMITATE_PIGLIN_BRUTE` (`Parrot.java` **97**) | Sound table | Identity sufficient | None | **A** |
| Advancements | kill-mob lists | `kill_a_mob.json` / `kill_all_mobs.json` include `minecraft:piglin_brute` | UX checklist | Identity sufficient | None | **A** |
| Entity-type tags | **Absent** from extracted undead/zombie/illager/raider tags | `#undead` / `#zombies` / `#illager` / `#raiders` / `#fall_damage_immune` / `#sensitive_to_smite` (aliases `#undead`) / `#inverted_healing_and_harm` / `#ignores_poison_and_regen` / `#wither_friends` / `#no_anger_from_wind_charge` do **not** list `piglin_brute`. `#zombies` lists `zombified_piglin` and `zoglin`, not brute | Tag ≠ clade | Distinct key vs piglin / ZP | None | **A** |
| Host Registry participation | **ABSENT** | `hosts.json` has no `piglin_brute` | Participation missing. Unregistered ≠ biology | Fail-soft `organismKey`; HostType empty | `HostEligibilityService.isValidFacehuggerHost` false via null HostType. Origin blocked | **B** |

**No row is C.**

Behaviors owned by **Piglin**, not brute (negative controls; do not copy as brute biology):

| Piglin-owned | Why not brute |
|--------------|---------------|
| Barter / gold ingot admire | `PiglinAi.mobInteract` / `canAdmire` take `Piglin`, not `AbstractPiglin` (`PiglinAi.java` **540–555**). Brute brain has no admire activity |
| `#piglin_loved` / gold-armor neutrality | `PiglinSpecificSensor` fills `NEAREST_TARGETABLE_PLAYER_NOT_WEARING_GOLD`. Brute sensor list uses `PIGLIN_BRUTE_SPECIFIC_SENSOR` instead (`PiglinBrute.java` **35–36**) |
| Hoglin hunting / baby ride | Gated by `canHunt()`; brute returns false. No `StartHuntingHoglin` in `PiglinBruteAi` |
| Soul-fire / `#piglin_repellents` avoid | `PiglinSpecificSensor.findNearestRepellent`. Brute sensor does not write `NEAREST_REPELLENT` |
| Fear ZP / Zoglin (`isZombified`) | `PiglinAi` avoid-zombified. Brute fight/idle has no avoid activity |
| Baby state / 20% baby spawn | Piglin synched baby + `finalizeSpawn`. Brute `finalizeSpawn` only inits HOME + axe (`PiglinBrute.java` **70–75**) |
| 8-slot inventory dump on convert | `Piglin.finishConversion`. Brute does not override |

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` key `"piglin_brute"` | **UNREGISTERED / ABSENT** (expected) | Not in `vanilla_hosts.living_biological`, `undead`, or `unsuitable.*` (`hosts.json` **1–53**). Adjacent keys `"piglin"` / `"zombified_piglin"` also absent | Do **not** register in this pass. Participation ≠ eligibility ≠ manifestation |
| `BiologicalProfileResolver` | **LIVE** generic | `BiologicalProfileResolver.java` **35–56**: lowercased `organismKey`; `MobHostRegistry.getHostType`; unknown keys fail-soft (class comment **23–24**). Test `unknownKeyPreservesOrganismKeyWithEmptyOptionals` (`BiologicalProfileResolverTest.java` **47–55**) | `piglin_brute` is representable as identity without registration. No brute branch |
| `CompiledBiologicalProfile` | **LIVE** composition type | Fields: organismKey, HostType, xenomorphFormKey, hostEffectProfileId, behaviorTypeKey, contributingSourceKey (`CompiledBiologicalProfile.java` **23–28**) | Sparse identity + refs. Not a brute dossier. No new field used or earned |
| `HostEligibilityService` | **LIVE** generic; **origin blocked** for this key | `isSuitableForXenomorph(String)` → `MobHostRegistry.isSuitableForXenomorph` (**19–21**). Entity path encode-id → `HostRegistryPaths.registryPath` → same (**23–31**). `isValidFacehuggerHost` requires that suitability (**33–44**). Null HostType → **false** (`MobHostRegistry.java` **68–71**) | Not a brute-specific consumer. Facehugger/gestation origin cannot start from an unregistered brute |
| `GestationManager.writeContributingSource` | **LIVE machinery, origin blocked** | `GestationManager.java` **164–175**: if offspring `ContributingSourcePort.supports`, encode host id → `HostRegistryPaths.registryPath` → `setContributingSourceKey`. Called from `spawnChestburster` (**151**) | Representation exists for Model A xenomorphs. A brute cannot originate a **production** contribution because eligibility fails first. Do not treat that as a missing brute BP field |
| `HostConfigParser` | **LIVE** generic | Forbids biology keys in hosts.json (`HostConfigParser.java` **35–49**) | Cannot smuggle axe/conversion/bastion into Host Registry |
| `HostRegistryPaths` | **LIVE** generic | `minecraft:piglin_brute` → `piglin_brute` (`HostRegistryPaths.java` **16–21**) | Identity/source transport only |
| Analyzer / Model A | **LIVE** generic | Resolver accepts optional `contributingSourceKey` (**35–56**). No brute-specific analysis | If a vial were keyed `piglin_brute`, Analyzer would project fail-soft identity |
| Piglin Brute entity JSON / AI / DNA under BioCraft | **ABSENT** (not required for this packet’s conclusion; Host Registry + resolver already classify origin) | Vanilla remains gameplay owner | Docs mentions of Piglin are adjacency, not live brute consumers |
| Resolver unit test for key `piglin_brute` | **TEST** absent | Generic unknown-key test exists; no `"piglin_brute"` assertion | Expected UNREGISTERED; fail-soft proven for unknown keys |

Consumer classification for this organism:

| Candidate | Classification |
|-----------|----------------|
| `BiologicalProfileResolver` | **LIVE** generic fail-soft (not brute-specific) |
| `CompiledBiologicalProfile` | **LIVE** generic composition |
| `HostEligibilityService` | **LIVE** generic; **origin blocked** (null HostType) |
| `GestationManager.writeContributingSource` | **LIVE machinery, origin blocked** |
| Host Registry / `hosts.json` | **ABSENT** participation |
| Named missing-fact consumer | **NONE** |

---

## Tempting but rejected interpretations

| Tempting claim | Why rejected |
|----------------|--------------|
| AbstractPiglin is a biological clade | Shared Java parent. Piglin barters/hunts/babies; brute `canHunt()==false`, golden axe only, different sensor/brain. **AbstractPiglin ≠ clade** |
| Piglin Brute is the same organism as Piglin / “stronger piglin” | Distinct `EntityType.PIGLIN_BRUTE`. Same hitbox literals ≠ genetics. Do not copy `manifestations/piglin.md` as brute biology |
| Conversion preserves brute biology on ZP / ancestry | `convertTo` replacement. Brain discarded; `fireImmune` gained on destination. **Conversion ≠ inheritance** |
| Copy ZP `fireImmune` onto brute | Brute builder has no `.fireImmune()` |
| Gold axe is a Biological Profile gold / combat capability | `populateDefaultEquipmentSlots` + pickup filter. **Gold axe ≠ capability** |
| Gold-armor neutrality / barter apply to brutes | Those are `PiglinAi` / `PiglinSpecificSensor`. Brute player targeting is `NEAREST_VISIBLE_ATTACKABLE_PLAYER`, not gold-gated |
| Hoglin hunting / piglin–hoglin ancestry | `canHunt()` false; no hunt activity |
| Soul-fire fear / `#piglin_repellents` as brute biology | Brute sensor does not write repellent memory |
| Bastion remnant = Nether / bastion biological origin | Structure NBT + HOME at spawn block. **Bastion ≠ origin** |
| Shared `maybeRetaliate` / idle interact with Piglin proves one organism | Shared helper + type filters. Shared parent ≠ clade |
| `#minecraft:zombies` / undead / zombified name | Brute **absent** from `#zombies` and `#undead`. ZP is a member. Tag ≠ clade |
| `#illager` / raid / pillager kinship | Brute **absent** from `#illager` and `#raiders` |
| Host Registry absence = biological ineligibility field | Participation missing. Fail-soft identity still works. Unregistered ≠ BP field |
| Inventory planning label = HostType | Planning inventory is not this packet’s owner and is not edited here |
| Interesting brute AI earns C | Interesting behavior ≠ consumer. No named live BioCraft consumer needs a missing fact |

---

## Potential biological relationships

For each: relationship / owner / biological input / existing composition / named consumer / result.

### 1. Piglin Brute → Zombified Piglin conversion

- **Relationship:** Real 1.21.1 entity **replacement** when `!piglinSafe` for >300 ticks.
- **Owner:** `AbstractPiglin.customServerAiStep` / `finishConversion`. Brute does not override; brute-specific converted sound only.
- **Biological input?** No. Replacement + copied entity/equipment state. Conversion ≠ inheritance.
- **Existing composition:** `organismKey=piglin_brute` (source) and `organismKey=zombified_piglin` (destination). Optional `contributingSourceKey` is already the Model A slot if a later live host-contribution consumer existed.
- **Named consumer:** None live. Hosting/origin blocked (unregistered).
- **Result:** **A/B**. Not a conversion-source clade with Piglin/Hoglin/Villager.

### 2. Shared AbstractPiglin with Piglin

- **Relationship:** Java sibling; second conversion source to the same ZP type.
- **Owner:** Shared parent methods. Distinct brains (`PiglinBruteAi` vs `PiglinAi`).
- **Biological input?** No. AbstractPiglin ≠ clade. Do not absorb Piglin barter/gold/hunt/baby.
- **Existing composition:** Distinct keys already.
- **Named consumer:** None.
- **Result:** **A**. Adjacency only. Verified against `manifestations/piglin.md`; not copied as brute biology.

### 3. Hoglin as hunt target

- **Relationship:** **Absent** for brute. Piglin hunt is gated by `canHunt()`.
- **Owner:** Piglin AI. Brute override returns false.
- **Biological input?** No. Hunt-gate is a boolean override, not Hoglin genetics.
- **Existing composition:** Distinct `hoglin` / `piglin_brute` keys.
- **Named consumer:** None.
- **Result:** **A**. Negative control.

### 4. Wither / Wither Skeleton nemesis

- **Relationship:** Sensor closest-visible wither-family as attack fallback.
- **Owner:** `PiglinBruteSpecificSensor`.
- **Biological input?** No. Combat targeting. Brute is not `#wither_friends`.
- **Existing composition:** Identity sufficient.
- **Named consumer:** None.
- **Result:** **A**.

### 5. Bastion HOME stationing

- **Relationship:** Spawn-position HOME memory; melee_piglin structure piece can contain brute.
- **Owner:** `PiglinBruteAi.initMemories` + structure NBT.
- **Biological input?** No. Bastion ≠ origin.
- **Existing composition:** Not an origin field.
- **Named consumer:** None.
- **Result:** **A**.

### 6. Host Registry / Model A contribution

- **Relationship:** If brute were a live host, Model A could use `organismKey` + optional `contributingSourceKey`.
- **Owner:** `hosts.json` / `BiologicalProfileResolver` / `HostEligibilityService` / `GestationManager.writeContributingSource`.
- **Biological input?** Participation is missing. No extra fact is required for fail-soft identity.
- **Existing composition:** Sufficient for identity projection.
- **Named consumer:** Resolver **LIVE**; eligibility/gestation origin **blocked**. No consumer asking for axe/conversion/bastion fields.
- **Result:** **B** for identity; **not C**.

---

## Wiki orientation disagreements

Wiki is orientation only; **1.21.1 source wins**. Common aggregated claims vs this Java/data:

| Wiki orientation | 1.21.1 authority | Conclusion |
|------------------|------------------|------------|
| Same species / “elite piglin” as Piglin | Distinct `EntityType`; different brain, sensor, `canHunt()`, equipment, XP, health | **Source: distinct organism key.** Do not copy Piglin biology |
| Converts after 15s in the Overworld | `CONVERSION_TIME = 300` ticks; `!piglinSafe()`; End also converts | **Matches timer**; gate is dimension `piglin_safe`, not Overworld-named |
| Immune to zombification | Default `DATA_IMMUNE_TO_ZOMBIFICATION` is **false**. Same parent conversion as Piglin unless NBT immune | **Source: converts** unless flagged |
| Does not barter; always hostile even if player wears gold | No admire/barter in `PiglinBruteAi`. Player memory is `NEAREST_VISIBLE_ATTACKABLE_PLAYER`, not gold-gated | **Matches** |
| Does not hunt hoglins | `canHunt()` returns false | **Matches** |
| Spawns in bastion remnants; not in open Nether biomes | No `SpawnPlacements` row; crimson forest / nether wastes spawners list `piglin` not brute; `melee_piglin.nbt` contains `piglin_brute` | **Matches structure-not-biome.** Bastion ≠ origin |
| Always golden axe | `populateDefaultEquipmentSlots` always `GOLDEN_AXE` | **Matches.** Equipment ≠ capability |
| Drops nothing unique | Empty entity loot table; equipment still present | **Matches table**; do not treat empty pools as “no drops” of held items |
| Later-version changes | Out of `minecraft_version_range=[1.21.1,1.22)` | **Exclude** |

---

## Final stop gate

Piglin Brute is a vanilla-owned Nether monster with melee/HOME/nemesis AI and `AbstractPiglin`-owned replacement to a **different** EntityType that **gains** `fireImmune`. AbstractPiglin is not a clade. Conversion is not inheritance. Gold axe is not a capability. Bastion is not origin. The key is **unregistered** in Host Registry as expected. Fail-soft `organismKey=piglin_brute` already represents identity. No named live BioCraft consumer needs a missing biological fact.

**Do not register Piglin Brute as a conclusion of this investigation.** Generic fail-soft identity is **B**, not a missing-fact consumer.

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** |
| Named consumer exists | **NO** |
| Architectural escalation required | **NO** |

**Stop.**
