TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Ravager docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/ravager.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Ravager — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register Ravager as a conclusion of this investigation.**

Leftover `.tmp_manifestation_evidence/ravager.md` was **orientation only**. Every owner below was re-read independently from `.tmp_mc_sources/` and live `biocraft-alien/` for this rewrite. Leftover conclusions are **not** SSOT.

Method (every behavior): existing gameplay → actual owner → manifestation class → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**. Prefer disprove **C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied independently: shared `Raider` parent ≠ Illager clade; `#raiders` ≠ ancestry; `#illager` / `#illager_friends` membership ≠ Ravager biology; Witch adjacency via raid tag; Evoker→Vex (or fangs) as Ravager biology; Host Registry absence ≠ consumer absence; interesting roar/stun/knockback ≠ sonic/defensive organ; texture path under `illager/` ≠ tag membership; raid passenger seating ≠ reproduction; NBT combat timers ≠ lifecycle genetics; inventory planning label ≠ HostType.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey` (Model A Chestburster/Drone), optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

This organism is investigated independently. Do **not** absorb Evoker, Pillager, Vindicator, Illusioner, Witch, or Vex as Ravager biology. Working hypothesis only — prefer disprove **C**.

---

## 1. Subject / Version / Target identity

### Subject

Ravager (`minecraft:ravager`) — identity; roar / stun / knockback / melee attack damage; animation/entity events; `AttackTick` / `StunTick` / `RoarTick` entity state; leaf-block destruction; target selection; raid/Raider infrastructure vs organism identity; spawn/loot/tags with named 1.21.1 consumers; Host Registry **absence**; live BioCraft consumer search despite that absence; lifecycle/reproduction absence in 1.21.1.

Out of scope as organisms: Evoker, Pillager, Vindicator, Illusioner, Witch, Vex (cited only as adjacency / negative controls — raid passengers, roar damage skip, tags).

### Version

Minecraft Java **1.21.1** / NeoForge **21.1.208**.

- `biocraft-alien/gradle.properties`: `minecraft_version=1.21.1` (**15**); `minecraft_version_range=[1.21.1,1.22)` (**19**); `neo_version=21.1.208` (**21**).
- Temporary source cache (not SSOT): `.tmp_mc_sources/`.
- Wiki = orientation / disagreement discovery only. **Source wins.** Missing source → **UNKNOWN**; no wiki / superclass / sibling inference.

### Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:ravager` |
| `EntityType` | `EntityType.RAVAGER` — `EntityType.java` **575–581**: `register("ravager", Builder.of(Ravager::new, MobCategory.MONSTER).sized(1.95F, 2.2F).passengerAttachments(new Vec3(0.0, 2.2625, -0.0625)).clientTrackingRange(10))` |
| Fire / lava HP flag | **No** `.fireImmune()` on builder. Builder default false |
| Class | `Ravager extends Raider` (`Ravager.java` **44**). **Not** `AbstractIllager`. Chain: `Ravager` → `Raider` → `PatrollingMonster` → `Monster` → `PathfinderMob` → `Mob` → `LivingEntity` |
| Category | `MobCategory.MONSTER` |
| Summonable | Builder does **not** call `noSummon()` |
| Spawn egg | `Items.RAVAGER_SPAWN_EGG` (`Items.java` **1467–1468**) |
| Attributes | `DefaultAttributes.java` **142**: `EntityType.RAVAGER` → `Ravager.createAttributes()`. Stats (`Ravager.java` **88–97**): `MAX_HEALTH` **100.0**, `MOVEMENT_SPEED` **0.3**, `KNOCKBACK_RESISTANCE` **0.75**, `ATTACK_DAMAGE` **12.0**, `ATTACK_KNOCKBACK` **1.5**, `FOLLOW_RANGE` **32.0**, `STEP_HEIGHT` **1.0**. `xpReward = 20` (**60**) |
| Dimensions | Hitbox **1.95 × 2.2**; passengerAttachments `(0.0, 2.2625, -0.0625)` |
| Spawn placement | `SpawnPlacements.java` **168**: `ON_GROUND` + `MOTION_BLOCKING_NO_LEAVES` + `Monster::checkMonsterSpawnRules` |
| Host Registry | **UNREGISTERED.** `hosts.json` (`biocraft-alien/src/main/resources/data/biocraft_alien/systems/hosts.json` **1–53**): no `"ravager"` in `living_biological`, `undead`, `unsuitable.{construct,inorganic,elemental,spiritual}`, `modded_hosts`, or `variant_mappings`. `MobHostRegistry.getHostType("ravager")` → **null** (**46–48**). `isSuitableForXenomorph("ravager")` → **false** because `hostType == null` (**68–71**) |
| Inventory row | Planning inventory may mention `ravager`. Inventory ≠ HostType ≠ biology. This packet does **not** edit it |

