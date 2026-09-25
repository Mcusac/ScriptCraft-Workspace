TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Pufferfish docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/pufferfish.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Pufferfish — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not unregister Pufferfish as a conclusion of this investigation.** Pufferfish is already in `vanilla_hosts.living_biological`. Registration is participation, not extra biology.

Method: existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP |

Closed leaps: `AbstractFish` family ≠ clade; `#aquatic` / water locomotion ≠ aquatic BP; bucketability ≠ biology; puffer poison / `MobEffects.POISON` ≠ poison trait BP (Axolotl play-dead regen precedent); puff inflation / `PuffState` ≠ BP; Axolotl `#axolotl_hunt_targets` prey membership ≠ ancestry; `HostType` / registered ≠ biology / **C**.

Default: **NO** new BP field. Live contribution identity is **B**, not **C**.

Existing BP composition checked: `organismKey`, optional `contributingSourceKey`, optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

---

## Subject

Pufferfish (`minecraft:pufferfish`) — `AbstractFish` (not schooling), puff-state inflate/deflate AI + contact damage/poison, dimension scale by puff, vanilla + BioCraft bucket admission, fishing/loot item, Host Registry **LIVE** `living_biological`.

Out of scope: Cod/Salmon/TropicalFish as subjects; Axolotl as subject (prey-tag only).

---

## Version

Minecraft Java **1.21.1** only. `.tmp_mc_sources/` authoritative. Wiki orientation only.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:pufferfish` |
| `EntityType` | `EntityType.PUFFERFISH` — `EntityType.java` **569–570**: `register("pufferfish", Builder.of(Pufferfish::new, MobCategory.WATER_AMBIENT).sized(0.7F, 0.7F).eyeHeight(0.455F).clientTrackingRange(4))` |
| Class | `Pufferfish extends AbstractFish` (`Pufferfish.java` **29**). **Not** `AbstractSchoolingFish` |
| Category | `MobCategory.WATER_AMBIENT` |
| Attributes | `DefaultAttributes` → `AbstractFish.createAttributes()` — max health **3.0** (`AbstractFish.java` **40–41**) |
| Spawn | `SpawnPlacements` **97**: `IN_WATER` + `WaterAnimal::checkSurfaceWaterAnimalSpawnRules` |
| Host Registry | **LIVE** — `hosts.json` `vanilla_hosts.living_biological.mobs` includes `"pufferfish"` (line **9**); `default_dna: baseline_biological`. No pufferfish `variant_mappings` |
| Suitability | Registered living_biological → currently suitable. Registered ≠ extra biology |

---

## CRITICAL: puff → state → consequence chain (classify BEFORE A/B/C)

Documented from `Pufferfish.java` only. Classification axes: **persistent/identity** · **transient gameplay** · **rendering** · **externally consumed biology**.

### Chain (complete)

| Step | Owner / mechanism | 1.21.1 evidence | Classification |
|------|-------------------|-----------------|----------------|
| 1. Synched puff state | `PUFF_STATE` `EntityDataAccessor<Integer>` | Defined **30**; `defineSynchedData` default **0** (**54–56**); getters/setters **59–65** | **Persistent entity gameplay state** (synched). **Not** organism identity. **Not** BioCraft-consumed biology |
| 2. State constants | `STATE_SMALL=0`, `STATE_MID=1`, `STATE_FULL=2` | **44–46** | Enum-like gameplay levels |
| 3. Transient timers | `inflateCounter`, `deflateTimer` | Package fields **31–32**; **not** written to NBT | **Transient gameplay** only |
| 4. Scary-mob predicate | `SCARY_MOB` | Creative players excluded (**34–36**); types in `#not_scary_for_pufferfish` excluded (**38**); `TargetingConditions.forNonCombat()` **40–43** | Tag-driven AI input; consumer is **puffer AI**, not BioCraft |
| 5. Inflate trigger goal | `PufferfishPuffGoal` | Registered goal priority **1** (**97–99**). `canUse`: living entities in bbox `inflate(2.0)` matching targeting (**211–217**). `start`: `inflateCounter=1`, `deflateTimer=0` (**221–223**). `stop`: `inflateCounter=0` (**227–228**) | **Transient gameplay AI** |
| 6. Inflate / deflate tick | `tick` server AI branch | While `inflateCounter > 0`: 0→1 with blow-up sound; after counter **>40** and state 1 → state 2 (**105–114**). Else if state ≠ 0: deflate timer; **>60** at 2 → 1; **>100** at 1 → 0 with blow-out sounds (**115–125**) | **Transient gameplay** state machine driving synched state |
| 7. Contact damage + poison (mobs) | `aiStep` → `touch` | If alive and `getPuffState() > 0`: nearby `Mob`s in bbox `inflate(0.3)` matching targeting (**132–141**). `touch`: damage `(1 + i)`, then `MobEffects.POISON` duration `60 * i` amp **0** (**144–149**) | **Transient combat gameplay** + **mob effect**. Effect ≠ BP trait (Axolotl regen precedent) |
| 8. Contact damage + poison (players) | `playerTouch` | ServerPlayer, `i > 0`: same damage formula; sting game event; poison `60 * i` (**156–164**) | Same as row 7 |
| 9. Collision / size scale | `getDefaultDimensions` + `getScale` | Scales parent dims by puff: **0.5 / 0.7 / 1.0** for 0/1/else (**188–200**). `onSyncedDataUpdated` refreshes dims on `PUFF_STATE` (**68–74**) | **Derived gameplay collision** from state; also feeds client presentation |
| 10. NBT persist | `addAdditionalSaveData` / `readAdditionalSaveData` | Writes `"PuffState"` (**77–79**); reads clamped `min(..., 2)` (**86–88**) | **Persistent vanilla entity state** for continuity — **not** identity composition, **not** externally consumed biology |
| 11. Client model choice | `PufferfishRenderer` | Switches small/mid/big model from `getPuffState()`; shadow radius scales with state (`PufferfishRenderer.java` **37–51**) | **Rendering only** |

