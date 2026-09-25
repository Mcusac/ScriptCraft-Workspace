```text
TEMPORARY EVIDENCE — NOT PROJECT SSOT
Skeptical synthesis of a docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
```

# Skeptical synthesis — Hoglin, Piglin, Villager

**Status:** Temporary reviewer synthesis. **Not** project SSOT. **Not** DESIGN-BIO-MANIFEST-004.  
**Version gate:** Minecraft Java **1.21.1** (`minecraft_version_range=[1.21.1,1.22)`).  
**Grouping:** These three were investigated together for **evidence dependency** (living conversion sources already traced from Zoglin / Zombified Piglin / Zombie Villager). They are **not** a conversion-source clade, zombification family, Nether family, villager family, or bio-organic column.

**Independent re-check:** Packets were treated as claims. Load-bearing 1.21.1 classes, dimension types, biome spawn JSON, tags, loot, and AlienCraft `hosts.json` / `HostType` / `MobHostRegistry` / `HostEligibilityService` / `BiologicalProfileResolver` were re-read from `.tmp_mc_sources/` and the live tree.

**Primary objective:** find reasons a new Biological Profile representation is **not** earned.

**C is not earned for any organism in this group.**

---

## Independent verification of tempting claims

| Tempting claim | Independent 1.21.1 / repo finding | Verdict |
|----------------|-----------------------------------|---------|
| Hoglin/Piglin/Villager share a conversion-source biology | Hoglin owner: `Hoglin.customServerAiStep` → `ZOGLIN`. Piglin owner: `AbstractPiglin.customServerAiStep` → `ZOMBIFIED_PIGLIN`. Villager is **victim** of `Zombie.killedEntity` → `ZOMBIE_VILLAGER`. Three owners, three destinations, three triggers | **Reject clade.** Shared *outcome wording* ≠ shared cause |
| Shared `!piglinSafe()` means Hoglin and Piglin share a zombification trait | Same **dimension-type flag** consumed by two classes; Hoglin converts to Zoglin; AbstractPiglin converts to ZP; destinations differ (`fireImmune` on both destinations, absent on both sources) | **Reject shared trait.** Parallel consumers of a world flag |
| `HoglinBase` on Zoglin is Hoglin genetics | `Zoglin implements HoglinBase`; `Hoglin implements HoglinBase`; Zoglin does **not** extend Hoglin. Helpers are static methods on the interface | **Reject ancestry.** Implementation reuse |
| `AbstractPiglin` is a piglin biological clade | `Piglin` and `PiglinBrute` both extend it. Brute `canHunt()==false`, golden-axe-only pickup, separate brain. Conversion is parent-owned adjacency | **Reject clade.** Brute stays a later independent report |
| Piglin `fireImmune` / lava immunity | `EntityType.PIGLIN` has no `.fireImmune()`. ZP does | **Reject inheritance.** Destination flag |
| Hoglin `TimeInOverworld` means Overworld-only / Overworld origin | `isConverting()` reads `dimensionType().piglinSafe()`. Nether JSON `piglin_safe: true`. Overworld and End `false` | **Reject origin.** Misnamed NBT |
| Crimson Forest / Nether spawn is biological origin | Hoglin monster spawn extracted only in `crimson_forest.json` (weight 9). Piglin in crimson (5) and nether_wastes (15). Bastion template also places Hoglin | **Reject origin.** Encounter/worldgen |
| Profession/trades/gossip are BP composition | `VillagerData` + merchant offers + gossips NBT. Copied onto ZV as **destination entity state**. Resolver payload has no profession field | **Reject trait.** Merchant state |
| Live `contributingSourceKey=villager` earns C | `hosts.json` living_biological; `HostType.LIVING_BIOLOGICAL` suitability true; Model A already stores an organism-definition key | **Reject C.** Named consumer exists for **identity**, already represented (**B**) |
| Villager lightning → Witch is ancestry | `Villager.thunderHit` constructs a new `Witch`, copies pose/name, `discard`s villager — not `convertTo` | **Reject ancestry.** Do **not** queue Witch |
| `spawnGolemIfNeeded` is Villager reproduction | `SpawnUtil.trySpawnMob(EntityType.IRON_GOLEM, MOB_SUMMONED, …)` | **Reject parentage.** Already owned in iron_golem.md |
| Unregistered Hoglin/Piglin must be registered to finish | Fail-soft resolver preserves unknown keys. Eligibility false via null HostType | **Reject.** Unregistered ≠ ineligible forever; do not register here |
| `#minecraft:zombies` tying ZV/ZP/Zoglin back to these living sources | Tag members are destinations, not Hoglin/Piglin/Villager | **Reject reverse clade** |

