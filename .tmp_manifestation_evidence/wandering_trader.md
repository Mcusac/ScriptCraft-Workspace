TEMPORARY EVIDENCE — NOT PROJECT SSOT
BioCraft: Alien biological-manifestation investigation packet
Do not treat this file as canonical design documentation.
Do not promote into manifestations/wandering_trader.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004 without the authorized Phase 3 pass.
Do **not** register Wandering Trader as a conclusion of this investigation.
Do **not** mint `DESIGN-BIO-MANIFEST-004`.

# Wandering Trader — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**This pair is evidence-management / accounting closeout of a pending bio-organic inventory row.** It is **not** a merchant clade, villager family, item-production column, leftover biological group, or trader-llama ancestry continuation. Do **not** assume Sniffer conclusions. Do **not** queue this organism from trader_llama adjacency: trader llama already closed caravan/leash from the llama side.

Method (every behavior): owner → biological input? → existing composition? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

**Four-way consumer audit** (exactly one per tempting behavior):

| Class | Meaning | Typical A/B/C |
|-------|---------|---------------|
| **1** | No BioCraft consumer exists | usually **A** |
| **2** | Consumer exists but does not consume Biological Profile | usually **A** |
| **3** | Consumer consumes BP; existing composition already represents the fact | **B** |
| **4** | Consumer consumes BP and composition genuinely lacks a biological fact | only path that can become **C** |

**C threshold (hard gate):** a concrete, currently live BioCraft consumer whose correct behavior cannot be represented by existing Biological Profile composition, and whose required input is genuinely biological rather than implementation/state/behavior/lifecycle. Analyzer existence plus an interesting Minecraft mechanic does **not** earn a BP fact.

Closed leaps applied independently: shared Java parent (`AbstractVillager`) ≠ clade; same outer size ≠ shared anatomy; spawn/leash ≠ origin; conversion of `Villager` ≠ conversion of Wandering Trader; shared merchant helper ≠ biological family; trades ≠ capability; despawn ≠ biological death; night invisibility potion ≠ stealth trait; Host Registry absence ≠ automatic A/B and is **not** a registration order; `HumanEntityType.VILLAGER` homonym ≠ this organism.

Existing BP composition tested first (no invented fields): `organismKey`, fail-soft unregistered key, optional `contributingSourceKey`, sparse `CompiledBiologicalProfile` fields (`HostType`, xenomorph form key, host-effect id, behavior type).

**Default: NO new BP field.** Do **not** absorb Villager, Witch, Trader Llama, Illager, or Sniffer.

---

## Subject

Wandering Trader (`minecraft:wandering_trader`) — Minecraft Java **1.21.1** independent organism. Distinct `EntityType` vs Villager. `WanderingTrader extends AbstractVillager` is implementation sharing, **not** clade. Investigated for identity, merchant-table trades, TRADE_REBALANCE optional path, night/day potion AI, despawn timer, CustomSpawner + llama leash remainder, negative conversions, Host Registry **absence**, and whether any live BioCraft consumer needs a missing biological fact.

Out of scope as organisms: Villager (adjacency control only), Witch (adjacency control only), Trader Llama (caravan/leash already closed), Illagers, Sniffer.

---

## Version

- Target: `minecraft_version_range=[1.21.1,1.22)` (`biocraft-alien/gradle.properties`)
- Authoritative mapped sources: Minecraft Java **1.21.1** / NeoForge **21.1.208**
- Temporary source cache (not SSOT): `.tmp_mc_sources/` extracted this pass from `implementations/minecraft/AlienCraft/biocraft-alien/build/moddev/artifacts/neoforge-21.1.208-sources.jar` and `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar` (also Gradle cache `net.neoforged:neoforge:21.1.208`)
- Wiki: orientation / disagreement discovery only; **1.21.1 source wins**. Later-version trade tables (pale oak / 1.21.5 “rebalance now default”) are **not** imported.

---

## Target identity