Independent existence paths (not origin): spawn egg, `/summon` (`canSummon` default true), raid wave spawn (`Raid.RaiderType.RAVAGER`), monster spawn-placement registration (biome natural-spawn JSON for `ravager` **not found** under `.tmp_mc_sources/data/minecraft/worldgen` this pass — see UNKNOWN).

**Raid vs Illager identity (fact, not clade):**

| Tag / type | Ravager? | Named 1.21.1 consumers (this pass) |
|------------|----------|-------------------------------------|
| `#minecraft:raiders` | **Yes** (`raiders.json` **5**; datagen `EntityTypeTagsProvider.java` **38–39**) | `BellBlockEntity.areRaidersNearby` **131**; `BellBlockEntity` glow path filter **173**; `Ravager.updateControlFlags` passenger AI gate **80**; adventure captain predicate `VanillaAdventureAdvancements.java` **411** |
| `#minecraft:illager` | **No** (`illager.json`: evoker, illusioner, pillager, vindicator only; datagen **118**) | Composes `#illager_friends` only in this extract (**141**) — no Ravager membership |
| `#minecraft:illager_friends` | **No** (aliases `#illager` — `illager_friends.json` **1–3**; datagen **141**) | `AbstractIllager.isAlliedTo` **35–40** — Ravager is **not** `AbstractIllager`, so this ally path does **not** apply to Ravager as subject |
| Extends `Raider` | **Yes** | Raid membership / wave / celebration goals (`Raider.registerGoals` **57–62**) |
| Extends `AbstractIllager` | **No** | Closed leap: Raider ≠ Illager clade |

```text
Ravager does X
    → Minecraft entity / Raider / Raid / tag owns X?
    → Ravager biological composition contributes something to X?
    → a live AlienCraft consumer needs that distinction beyond organismKey / contributingSourceKey?
```

---

## 2. Source-completeness table

| Source / owner | Present in `.tmp_mc_sources` / live tree? | Used for |
|----------------|-------------------------------------------|----------|
| `Ravager.java` | **YES** | Roar, stun, knockback, attack, ticks, leaves, goals, NBT, raid stubs |
| `Raider.java` | **YES** | Raid join, celebration, `finalizeSpawn` canJoinRaid, abstract buffs |
| `Raid.java` | **YES** | `RaiderType.RAVAGER` wave table; passenger seating on Ravager spawn |
| `AbstractIllager.java` | **YES** | Roar damage skip is `instanceof AbstractIllager`; ally tag consumer; **not** Ravager parent |
| `PatrollingMonster.java` | **YES** | Default `canBeLeader()` true — Ravager overrides false |
| `EntityType.java` RAVAGER | **YES** | Identity / size / passenger attachments |
| `DefaultAttributes.java` | **YES** | Attribute bind **142** |
| `SpawnPlacements.java` | **YES** | Encounter placement **168** |
| `Items.java` RAVAGER_SPAWN_EGG | **YES** | Egg existence |
| `Mob.java` `doHurtTarget` | **YES** | Melee damage applies `ATTACK_DAMAGE` attribute **1491–1518** |
| `loot_table/entities/ravager.json` | **YES** | Saddle only |
| `#raiders` / `#illager` / `#illager_friends` / `#dismounts_underwater` JSON + datagen | **YES** | Tag membership + named consumers |
| `BellBlockEntity.java` | **YES** | `#raiders` glow consumer |
| `VillagerHostilesSensor.java` | **YES** | Exact-type flee distance for `EntityType.RAVAGER` **15** |
| `RavagerRenderer.java` | **YES** | Presentation texture path only |
| `RavagerModel.java` | **YES** | Client pose from attack/stun/roar ticks |
| `Entity.java` `dismountsUnderwater` | **YES** | Tag consumer **2335–2336** |
| Live `biocraft-alien/src` `ravager` / `Ravager` / `RAVAGER` | **ABSENT** (grep zero under `src` main+test) | Consumer search |
| Live `hosts.json` `"ravager"` | **ABSENT** | Registry participation |
| Biome / structure JSON natural `ravager` spawn | **Not found** under `.tmp_mc_sources/data/minecraft/worldgen` this pass | Encounter path → see UNKNOWN |
| Wiki-only claims | Not authority | Excluded |

