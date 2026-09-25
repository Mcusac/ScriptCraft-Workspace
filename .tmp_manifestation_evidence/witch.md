TEMPORARY EVIDENCE — NOT PROJECT SSOT

Do not treat this file as canonical design documentation.
Do not promote into manifestations/witch.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004 without the authorized Phase 3 pass.
Do **not** register Witch as a conclusion of this investigation.

# Witch — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

Method (every behavior): owner → biological input? → `organismKey` / `contributingSourceKey` enough? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied independently: **unregistered ≠ no biology**; absence is **participation evidence**; fail-soft `organismKey` only; **do not register**; Villager lightning→Witch is **entity replacement** (Villager report locked — do not reopen as C); `Witch extends Raider` **not** `AbstractIllager`; `#raiders` membership ≠ `#illager` clade; Illager/Raider infrastructure ≠ Witch clade; Evoker/Pillager/Vindicator/Ravager adjacency does not absorb Witch.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey`, optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

**Default: NO new BP field.** Villager / Evoker / Pillager / Vindicator / Ravager / Creeper / Ghast / Warden are **not absorbed**.

---

## Subject

Witch (`minecraft:witch`) — living Witch identity on Minecraft Java **1.21.1**. Scope: EntityType; `Witch extends Raider implements RangedAttackMob`; potion drink/throw; raid membership; Host Registry **absence**; Villager lightning replacement as **creation path only** (Villager-owned).

Out of scope as organisms: Villager (locked), Evoker, Pillager, Vindicator, Ravager, Illusioner.

---

## Version

Minecraft Java **1.21.1** only. Mapped sources in `.tmp_mc_sources/` are authoritative. Wiki is orientation / disagreement discovery only; **source wins**.

---

## Phase 1 gate

| Required probe | Status |
|----------------|--------|
| `.tmp_mc_sources/.../monster/Witch.java` | **Present** (286 lines) |
| `Raider.java` / `AbstractIllager.java` / `NearestAttackableWitchTargetGoal.java` | **Present** |
| `Villager.thunderHit` (replacement owner; not Witch-owned) | **Present** |
| Related loot / tags | **Present** (`loot_table/entities/witch.json`; `#raiders`; `#illager`; `#witch_resistant_to`) |
| BioCraft `hosts.json` | **Present** — **no** `"witch"` key |

