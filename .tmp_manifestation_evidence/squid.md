TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Squid docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/squid.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Squid — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not unregister Squid as a conclusion of this investigation.** Squid is already in `vanilla_hosts.living_biological`. Registration is participation, not extra biology.

Method: existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP |

Closed leaps: `#minecraft:aquatic` ≠ aquatic BP field; ink particle / swim AI ≠ shared biological cause or capability field without a named consumer; GlowSquid inheritance / squid family = **OUT OF SCOPE** (do not conclude); Host Registry registered ≠ eligibility fact and ≠ missing BP fact; live `contributingSourceKey=squid` ≠ C.

Existing BP composition checked: `organismKey`, optional `contributingSourceKey`, optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

Default: **NO** new BP field. Live contribution identity is **B**, not **C**.

---

## Subject

Squid (`minecraft:squid`) — `WaterAnimal` water locomotion + flee/random movement goals, hurt-triggered ink particle cloud, surface-water spawn, ink_sac loot, aquatic / breathe / hunt / pufferfish tags, Host Registry **LIVE** `living_biological`, BioCraft gestation identity routing only.

Out of scope for this agent: GlowSquid class/family conclusions; tadpole/frog packets.

---

## Version

Minecraft Java **1.21.1** only. Authority: `neoforge-21.1.208-sources.jar` extracts under `.tmp_mc_sources/` > live BioCraft > vanilla JSON > design docs > Wiki orientation.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:squid` |
| `EntityType` | `EntityType.SQUID` — `EntityType.java` **647–648**: `Builder.of(Squid::new, MobCategory.WATER_CREATURE).sized(0.8F, 0.8F).eyeHeight(0.4F).clientTrackingRange(8)` |
| Fire / lava | **No** `.fireImmune()` |
| Class | `Squid extends WaterAnimal` (`Squid.java` **26**). `WaterAnimal extends PathfinderMob` (`WaterAnimal.java` **15**) |
| Category | `MobCategory.WATER_CREATURE` |
| Attributes | Health **10** only (`Squid.createAttributes` **54–55**). No movement attribute override |
| Spawn | `SpawnPlacements` **99**: `IN_WATER` + `WaterAnimal::checkSurfaceWaterAnimalSpawnRules` (sea-level window, water below + water above) |
| Host Registry | **LIVE.** `hosts.json` `vanilla_hosts.living_biological.mobs` includes `"squid"` (**8**). `default_dna: baseline_biological`. No squid `variant_mappings` |
| Suitability | Registered living_biological → currently suitable via `MobHostRegistry.isSuitableForXenomorph`. Registered ≠ extra biology |

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP representation? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|----------------------------|--------------------|-------|
| Identity / WATER_CREATURE / size | `EntityType.SQUID` | `EntityType.java` **647–648** | Identity | `organismKey = squid` | Resolver / Analyzer / host lookup | **B** |
| Base water-animal air / drown-out-of-water | `WaterAnimal.handleAirSupply` + `baseTick` | Out of water/bubble: air decrement; at −20 drown 2 (`WaterAnimal.java` **36–52**). In water/bubble: air reset **300** | Entity survival | Not needed | None | **A** |
| Tag underwater breathing gate | `LivingEntity.canBreatheUnderwater` | Type in `#can_breathe_under_water` (`LivingEntity.java` **382–383**). Squid is a member | Tag membership | Tag ≠ BP trait | None | **A** |
| Water path malus | `WaterAnimal` ctor | `PathType.WATER` malus **0.0F** (`WaterAnimal.java` **18**) | Navigation | Not needed | None | **A** |
| Goals | `Squid.registerGoals` | Priority 0 `SquidRandomMovementGoal`; priority 1 `SquidFleeGoal` (`Squid.java` **49–51**) | Entity AI | Identity sufficient | None | **A** |
| Random swim vector | `SquidRandomMovementGoal.tick` | Random TX/TY/TZ when idle / not touching water / no vector; freeze if noActionTime > 100 (`Squid.java` **284–308**) | Locomotion AI | Not swim capability field | None | **A** |
| Flee from last hurt-by | `SquidFleeGoal` | In water + lastHurtBy within 100²: push away in water/air cells; speed scale down past 5 blocks (`Squid.java` **224–281**) | Combat flee AI | Not needed | None | **A** |
| Water / out-of-water travel presentation | `aiStep` + `travel` | In water: apply TX/TY/TZ × speed, body rot (`Squid.java` **118–143**). Out of water: gravity / levitation, tentacle presentation (**144–158**). `travel` only `move(SELF, delta)` (**198–200**) | Entity movement | Not aquatic BP | None | **A** |
| Ink cloud on hurt | `Squid.hurt` → `spawnInk` | After successful hurt with `getLastHurtByMob() != null`: server plays squirt sound + 30× `ParticleTypes.SQUID_INK` (`Squid.java` **165–195**) | Presentation / VFX | Ink ≠ biological composition without consumer | None | **A** |
| Ink particle client | `SquidInkParticle` | Client particle only | Presentation | Not needed | None | **A** |
| Leash override | `Squid.canBeLeashed` | Returns **true** (`Squid.java` **78–80`); base `WaterAnimal` returns false (**61–63**) | Interaction flag | Not needed | None | **A** |
| Loot | `entities/squid.json` / `VanillaEntityLoot` **812–822** | `ink_sac` 1–3 + looting | Drops ≠ anatomy BP | Not needed | None | **A** |
| Spawn / worldgen | `BiomeDefaultFeatures.oceanSpawns` / biomes | `WATER_CREATURE` spawner data for SQUID | Encounter ≠ origin | Not origin field | None | **A** |
| Host → contributingSourceKey | Host Registry + gestation writer | `"squid"` → path `"squid"` (see Host Registry path probe) | Identity only | `organismKey` + optional `contributingSourceKey=squid` + `baseline_biological` | **LIVE** generic writer / Resolver / Analyzer | **B** |

No row is **C**.

---

## Tags: membership → named 1.21.1 consumer → biological? → BioCraft?

| Tag | Membership | Named 1.21.1 consumer | Behavior | Biological? | BioCraft consumer? |
|-----|------------|----------------------|----------|-------------|-------------------|
| `#minecraft:aquatic` | includes `minecraft:squid` | `#sensitive_to_impaling` = `#aquatic`; Impaling enchantment predicate | Enchant damage bonus | Tag ≠ aquatic BP | None |
| `#minecraft:can_breathe_under_water` | includes squid | `LivingEntity.canBreatheUnderwater` | Skip water-eye drown path when tagged | Survival tag | None |
| `#minecraft:axolotl_hunt_targets` | includes squid | `AxolotlAttackablesSensor` | Axolotl hunt AI | Prey tag ≠ clade | None |
| `#minecraft:not_scary_for_pufferfish` | includes squid | `Pufferfish` scare predicate | Puffer inflate AI | Interaction tag | None |
| `#minecraft:sensitive_to_impaling` | via `#aquatic` | Impaling enchantment | Damage | Tag ≠ anatomy | None |

---

## Host Registry path probe

**Participation (separate concept):** LIVE — `"squid"` listed under `vanilla_hosts.living_biological` (`hosts.json` **8**). Loaded into `MobHostRegistry` → `HostType.LIVING_BIOLOGICAL`, DNA profile id `baseline_biological`.

**contributingSourceKey consumer path (separate concept):**

1. Chestburster hatch: `GestationManager.writeContributingSource(host, offspring)` (**164–176**).
2. `BoundaryServices.entityQuery().encodeId(host)` → e.g. `minecraft:squid`.
3. `HostRegistryPaths.registryPath` → `"squid"` (**16–22**).
4. `ContributingSourcePort.setContributingSourceKey(offspring, "squid")` on carriers that implement `ContributingSourceCarrier` (e.g. chestburster).
5. Lab projection: `BiologicalProfileResolver.resolve(ref, contributingSourceKey)` passes the key through as optional composition (**35–56**); Analyzer / vial paths observe identity + optional source (`DnaSampleFromOccupant`, `BiologicalProfileDnaAnalysisPort`).
6. Host eligibility also uses the same path strip (`HostEligibilityService` **27–29**) — suitability lookup by registry path, not ink/swim facts.

**Verdict:** The only biological input BioCraft consumes for Squid is the **generic identity route** (host list + encodeId path → `organismKey` / `contributingSourceKey`). That is **B**. Registration alone is **not** manifestation evidence for ink, swim, or aquatic BP fields.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"squid"` | **LIVE** | living_biological **8** | Participation. Can originate contribution |
| `variant_mappings` squid | **ABSENT** | No entry | No override |
| `BiologicalProfileResolver` squid-specific branch | **ABSENT** | Generic lookup by `organismKey` only | Identity **B** |
| Squid entity / mob / lifecycle JSON under `biocraft_alien` | **ABSENT** (verified: only hosts.json mention; no `entity/` squid file; no test named squid) | Vanilla remains owner of ink/swim/loot | |
| Squid-specific BioCraft Java consumer | **ABSENT** | No `squid`/`SQUID`/`ink` gameplay consumer in mod sources | No named missing-fact consumer |
| Inventory row | **PLANNING** | `vanilla_organism_inventory.md` pending | Docs ≠ consumer |
| `MobBucketSpecimenSource` | **N/A** | Squid not in vanilla bucket map (`MobBucketSpecimenSource` **107–126**) | No bucket admission path |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails |
|----------------|--------------|
| Aquatic tag / WATER_CREATURE → aquatic BP field | Tag + category own Impaling / spawn category. Closed leap. **A** |
| Ink cloud → ink / defense capability BP | `spawnInk` emits particles + sound only. No BioCraft (or shared capability) consumer. **A** |
| Swim / flee AI → shared swim capability field | Owned by Squid goals + `aiStep`. No named BioCraft consumer needing a swim fact. **A** |
| Squid + GlowSquid → squid family / inheritance BP | GlowSquid inheritance **OUT OF SCOPE** for this agent. Shared class is Minecraft ownership, not a BioCraft family conclusion |
| Host Registry registered → needs BP fields or earns C | Participation ≠ missing composition fact. Live `contributingSourceKey=squid` is identity **B** |
| ink_sac loot → gland / anatomy BP | Loot table item production. **A** |
| Axolotl hunt-target membership → predator/prey biology column | Tag-driven Axolotl AI only. **A** |

---

## Potential biological relationships

### 1. Live xenomorph host / Model A source

- **Owner:** hosts + eligibility + gestation writer + Resolver/Analyzer.
- **Biological input?** Key `"squid"` only.
- **Result:** **B**.

### 2. Ink / swim / water survival

- **Owner:** `Squid` / `WaterAnimal` / tags.
- **Named BioCraft consumer:** None needing an ink/swim/aquatic fact.
- **Result:** **A**.

### 3. GlowSquid (mention only — out of scope)

- Shares size/ink pattern in Minecraft sources; different category (`UNDERGROUND_WATER_CREATURE`) and ink particle type.
- **Do not** conclude family, inheritance, or queue GlowSquid from this packet.

### 4. Axolotl hunt / fish aquatic tags

- Shared tag membership only. No concrete dependency that changes Squid BP reading.
- **Do not** invent an aquatic column from tags.

**C is not earned.**

---

## Final evidence conclusion

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** (identity) |
| Named missing-fact consumer | **NO** |
| Architectural escalation | **NO** |
| **C** | **Not earned** |

**Closeout:** **A** = vanilla ownership for ink VFX, swim/flee AI, water air, tags, loot, spawn; **B** = identity including LIVE Host Registry participation and generic `contributingSourceKey=squid` gestation/Analyzer route; **C** = not earned.
