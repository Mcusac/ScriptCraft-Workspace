```text
TEMPORARY EVIDENCE — NOT PROJECT SSOT
Skeptical synthesis of a docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
```

# Skeptical synthesis — Armadillo, Axolotl, Bat

**Status:** Temporary reviewer synthesis. **Not** project SSOT. **Not** DESIGN-BIO-MANIFEST-004.  
**Version gate:** Minecraft Java **1.21.1** (NeoForge 21.1.208 mapped sources).  
**Grouping:** Authorized **evidence-management batch** for remaining bio-organic baseline. Heterogeneous ordinary organisms. **Not** a clade, family, or HostType column. Does **not** finish Strider (leftover packet at `.tmp_manifestation_evidence/strider.md` left untouched).

**Independent re-check:** Packets treated as claims. Re-read `EntityType.ARMADILLO` / `AXOLOTL` / `BAT`, `Armadillo` / `ArmadilloAi`, `Axolotl` / `AxolotlAi` / `PlayDead` / `ValidatePlayDead` / `AxolotlAttackablesSensor`, `Bat` / `AmbientCreature` / `FlyingMob`, spawn placements, tags, loot, `hosts.json`, `MobBucketSpecimenSource`, SPRINT Bat identity notes.

**Primary objective:** find reasons a new Biological Profile representation is **not** earned.

**C is not earned for any organism in this group.**

**New BP field: NO.** Existing `organismKey` / optional `contributingSourceKey` remain sufficient for the bio-organic baseline test.

---

## Independent verification of tempting claims

| Tempting claim | Independent finding | Verdict |
|----------------|---------------------|---------|
| Shell / roll → armor or defensive-morphology trait | Synched `ArmadilloState`; `hurt` halves after −1 while scared; AI-owned | **Reject.** Entity state/combat (**A**) |
| Scute → stored biological property | Timer drop + brush → `Items.ARMADILLO_SCUTE`; empty death loot | **Reject.** Item production (**A**) |
| Unregistered armadillo must be registered | Fail-soft identity pattern | **Reject.** Do not register here |
| Aquatic movement → aquatic BP field | Amphibious nav + water `travel` + dry-out air | **Reject.** Entity locomotion (**A**) |
| Regeneration → regen trait | `PlayDead` applies `REGENERATION` to axolotl; `applySupportingEffects` buffs player | **Reject.** Mob effects (**A**); effect ≠ composition |
| Variant/color → biological subtype | `DATA_VARIANT` / NBT / bucket tag | **Reject.** Presentation/state (**A**) |
| Bucket admission proves variant/aquatic BP need | `MobBucketSpecimenSource` maps `AXOLOTL_BUCKET` → `EntityType.AXOLOTL` + payload bytes | **Reject C.** Admission/identity (**B**) |
| DnaAnalysisPort / Analyzer visibility → composition | Lab-report projection | **Reject.** Observability ≠ composition |
| Flight → flight trait / `canFly` / shared locomotion | Bat does **not** extend `FlyingMob`; no flying nav; custom deltas | **Reject.** Re-check confirms Bee/Phantom/Allay/Vex non-generalization |
| Ceiling attach → climbing | `isRedstoneConductor` on block above + `FLAG_RESTING` | **Reject.** Resting predicate (**A**) |
| SPRINT Bat identity → C | SPRINT fact: `contributingSourceKey` differs / displays | **Reject C.** Identity already (**B** / **PLAYTEST**) |
| This trio is a bio-organic clade | Different parents (`Animal` / `Animal+Bucketable` / `AmbientCreature`); categories CREATURE / AXOLOTLS / AMBIENT; Host Registry armadillo absent | **Reject grouping.** Administrative batch only |
| Auto-queue Tadpole/Frog, Ghast/Creeper, Donkey/Camel | Hunt tag / aerial / desert spawn adjacency only | **Reject auto-queue.** No concrete dependency changing current readings |

---

## Consolidated matrix

| Organism | Interesting behavior | Actual owner | Biological input | Composition sufficient? | Named consumer | Result |
|----------|---------------------|--------------|------------------|-------------------------|----------------|--------|
| Armadillo | Identity | `EntityType.ARMADILLO` | Identity | `organismKey=armadillo` fail-soft | Generic resolver | **B** |
| Armadillo | Roll/scare/damage/scute/breed | Entity + AI + items | No | Identity sufficient | None | **A** |
| Armadillo | Host Registry | **ABSENT** | Participation missing | Fail-soft | Origin blocked | **B** |
| Axolotl | Identity | `EntityType.AXOLOTL` | Identity | Registered key | Resolver / Analyzer | **B** |
| Axolotl | Aquatic / play-dead / regen / variant / hunt | Entity + AI + effects + tags | No | Identity sufficient | None for those facts | **A** |
| Axolotl | Bucket admission | `MobBucketSpecimenSource` | EntityType + NBT payload | Identity | **LIVE** admission | **B** |
| Axolotl | Host contribution | `hosts.json` + gestation | Identity | `contributingSourceKey=axolotl` | **LIVE** generic | **B** |
| Bat | Identity | `EntityType.BAT` | Identity | Registered key | Resolver / Analyzer | **B** |
| Bat | Flight / resting / spawn | Custom AmbientCreature AI | No | Identity sufficient | None for flight | **A** |
| Bat | Host contribution / SPRINT | hosts + gestation + playtest | Identity | `contributingSourceKey=bat` | **LIVE** + **PLAYTEST** | **B** |

---

## Consumer existence test (all C candidates)

Every tempting C failed the live-consumer gate: either no BioCraft consumer, or the consumer only needs identity already supplied by `organismKey` / `contributingSourceKey` / admission EntityType mapping.

---

## Bio-organic baseline result

**Existing composition remains sufficient.** Ordinary Minecraft biology in this heterogeneous trio does **not** expose a BP gap beyond identity. Baseline answer: `organismKey` / optional `contributingSourceKey` remain enough; no new field.

---

## Next organism group (evidence dependency)

**Independent Strider** remains next. A dangling temp packet already exists; this batch does not conclude Strider and must not absorb it. Do **not** queue Tadpole/Frog, Ghast, Creeper, Donkey/Camel from adjacency. Undead reassessment stays deferred. End/boss/flying comparisons remain deferred as separate later work (Bat is now investigated as ordinary bio-organic identity/flight owner, which still does not open those comparisons).

---

## Documentation gate

Result is **A/B and no C** → authorized to write canonical organism reports + comparison + inventory/dna.md/design README status notes only. No Java/`hosts.json`/BP/Model A/Feature/BACKLOG/SPRINT changes. Do not mint `DESIGN-BIO-MANIFEST-004`.
