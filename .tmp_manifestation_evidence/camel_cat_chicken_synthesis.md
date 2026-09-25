TEMPORARY EVIDENCE — NOT PROJECT SSOT
Independent skeptical synthesis — Camel / Cat / Chicken
Do not treat this file as project SSOT. Do not mint DESIGN-BIO-MANIFEST-004.

# Camel / Cat / Chicken — skeptical synthesis

**Role:** Independent reviewer. Re-opened load-bearing mapped 1.21.1 sources and live BioCraft participation paths. Did **not** accept packet consensus without re-checks.

**Version:** Minecraft Java **1.21.1** / NeoForge 21.1.208 mapped cache under `.tmp_mc_sources/`.

**External baseline:** Concurrent Armadillo / Axolotl / Bat artifacts became available by finish time (packets under `.tmp_manifestation_evidence/`, canonical `manifestations/armadillo.md` / `axolotl.md` / `bat.md`, comparison, and matching inventory/dna/README index cells). Mid-run synthesis initially lacked those completed reports and recorded comparison as unavailable then; final re-check confirms their independent A/B (no C) baseline. That does **not** change this group's independent A/B/C.

---

## Re-verification anchors

| Claim | Re-check |
|-------|----------|
| Camel identity | `EntityType.java` **236–238**: `"camel"`, CREATURE, **1.7×2.375**, eyeHeight **2.275** |
| Cat identity | **239–241**: `"cat"`, **0.6×0.7**, eyeHeight **0.35** |
| Chicken identity | **252–259**: `"chicken"`, **0.4×0.7**, eyeHeight **0.644** |
| Camel class | `Camel extends AbstractHorse implements PlayerRideableJumping, Saddleable` |
| Cat class | `Cat extends TamableAnimal implements VariantHolder<Holder<CatVariant>>` |
| Chicken class | `Chicken extends Animal` — **not** FlyingMob / FlyingAnimal |
| hosts.json | `"cat"` + `"chicken"` in living_biological **6**; `"camel"` **ABSENT**; `"ocelot"` **ABSENT** |
| Camel food | `#camel_food` → cactus only |
| Cat food | `#cat_food` → cod, salmon |
| Chicken food | `#chicken_food` → seed/pod set |
| Camel sit/dash | `LAST_POSE_CHANGE_TICK`, `DASH`, cooldown **55**, dual passengers |
| Cat variant/tame | `CatVariant` registry; `tryToTame` 1/3; structure all-black |
| Chicken fall/egg | Y×**0.6** when falling; `eggTime` → `Items.EGG` |

---

## Consolidated A/B/C matrix

| Organism | Behavior cluster | Owner | Result |
|----------|------------------|-------|--------|
| Camel | Identity | `EntityType.CAMEL` | **B** |
| Camel | Sit/stand, dash, dual ride, always-tamed, brain AI | `Camel` / `CamelAi` / `AbstractHorse` | **A** |
| Camel | Food/breed/spawn/loot/sounds | tags + EntityType + village pool | **A** |
| Camel | Host Registry | **ABSENT** | **B** fail-soft identity; do **not** register |
| Cat | Identity + live host contribution | `EntityType.CAT` + hosts + gestation path | **B** |
| Cat | Variant, tame, sit/lie/beg/avoid/hunt, gift, spawn | `Cat` / `TamableAnimal` / goals / loot / `CatSpawner` | **A** |
| Cat | Ocelot adjacency | Shared `OcelotAttackGoal` only | **A** — do not absorb |
| Chicken | Identity + live host contribution | `EntityType.CHICKEN` + hosts + gestation path | **B** |
| Chicken | Fall damping, egg timer, jockey, food/breed/loot | `Chicken` / tags / loot | **A** |
| Chicken | Flight abstraction | **Rejected** | **A** — not FlyingMob |

**C surviving?** **None.**

---

## Rejected abstractions (must stay closed)

| Abstraction | Why rejected |
|-------------|--------------|
| Flight Profile / `canFly` from Chicken | Fall damping only; Bee/Phantom/Allay precedents |
| Mountability / size / movement fields from Camel sit/dash/ride | Entity pose + ride API; no named missing-fact consumer |
| Variant / domestication / social / fear / sleep fields from Cat | Presentation + TamableAnimal + goals |
| Oviparity / reproductive-strategy from Chicken eggs | Item spawn timer, not entity birth |
| Clade: AbstractHorse / feline / livestock | Distinct EntityTypes; Host Registry participation differs |
| Absorb Donkey / Mule / Ocelot / camel_husk | Explicit non-goals; camel_husk has no 1.21.1 organism |
| Register Camel because Horse is registered | Host Registry edit out of scope; absence stays |
| Treat live `contributingSourceKey` as C | Identity already in Model A composition |

---

## Consumer audit (skeptical)

| Candidate | Status | Survives as C? |
|-----------|--------|----------------|
| Generic resolver / Analyzer projecting `organismKey` | **LIVE** generic | No — **B** |
| Gestation `contributingSourceKey` for cat/chicken | **LIVE** generic writer path (same as Cow/Horse); cat/chicken-named unit tests not required | No — **B** |
| Camel host contribution | **ABSENT** registration | No — fail-soft **B**; do not register |
| MovementFormFsm / vials / classification runtime | Out of scope / unused here | No |
| Inventory / planning rows | **PLANNING** | No |
| Sparse imported BP core sources | **UNKNOWN** where omitted from checkout | Does not invent C |

Identity consumers already served by `organismKey` / `contributingSourceKey` remain **B**, not **C**.

---

## Documentation gate

Synthesis finds **A/B only** for Camel, Cat, and Chicken. **No C survives.**

**Authorized:** write canonical `manifestations/camel.md`, `cat.md`, `chicken.md`, and `camel_cat_chicken_comparison.md`, plus inventory / dna.md / design README index cells only.

**Forbidden:** Java, `hosts.json`, HostType/eligibility, BP architecture, Model A, vials, Analyzer, lifecycle, AI, rendering, MovementFormFsm, classification runtime, Feature/BACKLOG/SPRINT IDs, ROADMAP, system.md, classification_investigation.md, `DESIGN-BIO-MANIFEST-004`.

---

## Next branch (evidence-dependent)

After this batch: remaining bio-organic work continues. Prefer independent **Armadillo** / **Axolotl** if concurrent chats deliver; otherwise previously authorized independent **Strider**. Do **not** queue Donkey, Mule, Ocelot, camel_husk, Mooshroom, Ghast, Creeper, or Bat from this group.