---

## 3. Ravager manifestation probe

Classify **before** A/B/C. Prove ownership. Do **not** infer sonic organ / defensive anatomy without a named live BioCraft consumer.

### Pre-A/B/C manifestation class (each interesting behavior)

| Behavior | Manifestation class (pre-gate) | Exact owner |
|----------|--------------------------------|-------------|
| Roar AoE damage + knockback | **Combat consequence** driven by **transient gameplay state** (`roarTick`) | `Ravager.roar` **220–241**; scheduled from `aiStep` when `roarTick == 10` (**159–163**); `roarTick` armed when stun ends (**173–176**) |
| Stun | **Transient gameplay state** | `blockedByShield` sets `stunnedTick = 40` (**205–210**); countdown in `aiStep` (**170–177**); client event byte 39 (**258–260**) |
| Strong knockback (shield miss / roar) | **Combat consequence** | `strongKnockback` **243–248**; from `blockedByShield` else-branch (**213**) and from `roar` (**227**) |
| Melee attack damage | **Combat consequence** | Attribute `ATTACK_DAMAGE` 12.0 (`createAttributes` **93**); `doHurtTarget` **278–283** → `Mob.doHurtTarget`; goal `MeleeAttackGoal` (**68**) |
| `attackTick` / `stunnedTick` / `roarTick` | **Transient gameplay state** (also written to NBT) | Fields **54–56**; save/load **100–116**; immobilize / LOS gates **195–202**; client pose via `RavagerModel.prepareMobModel` **111–148** |
| Leaf block destruction | **Environmental interaction** | `aiStep` **140–157**: `horizontalCollision` + `EventHooks.canEntityGrief` → destroy `LeavesBlock` only |
| Target selection | **Transient gameplay state** (AI) | `registerGoals` **72–75**: `HurtByTargetGoal(..., Raider.class)`; `NearestAttackableTargetGoal` Player / non-baby `AbstractVillager` / `IronGolem` |
| Entity events 4 / 39 | **Other** (presentation sync of transient combat timers) | `broadcastEntityEvent` / `handleEntityEvent` **254–262**, **279–280** |

### Ownership traces

#### Roar

1. **Owner:** `Ravager.roar` (private). **Not** a Raider/AbstractIllager shared spell API. **Not** a sonic-organ type.
2. **Arming chain:** Shield block → 50% `stunnedTick = 40` → on stun expiry (`stunnedTick == 0`) play `SoundEvents.RAVAGER_ROAR` and set `roarTick = 20` → when `roarTick` counts down to **10**, call `roar()`.
3. **Effect:** LivingEntity in AABB `inflate(4.0)`, predicate `NO_RAVAGER_AND_ALIVE` (**45**, **222**); deal **6.0F** `mobAttack` **unless** `instanceof AbstractIllager` (**223–225**); **always** `strongKnockback` (**227**); poof particles; `GameEvent.ENTITY_ACTION`.
4. **Illager skip proof:** Java `instanceof AbstractIllager` — **not** `#illager` tag, **not** `#raiders`, **not** Ravager anatomy. Witch (Raider, not AbstractIllager) is **not** exempted by this check.
5. **Biological input?** **No.** Vanilla combat + timer.
6. **Named BioCraft consumer?** **None** (search below).
7. **Gate:** **A**.