| Field | 1.21.1 evidence |
|-------|-----------------|
| Registry | `EntityType.WANDERING_TRADER` register `"wandering_trader"` — `EntityType.java` **717–719** |
| Builder | `EntityType.Builder.of(WanderingTrader::new, MobCategory.CREATURE).sized(0.6F, 1.95F).eyeHeight(1.62F).clientTrackingRange(10)` |
| Category | **`MobCategory.CREATURE`**. Villager is **`MobCategory.MISC`** (`EntityType.java` **710–712**). Same outer size, **different category** |
| Fire / lava | Builder does **not** call `.fireImmune()` |
| Java type | `WanderingTrader extends AbstractVillager` — `WanderingTrader.java` **49**. Does **not** implement `VillagerDataHolder` or `ReputationEventHandler` |
| Parent chain | `WanderingTrader` → `AbstractVillager` (`AgeableMob` + `InventoryCarrier` + `Npc` + `Merchant`) — `AbstractVillager.java` **40** |
| Attributes | `DefaultAttributes.java` **164**: `EntityType.WANDERING_TRADER` → **`Mob.createMobAttributes().build()`**. Villager is **`Villager.createAttributes()`** (**161**): speed **0.5**, follow **48.0** (`Villager.java` **269–271**). Same hitbox ≠ shared attribute supplier |
| Spawn placement | `SpawnPlacements.java` **173**: `ON_GROUND` / `MOTION_BLOCKING_NO_LEAVES` / `Mob::checkMobSpawnRules` (same placement family as Villager **147**, different category) |
| Spawn egg | `Items.WANDERING_TRADER_SPAWN_EGG` `"wandering_trader_spawn_egg"` — `Items.java` **1514–1515** |
| Host Registry | **ABSENT** from `hosts.json`. Adjacent `"villager"` is registered `living_biological` (**6**). Do **not** register from this packet. Absence ≠ automatic A/B |
| Inventory (planning only; not edited) | `wandering_trader` / bio-organic / unregistered / manifestation pending |
| Entity-type tags | **No** `data/minecraft/tags/entity_type/*.json` member `wandering_trader` (resources-jar scan of 34 tags) |
| Loot | `data/minecraft/loot_table/entities/wandering_trader.json`: entity type + `random_sequence` only — **no pools / no drops** |

Independent existence paths (not origin): spawn egg / `/summon`; overworld `WanderingTraderSpawner` `MobSpawnType.EVENT`. Trader llamas are a **spawn/leash remainder**, not biological origin (closed on trader_llama side).

