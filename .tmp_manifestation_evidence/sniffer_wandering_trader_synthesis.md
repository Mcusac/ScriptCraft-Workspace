TEMPORARY EVIDENCE — NOT PROJECT SSOT
Skeptical synthesis / review of Sniffer + Wandering Trader manifestation packets
Do not treat this file as canonical design documentation.
Do not mint DESIGN-BIO-MANIFEST-004.
Do not register either organism.
Do not edit Java, hosts.json, BACKLOG, SPRINT, ROADMAP, system.md, or classification docs.

Packets reviewed as hypotheses, not authority:
- `.tmp_manifestation_evidence/sniffer.md` (Agent 86702c76-7992-48de-874a-37268714a7bb)
- `.tmp_manifestation_evidence/wandering_trader.md` (Agent 83d0963c-eaf9-46aa-8b4d-fe3b7b64aba4)

This pair is **evidence-management / accounting closeout** of the last two pending 1.21.1 bio-organic inventory rows. It is **not** a merchant clade, villager family, item-production column, leftover biological group, or llama-adjacency continuation.

**Pairing may yield zero shared biological finding.** Shared Minecraft mechanics, shared Host Registry absence, shared fail-soft identity path, or shared absence of BP consumers do **not** constitute a biological abstraction.

Version: Minecraft Java **1.21.1** / NeoForge **21.1.208**. Wiki orientation only; 1.21.1 mapped source wins.

---

## Independent spot-checks of load-bearing claims

Re-opened against `.tmp_mc_sources/` (NeoForge 21.1.208 mapped sources / resources) and live `biocraft-alien` production Java. Packet line citations that match are accepted; mismatches are called out.

### Sniffer

| Claim | Independent result | Citation |
|-------|--------------------|----------|
| `EntityType.SNIFFER` CREATURE 1.9×1.75 eye 1.05; no `fireImmune()` | **Confirmed** | `EntityType.java` **619–627** |
| `Sniffer extends Animal` | **Confirmed** | `Sniffer.java` **65** |
| Attributes health 14 / speed 0.1 | **Confirmed** | `Sniffer.createAttributes` **82–84**; `DefaultAttributes.java` **150** |
| Digging gift loot `gameplay/sniffer_digging` | **Confirmed.** `dropSeed` GIFT loot at head origin; adult-only `canDig` | `Sniffer.java` **251–286**; `sniffer_digging.json` torchflower_seeds / pitcher_pod rolls 1 |
| `#sniffer_diggable_block` | **Confirmed** dirt/grass/podzol/coarse/rooted/moss/mud/muddy_mangrove_roots | tag JSON; `Sniffer.canDig(BlockPos)` **261–265** |
| Breed drops egg **item**, not live baby | **Confirmed.** Override spawns `Items.SNIFFER_EGG` and `finalizeSpawnChildFromBreeding(..., null)`. Default `Animal.spawnChildFromBreeding` would add `getBreedOffspring` child | `Sniffer.java` **339–346**; `Animal.java` **214–232**; `getBreedOffspring` still `EntityType.SNIFFER.create` **427–429** (contract / spawn-egg path) |
| `SnifferEggBlock` hatch vs entity baby | **Confirmed.** HATCH 0→2; regular 24000 / moss-boosted 12000; hatch `EntityType.SNIFFER.create` + `setBaby(true)` | `SnifferEggBlock.java` **28–32**, **64–91**, **99–101** |
| `#sniffer_egg_hatch_boost` = moss_block | **Confirmed** | tag JSON; `hatchBoost` **99–101** |
| Archaeology egg = encounter not origin | **Confirmed.** `sniffer_egg` only in `archaeology/ocean_ruin_warm.json` (weight 1 among pool). Not organism-native origin | warm archaeology JSON |
| Memories vs biological state | **Confirmed AI state.** `SNIFFER_EXPLORED_POSITIONS` has `Codec.list(GlobalPos.CODEC)`; also `SNIFFER_SNIFFING_TARGET`, `SNIFFER_DIGGING`, `SNIFFER_HAPPY`. `SNIFF_COOLDOWN` **is** in `SnifferAi.MEMORY_TYPES` (**50–66**) — still brain/AI, not composition. No `addAdditionalSaveData` on `Sniffer` | `MemoryModuleType.java` **120**, **130–133**; `SnifferAi.java` **50–66** |
| Synched `State` enum | **Confirmed** IDLING/FEELING_HAPPY/SCENTING/SNIFFING/SEARCHING/DIGGING/RISING | `Sniffer.java` **488–508** |
| Baby age 48000 | **Confirmed** vs `AgeableMob.BABY_START_AGE` **-24000** | `Sniffer.java` **70**, **422–424**; `AgeableMob.java` **17** |
| No `SpawnPlacements` SNIFFER row | **Confirmed.** Static register list **92–174** has no `EntityType.SNIFFER` | `SpawnPlacements.java` |
| `hosts.json` absence | **Confirmed.** `"sniffer"` not in `living_biological` / undead / unsuitable / modded / `variant_mappings` | `data/biocraft_alien/systems/hosts.json` |
| Production Java named sniffer | **Confirmed ABSENT** under `biocraft-alien/src` | this-pass scan |

