TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Bat docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/bat.md until synthesis authorizes.

# Bat — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT.

Method: existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

Closed leaps: flying ≠ `canFly` / flight trait; ceiling attach ≠ climbing; do **not** reopen `MovementFormFsm`; Bee/Phantom/Allay/Vex flight rejections are adjacent evidence to re-check, not copied conclusions; SPRINT Bat identity is **B not C**.

Existing BP composition checked: `organismKey`, optional `contributingSourceKey`, optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

Default: **NO** new BP field.

---

## Subject

Bat (`minecraft:bat`) — custom flight in `tick`/`customServerAiStep`, `FLAG_RESTING` ceiling attach via redstone-conductor predicate, collision/push disabled, fall damage no-op, Halloween brightness spawn, Host Registry **LIVE** + SPRINT `contributingSourceKey` identity playtest.

---

## Version

Minecraft Java **1.21.1** only. `.tmp_mc_sources/` authoritative.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:bat` |
| `EntityType` | `EntityType.BAT` — `EntityType.java` **207–208**: `register("bat", Builder.of(Bat::new, MobCategory.AMBIENT).sized(0.5F, 0.9F).eyeHeight(0.45F).clientTrackingRange(5))` |
| Class | `Bat extends AmbientCreature` (`Bat.java` **29**); `AmbientCreature extends Mob` — **not** `Animal`, **not** `FlyingMob` |
| Category | `MobCategory.AMBIENT` |
| Attributes | Health **6.0** only (`createAttributes` **97–98**) — no flying speed attribute |
| Flying helpers | **Does not** extend `FlyingMob`. **Does not** use `FlyingPathNavigation` / `FlyingMoveControl`. Custom delta in `tick` / `customServerAiStep` |
| Spawn | `SpawnPlacements` **102**: ON_GROUND + `Bat::checkBatSpawnRules` — Y below sea level; brightness gate; Halloween widens threshold |
| Host Registry | **LIVE** — `"bat"` in living_biological; HostType `LIVING_BIOLOGICAL` |

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|--------------|--------------------|-------|
| Identity / AMBIENT / size | `EntityType.BAT` | **207–208** | Identity | `organismKey=bat` | Resolver + Analyzer | **B** |
| Custom flight | `Bat.tick` + `customServerAiStep` | Resting: zero motion + snap under ceiling (**117–119**). Flying: Y×0.6 damp; random target pos; signum steering (**121–174**) | Entity locomotion | Identity sufficient | None for flight trait | **A** |
| Not `FlyingMob` | Class hierarchy | `FlyingMob.java` exists for other mobs; Bat does not extend it | Implementation choice | Distinct key | None | **A** |
| Resting / ceiling attach | `FLAG_RESTING` (`DATA_ID_FLAGS` bit 1) | Attach when `getBlockState(blockpos.above()).isRedstoneConductor(level, blockpos1)` (**175–177**). Stay only while above block remains redstone conductor (**134**). Else unset resting | Block predicate + flag | Not climbing trait | None | **A** |
| Wake on player | Resting AI | `getNearestPlayer(BAT_RESTING_TARGETING, this)` range **4** → unset resting (**139–143**) | AI | Not needed | None | **A** |
| Push / collision | Overrides | `isPushable()==false`; empty `doPush` / `pushEntities` (**85–95**) | Entity physics | Not needed | None | **A** |
| Fall damage | `checkFallDamage` empty | **187–188** | Physics no-op | Not needed | None | **A** |
| Hurt wakes | `hurt` | If resting on server → unset resting (**199–205**) | State | Not needed | None | **A** |
| Spawn / Halloween | `checkBatSpawnRules` | Below sea level; brightness vs random; Halloween Oct 20–Nov 3 raises brightness allowance to **7** (**226–248**) | Encounter calendar | Not origin | None | **A** |
| Host contribution / SPRINT | `hosts.json` + gestation + SPRINT | `"bat"` living_biological; SPRINT `DESIGN-BIO-CONSEQUENCE-001` / playtest checklist: Bat displays `contributingSourceKey` | Identity only | `contributingSourceKey=bat` already | **LIVE** + **PLAYTEST** identity | **B** |

No row is **C**. SPRINT Bat is identity proof, already represented.

---

## Ceiling-attach predicate (exact)

From `Bat.customServerAiStep` (`Bat.java` **132–177**):

1. While resting: keep resting only if `level.getBlockState(blockpos.above()).isRedstoneConductor(level, blockpos)` where `blockpos` is bat block position and `blockpos1 = blockpos.above()` is used for the conductor check at **134** (argument `blockpos` in call — block state of above, conductor query with that pos).
2. Enter resting when flying: `random.nextInt(100)==0` AND `getBlockState(blockpos1).isRedstoneConductor(level, blockpos1)` (**175–177**).

Wiki "solid block" orientation must yield to **redstone conductor** predicate. Disagreement labeled: wiki may say solid/opaque; **source = `isRedstoneConductor`**.

---

## Tags / loot

Loot `entities/bat.json` empty entity table. No bat-specific food tag. No flying-path tag consumer found for Bat.

---

## AlienCraft configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"bat"` | **LIVE** | living_biological | Participation |
| SPRINT Bat playtest | **PLAYTEST** | SPRINT + S3F checklist | Identity **B**, not C |
| Resolver / Analyzer | **LIVE** generic | — | Projects key; no flight field |
| `MovementFormFsm` | Out of scope | Plan lock | Do not reopen |
| Bat entity JSON | **ABSENT** | — | Vanilla owner |

---

## Adjacent flight re-check (not copied conclusions)

| Prior organism | Flight owner | Shared with Bat? |
|----------------|--------------|------------------|
| Bee | `FlyingMoveControl` + `FlyingPathNavigation` | **No** — Bat uses neither |
| Phantom | Phantom-owned aerial AI; undead | **No** — different class/category |
| Allay / Vex | Flying helpers / Vex charge | **No** — Bat is AmbientCreature custom deltas |
| `FlyingMob` | Abstract travel helper | Bat does **not** extend it |

Shared "can be in air" observation ≠ shared flight BP representation. Prior rejections hold under re-check.

---

## Rejected interpretations

- Flight → flight trait / locomotion registry / `canFly`
- Ceiling attach → climbing trait
- Halloween spawn → biological origin calendar field
- SPRINT Bat visibility → missing-fact **C**
- Grouping with Armadillo/Axolotl → clade
- Auto-queue Ghast/Creeper from aerial adjacency

---

## A/B/C closeout

| Candidate | Result |
|-----------|--------|
| Identity / live contribution / SPRINT | **B** |
| Flight, resting, spawn, physics | **A** |
| New BP field | **NO** |
| **C** | **Not earned** |
