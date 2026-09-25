TEMPORARY EVIDENCE — NOT PROJECT SSOT
Skeptical synthesis — Creeper / Ghast / Warden / Witch
Do not treat this file as canonical design documentation.
Do not mint DESIGN-BIO-MANIFEST-004. Phase 3 docs may promote conclusions only if no new BP representation is earned.

# Skeptical synthesis — Creeper / Ghast / Warden / Witch

**Primary objective:** find why a new BP representation is **not** earned. Prefer disprove **C**.

**Version:** Minecraft Java **1.21.1** / NeoForge **21.1.208**.

**Packets:** [creeper.md](./creeper.md) · [ghast.md](./ghast.md) · [warden.md](./warden.md) · [witch.md](./witch.md)

This quartet is an **evidence-management / contrastive** batch, **not** an explosive / elemental / boss / illager clade.

Formal C gate (re-applied): C is earned **only** when an existing production BioCraft consumer’s behavior currently depends on an organism-specific biological fact that existing composition (`organismKey` / `contributingSourceKey` / sparse compiled fields) cannot express without loss. Vanilla mechanic, entity property, AI goal, tag, HostType, or planned config **never** earns C.

---

## Independent spot-checks (load-bearing)

### Creeper lightning is a flag, not replacement

Re-opened `Creeper.thunderHit` (`.tmp_mc_sources/.../Creeper.java` **219–222**):

- Calls `super.thunderHit` then `DATA_IS_POWERED = true`.
- Same EntityType. No `create` / `discard`.
- Contrast `Villager.thunderHit` (**820–837**): `EntityType.WITCH.create` + villager `discard()`.

**Classification:** persistent entity flag. **A**. Not ancestry. Not `explosiveCapability`.

Re-opened `creeper.json` vs `MobEntityConfigLoader`: `bootstrap_entries` **does** list creeper (**5**). `infection_spread: true` is parsed; `SpecializedXenomorphManager` maps it to in-memory `"explosive_ability"`. Production callers of `getSpecialAbilities` / `getVariantProperties`: **none**. Planned/unused config **does not earn C**.

`dna.md` already forbids recreating Creeper fuse/explosion in a profile.

### Ghast `FlyingMob` is not `canFly`; Happy Ghast still absent

Re-opened `Ghast.java` **34** (`extends FlyingMob`) and `EntityType.java` **381–390** (`fireImmune()`, 4×4).

Re-opened `Blaze.java` **28**: `extends Monster`, uses `SmallFireball` — **not** `FlyingMob`, **not** `LargeFireball`.

Grep of extracted `EntityType.java` for `HAPPY_GHAST` / `happy_ghast`: **no matches**. Ordinary `"ghast"` in `hosts.json` `unsuitable.elemental` with blaze (**29–32**) is **not** Happy Ghast.

**Classification:** movement / projectile owners **A**. HostType `ELEMENTAL` suitability false is routing **B**, not C. No `canFly` field.

### Warden sonic boom has no BioCraft consumer

Re-opened `SonicBoom.java` (10 damage, `sonicBoom` damage source, knockback) and `WardenAi.java` FIGHT activity.

Workspace search of `biocraft-alien/src/main` for `SonicBoom` / `sonicBoom`: **no production hits**.

`warden.json` exists under `boss/inorganic` but is **not** in `bootstrap_entries`. `deep_mob_configs.boss` comment: planning matrix only. **boss is not a biological category.**

Inventory **bio-organic** is planning-only (not read by Java). HostType **INORGANIC** **is** a live `isSuitableForXenomorph` decision. Independently owned — **not reconciled**.

**Classification:** combat AI **A**. HostType routing **B**. Sonic boom without consumer **does not** mint an organ field.

### Witch is a Raider, not an Illager type

Re-opened `Witch.java` **44**: `extends Raider implements RangedAttackMob` — **not** `AbstractIllager`.

`#illager` JSON: evoker, illusioner, pillager, vindicator — **no witch**. `#raiders` **includes** witch.

`hosts.json` has **no** `"witch"`. Resolver fail-soft preserves `organismKey`. **Do not register.**

**Classification:** potion/raid owners **A**. Unregistered identity **B**. Illager column **rejected**.

---

## Required matrix

