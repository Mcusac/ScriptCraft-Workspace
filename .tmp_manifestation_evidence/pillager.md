# Pillager — biological-manifestation evidence packet

Temporary investigator packet. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, inventory, backlog, sprint, roadmap, Java, resources, or `DESIGN-BIO-MANIFEST-004`.

Gathered against Minecraft Java **1.21.1** / NeoForge **21.1.208** mapped sources in `.tmp_mc_sources/` (extracted from `biocraft-alien/build/moddev/artifacts/neoforge-21.1.208-sources.jar` and `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar`). Wiki used only as orientation / disagreement check.

Method: owner → biological input? → existing `organismKey` / `contributingSourceKey`? → named live BioCraft consumer? → **A / B / C**.
C only with named live consumer **and** missing biological fact. Default expectation A/B is not a conclusion.

Closed leaps applied (independently traced): AbstractIllager / Raider / tags / raid / patrols / village hostility / equipment / AI / faction ≠ clade.

---

## Subject / Version / Target identity

| Field | Evidence |
|-------|----------|
| Subject | Pillager |
| Minecraft | Java 1.21.1 / NeoForge 21.1.208 |
| Registry identity | `EntityType.PILLAGER` register `"pillager"` — `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` **554–562** |
| Builder | `Pillager::new`, `MobCategory.MONSTER`, `.canSpawnFarFromPlayer()`, `.sized(0.6F, 1.95F)`, `passengerAttachments(2.0F)`, `ridingOffset(-0.6F)`, `clientTrackingRange(8)`. No `fireImmune()`. |
| Java type | `Pillager extends AbstractIllager implements CrossbowAttackMob, InventoryCarrier` — `Pillager.java` **51** |
| Parent chain | `Pillager` → `AbstractIllager` → `Raider` → `PatrollingMonster` → `Monster` |
| Inventory (planning only) | `pillager` / bio-organic / unregistered / manifestation pending / eligibility undetermined — `vanilla_organism_inventory.md` row. Category ≠ HostType. |
| Host Registry | **UNREGISTERED.** `hosts.json` `vanilla_hosts` / `modded_hosts` / `variant_mappings` contain no `"pillager"`. Unregistered ≠ ineligible ≠ biology. |
| Live BioCraft key | `BiologicalProfileResolver` fail-soft: unknown keys preserve `organismKey`, `HostType` null (`MobHostRegistry.getHostType` → `null` at `MobHostRegistry.java` **46–48**). `isSuitableForXenomorph("pillager")` is false because `hostType == null` (**68–71**), which is participation absence, not a biological verdict. |
| Tracking | Do **not** mint `DESIGN-BIO-MANIFEST-004`. No Illager / Raider / Pillager / Ranged / Crossbow Profile. |

```text
Pillager does X
    → Minecraft entity / item / AI / raid / patrol / tag / world owns X
    → Pillager biological composition contributes something to X?
    → a live AlienCraft consumer needs that distinction?
```

---

## Behavior ownership table

Columns: owner → biological input? → existing composition? → named live BioCraft consumer? → A/B/C.

