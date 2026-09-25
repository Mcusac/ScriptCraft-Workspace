TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Cod docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/cod.md until synthesis authorizes.
Do **not** mint `DESIGN-BIO-MANIFEST-004`. Do **not** decide for salmon / tropical_fish / pufferfish / tadpole.

# Cod — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT.

Method: existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

Closed leaps: `AbstractFish` / `AbstractSchoolingFish` family ≠ clade; aquatic tag / water movement ≠ aquatic BP field; bucketability ≠ biology; Axolotl hunt adjacency ≠ ancestry; HostType / Host Registry registration ≠ contributor biology; loot/fishing drops ≠ traits; biome spawn ≠ origin; majority fish agreement ≠ Cod evidence.

Existing BP composition checked: `organismKey`, optional `contributingSourceKey`, optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

Default: **NO** new BP field.

---

## Subject

Cod (`minecraft:cod`) — thin `Cod` subclass of `AbstractSchoolingFish`; shared fish move/nav/flop/panic/flee/bucket from `AbstractFish`; schooling from `AbstractSchoolingFish` + `FollowFlockLeaderGoal`; BioCraft `MobBucketSpecimenSource` maps `COD_BUCKET` → `EntityType.COD`; Host Registry **LIVE** `living_biological`.

---

## Version

