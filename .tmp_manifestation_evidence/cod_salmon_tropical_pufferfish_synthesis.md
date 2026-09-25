```text
TEMPORARY EVIDENCE — NOT PROJECT SSOT
Skeptical synthesis of a docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
```

# Skeptical synthesis — Cod, Salmon, Tropical Fish, Pufferfish

**Status:** Temporary reviewer synthesis. **Not** project SSOT. **Not** DESIGN-BIO-MANIFEST-004.  
**Version gate:** Minecraft Java **1.21.1** (NeoForge 21.1.208 mapped sources).  
**Grouping:** Authorized **contrastive evidence-management batch**. Ordinary fish / size probe / variant-heavy fish / chemically defensive fish. **Not** a clade, aquatic family, `AbstractFish` biological column, or HostType conclusion. Shared Java parent ≠ biological inheritance.

**Independent re-check:** Packets treated as claims. Re-read `Cod` / `Salmon` / `TropicalFish` / `Pufferfish`, `AbstractFish` / `AbstractSchoolingFish` / `Bucketable` / `FollowFlockLeaderGoal`, `EntityType` registrations, `SpawnPlacements`, `DefaultAttributes`, entity loot + fishing/fish, tags (`aquatic`, `axolotl_hunt_targets`, `not_scary_for_pufferfish`), `hosts.json`, `MobBucketSpecimenSource` fish-bucket maps. Grep live BioCraft for `PuffState` / `BucketVariantTag` / fish-specific BP reads → **none** beyond EntityType admission.

**Primary objective:** find reasons a new Biological Profile representation is **not** earned.

**C is not earned for any organism in this group.**

**New BP field: NO.** Existing `organismKey` / optional `contributingSourceKey` remain sufficient.

---

## Seven-step C burden (applied to every proposed distinction)

| Proposed distinction | 1 Present 1.21.1? | 2 Owner? | 3 More than impl/state/render? | 4 Live BioCraft needs it? | 5 Already from key/source/existing BP? | 6 Genuinely biological? | 7 C remains? |
|----------------------|-------------------|----------|--------------------------------|---------------------------|----------------------------------------|-------------------------|--------------|
| Shared `AbstractFish` / water move / bucketability | Yes | Parent classes | No — implementation sharing | No | Identity covers type | No — gameplay impl | **No** |
| `#aquatic` / Impaling | Yes | Tag + enchant | No | No BioCraft | n/a | No — combat tag | **No** |
| Axolotl hunt membership | Yes | Axolotl sensor | No | No for fish BP | n/a | No — prey AI | **No** |
| Schooling (Cod/Salmon/Tropical) | Yes | `AbstractSchoolingFish` | No | No | Identity | No — AI | **No** |
| Salmon “size” S/M/L | **No** in Java 1.21.1 | — | — | — | — | Wiki/other edition | **No** |
| Salmon school max 5 | Yes | `getMaxSchoolSize` | No — spawn/AI param | No | Identity | No | **No** |
| Tropical packed variant | Yes | Entity + NBT + render | No — state/render | Payload opaque only | Identity + specimen NBT | No — presentation | **No** |
| Puffer puff 0/1/2 | Yes | `PUFF_STATE` + goal/tick | No — gameplay state | No | Identity | No — combat AI | **No** |
| Puffer poison contact | Yes | `MobEffects.POISON` | No — status effect | No | Identity | Effect ≠ composition | **No** |
| Bucket admission (all four) | Yes | `MobBucketSpecimenSource` | Admission only | LIVE EntityType map | `organismKey` / EntityType | No missing biology | **No** (stays **B**) |
| Host Registry LIVE keys | Yes | `hosts.json` | Participation ≠ trait | LIVE generic gestation | `contributingSourceKey` | Identity only | **No** (stays **B**) |

---

## Independent verification of tempting claims

| Tempting claim | Independent finding | Verdict |
|----------------|---------------------|---------|
| Four fish form a BioCraft clade / aquatic family | Distinct EntityTypes; Cod/Salmon/Tropical share schooling parent; Pufferfish does **not**. Shared `AbstractFish` is code reuse. | **Reject grouping.** Administrative contrastive batch only |
| Aquatic movement → aquatic BP field | `FishMoveControl` + `WaterBoundPathNavigation` + `travel` on `AbstractFish` | **Reject.** Entity locomotion (**A**) |
| Bucketability → biology | Vanilla `Bucketable`; BioCraft maps bucket item → EntityType (+ opaque payload) | **Reject C.** Admission/identity (**B**) |
| Salmon size → BP / size variant | `Salmon.java` has **no** `DATA_SIZE` / Variant; only `getMaxSchoolSize()=5`. EntityType fixed `0.7×0.4`. No `SalmonSize` type in sources. | **Reject.** Fixed type dims + school max (**A**); wiki S/M/L = wiki-only |
| Tropical pattern/color → subtype / genetics | Packed `Variant` / `BucketVariantTag`; client pattern layer | **Reject.** Specimen state + rendering (**A**); no live BP parser |
| Puffer poison / puff → defensive biology trait | Puff goal → synched state → contact damage + POISON duration `60*i`; dims scale | **Reject.** Transient/persistent gameplay state + effect (**A**); effect ≠ composition |
| Axolotl prey → fish ancestry | All four in `#axolotl_hunt_targets` | **Reject.** Hunt AI adjacency only |
| HostType `LIVING_BIOLOGICAL` → biology | Registered living_biological | **Reject.** Suitability/participation, not manifestation |
| Auto-queue Tadpole/Frog | Shared bucket map + hunt tags | **Reject auto-queue.** No unresolved dependency |