Minor packet notes (do not change results): Hoglin `AnimalMakeLove` is installed on both idle and fight activities. Piglin entity loot table has empty pools; inventory still dumps on death/convert. Villager is `MobCategory.MISC`; Wandering Trader is a separate `CREATURE` type.

---

## Consolidated matrix

| Organism | Interesting behavior | Actual owner | Biological input | Existing composition sufficient? | Named consumer | Result |
| -------- | -------------------- | ------------ | ---------------- | -------------------------------- | -------------- | ------ |
| Hoglin | Identity / no fireImmune | `EntityType.HOGLIN` | Identity | `organismKey=hoglin` fail-soft | Generic resolver | **B** |
| Hoglin | Convert to Zoglin | `Hoglin.customServerAiStep` / `finishConversion` | Replacement via `!piglinSafe` + 300 ticks | Distinct hoglin/zoglin keys | None | **A/B** |
| Hoglin | Knockback fling | `HoglinBase` static helpers | Combat helper | Not a knockback field | None | **A** |
| Hoglin | Food / breeding | `ItemTags.HOGLIN_FOOD` + `AnimalMakeLove` + `getBreedOffspring` | Vanilla animal loop | Identity if ever needed | None | **A** |
| Hoglin | Repellents | `HoglinSpecificSensor` + `#hoglin_repellents` | Block-tag AI | Not a diet/repellent field | None | **A** |
| Hoglin | Crimson spawn / nylium walk | biome JSON + `getWalkTargetValue` | Encounter / path score | Not origin | None | **A** |
| Hoglin | Host Registry | **ABSENT** | Participation missing | Fail-soft identity | Origin blocked | **B** |
| Piglin | Identity / no fireImmune | `EntityType.PIGLIN` | Identity | `organismKey=piglin` fail-soft | Generic resolver | **B** |
| Piglin | Convert to ZP | `AbstractPiglin` + Piglin inventory dump | Replacement | Distinct piglin/zombified_piglin keys | None | **A/B** |
| Piglin | Barter / gold / crossbow | `PiglinAi` + tags + equipment + barter loot table | AI/items | Not a gold capability | None | **A** |
| Piglin | Hunt Hoglin / fear ZP+Zoglin | `PiglinAi` predicates | Entity-type AI | Identity already | None | **A** |
| Piglin | Soul-fire repellents | `PiglinSpecificSensor` + `#piglin_repellents` | Block-tag AI | Not soul-fire biology | None | **A** |
| Piglin | Host Registry | **ABSENT** | Participation missing | Fail-soft identity | Origin blocked | **B** |
| Villager | Identity / MISC | `EntityType.VILLAGER` | Identity | `organismKey=villager` | LIVE host + Analyzer | **B** |
| Villager | Profession / trades / gossip | `VillagerData` / merchant / gossips | Entity state | Identity does not need those fields | None as biology | **A** |
| Villager | Breed | `canBreed` foodLevel + `getBreedOffspring` | Minecraft birth | Identity sufficient | None | **A** |
| Villager | Infected to ZV | `Zombie.killedEntity` + `convertTo` | Replacement; villager is victim | Distinct keys | None | **A/B** |
| Villager | Lightning → Witch | `thunderHit` new Witch + discard | Replacement | Distinct keys | None; do not queue Witch | **A** |
| Villager | Summon Iron Golem | `spawnGolemIfNeeded` | Creation ≠ parentage | iron_golem identity | Vanilla golem path | **A** |
| Villager | Host contribution | `hosts.json` + `HostEligibilityService` + Model A | Identity only | `contributingSourceKey=villager` already | LIVE generic identity | **B** |

