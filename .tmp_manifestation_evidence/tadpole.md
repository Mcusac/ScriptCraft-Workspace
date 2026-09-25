TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Tadpole docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/tadpole.md until synthesis authorizes.
Do not mint DESIGN-BIO-MANIFEST-004 from this packet.

# Tadpole — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT.

Method: owner → biological input? → existing composition? → named live BioCraft consumer? → **A / B / C**.

Closed leaps:
- Entity replacement / growth timer alone ≠ biological inheritance, developmental composition, or a BP lifecycle field.
- Bucket admission ≠ developmental / aquatic BP fact.
- Tag membership (including `#axolotl_hunt_targets`) ≠ clade or shared BP.
- `biological phenomenon exists ≠ BioCraft needs a new representation`.

Existing BP composition checked: `organismKey`, optional `contributingSourceKey`, optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

Default: **NO** new BP field.

Authority: 1.21.1 `neoforge-21.1.208-sources.jar` → extracted under `.tmp_mc_sources/` > live BioCraft > vanilla JSON > design inventory > Wiki (orientation only).

---

## Subject

Tadpole (`minecraft:tadpole`) — inventory key `tadpole`; bio-organic; Host Registry **unregistered**; AbstractFish / Bucketable aquatic juvenile with private age timer that replaces the entity with a new Frog; slime-ball feed; swim brain; Axolotl hunt-target tag adjacency; BioCraft `MobBucketSpecimenSource` maps `TADPOLE_BUCKET` → `EntityType.TADPOLE`.

---

## Version

Minecraft Java **1.21.1** only (NeoForge mapped sources `neoforge-21.1.208-sources.jar`). Wiki orientation only.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:tadpole` |
| Inventory key | `tadpole` |
| `EntityType` | `EntityType.TADPOLE` — `EntityType.java` **662–663**: `register("tadpole", Builder.of(Tadpole::new, MobCategory.CREATURE).sized(0.4F, 0.3F).eyeHeight(0.19500001F).clientTrackingRange(10))` |
| Class | `Tadpole extends AbstractFish` (`Tadpole.java` **40**); `AbstractFish extends WaterAnimal implements Bucketable` |
| Category | `MobCategory.CREATURE` (not a dedicated aquatic category) |
| Attributes | Movement **1.0**, max health **6.0** (`createAttributes` **105–107**) |
| Hitbox constants | `HITBOX_WIDTH=0.4F`, `HITBOX_HEIGHT=0.3F` (**43–44**) |
| Bucket item | `Items.TADPOLE_BUCKET` (`Items.java` **1268–1273**; `getBucketItemStack` **191–193**) |
| Spawn egg | `Items.TADPOLE_SPAWN_EGG` (**1497–1498**) |
| Loot | Empty entity loot table (`VanillaEntityLoot.java` **870**); no `loot_table/entities/tadpole.json` extracted |
| Host Registry | **ABSENT** — `hosts.json` has **zero** `"tadpole"` entries (verified). Inventory row: unregistered / — |

---

## HIGHEST PRIORITY — Lifecycle / state-transfer probe (1.21.1 source first)

### Facts established from `Tadpole.java`

| Question | Answer | Evidence |
|----------|--------|----------|
| Is Tadpole aging? | **Yes.** Private `int age`; server `aiStep` does `setAge(this.age + 1)` each tick. | **45**, **110–114**, **222–227** |
| What state/timer controls growth? | Static threshold `ticksToBeFrog = Math.abs(-24000)` → **24000** ticks (~20 min). Growth fires when `age >= ticksToBeFrog`. | **41–42**, **222–226** |
| Persistence of age? | NBT key `"Age"`; also written into bucket `BUCKET_ENTITY_DATA`. | **118–129**, **177–187** |
| Is Tadpole entity removed? | **Yes.** `this.discard()` after successful spawn. | **247** |
| Is a new Frog entity created? | **Yes.** `Frog frog = EntityType.FROG.create(this.level())` then `serverlevel.addFreshEntityWithPassengers(frog)`. | **232–246** |
| Age-only or other gates? | **Age threshold is the gameplay gate.** Feed path only accelerates age (`ageUp(seconds)` → `setAge(age + offset*20)` using `AgeableMob.getSpeedUpSecondsWhenFeeding`). NeoForge `EventHooks.canLivingConvert(this, EntityType.FROG, …)` can cancel. | **200–220**, **229–231**, **165–167** in `AgeableMob.java` |
| What information transfers? | Position + yaw/pitch; `isNoAi`; custom name + visibility; `setPersistenceRequired()`; `fudgePositionAfterSizeChange`; grow-up sound. NeoForge `onLivingConvert(this, frog)`. | **235–246** |
| Does new Frog inherit meaningful biological state? | **No developmental / genetic / health / age / variant transfer from Tadpole.** Frog then runs `finalizeSpawn(..., MobSpawnType.CONVERSION, null)` which **re-selects variant from biome tags** (`SPAWNS_COLD/WARM_VARIANT_FROGS` else temperate) — not from Tadpole. | `Tadpole.java` **236**; `Frog.java` **273–284** |
| Generic lifecycle mechanism or Frog/Tadpole-specific? | **Tadpole/Frog-specific.** Does **not** use `AgeableMob` baby→adult (`Tadpole` is not an `AgeableMob`; Frog `isBaby()`/`setBaby` are no-ops). Does **not** use generic `Mob.convertTo`. Private age field + local `ageUp()` replacement. | Class hierarchy **40**; `Frog.java` **255–264**; `ageUp()` **229–249** |

### Upstream birth path (Tadpole-side only)

`FrogspawnBlock.hatchFrogspawn` → `spawnTadpoles`: creates **2–5** new `EntityType.TADPOLE` at water surface, `setPersistenceRequired()`, no age seed beyond default 0 (`FrogspawnBlock.java` **100–122**). Hatch delay random **3600–12000** ticks (**30–34**, **60–61**). This is block→entity spawn, not state inheritance into Tadpole.

### Classification (post-evidence)

| Candidate | A/B/C | Why |
|-----------|-------|-----|
| Age timer / grow-up replacement | **A** | Vanilla owns timer + discard + create. No live BioCraft consumer. Closed leap: replacement ≠ BP lifecycle / inheritance field. |
| Slime-ball age acceleration | **A** | `#frog_food` item interact on Tadpole only. |
| Frogspawn → Tadpole hatch | **A** | Block spawn rules; not BP. |