| Behavior | 1.21.1 owner (path / method / lines) | Biological input? | `organismKey` / `contributingSourceKey`? | Named live BioCraft consumer? | Gate |
|----------|--------------------------------------|-------------------|------------------------------------------|-------------------------------|------|
| Identity | `EntityType.PILLAGER` `"pillager"` `EntityType.java` **554–562** | Identity only | `organismKey = pillager` (fail-soft; unregistered) | Generic resolver / Analyzer identity if a sample is named `pillager` | **B** |
| Size / category | Same builder: `MONSTER`, 0.6×1.95 | Presentation / spawn category | Distinct key already | None | **A** |
| `canSpawnFarFromPlayer` | `EntityType.java` **557**, **1354–1355**; consumed by `NaturalSpawner.isValidSpawnPostitionForType` **242–244** (distance gate vs category despawn²) | **No.** Encounter spawn helper. Shared with `SHULKER` (**591**). | Identity sufficient | None | **A** |
| Default spawn placement | `SpawnPlacements.java` **130–132**: `ON_GROUND` / `MOTION_BLOCKING_NO_LEAVES` / `PatrollingMonster::checkPatrollingMonsterSpawnRules` | **No.** Generic monster light gate (`PatrollingMonster.java` **91–97**: block light > 8 rejects) | Identity sufficient | None | **A** |
| Patrol encounter | `PatrolSpawner.java` **18–118**: `CustomSpawner`; always `EntityType.PILLAGER.create` (**103**); `MobSpawnType.PATROL`; gamerule `RULE_DO_PATROL_SPAWNING` (`GameRules.java` **154–156**). Wired Overworld-only in `MinecraftServer.createLevels` **363–365**. Biome skip `#minecraft:without_patrol_spawns` (`mushroom_fields`). | **No.** Encounter, not origin. | Identity sufficient | None | **A** |
| Patrol AI / banner | `PatrollingMonster.registerGoals` **37–39** `LongDistancePatrolGoal`; `finalizeSpawn` **70–88** sets leader banner via `Raid.getLeaderBannerInstance` and `patrolling` if `PATROL`. `Raider.canJoinPatrol` **135–137** = `!hasActiveRaid()`. | **No.** Patrol state + equipment banner. | Identity sufficient | None | **A** |
| Outpost encounter | `data/minecraft/worldgen/structure/pillager_outpost.json` **7–18** `spawn_overrides.monster` type `minecraft:pillager`; biomes `#has_structure/pillager_outpost`; structure set excludes villages (`pillager_outposts.json` **4–7**). Jigsaw pools in `PillagerOutpostPools.java`. | **No.** Worldgen encounter. | Identity sufficient | None | **A** |
| Raid membership | `Raider` fields `raid` / `wave` / `canJoinRaid` (`Raider.java` **47–50**, **73–79**, **139–164**). `Raids.canJoinRaid` **72–78**. `Raider.finalizeSpawn` **274–277** sets `canJoinRaid` (Witch NATURAL special-case is **not** a Pillager conclusion). Gamerule `RULE_DISABLE_RAIDS` (`GameRules.java` **123–125**; `Raids.java` **53–55**, **85–86**). Dimension `hasRaids()`. | **No.** Raid system attaches membership. | Identity sufficient | None | **A** |
| Raid role / wave composition | `Raid.RaiderType.PILLAGER` `spawnsPerWaveBeforeBonus = {0,4,3,3,4,4,4,2}` (`Raid.java` **837–842**). Spawned by `Raid` iterating `RaiderType.VALUES` **500–507**. Bonus counts `getPotentialBonusSpawns` **728–737** share a switch arm with Vindicator (raid table, not clade). Ravager rider assignment **518–535** can create a Pillager passenger on Normal last wave. `joinRaid` **546–560** calls `finalizeSpawn(..., EVENT)` then `applyRaidBuffs`. | **No.** External wave table. “Ranged raid unit” is composition + equipment. | Identity sufficient | None | **A** |
| Raid-specific AI | `Raider.registerGoals` **57–63**: `ObtainRaidLeaderBannerGoal`, `PathfindToRaidGoal` (`PathfindToRaidGoal.java` **26–32** requires `hasActiveRaid()`), `RaiderMoveThroughVillageGoal` (`isValidRaid` **461–463**), `RaiderCelebration` (raid loss **409–411**). `HoldGroundAttackGoal` (`Raider.java` **293–299**) requires `getCurrentRaid()==null` **and** `isPatrolling()` — patrol shout, not melee. | **No.** Goals gated on raid/patrol flags. | Identity sufficient | None | **A** |
| Raid equipment buffs | `Pillager.applyRaidBuffs` **231–252**: chance `raid.getEnchantOdds()`; may replace mainhand with enchanted `Items.CROSSBOW` via `RAID_PILLAGER_POST_WAVE_3` / `_5` (`VanillaEnchantmentProviders.java` **15–17**, **25–27**; JSON `enchantment_provider/raid/pillager_post_wave_*.json` = Quick Charge 1/2). | **No.** Raid-supplied enchantment of an item. | Identity sufficient | None | **A** |
| Village hostility targeting | `Pillager.registerGoals` **71–73**: `NearestAttackableTargetGoal` Player / `AbstractVillager` / `IronGolem`. `AbstractIllager.canAttack` **27–28** refuses baby villagers. `VillagerHostilesSensor` **14** lists `EntityType.PILLAGER` at 15.0F (exact-type map, not `#illager`). | **No.** Generic targeting AI + villager sensor table. Faction hostility ≠ ancestry. | Identity sufficient | None | **A** |
| Hurt-by alert | `HurtByTargetGoal(this, Raider.class).setAlertOthers()` `Pillager.java` **70** | **No.** Java class filter `Raider`, not biology. | Identity sufficient | None | **A** |
| **Combat: crossbow (organism vs equipment vs AI)** | See dedicated combat test below. | **No.** Equipment + generic goal + item projectile factory. | Identity sufficient | None | **A** |
| Default equipment | `Pillager.populateDefaultEquipmentSlots` **156–158**: `MAINHAND = new ItemStack(Items.CROSSBOW)`. Rare spawn enchant `PILLAGER_SPAWN_CROSSBOW` Piercing 1 (`enchantSpawnedWeapon` **161–171**; JSON `enchantment_provider/pillager_spawn_crossbow.json`). | **No.** Spawned item. Left-handedness is generic `Mob` flag (`Mob.java` **92**, **1462**), not a Pillager spawn table. | Identity sufficient | None | **A** |
| Projectile creation | `Pillager.performRangedAttack` **192–194** → `CrossbowAttackMob.performCrossbowAttack` **19–29** → `CrossbowItem.performShooting` **192–206** / `createProjectile` **173–185** (arrow via `super` or `FireworkRocketEntity`). Ammo: `Monster.getProjectile` **149–157** defaults `Items.ARROW` if no held ammo. Velocity 1.6F matches `CrossbowItem.MOB_ARROW_POWER` **55**. | **No.** Item owns shot; Monster owns default arrow. | Identity sufficient | None | **A** |
| `canFireProjectileWeapon` | `Pillager.java` **91–93**: `projectileWeapon == Items.CROSSBOW` only | Equipment filter, not a ranged trait | Identity sufficient | None | **A** |
| Charging pose | Synched `IS_CHARGING_CROSSBOW`; `getArmPose` **116–124** picks `CROSSBOW_CHARGE` / `CROSSBOW_HOLD` / `ATTACKING` / `NEUTRAL` | Presentation | Identity sufficient | None | **A** |
| Attributes | `Pillager.createAttributes` **76–82**: speed 0.35, health 24, `ATTACK_DAMAGE` 5.0, follow 32. Bound `DefaultAttributes` PILLAGER. | Numeric combat stats on the entity; **unused by any Pillager melee goal** (no `MeleeAttackGoal`, no `doHurtTarget` override). | Identity sufficient | None | **A** |
| Inventory / banner pickup | 5-slot `SimpleContainer`; `pickUpItem` **205–218**: banners → `Raider.pickUpItem`; else `wantsItem` **220–222** = `hasActiveRaid() && WHITE_BANNER`. Raid leader banner match in `Raider.pickUpItem` **218–239**. | **No.** Raid/patrol item rules. | Identity sufficient | None | **A** |
| Entity loot | `data/minecraft/loot_table/entities/pillager.json`: **only** `ominous_bottle` when `type_specific.raider.is_captain`. No crossbow / arrow / emerald pool. Crossbow is equipment drop chance, not organism loot. | **No.** | Identity sufficient | None | **A** |
| `#minecraft:illager` | JSON `illager.json`: evoker, illusioner, pillager, vindicator. Java `EntityTypeTags.ILLAGER` **has no gameplay reader** except composing `ILLAGER_FRIENDS` (`EntityTypeTagsProvider.java` **118**, **141**). | Tag membership ≠ clade | Distinct keys | None | **A** |
| `#minecraft:illager_friends` | JSON aliases `#illager`. **Named consumer:** `AbstractIllager.isAlliedTo` **35–40**: allied if other type is tag member **and** both scoreboard teams null. | Faction alliance when unteamed. **Not** ancestry. | Distinct keys | None | **A** |
| `#minecraft:raiders` | JSON: evoker, pillager, ravager, vindicator, illusioner, witch (Witch **not** in `#illager`). **Named consumers:** `BellBlockEntity.areRaidersNearby` / `isRaiderWithinRange` **126–137**, **169–174** (glow); `VanillaAdventureAdvancements` captain predicate; `Ravager.updateControlFlags` **80** (passenger control — see cross-organism request). | Raid-gameplay grouping. Witch inclusion disproves Illager=Raider clade. | Distinct keys | None | **A** |
| Sounds / renderer | `PILLAGER_*` sounds; `PillagerRenderer` uses `IllagerModel` + `ItemInHandLayer` (`PillagerRenderer.java` **12–17**, texture `textures/entity/illager/pillager.png`) | Presentation sharing ≠ clade | Distinct keys | None | **A** |
| Advancement UX | `whos_the_pillager_now.json`: player `killed_by_crossbow` with victim type pillager | UX, not organism biology | Distinct keys | None | **A** |
| Host participation | Absent from `hosts.json`. Resolver `hostType == null`. | Unregistered ≠ biology | Fail-soft `organismKey` | Eligibility remains undetermined; no live Pillager consumer | **B** (identity only) |