Minecraft Java **1.21.1** / NeoForge **21.1.208** only. `.tmp_mc_sources/` authoritative. Wiki orientation only. Distinctive claims require concrete `Cod.java` + named helpers — not `AbstractFish` / wiki / memory alone.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:cod` |
| `EntityType` | `EntityType.COD` — `EntityType.java` **260–261**: `register("cod", Builder.of(Cod::new, MobCategory.WATER_AMBIENT).sized(0.5F, 0.3F).eyeHeight(0.195F).clientTrackingRange(4))` |
| Class | `Cod extends AbstractSchoolingFish` (`Cod.java` **11**) → `AbstractSchoolingFish extends AbstractFish` → `AbstractFish extends WaterAnimal implements Bucketable` |
| Category | `MobCategory.WATER_AMBIENT` |
| Attributes | `DefaultAttributes.java` **102**: `EntityType.COD` → `AbstractFish.createAttributes().build()` — **MAX_HEALTH 3.0** only (`AbstractFish.java` **40–42**) |
| Spawn placement | `SpawnPlacements.java` **93**: `IN_WATER` + `WaterAnimal::checkSurfaceWaterAnimalSpawnRules` (Y between seaLevel−13 and seaLevel; water below + water above — `WaterAnimal.java` **65–74**) |
| Host Registry | **LIVE** — `hosts.json` `vanilla_hosts.living_biological` includes `"cod"`; HostType `LIVING_BIOLOGICAL` |

### Cod concrete overrides only (`Cod.java`)

`Cod` adds **no** AI, movement, schooling, attributes, or spawn logic. Overrides:

| Method | Returns |
|--------|---------|
| `getBucketItemStack` | `Items.COD_BUCKET` (**17–19**) |
| `getAmbientSound` | `SoundEvents.COD_AMBIENT` (**22–24**) |
| `getDeathSound` | `SoundEvents.COD_DEATH` (**27–29**) |
| `getHurtSound` | `SoundEvents.COD_HURT` (**32–34**) |
| `getFlopSound` | `SoundEvents.COD_FLOP` (**37–39**) |

Everything else cited below is **implementation sharing** on parent classes, not a Cod-specific clade claim.

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|--------------|--------------------|-------|
| Identity / WATER_AMBIENT / size | `EntityType.COD` | **260–261** | Identity | `organismKey=cod` | Resolver + Analyzer + host | **B** |
| Thin subclass (bucket + sounds) | `Cod` | `Cod.java` **11–39** only | Presentation / item id | Identity sufficient | Bucket map uses EntityType | **A** (sounds); bucket row below |
| Shared fish attributes | `AbstractFish.createAttributes` | MAX_HEALTH **3.0** (**40–42**); wired via `DefaultAttributes` **102** | Entity stats | Identity sufficient | None needing BP | **A** |
| Move control | `AbstractFish.FishMoveControl` | Set in ctor (**37**); water-eye buoyancy + MOVE_TO steering (**167–200**) | Entity locomotion | Not aquatic trait | None | **A** |
| Water navigation | `WaterBoundPathNavigation` | `createNavigation` (**99–101**) | Entity navigation | Not needed | None | **A** |
| Water travel damp | `AbstractFish.travel` | In water: `moveRelative(0.01F)` + scale **0.9** + idle Y drift (**104–114**) | Entity movement | Not needed | None | **A** |
| Land flop | `AbstractFish.aiStep` | Out of water + onGround + verticalCollision → impulse + `getFlopSound()` (**118–127**); Cod supplies `COD_FLOP` | Entity physics / SFX | Not needed | None | **A** |
| Panic | `PanicGoal` on `AbstractFish` | Priority **0**, speed **1.25** (`registerGoals` **93**) | Combat AI | Not needed | None | **A** |
| Flee player | `AvoidEntityGoal` on `AbstractFish` | Priority **2**, Player, range **8**, speeds **1.6/1.4** (**94**) | Combat AI | Not needed | None | **A** |
| Random swim | `AbstractFish.FishSwimGoal` | Priority **4**; gated by `canRandomSwim()` (**95**, **203–214**) | AI | Not needed | None | **A** |
| Schooling / follow leader | `AbstractSchoolingFish` + `FollowFlockLeaderGoal` | Goal priority **5** (`AbstractSchoolingFish.registerGoals` **24–27**); leader/follower/schoolSize (**16–100**); spawn group data (**104–113**); `FollowFlockLeaderGoal` same-class flock within inflate **8** | Schooling AI | Shared impl ≠ clade | None | **A** |
| Follower swim gate | `AbstractSchoolingFish.canRandomSwim` | Returns `!isFollower()` (**39–41**) so followers defer random swim to leader path | AI coupling | Not needed | None | **A** |
| Vanilla bucket | `Bucketable` via `AbstractFish` | `mobInteract` → `bucketMobPickup` (**133–135**); `FROM_BUCKET` synched + NBT (**33**, **66–88**); default bucket save/load (**137–145**); Cod item `COD_BUCKET` | Item + NBT adapter | Observability ≠ composition | None needing BP | **A** |
| BioCraft bucket admission | `MobBucketSpecimenSource` | `Items.COD_BUCKET` → `EntityType.COD` (`MobBucketSpecimenSource.java` **111–112**); optional encoded bucket payload (**91–105**, **50**) — **path-checked**, not assumed from Axolotl | Admission / EntityType adapter | Identity already | **LIVE** admission (identity/payload, not fish BP) | **B** |
| `#aquatic` / Impaling | Tag membership → enchantment | Cod in `tags/entity_type/aquatic.json`; `#sensitive_to_impaling` includes `#aquatic` (`EntityTypeTagsProvider` **119**, **154**); Impaling targets that tag (`Enchantments.java` ~**986**) | Combat enchantment targeting | Tag ≠ aquatic BP | None BioCraft | **A** |
| Axolotl hunt adjacency | `#axolotl_hunt_targets` | Cod listed (`axolotl_hunt_targets.json`); consumer `AxolotlAttackablesSensor.isHuntTarget` (**21–22**) — prey AI for **Axolotl**, not Cod ancestry | Tag-driven AI on another mob | Hunt ≠ clade | None for Cod BP | **A** |
| Entity loot | `loot_table/entities/cod.json` | Drops `minecraft:cod` (+ furnace_smelt if on fire / smelts_loot); 5% bone meal | Kill drops | Do **not** promote to traits | None | **A** |
| Fishing loot | `loot_table/gameplay/fishing/fish.json` | Item `minecraft:cod` **weight 60** among fish pool | Fishing table | Item weight ≠ organism trait | None | **A** |
| Biome encounter | e.g. `worldgen/biome/ocean.json` | `water_ambient` spawn: type `minecraft:cod`, weight **10**, min **3**, max **6** (**169–174**) | Encounter density | Encounter ≠ origin | None | **A** |
| Host contribution | `hosts.json` + gestation | `"cod"` in living_biological (**8**) | Identity only | `contributingSourceKey=cod` | **LIVE** generic identity | **B** |

No row is **C**. Bucket admission and host contribution consume EntityType / identity keys already expressible as `organismKey` / `contributingSourceKey`. Closest precedent: Axolotl bucket admission = **B** (identity), not **C** — same shape for Cod after path verification.

---

## Tags: membership → named consumer

