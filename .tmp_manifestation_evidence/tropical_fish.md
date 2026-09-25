TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Tropical Fish docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/tropical_fish.md until synthesis authorizes.

# Tropical Fish — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT.

Method: existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

Closed leaps: AbstractFish family ≠ aquatic BP clade; aquatic tags ≠ aquatic trait; bucketability ≠ biology; tropical packed variant ≠ subtype/BP; Axolotl prey/hunt-food ≠ ancestry; HostType / `hosts.json` registration ≠ biology field; Analyzer/vial observability ≠ composition; client pattern/base model ≠ genetic composition.

Existing BP composition checked: `organismKey`, optional `contributingSourceKey`, optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

Default: **NO** new BP field.

---

## Subject

Tropical Fish (`minecraft:tropical_fish`) — schooling AbstractFish, packed Pattern + DyeColor variant, spawn school vs rare singleton, bucket + BioCraft `MobBucketSpecimenSource`, aquatic/hunt tags, fishing item weight, Host Registry **LIVE** `living_biological`.

Out of scope: Cod, Salmon, Pufferfish, Tadpole as co-subjects (tags/admission peers only).

---

## Version

Minecraft Java **1.21.1** only. `.tmp_mc_sources/` authoritative. Wiki orientation only.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:tropical_fish` |
| `EntityType` | `EntityType.TROPICAL_FISH` — `EntityType.java` **693–695**: `register("tropical_fish", Builder.of(TropicalFish::new, MobCategory.WATER_AMBIENT).sized(0.5F, 0.4F).eyeHeight(0.26F).clientTrackingRange(4))` |
| Class | `TropicalFish extends AbstractSchoolingFish implements VariantHolder<TropicalFish.Pattern>` (`TropicalFish.java` **37**) |
| Hierarchy | `AbstractSchoolingFish` → `AbstractFish` → `WaterAnimal` + `Bucketable`; attributes via `AbstractFish.createAttributes()` health **3.0** (`DefaultAttributes` maps `TROPICAL_FISH`) |
| Category | `MobCategory.WATER_AMBIENT` |
| Spawn | `SpawnPlacements` **100**: `IN_WATER` + `TropicalFish::checkTropicalFishSpawnRules` — water below + water above; biome `#allows_tropical_fish_spawns_at_any_height` **or** surface water-animal rules (`TropicalFish.java` **207–216**; tag = lush caves in `BiomeTagsProvider`) |
| Host Registry | **LIVE** — `hosts.json` `vanilla_hosts.living_biological` includes `"tropical_fish"`; HostType `LIVING_BIOLOGICAL` |

---

## CRITICAL VARIANT PROBE (required before A/B/C)

### What the packed variant is

Vanilla packs **Pattern** (low 16 bits, includes SMALL/LARGE `Base`) + **base DyeColor** (bits 16–23) + **pattern DyeColor** (bits 24–31) into one int:

- Synched: `DATA_ID_TYPE_VARIANT` (`TropicalFish.java` **39**, **91–93**, **111–122**)
- Entity NBT: `"Variant"` (**97–109**)
- Bucket: `BUCKET_VARIANT_TAG = "BucketVariantTag"` written in `saveToBucketTag` (**144–147**); restored in `loadFromBucketTag` (**175–179**)
- `VariantHolder<Pattern>` exposes **Pattern only**; colors are parallel getters on the same packed int (**124–141**)

| Lens | Verdict | Evidence |
|------|---------|----------|
| Entity identity / specimen state | **YES** | Per-entity synched int + NBT + bucket tag; spawn assigns packed id (**184–204**); school leaders share `TropicalFishGroupData.variant` |
| Rendering configuration | **YES** | Client `TropicalFishRenderer` selects SMALL/LARGE model + base tint (**39–54**); `TropicalFishPatternLayer` maps Pattern → pattern texture + pattern tint (**52–88**) |
| Genetic / biological composition | **NO** | No breeding genetics on TropicalFish; no BP field; Pattern/`DyeColor` are appearance + school-group spawn state, not organism composition keys |
| Combination | **Entity state + rendering config** | Not genetic/BP subtype |

