TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Axolotl docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/axolotl.md until synthesis authorizes.

# Axolotl — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT.

Method: existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

Closed leaps: Mob effect application ≠ biological composition; Minecraft combat/status ≠ organism physiological BP field; aquatic movement ≠ aquatic trait; variant/color ≠ subtype field; bucket admission ≠ variant BP; Analyzer/vial observability ≠ composition; `DnaAnalysisPort` ≠ BP composition.

Existing BP composition checked: `organismKey`, optional `contributingSourceKey`, optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

Default: **NO** new BP field.

---

## Subject

Axolotl (`minecraft:axolotl`) — aquatic/land movement, play-dead + regeneration effect path, hunt/hostile tags, variants, bucket (vanilla + BioCraft `MobBucketSpecimenSource`), breeding, Host Registry **LIVE** `living_biological`.

---

## Version

Minecraft Java **1.21.1** only. `.tmp_mc_sources/` authoritative. Wiki orientation only.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:axolotl` |
| `EntityType` | `EntityType.AXOLOTL` — `EntityType.java` **204–205**: `register("axolotl", Builder.of(Axolotl::new, MobCategory.AXOLOTLS).sized(0.75F, 0.42F).eyeHeight(0.2751F).clientTrackingRange(10))` |
| Class | `Axolotl extends Animal implements LerpingModel, VariantHolder<Variant>, Bucketable` (`Axolotl.java` **69**) |
| Category | `MobCategory.AXOLOTLS` (dedicated category, not CREATURE) |
| Attributes | Health **14**, movement **1.0**, attack **2.0**, step height **1.0** (**300–305**) |
| Spawn | `SpawnPlacements` **92**: IN_WATER + `Axolotl::checkAxolotlSpawnRules` — below block `#axolotls_spawnable_on` (clay) |
| Host Registry | **LIVE** — `hosts.json` `vanilla_hosts.living_biological` includes `"axolotl"`; HostType `LIVING_BIOLOGICAL` |

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|--------------|--------------------|-------|
| Identity / AXOLOTLS / size | `EntityType.AXOLOTL` | **204–205** | Identity | `organismKey=axolotl` | Resolver + Analyzer + host | **B** |
| Aquatic / land locomotion | `AmphibiousPathNavigation` + `SmoothSwimming*` controls + `travel` water branch | Nav **309–310**; water travel scale **0.9** (**476–483**); land speeds in `AxolotlAi` | Entity movement | Identity sufficient | None | **A** |
| Air / dry-out | `handleAirSupply` | Max air **6000**; out of water/rain/bubble: dryOut damage (**192–201**) | Entity survival | Not needed | None | **A** |
| Play-dead trigger | `Axolotl.hurt` | Server, 1/3 chance gates, water, not already playing dead → `PLAY_DEAD_TICKS=200` (**322–335**) | Combat AI state | Not needed | None | **A** |
| Play-dead regen (self) | `PlayDead.start` | Adds `MobEffects.REGENERATION` duration **200** amp **0** to **axolotl** (`PlayDead.java` **25–29**) | Status effect on self | Effect ≠ BP trait | None | **A** |
| Playing-dead flag sync | `customServerAiStep` | Synchs `DATA_PLAYING_DEAD` from memory (**294–297**) | Presentation | Not needed | None | **A** |
| Player supporting regen | `onStopAttacking` → `applySupportingEffects` | When kill credited to player within **20** inflate: regen buff (base **100**, max **2400**) + remove mining fatigue (**394–419**) | Combat reward effect | Not organism regen trait | None | **A** |
| Hunt / hostile targets | `AxolotlAttackablesSensor` | `#axolotl_hunt_targets` / `#axolotl_always_hostiles`; target must be in water (**14–27**) | Tag-driven AI | Tag ≠ clade | None | **A** |
| Variant / color | `DATA_VARIANT` + `Variant` enum | lucy/wild/gold/cyan/blue; NBT `"Variant"`; rare blue; breed 1/1200 rare (**554–601**, **256–270**) | Presentation / entity state | Not subtype field | None | **A** |
| Vanilla bucket | `Bucketable` + `saveToBucketTag` / `loadFromBucketTag` | `Items.AXOLOTL_BUCKET`; bucket stores Variant/Age/HuntingCooldown (**349–381**) | Item + NBT | Observability ≠ composition | None needing BP | **A** |
| BioCraft bucket admission | `MobBucketSpecimenSource` | `Items.AXOLOTL_BUCKET` → `EntityType.AXOLOTL` + optional bucket NBT payload (`MobBucketSpecimenSource.java` **107–109**) | Admission / EntityType adapter | Identity already | **LIVE** admission (identity/payload, not variant BP) | **B** |
| Breeding | `getBreedOffspring` + food tag | `#axolotl_food` = tropical_fish_bucket; offspring AXOLOTL with variant pick | Vanilla birth | Child remains axolotl | None | **A** |
| Host contribution | `hosts.json` + gestation | `"axolotl"` living_biological | Identity only | `contributingSourceKey=axolotl` | **LIVE** generic identity | **B** |

No row is **C**. Bucket admission consumes EntityType (+ payload bytes), not a new composition fact. Variant in bucket NBT is specimen state, not BP.

---

## Tags: membership → named consumer

| Tag | Membership | Named consumer | Meaning |
|-----|------------|----------------|---------|
| `#axolotl_food` | tropical_fish_bucket | `isFood` / temptations | Breeding item |
| `#axolotl_hunt_targets` | tropical_fish, pufferfish, salmon, cod, squid, glow_squid, tadpole | `AxolotlAttackablesSensor.isHuntTarget` | Hunt AI |
| `#axolotl_always_hostiles` | drowned, guardian, elder_guardian | `isHostileTarget` | Combat AI |
| `#axolotls_spawnable_on` | clay | spawn rules | Encounter surface |

Loot `entities/axolotl.json` empty entity table.

---

## AlienCraft configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"axolotl"` | **LIVE** | living_biological list | Participation / identity |
| `MobBucketSpecimenSource` AXOLOTL | **LIVE** | mapVanillaBucket | Admission adapter; not aquatic/regen/variant BP |
| Resolver / Analyzer / DnaAnalysisPort | **LIVE** generic | Projection | Lab report observability ≠ composition |
| Gestation `writeContributingSource` | **LIVE** generic | Registry path | Identity **B** |
| Axolotl entity JSON | **ABSENT** | — | Vanilla remains owner |

---

## Rejected interpretations

- Aquatic movement → aquatic BP field
- Play-dead / regen → regeneration trait
- Variant/color → biological subtype composition
- Bucket admission → needs variant/aquatic BP fact
- Analyzer seeing variant or identity → BP composition
- Hunt tags → predator clade with tadpole/fish
- Grouping with Armadillo/Bat → bio-organic clade

---

## Potential relationships (no auto-queue)

- Tadpole/Frog — tadpole is hunt target only; **no** concrete dependency that changes Axolotl BP reading
- Other bucket mobs — shared admission SPI, already identity

---

## A/B/C closeout

| Candidate | Result |
|-----------|--------|
| Identity / host contribution / bucket EntityType | **B** |
| Aquatic, play-dead, regen effects, variants, hunt, breed, spawn | **A** |
| New BP field | **NO** |
| **C** | **Not earned** |