#### Stun / knockback

1. **Owner:** `Ravager.blockedByShield` + `strongKnockback`. Gate: `roarTick == 0` (**206**).
2. **Stun (50%):** `stunnedTick = 40` (`STUN_DURATION` **53**), `RAVAGER_STUNNED`, entity event **39**, `entity.push(this)` (**208–211**).
3. **Else:** `strongKnockback(entity)` — horizontal push ×4 / distance + 0.2 Y (**243–248**).
4. **Class:** stun = transient state; knockback = combat consequence.
5. **Biological input?** **No.** Do not invent defensive/sonic anatomy.
6. **Gate:** **A**.

#### Attack damage

1. **Owner:** attribute supplier + `MeleeAttackGoal` (**68**) + `Ravager.doHurtTarget` (**278–283**): sets `attackTick = 10`, broadcasts event **4**, plays `RAVAGER_ATTACK`, then `super.doHurtTarget` → `Mob.doHurtTarget` reads `Attributes.ATTACK_DAMAGE` (**1491–1498**).
2. **Attribute knockback:** `ATTACK_KNOCKBACK` **1.5** is separate from roar/shield `strongKnockback` helper.
3. **Equipment?** Ravager does **not** override equipment populate in this class — melee is organism method + attributes, not a held-weapon gate (Pillager crossbow cited only as negative control).
4. **Class:** combat consequence.
5. **Biological input?** Numeric vanilla combat stats — no BioCraft consumer asks for a Ravager damage field.
6. **Gate:** **A**.

#### Animation / entity state (`AttackTick` / `StunTick` / `RoarTick`)

1. **Owner:** Ravager instance ints; persisted as NBT `"AttackTick"` / `"StunTick"` / `"RoarTick"` (**100–116**).
2. **Gameplay uses:** `isImmobile` true while any > 0 (**195–197**); `hasLineOfSight` false while stun/roar > 0 (**200–202**); movement speed forced 0 while immobile (**132–133**); attack speed lerp 0.35 vs 0.3 when mobile with/without target (**135–137**).
3. **Client:** `handleEntityEvent` sets local ticks for events 4/39 (**254–260**); `RavagerModel.prepareMobModel` reads getters (**265–275**, model **111–148**) for neck/mouth pose.
4. **Class:** transient gameplay state. NBT persistence of countdown ≠ lifecycle phase ≠ genetics ≠ sonic organ.
5. **Gate:** **A**.

#### Block destruction (leaves)

1. **Owner:** `Ravager.aiStep` **140–157**.
2. **Gates:** `horizontalCollision` + `EventHooks.canEntityGrief`; only `block instanceof LeavesBlock`; `destroyBlock(..., true, this)`. If no leaf destroyed and `onGround()`, `jumpFromGround()`. Path malus for leaves set to 0.0F in ctor (**61**).
3. **Class:** environmental interaction. Leaves only — not general terrain demolition as “charge anatomy.”
4. **Gate:** **A**.

#### Target selection

1. **Owner:** Ravager `registerGoals` **65–76** + inherited `Raider.registerGoals` (banner / pathfind-to-raid / village move / celebration).
2. **Ravager-specific targets:** `HurtByTargetGoal(this, Raider.class).setAlertOthers()`; `NearestAttackableTargetGoal` Player; `AbstractVillager` with `!isBaby`; `IronGolem`.
3. **Villager flee adjacency:** `VillagerHostilesSensor` exact map includes `EntityType.RAVAGER` at **12.0F** (**15**) — exact-type table, **not** `#illager` / `#raiders`.
4. **Class:** transient AI / faction hostility.
5. **Gate:** **A**.

### BioCraft consumer test (manifestation behaviors)

Live tree grep `ravager` / `Ravager` / `RAVAGER` under `biocraft-alien/src` (main+test): **zero** matches. Generic Analyzer / resolver / gestation do not read roar/stun/attack/leaves/ticks. **No named live consumer needs these distinctions.** → **A** for all rows above (identity separately **B**).

---

## 4. Lifecycle / reproduction probe