### Chain verdict (pre-A/B/C)

| Question | Answer |
|----------|--------|
| Is puff state organism **identity**? | **No** — identity remains `EntityType.PUFFERFISH` / `organismKey=pufferfish` |
| Is puff / poison **externally consumed biology** by a named live BioCraft consumer? | **No** — no BioCraft type reads `PuffState`, inflate timers, or poison application as composition |
| Does persistence of `PuffState` earn a BP field? | **No** — vanilla entity NBT continuity ≠ biological profile fact |
| Mob effect poison | Combat status effect path; **≠** BP trait |

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|--------------|--------------------|-------|
| Identity / WATER_AMBIENT / 0.7×0.7 / eye 0.455 | `EntityType.PUFFERFISH` | `EntityType.java` **569–570** | Identity | `organismKey=pufferfish` | Resolver + Analyzer + host | **B** |
| Class hierarchy / non-schooling | `Pufferfish extends AbstractFish` | `Pufferfish.java` **29**; Cod/Salmon/TropicalFish extend `AbstractSchoolingFish` | Implementation sharing ≠ clade | Identity sufficient | None | **A** |
| Movement / swim / flop / bucket base | `AbstractFish` | Fish move control, water travel, panic/avoid/swim goals, `Bucketable` (`AbstractFish.java`) | Entity movement / item | Not aquatic BP | None | **A** |
| Distinctive puff AI | `PufferfishPuffGoal` on concrete class | `registerGoals` **97–99**; goal **203–230** | Entity AI | Not needed | None | **A** |
| Puff inflate/deflate + contact poison | `tick` / `aiStep` / `playerTouch` | Chain above **103–165** | Combat + effect | Effect ≠ BP | None | **A** |
| Dimension scale by puff | `getDefaultDimensions` | **188–200** | Collision / presentation | Not needed | None | **A** |
| NBT `PuffState` | save/load on entity | **77–88** | Persistent entity state | Not composition | None | **A** |
| Vanilla bucket | `getBucketItemStack` → `Items.PUFFERFISH_BUCKET` | **92–94**; `Items.java` **1223–1230** `MobBucketItem(EntityType.PUFFERFISH, …)` | Item + entity data component | Observability ≠ composition | None needing BP | **A** |
| BioCraft bucket admission | `MobBucketSpecimenSource.mapVanillaBucket` | `Items.PUFFERFISH_BUCKET` → `EntityType.PUFFERFISH` (**117–118**) | Admission / EntityType adapter | Identity already | **LIVE** admission (identity only; does not consume puff/poison) | **B** |
| Tags (scary / aquatic / hunt prey) | Tag JSON + vanilla AI | See tags table | Tag-driven AI / membership | Tag ≠ trait | None for BP | **A** |
| Loot / fishing weight 13 | loot tables | `entities/pufferfish.json`; fishing `fish.json` weight **13** | Drops / encounter | Not anatomy BP | None | **A** |
| Client puff models | `PufferfishRenderer` | Model switch by puff state | Rendering | Not needed | None | **A** |
| Host contribution | `hosts.json` + gestation | `"pufferfish"` living_biological | Identity only | `contributingSourceKey=pufferfish` | **LIVE** generic identity | **B** |

