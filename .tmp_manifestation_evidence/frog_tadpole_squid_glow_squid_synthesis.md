```text
TEMPORARY EVIDENCE — NOT PROJECT SSOT
Skeptical synthesis of a docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
```

# Skeptical synthesis — Frog, Tadpole, Squid, Glow Squid

**Status:** Temporary reviewer synthesis. **Not** project SSOT. **Not** DESIGN-BIO-MANIFEST-004.  
**Version gate:** Minecraft Java **1.21.1** (NeoForge 21.1.208 mapped sources + live `biocraft-alien`).  
**Grouping:** Authorized **contrastive evidence-management batch** only. **Not** an amphibian clade, squid family, aquatic column, or HostType conclusion. Shared Java parents / tags ≠ biological inheritance.

**Independent re-check:** Packets treated as claims. Re-opened `Frog` / `ShootTongue` / `FrogVariant` / `FrogspawnBlock`, `Tadpole.ageUp`, `Squid` / `WaterAnimal`, `GlowSquid` / `GlowSquidRenderer`, `EntityType` registrations, `#aquatic` / `#can_breathe_under_water` / `#axolotl_hunt_targets`, slime/magma_cube/frog loot, `hosts.json`, `MobBucketSpecimenSource`, `CompiledBiologicalProfile`, `BiologicalProfileResolver`, `GestationManager.writeContributingSource`. Live BioCraft `rg` for frog/tadpole/squid/glow gameplay consumers → **only** `TADPOLE_BUCKET` map + hosts list membership for `squid` / `glow_squid`.

**Primary objective:** find reasons a new Biological Profile representation is **not** earned.

**C is not earned for any organism in this group.**

**New BP field: NO.** Existing `organismKey` / optional `contributingSourceKey` remain sufficient.

---

## 1. Re-verification anchors (load-bearing claims)

| Claim | Independent anchor | Packet status |
|-------|-------------------|---------------|
| Frog not in `#aquatic`; is in `#can_breathe_under_water` | `.tmp_mc_sources/data/minecraft/tags/entity_type/aquatic.json` (no frog); `can_breathe_under_water.json` includes frog | **Hold** |
| Frog variant = texture + biome spawn + magma froglight loot | `FrogVariant` record = texture only; `Frog.finalizeSpawn` biome tags; `magma_cube.json` source_entity frog variant → froglight | **Hold** |
| Frog entity loot empty; slimeball from slime loot | `loot_table/entities/frog.json` empty pools; `slime.json` frog-as-source forces count 1 | **Hold** |
| Tongue = AI/combat/VFX, not anatomy | `ShootTongue` + `DATA_TONGUE_TARGET_ID` + `doHurtTarget`; no BioCraft tongue reader | **Hold** |
| Tadpole→Frog = discard + create; no developmental inheritance | `Tadpole.ageUp` **229–249**: position/noAi/name/persistence only; `finalizeSpawn(..., CONVERSION)` **re-rolls** Frog variant from biome | **Hold — strongest anti-C** |
| Frogspawn → fresh Tadpoles age 0 | `FrogspawnBlock.spawnTadpoles` **110–122** | **Hold** |
| Tadpole bucket LIVE identity admission | `MobBucketSpecimenSource` **123–125** → `EntityType.TADPOLE`; opaque `BUCKET_ENTITY_DATA` bytes; does not compose Age into BP | **Hold as B** |
| Squid / Glow Squid Host Registry LIVE | `hosts.json` living_biological includes `"squid"`, `"glow_squid"`; **no** `"frog"` / `"tadpole"` | **Hold** |
| Squid ink = particles + sound | `Squid.spawnInk` **182–191**; no BioCraft ink consumer | **Hold** |
| Glow “bioluminescence” = client brightness + particles; no world light | `GlowSquidRenderer.getBlockLightLevel` client-only lerp; `GlowSquid.aiStep` ambient `GLOW`; no LightEngine / `getLightEmission` | **Hold — anti-C** |
| Glow ink item ≠ organism light | Loot `glow_ink_sac` + `GlowInkSacItem` → sign `hasGlowingText` | **Hold** |
| BP composition sparse: identity + optionals only | `CompiledBiologicalProfile`: `organismKey`, optional HostType / form / effect / behavior / `contributingSourceKey` — no aquatic/tongue/glow/lifecycle fields | **Hold** |
| Live contribution writer is identity path | `GestationManager.writeContributingSource` **164–174**: encodeId → `HostRegistryPaths.registryPath` → `setContributingSourceKey` | **Hold as B** |
| No organism-specific frog/squid BioCraft gameplay modules | `rg` under biocraft-alien: only bucket map + hosts strings | **Hold** |

