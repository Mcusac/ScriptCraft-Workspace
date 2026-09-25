# TEMPORARY EVIDENCE PACKET — NOT PROJECT SSOT

**Status:** Temporary Evoker-branch investigation artifact. **Not** Biological Profile SSOT. **Not** a canonical manifestation report. **Not** permission to mint Feature IDs, edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or DESIGN-BIO-MANIFEST-004.

**Do not** promote this file into `manifestations/evoker.md` or any living hub without a later authorized pass.

**Subject lock:** Evoker only. SpellcasterIllager / AbstractIllager / Raider / tags / raid / patrols / village hostility / shared equipment / shared AI / faction look are **closed leaps** (≠ clade, ancestry, or BP field). EvokerFangs is **MISC**, not a fourth organism. Vex is a **separate** organism investigation candidate; creation ≠ reproduction; do not promote Vex, Allay, or a “spiritual/summoned” category from this packet. Do not write Pillager, Vindicator, Illusioner, Ravager, Witch, or Sheep reports.

**Isolation:** Authoritative 1.21.1 mapped sources, live BioCraft, locked context, and this packet’s own reads only. Other investigators’ conclusions were not used as evidence.

---

## Subject

Evoker (`minecraft:evoker`) — spellcasting / fangs / Vex creation / sheep-coloring / raid membership vs organism-native behavior; whether any of that earns a Biological Profile field or named BioCraft consumer.

## Version

Minecraft Java **1.21.1** (`minecraft_version_range=[1.21.1,1.22)` in `biocraft-alien/gradle.properties`). Mapped NeoForge **21.1.208** sources jar is authoritative (`biocraft-alien/build/moddev/artifacts/neoforge-21.1.208-sources.jar` and client-extra resources). Wiki is orientation and disagreement discovery only; **source wins**.

