TEMPORARY EVIDENCE — NOT PROJECT SSOT
Skeptical synthesis — Pig / Strider / Ravager / Happy Ghast
Do not treat this file as canonical design documentation.
Do not mint DESIGN-BIO-MANIFEST-004. Phase 3 docs may promote conclusions only if no new BP representation is earned.

# Skeptical synthesis — Pig / Strider / Ravager / Happy Ghast

**Primary objective:** find why a new BP representation is **not** earned. Prefer disprove **C**.

**Version:** Minecraft Java **1.21.1** / NeoForge **21.1.208**.

**Packets:** [pig.md](./pig.md) · [strider.md](./strider.md) · [ravager.md](./ravager.md) · [happy_ghast.md](./happy_ghast.md)

This quartet is an **evidence-management / contrastive** batch, **not** a livestock / Nether / raid / mount / ghast clade. Ordinary `ghast` stays inventory-pending and is **not** promoted by Happy Ghast absence.

---

## Independent spot-checks (load-bearing)

### Pig lightning → Zombified Piglin

Re-opened `Pig.thunderHit` (`.tmp_mc_sources/.../Pig.java` **211–234**):

- Gate: non-PEACEFUL + NeoForge `canLivingConvert` to `ZOMBIFIED_PIGLIN`.
- Creates fresh `ZombifiedPiglin`; sets golden sword; copies pos/rot, `NoAi`, baby, custom name; `setPersistenceRequired`; `onLivingConvert`; `addFreshEntity`; **`this.discard()`**.
- No saddle/steering/passenger copy. No reverse path in Pig.
- Live BioCraft: no `thunderHit` / lightning-convert consumer of Pig→ZP. Gestation/Analyzer use host **identity** only if a living Pig is sampled **before** replacement.

**Classification:** entity/state transformation = **entity replacement rule**. **A**. Not ancestry. Not a BP field.

### Strider warm/cold

Re-opened `Strider` (`DATA_SUFFOCATING` **82**, save **127–129** steering only, `tick` warm check **315–327**, speed **273**):

- Warm env = feet/on-block `#strider_warm_blocks` **or** lava fluid height; forced cold if vehicle Strider is suffocating.
- `#strider_warm_blocks` JSON = **only** `minecraft:lava`.
- State is **synched, re-derived each tick, not NBT-persistent**. Distinct from `EntityType.fireImmune()` and lava-stand/path owners.
- Live BioCraft: **zero** `strider`/`Strider` under `biocraft-alien/src`. Thermal distinction unused.

**Classification:** transient gameplay state ← environmental interaction. **A**. Do not collapse fireImmune + lava walk + warm-state.

### Ravager roar / stun / attack / leaves

Re-opened `Ravager.java`:

- Stun: `blockedByShield` 50% → `stunnedTick=40` → on expiry arms `roarTick=20` → at 10 calls `roar()`.
- Roar: AoE 6 damage (skips `instanceof AbstractIllager`) + `strongKnockback`. Private method — not a shared Illager spell API.
- Attack: attributes + `MeleeAttackGoal` + `doHurtTarget`/`attackTick` event 4.
- Leaves: `aiStep` grief + `LeavesBlock` only.
- Tick fields NBT-saved but are **combat countdowns**, not genetics.
- Lifecycle/reproduction: **absent** (not AgeableMob; no breed/offspring/variant/transform).
- Live BioCraft: **zero** `ravager`/`Ravager` under `biocraft-alien/src`.

**Classification:** transient combat state / combat consequence / environmental interaction. **A**. No sonic organ.

### Happy Ghast version-gate

Re-confirmed: no `EntityType.HAPPY_GHAST` / `happy_ghast` / `HappyGhast` in 1.21.1 `EntityType` / sources. Ordinary `GHAST` exists and must not be conflated. Inventory §9.3 only. **Absence ≠ A**. **C not earned** (no organism to escalate).

---

## Consolidated A/B/C matrix