---

## 2. Consolidated matrix

| Organism | Interesting behavior | Actual owner | Biological input | Existing composition sufficient? | Named consumer | Result |
|----------|---------------------|--------------|------------------|-----------------------------------|----------------|--------|
| Frog | Soft identity (unregistered) | `EntityType.FROG` + generic resolver | Identity | `organismKey=frog` fail-soft | Generic resolver only | **B** |
| Frog | Host Registry | **ABSENT** | Participation missing | Fail-soft | Origin blocked | **B** |
| Frog | Variant / froglight loot gate | `FrogVariant` + biome tags + magma loot | No | Identity | None (vanilla loot) | **A** |
| Frog | Tongue hunt / pull / eat | `FrogAttackablesSensor` + `ShootTongue` + combat | No | Identity | None | **A** |
| Frog | Swim/land AI, breathe tag, fall −5 | Frog nav/AI + tags + override | No | Identity | None | **A** |
| Frog | Breed → pregnant → frogspawn | Brain memory + `TryLaySpawnOnWaterNearLand` + block | No | Identity | None | **A** |
| Tadpole | Soft identity (unregistered) | `EntityType.TADPOLE` | Identity | Fail-soft key | Generic resolver | **B** |
| Tadpole | Host Registry | **ABSENT** | Participation missing | Fail-soft | Origin blocked | **B** |
| Tadpole | Bucket admission | `MobBucketSpecimenSource` | EntityType + opaque payload | Identity | **LIVE** | **B** |
| Tadpole | Age timer → Frog replacement | `Tadpole.setAge` / `ageUp` | Lifecycle replacement; **no** bio state transfer | Identity sufficient | None needing BP | **A** |
| Tadpole | Feed/tempt/swim/tags/hunt adjacency | AbstractFish + tags + AI | No | Identity | None | **A** |
| Squid | Identity / Host LIVE | `EntityType.SQUID` + `hosts.json` | Identity | `organismKey=squid` | Resolver / Analyzer / eligibility | **B** |
| Squid | Contribution route | Gestation writer + Resolver | Identity | `contributingSourceKey=squid` | **LIVE** generic | **B** |
| Squid | Ink / swim / flee / water air / tags / loot | `Squid` / `WaterAnimal` / tags / loot | No | Identity | None for ink/swim | **A** |
| Glow Squid | Identity / Host LIVE | `EntityType.GLOW_SQUID` + hosts | Identity | Registered key | Resolver / Analyzer | **B** |
| Glow Squid | Contribution route | Same generic writer | Identity | `contributingSourceKey=glow_squid` | **LIVE** generic | **B** |
| Glow Squid | Dark-ticks / client glow / particles / glow ink / dark spawn | `GlowSquid` + renderer + loot + item | No | Identity | None for glow/ink | **A** |
| Glow Squid | `extends Squid` | Java inheritance | Implementation sharing | Distinct key already | None treating as clade | **A** |

**No row is C.**

---

## 3. Shared findings (genuine implementation facts — not clade)

1. All four are distinct EntityTypes with distinct MobCategories where it matters (Frog/Tadpole `CREATURE`; Squid `WATER_CREATURE`; Glow Squid `UNDERGROUND_WATER_CREATURE`).
2. `#aquatic` membership is **not** shared: Squid, Glow Squid, Tadpole **yes**; Frog **no**. Cannot mint an aquatic BP column from this batch.
3. Host Registry participation splits the batch: Squid + Glow Squid **LIVE** `living_biological`; Frog + Tadpole **ABSENT**. Participation ≠ missing BP fact.
4. BioCraft named consumers in this batch are **identity-only**: generic resolver soft-fail; `TADPOLE_BUCKET` → EntityType; gestation `contributingSourceKey` for registered squid keys. No tongue/glow/lifecycle/aquatic field readers.
5. Vanilla tag adjacency (`#axolotl_hunt_targets`, `#not_scary_for_pufferfish`, breathe-under-water) drives other entities’ AI/enchant rules — not BioCraft composition.

---

## 4. Important differences (break over-broad abstractions)

| Difference | Why it matters |
|------------|----------------|
| Frog ∉ `#aquatic`; Tadpole ∈ `#aquatic` | “Amphibian aquatic column” fails on tag evidence alone |
| Frog unregistered; Squid/Glow registered | Cannot treat batch as one HostType story |
| Tadpole bucket exists; Frog does not implement `Bucketable` | Bucket admission is Tadpole-only identity **B** |
| Tadpole→Frog transfers **no** variant/health/age genetics | Developmental story is entity replacement, not inheritance |
| Glow Squid category + dark spawn + dark-ticks vs Squid surface spawn + plain ink | Inheritance = code reuse; not shared bioluminescence biology |
| Frog tongue vs Squid ink | Both presentation/combat FX under vanilla; neither has a BioCraft consumer |

