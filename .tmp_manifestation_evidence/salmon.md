TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Salmon docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/salmon.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Salmon — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not unregister Salmon as a conclusion of this investigation.** Salmon is already in `vanilla_hosts.living_biological`. Registration is participation, not extra biology.

Method: existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP |

Closed leaps: AbstractFish / AbstractSchoolingFish family ≠ clade; aquatic tag / WaterAnimal movement ≠ aquatic BP field; bucketability ≠ biology; salmon “size” (wiki S/M/L or school max) ≠ BP size/variant; Axolotl hunt-target membership ≠ ancestry; HostType `LIVING_BIOLOGICAL` ≠ biological composition.

Default: **NO** new BP field. Live contribution / bucket EntityType identity is **B**, not **C**.

Out of scope: Cod, Tropical Fish, Pufferfish, Tadpole decisions (independent packets only).

---

## Subject

Salmon (`minecraft:salmon`) — fixed EntityType hitbox, AbstractFish swim/panic/flee + AbstractSchoolingFish flock (`getMaxSchoolSize()=5`), bucket item, aquatic + axolotl hunt tags, fishing weight 25, Host Registry **LIVE** `living_biological`, BioCraft `MobBucketSpecimenSource` admission.

---

## Version

Minecraft Java **1.21.1** / NeoForge **21.1.208** only. `.tmp_mc_sources/` authoritative. Wiki orientation only (label wiki-only).

---

## CRITICAL: Salmon “size” probe (before A/B/C)

| Question | 1.21.1 Java answer | Owner | Named consumer |
|----------|-------------------|-------|----------------|
| Fixed `EntityType` dimensions? | **YES** — `sized(0.7F, 0.4F).eyeHeight(0.26F)` | `EntityType.SALMON` (`EntityType.java` **582–583**) | Hitbox / tracking / BioCraft `extentsOf(EntityType)` from type dims |
| Stored per-entity size state? | **NO** — `Salmon.java` has no synched size field; only inherited `FROM_BUCKET` on `AbstractFish` | — | — |
| Age / variant distinction? | **NO** — no `Variant` enum, no `VariantHolder`, no baby scale override on Salmon | — | — |
| Rendering-only size scale by entity state? | **NO** — `SalmonRenderer` single texture; `setupRotations` flop tilt only (`SalmonRenderer.java` **24–44**); no scale-from-entity-size | `SalmonRenderer` | Client presentation |
| Gameplay-relevant body-size value? | **ABSENT** as per-entity variants | — | — |
| School-size only? | **YES for the only Salmon “size” override** — `getMaxSchoolSize()` returns **5** (`Salmon.java` **16–18**); flock counter `schoolSize` on `AbstractSchoolingFish` (**17**, **58–67**, **96–99**) is membership count, not body size | `Salmon` + `AbstractSchoolingFish` | Spawn cluster / `FollowFlockLeaderGoal` / `canBeFollowed` |
| `SalmonSize` type in sources? | **ABSENT** — no `SalmonSize`, no `DATA_SIZE` under salmon paths in `.tmp_mc_sources` | — | — |

**Size-kind conclusion:** In Java 1.21.1, Salmon body size is **fixed EntityType dimensions only** (`0.7×0.4`, eye `0.26`). The sole Salmon-specific “size” API is **`getMaxSchoolSize()=5` (school/flock capacity)**. Per-entity small/medium/large salmon body variants are **absent**. Wiki S/M/L salmon — **wiki-only / Bedrock-or-later**; do not treat as 1.21.1 Java fact.

