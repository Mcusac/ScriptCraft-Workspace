TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent D docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/trader_llama.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Trader Llama — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register Trader Llama as a conclusion of this investigation.** Trader Llama is **ABSENT** from `hosts.json`. Host Registry absence is **not** itself evidence for **A** or **B**. Classification below rests on whether any **other** live BioCraft consumer requires a biological distinction beyond fail-soft identity.

Method (every behavior): owner → meaningful biological input? → existing composition? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps: `TraderLlama extends Llama` = implementation ≠ ancestry; Wandering-trader caravan spawn ≠ biological origin; encounter / leash / despawn role ≠ biological distinction; Host Registry absence ≠ automatic **A** or **B**; shared caravan AI / loot / size with Llama ≠ clade BP; inventory planning row ≠ live consumer.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey`, optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

**Default: NO new BP field.** Do **not** absorb Wandering Trader, Llama, Donkey, Horse, or Camel as required next organisms from this packet (Wandering Trader noted only as spawn/lifecycle adjacency).

---

## Subject

Trader Llama (`minecraft:trader_llama`) — distinct EntityType that **extends** `Llama`, differential state vs ordinary Llama (despawn, trader leash, defend-trader goal, ride gate, EVENT spawn age, default decor), Host Registry **ABSENCE**, and whether any live BioCraft consumer distinguishes it biologically from `llama`.

Out of scope as organisms: Wandering Trader (unless evidence dependency — none for biology), ordinary Llama (adjacency / differential control only), Horse / Donkey / Mule / Camel.

---

## Version

Minecraft Java **1.21.1** only. Mapped sources in `.tmp_mc_sources/` are authoritative. Wiki is orientation / disagreement discovery only; **source wins**.

### Phase 1 gate (confirmed)

| Artifact | Path | Status |
|----------|------|--------|
| `TraderLlama.java` | `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/TraderLlama.java` | **PRESENT** |
| `Llama.java` | `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/Llama.java` | **PRESENT** (differential) |
| `WanderingTraderSpawner.java` | `.tmp_mc_sources/net/minecraft/world/entity/npc/WanderingTraderSpawner.java` | **PRESENT** (caravan spawn) |
| `WanderingTrader.java` | `.tmp_mc_sources/net/minecraft/world/entity/npc/WanderingTrader.java` | **PRESENT** (DespawnDelay sync) |
| `LlamaFollowCaravanGoal.java` | `.tmp_mc_sources/net/minecraft/world/entity/ai/goal/LlamaFollowCaravanGoal.java` | **PRESENT** |
| Loot | `data/minecraft/loot_table/entities/trader_llama.json` | **PRESENT** (leather 0–2; same shape as `llama.json`) |
| BioCraft `hosts.json` | `biocraft-alien/src/main/resources/data/biocraft_alien/systems/hosts.json` | **ABSENT** `"trader_llama"`; **PRESENT** `"llama"` in `living_biological.mobs` |
| AlienCraft mention | inventory planning row only | **No** Java / hosts / production consumer named `trader_llama` |

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:trader_llama` |
| `EntityType` | `EntityType.TRADER_LLAMA` — `EntityType.java` **681–687**: `register("trader_llama", Builder.of(TraderLlama::new, MobCategory.CREATURE).sized(0.9F, 1.87F).eyeHeight(1.7765F).passengerAttachments(new Vec3(0.0, 1.37, -0.3)).clientTrackingRange(10))` |
| Ordinary Llama size | **Identical** numeric registration: `EntityType.LLAMA` **476–483** same size / eyeHeight / passengerAttachments / tracking |
| Fire / lava | Neither builder calls `.fireImmune()` |
| Class | `TraderLlama extends Llama` (`TraderLlama.java` **22**). `Llama extends AbstractChestedHorse` (`Llama.java` **65**) |
| Category | `MobCategory.CREATURE` |
| Attributes | `DefaultAttributes` maps `TRADER_LLAMA` → `Llama.createAttributes()` (**157**) — same supplier as Llama |
| Spawn placement | `TRADER_LLAMA`: `NO_RESTRICTIONS` + `Animal::checkAnimalSpawnRules` (`SpawnPlacements.java` **170**). `LLAMA`: `ON_GROUND` (**121**) — placement difference is spawn system, not body plan |
| Spawn egg | `Items.TRADER_LLAMA_SPAWN_EGG` (`Items.java` **1500–1501**) |
| Host Registry | **ABSENT.** `hosts.json` `living_biological.mobs` includes `"llama"` (**6–7**) and does **not** include `"trader_llama"`. No undead / unsuitable / modded / `variant_mappings` entry |
| Suitability | Unregistered → no live Host Registry contribution route for xenomorph hosting. **Do not register from this packet.** Absence ≠ automatic **A**/**B**; see consumers below |

Independent existence paths (not origin): `/summon` / spawn egg; `WanderingTraderSpawner.tryToSpawnLlamaFor` (`MobSpawnType.EVENT`, leash to trader); breeding when `makeNewLlama` runs on a TraderLlama parent → `EntityType.TRADER_LLAMA.create`.

---

## Mandatory differential: TraderLlama vs Llama

### Llama-owned biology / state (shared via inheritance — not TraderLlama deltas)

| Mechanic | Owner | Notes |
|----------|-------|-------|
| Coat variant (creamy/white/brown/gray) | `Llama` synched `DATA_VARIANT_ID` + `finalizeSpawn` | TraderLlama `finalizeSpawn` still calls `super` → same variant lottery |
| Strength / chest columns | `Llama` strength 1–5; inventory columns = strength if chested | Inherited |
| Spit / ranged attack / wolf target / hurt-by spit cutoff | `Llama` goals + `LlamaSpit` | Inherited; TraderLlama adds goals **after** `super.registerGoals()` |
| Carpet BODY “swag” / chest / food / breed / tempt / caravan join | `Llama` + `AbstractChestedHorse` + `LlamaFollowCaravanGoal` | Caravan goal accepts **both** `EntityType.LLAMA` and `TRADER_LLAMA` (**28**) |
| Sounds / not saddleable / fall damage rules | `Llama` | Inherited |
| Leather loot | Separate loot tables, **identical** pools | Drops ≠ anatomy distinction |

### Trader-lifecycle / ownership deltas (not biological origin)

| Delta | Owner | Evidence | Biological? |
|-------|-------|----------|-------------|
| Distinct registry id | `EntityType.TRADER_LLAMA` | Separate key from `llama` | Identity only |
| `isTraderLlama() == true` | `TraderLlama` override | `TraderLlama.java` **30–32**; base Llama returns **false** (**83–85**) | Flag for client decor / type query — not anatomy |
| Default trader decor texture | Client `LlamaDecorLayer` | If no carpet dye and `isTraderLlama()`, draw `textures/entity/llama/decor/trader_llama.png` (**63–67**) | Presentation / equipment fallback |
| `DespawnDelay` NBT + `maybeDespawn` | `TraderLlama` | Default **47999** (**23**); NBT (**41–55**); tick (**77–91**); if leashed to `WanderingTrader`, sync to trader’s delay − 1 | Trader-owned lifecycle |
| Despawn gates | `canDespawn` | Blocks despawn if tamed, leashed to non-trader, or has exactly one player passenger (**94–96**) | Persistent entity / leash state |
| Defend Wandering Trader | `TraderLlamaDefendWanderingTraderGoal` | Target trader’s last hurt-by while leashed (**120–154**) | Encounter / owner AI |
| Extra `PanicGoal(2.0)` | `TraderLlama.registerGoals` | Priority 1 after super (**58–61**); Llama already has Panic 1.2 at priority 3 | AI tuning |
| Ride blocked while trader-leashed | `doPlayerRide` | Empty body if leash holder is `WanderingTrader` (**69–74**) | Interaction / leash gate |
| EVENT spawn age 0 + group data | `finalizeSpawn` | `MobSpawnType.EVENT` → `setAge(0)`; null group → `AgeableMobGroupData(false)` then `super` (**108–117**) | Spawn/lifecycle |
| Caravan companion spawn | `WanderingTraderSpawner` | Up to **2** `TRADER_LLAMA` per trader, leashed (`tryToSpawnLlamaFor` **124–131**); trader delay **48000** (**113**) | Encounter placement ≠ origin |
| Offspring EntityType | `makeNewLlama` | TraderLlama → `TRADER_LLAMA.create` (**36–38**); Llama → `LLAMA.create` (**348–350**) | Reproduction **factory** (EntityType selection), same pattern as other horse-family factories |
| Mate eligibility | `Llama.canMate` | Any other `Llama` (includes TraderLlama) (**325–327**) | Vanilla breed gate; cross-type ≠ shared ancestry BP |

**Verdict of differential:** Trader Llama does **not** introduce a separate body plan, diet, attributes supplier, or loot anatomy. Deltas are **identity key** + **trader-owned lifecycle / leash / AI / presentation**. Inheritance from Llama is **implementation reuse**, not proof of shared BioCraft ancestry fields.

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing composition? | Named BioCraft consumer? | Refined manifestation classification | A/B/C |
|----------|--------------|-----------------|-------------------|----------------------|--------------------------|--------------------------------------|-------|
| Identity / CREATURE / size 0.9×1.87 | `EntityType.TRADER_LLAMA` | `EntityType.java` **681–687** (same dims as Llama) | Identity only | `organismKey = trader_llama` (fail-soft; unregistered) | Generic resolver / Analyzer identity path only — **no** trader_llama branch in Java | **identity** | **B** |
| `extends Llama` | class hierarchy | Implementation reuse | Shared parent ≠ ancestry BP | Distinct registry keys | None for clade | **implementation reuse** (not ancestry) | **A** |
| Variant / strength / spit / chest / carpet / food / breed goals | `Llama` (+ `AbstractChestedHorse`) | Inherited; trader `finalizeSpawn` → `super` | Llama biology/state shared | Distinct key already sufficient | None that splits trader vs llama anatomy | **persistent entity state** / **environmental interaction** / AI | **A** |
| Caravan follow | `LlamaFollowCaravanGoal` | Both EntityTypes eligible (**28**) | AI adjacency | Identity sufficient | None | **transient gameplay state** (AI) | **A** |
| `isTraderLlama` + default decor | Type flag + `LlamaDecorLayer` | **30–32**; decor **63–67** | No | Identity / presentation | None | **presentation** + type flag | **A** |
| DespawnDelay / discard | `TraderLlama.maybeDespawn` + optional sync to `WanderingTrader.getDespawnDelay` | **77–104**; trader NBT **165–178**, **228–233** | No — lifecycle | Not a longevity BP field | None | **persistent entity state** (timer) + **entity/state transformation** (discard) | **A** |
| Defend trader / panic priority | TraderLlama goals | **58–61**, **120–154** | No | Identity sufficient | None | **transient gameplay state** (AI) | **A** |
| Ride gate while trader-leashed | `doPlayerRide` | **69–74** | No | Identity sufficient | None | **transient gameplay state** (interaction) | **A** |
| Wandering-trader caravan spawn | `WanderingTraderSpawner` | **106–130** | **No.** Encounter ≠ origin | Not an origin field | None | **environmental interaction** (spawn) | **A** |
| Spawn placement `NO_RESTRICTIONS` | `SpawnPlacements` | **170** vs Llama `ON_GROUND` **121** | No | Identity sufficient | None | **environmental interaction** | **A** |
| Offspring `TRADER_LLAMA` factory | `makeNewLlama` | **36–38** | Reproduction/creation mechanic | Child key = `trader_llama` | None needing breed BP | **entity/state transformation** (creation) | **A/B** |
| Leather loot | `entities/trader_llama.json` | Same as llama leather 0–2 | Drops ≠ anatomy | Not needed | None | **item/block production** | **A** |
| Host Registry participation | `hosts.json` | `"llama"` present; `"trader_llama"` **ABSENT** | N/A — no contribution route | Fail-soft `organismKey` only | **No** production writer for trader_llama; inventory row is planning only | Host Registry **absence** (participation gap, not missing bio fact) | **B** (identity fail-soft — **not** because of absence alone) |

**No row is C.** No live BioCraft consumer distinguishes `trader_llama` from `llama` on biological facts.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"trader_llama"` | **ABSENT** | Not in living_biological / undead / unsuitable / modded / variant_mappings | Do **not** register. Absence ≠ automatic **A**/**B**; no other live consumer needs a bio distinction → identity remains fail-soft **B** |
| Adjacent `"llama"` | **LIVE** registered | `hosts.json` **6–7** | Distinct key. Registered Llama ≠ Trader Llama clade / do not absorb Llama investigation here |
| Java / config consumers named trader_llama | **ABSENT** | Grep under `implementations/minecraft/AlienCraft` (excl. inventory planning) | No named distinction consumer |
| Inventory row `trader_llama` | **PLANNING** | `vanilla_organism_inventory.md` **168**: unregistered, pending | Docs ≠ live consumer |
| TraderLlama entity JSON / BioCraft profile | **ABSENT** | No production config | Vanilla owns differentials |
| Wandering Trader | Not registered as dependency organism | Spawn/leash/despawn only | Do **not** queue Wandering Trader from this packet |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails |
|----------------|--------------|
| Trader Llama is a biological subspecies / needs Llama-diff BP fields | Differentials are despawn, leash, defend-trader, ride gate, decor, EVENT spawn — trader lifecycle, not body plan |
| `extends Llama` means same Host Registry / same organismKey | Distinct `EntityType`; Llama registered, trader_llama absent; shared parent ≠ clade |
| Caravan with Wandering Trader is biological origin | `WanderingTraderSpawner` encounter placement; spawn ≠ origin |
| Default trader carpet texture is anatomy | Client decor when `isTraderLlama()` and no dyed carpet |
| Host Registry absence earns **C** (must register) | Absence is participation gap. No named live consumer demands missing bio facts. Fail-soft identity is **B**. Do **not** register here |
| Absence earns automatic **B** | Ruled out by mission: classify from other consumers. Other consumers: **none** distinguish biologically → residual identity **B**, not “absence ⇒ B” |
| Must investigate Wandering Trader next | Only leash/despawn/spawn adjacency; no BioCraft bio-fact dependency |
| Breeding factory needs Model A field | EntityType selection only; no live consumer |

