```text
TEMPORARY EVIDENCE — NOT PROJECT SSOT
BioCraft: Alien biological-manifestation investigation packet
Do not treat this file as canonical design documentation.
Do not edit Host Registry, inventory, BACKLOG, SPRINT, dna.md, system.md,
vanilla_organism_inventory.md, Java, or any canonical manifestation report from this packet.
```

# Villager — biological-manifestation evidence packet

Temporary investigator packet. **Not** a canonical manifestation report. **Not** permission to mint `DESIGN-BIO-MANIFEST-004` or add a Biological Profile field.

Gathered against Minecraft Java **1.21.1** / NeoForge **21.1.208** mapped sources in `.tmp_mc_sources/` (extracted from `implementations/minecraft/AlienCraft/biocraft-alien/build/moddev/artifacts/neoforge-21.1.208-sources.jar` and `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar`). Wiki used only as orientation / disagreement check.

Method for every behavior: existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| A | Minecraft owns it; no biological input required |
| B | `organismKey` / optional `contributingSourceKey` already sufficient |
| C | A named live consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied: shared parent ≠ clade; tag ≠ clade; conversion ≠ inheritance; spawn biome ≠ origin; equipment ≠ capability; Host Registry ≠ eligibility science; interesting behavior ≠ consumer; Human enum homonym ≠ Minecraft Villager; raid adjacency ≠ queue Ravager/Witch.

Existing BP composition: `organismKey`, optional `contributingSourceKey` (Model A Chestburster/Drone), optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

**This organism is not a Hoglin/Piglin conversion-source clade member.** Hoglin/Piglin conversion destinations cannot originate production `contributingSourceKey` because those sources are unregistered. Villager **is** registered `LIVING_BIOLOGICAL` and **can** originate a production source key. That is participation + identity transport, not a new field.

---

## Subject

Villager (`minecraft:villager`) — Minecraft Java 1.21.1 organism. BioCraft host-consumer investigation, not a conversion-clade continuation.

## Version

- Target: `minecraft_version_range=[1.21.1,1.22)`
- Authoritative mapped sources: Minecraft Java **1.21.1** / NeoForge **21.1.208**
- Wiki: orientation / disagreement discovery only; source wins

## Target identity

| Field | 1.21.1 evidence |
|-------|-----------------|
| Registry | `EntityType.VILLAGER` register `"villager"` — `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` **710–712** |
| Builder | `EntityType.Builder.<Villager>of(Villager::new, MobCategory.MISC).sized(0.6F, 1.95F).eyeHeight(1.62F).clientTrackingRange(10)` |
| Category | **`MobCategory.MISC`**, not `CREATURE` and not `MONSTER` |
| Java type | `Villager extends AbstractVillager implements ReputationEventHandler, VillagerDataHolder` — `Villager.java` **93** |
| Parent chain | `Villager` → `AbstractVillager` (`AgeableMob` + `InventoryCarrier` + `Npc` + `Merchant`) — `AbstractVillager.java` **40** |
| Attributes | `Villager.createAttributes()` speed **0.5**, follow **48.0** — `Villager.java` **269–271**; bound `DefaultAttributes` `EntityType.VILLAGER` |
| Spawn placement | `SpawnPlacements.java` **147**: `ON_GROUND` / `MOTION_BLOCKING_NO_LEAVES` / `Mob::checkMobSpawnRules` |
| Spawn egg | `Items.VILLAGER_SPAWN_EGG` `"villager_spawn_egg"` `SpawnEggItem(EntityType.VILLAGER, …)` — `Items.java` **1508–1509** |
| Host Registry | **REGISTERED** `vanilla_hosts.living_biological` key `"villager"` — `hosts.json` **6**. Can originate production `contributingSourceKey`. Registered ≠ extra biology. |
| Inventory (planning only; not edited) | `villager` / bio-organic / registered / `LIVING_BIOLOGICAL` / manifestation pending — read as context, not copied as conclusion |
| Distinct non-merge | `EntityType.WANDERING_TRADER` `"wandering_trader"` `MobCategory.CREATURE` — `EntityType.java` **717–718**. Separate type. Do not absorb. |
| Human homonym | BioCraft `HumanEntityType.VILLAGER("villager", "human_villager")` is a **Human subtype enum**, not `EntityType.VILLAGER`. Live Human entity is `biocraft_alien:human` (`EntityInit.java` **62–64**). |