```text
WanderingTrader does X
    → Minecraft entity / merchant table / CustomSpawner / AI / conversion owner owns X?
    → Wandering Trader biological composition contributes something to X?
    → a live AlienCraft consumer needs that distinction beyond fail-soft organismKey?
```

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP representation? | Four-way consumer class | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|----------------------------|-------------------------|--------------------|-------|
| Distinct identity vs Villager | `EntityType.WANDERING_TRADER` | `EntityType.java` **717–719**: `"wandering_trader"`, **CREATURE**, `0.6F×1.95F`, eyeHeight `1.62F`. Villager is separate `"villager"` **MISC** **710–712** | Identity only | Fail-soft `organismKey = wandering_trader` | **3** | LIVE generic resolver / Analyzer projection (empty HostType optionals) | **B** |
| `extends AbstractVillager` | Class inheritance | `WanderingTrader.java` **49**; `AbstractVillager.java` **40**: merchant offers, 8-slot inventory, `canBeLeashed() == false` (**225–227**) | Implementation sharing ≠ clade | Distinct keys (`wandering_trader` vs `villager`) | **2** | LIVE combat class filter `AbstractVillager` (see targeting). Does **not** read BP | **A** |
| Same outer size as Villager | `EntityType` builders | Both `sized(0.6F, 1.95F).eyeHeight(1.62F)` | **No.** Hitbox coincidence. Attributes **differ** (`Mob.createMobAttributes` vs Villager speed 0.5 / follow 48) | Identity does not encode anatomy; anatomy contract is **not yet** (`system.md` §C) | **1** | None needing a shared-anatomy field | **A** |
| Default attributes | `DefaultAttributes` | **164** `Mob.createMobAttributes()` = living defaults + follow **16** (`Mob.java` **159–160**). Not `Villager.createAttributes` | **No.** Numeric attr table | Soft key sufficient | **1** | None | **A** |
| `getBreedOffspring` returns null | `WanderingTrader.getBreedOffspring` | `WanderingTrader.java` **99–103** returns **null**. `AgeableMob.canBreed()` default **false** (`AgeableMob.java` **53–55**). Load clamps `setAge(Math.max(0, getAge()))` (**182**) | **No.** Explicit non-breeding vs Villager `getBreedOffspring` creating `EntityType.VILLAGER` | Identity sufficient (organism does not breed) | **1** | None needing a sterility trait | **A** |
| Trades (default 1.21.1 path) | `WanderingTrader.updateTrades` + `VillagerTrades.WANDERING_TRADER_TRADES` | `WanderingTrader.java` **134–150**: if **not** `FeatureFlags.TRADE_REBALANCE`, pool **1** → 5 offers (`NUMBER_OF_TRADE_OFFERS`), pool **2** → 1 random offer. Tables at `VillagerTrades.java` **662–740**. **Not** profession NBT / `VillagerData` | **No.** Merchant offer tables + `Offers` NBT (`AbstractVillager` **165–176**) | Not needed. “Trader trades → capability” rejected | **1** | None as biology | **A** |
| Trades (TRADE_REBALANCE experimental path) | `experimentalUpdateTrades` + `VillagerTrades.EXPERIMENTAL_WANDERING_TRADER_TRADES` | `WanderingTrader.java` **135–136**, **153–159**. Experimental list `VillagerTrades.java` **1252+**: three `Pair` pools maxNumbers **2 / 2 / 5**. Flag **default-off** (see configuration audit) | **No.** Optional 1.21.1 feature-pack trade table, not a later-version import | Not needed | **1** | None | **A** |
| Night invisibility / day milk | `UseItemGoal` in `registerGoals` | `WanderingTrader.java` **62–80**: night + not invisible → `Potions.INVISIBILITY` potion; day + invisible → `Items.MILK_BUCKET`. Goal owner `UseItemGoal.java` **18–47** (equip / `startUsingItem` / clear slot) | **No.** AI + item use, not a stealth trait | Not needed | **1** | None | **A** |
| Avoid / panic AI | `AvoidEntityGoal` + `PanicGoal` | `WanderingTrader.java` **83–90**: Zombie (8), Evoker (12), Vindicator (8), Vex (8), Pillager (15), Illusioner (12), Zoglin (10), Panic 0.5. **No** Ravager. Husk/Drowned/ZV match via `Zombie.class` | **No.** Combat AI taxonomy | Identity of those types | **1** | None needing a fear BP field | **A** |
| DespawnDelay 48000 + discard | Spawner sets delay; `maybeDespawn` owns discard | `WanderingTraderSpawner.java` **113** `setDespawnDelay(48000)`; `WanderingTrader.maybeDespawn` **244–247** decrements when not trading and `discard()` at 0. NBT `"DespawnDelay"` **165**. `removeWhenFarAway` **false** (**186–188**) | **No.** Encounter lifecycle, not biological death | Not needed. “Trader despawns → lifecycle profile” rejected | **1** | None | **A** |
| CustomSpawner spawn | `WanderingTraderSpawner` on **overworld only** | `MinecraftServer.createLevels` **363–368**: CustomSpawner list including `new WanderingTraderSpawner(serverleveldata)` passed only to **OVERWORLD** `ServerLevel`. Tick: `RULE_DO_TRADER_SPAWNING` (`GameRules.java` **157–158**, default **true**), delay 24000, chance 25–75, 1-in-10 after player, meeting `PoiTypes.MEETING` within 48, `#without_wandering_trader_spawns` (`BiomeTags.java` **67**; JSON = `minecraft:the_void` only), then `EntityType.WANDERING_TRADER.spawn(..., EVENT)` | **No.** World spawn system. Spawn ≠ origin | Soft key sufficient | **1** | None | **A** |
| Two trader llamas + leash | `tryToSpawnLlamaFor` | `WanderingTraderSpawner.java` **108–110**, **124–131**: two `EntityType.TRADER_LLAMA.spawn(..., EVENT)` then `setLeashedTo(trader, true)` | **No.** Spawn/leash remainder. Trader llama already closed caravan/leash from llama side | Distinct `trader_llama` key already fail-soft; do not re-open as origin | **1** | None needing caravan-as-origin | **A** |
| Llama defend / despawn sync (remainder) | `TraderLlama` | `TraderLlama.maybeDespawn` **84–91** copies trader DespawnDelay when leashed; `TraderLlamaDefendWanderingTraderGoal` **120–141**; ride blocked if leashed to trader **69–73** | **No.** Trader-lifecycle on llama entity. Not wandering-trader biology | Closed in trader_llama evidence | **1** | None | **A** |
| Zombie infection **negative** | `Zombie.killedEntity` | `Zombie.java` **421–428**: `entity instanceof Villager villager` only, then `convertTo(ZOMBIE_VILLAGER, false)`. `WanderingTrader` **is not** `Villager`. Husk/Drowned inherit this method | **No conversion.** Death is ordinary. Conversion of Villager ≠ conversion of Wandering Trader | Distinct keys already | **1** | None | **A** |
| Lightning → Witch **negative** | No `WanderingTrader.thunderHit` override | `WanderingTrader.java` has **no** `thunderHit`. Default `Entity.thunderHit` **2511–2517**: fire ticks + lightning damage. Witch factory is **`Villager.thunderHit` only** (`Villager.java` **820–843**) | **No conversion.** Lightning is not Villager→Witch for this type | Distinct keys | **1** | None; do not reopen Witch | **A** |
| Host Registry absence | `hosts.json` | No `"wandering_trader"` key. `"villager"` present **6**. `MobHostRegistry.getHostType("wandering_trader")` → **null**. `isSuitableForXenomorph` → **false** (**46–48**, **68–71**) | Participation gap, not missing biology. Unregistered ≠ ineligible-as-biology ≠ BP field | Fail-soft `organismKey`; empty `HostType` / host-effect optionals | **3** (resolver) / **2** (eligibility) | LIVE fail-soft resolver; LIVE eligibility uses registry not BP. **Do not register** | **B** (identity) / **A** (gameplay participation) |
| Analyzer / DNA page | `BiologicalProfileDnaAnalysisPort` | Projects compiled refs only (`BiologicalProfileDnaAnalysisPort.java` **30–41**). Unregistered key → organismKey preserved, empty optionals (`BiologicalProfileResolver.java` **23**, **41–56**; test `unknownKeyPreservesOrganismKeyWithEmptyOptionals`) | Identity projection only | Existing sparse payload | **3** | LIVE Analyzer / Pen-Pod DNA UI. Does **not** need trades/despawn/invisibility as BP facts | **B** |
| Xenomorph `AbstractVillager` targeting | `StandardTargetingHelper` + `NeoForgeEntityQueryAdapter` | `NearestAttackableTargetGoal<>(…, AbstractVillager.class, …)` `StandardTargetingHelper.java` **51–54**. `instanceof AbstractVillager` → `EntityKind.VILLAGER` `NeoForgeEntityQueryAdapter.java` **123–124**. `XenomorphTargetingHelper` treats `EntityKind.VILLAGER` as combat prey **without** hosts.json lookup **45–47** | **No.** Java class combat taxonomy. Lumps WanderingTrader with Villager for **AI targeting only** | Soft keys already distinct; targeting does not read them | **2** | LIVE combat. Does **not** consume BP. Not a missing biological fact | **A** |
| Capture / admission | `CaptureEligibilityPolicy` | `canCapture(alive, !player)` — wandering trader is capturable as a living non-player. Does not branch on trader biology | Admission identity, not extra biology | `organismKey` from encode-id path | **2** (policy) / **3** (later Analyzer) | LIVE generic capture. No wandering_trader-named writer | **A** / **B** |
| Gestation contributing source | `HostEligibilityService` + `GestationManager.writeContributingSource` | Facehugger host gate uses `MobHostRegistry.isSuitableForXenomorph` — unregistered → **false**. Writer (**164–175**) copies encode-id path if gestation occurred; **no** production wandering_trader host path | No live Model A source from this organism | Fail-soft identity if a key were supplied; it is not produced here | **2** | LIVE generic writer; **no** wandering_trader production source | **A** |
| `HumanEntityType.VILLAGER` | Human factory enum | `HumanEntityType.java` **15**: config key `"villager"` / entity `"human_villager"`. Live Human encode-id is `biocraft_alien:human` | Homonym, **not** `EntityType.WANDERING_TRADER` and **not** `EntityType.VILLAGER` | Do not treat as this organism | **2** | LIVE Human subtype. Wrong organism | **A** |