Do **not** mint a salmon size BP field from school max or wiki body tiers.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:salmon` |
| `EntityType` | `EntityType.SALMON` — `EntityType.java` **582–583**: `Builder.of(Salmon::new, MobCategory.WATER_AMBIENT).sized(0.7F, 0.4F).eyeHeight(0.26F).clientTrackingRange(4)` |
| Class | `Salmon extends AbstractSchoolingFish` (`Salmon.java` **11**) → `AbstractFish` → `WaterAnimal` |
| Category | `MobCategory.WATER_AMBIENT` |
| Attributes | `AbstractFish.createAttributes()` — health **3.0** only (`AbstractFish.java` **40–42**; `DefaultAttributes.java` **143**) |
| Salmon overrides | `getMaxSchoolSize` **5**; `getBucketItemStack` → `SALMON_BUCKET`; ambient/death/hurt/flop sounds (`Salmon.java` **16–44**). **No** other behavior overrides |
| Spawn | `SpawnPlacements` **98**: `IN_WATER` + `WaterAnimal::checkSurfaceWaterAnimalSpawnRules` |
| Host Registry | **LIVE** — `hosts.json` `vanilla_hosts.living_biological.mobs` includes `"salmon"` (**8**); `default_dna: baseline_biological`; HostType `LIVING_BIOLOGICAL` |

Implementation sharing (`AbstractFish` / `AbstractSchoolingFish`) is **code reuse**, not a biological clade for BP.

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|--------------|--------------------|-------|
| Identity / WATER_AMBIENT / fixed size | `EntityType.SALMON` | **582–583** | Identity | `organismKey=salmon` | Resolver + Analyzer + host | **B** |
| Swim / flop / bucket base | `AbstractFish` | `FishMoveControl`, water `travel` scale **0.9**, land flop (`AbstractFish.java` **104–130**); `FROM_BUCKET` only synched data (**33**, **60–73**) | Entity movement / item state | Identity sufficient | None for movement | **A** |
| Panic / flee player | `AbstractFish.registerGoals` | `PanicGoal` **1.25**; `AvoidEntityGoal` Player **8.0F** speeds **1.6/1.4** (**91–95**) | Entity AI | Not needed | None | **A** |
| Schooling / max school 5 | `Salmon.getMaxSchoolSize` + `AbstractSchoolingFish` | Override **5** (`Salmon.java` **16–18`); leader/follower + `FollowFlockLeaderGoal` (`AbstractSchoolingFish.java` **24–27**, **34–36**, **47–99**) | Flock AI param | Not body-size / not BP | None | **A** |
| Vanilla bucket | `Bucketable` via `AbstractFish` + `Items.SALMON_BUCKET` | `getBucketItemStack` (`Salmon.java` **21–24`); `MobBucketItem(EntityType.SALMON, …)` (`Items.java` **1232–1239**) | Item + default bucket NBT | Observability ≠ composition | None needing BP | **A** |
| BioCraft bucket admission | `MobBucketSpecimenSource.mapVanillaBucket` | `Items.SALMON_BUCKET` → `EntityType.SALMON` (**114–115**) | Admission / EntityType adapter | Identity already | **LIVE** admission | **B** |
| Tags aquatic / hunt | JSON tags | `#aquatic`, `#axolotl_hunt_targets` (also breathe-underwater, not_scary_for_pufferfish) | Tag-driven AI / grouping | Tag ≠ clade / ancestry | Axolotl hunt sensor consumes hunt tag — **not** Salmon BP | **A** |
| Loot / fishing | loot tables | Entity: raw salmon + 5% bone meal (`entities/salmon.json`); fishing fish pool weight **25** (`gameplay/fishing/fish.json` **12–15**) | Drops / encounter weight | Not anatomy BP | None | **A** |
| Host contribution | `hosts.json` + gestation | `"salmon"` living_biological (**8**) | Identity only | `contributingSourceKey=salmon` | **LIVE** generic identity | **B** |
| Wiki S/M/L body size | — | **Not present** in Java 1.21.1 Salmon sources | — | Reject | None | **A** (absent) |

No row is **C**. Bucket admission consumes EntityType (+ optional default bucket payload), not a size/aquatic composition fact.

---

## Tags: membership → named consumer

| Tag | Membership | Named consumer | Meaning |
|-----|------------|----------------|---------|
| `#aquatic` | includes `minecraft:salmon` | Various aquatic checks | Category tag — not BP aquatic trait |
| `#axolotl_hunt_targets` | includes `minecraft:salmon` | `AxolotlAttackablesSensor` | Axolotl hunt AI; **≠ Salmon ancestry** |
| `#can_breathe_under_water` | includes salmon | Breathing helpers | Survival tag |
| `#not_scary_for_pufferfish` | includes salmon | Pufferfish scare filter | AI adjacency |

---

## AlienCraft configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"salmon"` | **LIVE** | living_biological mobs list **8** | Participation / identity |
| `MobBucketSpecimenSource` SALMON | **LIVE** | mapVanillaBucket **114–115** | Admission adapter; not size/aquatic/school BP |
| Resolver / Analyzer / DnaAnalysisPort | **LIVE** generic | Projection | Lab observability ≠ composition |
| Gestation `writeContributingSource` | **LIVE** generic | Registry path when host | Identity **B** |
| Salmon entity JSON / variant_mappings | **ABSENT** | no salmon override | Vanilla remains owner |
| Salmon size BP / school BP | **ABSENT / not warranted** | size probe above | Default no new field |

---

## Rejected interpretations

- AbstractFish / AbstractSchoolingFish → fish clade / shared aquatic BP
- `#aquatic` or WaterAnimal travel → aquatic trait field
- Bucket admission → needs size or aquatic BP fact
- `getMaxSchoolSize()=5` or flock `schoolSize` → organism body-size composition
- Wiki small/medium/large salmon → Java 1.21.1 per-entity size variants
- `#axolotl_hunt_targets` → prey ancestry linking Salmon to Axolotl BP
- HostType `LIVING_BIOLOGICAL` / registered → extra biology or **C**
- Deciding Cod / Tropical Fish / Pufferfish from this packet

---

## Potential relationships (no auto-queue)

- Other bucket fish — shared `MobBucketSpecimenSource` SPI; each needs own packet
- Axolotl — hunt-tag adjacency only; does not change Salmon BP reading

---

## A/B/C closeout

| Candidate | Result |
|-----------|--------|
| Identity / host contribution / bucket EntityType | **B** |
| Movement, panic/flee, schooling max 5, tags, loot, fishing, fixed dims, flop render | **A** |
| Per-entity body size / wiki S/M/L / size BP | **NO** (absent as variants; school-size ≠ body size) |
| New BP field | **NO** |
| **C** | **Not earned** |

---

## Return summary (investigator)

- **Path:** `.tmp_manifestation_evidence/salmon.md`
- **A/B/C:** Identity + LIVE host + LIVE bucket map → **B**; all other probed behaviors → **A**; **C** not earned; **no** new BP field.
- **Salmon size-kind:** Fixed `EntityType` dimensions (`0.7×0.4`); **school-size only** as Salmon override (`getMaxSchoolSize=5`); **absent** as per-entity size variants / `DATA_SIZE` / `SalmonSize` / renderer state scaling. Wiki S/M/L = wiki-only for this version.