### Wandering Trader

| Claim | Independent result | Citation |
|-------|--------------------|----------|
| Distinct `EntityType` vs Villager; CREATURE vs MISC; same outer size | **Confirmed.** WT `"wandering_trader"` CREATURE 0.6×1.95 eye 1.62. Villager `"villager"` **MISC** same size | `EntityType.java` **710–712**, **717–719** |
| Attributes differ | **Confirmed.** WT `Mob.createMobAttributes()` (follow **16**). Villager speed **0.5** follow **48** | `DefaultAttributes.java` **161**, **164**; `Mob.java` **159–160**; `Villager.java` **269–271** |
| `WanderingTrader extends AbstractVillager` | **Confirmed.** Parent is `AgeableMob` + `InventoryCarrier` + `Npc` + `Merchant`. `canBeLeashed() == false` | `WanderingTrader.java` **49**; `AbstractVillager.java` **40**, **225–227** |
| `getBreedOffspring` null | **Confirmed.** `AgeableMob.canBreed()` default **false**. Load clamps age ≥ 0 | `WanderingTrader.java` **99–103**, **182**; `AgeableMob.java` **53–55** |
| TRADE_REBALANCE default-off in 1.21.1 | **Confirmed.** `DEFAULT_FLAGS = VANILLA_SET`; `TRADE_REBALANCE` created but not in `VANILLA_SET` | `FeatureFlags.java` **31–40**; `WanderingTrader.updateTrades` **134–150** vs `experimentalUpdateTrades` **153–159** |
| DespawnDelay 48000 + discard | **Confirmed.** Spawner sets delay; `maybeDespawn` decrements when not trading and `discard()` at 0. NBT `"DespawnDelay"` | `WanderingTraderSpawner.java` **113**; `WanderingTrader.java` **165**, **244–247** |
| CustomSpawner overworld-only + two llamas leashed | **Confirmed.** `MinecraftServer.createLevels` CustomSpawner list including `new WanderingTraderSpawner(serverleveldata)` passed only to **OVERWORLD** `ServerLevel`. Two `TRADER_LLAMA` EVENT + `setLeashedTo` | `MinecraftServer.java` **363–368**; `WanderingTraderSpawner.java` **106–113**, **124–131** |
| Zombie infection **negative** | **Confirmed.** `entity instanceof Villager villager` only → `convertTo(ZOMBIE_VILLAGER)`. WT is not `Villager` | `Zombie.java` **421–428** |
| Lightning → Witch **negative** | **Confirmed.** No `thunderHit` on `WanderingTrader`. Witch factory is `Villager.thunderHit` only | `Villager.java` **820–843** |
| Night invisibility / day milk | **Confirmed** `UseItemGoal` predicates | `WanderingTrader.java` **62–80** |
| Empty entity loot | **Confirmed** type + random_sequence only | `entities/wandering_trader.json` |
| `hosts.json` absence; `"villager"` present | **Confirmed** | `hosts.json` **6** has `"villager"`; no `"wandering_trader"` |
| `HumanEntityType.VILLAGER` homonym | **Confirmed.** Config key `"villager"` / entity `"human_villager"` — not this EntityType | `HumanEntityType.java` **15** |
| Production Java named wandering_trader | **Confirmed ABSENT** (except generic `AbstractVillager` class filter below) | this-pass scan |

### Live BioCraft callers (resolver / production)