| Tag | Membership (Cod) | Named consumer | Biological meaning? | BioCraft consumer? |
|-----|------------------|----------------|---------------------|--------------------|
| `#minecraft:aquatic` | Yes (`aquatic.json`) | Feeds `#sensitive_to_impaling` → Impaling enchantment entity predicate | Combat targeting convenience | **None** — not a BP field |
| `#minecraft:axolotl_hunt_targets` | Yes | `AxolotlAttackablesSensor` (Axolotl brain) | Prey list for Axolotl AI | **None** for Cod composition; adjacency ≠ ancestry |
| `#minecraft:sensitive_to_impaling` | Via `#aquatic` | Impaling damage conditional | Enchantment | **None** |

No tag row earns a Cod biological Profile fact.

---

## Loot / fishing / worldgen (non-traits)

| Surface | Owner | Interpretation |
|---------|-------|----------------|
| Kill drops cod item (+ rare bone meal) | `entities/cod.json` | Drops are items, not organism traits |
| Fishing weight 60 for cod **item** | `gameplay/fishing/fish.json` | Fishing loot table, not live Cod entity biology |
| Ocean `water_ambient` spawn | biome JSON + `SpawnPlacements` + `checkSurfaceWaterAnimalSpawnRules` | Encounter rules; **not** origin / clade |

---

## AlienCraft configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"cod"` | **LIVE** | `living_biological` mobs list | Participation / identity — **registered ≠ contributor biology** |
| Host Registry → identity route | **LIVE** generic | HostType `LIVING_BIOLOGICAL` + `organismKey` / `contributingSourceKey=cod` | Identity **B** IFF gestation/Analyzer project the key — no missing biology |
| `MobBucketSpecimenSource` COD | **LIVE** | `mapVanillaBucket` **111–112** | Admission adapter EntityType (+ optional payload); not aquatic/schooling BP |
| Resolver / Analyzer / DnaAnalysisPort | **LIVE** generic | Projection | Lab observability ≠ composition |
| Gestation `writeContributingSource` | **LIVE** generic | Registry path | Identity **B** |
| Cod-specific entity JSON / Profile | **ABSENT** | — | Vanilla remains owner of fish behavior |
| Aquatic / schooling BP field | **ABSENT** (correct) | — | Do not invent |

Route check (probe 10): Host Registry `"cod"` → identity `organismKey=cod` → optional `contributingSourceKey=cod` → live consumers are **generic** host/gestation/Analyzer plus **LIVE** bucket EntityType map. No live consumer requires a missing biological fact → **no C**.

---

## Rejected interpretations

- `AbstractFish` / `AbstractSchoolingFish` inheritance → fish clade or shared biological family
- Water movement / `WATER_AMBIENT` / `#aquatic` → aquatic BP field
- Bucketability (vanilla or BioCraft admission) → biological composition fact
- Axolotl `#axolotl_hunt_targets` membership → Cod ancestry or prey-clade BP
- HostType `LIVING_BIOLOGICAL` / hosts.json listing → biological contributor beyond identity
- Cod item loot / fishing weight → organism traits
- Ocean biome spawn → origin biology
- Majority agreement with other fish packets → Cod evidence (other fish out of scope)

---

## Potential relationships (no auto-queue)

- Salmon / Tropical Fish / Pufferfish — share parents; **do not** decide here; each needs own packet
- Axolotl — hunt-tag adjacency only; Axolotl packet already treats hunt as AI, not clade
- Tadpole — also hunt target / bucketable; **not** Cod evidence

---

## Final YES/NO gates

| Gate | Answer |
|------|--------|
| Any **C**? | **NO** — no named live BioCraft consumer needs missing Cod biology |
| Any new BP field? | **NO** — default stands; identity (`organismKey` / `contributingSourceKey`) + EntityType admission suffice |
| Bucket path verified for Cod? | **YES** — `COD_BUCKET` → `EntityType.COD` at `MobBucketSpecimenSource.java` **111–112** |
| Host Registry registered? | **YES** (`"cod"` living_biological) — still identity **B**, not C |

---

## A/B/C closeout

| Candidate | Result |
|-----------|--------|
| Identity / host contribution / bucket EntityType admission | **B** |
| Shared fish move/nav/flop/panic/flee/swim, schooling, sounds, tags, loot, fishing, biomes, Axolotl hunt adjacency | **A** |
| New BP field | **NO** |
| **C** | **Not earned** |