| Organism | Identity / Host | Distinctive stress | A | B | C | Escalation |
|----------|-----------------|--------------------|---|---|---|------------|
| **Pig** | Registered `LIVING_BIOLOGICAL` | Lightning → ZP replacement; breeding; saddle/`ItemSteerable` | Many vanilla rows | `organismKey=pig` + live `contributingSourceKey=pig` | **0** | **None** |
| **Strider** | Unregistered | Warm/cold vs fireImmune vs lava walk; breeding; stick steer | Many vanilla rows | Fail-soft `organismKey=strider`; registry gap ≠ missing fact | **0** | **None** |
| **Ravager** | Unregistered | Roar/stun/attack/leaves; raid infra; reproduction absence | Many vanilla rows | Fail-soft `organismKey=ravager`; registry gap ≠ missing fact | **0** | **None** |
| **Happy Ghast** | Absent in 1.21.1 | Version-gate only | N/A | N/A | **not earned** | **None** (version absence) |

**New BP representation:** **None earned.**

---

## Shared findings

1. Existing composition (`organismKey`, optional `contributingSourceKey`, sparse compiled fields) covers every named live BioCraft consumer found.
2. Host Registry participation on Pig is identity **B**, not eligibility science and not a new field.
3. Host Registry **absence** on Strider/Ravager is not consumer absence; live-tree search still found **no** organism-specific missing-fact consumer.
4. Interesting physiology-looking or combat-looking state (Strider cold skin; Ravager roar) fails the named-consumer gate.

## Important differences

| Seam | Pig | Strider | Ravager | Happy Ghast |
|------|-----|---------|---------|-------------|
| Transformation | Lightning discard+create → ZP | None organism-owned | None | N/A (absent) |
| Persistent biology-looking state | Saddle equipment NBT | Warm/cold **not** NBT | Combat ticks NBT but transient combat | N/A |
| Reproduction | Same-type Animal piglet | Same-type Animal + warped fungus | **Explicitly absent** | N/A |
| Registry | LIVE host | Absent | Absent | Absent (+ ordinary ghast separate) |

## Rejected abstractions (closed leaps)

- Shared `ItemSteerable` / saddle ≠ mount biology clade (Pig/Strider/Horse).
- Warped fungus item vs `#hoglin_repellents` block ≠ shared fungus trait.
- Nether spawn / lava walk / `fireImmune` / warm-state ≠ one intrinsic thermal trait.
- Pig name / lightning destination ≠ Hoglin/Piglin ancestry.
- `#raiders` / `extends Raider` / texture under `illager/` ≠ Illager clade; Ravager **not** in `#illager`.
- Roar/stun/knockback ≠ sonic/defensive anatomy field.
- Happy Ghast absence ≠ ordinary Ghast manifestation complete; absence ≠ A.
- Host Registry on Pig ≠ eligibility or new BP field.
- Host Registry absence ≠ proof of no live consumer (searched anyway).

## A/B/C summary

| Bucket | Result |
|--------|--------|
| **A** | Dominates all three full organisms (vanilla owners) |
| **B** | Pig live identity/contribution; Strider/Ravager fail-soft identity |
| **C** | **0** across the batch; Happy Ghast: C not earned via absence |

## Recommended next branch (evidence dependency)

Do **not** hard-restore prior “Strider next” (this pass closed Strider).

Do **not** queue: ordinary Ghast from Happy Ghast absence; Witch/Illusioner from Ravager/Raider adjacency; Hoglin/Piglin/ZP reopen from Pig lightning; Horse/Pig rideable clade from `ItemSteerable`.

**Next evidence-dependency candidate:** independent **Sheep** — wool color / dye / shear item-production stress test among remaining pending bio-organic rows (distinct from Pig lightning replacement and Mooshroom shear→Cow already closed). Alternate candidates from remaining pending inventory: Wolf (tame/anger), Rabbit (variant), Sniffer (dig), Panda (complex state). Ordinary **Ghast** remains later inventory, not authorized by this batch.

---

## UNKNOWN carried forward

- Pig: exact passenger teardown on `discard()` during lightning (not copied onto ZP).
- Strider: wiki-era shears unequip / golden dandelion / later tags not evidenced in 1.21.1 extract.
- Ravager: natural biome/structure spawn JSON not found under cached worldgen (raid/egg/summon proven).
- Happy Ghast: none beyond confirmed absence (later-version mechanics intentionally not researched).

## Path

`.tmp_manifestation_evidence/pig_strider_ravager_happy_ghast_synthesis.md`