---

## Shared findings (genuine shared evidence only)

These are **not** a clade:

1. **Same evidence-management batch** — living sources of already-investigated conversions. Administrative, not biological.
2. **Hoglin and Piglin both consume `dimensionType().piglinSafe()`** with a 300-tick timer and `IsImmuneToZombification`. That is a **shared Minecraft dimension-type consumer**, not a shared biological cause. Destinations, class owners, and discarded state differ.
3. **No new BP field.** Generic `BiologicalProfileResolver` already projects `organismKey` (+ HostType / host-effect id when registered).
4. **Unregistered Hoglin/Piglin vs registered Villager** is a Host Registry participation difference, not a biological grouping.

---

## Important differences that disprove overly broad abstractions

| Abstraction that would collapse them | Disproof |
|--------------------------------------|----------|
| Conversion-source clade / zombification family | Three different owners and destinations. Villager is not even the conversion AI owner. |
| Nether-native biology | Villager is Overworld village `MISC`. Hoglin crimson-weighted; Piglin also nether_wastes. Nether spawn ≠ origin. |
| Shared Java parent | Hoglin is `Animal`+`Enemy`+`HoglinBase`. Piglin is `AbstractPiglin`. Villager is `AbstractVillager`. |
| Shared tag | Living Hoglin/Piglin/Villager are **not** `#minecraft:zombies`. Destinations are. |
| Registered living host = extra composition | Villager registration enables Model A identity already designed. Profession still unused. Hoglin/Piglin remain representable fail-soft without registration. |
| Breeding = BP reproduction | Hoglin uses `Animal`/`HOGLIN_FOOD`. Villager uses foodLevel/WANTED_ITEMS. Piglin does **not** breed. Three different answers. |

---

## Rejected abstractions

- Conversion-source / zombified-living family column
- `AbstractPiglin` clade (would swallow Piglin Brute)
- Hoglin/Zoglin genetics from `HoglinBase`
- Gold / barter / soul-fire / crimson-fungus Biological Profile dimensions
- Profession / gossip / villager-type as genetics
- Lightning-witch ancestry; raid-queued Ravager/Witch
- Nether-origin field from biome spawn
- Registering Hoglin or Piglin as a manifestation conclusion
- Treating Villager’s live host path as C

---

## Biological Profile result

```text
A/B/C summary
Hoglin: A (vanilla owners) + B (fail-soft identity). C not earned.
Piglin: A + B. C not earned. Piglin Brute adjacency only.
Villager: A + B (registered identity / contributingSourceKey). Named consumer of identity exists; no missing-fact consumer. C not earned.
```

### New representation

```text
None earned
```

### Named consumer nuance (Villager)

A live BioCraft consumer **does** exist for Villager: Host Registry + gestation suitability + Model A `contributingSourceKey`. That consumer needs **organism identity**, which existing composition already supplies. C is only for a **missing** biological fact. Do not escalate identity routing into a new field.

---

## Recommended next investigation

**Evidence dependency:** independent **Piglin Brute** (second `AbstractPiglin` conversion source; `canHunt()==false`; unregistered). Treat as its own organism, **not** a piglin-family continuation.

Then continue remaining current-version bio-organic rows independently. Do **not** jump to Witch from lightning, Wandering Trader from `AbstractVillager`, Ravager from raid sensor, Ghast from Nether spawn, or Creeper/Bat (still deferred).

Undead reassessment remains **deferred** while remaining bio-organic work continues (user-authorized). Completing these three living sources does **not** authorize a conversion-source column.