No row is **C**. No row is four-way class **4**.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"wandering_trader"` | **ABSENT** | `vanilla_hosts.living_biological.mobs` has `"villager"` (**6**), not `"wandering_trader"`. No undead / unsuitable / modded / `variant_mappings` entry | Do **not** register. Absence is participation evidence, not a BP field and not a registration order |
| `"villager"` adjacent | **LIVE** | `hosts.json` **6**; `HostType.LIVING_BIOLOGICAL` | Distinct keys ≠ register-wandering-trader mandate |
| `MobHostRegistry.getHostType("wandering_trader")` | **LIVE** (null) | `MobHostRegistry.java` **46–48** | Unregistered → not suitable. Unregistered ≠ extra biology |
| `BiologicalProfileResolver` | **LIVE** generic fail-soft | Preserves non-blank key; empty HostType / form / effect / behavior (`BiologicalProfileResolver.java` **23**, **41–56**) | Projects `organismKey = wandering_trader` if asked. No trader-lifecycle field |
| Analyzer `DnaAnalysisPort` | **LIVE** | `BiologicalProfileDnaAnalysisPort` + `DnaAnalysisReport.fromCompiled`; Pen/Pod DNA pages same projection | Consumer of compiled refs. Genome remains `unknown()`. Not a missing-fact consumer |
| `HostEligibilityService` | **LIVE** | Unregistered → `isSuitableForXenomorph` false | Gestation participation uses Host Registry, **not** BP |
| `GestationManager.writeContributingSource` | **LIVE** generic | After Chestburster spawn, encode-id path of **host** | No production wandering_trader host, so no production `contributingSourceKey=wandering_trader` |
| `StandardTargetingHelper` `AbstractVillager` | **LIVE** combat | `StandardTargetingHelper.java` **51–54**; xenomorph JSON slot `target_villager` is a **goal-priority key**, not this EntityType | Class **2**: exists, does not consume BP |
| `NeoForgeEntityQueryAdapter` `EntityKind.VILLAGER` | **LIVE** combat classify | `instanceof AbstractVillager` | Homonym of “villager” kind. Not BP. Not Host Registry |
| `HumanEntityType.VILLAGER` / `defensive_villager.json` | **LIVE** Human factory | Enum + AI behavior JSON | Homonym. Not Minecraft Wandering Trader |
| Wandering Trader entity JSON / DNA JSON | **ABSENT** | No production config named wandering_trader; empty `data/biocraft_alien/dna/` is **not** live SSOT (`dna.md`) | Vanilla remains merchant/AI/spawn owner |
| Production Java/resources named `wandering_trader` / `WanderingTrader` | **ABSENT** | `rg` over `biocraft-alien/src` (excluding inventory planning markdown) | Inventory row is **PLANNING** only |
| Resolver unknown-key test | **TEST** | `BiologicalProfileResolverTest.unknownKeyPreservesOrganismKeyWithEmptyOptionals` | Generic fail-soft proof. **No** wandering_trader-named unit test |
| `FeatureFlags.TRADE_REBALANCE` | **default-OFF** in 1.21.1 | `FeatureFlags.java` **31–40**: `VANILLA_SET = of(VANILLA)`; **`DEFAULT_FLAGS = VANILLA_SET`**. `TRADE_REBALANCE = createVanilla("trade_rebalance")` is **not** in `VANILLA_SET`. `WorldDataConfiguration.DEFAULT` uses `FeatureFlags.DEFAULT_FLAGS` (`WorldDataConfiguration.java`). `DataPackConfig.DEFAULT` enables **`"vanilla"` only** | Optional experimental 1.21.1 path via built-in datapack `data/minecraft/datapacks/trade_rebalance/pack.mcmeta` (`features.enabled: minecraft:trade_rebalance`). **Do not import 1.21.5 “now default” wiki** |
| `RULE_DO_TRADER_SPAWNING` | default **true** | `GameRules.java` **157–158** | Spawn gamerule, not biology |
| `#without_wandering_trader_spawns` | **LIVE vanilla tag** | JSON values: `minecraft:the_void` only | Spawn exclusion, not origin |
| Entity loot | empty table | `wandering_trader.json` type + random_sequence only | No drop biology |
| `kill_a_mob` / `kill_all_mobs` | **ABSENT** wandering_trader | Advancement JSON has `zombie_villager`, not this type | Advancement taxonomy, not BP |