| Question | 1.21.1 finding |
|----------|----------------|
| Extends `AgeableMob` / `Animal`? | **No.** `Monster` lineage via `Raider` / `PatrollingMonster`. |
| `getBreedOffspring` / breeding goals / love mode / food tempt? | **Absent** from `Ravager.java` (full class read). |
| Baby / age progression on Ravager? | **No** age fields. Targeting **filters** villager babies (`!isBaby` on `AbstractVillager` targets) — target AI, not Ravager offspring. |
| Variants / dyes / types? | **No** variant enum or synched variant on Ravager. |
| Transformation / `convertTo` / lightning / zombify? | **Absent** on Ravager. |
| Persistent biological state beyond combat timers + inherited Raider raid NBT? | Combat ticks are **transient combat countdowns** even though NBT-saved. Raid fields (`CanJoinRaid`, raid pointer, wave, celebrating — owned by `Raider`) are **raid system state**, not organism reproduction. |
| `applyRaidBuffs` | **Empty** (`Ravager.java` **312–313**) — no wave equipment/enchant biology. |
| `canBeLeader` | **false** (**316–318**) — overrides `PatrollingMonster` default true (**64–66**); not patrol-captain biology. |

**Explicit absence:** No breeding, offspring factory, age progression, variant, or organism-owned transformation/reproduction path exists for Ravager in 1.21.1. Do **not** infer reproduction from Raider infrastructure, raid passenger seating, or Illager adjacency.

**Classification:** absence of reproduction gameplay — **A** (nothing to project). Child identity N/A.

---

## 5. Baseline — raid / Raider / Illager infra vs organism identity; spawn/loot; tags; live BioCraft search

### Raid / Raider infrastructure vs organism identity

| Fact | Owner | Organism-native biology? |
|------|-------|---------------------------|
| Identity | `EntityType.RAVAGER` | Identity only |
| Raid membership | `Raider` fields + `finalizeSpawn` sets `canJoinRaid` true unless Witch+NATURAL (`Raider.java` **274–277**) | **No** — raid role. Ravager is not Witch, so egg/summon/raid paths set joinable |
| Wave table | `Raid.RaiderType.RAVAGER` `{0,0,0,1,0,1,0,2}` (`Raid.java` **842**); bonus case `RAVAGER` (**748–749**) | **No** — encounter table |
| Illager passengers | `Raid.spawnGroup` **518–535**: when spawning Ravager, may create Pillager (Normal last wave) or Evoker/Vindicator (Hard+) as `startRiding` passengers | **No** — raid placement. Passenger types are **other organisms**; not Ravager reproduction or Evoker→Vex biology |
| Passenger control flags | `Ravager.updateControlFlags` **79–86**: controlling passenger must be `#raiders` (or non-Mob) to keep MOVE/JUMP/LOOK/TARGET | **No** — vehicle/AI control using raid tag |
| `#dismounts_underwater` | Tag member (`dismounts_underwater.json` **10**; datagen **111**); `Entity.dismountsUnderwater` **2335–2336** | Ride/dismount rule — **A** |
| Texture package `textures/entity/illager/ravager.png` | `RavagerRenderer` **12** | Presentation path ≠ `#illager` membership ≠ clade |
| Entity loot | `entities/ravager.json`: guaranteed **saddle** only | Item production loot — **A** |
| Natural biome spawn JSON | **Not found** this pass under worldgen cache | Raid/egg/summon remain proven existence paths; see UNKNOWN |

### Live BioCraft consumer search (despite Host Registry absence)

**Mandatory:** Host Registry absence is **not** proof of consumer absence.

| Search surface | Result |
|----------------|--------|
| `biocraft-alien/src` (`*.java`, `*.json`) for `ravager` / `Ravager` / `RAVAGER` | **Zero** matches (main + test) |
| `hosts.json` | `"ravager"` **ABSENT** all groups |
| `BiologicalProfileResolver` | **LIVE** generic fail-soft; no Ravager branch (**35–56**) |
| Analyzer / `BiologicalProfileDnaAnalysisPort` / vial / report lines | **LIVE** generic `organismKey` (+ optional `contributingSourceKey`); no Ravager branch |
| `GestationManager.writeContributingSource` | **LIVE** xenomorph-side (**164–175**); origin requires eligible host → Ravager blocked by null HostType |
| `HostEligibilityService` / `MobHostRegistry` | **LIVE** gate; `"ravager"` → null HostType → unsuitable |
| Docs outside `src` (BACKLOG/inventory/dna.md mentions) | **PLANNING** only — not live consumers |