**Combat test (mandatory)** — organism capability vs equipment vs generic AI:

1. **Equipment gate:** `RangedCrossbowAttackGoal.canUse` **39–45** requires `isValidTarget()` **and** `isHoldingCrossbow()` (`item instanceof CrossbowItem`). `canContinueToUse` **48–50** also requires holding a crossbow. Removing/replacing the crossbow **disables the only attack goal** without changing `EntityType.PILLAGER`.
2. **No melee fallback on this organism:** `Pillager.registerGoals` **62–74** registers `RangedCrossbowAttackGoal` only. Jar-wide `new MeleeAttackGoal` is **absent** from `Pillager.java`. Pillager does **not** override `doHurtTarget`. `HoldGroundAttackGoal` stops navigation / shouts to nearby `Raider`s / sets aggressive (`Raider.java` **281–351**); it does not call `doHurtTarget`.
3. **Replacing with a bow:** `canFireProjectileWeapon` accepts **only** `Items.CROSSBOW`. There is no `RangedBowAttackGoal`. A bow does not restore ranged execution.
4. **Projectile owner:** shot is `CrossbowItem.createProjectile` / `performShooting`, not a Pillager-native projectile type.
5. **Identity unchanged:** equipment slot mutation does not convert entity type.
6. **Negative control (same item, different organism):** `Piglin implements CrossbowAttackMob` (`Piglin.java` **57**). `Piglin.createSpawnWeapon` **329–330** is 50% `CROSSBOW` / 50% `GOLDEN_SWORD`. Fight brain registers **both** `MeleeAttack.create(20)` and `new CrossbowAttack()` (`PiglinAi.java` **176–177**). `CrossbowAttack.checkExtraStartConditions` **26–30** also requires holding `CrossbowItem`. Crossbow use is therefore a **shared item/AI interface**, not a Pillager biological ranged trait.

