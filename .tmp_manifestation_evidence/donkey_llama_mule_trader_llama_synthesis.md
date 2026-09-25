TEMPORARY EVIDENCE — NOT PROJECT SSOT
Independent skeptical synthesis — Donkey / Llama / Mule / Trader Llama
Do not treat this file as project SSOT. Do not mint DESIGN-BIO-MANIFEST-004.

# Donkey / Llama / Mule / Trader Llama — skeptical synthesis

**Role:** Independent reviewer. Re-opened load-bearing mapped 1.21.1 sources and live BioCraft participation paths. Did **not** accept packet consensus without re-checks.

**Version:** Minecraft Java **1.21.1** / NeoForge 21.1.208 mapped cache under `.tmp_mc_sources/`.

**Architectural stress question (answered from ownership evidence):** Does a reproduction-derived entity distinction (Mule), a persistent phenotype/state (Llama variant/strength), or a contextually specialized entity (Trader Llama) become an actual biological input consumed by BioCraft?

**Answer:** No. BioCraft live consumers ask only for identity (`organismKey` / optional `contributingSourceKey`) where Host Registry participation exists. Variant, strength, mule factory transfer, spit, chest, and trader lifecycle remain Minecraft owners with **no** named missing-fact consumer.

---

## Re-verification anchors

| Claim | Re-check |
|-------|----------|
| Donkey identity | `EntityType.java`: `"donkey"`, CREATURE, **1.3964844×1.5**, eyeHeight **1.425** |
| Llama identity | `"llama"`, CREATURE, **0.9×1.87**, eyeHeight **1.7765** |
| Mule identity | `"mule"`, CREATURE, **1.3964844×1.6**, eyeHeight **1.52**, tracking **8** |
| Trader Llama identity | `"trader_llama"`, same outer size as Llama |
| Donkey class | `Donkey extends AbstractChestedHorse` |
| Llama class | `Llama extends AbstractChestedHorse implements VariantHolder, RangedAttackMob` |
| Mule class | `Mule extends AbstractChestedHorse` |
| TraderLlama class | `TraderLlama extends Llama`; `isTraderLlama()==true` |
| Donkey×Donkey / Donkey×Horse | `Donkey.getBreedOffspring`: other `Horse` → `EntityType.MULE`, else `DONKEY`; `setOffspringAttributes` |
| Horse×Donkey symmetry | `Horse.getBreedOffspring` creates `MULE` when other is Donkey |
| Mule sterility | `AbstractHorse.canMate` default **false**; Mule does not override |
| Mule factory transfer | `setOffspringAttributes` blends MAX_HEALTH / JUMP_STRENGTH / MOVEMENT_SPEED only |
| Llama variant | Synched + NBT `"Variant"`; herd spawn; breed 50/50 parent pick |
| Llama strength | Synched + NBT `"Strength"` 1–5; `getInventoryColumns()` = strength when chested |
| Llama spit | `Llama.spit` constructs `LlamaSpit`; wolf goal is AI targeting |
| Trader deltas | `DespawnDelay`, trader-leash sync, defend-trader goal, ride gate while trader-leashed, EVENT age 0, `makeNewLlama` → `TRADER_LLAMA` |
| hosts.json | `"donkey"`, `"mule"`, `"llama"` **PRESENT** in living_biological; `"trader_llama"` **ABSENT** |

---

## Consolidated matrix (refined classification column)

| Organism | Behavior | Owner | Classification | Result |
|----------|----------|-------|----------------|--------|
| Donkey | Identity + live host contribution | EntityType + hosts + gestation writer | identity / actual biological input (identity only) | **B** |
| Donkey | Chest / tame / saddle / ride / food | AbstractChestedHorse / AbstractHorse / tags | transient gameplay / item interaction | **A** |
| Donkey | Mate gate + offspring EntityType | Donkey/Horse breed factories | entity/state transformation | **A** (factory; **B** for resulting key identity) |
| Donkey | Attribute blend on foal | `setOffspringAttributes` | persistent entity state (vanilla attrs) | **A** |
| Llama | Identity + live host contribution | EntityType + hosts + gestation | identity | **B** |
| Llama | Variant | Llama NBT / renderer | persistent entity state (presentation) | **A** |
| Llama | Strength → chest columns | Llama NBT + inventory UI | persistent entity state / gameplay | **A** |
| Llama | Spit / wolf target / caravan / carpet | Llama / LlamaSpit / goals / equipment | combat / AI / equipment | **A** |
| Mule | Identity + live host contribution | EntityType + hosts + gestation | identity | **B** |
| Mule | Creation Horse↔Donkey | breed factories | entity/state transformation | **A** (distinct-key factory; not ancestry) |
| Mule | Surviving factory attrs | setOffspringAttributes | persistent entity state | **A** (BioCraft does not consume) |
| Mule | Sterility / no natural breed | AbstractHorse.canMate false | transient/negative gameplay | **A** |
| Mule | Chest vs Donkey | AbstractChestedHorse fixed 5 cols | gameplay state | **A** |
| TraderLlama | Distinct EntityType | EntityType.TRADER_LLAMA | identity | **B** fail-soft (no host route) |
| TraderLlama | Shared Llama biology | inheritance reuse | implementation ≠ ancestry | **A** |
| TraderLlama | Despawn / leash / defend / EVENT spawn | TraderLlama + WanderingTraderSpawner | environmental / lifecycle | **A** |
| TraderLlama | Host Registry | **ABSENT** | N/A | **B** fail-soft; do **not** register — absence ≠ automatic A/B alone; no other consumer requires distinction |