| Organism | Vanilla fact | Existing BioCraft composition | Existing consumer | C? | Why / why not |
|----------|--------------|-------------------------------|-------------------|----|----------------|
| **Creeper** | Fuse/swell/`explodeCreeper`; lightning sets `powered` flag; `PowerableMob` | `organismKey=creeper`; optional `contributingSourceKey=creeper`; `HostType.LIVING_BIOLOGICAL`; `hostEffectProfileId=baseline_biological` | LIVE eligibility + gestation writer + generic resolver. `creeper.json` PARSE-ONLY (no ability caller). ResolverTest TEST identity | **No** | Explosion is vanilla combat. Unused `infection_spread` is planned config. Identity already represented |
| **Ghast** | `FlyingMob` travel; `LargeFireball`; `fireImmune`; Nether biome lists | `organismKey=ghast`; `HostType.ELEMENTAL`; `hostEffectProfileId=elemental` | LIVE HostType suitability **false**. Generic resolver. AdmissionTest TEST fixture only | **No** | `FlyingMob` ≠ `canFly`. HostType never earns C. Shared fireball word with Blaze is not a shared cause |
| **Warden** | Vibration + anger + `SonicBoom`; shrieker `TRIGGERED` spawn; `fireImmune` | `organismKey=warden`; `HostType.INORGANIC`; `hostEffectProfileId=inorganic` | LIVE HostType suitability **false**. Generic resolver. `warden.json` DEAD (not bootstrapped). Inventory bio-organic not a runtime consumer | **No** | Sonic/sculk are vanilla. HostType/inventory labels independently owned. boss catalog PLANNING |
| **Witch** | Potion drink/throw; `Raider` not `AbstractIllager`; Villager lightning **replacement** (Villager-owned) | Fail-soft `organismKey=witch`; empty HostType optionals | LIVE fail-soft resolver. No hosts.json row. No gestation origin | **No** | Absence is participation evidence, not missing potion/illager fact. Do not register |

**New BP representation:** **None earned.**

---

## Shared findings (genuine only)

1. Existing composition covers every named live BioCraft consumer found (generic resolver; Creeper gestation identity; Ghast/Warden HostType suitability; Witch fail-soft key).
2. Distinctive combat-looking state (fuse, fireball, sonic boom, potions) fails the named-consumer gate.
3. Host Registry **presence** (Creeper/Ghast/Warden) is identity/routing **B**, not eligibility science and not a new field.
4. Host Registry **absence** (Witch) is not consumer absence of a missing fact; fail-soft identity is enough. Do not register.
5. Lightning is **not one biology**: Creeper mutates a flag; Villager replaces with Witch; Pig (prior batch) replaces with Zombified Piglin.

## Important differences

| Seam | Creeper | Ghast | Warden | Witch |
|------|---------|-------|--------|-------|
| Host Registry | `LIVING_BIOLOGICAL` suitable | `ELEMENTAL` unsuitable | `INORGANIC` unsuitable | Unregistered |
| Inventory category | bio-organic | bio-organic | bio-organic | bio-organic |
| Inventory vs HostType | Aligned `LIVING_BIOLOGICAL` | bio-organic ≠ `ELEMENTAL` | bio-organic ≠ `INORGANIC` | unregistered / — |
| Lightning | Same-entity `powered` flag | None organism-owned | None | Destination of Villager replacement (not Witch-owned) |
| Movement | Ground `Monster` | `FlyingMob` | Ground brain / dig pose | Ground `Raider` |
| Distinctive combat | Fuse explosion | `LargeFireball` | Sonic boom | Splash potions |
| Catalog JSON | `creeper.json` **LIVE load / PARSE-ONLY** | No ghast variant file | `warden.json` **DEAD** + boss **PLANNING** | None |
| Reproduction | Absent | Absent | Absent | Absent |

## Rejected abstractions (closed leaps)

- **Elemental column** from HostType `ELEMENTAL` or `hosts.json` ghast+blaze list.
- **Boss column** from `deep_mob_configs.boss` / `warden.json` path.
- **Illager column** from `Raider` / `#raiders` / Villager lightning.
- **Explosive / flight / sonic physiology** (`explosiveCapability`, `canFly`, sonic organ).
- Shared `PowerableMob` with Wither.
- Shared “fireball” with Blaze (`LargeFireball` vs `SmallFireball`).
- Happy Ghast absence as Ghast completion.
- Magma Cube Nether / Blaze hover as Ghast traits.
- Sculk encounter as Warden origin.
- Inventory vs HostType mismatch as a defect to fix in this pass.

## A/B/C summary

| Bucket | Result |
|--------|--------|
| **A** | Dominates vanilla owners on all four |
| **B** | Creeper live identity/contribution; Ghast/Warden identity + HostType routing; Witch fail-soft identity |
| **C** | **0** across the batch |

## New representation

**None.** No architectural escalation. Do not design fields.

## Recommended next branch (evidence dependency)

Do **not** queue: Happy Ghast from ordinary Ghast; Blaze reopen from elemental list; Guardian/Shulker from inorganic list; Evoker/Ravager reopen from Witch raid; Wither from `PowerableMob`; Flight Profile from `FlyingMob`.

This batch does **not** create a stronger dependency than remaining pending bio-organic rows.

**Next evidence-dependency candidate:** independent **Sheep** — wool color / dye / shear item-production among remaining pending bio-organic rows (already the authorized next from Panda/Parrot/Player and Pig/Strider/Ravager/Happy Ghast). Alternate remaining pending: Wolf (tame/anger), Rabbit (variant), Sniffer (dig), Polar Bear, Wandering Trader.

---

## UNKNOWN carried forward

- Creeper: whether any **future** xenomorph variant gameplay will read PARSE-ONLY `infection_spread` (today: no caller; still not a BP field).
- Warden: natural structure spawn JSON beyond shrieker/egg/summon was not required once triggered create was proven.
- Witch: swamp-hut structure piece JSON not separately extracted (biome monster lists + EntityType suffice for existence).

## Path

`.tmp_manifestation_evidence/creeper_ghast_warden_witch_synthesis.md`