`COMMON_VARIANTS` (**40–63**): 22 named looks. `finalizeSpawn` (**184–204**): if group data present → copy leader variant; else **~90%** (`nextFloat() < 0.9`) pick random common + set school group data; else `isSchool = false` and fully random Pattern + two DyeColors. `isMaxGroupSizeReached` returns `!isSchool` (**116–118**) — rare spawn suppresses schooling, not a BP fact.

Tooltip (`MobBucketItem` **60–86**) reads `BucketVariantTag` for display only — still presentation.

### Does any live BioCraft consumer read variant independently of `organismKey`?

| Consumer | Reads variant into BP? | What it actually does |
|----------|------------------------|------------------------|
| `MobBucketSpecimenSource` | **NO** | `TROPICAL_FISH_BUCKET` → `EntityType.TROPICAL_FISH` (**120–121**); optional compressed `BUCKET_ENTITY_DATA` bytes as opaque payload (**91–105**, **47–52**). No parse of `BucketVariantTag` |
| `NeoForgeSpecimenRealizationAdapter.applyCapturedPayload` | **NO (not BP)** | Bucket-shaped tags → `Bucketable.loadFromBucketTag` (**165–167**) — reconstitutes **specimen entity state** (including variant) onto the live mob; comment: bucket payloads ≠ entity snapshot (**139–140**). Axolotl precedent stands: payload = specimen state, not BP composition |
| `BiologicalProfileResolver` | **NO** | Resolves `organismKey` (+ optional `contributingSourceKey`) → HostType / hostEffect / xenomorph / behavior — no variant fields |
| `BiologicalProfileDnaAnalysisPort` / `DnaAnalysisReport` | **NO** | Projects compiled profile keys only (`organismKey`, `contributingSourceKey`, `HostType`, …) |
| `DnaVialItemHelper` | **NO** | Stores only `organismKey` + optional `contributingSourceKey` |
| Client renderers | N/A (vanilla) | Rendering only; not BioCraft BP |

**Conclusion:** Variant is **entity identity/state + rendering configuration**. It is **not** genetic/BP composition. **No** live BioCraft consumer elevates packed variant into BP independently of `organismKey`. Bucket payload may preserve `BucketVariantTag` for reconstitution / observability of the specimen, same class as Axolotl bucket Variant — **not** a new composition fact.

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|--------------|--------------------|-------|
| Identity / WATER_AMBIENT / 0.5×0.4 | `EntityType.TROPICAL_FISH` | **693–695** | Identity | `organismKey=tropical_fish` | Resolver + Analyzer + host | **B** |
| Fish locomotion / flop / bucketable base | `AbstractFish` | travel / goals / `Bucketable` | Entity movement / item | Identity sufficient | None for aquatic trait | **A** |
| Schooling / follow leader | `AbstractSchoolingFish` + `isSchool` | Follow flock goal; `TropicalFishGroupData`; rare `isSchool=false` | Spawn/AI grouping | Not needed | None | **A** |
| Packed variant (Pattern + colors) | `DATA_ID_TYPE_VARIANT` + NBT/bucket | **39–179**, **184–204** | Specimen state + presentation | Not subtype field | None into BP | **A** |
| Client model / pattern layer | `TropicalFishRenderer` + `TropicalFishPatternLayer` | Model A/B + pattern textures + tints | Rendering | Not needed | None | **A** |
| Spawn rules / lush caves height | `checkTropicalFishSpawnRules` + biome tag | **207–216** | Encounter | Not origin | None | **A** |
| Vanilla bucket | `getBucketItemStack` + `saveToBucketTag` | `Items.TROPICAL_FISH_BUCKET`; `BucketVariantTag` (**149–151**, **144–147**) | Item + NBT | Observability ≠ composition | None needing BP | **A** |
| BioCraft bucket admission | `MobBucketSpecimenSource` | map + opaque payload (**120–121**, **47–52**) | Admission / EntityType adapter | Identity already | **LIVE** admission (identity/payload, not variant BP) | **B** |
| Hunt / food relation to Axolotl | Tags only | `#axolotl_hunt_targets` entity; `#axolotl_food` = tropical_fish_bucket | AI / breeding item for Axolotl | Prey ≠ ancestry | None for tropical_fish BP | **A** |
| Fishing catch (item) | loot `gameplay/fishing/fish.json` | `minecraft:tropical_fish` **weight 2** | Encounter loot | Not biology | None | **A** |
| Entity loot | `entities/tropical_fish.json` | 1× tropical_fish item; 5% bone meal | Drops | Not needed | None | **A** |
| Host contribution | `hosts.json` + gestation | `"tropical_fish"` living_biological | Identity only | `contributingSourceKey=tropical_fish` | **LIVE** generic identity | **B** |

