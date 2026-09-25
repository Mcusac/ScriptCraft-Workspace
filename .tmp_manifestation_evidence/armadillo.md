TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Armadillo docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/armadillo.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004 until synthesis authorizes.

# Armadillo — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT.

Method: existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP |

Closed leaps: scute item ≠ stored organism property; roll/scare ≠ defensive-morphology BP field; shared `Animal` ≠ clade; spawn biome ≠ origin; unregistered ≠ must register; interesting behavior ≠ consumer.

Existing BP composition checked: `organismKey`, optional `contributingSourceKey`, optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

Default: **NO** new BP field.

---

## Subject

Armadillo (`minecraft:armadillo`) — roll/scare state, scare detection, rolled damage reduction, scute timer/brush drop, breeding/`#armadillo_food`, spawn block tag, Host Registry **ABSENT**.

---

## Version

Minecraft Java **1.21.1** only. Mapped sources in `.tmp_mc_sources/` are authoritative. Wiki orientation only; **source wins**.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:armadillo` |
| `EntityType` | `EntityType.ARMADILLO` — `EntityType.java` **195–196**: `register("armadillo", Builder.of(Armadillo::new, MobCategory.CREATURE).sized(0.7F, 0.65F).eyeHeight(0.26F).clientTrackingRange(10))` |
| Class | `Armadillo extends Animal` (`Armadillo.java` **49**) |
| Category | `MobCategory.CREATURE` |
| Attributes | Health **12.0**, movement **0.14** (`Armadillo.createAttributes` **77–78**); `DefaultAttributes` binds ARMADILLO |
| Spawn | `SpawnPlacements` **101**: ON_GROUND + `Armadillo::checkArmadilloSpawnRules` — below block in `#armadillo_spawnable_on` + bright enough |
| Host Registry | **ABSENT** from `hosts.json` (no `"armadillo"`). Unregistered ≠ ineligible forever; do **not** register from this packet |

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|--------------|--------------------|-------|
| Identity / CREATURE / size | `EntityType.ARMADILLO` | **195–196** | Identity | `organismKey=armadillo` | Generic resolver fail-soft | **B** |
| Synched roll state | `ARMADILLO_STATE` + `ArmadilloState` enum | IDLE/ROLLING/SCARED/UNROLLING (`Armadillo.java` **55–57**, **403–467**); NBT `"state"` | Entity presentation/AI state | Not needed | None | **A** |
| Scare / roll-up AI | `ArmadilloAi` + `ArmadilloBallUp` + `ARMADILLO_SCARE_DETECTED` sensor | Brain PANIC when `DANGER_DETECTED_RECENTLY` (`ArmadilloAi.java` **154–167**, **173–240**) | Entity AI | Identity sufficient | None | **A** |
| `isScaredBy` predicate | `Armadillo.isScaredBy` | Inflate **7×2×7**; undead tag OR last hurter OR sprinting/passenger player (`Armadillo.java` **234–246**) | Threat AI | Not needed | None | **A** |
| Rolled damage reduction | `Armadillo.hurt` | If scared: `(amount - 1.0F) / 2.0F` (**289–294**) | Damage handling | Not armor trait | None | **A** |
| Scute timer drop | `customServerAiStep` | Adult non-baby: `--scuteTime` then `spawnAtLocation(Items.ARMADILLO_SCUTE)`; interval 5–10 min (**140–151**) | Item production | scute ≠ composition | None | **A** |
| Brush scute | `mobInteract` + `brushOffScute` | Brush ability → `Items.ARMADILLO_SCUTE`; baby false (**316–344**) | Item interact | Not needed | None | **A** |
| Food / tempt / breed | `isFood` + `ArmadilloAi` temptations + `AnimalMakeLove` | `#armadillo_food` = spider_eye; offspring `EntityType.ARMADILLO.create` (**73–74**, **224–226**) | Vanilla animal loop | Child remains armadillo | None | **A** |
| Spawn block tag | `checkArmadilloSpawnRules` | `#armadillo_spawnable_on` includes animals_spawnable_on, badlands terracotta, red_sand, coarse_dirt | Encounter | Not origin | None | **A** |
| Host contribution | `hosts.json` | **ABSENT** | Participation missing | Fail-soft identity | Origin blocked | **B** |

No row is **C**. Consumer existence test: no live BioCraft consumer needs shell/scute/roll beyond `organismKey`.

---

## Tags: membership → named consumer

| Tag | Membership | Named 1.21.1 consumer | Meaning |
|-----|------------|----------------------|---------|
| `#minecraft:armadillo_food` | spider_eye | `Armadillo.isFood` / temptations | Breeding item, not diet trait |
| `#minecraft:armadillo_spawnable_on` | animals_spawnable_on + terracotta/sand/dirt | `checkArmadilloSpawnRules` | Spawn surface, not origin |
| `#minecraft:undead` | used by scare | `isScaredBy` | Threat AI input, not Armadillo clade |

Loot table `entities/armadillo.json` is empty entity table (no drops listed beyond empty structure) — scute is timer/brush owned, not death loot.

---

## AlienCraft configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"armadillo"` | **ABSENT** | Not in file | Unregistered. Do not register here |
| Resolver / Analyzer | **LIVE** generic | Sparse compiled refs | Projects key if present; no roll/scute field |
| Gestation contribution | **N/A** | Unregistered | No live `contributingSourceKey=armadillo` |
| Armadillo entity JSON | **ABSENT** | No production config | Vanilla remains owner |

---

## Rejected interpretations

- Shell / roll → armor or defensive-morphology BP field
- Scute item → stored biological property or composition fact
- Undead scare → undead ancestry
- Unregistered → must register to finish investigation
- Administrative grouping with Axolotl/Bat → bio-organic clade

---

## Potential relationships (do not queue unless synthesis finds concrete dependency)

- Donkey/Camel adjacency via desert spawn surfaces — **no** evidence dependency for Armadillo interpretation
- Turtle scute item name adjacency — different item; different owner

---

## A/B/C closeout

| Candidate | Result |
|-----------|--------|
| Identity | **B** (`organismKey=armadillo`; fail-soft) |
| Roll/scare/damage/scute/breed/spawn | **A** |
| New BP field | **NO** |
| **C** | **Not earned** — no named live missing-fact consumer |