**Lifecycle did not earn C.**

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|--------------|--------------------|-------|
| Identity / CREATURE / size | `EntityType.TADPOLE` | **662–663** | Identity | Would be `organismKey=tadpole` if registered | No host row LIVE | **B** (identity only; registration ABSENT) |
| Age → Frog replacement | `Tadpole.setAge` / `ageUp()` | **222–249** | Entity lifecycle / replacement | Not needed (closed leap) | None | **A** |
| Feed / age speed-up | `isFood` + `feed` + `ItemTags.FROG_FOOD` | Food = slime balls; **200–208**, tag JSON | Item interact | Not needed | None | **A** |
| Temptation AI | `SensorType.FROG_TEMPTATIONS` + `FollowTemptation` | Shared frog temptations predicate `ItemTags.FROG_FOOD` (`SensorType` **42**; `TadpoleAi` **58**; `FrogAi.getTemptations`) | AI | Not needed | None | **A** |
| Swim locomotion | `SmoothSwimmingMoveControl` / `SmoothSwimmingLookControl` + `WaterBoundPathNavigation` + `TadpoleAi` `RandomStroll.swim(0.5F)` | **65–71**, **67–69** in `TadpoleAi` | Movement | Not needed | None | **A** |
| Brain activities | `TadpoleAi` CORE/IDLE (panic, look, move, tempt, swim stroll) | **31–78** | AI | Not needed | None | **A** |
| Bucket pickup (vanilla) | `Bucketable` + overrides | Always `fromBucket()==true`; `setFromBucket` no-op; save/load `"Age"` | Item + NBT | Observability ≠ composition | None needing BP | **A** |
| BioCraft bucket admission | `MobBucketSpecimenSource.mapVanillaBucket` | `Items.TADPOLE_BUCKET` → `EntityType.TADPOLE` (**123–125**); optional compressed `BUCKET_ENTITY_DATA` payload (**91–105**) | Admission / EntityType (+ bytes) | Identity already | **LIVE** identity/payload only | **B** |
| Axolotl hunt adjacency | `#minecraft:axolotl_hunt_targets` includes tadpole | Tag JSON; consumed by Axolotl hunt sensor (not Tadpole code) | Tag AI only | Tag ≠ BP | None on Tadpole | **A** |
| Aquatic / breathe tags | `#aquatic`, `#can_breathe_under_water`, `#not_scary_for_pufferfish` | Tag membership | Tag / WaterAnimal air | Not aquatic trait BP | None | **A** |
| Host contribution | `hosts.json` | **ABSENT** | Participation missing | Fail-soft / no origin | No tadpole writer path | **B** (absence = no participation; not C) |
| XP on death | `shouldDropExperience` → false | **257–259** | Presentation | Not needed | None | **A** |

No row is **C**.

---

## Bucket probe (LIVE BioCraft)

| Check | Result |
|-------|--------|
| Route exists? | **Yes.** `MobBucketSpecimenSource.mapVanillaBucket`: `stack.is(Items.TADPOLE_BUCKET)` → `EntityType.TADPOLE` |
| `supports`? | Any `MobBucketItem` (Tadpole bucket is that family) |
| Extracted specimen? | `PortableSpecimen.captured(typeKey, extentsOf(type), optional payload)` — type key from registry; extents from `EntityType` dimensions; payload = compressed bucket entity NBT if present (Age + default Bucketable fields) |
| Settlement? | Replaces carrier with empty `Items.BUCKET` |
| Biological distinction beyond existing composition? | **No.** Same identity/admission pattern as other mapped buckets (Axolotl precedent): EntityType + optional carrier bytes. Does **not** read age into a BP field. |
| Classification | **B** — identity/admission only |

Do **not** upgrade to C from bucket existence.

