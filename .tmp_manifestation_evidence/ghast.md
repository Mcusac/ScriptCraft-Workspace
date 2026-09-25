TEMPORARY EVIDENCE — NOT PROJECT SSOT

Do not treat this file as canonical design documentation.
Do not promote into manifestations/ghast.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004 without the authorized Phase 3 pass.

# Ghast — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

Method (every behavior): owner → biological input? → `organismKey` / `contributingSourceKey` enough? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied independently: `extends FlyingMob` is **evidence, not** a `canFly` BP field (Bee/Phantom/Blaze hover already closed that leap); HostType `ELEMENTAL` ≠ biology; inventory `bio-organic` ≠ HostType; Happy Ghast is **absent in 1.21.1** and must not be conflated; Blaze hover / Magma Cube Nether / Happy Ghast absence do **not** earn Ghast traits; shared “fireball” name with Blaze ≠ shared biological cause (`LargeFireball` vs `SmallFireball`); shared `hosts.json` `unsuitable.elemental` list with Blaze ≠ elemental clade.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey`, optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

**Default: NO new BP field.** Creeper / Warden / Witch / Blaze / Happy Ghast / Magma Cube are **not absorbed**.

---

## Subject

Ghast (`minecraft:ghast`) — ordinary 1.21.1 Ghast identity. Scope: EntityType; `Ghast extends FlyingMob implements Enemy`; fireImmune; large fireballs; charging flag; Nether biome encounter; Host Registry `unsuitable.elemental` (with Blaze); BioCraft identity / suitability routing.

Out of scope as organisms: Happy Ghast (version-gate absence already recorded), Blaze, Magma Cube, Phantom, Creeper, Warden, Witch.

---

## Version

Minecraft Java **1.21.1** only. Mapped sources in `.tmp_mc_sources/` are authoritative. Wiki is orientation / disagreement discovery only; **source wins**.

Post-1.21.1 Happy Ghast mechanics are **out of range** and were **not** imported as Ghast evidence.

---

## Phase 1 gate

| Required probe | Status |
|----------------|--------|
| `.tmp_mc_sources/.../monster/Ghast.java` | **Present** (339 lines) |
| `FlyingMob.java` | **Present** (54 lines) |
| Related loot / tags | **Present** (`loot_table/entities/ghast.json`; `#fall_damage_immune` includes ghast) |
| BioCraft `hosts.json` elemental group | **Present** (`"ghast", "blaze"`) |
| Happy Ghast anti-conflation | **Confirmed absent** in 1.21.1 `EntityType` / sources jar (prior version-gate; re-checked: no `HAPPY_GHAST` in extracted `EntityType.java`) |