---

## Consolidated matrix

| Organism | Interesting behavior | Actual owner | Biological input | Composition sufficient? | Named consumer | Result |
|----------|---------------------|--------------|------------------|-------------------------|----------------|--------|
| Cod | Identity | `EntityType.COD` | Identity | `organismKey=cod` | Resolver / Analyzer | **B** |
| Cod | Move / school / panic / flee / flop / sounds | `AbstractFish` / `AbstractSchoolingFish` / Cod sounds | No | Identity | None | **A** |
| Cod | Bucket admission | `MobBucketSpecimenSource` | EntityType + payload | Identity | **LIVE** | **B** |
| Cod | Host contribution | `hosts.json` + gestation | Identity | `contributingSourceKey=cod` | **LIVE** generic | **B** |
| Salmon | Identity | `EntityType.SALMON` | Identity | Registered key | Resolver / Analyzer | **B** |
| Salmon | School max 5; fixed dims; no body-size state | `Salmon.getMaxSchoolSize`; EntityType sized | No | Identity | None | **A** |
| Salmon | Bucket / host | Same LIVE paths as Cod | Identity | Identity | **LIVE** | **B** |
| Tropical Fish | Identity | `EntityType.TROPICAL_FISH` | Identity | Registered key | Resolver / Analyzer | **B** |
| Tropical Fish | Packed variant / spawn rules / render | Entity + biome tag + client layers | No | Identity + specimen NBT | None for BP | **A** |
| Tropical Fish | Bucket / host | LIVE EntityType (+ opaque variant in payload) | Identity | Identity | **LIVE** | **B** |
| Pufferfish | Identity | `EntityType.PUFFERFISH` | Identity | Registered key | Resolver / Analyzer | **B** |
| Pufferfish | Puff chain / poison / non-schooling | Concrete `Pufferfish` + AbstractFish move | No | Identity | None for BP | **A** |
| Pufferfish | Bucket / host | LIVE EntityType | Identity | Identity | **LIVE** | **B** |

---

## Genuine shared findings (implementation facts, not clades)

1. All four are distinct `WATER_AMBIENT` EntityTypes with `AbstractFish.createAttributes()` (MAX_HEALTH 3).
2. All four implement vanilla `Bucketable` via `AbstractFish`; BioCraft `MobBucketSpecimenSource` path-checks each bucket item → matching EntityType (**B**, Axolotl-class).
3. All four are Host Registry **LIVE** `living_biological` → identity `contributingSourceKey` (**B**).
4. Cod / Salmon / Tropical Fish share `AbstractSchoolingFish` schooling; **Pufferfish does not** — breaks “all fish school” abstraction.
5. All four appear in `#aquatic` and `#axolotl_hunt_targets` — tag AI / enchant targeting, not origin.

## Important differences that break over-broad abstractions

| Difference | Why it matters |
|------------|----------------|
| Pufferfish ≠ schooling | Cannot treat AbstractFish family as uniform behavior set |
| Salmon has **no** per-entity size variants in 1.21.1 | Cannot invent size-as-BP from wiki |
| Tropical variant is packed presentation state | Cannot mint subtype field without consumer |
| Puffer puff/poison is combat state/effect | Cannot mint poison trait without consumer |
| Cod is thin sound/bucket subclass | Ordinary fish baseline remains identity-only |

## Rejected abstractions

Fish family · aquatic BP field · AbstractFish trait · shared schooling biology · shared poison biology · variant-as-subtype · salmon size-as-BP · bucketability-as-biology · Axolotl-prey ancestry · HostType-as-biology · auto Tadpole/Frog queue.

---

## A/B/C summary and new-representation gate

| Organism | A | B | C |
|----------|---|---|---|
| Cod | Vanilla fish impl | Identity + LIVE host + LIVE bucket | **Not earned** |
| Salmon | Vanilla fish + school max; no body-size state | Identity + LIVE host + LIVE bucket | **Not earned** |
| Tropical Fish | Variant/state/render/spawn | Identity + LIVE host + LIVE bucket | **Not earned** |
| Pufferfish | Puff→poison chain | Identity + LIVE host + LIVE bucket | **Not earned** |

**New BP field: None earned.**

---

## Next organism (evidence dependency)

No unresolved dependency from this batch requires another organism before Strider (no Tadpole/Frog from hunt/bucket adjacency; no dolphin/squid forced by `#aquatic`).

**Restore next → independent Strider.** Do not auto-queue Tadpole/Frog. Leave any leftover Strider temp packet to be investigated on its own merits.

---

## Documentation gate

Result is **A/B and no C** → authorized to write synthesis-verified canonical organism reports + research-adjacency comparison + inventory status notes only. No Java / `hosts.json` / BP / Model A / Feature / BACKLOG / SPRINT changes. Do not mint `DESIGN-BIO-MANIFEST-004`. Do not update `dna.md` (no surviving C).