No row is **C**. Bucket admission consumes EntityType (+ opaque payload bytes). Variant in bucket NBT is specimen state, not BP.

---

## Tags: membership → named consumer

| Tag | Membership | Named consumer | Meaning |
|-----|------------|----------------|---------|
| `#minecraft:aquatic` | tropical_fish (+ others) | Vanilla aquatic consumers | Category tag ≠ aquatic BP |
| `#minecraft:axolotl_hunt_targets` | tropical_fish first entry | Axolotl hunt AI | Prey AI only |
| `#minecraft:axolotl_food` | `tropical_fish_bucket` | Axolotl `isFood` / temptations | Breeding item for Axolotl |
| `#minecraft:can_breathe_under_water` | tropical_fish | Vanilla breath rules | Entity survival |
| `#minecraft:not_scary_for_pufferfish` | tropical_fish | Pufferfish AI | Peer tag |
| `#minecraft:allows_tropical_fish_spawns_at_any_height` | lush_caves biome | `checkTropicalFishSpawnRules` | Spawn height exception |

---

## AlienCraft configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"tropical_fish"` | **LIVE** | living_biological list | Participation / identity |
| `MobBucketSpecimenSource` TROPICAL_FISH | **LIVE** | mapVanillaBucket | Admission adapter; not aquatic/variant BP |
| Realization bucket `loadFromBucketTag` | **LIVE** generic | NeoForgeSpecimenRealizationAdapter | Specimen state restore; not BP parse |
| Resolver / Analyzer / DnaAnalysisPort | **LIVE** generic | organismKey path only | Lab observability ≠ composition |
| Dna vial observation | **LIVE** generic | organismKey ± contributingSourceKey | No variant field |
| Gestation `writeContributingSource` | **LIVE** generic | Registry path | Identity **B** |
| Tropical fish entity JSON / variant BP | **ABSENT** | — | Vanilla remains owner of looks/school |

---

## Rejected interpretations

- AbstractFish / AbstractSchoolingFish family → aquatic BP clade
- `#aquatic` / water ambient → aquatic trait field
- Bucketability / `TROPICAL_FISH_BUCKET` → biology composition requirement
- Packed Pattern + DyeColors / `BucketVariantTag` → subtype or genetic BP
- Axolotl hunt target / tropical_fish_bucket food → ancestry or shared BP with Axolotl
- HostType / `hosts.json` registration → biology beyond identity participation
- Analyzer or vial seeing `tropical_fish` → proof of variant composition
- Client PatternLayer / SMALL-LARGE base → genetic morphology field

---

## Potential relationships (no auto-queue)

- Cod / Salmon / Pufferfish / Tadpole — shared AbstractFish or bucket admission SPI; already identity-level peers
- Axolotl — hunt/food tags only; no tropical_fish BP dependency

---

## A/B/C closeout

| Candidate | Result |
|-----------|--------|
| Identity / host contribution / bucket EntityType | **B** |
| Schooling, locomotion, spawn, tags, fishing, loot, packed variant, client render | **A** |
| New BP field | **NO** |
| **C** | **Not earned** |

### Variant identity / consumer closeout (explicit)

- **Identity of variant:** combination of **per-specimen entity state** and **rendering configuration**; **not** genetic/biological composition.
- **BioCraft:** no live consumer reads Pattern/DyeColors/`BucketVariantTag` into BP independent of `organismKey`. Bucket payload may carry the tag for specimen reconstitution only (Axolotl-class precedent).