---

## Potential biological relationships

### 1. Identity without Host Registry

- **Owner:** `EntityType.TRADER_LLAMA` + fail-soft resolver path.
- **Biological input?** Registry key only.
- **Named consumer:** Generic Analyzer/resolver for unknown/unregistered keys (**LIVE** generic). No trader_llama-specific production writer.
- **Result:** **B**.

### 2. Llama-shared gameplay (variant, spit, chest, carpet, food, caravan)

- **Owner:** `Llama` / `AbstractChestedHorse` / goals.
- **Biological input?** No BioCraft composition required beyond optional identity.
- **Named consumer:** None distinguishing trader vs llama.
- **Result:** **A**.

### 3. Trader leash / despawn / defend / ride gate / EVENT spawn

- **Owner:** `TraderLlama` + `WanderingTrader` / `WanderingTraderSpawner`.
- **Biological input?** No.
- **Result:** **A**.

### 4. Adjacency to registered Llama

- Distinct keys. Shared Java parent and caravan eligibility only.
- Do **not** treat Host Registry presence of `llama` as evidence to register or merge `trader_llama`.
- **Result:** **A** (adjacency) / **B** (separate identity if consumed).

**C is not earned.**

---

## Wandering Trader evidence dependency

| Question | Answer |
|----------|--------|
| Does Trader Llama code reference Wandering Trader? | **Yes** — leash type checks, despawn sync, defend goal, ride gate; spawner creates leashed pairs |
| Is that a **biological** dependency requiring Wandering Trader as next organism? | **No** — merchant / caravan lifecycle ownership |
| Absorb Wandering Trader into this batch? | **No** |