**Live vs other classifications (never promote stubs/parse-only into SSOT):**

| Surface | Classification |
|---------|----------------|
| `hosts.json` absence / villager presence | **LIVE** participation SSOT |
| Resolver + Analyzer + DNA UI | **LIVE** |
| Host eligibility / gestation writer | **LIVE** generic |
| AbstractVillager targeting / EntityKind.VILLAGER | **LIVE** combat (not BP) |
| Human `VILLAGER` enum / `defensive_villager` | **LIVE** wrong organism (homonym) |
| Resolver unknown-key JUnit | **TEST** |
| Inventory row | **PLANNING** |
| `data/biocraft_alien/dna/` | **DEAD** / not live SSOT |
| Organism-specific wandering_trader profile/JSON | **ABSENT** (not a stub to promote) |

---

## Tempting but rejected interpretations

| Tempting reading | Why rejected |
|------------------|--------------|
| Villager / merchant / illager clade because `AbstractVillager` | Shared merchant helper ≠ biological family. Distinct EntityType, category, attributes, no `VillagerData`, no profession, no gossip/POI/brain |
| Register because Villager is registered | Host Registry is participation, not ancestry. Absence is not a registration order |
| Same 0.6×1.95 hitbox → shared anatomy BP | Anatomy is **not yet** a domain contract. Attribute suppliers already differ. Same size ≠ shared anatomy |
| Trades as Biological Profile capability | Merchant tables + NBT. Gameplay, not composition. Explicitly not a BP fact |
| TRADE_REBALANCE as new biology / later-version default | 1.21.1 `DEFAULT_FLAGS` is VANILLA-only. Optional experimental datapack path |
| Night invisibility as stealth / camouflage trait | `UseItemGoal` drinks vanilla potion / milk on day-night predicate |
| DespawnDelay as biological death / lifecycle profile | Encounter timer `discard()`. Not death loot, not BP lifecycle |
| Spawner + two llamas as origin / caravan ancestry | CustomSpawner EVENT + leash. Trader llama already closed this from the llama side. Spawn/leash ≠ origin |
| Queue from trader_llama adjacency | Explicitly forbidden. No evidence dependency forcing this organism from llama |
| Zombie infection like Villager | `killedEntity` is `instanceof Villager` only. WanderingTrader is not Villager |
| Lightning → Witch like Villager | No `thunderHit` override; default fire/damage only |
| `EntityKind.VILLAGER` targeting proves a missing BP distinction | Class **2**: combat `instanceof AbstractVillager`. Correct current behavior does not read BP and does not lack a biological input |
| `HumanEntityType.VILLAGER` is this organism | Human factory homonym |
| Classification forest / absorbing Villager, Witch, Trader Llama | Out of scope; C not earned |
| Sniffer conclusions apply here | Independent investigation; do not assume |