Temporary source cache (not SSOT): `.tmp_mc_sources/`.

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:evoker` |
| `EntityType` | `EntityType.EVOKER` — `EntityType.java` 335–338: `Builder.of(Evoker::new, MobCategory.MONSTER).sized(0.6F, 1.95F).passengerAttachments(2.0F).ridingOffset(-0.6F).clientTrackingRange(8)` |
| Class | `Evoker extends SpellcasterIllager` (`Evoker.java` 43). `SpellcasterIllager extends AbstractIllager` (`SpellcasterIllager.java` 20). `AbstractIllager extends Raider` (`AbstractIllager.java` 12). `Raider extends PatrollingMonster` (`Raider.java` 41) |
| Category | `MobCategory.MONSTER` |
| Fire / lava | **No** `fireImmune()` on EVOKER. Contrast: `EntityType.VEX` **has** `fireImmune()` (`EntityType.java` 700–708) — Vex EntityType flag, not Evoker biology |
| Summonable | EVOKER builder does **not** call `noSummon()`; `EntityType.canSummon()` (`EntityType.java` 1034–1036) |
| Attributes | `DefaultAttributes` → `Evoker.createAttributes()` (`DefaultAttributes.java` 112): movement 0.5, follow range 12.0, max health 24.0 (`Evoker.java` 70–72). `xpReward = 10` in constructor (48–50) |
| Spawn placement | `SpawnPlacements.register(EntityType.EVOKER, NO_RESTRICTIONS, MOTION_BLOCKING_NO_LEAVES, Monster::checkMonsterSpawnRules)` (`SpawnPlacements.java` 163). **No** 1.21.1 biome JSON under `data/minecraft/worldgen/biome/` contains `evoker` or `vex` (full scan of client-extra jar) |
| Spawn egg | `Items.EVOKER_SPAWN_EGG` (`Items.java` 1421) |
| Host Registry | **UNREGISTERED.** `hosts.json` has no `"evoker"`. `MobHostRegistry.getHostType("evoker")` → `null`. `isSuitableForXenomorph("evoker")` → **false** (`MobHostRegistry.java` 46–48, 68–71) |
| Inventory row | Planning inventory: `evoker` / bio-organic / unregistered / pending / undetermined. Inventory category ≠ HostType ≠ biology. This packet does **not** update that row |
| Suitability | Unregistered → not suitable. Unregistered ≠ ineligible-as-biology ≠ BP field |

Adjacent vanilla types (identity only; **not** investigated here as organisms):

| Type | 1.21.1 fact | This packet’s use |
|------|-------------|-------------------|
| `EntityType.EVOKER_FANGS` | `MobCategory.MISC`, sized 0.5×0.8, tracking 6, updateInterval 2 (`EntityType.java` 339–341). Class `EvokerFangs extends Entity implements TraceableEntity` | MISC combat entity, **not** a fourth organism report |
| `EntityType.VEX` | `MobCategory.MONSTER`, `fireImmune()`, sized 0.4×0.8 (`EntityType.java` 700–708). `Vex extends Monster implements TraceableEntity` | Creation-test destination only. Inventory `other` / HostType `SPIRITUAL` already registered. Do not reopen as Evoker biology |
| `Illusioner` | `Illusioner extends SpellcasterIllager implements RangedAttackMob` (`Illusioner.java` 40) | Java-parent sibling only. Closed leap. No Illusioner report |

---

## Vex creation test (creation ≠ reproduction)

| Record | 1.21.1 fact |
|--------|-------------|
| 1. Exact vanilla owner | **`Evoker.EvokerSummonSpellGoal.performSpellCasting`** (`Evoker.java` 266–288). Goal registered at priority 4 (`Evoker.java` 58). Uses `SpellcasterIllager.IllagerSpell.SUMMON_VEX` (296–298). **Not** Vex-owned. **Not** Raid-owned. **Not** SpellcasterIllager-generic (Illusioner does not create Vex) |
| 2. Trigger | `EvokerSummonSpellGoal.canUse` (`Evoker.java` 245–254): `super.canUse()` **requires a living combat target** (`SpellcasterIllager.SpellcasterUseSpellGoal.canUse`, 183–191) **and** nearby `Vex` count gate: `random.nextInt(8) + 1 >` count of Vex within inflate(16). Casting time 100, interval 340 (256–264). Prepare sound `EVOKER_PREPARE_SUMMON` |
| 3. Create / replace / attach | **Create + runtime attach.** `EntityType.VEX.create` → `moveTo` → `finalizeSpawn(..., MobSpawnType.MOB_SUMMONED, null)` → `vex.setOwner(Evoker.this)` → `setBoundOrigin(blockpos)` → `setLimitedLife(20 * (30 + random.nextInt(90)))` → optional scoreboard team copy → `addFreshEntityWithPassengers`. Evoker is **not** replaced, converted, or discarded. Up to **3** new Vex per cast (loop `i < 3`, 271). Not in-place mutate |
| 4. Transferred properties | **Copied/attached:** runtime `owner` pointer; bound origin at spawn pos; limited life 600–2380 ticks; scoreboard team if Evoker has one. **Not copied:** health, Evoker NBT/`SpellTicks`, Evoker equipment (Evoker has none by default), genetics, raid wave, identity. Vex `finalizeSpawn` then `populateDefaultEquipmentSlots` gives **its own** iron sword with 0 drop chance (`Vex.java` 217–228) |
| 5. Independent Vex existence / creation path | **Type is independently instantiable.** `EntityType.VEX` does not `noSummon()`; `Items.VEX_SPAWN_EGG` (`Items.java` 1507); `SpawnPlacements.register(EntityType.VEX, ..., Monster::checkMonsterSpawnRules)` (`SpawnPlacements.java` 171); `Vex.finalizeSpawn` / iron sword **do not require** an owner. **Survival-world natural/structure/raid spawn of Vex was not found:** no biome JSON lists `vex`; woodland mansion markers spawn Evoker / Vindicator / Allay only (`WoodlandMansionPieces.java` 1323–1338); `Raid.RaiderType` has no VEX (`Raid.java` 837–842); `#minecraft:raiders` has no vex. Spawn-egg availability is **not** the conceptual test; `/summon` and `EntityType.VEX.create` without `setOwner` are independent placement paths. Independent existence **does not disprove** Evoker→Vex summoning; it **prevents** treating Evoker creation as sufficient evidence of biological origin |
| Owner persistence | **Owner is not written to Vex NBT.** `Vex.addAdditionalSaveData` writes BoundX/Y/Z and optional `LifeTicks` only (`Vex.java` 135–146). `readAdditionalSaveData` does not restore owner (112–121). Dimension `restoreFrom` copies owner if source is Vex (127–132). Contrast: `EvokerFangs` **does** persist `Owner` UUID (`EvokerFangs.java` 68–80). Runtime owner ≠ persistent lineage |
| Limited life | Only if `setLimitedLife` was called. Tick: `hasLimitedLife && --limitedLifeTicks <= 0` → reset to 20 and `hurt(starve, 1.0F)` (`Vex.java` 79–82). Independent Vex without that call has **no** limited-life starve |
| 6. Classify | **Summoning / entity creation.** Not replace. Not attach-as-part (Vex is a full `Monster`). **Not** lifecycle phase of Evoker. **Not** reproduction (no `AgeableMob` / offspring factory; creates new typed entities). **Not** ancestry. **Not** genetics. Creation alone is not genetics |
| 7. Alliance after create | `Evoker.isAlliedTo`: if other is `Vex`, allied iff Evoker is allied to `vex.getOwner()` (`Evoker.java` 106–116). Runtime owner pointer, not a clade |