Gate **PASS** — proceed (not UNKNOWN).

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:ghast` |
| `EntityType` | `EntityType.GHAST` — `EntityType.java` **381–390**: `register("ghast", Builder.of(Ghast::new, MobCategory.MONSTER).fireImmune().sized(4.0F, 4.0F).eyeHeight(2.6F).passengerAttachments(4.0625F).ridingOffset(0.5F).clientTrackingRange(10))` |
| Fire / lava | **`fireImmune()`** on the builder |
| Class | `Ghast extends FlyingMob implements Enemy` (`Ghast.java` **34**). `FlyingMob extends Mob` (**8**) |
| Category | `MobCategory.MONSTER` |
| Dimensions | **4.0 × 4.0**, eyeHeight **2.6**, tracking **10** |
| Default attributes | `DefaultAttributes.java` **116**: `Ghast.createAttributes()` — max health **10.0**, follow range **100.0** (`Ghast.java` **102–104**). Constructor `xpReward = 5` (**40**) |
| Spawn placement | `SpawnPlacements.java` **114**: `ON_GROUND`, `MOTION_BLOCKING_NO_LEAVES`, `Ghast::checkGhastSpawnRules` |
| Spawn rules | Non-PEACEFUL, `random.nextInt(20) == 0`, then `checkMobSpawnRules` (`Ghast.java` **131–137**). Cluster size **1** (**140–142**) |
| Host Registry | **REGISTERED** under `vanilla_hosts.unsuitable.elemental.mobs` with `"blaze"` (`hosts.json` **29–32**). Group `default_dna: elemental`. **Not** in `living_biological` |
| Suitability | `HostType.ELEMENTAL` → `isSuitableForXenomorph("ghast")` **false** (`HostType.java` **28**, **44–45**) |
| Inventory baseline | Inventory category **bio-organic**; HostType **ELEMENTAL**. Columns are independently owned — **do not collapse** |

Happy Ghast: **no** `EntityType.HAPPY_GHAST` in 1.21.1. Ordinary Ghast does **not** substitute for that absent organism.

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing composition? | Named BioCraft consumer? | Refined manifestation classification | A/B/C |
|----------|--------------|-----------------|-------------------|----------------------|--------------------------|--------------------------------------|-------|
| Identity / size / `fireImmune` | `EntityType.GHAST` | `EntityType.java` **381–390** | Identity only | `organismKey = ghast` | Generic resolver. **No** Ghast-named branch | **identity** | **B** |
| `FlyingMob` superclass | `FlyingMob` | Empty `checkFallDamage`; custom `travel`; `onClimbable` false (`FlyingMob.java` **14–53**) | Movement helper. **Not** a Flight Profile | Distinct key already | **None.** Phantom also extends `FlyingMob`; Blaze does **not** | **transient movement** | **A** |
| Float / look / shoot goals | Inner Ghast goals | `RandomFloatAroundGoal`, `GhastLookGoal`, `GhastShootFireballGoal` (`Ghast.java` **45–50**, **161–338**) | AI | Identity sufficient | None | **transient gameplay state** / AI | **A** |
| Charging flag | `DATA_IS_CHARGING` | Synched; set when `chargeTime > 10`; **not** NBT-saved (`Ghast.java` **35–59**, **97–99**, **145–158**) | Presentation / attack windup | Identity sufficient | None | **transient gameplay state** | **A** |
| ExplosionPower NBT | Instance field | Default **1**; NBT `"ExplosionPower"` (`Ghast.java` **36**, **145–158**) | Fireball constructor arg | Identity sufficient | None | **persistent entity state** (vanilla) | **A** |
| Large fireball | `GhastShootFireballGoal` | `new LargeFireball(..., getExplosionPower())` (`Ghast.java` **289**) | Projectile. **Not** Blaze `SmallFireball` | Identity sufficient | None | **combat** / projectile | **A** |
| Reflected-fireball vulnerability | `hurt` / `isInvulnerableTo` | Player-reflected `LargeFireball` deals **1000** (`Ghast.java` **70–93**) | Combat special case | Identity sufficient | None | **combat consequence** | **A** |
| `#fall_damage_immune` | Entity-type tag | Includes `minecraft:ghast` (also blaze, phantom, chicken, …) | Tag ≠ clade / ≠ canFly | Distinct key | Vanilla fall, not BioCraft | **environmental interaction** | **A** |
| Nether biome spawn | Worldgen JSON | `nether_wastes`, `soul_sand_valley`, `basalt_deltas` list ghast. Encounter ≠ origin | Spawn ≠ origin BP | Not an origin field | None | **environmental interaction** | **A** |
| Ghast tear / gunpowder loot | Vanilla loot table | Tear 0–1; gunpowder 0–2 | Drops ≠ anatomy | Not needed | None | **item/block production** | **A** |
| Spyglass advancement | `spyglass_at_ghast.json` | Adventure criterion | Advancement ≠ biology | Not needed | None | presentation / player challenge | **A** |
| Host Registry / HostType | `hosts.json` `unsuitable.elemental` | Shared list with Blaze. `ELEMENTAL` description: “Elemental beings - no biological structure” (`HostType.java` **28**) | **Participation + suitability routing.** HostType **never earns C** | `organismKey=ghast` + `HostType.ELEMENTAL` + `hostEffectProfileId=elemental` | **LIVE** `MobHostRegistry.isSuitableForXenomorph` → false; facehugger gate | **identity** + eligibility routing | **B** |
| Gestation contribution | Blocked by suitability | `isValidFacehuggerHost` requires suitable HostType (`HostEligibilityService.java` **33–45**) | No live Model A write from a Ghast host in current lifecycle | Fail-soft / blocked origin is still identity, not a missing flight/fire fact | None missing | **identity** (blocked participation) | **B** |

**No row is C.**

---

## FlyingMob ≠ canFly BP (mandatory anti-conflation)

| Record | Fact |
|--------|------|
| Ghast | `extends FlyingMob` |
| Phantom | `extends FlyingMob` (separate investigated organism; flight remains vanilla) |
| Blaze | **`extends Monster`**, hover via Y-damp — **not** `FlyingMob` |
| Happy Ghast | **Absent** in 1.21.1 |
| Bee | Custom flight, not `FlyingMob` (locked: no `canFly` field) |

`FlyingMob` is a Minecraft movement base class. Recording that Ghast extends it is **A** (vanilla movement owner). It does **not** authorize a Biological Profile `canFly` / Flight Profile. Shared superclass with Phantom ≠ flying clade.