| Caller | What it actually reads | Four-way |
|--------|------------------------|----------|
| `BiologicalProfileResolver.resolve` | `organismKey`; `MobHostRegistry.getHostType(lookup)` → null for both keys; empty form/effect/behavior; optional contributing source only if supplied | **3** for identity. Unknown non-blank keys fail soft (`BiologicalProfileResolver.java` **23–24**, **41–56**). TEST: `unknownKeyPreservesOrganismKeyWithEmptyOptionals` — generic, not organism-named |
| `BiologicalProfileDnaAnalysisPort` / `DnaAnalysisReport.fromCompiled` | Projects compiled refs only. `Genome.unknown()`. Does **not** read dig loot, egg, trades, despawn, memories | **3** identity |
| `DnaSampleFromOccupant` | `encodeId` → `HostRegistryPaths.registryPath` (`minecraft:sniffer` → `sniffer`). Contributing source only if `ContributingSourcePort.supports` (Chestburster/Drone), not these vanilla types | **3** identity |
| `HostEligibilityService` / `MobHostRegistry.isSuitableForXenomorph` | Host Registry, **not** BP. Unregistered → `getHostType` null → false (**46–48**, **68–71**) | **2** |
| `GestationManager.writeContributingSource` | After chestburster spawn, copies **host** encode-id path onto offspring if port supports offspring (**164–175**). Unreachable for these organisms (not suitable hosts) | **2** machinery; **1** for these keys |
| `StandardTargetingHelper` | `NearestAttackableTargetGoal<>(…, AbstractVillager.class, …)` **51–54** matches WT. `Animal.class` **55–58** matches Sniffer. Goal slot `target_villager` is a **priority key**, not EntityType | **2** — combat class filter, does **not** consume BP |
| `NeoForgeEntityQueryAdapter.classifyEntity` | `instanceof AbstractVillager` → `EntityKind.VILLAGER` **123–124**. Sniffer is `Animal` → `EntityKind.ANIMAL` **126–128** | **2** |
| `XenomorphTargetingHelper.isValidTargetEntity` | `EntityKind.PLAYER / VILLAGER / ANIMAL` remain combat prey **without** hosts.json lookup **45–47** | **2** |
| `CaptureEligibilityPolicy.canCapture` | `alive && !player` **19–20**. Neither organism is a player | **2** |

**Candidate shared finding (fail-soft identity path):** independently confirmed. Both unregistered keys resolve through the same generic unknown-key path. That is **existing composition working as designed**, not a new biological fact, not a shared trait, and not Host Registry absence-as-abstraction.

**Class 4 was not reached for either organism.**

---

## Consolidated matrix