**Result:** No named Ravager-specific live BioCraft consumer. Generic identity plumbing exists; no missing biological fact demanded. **C not earned.**

---

## 6–7. Behavior ownership table (pre-A/B/C class + A/B/C)

Method: owner → manifestation class → biological input? → existing composition? → named live BioCraft consumer? → **A / B / C**.

| Behavior | Actual owner | Manifestation class | Biological input? | Existing BP? | Named live BioCraft consumer? | A/B/C |
|----------|--------------|---------------------|-------------------|--------------|-------------------------------|-------|
| Identity / MONSTER / size / passenger attach | `EntityType.RAVAGER` **575–581** | identity | Identity only | `organismKey=ravager` (fail-soft) | Generic resolver / Analyzer if key named; **no** Ravager branch | **B** |
| Java parent `Raider` / not `AbstractIllager` | Class **44** | other (implementation) | Shared parent ≠ clade | Distinct key | None for ancestry | **A** |
| Roar AoE | `roar` + `roarTick` | combat consequence ← transient state | No | Identity sufficient | **None** | **A** |
| Stun | `blockedByShield` / `stunnedTick` | transient gameplay state | No | Identity sufficient | **None** | **A** |
| Strong knockback | `strongKnockback` | combat consequence | No | Identity sufficient | **None** | **A** |
| Melee attack damage 12 | attributes + `doHurtTarget` + `MeleeAttackGoal` | combat consequence | No | Identity sufficient | **None** | **A** |
| Tick state / model pose / events 4·39 | fields + NBT + model | transient gameplay state | No | Identity sufficient | **None** | **A** |
| Leaf break | `aiStep` + griefing gate | environmental interaction | No | Identity sufficient | **None** | **A** |
| Target selection / villager flee row | goals + `VillagerHostilesSensor` | transient gameplay state | No | Identity sufficient | **None** | **A** |
| Raid wave / passenger assignment | `Raid` / `Raider` | environmental / encounter | No | Identity sufficient | **None** | **A** |
| `#raiders` / `#illager*` | tags + named readers above | other (faction/raid grouping) | Tag ≠ clade | Distinct keys | None needing Illager BP | **A** |
| `#dismounts_underwater` | tag + `Entity.dismountsUnderwater` | environmental interaction | No | Identity sufficient | Vanilla `Entity` | **A** |
| Loot saddle | entity loot table | item/block production | No | Identity sufficient | **None** | **A** |
| Breeding / offspring / age / variant / transform | **ABSENT** | — (explicit absence) | N/A | N/A | **None** | **A** |
| Host Registry participation | **ABSENT** `"ravager"` | (registry gap) | Participation missing ≠ biology field | Fail-soft key; HostType empty | Eligibility false via null HostType; **not** a missing BP fact consumer | **B** |

**No row is C.**

---