---

## Fireball ≠ Blaze biology (mandatory)

| | Ghast | Blaze (adjacency only, not absorbed) |
|--|-------|--------------------------------------|
| Projectile | `LargeFireball` | `SmallFireball` |
| Superclass | `FlyingMob` | `Monster` (hover) |
| HostType | `ELEMENTAL` (same **list** as Blaze) | `ELEMENTAL` |
| Shared biological cause? | **Not established.** Same HostType bucket and “fireball” word are **not** a fire-organ / elemental clade |

---

## AlienCraft configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"ghast"` | **LIVE** | `unsuitable.elemental.mobs` with `"blaze"` (**29–32**) | Participation. Shared list ≠ clade |
| `MobHostRegistry.getHostType("ghast")` | **LIVE** | `HostType.ELEMENTAL` | Suitability routing, **not** composition |
| `isSuitableForXenomorph("ghast")` | **LIVE** | **false** | Current eligibility outcome. HostType never earns C |
| Elemental host-effect pack | **LIVE pack, not Ghast-specific** | `parasite/host_effects/elemental.json`; empty attachment effects; lifecycle-incompatible | Attachment routing |
| Resolver identity | **LIVE** generic | `organismKey=ghast`, `HostType.ELEMENTAL`, `hostEffectProfileId=elemental` | Identity sufficient |
| Ghast xenomorph JSON | **ABSENT** | No `*ghast*.json` under `entity/xenomorph` | Vanilla remains gameplay owner |
| `bootstrap_entries` | **ABSENT** ghast | Catalog does not load a ghast variant | Not a missing BP field |
| `AdmissionTransactionTest` `minecraft:ghast` | **TEST** | Large extents (4.0, 4.0) for “does not fit” rollback | Fixture uses vanilla size, **not** a Ghast biology consumer |
| Happy Ghast Host Registry | **ABSENT** | No `happy_ghast` key. Do not treat ordinary `"ghast"` as Happy Ghast | Anti-conflation |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails on 1.21.1 evidence |
|----------------|--------------------------------|
| `FlyingMob` ⇒ `canFly` BP | Movement base class; Bee/Phantom already closed this leap |
| HostType `ELEMENTAL` ⇒ elemental biology / clade with Blaze | HostType is suitability taxonomy. Shared JSON list ≠ composition |
| Inventory bio-organic vs HostType ELEMENTAL is “wrong” | Independently owned columns. Do not reconcile in this packet |
| LargeFireball ⇒ shared fire organ with Blaze | Different projectile class and combat owners |
| Nether spawn / `fireImmune` / Magma Cube Nether ⇒ thermal trait | Encounter + EntityType flag. Distinct organisms |
| Happy Ghast absence completes Ghast manifestation by adjacency | Absence ≠ A for Happy Ghast; ordinary Ghast is this packet only |
| Unsuitable ⇒ no biology / no identity | Registration + resolver still project `organismKey=ghast` (**B**) |
| Admission ghast extents test ⇒ size is a missing BP field | TEST fixture; vanilla EntityType size already exists |

---

## Potential biological relationships (hypotheses only — after ownership)

### 1. Ghast identity / HostType routing

- **Owner:** `hosts.json` + `HostType.ELEMENTAL` + resolver.
- **Biological input?** Organism key only.
- **Named consumer?** LIVE suitability false; LIVE identity projection.
- **Result:** **B**. HostType decision is **not C**.

### 2. Flight as biological capability

- **Owner:** `FlyingMob` + Ghast move control.
- **Named consumer?** None.
- **Result:** **A**.

### 3. Fireball / elemental kinship with Blaze

- **Owner:** Distinct projectile/AI classes; shared HostType bucket only.
- **Named consumer?** None for a shared fire/elemental fact.
- **Result:** **A**. Reject elemental column.

**C is not earned for any relationship.**

---

## Wiki disagreements

| Orientation claim | 1.21.1 authority | Conclusion |
|-------------------|------------------|------------|
| Happy Ghast is a Ghast variant in this version | No Happy Ghast EntityType | **Absent**; do not conflate |
| Ghast is elemental biology because HostType says so | HostType is suitability text, not BP | **B** routing, not C |
| Ghast and Blaze share fireball biology | `LargeFireball` vs `SmallFireball` | **Reject** |

---

## Final evidence conclusion

| Gate | Result |
|------|--------|
| New BP field | **No** |
| Existing composition sufficient | **Yes** — `organismKey=ghast` + `HostType.ELEMENTAL` |
| Named consumer of a missing fact | **None** |
| Architectural escalation | **None** |

**A + B; C not earned.**