---

## Potential biological relationships

| Relationship | Owner | Biological input? | Existing composition | Named consumer | Result |
|--------------|-------|-------------------|----------------------|----------------|--------|
| Distinct EntityType vs Villager | `EntityType.WANDERING_TRADER` vs `VILLAGER` | Identity | Two organism keys | Generic resolver | **B** — keys already distinguish |
| `AbstractVillager` parent | Merchant helper class | Inheritance ≠ clade | Distinct keys | Combat `AbstractVillager` (not BP) | **A** |
| Villager profession / gossip / POI / breeding | **Villager-only** | N/A to this type | Do not copy Villager facts | None | **A** (absent mechanics) |
| Zombie → Zombie Villager | `Zombie.killedEntity` **Villager only** | No WT conversion | Distinct keys | None | **A** negative |
| Lightning → Witch | `Villager.thunderHit` only | No WT conversion | Distinct keys | None; Witch already investigated | **A** negative |
| Trader llama leash / defend / despawn sync | `WanderingTraderSpawner` + `TraderLlama` | Spawn/leash ≠ origin | `trader_llama` fail-soft already | None as WT biology | **A**; do not reopen llama |
| Host contribution / Model A source | Unregistered | No live contribution route | Fail-soft identity | Eligibility **LIVE** (false); gestation writer unused for this key | **B** fail-soft; **do not register** |
| Analyzer identity display | Resolver projection | Identity only | `organismKey` | LIVE Analyzer | **B** not **C** |