| Organism | Interesting behavior | Actual owner | Biological input? | Existing composition sufficient? | Named consumer | Four-way class | Result |
|----------|----------------------|--------------|-------------------|----------------------------------|----------------|----------------|--------|
| Sniffer | Identity / CREATURE / size | `EntityType.SNIFFER` | Identity only | Fail-soft `organismKey=sniffer`; empty HostType/form/effect/behavior | LIVE resolver / Analyzer / occupant sample | **3** | **B** |
| Sniffer | Dig → gift seeds | `Sniffer.dropSeed` + `sniffer_digging` loot | No stored composition (loot roll, not Color-like NBT) | Identity does not encode seed type — and nothing needs it to | None | **1** | **A** |
| Sniffer | `#sniffer_diggable_block` / `#sniffer_food` | Tags + `canDig` / `isFood` | Tag ≠ clade / diet trait | Not needed | None | **1** | **A** |
| Sniffer | Brain memories / `State` FSM / sniff-search-dig | `SnifferAi` + synched `DATA_STATE` | AI / presentation | Not needed | None that read Sniffer brain | **1** | **A** |
| Sniffer | Breed → egg item, not baby entity | `spawnChildFromBreeding` override | Lifecycle/mechanic; egg-as-item ≠ Genome | Child would still be `sniffer` if a baby existed | None | **1** | **A** |
| Sniffer | Egg block hatch + moss boost | `SnifferEggBlock` | Block timer / environment | Not a lifecycle Profile | None | **1** | **A** |
| Sniffer | Warm-ruins archaeology egg | archaeology loot table | Encounter ≠ origin | Not an origin field | None | **1** | **A** |
| Sniffer | Baby 48000 / digging pose hitbox / attrs | `setBaby` / `DIGGING_DIMENSIONS` / `createAttributes` | Vanilla timers/stats/pose | Not needed | None | **1** | **A** |
| Sniffer | No natural biome spawn | Missing `SpawnPlacements` row | Spawn encounter (here: absent) | Identity sufficient for egg/summon | None | **1** | **A** |
| Sniffer | Capture | `CaptureEligibilityPolicy` | Eligibility gameplay | Type id after capture | LIVE generic; not BP | **2** | **A** |
| Sniffer | Xenomorph `Animal` targeting | `StandardTargetingHelper` `Animal.class` | Java combat taxonomy | Soft key unused by this caller | LIVE combat; not BP | **2** | **A** |
| Sniffer | Host eligibility / contribution | `hosts.json` absence + `writeContributingSource` | Participation gap, not missing biology | Fail-soft identity already | Eligibility **2**; writer unreachable | **B** identity / **A** participation. **Do not register** |
| Wandering Trader | Distinct identity vs Villager | `EntityType.WANDERING_TRADER` | Identity only | Fail-soft `organismKey=wandering_trader` | LIVE resolver / Analyzer | **3** | **B** |
| Wandering Trader | `extends AbstractVillager` | Class inheritance | Implementation sharing ≠ clade | Distinct keys already | LIVE `AbstractVillager` combat filter | **2** | **A** |
| Wandering Trader | Same 0.6×1.95 hitbox as Villager | Independent builders | Hitbox coincidence; attrs differ | Anatomy contract not yet; not needed | None | **1** | **A** |
| Wandering Trader | `getBreedOffspring` null | WT override | Non-breeding mechanic, not a sterility trait | Identity sufficient | None | **1** | **A** |
| Wandering Trader | Trades / TRADE_REBALANCE | `updateTrades` + `VillagerTrades` tables | Merchant offers + NBT | Not a capability BP | None | **1** | **A** |
| Wandering Trader | Night potion / day milk | `UseItemGoal` | AI + items, not stealth trait | Not needed | None | **1** | **A** |
| Wandering Trader | DespawnDelay discard | `maybeDespawn` + spawner | Encounter timer ≠ biological death | Not needed | None | **1** | **A** |
| Wandering Trader | Overworld CustomSpawner + llama leash | `WanderingTraderSpawner` | Spawn/leash ≠ origin | `trader_llama` already closed | None | **1** | **A** |
| Wandering Trader | Zombie infection negative | `Zombie.killedEntity` Villager-only | No conversion | Distinct keys | None | **1** | **A** |
| Wandering Trader | Lightning → Witch negative | No WT `thunderHit`; `Villager.thunderHit` only | No conversion | Distinct keys | None; do not reopen Witch | **1** | **A** |
| Wandering Trader | `AbstractVillager` targeting / `EntityKind.VILLAGER` | `StandardTargetingHelper` + adapter + `XenomorphTargetingHelper` | Combat class taxonomy. Lumps WT with Villager for AI only | Soft keys unused | LIVE combat; **does not consume BP** | **2** | **A** |
| Wandering Trader | Capture | `CaptureEligibilityPolicy` | Eligibility | Type id after capture | LIVE generic | **2** | **A** |
| Wandering Trader | Host eligibility / contribution | Unregistered; `"villager"` adjacent | Participation ≠ ancestry | Fail-soft identity | Eligibility **2**; writer unreachable | **B** identity / **A** participation. **Do not register** |
| Wandering Trader | `HumanEntityType.VILLAGER` | Human factory enum | Homonym | Wrong organism | LIVE Human subtype | **2** | **A** |

No row is **C**. No row is four-way class **4**.

---

## Shared findings

**Genuine shared biological finding: none.**

What this pair actually shares, and why it is **not** a biological abstraction:

| Apparent overlap | Why it is not shared biology |
|------------------|------------------------------|
| Both unregistered in `hosts.json` | Participation / accounting. Locked rule: Host Registry absence is not a biological abstraction and is not automatic A/B |
| Both resolve fail-soft `organismKey` with empty optionals | Same **existing** composition path. Shared registration status / shared fail-soft / shared absence of extra BP consumers ≠ a biological trait |
| Both `MobCategory.CREATURE` | Category coincidence. Villager is MISC; WT is CREATURE. Category is spawn-system, not clade |
| Both have empty entity loot tables | Drops ≠ anatomy; still **A** each |
| Both capturable as living non-players | Generic capture policy |
| Both inventory-`bio-organic` pending rows | Planning label / bookkeeping — the reason this pair exists |

Sheep Color contrast was tested on Sniffer only (world-search loot vs Color-keyed wool). That contrast does **not** travel to Wandering Trader and does **not** mint a foraging/wool field (sheep.md lock: Color **A**; `contributingSourceKey=sheep` **B not C**).