---

## Sheep-coloring (not genetics)

| Record | 1.21.1 fact |
|--------|-------------|
| Owner | **`Evoker.EvokerWololoSpellGoal.performSpellCasting`** (`Evoker.java` 340–345). Goal priority 6 (`Evoker.java` 60). Spell id `WOLOLO` (368–370) |
| Trigger | Overrides `canUse` (`Evoker.java` 307–326): **no combat target**; not already casting; cooldown; `EventHooks.canEntityGrief(level, evoker)` (`EventHooks.java` 752–757` → `GameRules.RULE_MOBGRIEFING` if no event override); nearby `Sheep` with `getColor() == DyeColor.BLUE` in inflate(16, 4, 16) |
| Target | Existing `Sheep` instance (not a new entity) |
| Resulting change | `sheep.setColor(DyeColor.RED)` (`Evoker.java` 343; `Sheep.setColor` 305–308) |
| Persistent biological state? | **Persistent wool-color NBT on Sheep**, not new genetics. `Sheep.addAdditionalSaveData` / `readAdditionalSaveData` store `Color` byte (`Sheep.java` 265, 275). Same field used by player dye (`DyeItem.interactLivingEntity` 30–38), random spawn color (`Sheep.finalizeSpawn` 363), and breeding mix (`getBreedOffspring` / `getOffspringColor` 342–382). Wololo is one **mutator** of Sheep color state. **Not** a sheep-coloring trait on Evoker BP. **Not** genetics |
| Independent coloring path | **Yes:** `DyeItem` → `sheep.setColor(this.dyeColor)`. Independent path does not disprove Evoker wololo; it prevents wololo from being Evoker genetics or a unique biological color trait |

---

## Combat test (spellcasting / fangs vs equipment vs generic AI)

| Test | Result |
|------|--------|
| Default equipment | Evoker **does not** override `populateDefaultEquipmentSlots`. No totem in hand. Totem is **loot** (`data/minecraft/loot_table/entities/evoker.json` first pool: guaranteed `totem_of_undying`). Raid captain banner can appear via inherited `PatrollingMonster.finalizeSpawn` head slot (`PatrollingMonster.java` 79–82) — raid/patrol **equipment**, not spellcasting |
| `applyRaidBuffs` | **Empty** on Evoker (`Evoker.java` 147–149). Raid does not enchant Evoker weapons because there are none to buff |
| Fang attack owner | `Evoker.EvokerAttackSpellGoal.performSpellCasting` (`Evoker.java` 163–185) → `createSpellEntity` → `new EvokerFangs(..., Evoker.this)` (`Evoker.java` 212–213). Close range (`distanceToSqr < 9`): 5 inner + 8 outer; else 16 in a line |
| Fang entity | `EvokerFangs` MISC, `dealDamageTo`: 6.0F `magic()` if no owner, else `indirectMagic` and skip if `owner.isAlliedTo(target)` (`EvokerFangs.java` 119–135). Owner UUID persisted. `discard()` after life ticks. **Not** an organism |
| Equipment removal | Fangs and Vex summon are **inner Goal classes** on Evoker, not held items. `EvokerRenderer` only renders the item-in-hand layer **while `isCastingSpell()`** (`EvokerRenderer.java` 19–36) — presentation of empty hands / casting pose, not a required weapon. Removing/replacing equipment **does not** change fang/summon identity; organism identity remains `EntityType.EVOKER` |
| Shared spellcaster framework | `SpellcasterIllager` owns tick/`SpellTicks` NBT, arm pose SPELLCASTING, particle colors, abstract `SpellcasterUseSpellGoal` (`SpellcasterIllager.java` 20–235). `IllagerSpell` enum includes `DISAPPEAR` / `BLINDNESS` (122–128) **unused by Evoker** (Illusioner uses those). Shared Java helper ≠ Magic Profile ≠ shared spells as Evoker composition |
| Generic AI also present | `FloatGoal`, `AvoidEntityGoal<>(Player, 8.0F, 0.6, 1.0)`, `RandomStrollGoal`, `LookAtPlayerGoal`, `HurtByTargetGoal(this, Raider.class).setAlertOthers()`, `NearestAttackableTargetGoal` Player / AbstractVillager / IronGolem (`Evoker.java` 52–68). Avoid-player and targeting are generic/raid-adjacent AI, not a spell trait |

**Combat classification:** fang + summon + wololo are **organism-owned vanilla capabilities** implemented as Evoker inner goals. They are **not** equipment capabilities. Shared `SpellcasterIllager` / `Raider` goals are **not** a caster clade.

---

## Raid vs organism-native

| Fact | Owner | Organism-native? |
|------|-------|------------------|
| Raid membership | `Raider` + `Raid.joinRaid` / `canJoinRaid`. `Raider.finalizeSpawn` sets `canJoinRaid` true for Evoker (`Raider.java` 274–277; Witch NATURAL is the exception) | **No** — raid role |
| Wave table | `Raid.RaiderType.EVOKER(EntityType.EVOKER, {0,0,0,0,0,1,1,2})` (`Raid.java` 839). `getDefaultNumSpawns` indexes that array (`718–720`). Easy/Normal/Hard group counts 3/5/7 (`getNumGroups` 784–795). Wave 5+ matches wiki numerically. Bonus spawns for EVOKER **return 0** (`738–740`) | **No** — encounter table |
| Ravager passenger | `Raid.spawnGroup` (`493–536`): on Hard (`i >= getNumGroups(HARD)`), first ravager passenger `k==0` is **EVOKER**, else VINDICATOR; Normal last wave passenger is PILLAGER | **No** — raid placement. **CROSS-ORGANISM REQUEST** below for Vindicator/Pillager, not a conclusion |
| Raid AI goals | Inherited `Raider.registerGoals`: banner, `PathfindToRaidGoal`, village POI move, celebration (`Raider.java` 56–63) | **No** — raid-AI |
| Bell glowing | `BellBlockEntity` filters `#minecraft:raiders`, `GLOWING` 60 ticks (`BellBlockEntity.java` 126–177) | **No** — raid-tag presentation |
| `#minecraft:raiders` | JSON members: evoker, pillager, ravager, vindicator, illusioner, witch (`data/minecraft/tags/entity_type/raiders.json`). Readers found: `BellBlockEntity`, `Ravager` passenger check, adventure captain predicate | Tag grouping ≠ clade |
| Patrol **spawn** | `PatrolSpawner.spawnPatrolMember` creates **`EntityType.PILLAGER` only** (`PatrolSpawner.java` 96–117) | Evoker is **not** patrol-spawned. Inherited `PatrollingMonster` goals/NBT do not make Evoker a patrol unit |
| Mansion spawn | `WoodlandMansionPieces.handleDataMarker` `"Mage"` → `EntityType.EVOKER.create` + `setPersistenceRequired` + `MobSpawnType.STRUCTURE` (`1323–1348`). Structure `mansion.json` biomes `#has_structure/woodland_mansion` = dark_forest | Encounter placement ≠ origin |
| “Caster raid unit” | Wave table + empty `applyRaidBuffs` | **Rejected** as biology |

---

## Behavior ownership table

Method: owner → biological input? → existing `organismKey` / `contributingSourceKey`? → named live BioCraft consumer? → **A / B / C**.

Default expectation: **A/B**. **C** only with named live BioCraft consumer **and** missing biological fact. Expectation is not a conclusion; conclusion below is from this table.

| Behavior | Actual owner | Biological input? | Existing composition | Named BioCraft consumer | Live/stub class | Result |
|----------|--------------|-------------------|----------------------|-------------------------|-----------------|--------|
| Identity / MONSTER / size | `EntityType.EVOKER` | Identity only | `organismKey = evoker` (fail-soft if unregistered) | Generic resolver / `DnaSampleFromOccupant` encode-id path if a sample exists | **LIVE** generic | **B** |
| Java parents SpellcasterIllager / AbstractIllager / Raider / PatrollingMonster | Shared Minecraft classes | Implementation reuse | Distinct registry id already | None for clade | **LIVE** vanilla | **A** (closed leap) |
| Attributes / XP | `Evoker.createAttributes` / constructor `xpReward` | No | Identity sufficient | None | **LIVE** vanilla | **A** |
| Fang attack | `Evoker.EvokerAttackSpellGoal` + `EvokerFangs` MISC | Combat capability, not composition | Identity sufficient | **None** | **LIVE** vanilla | **A** |
| Spellcasting framework / `SpellTicks` / arm pose | `SpellcasterIllager` | Presentation + AI helper | Identity sufficient | None | **LIVE** vanilla | **A** |
| Vex summoning | `Evoker.EvokerSummonSpellGoal` | Entity **creation**, not genetics | Distinct keys `evoker` / `vex` already exist as inventory/registry ids | None for lineage | **LIVE** vanilla | **A/B** |
| Vex independent type | `EntityType.VEX` + spawn egg + `canSummon` | Independent existence | `organismKey = vex` (registered SPIRITUAL — Vex’s registry fact, not earned here) | Do not consume as Evoker biology | **LIVE** vanilla + Host Registry for **vex** only | **A** (blocks origin-from-Evoker) |
| Wololo sheep color | `Evoker.EvokerWololoSpellGoal` → `Sheep.setColor(RED)` | External mutation of Sheep color NBT | Sheep identity already; color is Sheep state | None | **LIVE** vanilla | **A** |
| Player dye / breed color | `DyeItem` / `Sheep.getOffspringColor` | Sheep-owned color paths | Not Evoker | None (Sheep not this report) | **LIVE** vanilla | **A** |
| Default equipment / totem hold | **Absent** on Evoker. Totem is loot table | Loot ≠ held capability | Identity sufficient | None | **LIVE** vanilla loot | **A** |
| Raid buffs | `applyRaidBuffs` empty | N/A | Not needed | None | **LIVE** vanilla | **A** |
| Raid waves / ravager ride / join raid | `Raid` / `Raider` | Encounter / raid-AI | Identity sufficient | None | **LIVE** vanilla | **A** |
| Patrol spawn | `PatrolSpawner` → PILLAGER only | Evoker not owner | Not needed | None | **LIVE** vanilla | **A** |
| Mansion Mage marker | `WoodlandMansionPieces` | Structure encounter | Identity sufficient | None | **LIVE** vanilla | **A** |
| `#minecraft:illager` / `ILLAGER_FRIENDS` | Tag JSON + `AbstractIllager.isAlliedTo` (`AbstractIllager.java` 35–41) | Faction look | Identity sufficient | None | **LIVE** vanilla | **A** (closed leap) |
| `#minecraft:raiders` / bell glow | Tag + `BellBlockEntity` | Raid presentation | Identity sufficient | None | **LIVE** vanilla | **A** |
| Village hostility distance | `VillagerHostilesSensor` exact `EntityType.EVOKER` at 12.0F (`VillagerHostilesSensor.java` 11) | Combat taxonomy | Identity sufficient | None | **LIVE** vanilla | **A** |
| Hurt-by alert | `HurtByTargetGoal(this, Raider.class).setAlertOthers()`: **ignore damage from Raider**; alert **same Java class** (`Evoker`) within follow-range (`HurtByTargetGoal.java` 30–33, 57–61, 76–79) | Generic AI | Identity sufficient | None | **LIVE** vanilla | **A** |
| Avoid player 8 blocks | `AvoidEntityGoal` | Generic AI | Not needed | None | **LIVE** vanilla | **A** |
| Baby villager non-target | `AbstractIllager.canAttack` skips baby `AbstractVillager` (`AbstractIllager.java` 27–29) | Shared parent AI | Not needed | None | **LIVE** vanilla | **A** |
| Natural biome spawn | **Absent** in biome JSON despite `SpawnPlacements` | Placement helper ≠ spawn list | Not needed | None | **ABSENT** biomes | **A** |
| Sounds / texture `illager/evoker.png` | `Evoker` sounds + `EvokerRenderer` / `IllagerModel` | Presentation | Not needed | None | **LIVE** vanilla client | **A** |
| Loot totem + emerald | Dedicated evoker loot table | Loot | Identity sufficient | None | **LIVE** vanilla | **A/B** |
| Host Registry key | **ABSENT** | Participation missing | Fail-soft `organismKey = evoker` still representable | Eligibility false via null HostType | **UNREGISTERED** | **B** (identity only) |
| Magic / spellcasting / summoner / Illager / Raider / caster Profile | No BioCraft owner | Would be new facts | Existing identity already distinguishes Evoker | **None** | **PLANNING ONLY** if imagined | not **C** |

**No row is C.**

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` key `"evoker"` | **ABSENT / UNREGISTERED** | Not in any `vanilla_hosts` group (`hosts.json` 1–53) | Participation missing. Not a BP field. Do not register in this pass |
| `hosts.json` key `"vex"` | **LIVE** (Vex’s registry, not Evoker’s) | `vanilla_hosts.unsuitable.spiritual.mobs`: `"vex", "allay"` (33–35) | Locked: do not promote Vex/Allay/spiritual category from Evoker evidence |
| `hosts.json` key `"sheep"` | **LIVE** (Sheep’s registry) | `living_biological` includes `"sheep"` | Wololo target is a registered living host; that does not make wololo a Sheep or Evoker BP field |
| HostType / suitability for evoker | **N/A via registry** | `getHostType("evoker") == null` → `isSuitableForXenomorph` false | Unregistered ≠ biology |
| `HostConfigParser` | **LIVE** generic | Forbids biology keys in hosts.json (`HostConfigParser.java` 35–49) | Cannot smuggle spellcasting into Host Registry |
| `BiologicalProfileResolver` | **LIVE** generic | Unknown keys **fail-soft**: preserve `organismKey`, empty HostType / form / pack / source (`BiologicalProfileResolver.java` 35–56; test `unknownKeyPreservesOrganismKeyWithEmptyOptionals`) | `organismKey = evoker` is representable **without** registration |
| Resolver unit test for key `evoker` | **TEST ONLY absent** | Generic unknown-key test exists; no `"evoker"` test | Generic path live |
| `DnaSampleFromOccupant` | **LIVE** generic | `minecraft:evoker` → `evoker` via `HostRegistryPaths.registryPath` even if unregistered (`DnaSampleFromOccupant.java` 50–59; `HostRegistryPaths.java` 16–21) | Identity/source transport only. Not a spellcasting consumer |
| `contributingSourceKey` production from this host | **LIVE machinery, origin blocked** | Gestation/eligibility uses `HostEligibilityService` → null HostType fails (`HostEligibilityService.java` 19–31, 47–49) | Representation exists; origin production does not |
| `HostEligibilityService` | **LIVE** generic | Null HostType → not suitable | Not an Evoker consumer |
| Evoker / Illager / Raider / Magic entity JSON / AI / DNA | **ABSENT** | No matches for evoker/illager/raider/wololo/spellcast under `biocraft-alien/src` Java or resources | Vanilla remains behavior owner |
| DESIGN-BIO-MANIFEST-004 / Magic / Summoner / Illager / Raider Profile | **PLANNING / RESERVED** | Locked: 004 remains reserved. No such profile | Do not mint |

---

## Wiki disagreements (orientation only; source wins)

Source: [minecraft.wiki/w/Evoker](https://minecraft.wiki/w/Evoker) (version-aggregated page, fetched 2026-09-10).

| Wiki claim | 1.21.1 source |
|------------|---------------|
| “Spell-casting illager” as type | Presentation + `SpellcasterIllager` parent. **Rejected** as Magic Profile / caster category |
| “Only way for vexes to spawn (without Creative or commands)” | Overstates origin. Type is independently instantiable (`canSummon`, spawn egg, `SpawnPlacements`, owner-optional `finalizeSpawn`). Survival biome/structure/raid Vex spawn **was not found**. Independent path does not disprove summoning; it blocks biological-origin |
| Player flee “ten block radius” | `AvoidEntityGoal` distance **8.0F** (`Evoker.java` 57) |
| Alert “all evokers in a twelve block radius” then infinite chase | `HurtByTargetGoal` alerts **same class** using **follow range 12** and Y=10 (`HurtByTargetGoal.java` 76–79). `unseenMemoryTicks = 300` (68), not infinite. `Raider.class` in the constructor is **ignore-damage**, not alert-all-raiders |
| Combo fangs while summoning vexes (JE) | **Not found.** `SpellcasterUseSpellGoal.canUse` returns false while `isCastingSpell()` (`SpellcasterIllager.java` 189) |
| Flee from creakings within 8 blocks | **Absent** in 1.21.1 `Evoker.java`. Creaking is a later version. Wiki mixes versions |
| Wololo disabled when `mobGriefing` false (JE) | Matches: `canEntityGrief` → `RULE_MOBGRIEFING` (`Evoker.java` 314; `EventHooks.java` 752–757) |
| Fangs 6 damage, armor-piercing magic | Matches `EvokerFangs.dealDamageTo` 6.0F magic / indirectMagic |
| Raid from wave 5; Hard ravager rider | Matches `RaiderType` array + `spawnGroup` passenger logic |
| Totem 100% drop; emerald if player-killed | Matches loot table |
| Snow golem target JE | **Absent** in Evoker goals (wiki correctly marks Bedrock-only) |

---

## Rejected interpretations

Unless evidence surviving this packet (it does not):

- Magic Profile
- Spellcasting trait / caster category
- Summoner trait
- Vex lineage / offspring / ancestry / genetics (creation ≠ reproduction; owner not even NBT-persistent)
- Illager ancestry / Illager Profile
- Raider Profile / “caster raid unit” as biology
- Sheep-coloring trait / wololo-as-genetics
- AbstractIllager / Raider / tags / raid / patrols / village hostility / shared equipment / shared AI / faction look as clade or BP field
- Promoting Vex, Allay, or a broader spiritual/summoned-organism category from Evoker evidence
- EvokerFangs as a fourth organism
- Host Registry unregistered as ineligibility-biology
- Inventory `bio-organic` as HostType
- Minting `DESIGN-BIO-MANIFEST-004`

---

## Potential relationships (identify, do not encode)

```text
Evoker  --creates (summon, runtime owner, limited life)-->  Vex     [separate organism; not offspring]
Evoker  --creates (MISC, owner UUID)------------------->  EvokerFangs
Evoker  --mutates wool Color NBT----------------------->  Sheep    [Sheep-owned persistent color]
Evoker  --Java parent---------------------------------->  SpellcasterIllager / AbstractIllager / Raider
Evoker  --tag member----------------------------------->  #illager, #illager_friends, #raiders
Evoker  --encounter------------------------------------>  woodland mansion "Mage"; raid waves 5+
```

Implementation adjacency only. Distinct `organismKey` values already name Evoker vs Vex vs Sheep. Optional Model A `contributingSourceKey` could name a **source identity** if a xenomorph consumer ever needed it; **no live consumer asks.** Do not encode.

---

## CROSS-ORGANISM VERIFICATION REQUESTS

Not conclusions about those organisms. Recorded because Evoker-adjacent source could be misread on those branches:

1. **Pillager — patrol spawn vs inherited patrol AI.** `PatrolSpawner` creates **only** `EntityType.PILLAGER` (`PatrolSpawner.java` 96–117). Evoker inherits `PatrollingMonster` but is **not** patrol-spawned. Request the Pillager branch verify patrol **spawn ownership** independently and not treat `PatrollingMonster` / `Raider` inheritance as a shared biological patrol trait with Evoker.

2. **Vindicator — mansion / raid passenger adjacency.** Woodland mansion `"Warrior"` marker creates Vindicator beside `"Mage"` Evoker (`WoodlandMansionPieces.java` 1323–1328). Hard-raid ravager passenger is Evoker when `k==0`, else Vindicator (`Raid.java` 522–527). Request the Vindicator branch treat those as **encounter placement**, not Evoker/Vindicator clade or shared caster/melee biology.

3. **Pillager / Vindicator — `#minecraft:illager` / `ILLAGER_FRIENDS` / `HurtByTargetGoal(Raider.class)`.** Evoker uses those for faction alliance and ignore-Raider revenge. Request those branches keep the locked closed leap: tags / AbstractIllager / Raider / village hostility ≠ ancestry. Do not inherit an Illager Profile from this packet.

Sheep and Vex are **not** Pillager/Vindicator. Sheep wololo and Vex summon are documented above as Evoker-owned tests only; they are not Sheep/Vex reports.

---

## Final YES/NO gates

| Gate | Answer |
|------|--------|
| New BP field? | **NO** |
| Existing composition sufficient? | **YES** — `organismKey = evoker` (fail-soft unregistered). Vex remains its own key. No new `contributingSourceKey` contract earned |
| Named live BioCraft consumer of an Evoker-specific biological fact? | **NO** — only generic identity plumbing (`BiologicalProfileResolver`, `DnaSampleFromOccupant`, `HostEligibilityService`). No spellcasting/summon/wololo/raid consumer |
| Escalation / mint `DESIGN-BIO-MANIFEST-004` / Magic/Illager/Raider/Summoner Profile? | **NO** — 004 remains reserved. C not earned |
| Implement anything? | **NO** — stop |

**C was not earned.** Default A/B expectation matches the table; it is now a conclusion from named owners + absent consumers.

---

## Recommended next dependency (THIS organism only)

**Stop.** No further Evoker evidence dependency. Do not open Vex, Pillager, Vindicator, Illusioner, Ravager, Witch, or Sheep from this packet. Do not set the global queue. If a later **named** BioCraft consumer needs Evoker **identity** only, existing `organismKey` fail-soft is enough; that still would not mint 004 without a missing biological fact.

---

## Source index (extracted to `.tmp_mc_sources/`)

- `net/minecraft/world/entity/monster/Evoker.java` — class, goals, fangs, summon, wololo, empty raid buffs, Vex alliance
- `net/minecraft/world/entity/monster/SpellcasterIllager.java` — spell ticks, enum, use/cast goals
- `net/minecraft/world/entity/monster/AbstractIllager.java` — `ILLAGER_FRIENDS` alliance, baby villager, arm pose
- `net/minecraft/world/entity/raid/Raider.java` — raid join/AI/NBT, `finalizeSpawn` canJoinRaid
- `net/minecraft/world/entity/raid/Raid.java` — `RaiderType.EVOKER`, spawnGroup, getNumGroups
- `net/minecraft/world/entity/projectile/EvokerFangs.java` — MISC damage, owner UUID
- `net/minecraft/world/entity/monster/Vex.java` — owner, limited life, equipment, NBT (no owner)
- `net/minecraft/world/entity/monster/PatrollingMonster.java` — leader banner, patrol NBT
- `net/minecraft/world/level/levelgen/PatrolSpawner.java` — PILLAGER-only spawn
- `net/minecraft/world/level/levelgen/structure/structures/WoodlandMansionPieces.java` — Mage marker
- `net/minecraft/world/entity/EntityType.java` — EVOKER / EVOKER_FANGS / VEX
- `net/minecraft/world/entity/SpawnPlacements.java` — EVOKER / VEX placement helpers
- `net/minecraft/world/item/Items.java` — spawn eggs
- `net/minecraft/world/entity/animal/Sheep.java` — color NBT / setColor
- `net/minecraft/world/item/DyeItem.java` — independent dye path
- `net/minecraft/world/entity/ai/sensing/VillagerHostilesSensor.java` — EVOKER 12.0F
- `net/minecraft/world/level/block/entity/BellBlockEntity.java` — `#raiders` glow
- `net/minecraft/tags/EntityTypeTags.java` / `data/tags/EntityTypeTagsProvider.java`
- `data/minecraft/tags/entity_type/illager.json`, `illager_friends.json`, `raiders.json`
- `data/minecraft/loot_table/entities/evoker.json`
- `data/minecraft/worldgen/structure/mansion.json`, `tags/worldgen/biome/has_structure/woodland_mansion.json`
- Live BioCraft: `hosts.json`, `HostType.java`, `MobHostRegistry.java`, `BiologicalProfileResolver.java`, `HostEligibilityService.java`, `DnaSampleFromOccupant.java`, `HostRegistryPaths.java`, `BiologicalProfileResolverTest.java`