## 8. Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` key `ravager` | **UNREGISTERED / ABSENT** | Absent all groups (**1–53**) | Do **not** register here. Absence ≠ consumer absence (searched separately) |
| Live `biocraft-alien` `ravager`/`Ravager`/`RAVAGER` | **ABSENT** | Grep zero under `src` (main+test) | No Ravager-specific production code |
| `BiologicalProfileResolver` | **LIVE** generic | **35–56**: lowercased key; `MobHostRegistry.getHostType`; unknown keys fail-soft | `ravager` representable as identity without registration |
| `CompiledBiologicalProfile` | **LIVE** composition | Fields organismKey, HostType, xenomorphFormKey, hostEffectProfileId, behaviorTypeKey, contributingSourceKey | Sparse; no roar/stun/anatomy field |
| Analyzer `BiologicalProfileDnaAnalysisPort` | **LIVE** generic | resolve + `fromCompiled` | Would project fail-soft `ravager` if sampled; **no** combat/tick projection |
| `DnaSampleFromOccupant` | **LIVE** generic | organismKey from form or encode-id | Captured Ravager would sample as `ravager`; not a contributing-source carrier today |
| Gestation `writeContributingSource` | **LIVE** xenomorph-side | `GestationManager` **164–175**; requires eligible host | Ravager suitability **false** (null HostType) → cannot originate live contribution today. Block is registry gate, not missing Ravager BP field |
| `HostEligibilityService` | **LIVE** registry gate | Delegates to `MobHostRegistry.isSuitableForXenomorph` | Unregistered → ineligible path |
| Ravager entity JSON / AI config | **ABSENT** | No production Ravager config | Vanilla owns gameplay |
| JUnit named `ravager` | **ABSENT** | Generic unknown-key tests only | Fail-soft proven for unknown keys |
| Inventory / dna.md / BACKLOG mentions | **PLANNING** | Docs only | Not live consumers |

Consumer classification:

| Candidate | Classification |
|-----------|----------------|
| Resolver / Compiled BP / Analyzer / DnaSample | **LIVE** generic — not Ravager-specific; no missing-fact demand |
| Gestation contributing source | **LIVE** xenomorph machinery; Ravager **origin blocked** by null HostType |
| `HostEligibilityService` | **LIVE** gate; false via absence |
| `hosts.json` ravager row | **DEAD / ABSENT** |
| Ravager production JSON / tests | **ABSENT** |
| Inventory / design docs | **PLANNING** |

---

## 9. Tempting but rejected interpretations

| Tempting claim | Why it fails on 1.21.1 evidence |
|----------------|--------------------------------|
| Illager/Raider clade from shared AI / `HurtByTargetGoal(Raider.class)` | Java class filter + raid goals. Ravager **not** in `#illager`, **not** `AbstractIllager`. Witch ∈ `#raiders` ∉ `#illager` further breaks Illager=Raider |
| Witch adjacency via `#raiders` | Tag grouping / bell / captain / passenger-control — not ancestry |
| Evoker→Vex (or fangs) as Ravager biology | Evoker-owned summon; Ravager only appears as **raid vehicle** that may carry Evoker — placement, not biology |
| Host Registry absence ⇒ no BioCraft consumers / proves ineligibility-as-biology | Participation fact only. Fail-soft `organismKey` still exists. Full tree search required and performed |
| Roar / stun / knockback ⇒ sonic organ or defensive anatomy field | Owned as combat timers + `roar`/`blockedByShield`/`strongKnockback`. No live BioCraft consumer needs a missing anatomy fact |
| NBT `AttackTick`/`StunTick`/`RoarTick` ⇒ persistent biological lifecycle | Countdown combat state + client pose; not age/breed/variant |
| Texture under `textures/entity/illager/` ⇒ Illager organism | Renderer path string only |
| Raid passenger seating ⇒ reproduction / symbiotic biology | `Raid.spawnGroup` creates separate entity types and `startRiding` |
| Inventory `bio-organic` ⇒ HostType `LIVING_BIOLOGICAL` | Planning label only |
| Mint `DESIGN-BIO-MANIFEST-004` | No C; reserved |
| Infer breeding from `Raider` / raid infra | Explicit absence on Ravager; Raider is not AgeableMob |

---

## 10. Potential biological relationships

### 1. Raider / `#raiders` with Evoker, Pillager, Vindicator, Witch, Illusioner

- **Owner:** `Raider` + `Raid.RaiderType` + tag readers listed above.
- **Class:** faction / encounter infrastructure — **not** clade.
- **Biological input for BioCraft?** No named consumer of a shared Illager/Raider BP field.
- **Result:** **A**. Closed leap.

### 2. Hard-wave Evoker/Vindicator (or Normal Pillager) riding Ravager

- **Owner:** `Raid.spawnGroup` passenger branch **518–535**.
- **Class:** environmental / encounter seating.
- **Result:** **A**. Do not queue Evoker/Vex or Illager reports from Ravager.