Trader-llama caravan/leash was already closed from the llama side. WT investigation independently confirms spawn/leash remainder; it does **not** earn WT by llama adjacency.

---

## Important differences

| Dimension | Sniffer | Wandering Trader |
|-----------|---------|------------------|
| Java parent | `Animal` | `AbstractVillager` (not `Villager`, not `Animal`) |
| BioCraft combat slot | `Animal.class` → `EntityKind.ANIMAL` | `AbstractVillager.class` → `EntityKind.VILLAGER` |
| Reproduction | Food → egg **item** → block hatch → baby entity | `getBreedOffspring` **null**; age clamped ≥ 0 |
| Distinctive vanilla owner | Brain-driven dig + gift loot; egg block | Merchant tables; despawn timer; CustomSpawner + llama leash |
| Conversion | None at issue | Explicit **negatives**: no Zombie infection; no lightning→Witch |
| Adjacent registered key | None required | `"villager"` registered — still **do not register** WT |
| Sheep Color contrast | Relevant as **rejected** foraging/wool leap | Irrelevant |
| Trader-llama adjacency | None | Spawn/leash remainder only; already closed |

---

## Rejected abstractions

| Tempting abstraction | Why rejected |
|----------------------|--------------|
| Shared fail-soft / unregistered-organism BP field | Existing composition already preserves unknown keys. Shared absence of extra consumers is bookkeeping |
| Merchant / villager / illager clade from `AbstractVillager` | Inheritance ≠ clade. Distinct EntityType, category, attributes, no `VillagerData`, no profession. Combat `instanceof` is class **2** |
| Item-production column (Sniffer seeds + WT trades + Sheep wool) | Different owners: loot table vs merchant offers vs Color-keyed shear. Shared outcome class ≠ shared cause |
| Foraging / chemoreception / “ancient” origin BP | Dig loot + `State.SCENTING` + archaeology encounter. No consumer. Encounter ≠ origin |
| Egg-as-Genome / Ovomorph analogue | Block item + `SnifferEggBlock`. Minecraft hatch ≠ Genome |
| Sterility trait from `getBreedOffspring` null | Mechanic; no consumer |
| Trades-as-capability / despawn-as-lifecycle-profile / night-invisibility stealth | Merchant/AI/encounter owners |
| Register because Villager is registered, or because interesting | Participation ≠ manifestation conclusion |
| Queue WT from trader_llama, or Sniffer from Sheep Color contrast as a field | Locked priors. Contrast tested; C not earned |
| `EntityKind.VILLAGER` targeting as missing BP distinction | Class **2**: correct behavior does not read BP |
| Classification forest / End/boss/flying / undead reopen | Out of scope. Empty pending queue is not permission |
| Majority agreement of packets | Packets are hypotheses; this review re-opened sources |

---

## A/B/C summary

| Organism | A | B | C |
|----------|---|---|---|
| Sniffer | Dig/loot/tags/memories/egg-hatch/archaeology/spawn-absence/renderer/capture/Animal targeting | Fail-soft `organismKey=sniffer` | **Not earned** |
| Wandering Trader | AbstractVillager reuse, trades, potions, despawn, spawner/leash, negative conversions, combat class filter, capture, Human homonym | Fail-soft `organismKey=wandering_trader` | **Not earned** |
| Pair | Bookkeeping only | Same fail-soft path used independently — not a shared biological B | **Not earned** |

C threshold failed: no concrete currently live BioCraft consumer whose correct behavior cannot be represented by existing composition (`organismKey`, fail-soft unregistered key, optional `contributingSourceKey`, sparse `CompiledBiologicalProfile`), and whose required input is genuinely biological.

---

## New representation

**None earned.**

No potential minimum fact + named consumer + composition insufficiency.

Implementation: **NOT AUTHORIZED.** Do not mint `DESIGN-BIO-MANIFEST-004`. Do not register `sniffer` or `wandering_trader`. Do not add foraging/wool/trade/despawn/egg/memory fields.

---

## Recommended next investigation

C was **not** earned.

Remaining 1.21.1 bio-organic manifestation-pending inventory rows: **none**.

Stay deferred (do not invent a next organism; empty pending queue is not permission to reopen):

- undead reassessment
- End / boss / flying comparisons
- classification forest

Current sprint remains owner lab playtest + `DESIGN-BIO-CONSEQUENCE-001` (inventory already states this; this synthesis does not change it).