Gate **PASS** — proceed (not UNKNOWN).

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:witch` |
| `EntityType` | `EntityType.WITCH` — `EntityType.java` **733–736**: `register("witch", Builder.of(Witch::new, MobCategory.MONSTER).sized(0.6F, 1.95F).eyeHeight(1.62F).passengerAttachments(2.2625F).clientTrackingRange(8))` |
| Fire / lava | WITCH builder does **not** call `.fireImmune()` |
| Class | `Witch extends Raider implements RangedAttackMob` (`Witch.java` **44**). Does **not** extend `AbstractIllager` |
| Category | `MobCategory.MONSTER` |
| Dimensions | **0.6 × 1.95**, eyeHeight **1.62**, tracking **8** |
| Default attributes | `DefaultAttributes.java` **165**: max health **26.0**, movement **0.25** (`Witch.java` **107–109**) |
| Spawn placement | `SpawnPlacements.java` **148**: `ON_GROUND`, `Monster::checkMonsterSpawnRules` |
| Host Registry | **UNREGISTERED.** `hosts.json` has no `"witch"`. `MobHostRegistry.getHostType("witch")` → **null**. `isSuitableForXenomorph("witch")` → **false** (`MobHostRegistry.java` **46–48**, **68–71**) |
| Inventory baseline | bio-organic, unregistered, pending (this packet does not edit inventory) |
| Suitability | Unregistered → not suitable. **Unregistered ≠ ineligible-as-biology ≠ BP field** |

`#minecraft:raiders` **includes** witch. `#minecraft:illager` = evoker, illusioner, pillager, vindicator — **no witch**. `#illager_friends` = `#illager` only.

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing composition? | Named BioCraft consumer? | Refined manifestation classification | A/B/C |
|----------|--------------|-----------------|-------------------|----------------------|--------------------------|--------------------------------------|-------|
| Identity / size / category | `EntityType.WITCH` | `EntityType.java` **733–736** | Identity only | Fail-soft `organismKey = witch` | Generic resolver (empty HostType optionals) | **identity** | **B** |
| `extends Raider` | Class hierarchy | `Witch.java` **44**. Shared parent with Evoker/Pillager/Vindicator/Ravager | Shared parent ≠ Illager clade (Witch is **not** `AbstractIllager`) | Distinct key | None | **identity** (type hierarchy ≠ biology) | **A/B** |
| Raid join / celebrate / banner goals | `Raider.registerGoals` | Super goals (`Witch.java` **60**; `Raider.java` **57–63**) | Raid infrastructure | Identity sufficient | None | **transient gameplay state** / raid | **A** |
| `applyRaidBuffs` | Witch override | **Empty** (`Witch.java` **278–280**) | No wave buffs | Identity sufficient | None | **absent raid buff** | **A** |
| `canBeLeader` | Witch override | **false** (`Witch.java` **283–285**) | Raid role gate | Identity sufficient | None | **transient gameplay state** | **A** |
| Drink potions | `aiStep` | Water breathing / fire resistance / healing / swiftness into MAINHAND; drinking slow modifier (`Witch.java` **111–173**) | Item + effects. Not a potion-organ | Identity sufficient | None | **transient gameplay state** / effects | **A** |
| Throw splash potions | `performRangedAttack` | Harming / healing-or-regen (if target Raider) / slowness / poison / weakness (`Witch.java` **232–275`) | Projectile items | Identity sufficient | None | **combat** | **A** |
| `#witch_resistant_to` | Damage tag + absorb | magic, indirect_magic, sonic_boom, thorns → ×0.15 (`Witch.java` **215–225**; tag JSON) | Combat reduction | Identity sufficient | None | **combat** | **A** |
| Heal other raiders | `NearestHealableRaiderTargetGoal` | Targets Raider ≠ WITCH while raid active (`Witch.java` **61–63**) | AI. Shared raid ≠ clade | Identity sufficient | None | **transient gameplay state** / AI | **A** |
| Overworld spawn | Biome monster lists | Many biomes list witch (same files as creeper in cached worldgen) | Encounter ≠ origin | Not an origin field | None | **environmental interaction** | **A** |
| Loot | Vanilla loot table | glowstone_dust, sugar, spider_eye, glass_bottle, gunpowder, stick, redstone | Drops ≠ brewing anatomy | Not needed | None | **item/block production** | **A** |
| Villager lightning → Witch | **`Villager.thunderHit`** | Create `EntityType.WITCH`, copy pos/rot/NoAi/name, persistence, `onLivingConvert`, `discard` villager (`Villager.java` **820–837**) | **Entity replacement.** Villager-owned. Locked: not ancestry | Child is `witch` key | **None** in BioCraft for lightning convert | **entity/state transformation** (replacement) | **A** |
| Reverse Witch → Villager | **ABSENT** | No Witch `thunderHit` override | No reverse path | Not a convert field | None | — | **A** |
| Host Registry | **ABSENT** | No `"witch"` in `hosts.json` | Participation **gap**, not missing biology | Fail-soft key | Resolver preserves key, empty optionals (`BiologicalProfileResolver.java` **41–56**; unknown-key test pattern) | **identity** (unregistered) | **B** |
| Gestation / facehugger | Unregistered → unsuitable | `getHostType` null → not suitable | No live contribution write | Fail-soft identity still sufficient | None missing | **identity** (non-participation) | **B** |

**No row is C.** Unregistered is **B** fail-soft, not C, and **not** a reason to register.

---

## Villager lightning probe (creation only — Villager locked)

| Probe | Outcome |
|-------|---------|
| Owner | `Villager.thunderHit` — **not** Witch |
| Gate | Non-PEACEFUL + NeoForge `canLivingConvert` to `WITCH` |
| Mechanism | `EntityType.WITCH.create` → copy pose/NoAi/name → `finalizeSpawn(CONVERSION)` → persist → `onLivingConvert` → add entity → villager `releaseAllPois` + `discard` |
| Transferred | Position, rotation, NoAi, custom name. **Not** profession, trades, gossip, inventory, villager data |
| BioCraft | No lightning-convert consumer. If a Villager is sampled **before** replacement, contribution is `villager`. After replacement the living entity is `witch` (unregistered) |
| Classification | Entity replacement = **A**. Not ancestry. Do not queue Witch from Villager; this packet investigates Witch **after** existence |

Independent Witch existence: biome spawn, spawn egg, `/summon`. Lightning is **one** factory, not origin biology.

---

## Illager / Raider anti-clade (mandatory)

```text
Witch extends Raider implements RangedAttackMob
        ≠
AbstractIllager
        ≠
#illager tag membership
        ≠
Illager biological clade
```

| Check | Witch |
|-------|-------|
| `AbstractIllager` | **No** |
| `#illager` | **No** |
| `#raiders` | **Yes** (with evoker, pillager, ravager, vindicator, illusioner) |
| `Raider` goals / raid join | **Yes** |
| Tag `#raiders` / `extends Raider` | Raid infrastructure, **not** a clade (Ravager already closed this leap independently) |

Do **not** register Witch to “complete” an illager column.

---

## AlienCraft configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"witch"` | **ABSENT** | Not in living_biological / undead / unsuitable groups | Participation gap. **Do not register** from this packet |
| Resolver `organismKey=witch` | **LIVE** fail-soft | Unknown/unregistered keys preserve key, empty optionals | Soft identity **B** |
| Witch xenomorph JSON | **ABSENT** | No witch variant under `entity/xenomorph` | Vanilla remains owner |
| `bootstrap_entries` | **ABSENT** witch | Not loaded | Not a missing BP field |
| Gestation writer | **N/A / blocked** | Unregistered → not a valid facehugger host | Absence ≠ missing potion fact |
| Witch-named Analyzer / potion / raid branch | **ABSENT** | No production Java | Vanilla remains owner |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails on 1.21.1 evidence |
|----------------|--------------------------------|
| Unregistered ⇒ no biology / skip investigation | Absence is participation evidence. Fail-soft key is **B** |
| Register Witch because bio-organic / interesting potions | Do **not** register. Registration is not this packet’s job |
| Villager lightning ⇒ Witch ancestry / profession remnant | Replacement; profession not copied. Villager locked |
| `extends Raider` / `#raiders` ⇒ Illager clade | Not `AbstractIllager`; not in `#illager` |
| Potion drink/throw ⇒ brewing / magic organ | Item + effect AI |
| `#witch_resistant_to` includes `sonic_boom` ⇒ Warden relationship | Damage tag list, not a clade |
| Queue from Evoker/Ravager adjacency | Closed: not an illager column |

---

## Potential biological relationships (hypotheses only — after ownership)

### 1. Unregistered identity (fail-soft)

- **Owner:** resolver fail-soft + Host Registry absence.
- **Biological input?** Key string only if something asks.
- **Named consumer?** Generic resolver. No missing-fact consumer.
- **Result:** **B**. **Do not register.**

### 2. Villager → Witch lightning replacement

- **Owner:** `Villager.thunderHit`.
- **Result:** **A**. Distinct-key replacement. Not C.

### 3. Raid / Illager kinship

- **Owner:** `Raider` + tags.
- **Result:** **A**. Reject illager column.

### 4. Potion combat as biology

- **Owner:** `Witch.aiStep` / `performRangedAttack`.
- **Named consumer?** None.
- **Result:** **A**.

**C is not earned for any relationship.**

---

## Wiki disagreements

| Orientation claim | 1.21.1 authority | Conclusion |
|-------------------|------------------|------------|
| Witch is an Illager | Not `AbstractIllager`; not `#illager`; is `#raiders` | **Raider, not Illager type** |
| Lightning cursed villager keeps profession | Create fresh Witch; villager discarded | **Replacement** |
| Unregistered means BioCraft has no Witch identity | Fail-soft `organismKey` | **B**, not “no organism” |

---

## Final evidence conclusion

| Gate | Result |
|------|--------|
| New BP field | **No** |
| Existing composition sufficient | **Yes** — fail-soft `organismKey=witch` |
| Named consumer of a missing fact | **None** |
| Architectural escalation | **None** |
| Host Registry action | **Do not register** |

**A + B (fail-soft); C not earned.**