---

## Tags: membership → named consumer

| Tag | Membership | Named consumer (vanilla) | Meaning for Tadpole BP? |
|-----|------------|--------------------------|-------------------------|
| `#minecraft:axolotl_hunt_targets` | tropical_fish, pufferfish, salmon, cod, squid, glow_squid, **tadpole** | Axolotl attackables sensor | Hunt AI adjacency only — **not** clade / BP |
| `#minecraft:aquatic` | includes tadpole | Impaling sensitivity via `#sensitive_to_impaling` | Tag AI / enchant — not aquatic trait BP |
| `#minecraft:can_breathe_under_water` | includes tadpole | Underwater breathing rules | Survival tag — not BP |
| `#minecraft:not_scary_for_pufferfish` | includes tadpole | Pufferfish scare filter | AI adjacency |
| `#minecraft:frog_food` (**item**) | `slime_ball` | Tadpole `isFood` / `FROG_TEMPTATIONS` | Feed + tempt items |
| `#minecraft:frog_food` (**entity_type**) | slime, magma_cube | `Frog.canEat` | Frog prey — **Tadpole not a member** |

---

## Configuration audit (live BioCraft — verified)

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"tadpole"` | **ABSENT** | rg count 0 on `data/biocraft_alien/systems/hosts.json` | Unregistered; inventory matches |
| `hosts.json` `"frog"` | Not required for this packet; Tadpole-side only | — | Do not absorb Frog registration from Tadpole |
| Organism-specific JSON under `data/biocraft_alien/` | **ABSENT** for tadpole/frog keys | rg no matches in resources data tree | Vanilla remains owner |
| `MobBucketSpecimenSource` TADPOLE | **LIVE** | Java **123–125** | Admission **B** |
| Tests naming tadpole / TADPOLE_BUCKET | **ABSENT** | no matches under `src/test` | No organism-specific test consumer |
| Entity / AI / parasite JSON for tadpole | **ABSENT** | no `*tadpole*` resources | — |

---

## Tempting but rejected interpretations

- Tadpole→Frog growth → developmental / lifecycle BP field (**rejected** by closed leap + no named consumer).
- Shared `"Age"` NBT with `AgeableMob` → same baby system (**rejected**: private field on AbstractFish subclass; Frog never baby).
- `MobSpawnType.CONVERSION` / NeoForge LivingConvert → generic convertTo inheritance pipeline for BioCraft (**rejected**: local create+discard; biome re-roll of Frog variant).
- Custom name / noAi copy → biological inheritance (**rejected**: presentation/control flags only).
- Bucket Age payload → BP age / maturation composition (**rejected**: carrier specimen state; admission does not compose BP).
- `#axolotl_hunt_targets` → predator/prey BP or Tadpole/Axolotl clade (**rejected**: tag AI only).
- `#aquatic` / WaterAnimal → aquatic trait BP (**rejected**: movement/survival ownership stays vanilla).
- Frogspawn hatch → developmental composition field (**rejected**: block spawns fresh Tadpoles at age 0).
- Unregistered host → need C to explain absence (**rejected**: absence is participation, not manifestation).

---

## Potential biological relationships (Tadpole-side facts only; no auto-queue)

| Related fact | Direction | Implication |
|--------------|-----------|-------------|
| `FrogspawnBlock` → creates Tadpole | Upstream spawn | Separate entity birth; no state transfer into growth BP |
| Tadpole `ageUp()` → creates Frog, discards self | Downstream replacement | Entity-type change; Frog variant from biome at conversion site |
| Shared `ItemTags.FROG_FOOD` / `FROG_TEMPTATIONS` with Frog | Item/AI reuse | Tempt/feed items, not shared BP |
| `#axolotl_hunt_targets` | Axolotl → Tadpole | Hunt adjacency only |
| Inventory also lists `frog` separately | Parallel organism | Do **not** absorb Frog manifestation into this packet |

---

## Final evidence conclusion

| Decision | Result |
|----------|--------|
| New BP field? | **NO** |
| Existing composition sufficient? | **YES** — identity (`organismKey`) covers registration-if-added; age/replacement/swim/food/tags remain vanilla; bucket is EntityType(+payload) admission |
| Named live BioCraft consumer needing new composition? | **Bucket admission only** (`MobBucketSpecimenSource`) — identity **B**, not a developmental consumer. **No** lifecycle consumer. Host contribution **ABSENT**. |
| Escalation / DESIGN-BIO-MANIFEST-004? | **None.** Do not mint. Lifecycle **did not earn C**. |

### A/B/C closeout

| Candidate | Result |
|-----------|--------|
| Identity (unregistered) / Host absence | **B** |
| Bucket `TADPOLE_BUCKET` → `EntityType.TADPOLE` | **B** |
| Age timer, Frog replacement, feed speed-up, frogspawn hatch, swim AI, temptations, aquatic/hunt tags | **A** |
| New BP field / lifecycle C | **NO / not earned** |

**Bucket classification:** **B** (Axolotl-precedent identity/admission; no biological distinction beyond existing composition).

**Lifecycle C earned?** **No.**