**Raid-role test:** raid membership (`Raider` raid pointer), raid role/leader (`isPatrolLeader` / banner / `Raid.setLeader`), wave composition (`RaiderType` counts), and raid AI (`PathfindToRaidGoal`, celebration, village POI walk, `applyRaidBuffs`) are supplied by the raid/patrol systems. A summoned/egg Pillager with no raid still has `EntityType.PILLAGER` and still needs a crossbow for ranged execution. “Ranged raid unit” is not biology.

**Patrol test:** `canSpawnFarFromPlayer` and `PatrolSpawner` are encounter. `MobSpawnType.PATROL` flips `patrolling` (`PatrollingMonster.finalizeSpawn` **84–86**). That flag is instance spawn-type state, not origin.

---

## Config audit (live BioCraft)

| Surface | Pillager finding |
|---------|------------------|
| `data/biocraft_alien/systems/hosts.json` | No `"pillager"` in living / undead / unsuitable / modded / variant_mappings |
| `MobHostRegistry.getHostType("pillager")` | `null` (**46–48**) |
| `MobHostRegistry.isSuitableForXenomorph("pillager")` | `false` via null HostType (**68–71**) — participation gap, not eligibility science |
| `BiologicalProfileResolver` | Unknown non-blank keys fail-soft (`BiologicalProfileResolver.java` **23**, **41–57**): `organismKey` preserved, empty HostType / host-effect / form / behavior |
| `CompiledBiologicalProfile` | Nullable `hostType` allowed (**31–38**) |
| Entity JSON / `behavior_type` | No Pillager config |
| Java / tests | **Zero** matches for `pillager` / `Pillager` / `illager` / `raider` / `crossbow` under `biocraft-alien/src` (main+test) |
| `DESIGN-BIO-MANIFEST-004` | Reserved. Not earned. |