```text
Villager does X
    → Minecraft entity / merchant / brain / POI / raid / conversion / world owns X?
    → Villager biological composition contributes something to X?
    → a live AlienCraft consumer needs that distinction beyond organismKey / contributingSourceKey?
```

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP representation? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|----------------------------|--------------------|-------|
| Identity / dimensions / MISC | `EntityType.VILLAGER` | `EntityType.java` **710–712**: `"villager"`, `MISC`, `0.6F×1.95F`, eyeHeight `1.62F` | Identity only | `organismKey = villager` | Resolver / Analyzer / host registry lookup | **B** |
| Java parent `AbstractVillager` | Class inheritance | Merchant + 8-slot inventory + ageable. Shared with Wandering Trader | Implementation sharing ≠ clade | Distinct keys (`villager` vs `wandering_trader`) | Combat class filter `AbstractVillager` (see targeting) | **A** |
| Profession / level / biome type | `VillagerData` synched + NBT | `DATA_VILLAGER_DATA`; default plains/NONE/1 (`Villager.java` **95**, **507–509**); `VillagerProfession` records (`VillagerProfession.java` **25–54**); `VillagerType` biome map (`VillagerType.java` **16–40**) | **No.** Merchant/presentation state | Identity covers the organism; profession is not composition | None that reads profession as biology | **A** |
| Trades / restock / career XP | `Villager` merchant methods | `updateTrades` **882–898** from `VillagerTrades.TRADES` (or experimental); `restock` **404–414**; `rewardTradeXp` **611–624**; HOTV price in `updateSpecialPrices` **494–503** | **No.** Offer tables + NBT | Not needed | None | **A** |
| Gossip / reputation | `GossipContainer` + `ReputationEventHandler` | Field `gossips` **131**; NBT **520**; `gossip` **901–908**; `onReputationEventFrom` **942–952**; player price via `getPlayerReputation` **731–732**, **486–492** | **No.** Village social state | Not needed | None | **A** |
| POI claim (bed / job / meeting) | Brain memories + `PoiManager` | `POI_MEMORIES` **182–191**; `releaseAllPois` **664+**; profession `heldJobSite` | **No.** Village infrastructure | Not needed | None | **A** |
| Brain schedule / work / meet | `Villager.registerBrainGoals` + `VillagerGoalPackages` | Activities CORE/WORK/MEET/REST/IDLE/PLAY — `Villager.java` **229–258** | **No.** Entity AI | Not needed | None | **A** |
| Breeding | `Villager.canBreed` + `VillagerMakeLove` + `getBreedOffspring` | Food threshold **12** (`FOOD_POINTS` **100**, `canBreed` **701–703**); `VillagerMakeLove` requires `EntityType.VILLAGER` partner **87–90**, vacant `PoiTypes.HOME` **93–97**, then `getBreedOffspring` **803–816** (child `EntityType.VILLAGER`, biome/parent type lottery) | Vanilla reproduction of same `EntityType`. Not xenomorph contribution | Identity sufficient; child is still `villager` | None that needs a breed trait | **A/B** |
| Iron Golem creation trigger | **`Villager.spawnGolemIfNeeded`** | Called from `gossip` **907** and `VillagerPanicTrigger.tick` **37**. Needs `wantsToSpawnGolem` (slept within 24000 ticks, no `GOLEM_DETECTED_RECENTLY` — **937–939**, **997–999**), ≥5 agreeing villagers in inflate(10), then `SpawnUtil.trySpawnMob(EntityType.IRON_GOLEM, MobSpawnType.MOB_SUMMONED, …, LEGACY_IRON_GOLEM)` **927–929**. Does **not** set `PlayerCreated`. | **No.** Village helper summon. **Not Villager biology.** iron_golem.md already owns this as a golem **creation path**. | Not a Villager BP field | Named **vanilla consumer of Villager**: Iron Golem spawn. BioCraft: none for a Villager golem-trait | **A** |
| Golem detection memory | `GolemSensor` | Exact `EntityType.IRON_GOLEM` **37–39**; `golemDetected` TTL 599 — detection, not lineage | No | Not needed | None (Iron Golem report owns this) | **A** |
| Raid / illager flee | Brain PANIC/PRE_RAID/RAID/HIDE + `VillagerHostilesSensor` | `Villager.java` **251–254**; panic walks from `NEAREST_HOSTILE` (`VillagerGoalPackages` **203–211**); sensor exact-type map (`VillagerHostilesSensor.java` **9–21**: drowned/evoker/husk/illusioner/pillager/ravager/vex/vindicator/zoglin/zombie/zombie_villager — **not** `#illager`, **not** `#raiders`). Raid bell/hide/celebrate in `getPreRaidPackage`/`getRaidPackage` **214–249**. Ambient raid particle `customServerAiStep` **304–308**. | **No.** Brain activities + exact-type fear table. Raid adjacency ≠ Illager clade. **Do not queue Ravager/Witch.** | Identity sufficient | None that needs a flee trait | **A** |
| Zombie infection (Villager side) | **`Zombie.killedEntity`** | `Zombie.java` **421–449**: victim `instanceof Villager`; NORMAL ~50% / HARD 100%; `villager.convertTo(EntityType.ZOMBIE_VILLAGER, false)`; copies VillagerData, gossips, offers, XP. Killer stays Zombie. Easy: none. | Conversion = entity replacement, not ancestry. Source identity does not remain a live BioCraft `villager` key on the ZV. | Distinct keys `villager` / `zombie_villager` already exist | None encodes this vanilla replacement as contribution | **A/B** |
| Cure reverse (destination of Villager) | `ZombieVillager.finishConversion` | `convertTo(EntityType.VILLAGER, false)` then copy data — `ZombieVillager.java` **224–258**. Independent Villager spawn/breed exist without ever being ZV. | Reverse replacement, not lineage | Distinct keys | None | **A/B** |
| Lightning → Witch | `Villager.thunderHit` | `Villager.java` **820–837**: non-PEACEFUL; `EntityType.WITCH.create`; copy pose/name/no-AI; `discard` Villager. Strike AABB owner is `LightningBolt` **156–165** (3-block box). | Conversion ≠ inheritance. **Do not queue Witch** from this adjacency or from raids. | Distinct destination key `witch` (out of this agent's scope to investigate) | None | **A** |
| Village structure spawn | Worldgen template pools | Resources jar `data/minecraft/worldgen/template_pool/village/*/villagers.json` + structure `village/*/villagers/*.nbt`. `finalizeSpawn` STRUCTURE sets `assignProfessionWhenSpawned` (`Villager.java` **795–797**) | Encounter ≠ origin | Identity sufficient | None | **A** |
| Village siege | `VillageSiege` | Spawns **`EntityType.ZOMBIE`**, not Villager (`VillageSiege.java` **102**, **121**) | Not Villager reproduction | N/A | None | **A** |
| Entity loot | `data/minecraft/loot_table/entities/villager.json` | `"type": "minecraft:entity"` + `random_sequence` only — **empty pools** | No | Not needed | None | **A** |
| HOTV gifts / farmer plant | Profession AI / item tag | `#minecraft:villager_plantable_seeds` consumed by `Villager.wantsToPickUp` **858–861**; gifts are raid-victory gameplay, not this loot table | Item/AI, not composition | Not needed | None | **A** |
| Entity-type tags | JSON membership | Resources-jar scan of `data/minecraft/tags/entity_type/*.json`: **no** `minecraft:villager` member (only `zombie_villager` inside `#zombies`). Java `EntityTypeTags` has no `VILLAGER` token in this extract | Tag ≠ clade; absence ≠ biology | Identity sufficient | No tag-driven BioCraft consumer | **A** |
| Xenomorph combat targeting | `StandardTargetingHelper` + `XenomorphTargetingHelper` | `NearestAttackableTargetGoal<>(…, AbstractVillager.class)` keyed `target_villager` (`StandardTargetingHelper.java` **51–54**; drone/queen JSON priority 3). `EntityKind.VILLAGER` if `instanceof AbstractVillager` (`NeoForgeEntityQueryAdapter.java` **123–124**) — **includes Wandering Trader**. Combat prey skip host-registry (`XenomorphTargetingHelper.java` **45–47**) | **No.** Entity-class combat AI, same pattern as `target_iron_golem` | Identity / Java class sufficient | Live combat AI. **A**, not a missing biological fact | **A** |
| **Live host → contributingSourceKey** | Host Registry + gestation + Analyzer | See Configuration audit. `hosts.json` `"villager"` → `HostType.LIVING_BIOLOGICAL` (`isSuitableForXenomorph==true`). Facehugger/ovomorph eligibility. `GestationManager.writeContributingSource` writes registry path `"villager"` onto Chestburster/Drone. Analyzer projects it. | Source **identity** only. Not profession, not golem, not raid | Existing `contributingSourceKey` | **LIVE** named consumers: eligibility, gestation copy, Analyzer | **B** |

No row is **C**.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` key `"villager"` under `vanilla_hosts.living_biological` | **LIVE** | `hosts.json` **6**; parser `HostConfigParser.parseGroup` **97**, **141–143** maps mob → `HostType.LIVING_BIOLOGICAL`, `default_dna` `baseline_biological` | Registered participation. Can originate production contribution. **Not** a profession/golem/raid field |
| `MobHostRegistry.getHostType("villager")` | **LIVE** | `MobHostRegistry.java` **46–48**, **68–71** | Returns `LIVING_BIOLOGICAL`; `isSuitableForXenomorph("villager")==true` |
| `HostType.LIVING_BIOLOGICAL.isSuitableForXenomorph()` | **LIVE** | `HostType.java` **17**, **44–46** | Suitability **true**. Contrast: Hoglin/Piglin unregistered → null HostType → facehugger false. Host Registry ≠ extra eligibility science |
| `HostEligibilityService` | **LIVE** generic | `isSuitableForXenomorph` / `isValidFacehuggerHost` **19–44**: `encodeId` → `HostRegistryPaths.registryPath` (`minecraft:villager` → `villager`) | Named live gate. Villager passes. Wandering Trader encodeId `wandering_trader` is **unregistered** → false |
| Facehugger attachment | **LIVE** | `HostValidationHelper.isValidHostForFacehugger` **18–19**; `FacehuggerAttachmentPersistence.restoreLatchedHostFromUUID` **128–129** | Uses eligibility. Villager is a valid current host |
| Ovomorph host selection | **LIVE** | `OvomorphHostSelectionPolicy.isViableHost` **31** | Same eligibility; Villager eligible |
| `GestationManager.writeContributingSource` | **LIVE** | `GestationManager.java` **147–175**: spawn Chestburster then `encodeId(host)` → `HostRegistryPaths.registryPath` → `ContributingSourceKeys.absentIfBlank` → `ContributingSourcePort.setContributingSourceKey` | **This is the production writer.** A gestated Villager host yields `contributingSourceKey="villager"` on Model A carriers. Same machinery as Cow/Human. No new field |
| `DnaSampleFromOccupant` | **LIVE** | `DnaSampleFromOccupant.java` **30–59**: xenomorph form → form configKey as `organismKey`; else registry path. Contribution only if `ContributingSourcePort.supports` (Chestburster/Drone carriers) | Sampling a live Villager: `organismKey=villager`, no source key. Sampling offspring of Villager host: `organismKey=chestburster|drone`, `contributingSourceKey=villager` |
| `BiologicalProfileResolver` | **LIVE** generic | `BiologicalProfileResolver.java` **35–56**: `organismKey=villager` → HostType `LIVING_BIOLOGICAL`, `hostEffectProfileId=baseline_biological`, empty form/behavior; optional source key passed through | No Villager-specific branch. Identity + HostType refs |
| Analyzer `BiologicalProfileDnaAnalysisPort` | **LIVE** | **39–41** projects compiled profile including contributing source | Identity/source display. Tests prove Cow vs Human differ **only** on source key (`BiologicalProfileDnaAnalysisPortTest` **54–67**). Villager is the same contract with key `"villager"` — **no villager-named unit test**, but the port is not stubbed |
| `HostEffectManager` + `baseline_biological.json` | **LIVE** host-effect pack | Registry routes Villager to `baseline_biological`; JSON immobilize + blindness/weakness/hunger/slowdown | Attachment-time effects shared with other living hosts. **Not** Villager genetics |
| `StandardTargetingHelper` `target_villager` | **LIVE** combat AI | Drone/queen JSON; `AbstractVillager.class` | AI targeting, not composition (**A**) |
| `HumanEntityType.VILLAGER` / `DefensiveVillagerAI` / `defensive_villager.json` | **LIVE Human factory, not Minecraft Villager** | `HumanEntityType.java` **15**; `HumanAIBehaviorFactory` **42–55**; `BehaviorDispatchContractTest` allowlists `defensive_villager` **without** entity `behavior_type` ref; README: shipped for human dispatch | Homonym. Human `encodeId` is `biocraft_alien:human` → source key `"human"`. Do **not** treat as Villager BP |
| `hosts.json` `"human"` under `modded_hosts.biocraft_alien.living_biological` | **LIVE** separate key | `hosts.json` **40–44** | Distinct from `"villager"` |
| Villager entity JSON / DNA / behavior_type | **ABSENT** | No `entity/.../villager.json` in production catalog | Vanilla remains behavior owner |
| Resolver/host tests named `"villager"` | **TEST coverage absent** (generic LIVE) | `BiologicalProfileResolverTest` asserts cow/sheep/creeper living hosts, not villager; `MobHostRegistryTest` uses pig | Same living-host contract would apply; absence of a named test is not a missing biological fact |
| `laboratory.md` Villager row | **PLANNING** | “Contain + observe; no special lab fork” | Lab genericity, not a C-level trait |
| Wandering Trader in Host Registry | **ABSENT** | No `"wandering_trader"` in `hosts.json` | Separate EntityType; unregistered ≠ merge into Villager |

---

## Tempting but rejected interpretations

- **Profession / trades / gossip / POI as biological traits.** Owned by `VillagerData`, merchant offers, `GossipContainer`, and POI memories. Survives ZV conversion as **destination Minecraft entity state**, not a BioCraft field (zombie_villager.md already recorded this; re-verified on Villager side).
- **`Villager.spawnGolemIfNeeded` as Villager biology or a Villager BP field.** Iron Golem creation path. iron_golem.md owns it as golem creation. Record Villager as a **named vanilla consumer/trigger**, not composition.
- **Raid flee / `#illager` / Raider adjacency as an Illager relationship or queue for Ravager/Witch.** Panic uses an **exact EntityType map**. Witch is lightning conversion, not raid membership. Do not queue.
- **Villager → Zombie Villager as ancestry or a conversion-source clade with Hoglin/Piglin.** `Zombie.killedEntity` replaces the Villager. Killer is a trigger agent. Conversion ≠ inheritance. Hoglin/Piglin are unrelated Nether conversion sources; Villager is not in that clade.
- **Lightning → Witch as a Villager biological product.** `thunderHit` replacement. Do not investigate Witch here.
- **`AbstractVillager` / `EntityKind.VILLAGER` as license to absorb Wandering Trader.** Separate `EntityType`, `CREATURE` vs `MISC`, `getBreedOffspring` returns **null** (`WanderingTrader.java` **100–103**), separate spawner `WanderingTraderSpawner`, not in `hosts.json`. Shared merchant parent is implementation.
- **`HumanEntityType.VILLAGER` / `defensive_villager` as Minecraft Villager biology.** Human factory routing. Live Human registry path is `human`.
- **Host Registry registration as eligibility science or a new BP dimension.** Registration enables the existing host path. Suitability is `HostType.LIVING_BIOLOGICAL`. No new field.
- **Xenomorph `target_villager` as a missing biological fact.** Combat class goal. Same A-pattern as Iron Golem targeting.
- **Village biome / structure spawn as origin.** Worldgen encounter + egg/summon/breed still create `EntityType.VILLAGER`.
- **Empty loot vs wiki “profession drops” as residual composition.** Entity loot table has no pools. HOTV gifts are a different gameplay owner.
- **Breeding as xenomorph contribution.** Same-type vanilla `AgeableMob` path. Child key remains `villager`.
- **Interesting merchant/village behavior as a consumer.** No live BioCraft system asks for profession, gossip, or POI as biology.

---

## Potential biological relationships

### 1. Villager as live xenomorph host / Model A contributing source

- **Relationship:** Facehugger/ovomorph may select Villager; gestation copies host registry path onto Chestburster/Drone; Analyzer displays it.
- **Owner:** `hosts.json` + `HostEligibilityService` + `GestationManager.writeContributingSource` + `DnaSampleFromOccupant` / Analyzer.
- **Biological input?** Only the organism-definition key `"villager"`.
- **Existing composition:** `organismKey` on the Villager sample; optional `contributingSourceKey="villager"` on Model A offspring. `HostType.LIVING_BIOLOGICAL` + `hostEffectProfileId=baseline_biological` already resolve.
- **Named consumer:** **LIVE** — eligibility, gestation writer, Analyzer projection.
- **Result:** **B**. This is the difference vs Hoglin/Piglin (unregistered; production origin blocked). Not C.

### 2. Villager → Zombie Villager (infection)

- **Relationship:** Kill conversion. Source Villager discarded; destination `ZOMBIE_VILLAGER` with copied merchant NBT.
- **Owner:** `Zombie.killedEntity` (`Zombie.java` **421–449**), not Villager methods.
- **Biological input?** Replacement, not ancestry. Profession copy is entity state.
- **Existing composition:** Distinct keys already named.
- **Named consumer:** None in BioCraft encodes this replacement.
- **Result:** **A/B**. Do not treat as Hoglin/Piglin conversion clade.

### 3. Zombie Villager → Villager (cure)

- **Relationship:** Reverse replacement (`ZombieVillager.finishConversion` **224–258**).
- **Owner:** Zombie Villager + golden-apple/weakness timer (ZV report).
- **Biological input?** No.
- **Existing composition:** Distinct keys.
- **Named consumer:** None.
- **Result:** **A/B**. Villager independent existence (spawn/breed) is not disproof and not ancestry.

### 4. Villager → Iron Golem (creation trigger)

- **Relationship:** Village helper summon.
- **Owner:** `Villager.spawnGolemIfNeeded` → `SpawnUtil.trySpawnMob(EntityType.IRON_GOLEM, …)`.
- **Biological input?** No. Not parentage (iron_golem.md).
- **Existing composition:** Golem identity is `iron_golem`; not a Villager field.
- **Named consumer:** Vanilla Iron Golem creation. BioCraft combat may target Iron Golem separately. **Not** a Villager BP consumer.
- **Result:** **A**. Record as named vanilla consumer of Villager, not a Villager BP field.

### 5. Villager → Witch (lightning)

- **Relationship:** `Villager.thunderHit` replaces with `EntityType.WITCH`.
- **Owner:** Lightning + Villager conversion hook.
- **Biological input?** Conversion ≠ inheritance.
- **Existing composition:** Distinct destination key.
- **Named consumer:** None. **Do not queue Witch.**
- **Result:** **A**.

### 6. Villager ↔ Wandering Trader

- **Relationship:** Shared `AbstractVillager` merchant parent; BioCraft combat class `AbstractVillager`; Wandering Trader even checks `Items.VILLAGER_SPAWN_EGG` in `mobInteract` (**113**) as an item gate.
- **Owner:** Two EntityTypes (`VILLAGER` MISC vs `WANDERING_TRADER` CREATURE).
- **Biological input?** Shared parent ≠ clade. Trader does not breed (`getBreedOffspring` null). Trader unregistered as host.
- **Existing composition:** Distinct keys; do not merge.
- **Named consumer:** Combat AI hits both via parent class — still A.
- **Result:** **A**. Do not absorb Wandering Trader.

### 7. Villager ↔ BioCraft Human (`HumanEntityType.VILLAGER`)

- **Relationship:** Name collision only.
- **Owner:** `HumanEntity` / `EntityInit.HUMAN` `"human"` vs `EntityType.VILLAGER`.
- **Biological input?** None shared.
- **Existing composition:** Host keys `"villager"` vs `"human"`.
- **Named consumer:** Human AI factory (`defensive_villager`) is not a Minecraft Villager consumer.
- **Result:** **A**. Closed leap: enum configKey ≠ vanilla organism.

### 8. Raid / illager fear table

- **Relationship:** Villagers flee listed hostile types; illagers target `AbstractVillager`.
- **Owner:** `VillagerHostilesSensor` exact map; illager `NearestAttackableTargetGoal`.
- **Biological input?** Faction AI. Tag ≠ clade.
- **Existing composition:** Distinct organism keys.
- **Named consumer:** None for a fear trait. **Do not queue Ravager/Witch.**
- **Result:** **A**.

---

## Wiki orientation disagreements

Source: [minecraft.wiki/w/Villager](https://minecraft.wiki/w/Villager) (orientation only). 1.21.1 mapped source wins.

| Wiki orientation | 1.21.1 authority | Conclusion |
|------------------|------------------|------------|
| “Humanoid **passive** mobs” | `MobCategory.MISC`, not `CREATURE`. Panic/raid/hide are dedicated activities | Gameplay wording. Category is MISC |
| Lightning “within 3–4 blocks” turns villager into witch | `LightningBolt` AABB is **3** blocks horizontal, Y−3 to Y+6+3 (`LightningBolt.java` **156–160**); Villager `thunderHit` then `WITCH.create` | Nearby-strike is the bolt’s entity list, not a Villager-radius trait. Distance is the bolt AABB, not a biological radius |
| Profession / biome outfit as identity | Identity is `EntityType.VILLAGER`. Profession/type are `VillagerData` | Presentation/state, not BP |
| Entity drops by profession / HOTV gifts as villager loot | `loot_table/entities/villager.json` has **no pools**. Gifts are raid-victory behavior | Do not treat gifts as organism loot/composition |
| Bedrock profession/census/breeding differences | Not this Java 1.21.1 pass | Do not import Bedrock |
| Igloo-basement generated villager always unemployed (JE) | Structure-specific; infection path **copies** `getVillagerData()` | Context-specific wiki; infection retains profession as NBT |
| Wandering Trader discussed as related villager | Separate EntityType `wandering_trader` / `CREATURE` | Do not merge |
| Iron Golem “village spawning” as villager nature | `spawnGolemIfNeeded` is a summon helper | Vanilla consumer of Villager, owned as golem creation |

---

## Final evidence conclusion

Villager is a distinct 1.21.1 organism (`EntityType.VILLAGER`, `MISC`, 0.6×1.95, eyeHeight 1.62). Profession, trades, gossip, POI, breeding, raid flee, and lightning/zombie conversions are Minecraft-owned. Iron Golem creation is a **named vanilla consumer** of Villager (`spawnGolemIfNeeded`), already owned by iron_golem.md as a golem path — not a Villager BP field.

The live BioCraft difference vs Hoglin/Piglin: Villager is **registered** `LIVING_BIOLOGICAL` and **does** originate production `contributingSourceKey="villager"` through eligibility → gestation copy → Analyzer. That consumer asks only for the existing organism-definition key. No profession, golem, raid, or conversion fact is missing.

**C is not earned.** Do not add a field. Do not absorb Wandering Trader. Do not queue Ravager/Witch. Do not treat this as a Hoglin/Piglin conversion-source clade.

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** |
| Named consumer exists | **YES** (live host/gestation/Analyzer identity-source path; combat targeting is A) |
| Architectural escalation required | **NO** |

### 1.21.1 authority anchors

- `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` **710–718** — `VILLAGER` / `WANDERING_TRADER`
- `.tmp_mc_sources/net/minecraft/world/entity/npc/Villager.java` — identity class, brain, gossip, `spawnGolemIfNeeded`, breeding, `thunderHit`
- `.tmp_mc_sources/net/minecraft/world/entity/npc/AbstractVillager.java` — shared merchant parent
- `.tmp_mc_sources/net/minecraft/world/entity/npc/WanderingTrader.java` — separate type; `getBreedOffspring` null
- `.tmp_mc_sources/net/minecraft/world/entity/monster/Zombie.java` **421–449** — Villager→ZV
- `.tmp_mc_sources/net/minecraft/world/entity/monster/ZombieVillager.java` **224–258** — cure
- `.tmp_mc_sources/net/minecraft/world/entity/ai/sensing/VillagerHostilesSensor.java` — exact-type flee map
- `.tmp_mc_sources/net/minecraft/world/entity/ai/behavior/VillagerMakeLove.java` — breed owner
- `.tmp_mc_sources/net/minecraft/world/entity/LightningBolt.java` **156–165** — strike AABB
- Resources jar `data/minecraft/loot_table/entities/villager.json` — empty pools
- AlienCraft: `hosts.json`; `HostConfigParser.java`; `MobHostRegistry.java`; `HostType.java`; `HostEligibilityService.java`; `HostRegistryPaths.java`; `GestationManager.java`; `DnaSampleFromOccupant.java`; `BiologicalProfileResolver.java`; `BiologicalProfileDnaAnalysisPort.java`; `HostValidationHelper.java`; `StandardTargetingHelper.java`; `NeoForgeEntityQueryAdapter.java`

Prior destination/golem reports verified independently, not copied blindly: `docs/design/biological/manifestations/zombie_villager.md`, `iron_golem.md`.