### 3. Roar skips `AbstractIllager` damage

- **Owner:** `instanceof AbstractIllager` inside `Ravager.roar` **223–225**.
- **Class:** combat consequence exception (faction), not shared anatomy.
- **Result:** **A**.

### 4. Villager flee distance row (12.0F)

- **Owner:** `VillagerHostilesSensor` exact-type map **15**.
- **Class:** transient AI / fear table — not Ravager genetics.
- **Result:** **A**.

### 5. Leaf griefing

- **Owner:** `aiStep` leaves destroy.
- **Class:** environmental interaction.
- **Result:** **A**. No “trampling anatomy” field.

### 6. Generic fail-soft `organismKey = ravager` / Host Registry gap

- **Owner:** `BiologicalProfileResolver` + optional Analyzer projection; `hosts.json` absence + `MobHostRegistry` null.
- **Class:** identity / participation.
- **Named consumer of a missing Ravager biological fact?** No — gate is null HostType.
- **Result:** **B**; do not register; do not invent contribution field. **C not earned.**

---

## 11. Final evidence conclusion — YES/NO gates

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** (`organismKey` fail-soft; optional xenomorph `contributingSourceKey` already exists and is not a Ravager field) |
| Named consumer of a **missing** Ravager biological fact | **NO** (generic identity plumbing ≠ Ravager-specific missing-fact consumer; roar/stun/attack/leaves unused) |
| Architectural escalation / DESIGN-BIO-MANIFEST-004 | **NO** |
| Register `ravager` from this packet | **NO** |
| Lifecycle/reproduction present in 1.21.1 | **NO** (explicit absence) |
| Illager / Raider / sonic / defensive Profile | **NO** |

**Stop.** Prefer disprove C: **C = 0**.

### A/B/C counts

- **A:** **14** — parent/ancestry rejection; roar; stun; knockback; melee; tick/model/events; leaf break; target/flee; raid wave/passengers; tags; dismounts-underwater; loot saddle; reproduction absence.
- **B:** **2** — registry identity `organismKey=ravager` (fail-soft unregistered); Host Registry participation gap / eligibility false without minting a new BP field.
- **C:** **0**.

### Key ownership (summary)

| Topic | Owner summary |
|-------|---------------|
| Roar | Transient `roarTick` → `roar()` AoE 6 damage (skip `AbstractIllager`) + knockback — **A** |
| Stun | Shield block 50% → `stunnedTick=40` → arms roar — **A** |
| Attack | Attribute 12 + `MeleeAttackGoal` + `doHurtTarget`/`attackTick` — **A** |
| Leaves | Collision + grief gate → `LeavesBlock` only — **A** |
| Lifecycle | **Absent** breeding/offspring/age/variant/transform — **A** (absence) |

### Live consumer search despite Host Registry absence

`hosts.json` has no `ravager`. Independent live-tree search: **zero** `ravager`/`Ravager`/`RAVAGER` under `biocraft-alien/src`. Generic resolver/Analyzer/gestation/eligibility exist but need **no** missing Ravager biological fact. Host Registry absence does **not** prove consumer absence; search still found no Ravager-specific consumer and **no C**.

---

## 12. UNKNOWN list

- Natural biome / structure JSON spawn listing `minecraft:ravager` under `.tmp_mc_sources/data/minecraft/worldgen`: **not found** this pass → treat full natural-overworld encounter table as **UNKNOWN** beyond proven raid wave + egg + summon + `SpawnPlacements` registration. Do **not** infer “raid-only organism” as biology from absence of cached biome JSON alone.
- Exact rider dismount / passenger fate semantics beyond `updateControlFlags` + `#dismounts_underwater` + raid `startRiding` seating: full `Entity` passenger stack not re-expanded this pass → **UNKNOWN** if a later pass needs finer vehicle law (not required for A/B/C here).
- Any helper class referenced by wiki but missing from `.tmp_mc_sources` for a future claim → **UNKNOWN** (do not invent). No such helper was required to close roar/stun/attack/leaves/lifecycle/BioCraft gates this pass.

### Path

`.tmp_manifestation_evidence/ravager.md`