No Pillager gameplay tuning exists in BioCraft to audit. Vanilla JSON (loot, tags, outpost, enchantment providers) is Minecraft-owned.

---

## Wiki disagreements

Source: [minecraft.wiki/w/Pillager](https://minecraft.wiki/w/Pillager) (orientation only).

| Wiki claim | 1.21.1 mapped finding |
|------------|------------------------|
| Mob type “Illager” | Wiki/gameplay category. Code: Java parent `AbstractIllager` + tag `#illager`. Tag has **no** gameplay reader except composing `#illager_friends`. Not a biological clade. |
| “A pillager is an illager armed with a crossbow” as identity | Identity is `EntityType.PILLAGER`. Crossbow is default **equipment** (`populateDefaultEquipmentSlots`). Combat goal refuses to run without it. |
| “Passive (broken crossbow) JE only” | Targeting goals remain. Attack **execution** stops because `RangedCrossbowAttackGoal` requires a held `CrossbowItem` and there is no melee goal. “Passive” overstates: hostility targeting is still registered. |
| Bedrock melee attack strength | **Not** 1.21.1 Java evidence. JE has `ATTACK_DAMAGE` 5.0 with no melee goal. |
| “Natural equipment” 95% right / 5% left | `populateDefaultEquipmentSlots` always sets `MAINHAND`. Handedness is generic `Mob.isLeftHanded()`, not a Pillager-specific 5% table in this class. |
| Entity drops including arrows / emeralds / iron gear | `entities/pillager.json` is **captain ominous bottle only**. Crossbow is equipment. Raid extras are raid/loot-system, not this entity table. Infinite combat arrows come from `Monster.getProjectile` default `Items.ARROW`, not loot. |
| Spawn listed as Patrols / Outpost / Raids as if origin | All three are **encounter systems** (`PatrolSpawner`, structure `spawn_overrides`, `Raid.RaiderType`). Egg/summon still create `EntityType.PILLAGER`. |

---

## Rejected interpretations

Rejected unless a later named consumer re-opens the question with new evidence:

- **Ranged Profile / Crossbow Trait / Projectile Trait** — shot owned by `CrossbowItem`; goal gated on holding the item; Piglin shares the interface.
- **Weapon / ranged genetics** — equipment slot + enchantment providers.
- **Illager Profile / Raider Profile / Pillager Profile** — Java parents and tags are implementation / faction / raid grouping.
- **Patrol / village-hunting biology** — `NearestAttackableTargetGoal` + `VillagerHostilesSensor` exact-type row + raid/patrol goals.
- **Faction ancestry** — `isAlliedTo` + `#illager_friends` + `HurtByTargetGoal(..., Raider.class)`.
- **`#minecraft:illager` or `#minecraft:raiders` as clade** — `#raiders` includes Witch and Ravager, which are **not** `AbstractIllager` / not both in `#illager`. `#illager` has no gameplay reader of its own.
- **`canSpawnFarFromPlayer` as origin / far-roaming biology** — NaturalSpawner distance exception.
- **Raid wave counts as organism-native population biology** — `Raid.RaiderType` table.
- **Inventory `bio-organic` as HostType or eligibility** — planning label only; unregistered.
- **Unregistered ⇒ ineligible as biology** — Host Registry participation fact only.
- **Mint `DESIGN-BIO-MANIFEST-004`** — reserved; no named consumer.

---

## Potential relationships (adjacency, not ancestry)

Implementation graph only. Do **not** encode as classification.

```text
PatrollingMonster
 └── Raider
      ├── AbstractIllager
      │    ├── Pillager  (+ CrossbowAttackMob, InventoryCarrier)
      │    ├── Vindicator          ← do not conclude here
      │    └── SpellcasterIllager  ← Evoker / Illusioner; do not conclude here
      ├── Ravager                  ← extends Raider, not AbstractIllager
      └── Witch                    ← in #raiders, not #illager; do not conclude here

CrossbowAttackMob
 ├── Pillager  (goal: RangedCrossbowAttackGoal; always spawn crossbow)
 └── Piglin    (brain: CrossbowAttack + MeleeAttack; 50% sword)  ← equipment negative control
```

Shared Java parent / tag / raid table / village hostility = **research adjacency**. Distinct `organismKey` values already name each entity.

---

## CROSS-ORGANISM VERIFICATION REQUESTS

Not conclusions about those organisms. Recorded because Pillager-adjacent 1.21.1 code also names them:

1. **Evoker / Vindicator** — both in `#illager` and `#raiders`; both `AbstractIllager`; both appear in `Raid.RaiderType` with **different** `spawnsPerWaveBeforeBonus` arrays (`Raid.java` **838–840**). Vindicator registers `MeleeAttackGoal` and `RaiderOpenDoorGoal` (`Vindicator.java` **61**, **63**); Pillager registers **neither**. Shared parent/tags/raid membership must be re-traced on those organisms; do not inherit Pillager’s “equipment-gated ranged, no melee goal” result.
2. **Evoker (raid rider branch)** — `Raid` spawn loop **522–527** may `EntityType.EVOKER.create` or `VINDICATOR.create` as Ravager passengers on Hard+ waves; Normal last wave uses `PILLAGER.create` (**520–521**). Wave passenger assignment is raid-system, not Pillager biology; Evoker/Vindicator investigators should own that branch.
3. **Ravager** — `Ravager.updateControlFlags` **80** uses `EntityTypeTags.RAIDERS` for passenger-controlled AI flags; Ravager extends `Raider` not `AbstractIllager`; in `#raiders` not `#illager`. Request: treat `#raiders` consumer independently; do not fold into an Illager clade from this packet.
4. **Witch** — `#raiders` member, **absent** from `#illager`; `Raider.finalizeSpawn` **275** special-cases `EntityType.WITCH` NATURAL `canJoinRaid`. Request: raid-tag membership ≠ Illager parent.
5. **Piglin** — independent `CrossbowAttackMob` + optional crossbow. If a later ranged/crossbow question is asked for Piglin, start from Piglin sources; do not copy Pillager’s always-crossbow spawn.
6. **Illusioner** — in `#illager` / `#raiders`; inventory **non-actionable** unused/legacy (`vanilla_organism_inventory.md` §9.1). Do not reopen here.

---

## Final YES / NO gates

| Gate | Answer |
|------|--------|
| Does any investigated behavior require a biological input BioCraft does not already represent? | **NO.** Vanilla owns combat, raid, patrol, tags, loot, worldgen. |
| Is existing `organismKey = pillager` (fail-soft) / optional `contributingSourceKey` sufficient? | **YES** for identity. No conversion path that would need a source key. |
| Is there a named **live** BioCraft consumer missing a biological fact? | **NO.** Zero live Pillager/illager/raid/crossbow consumers. |
| Is **C** earned? | **NO.** Stop. Do not design a fact. |
| Mint `DESIGN-BIO-MANIFEST-004`? | **NO.** |
| Illager / Raider / Ranged / Crossbow Profile? | **NO.** |
| Unregistered Host Registry block representation? | **NO.** Unregistered ≠ ineligible ≠ biology. |
| Inventory `bio-organic` imply HostType `LIVING_BIOLOGICAL`? | **NO.** |

**Verdict for this organism: A/B.** Vanilla ownership + identity key. C not earned.

---

## Recommended next dependency (THIS organism only)

**None.** Pillager does not earn a BP field, classification node, or follow-up consumer investigation.

Do not wait on Evoker/Vindicator/Ravager/Witch packets to close Pillager: those are independent organisms. Sequence adjacency in the inventory is not a Pillager biological dependency.

---

## Source index (extracted / read)

- `.tmp_mc_sources/net/minecraft/world/entity/monster/Pillager.java`
- `.tmp_mc_sources/net/minecraft/world/entity/monster/AbstractIllager.java`
- `.tmp_mc_sources/net/minecraft/world/entity/monster/CrossbowAttackMob.java`
- `.tmp_mc_sources/net/minecraft/world/entity/monster/PatrollingMonster.java`
- `.tmp_mc_sources/net/minecraft/world/entity/raid/Raider.java`
- `.tmp_mc_sources/net/minecraft/world/entity/raid/Raid.java`
- `.tmp_mc_sources/net/minecraft/world/entity/raid/Raids.java`
- `.tmp_mc_sources/net/minecraft/world/entity/ai/goal/RangedCrossbowAttackGoal.java`
- `.tmp_mc_sources/net/minecraft/world/entity/ai/goal/PathfindToRaidGoal.java`
- `.tmp_mc_sources/net/minecraft/world/entity/ai/behavior/CrossbowAttack.java`
- `.tmp_mc_sources/net/minecraft/world/item/CrossbowItem.java`
- `.tmp_mc_sources/net/minecraft/world/entity/monster/Monster.java` (`getProjectile`)
- `.tmp_mc_sources/net/minecraft/world/level/levelgen/PatrolSpawner.java`
- `.tmp_mc_sources/net/minecraft/server/MinecraftServer.java` (custom spawners)
- `.tmp_mc_sources/net/minecraft/world/level/NaturalSpawner.java`
- `.tmp_mc_sources/net/minecraft/world/entity/SpawnPlacements.java`
- `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java`
- `.tmp_mc_sources/net/minecraft/tags/EntityTypeTags.java`
- `.tmp_mc_sources/net/minecraft/data/tags/EntityTypeTagsProvider.java`
- `.tmp_mc_sources/net/minecraft/world/level/block/entity/BellBlockEntity.java`
- `.tmp_mc_sources/net/minecraft/world/entity/ai/sensing/VillagerHostilesSensor.java`
- `.tmp_mc_sources/data/minecraft/loot_table/entities/pillager.json`
- `.tmp_mc_sources/data/minecraft/tags/entity_type/{illager,illager_friends,raiders}.json`
- `.tmp_mc_sources/data/minecraft/worldgen/structure/pillager_outpost.json`
- Live: `hosts.json`, `MobHostRegistry.java`, `BiologicalProfileResolver.java`, `HostType.java`, `CompiledBiologicalProfile.java`