---

## Wiki orientation disagreements

| Common orientation | 1.21.1 authority | Conclusion |
|--------------------|------------------|------------|
| Trader Llama is “just a Llama skin” | Distinct EntityType + lifecycle NBT/AI; same dims/attrs/loot | Identity + lifecycle, not mere skin; still no bio BP |
| Trader Llama is a subspecies needing DNA split from Llama | No attribute/loot/diet split; Host Registry has no trader consumer | Do not invent subspecies field |
| Caravan spawn is where they “come from” | `WanderingTraderSpawner` EVENT | Encounter ≠ origin |

---

## Final stop gate

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** (`organismKey=trader_llama` fail-soft) |
| Named missing-fact consumer | **NO** |
| Live BioCraft consumer distinguishes trader_llama vs llama? | **NO** |
| Register Trader Llama? | **NO** — out of scope; absence stays |
| Host Registry absence used as automatic A/B? | **NO** — classified from lack of other distinguishing consumers + identity key |
| Architectural escalation | **NO** |
| Queue Wandering Trader? | **NO** |

---

## Final conclusion

Trader Llama is a **distinct creature EntityType** that reuses Llama implementation for shared mount/pack/spit/variant gameplay while layering **trader-owned** despawn, leash, defend, ride, and caravan-spawn lifecycle. Host Registry has **no** `trader_llama` contribution route (adjacent `llama` is registered). That absence is **not** scored as automatic **A** or **B**; independently, **no** live BioCraft consumer requires a biological distinction between the two. Overall: vanilla deltas **A**, identity **B**, **C** not earned. Do not register. Do not absorb Wandering Trader.

**Overall A/B/C: B** (with pervasive **A** ownership of trader-lifecycle and shared Llama mechanics; **C** not earned).

---

## UNKNOWN list

| Item | Why UNKNOWN |
|------|-------------|
| Sparse Biological Profile core contents for unregistered keys | Generic fail-soft path assumed from prior packets; trader_llama-specific BP JSON **ABSENT** — not probed as a design surface |
| Whether a future Host Registry registration of `trader_llama` would mirror `llama` HostType/`default_dna` | Out of scope; do not register |
| Client model layer bake differences beyond decor texture | `ModelLayers.TRADER_LLAMA` exists; full mesh parity with Llama not line-audited (presentation only) |
| Exact playtest behavior when cross-breeding Llama × TraderLlama under player control | Source factory rules clear (`makeNewLlama` on calling parent); live playtest not run |