---

## Wiki orientation disagreements

| Wiki / later-version orientation | 1.21.1 authority | Conclusion |
|----------------------------------|------------------|------------|
| “Similar to villagers” / framed as a villager variant | Distinct `EntityType`, **CREATURE** vs **MISC**, `Mob.createMobAttributes` vs `Villager.createAttributes`, no `VillagerDataHolder` | Source wins: not a villager |
| “Unlike other villagers, zombies do not infect wandering traders” | `Zombie.killedEntity` is `instanceof Villager` only — they are **not** villagers | Wiki implication of membership is wrong; the negative conversion is correct |
| Lightning should turn them into witches (MC-151572) | No `thunderHit` override; bug resolved invalid / not a feature | Source: fire/damage only |
| Bedrock extra invisibility when hurt by projectiles/magic | Java `UseItemGoal` is **night/not-invisible** and **day/invisible** only (`WanderingTrader.java` **62–80**) | Java source wins for this version |
| Avoid “all illager variants” | Explicit avoid list: Zombie, Evoker, Vindicator, Vex, Pillager, Illusioner, Zoglin. **No Ravager** | Source list wins |
| 1.21.2+ pale oak / 1.21.5 trade-rebalance “now default” | `FeatureFlags.DEFAULT_FLAGS = VANILLA_SET`; TRADE_REBALANCE not included; `DataPackConfig.DEFAULT` = `"vanilla"` only | **Do not import later versions.** 1.21.1 rebalance is optional experimental datapack |
| Despawn 40 minutes | `48000` ticks = 40 minutes of `aiStep` decrement | Agrees. Source also: no nametag check in `maybeDespawn`; `removeWhenFarAway` false |
| Empty / no drops | Loot table has no pools | Agrees |

---

## Final evidence conclusion

**New BP field earned: NO**

**Existing composition sufficient: YES**

**Named consumer exists: YES** (generic LIVE resolver / Analyzer identity projection; LIVE combat `AbstractVillager` filter does **not** consume BP)

**Architectural escalation required: NO**

Stop: **A + B; C not earned.** Four-way class **4** never triggered. Do **not** register `wandering_trader`. Do not mint `DESIGN-BIO-MANIFEST-004`. Do not create organism-specific profile classes, traits, capabilities, Feature IDs, or Host Registry edits. Do not absorb Villager / Witch / Trader Llama. Do not treat this as a merchant clade.

Unregistered fail-soft identity is **B** only after the four-way audit: the named BP consumer (resolver/Analyzer) already represents identity via `organismKey` with empty HostType optionals; no live consumer requires a missing biological fact.