---

## 5. Rejected abstractions

| Temptation | Why rejected |
|------------|--------------|
| Aquatic column / `#aquatic` BP field | Frog non-member; tag owns Impaling etc.; no BioCraft aquatic reader |
| Frog–Tadpole clade / amphibian family | Separate EntityTypes; lifecycle is block/entity replacement; Axolotl hunt includes tadpole **not** frog |
| Squid family / cephalopod clade from `GlowSquid extends Squid` | Implementation sharing; distinct keys already suffice |
| Bioluminescence / light-emission BP | Client render brightness + particles; no world light; no BioCraft glow consumer |
| Adaptation-from-variant (frog warm/cold/temperate) | Texture + spawn biome + loot gate; not adaptation trait |
| Tongue-as-anatomy | `ShootTongue` combat/VFX sequencing |
| Conversion-as-inheritance without audit | Tadpole→Frog audited: **no** developmental/genetic transfer; variant re-rolled at conversion site |
| Bucket Age / dark-ticks / ink_sac → BP fields | Carrier/payload/item/state — not composition without a named consumer |
| Host Registry LIVE → C | Registration + contribution key remain identity **B** |

---

## 6. Biological Profile result A/B/C summary

| Organism | A | B | C |
|----------|---|---|---|
| Frog | Tongue, variant/loot, amphibious AI, tags, breed/spawn chain | Soft identity + host absence | **Not earned** |
| Tadpole | Age→Frog replacement, feed/swim/tags, frogspawn hatch | Soft identity + host absence + LIVE bucket EntityType | **Not earned** |
| Squid | Ink, swim/flee, water survival, tags, loot | LIVE host + `contributingSourceKey=squid` | **Not earned** |
| Glow Squid | Dark-ticks, client glow, particles, glow ink, dark spawn, Squid inheritance | LIVE host + `contributingSourceKey=glow_squid` | **Not earned** |

---

## 7. New representation

**None earned.**

No Potential new representation. Do **not** implement. Do **not** mint `DESIGN-BIO-MANIFEST-004`.

---

## 8. Frog / Tadpole developmental transition (specific audit)

**Question:** Does the transition introduce biological information unavailable from existing organism identity/composition?

**Answer: No.**

| What transfers Tadpole → Frog | Biological composition fact? |
|------------------------------|------------------------------|
| Position, yaw/pitch | Spatial — no |
| `isNoAi`, custom name/visibility | Presentation/control — no |
| `setPersistenceRequired`, size fudge, grow-up sound | Persistence/presentation — no |
| NeoForge LivingConvert hooks | Event cancellation/notify — no BP payload |
| Frog `finalizeSpawn(..., CONVERSION)` | **Re-selects variant from biome tags** — explicitly **not** Tadpole-derived |

What does **not** transfer: health, age, variant, “developmental stage,” genetics, or any field `CompiledBiologicalProfile` could store today.

Therefore: the transition is **biologically meaningful as vanilla gameplay** (timer + entity replacement) but introduces **zero** BioCraft-needed biological information beyond knowing the resulting EntityType is `frog` (already covered by identity if/when that key is used). Lifecycle **does not earn C**.

---

## 9. Recommended next investigation

**No unresolved evidence dependency** from this batch forces another organism (no glow→squid family queue; no frogspawn→extra packet; no aquatic-column follow-on).

**Restore inventory independent sequence → independent Strider** (`vanilla_organism_inventory.md` § sequence). Treat that as inventory ordering only — **not** architectural guidance from this batch or any prior Strider note. Do not auto-queue further amphibians, cephalopods, or aquatics from tags/inheritance.

---

## 10. Explicit gate recommendation

| Gate | Decision |
|------|----------|
| All results A/B with no C? | **Yes** |
| Authorize docs-only closeout? | **YES** |
| Scope if authorized | Canonical organism reports + research-adjacency comparison + inventory status notes only |
| Forbidden | Java / `hosts.json` / BP architecture / Model A / Feature / BACKLOG / SPRINT / `dna.md` / DESIGN-BIO-MANIFEST-004 |

---

## Short verdict

- **C earned?** **No.**
- **Docs gate authorized?** **YES** (A/B only).
- **Next branch?** Independent **Strider** (inventory sequence; no evidence dependency from this batch).