No row is **C**. Bucket admission consumes EntityType (+ generic payload encoding), not puff state as composition. Poison/puff are vanilla-owned.

---

## Tags: membership → named consumer

| Tag | Membership (puffer relevant) | Named consumer | Meaning |
|-----|------------------------------|----------------|---------|
| `#not_scary_for_pufferfish` | turtle, guardians, cod, **pufferfish**, salmon, tropical_fish, dolphin, squid, glow_squid, tadpole (`not_scary_for_pufferfish.json`) | `Pufferfish.SCARY_MOB` / inflate goal | Puffer AI inflate filter — **not** BioCraft biology |
| `#aquatic` | includes `minecraft:pufferfish` | Vanilla aquatic helpers | Membership ≠ aquatic BP |
| `#axolotl_hunt_targets` | includes `minecraft:pufferfish` | `AxolotlAttackablesSensor` (Axolotl AI) | Prey list for **Axolotl**; does **not** invent puffer ancestry/clade |
| `#can_breathe_under_water` | includes `minecraft:pufferfish` | Vanilla breathing rules | Survival tag ≠ BP |

---

## AlienCraft configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"pufferfish"` | **LIVE** | `living_biological` mobs list line **9** | Participation / identity |
| `MobBucketSpecimenSource` PUFFERFISH | **LIVE** | mapVanillaBucket **117–118** | Admission adapter; not puff/poison/aquatic BP |
| Resolver / Analyzer / DnaAnalysisPort | **LIVE** generic | Projection | Lab report observability ≠ composition |
| Gestation `writeContributingSource` | **LIVE** generic | Registry path when host used | Identity **B** |
| Pufferfish entity JSON / puff BP | **ABSENT** | No BioCraft puff/poison consumer | Vanilla remains owner |
| Reads of `PuffState` / poison as composition | **ABSENT** | Grep biocraft-alien: only bucket EntityType map | No named consumer beyond identity |

---

## YES / NO gates

| Gate | Answer |
|------|--------|
| Biological input required beyond EntityType / `organismKey`? | **NO** |
| Existing composition (`organismKey` ± contributing source) sufficient for live consumers? | **YES** |
| Named live BioCraft consumer needs puff/poison/aquatic distinction? | **NO** |
| New BP field earned? | **NO** |
| **C** earned? | **NO** |

---

## Rejected interpretations

- `AbstractFish` / shared fish implementation → fish clade BP
- Water travel / `#aquatic` / `#can_breathe_under_water` → aquatic BP field
- Bucketability / `PUFFERFISH_BUCKET` → biology or subtype field
- Contact `MobEffects.POISON` → poison trait BP (same reject class as Axolotl self-regen)
- Inflate / `PuffState` / dimension scale → inflation BP
- `#axolotl_hunt_targets` membership → ancestry or shared biology with Axolotl
- Host Registry `LIVING_BIOLOGICAL` / `HostType` → biological composition fact
- Fishing weight / food item / brewing ingredient → anatomy or toxin BP
- Client puff models → biological profile

---

## Potential relationships (no auto-queue)

- Cod / Salmon / TropicalFish — shared `AbstractFish` movement/bucket base; schooling split is implementation, not clade queue
- Axolotl — hunt-target tag only; no dependency that changes Pufferfish BP reading
- Other bucket mobs — shared admission SPI; already identity **B**

---

## Independent consumer verdict

**Does any live BioCraft consumer need a biological distinction beyond `organismKey`?**

**NO.** Live paths are: (1) Host Registry identity → generic contributing source / Analyzer; (2) `MobBucketSpecimenSource` EntityType map for `PUFFERFISH_BUCKET`. Neither reads puff state, inflate timers, poison durations, aquatic tags, or AbstractFish hierarchy as composition. **No BP from puff/poison without a named consumer. Mob effect ≠ BP trait.**

---

## A/B/C closeout

| Candidate | Result |
|-----------|--------|
| Identity / host contribution / bucket EntityType | **B** |
| AbstractFish movement, non-schooling, puff AI, inflate/deflate, poison contact, dimension scale, NBT `PuffState`, tags, loot/fishing, client models | **A** |
| New BP field | **NO** |
| **C** | **Not earned** |

---

*TEMPORARY / NOT PROJECT SSOT — investigator packet only.*