**C surviving?** **None.**

---

## Shared findings that survive skepticism

Verified before A/B labeling:

1. Four distinct EntityType keys with distinct (or trader-sized) registration literals.
2. Donkey×Donkey → Donkey; Donkey×Horse / Horse×Donkey → Mule via distinct-key factory + attribute blend only.
3. Mule does not naturally mate (`canMate` false); `getBreedOffspring` stub is unreachable via mate gate.
4. Llama variant is heritable presentation; strength is persisted NBT driving chest columns — neither consumed by BioCraft.
5. Spit owner is Llama → LlamaSpit projectile; wolf targeting is goal ownership.
6. `donkey` / `llama` / `mule` are Host Registry `LIVING_BIOLOGICAL` with live generic `contributingSourceKey` path; `trader_llama` has **no** Host Registry contribution and **no** other live BioCraft consumer that distinguishes it.
7. `TraderLlama extends Llama` is code reuse, not ancestry; trader deltas are lifecycle/encounter.

**Why A/B (established after findings):**
- Vanilla owners suffice for gameplay mechanics → **A**.
- Where BioCraft participates, existing `organismKey` / `contributingSourceKey` composition suffices → **B**.
- No named live consumer needs a missing biological fact → **C not earned**.

---

## Rejected abstractions (after ownership tracing)

| Abstraction | Why rejected |
|-------------|--------------|
| AbstractHorse / AbstractChestedHorse / pack-animal clade | Shared parent ≠ clade; distinct keys; Host Registry participation differs |
| Chest / carpet / strength as anatomy BP | Traced to inventory/equipment NBT; no BioCraft consumer |
| Spit / wolf hostility as biological input | Projectile + targeting goals |
| Mule sterility / hybrid origin as ancestry field | Factory + negative mate gate; no composition consumer of parentage |
| Shared HostType / hosts list = clade | Participation ≠ biology taxonomy |
| Register trader_llama because llama is registered | Host Registry edit out of scope; absence stays |
| Wandering-trader caravan as biological origin | Spawn/lifecycle adjacency only |
| Absorb Horse / Camel / Skeleton Horse / Zombie Horse / Wandering Trader | Explicit non-goals; no evidence dependency for Wandering Trader as next organism |
| Treat live contributingSourceKey as C | Identity already Model A |
| Host Registry absence as automatic B | Ruled out: B for trader_llama is fail-soft identity sufficiency after confirming no other consumer needs a distinction — not from absence alone |

---

## Consumer audit (skeptical)

| Candidate | Status | Survives as C? |
|-----------|--------|----------------|
| Generic resolver / Analyzer projecting organismKey | **LIVE** generic | No — **B** |
| Gestation contributingSourceKey for donkey/llama/mule | **LIVE** generic writer | No — **B** |
| Trader Llama host contribution | **ABSENT** | No — fail-soft **B**; do not register |
| Variant / strength / mule attrs / spit / chest | Vanilla only | No |
| Inventory / planning rows | **PLANNING** | No |

---

## New representation

**None earned.** No BP field. No architectural escalation. Documentation gate **authorized**.

**Forbidden:** Java, `hosts.json`, HostType/eligibility, BP architecture, Model A, vials, Analyzer, lifecycle, AI, rendering, BACKLOG/SPRINT, `DESIGN-BIO-MANIFEST-004`, registering `trader_llama`.

---

## Next branch (evidence dependency only)

This batch creates **no** biological evidence dependency on Wandering Trader, Horse reopen, or a mount clade.

**Recommended next:** independent **Strider** (available pending bio-organic candidate with no dependency chain from this batch). Do **not** auto-queue Wandering Trader from trader_llama lifecycle adjacency. Do **not** select next solely because inventory previously listed Strider — selection here is the absence of a new dependency plus Strider remaining an independent candidate among remaining pending bio-organics.

---

## UNKNOWN (Phase 1 / live tree)

| Item | Status |
|------|--------|
| Required entity/helper sources for mandatory probes | **Present** — no gate UNKNOWN |
| Sparse `baseline_biological` pack internals beyond host-effect id | **UNKNOWN** detail; does not invent C |
| Unshipped BioCraft branch consuming mule ancestry or llama strength | **UNKNOWN** beyond live tree |
| In-world playtest of gestation writing keys for these organisms | Code path LIVE generic; playtest not required for this docs gate |
| Post-1.21.1 changes | Out of range |
