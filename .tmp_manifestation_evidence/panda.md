TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Panda docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/panda.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004 until synthesis.

**Isolation:** Minecraft Java **1.21.1** / NeoForge **21.1.208** mapped sources under `.tmp_mc_sources/`, live BioCraft under `biocraft-alien/src`, and this packet’s own reads only. Parrot / Player packets were **not** absorbed as evidence.

Method: owner → biological input? → existing composition? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact |

Working hypothesis: prefer disprove **C**. Soft warning: do **not** equate Minecraft panda genes with a BioCraft Biological Profile genetics representation without persistence + inheritance + manifestation + a named consumer requiring that distinction.

---

## 1. Subject / Version / Target identity

### Subject

Panda (`minecraft:panda`) — main/hidden gene storage, personality expression, breeding inheritance, bamboo food/tempt/breed/env, Host Registry participation.

### Version

Minecraft Java **1.21.1** / NeoForge **21.1.208** mapped sources under `.tmp_mc_sources/` (extracted from `biocraft-alien/build/moddev/artifacts/neoforge-21.1.208-sources.jar` and `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar`). Wiki = orientation only; **source wins**.

### Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:panda` |
| `EntityType` | `EntityType.PANDA` — `EntityType.java` **517–518**: `register("panda", Builder.of(Panda::new, MobCategory.CREATURE).sized(1.3F, 1.25F).clientTrackingRange(10))` |
| Class | `Panda extends Animal` (`Panda.java` **74**) |
| Category | `MobCategory.CREATURE` |
| Baby dims | `BABY_DIMENSIONS` = PANDA dims ×0.5, passenger attach **0.40625F** (**82–85**) |
| Attributes | `createAttributes`: MOVEMENT_SPEED **0.15F**, ATTACK_DAMAGE **6.0** (**291–292**). Weak personality overrides MAX_HEALTH to **10**; Lazy overrides MOVEMENT_SPEED to **0.07F** (`setAttributes` **623–630**) |
| Leash | `canBeLeashed()` → **false** (**325–327**) |
| Host Registry | **REGISTERED** `vanilla_hosts.living_biological`; HostType `LIVING_BIOLOGICAL`; `default_dna: baseline_biological` |

---

## 2. Source-completeness table

| Source path | Status | Role |
|-------------|--------|------|
| `.tmp_mc_sources/net/minecraft/world/entity/animal/Panda.java` | **PRESENT** | Genes, personality, breed, bamboo, goals |
| `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` | **PRESENT** | PANDA registration |
| `.tmp_mc_sources/net/minecraft/world/entity/animal/Animal.java` | **PRESENT** | Breed/love base |
| `.tmp_mc_sources/net/minecraft/world/entity/ai/goal/TemptGoal.java` | **PRESENT** | Bamboo tempt |
| `.tmp_mc_sources/net/minecraft/client/renderer/entity/PandaRenderer.java` | **PRESENT** | Personality textures |
| `.tmp_mc_sources/data/minecraft/tags/item/panda_food.json` | **PRESENT** | `#panda_food` = bamboo only |
| `.tmp_mc_sources/data/minecraft/loot_table/entities/panda.json` | **PRESENT** | Death drops bamboo |
| `.tmp_mc_sources/data/minecraft/loot_table/gameplay/panda_sneeze.json` | **PRESENT** | Gift slime ball (weight 1 vs empty 699) |
| `.tmp_mc_sources/data/minecraft/worldgen/biome/jungle.json` | **PRESENT** | Encounter spawn (weight 1) |
| `.tmp_mc_sources/data/minecraft/worldgen/biome/bamboo_jungle.json` | **PRESENT** | Encounter spawn (weight 80) |
| AlienCraft `hosts.json` | **PRESENT** | `"panda"` living_biological |
| AlienCraft `GestationManager.writeContributingSource` | **PRESENT** | Identity key writer |
| BioCraft production code reading `MainGene` / `HiddenGene` / `Panda.Gene` | **ABSENT** | No gene/personality consumer |

Worldgen biome scan of the 1.21.1 resources jar: panda spawners appear in **jungle** and **bamboo_jungle** only (this pass). Spawn biome ≠ origin.

---

## 3. Panda gene probe (mandatory)

Separate layers: **internal genetic state** → **persistent phenotype/personality** → **behavioral expression** → **inheritance** → **gameplay consequence** → **BioCraft consumption**.

| # | Question | Evidence | Classification |
|---|----------|----------|----------------|
| 1 | Storage | Synched `MAIN_GENE_ID` / `HIDDEN_GENE_ID` bytes (`Panda.java` **78–79**, **219–220**). Accessors `getMainGene`/`setMainGene`/`getHiddenGene`/`setHiddenGene` (**182–203**). Ids `> 6` re-roll via `Gene.getRandom`. | persistent entity state |
| 2 | Values | `Gene`: NORMAL, LAZY, WORRIED, PLAYFUL, BROWN, WEAK, AGGRESSIVE (**730–737**). BROWN and WEAK `isRecessive=true`. | persistent entity state |
| 3 | Initial assignment | `finalizeSpawn` → `Gene.getRandom` independently for main and hidden (**581–584**), then `setAttributes()`. `getRandom` uses `nextInt(16)`: 0 LAZY, 1 WORRIED, 2 PLAYFUL, 4 AGGRESSIVE, `<9` WEAK, `<11` BROWN, else NORMAL (**781–795**). | persistent entity state |
| 4 | Persistence | NBT `"MainGene"` / `"HiddenGene"` serialized names (**241–252**). Sit/sneeze/roll/on-back flags are synched (`DATA_ID_FLAGS`) but **not** written in Panda NBT — transient. | persistent entity state (genes only) |
| 5 | Mutable after creation | `setMainGene`/`setHiddenGene` are public. No in-class environment/thunder continuous re-roll found. Breeding and NBT/commands can change values. | persistent entity state |
| 6 | Personality expression | `getVariant()` = `Gene.getVariantFromGenes(main, hidden)` (**295–297**, **765–770**): if main is recessive, both alleles must match else NORMAL; else expressed = main. | persistent entity state (derived phenotype) |
| 7 | Behavior by personality | Lazy: speed **0.07F**; sit/lie goals gated on `isLazy`. Weak: MAX_HEALTH **10**; baby sneeze more frequent (`PandaSneezeGoal` **1151–1154**: weak 1/500 vs other babies 1/6000). Worried: thunder scare (`isScared` **400**); `PandaAvoidGoal` vs Player/Monster. Playful: `PandaRollGoal` onGround. Aggressive: melee/target; aggressive ambient. BROWN: texture via `PandaRenderer` (no extra AI branch found in `Panda.java`). | transient gameplay / environmental interaction / presentation |
| 8 | Breeding | `getBreedOffspring` → `EntityType.PANDA.create` + `setGeneFromParents` if partner is Panda (**257–267**). | entity/state transformation (offspring) |
| 9 | Parent contribution | Each slot: random parent’s `getOneOfGenesRandomly()` (main **or** hidden of that parent) (**593–620**). If mother null: one slot from father, other `getRandom`. | persistent entity state (offspring genes) |
| 10 | Determinism | Random: parent-slot coin flip; each slot 1/32 chance replaced by `Gene.getRandom` (**610–616**). Not deterministic copy of a single parent personality. | — |
| 11 | Offspring state | Offspring receives **gene alleles**, not a copied personality enum. Personality is re-derived via `getVariantFromGenes` after `setAttributes()`. Child EntityType remains `PANDA`. | entity/state transformation |
| 12 | BioCraft gene consume | **None.** `rg` under `biocraft-alien/src` for panda/parrot hits **hosts.json only**. No production read of `MainGene`/`HiddenGene`/`Panda.Gene`. | — |
| 13 | Identity key | `organismKey` / `contributingSourceKey` via `encodeId` → `HostRegistryPaths.registryPath` → `"panda"` if sampled/gestated. | actual biological input consumed by BioCraft (identity only) |
| 14 | Consumer needing panda-vs-panda composition | **None.** Analyzer/resolver/gestation consume the registry path, not gene/personality. | — |

**Soft warning applied:** vanilla persistence + weighted random assignment + inheritance + visible/AI manifestation exist. That does **not** mint a BioCraft Genome/trait field without a named consumer requiring the distinction. Result for genes/personality: **A**. Identity contribution if gestated/sampled: **B**.

---

## 4. Bamboo probe (mandatory)

Trace food / temptation / breeding / environmental-item separately. Consumed material ≠ biological composition without a live BioCraft consumer of that distinction.

| Layer | Owner | Classification | BioCraft |
|-------|-------|----------------|----------|
| Food / breed item | `isFood` → `#panda_food` (`panda_food.json` = `minecraft:bamboo` only) (**701–702**) | environmental interaction / item | None |
| Tempt | `TemptGoal` on `ItemTags.PANDA_FOOD` (**276**) | environmental interaction | None |
| Pickup | Item entities: bamboo **or** cake (`PANDA_ITEMS` **104–107**) | environmental interaction | None |
| Eat / cake | Cake is pickup/eat, **not** `isFood` / breed. `isFoodOrCake` (**705–706**) | transient gameplay state | None |
| Hand-feed | `mobInteract`: baby age-up; adult love if `canFallInLove`; else sit+eat (**642–676**) | environmental + Animal breed | None |
| Env bamboo blocks | Sit/scan goals inspect `Blocks.BAMBOO` (e.g. **865**) | environmental interaction | None |
| Death loot | `loot_table/entities/panda.json` — 1 bamboo | item/block production | None |
| Sneeze gift | `BuiltInLootTables.PANDA_SNEEZE` → slime ball 1/700 (**538–548**, `panda_sneeze.json`) | item/block production | None |

Rejected: “Panda consumes bamboo → bamboo is biological composition”; “bamboo required for breeding → plant-derived reproductive trait.”

---

## 5. Behavior ownership table

| Behavior | Actual owner | Classification | Biological input? | Existing composition | Named BioCraft consumer | Result |
|----------|--------------|----------------|-------------------|----------------------|-------------------------|--------|
| Identity | `EntityType.PANDA` | identity | Identity | `organismKey=panda` | LIVE host/gestation/resolver (generic encodeId) | **B** |
| Main/hidden genes | Panda synched + NBT | persistent entity state | Vanilla personality owner | Identity covers organism | **None** for gene values | **A** |
| Personality expression | `getVariantFromGenes` + goals/attrs + `PandaRenderer` textures | persistent phenotype + transient AI + presentation | No BP gene fact | Identity sufficient | None | **A** |
| Sit/sneeze/roll flags | `DATA_ID_FLAGS` (not in Panda NBT) | transient gameplay state | No | Identity sufficient | None | **A** |
| Breeding inheritance | `setGeneFromParents` | entity/state transformation | Offspring still `panda` | Child identity | None | **A** (+ identity **B** if sampled) |
| Bamboo food/tempt/breed/env | Tags + goals + blocks | environmental / item | No | Identity sufficient | None | **A** |
| Sneeze slime ball | gift loot table | item/block production | No | Identity sufficient | None | **A** |
| Jungle/bamboo_jungle spawn | biome spawners | environmental interaction | Encounter ≠ origin | Not origin field | None | **A** |
| Host contribution | `hosts.json` + `GestationManager.writeContributingSource` | actual biological input (key) | Identity only | key + `baseline_biological` | **LIVE** generic writer | **B** |

No row is **C**. Registration alone is not B; live `encodeId` → `registryPath("panda")` on the generic gestation/Analyzer path proves identity **B**.

---

## 6. Configuration audit

| Finding | Status | Interpretation |
|---------|--------|----------------|
| `hosts.json` `"panda"` | **LIVE** | Participation; `LIVING_BIOLOGICAL`; `isSuitableForXenomorph()==true` |
| Gene/personality fields in BioCraft | **ABSENT** | Do not invent |
| `variant_mappings` panda | **ABSENT** | No aggressive/neutral override |
| Resolver / Analyzer / gestation | **LIVE** generic | Identity only |
| Panda-named Java/tests | **ABSENT** | hosts.json list membership only |

---

## 7. Tempting but rejected

- Minecraft genes → BioCraft genetics / Genome / Trait registry
- Jungle spawn adjacency with parrot → clade
- Personality → automatic trait-registry membership
- Bamboo consumption → plant-derived reproductive trait
- Host Registry registration as manifestation science
- Polar bear adjacency from bamboo/bear name

---

## 8. Potential biological relationships

None earned for BioCraft composition. Adjacent `polar_bear` is **not** queued from this packet.

---

## 9. Final evidence conclusion

| Question | Answer |
|----------|--------|
| New BP field? | **No** |
| Existing composition? | **Yes** — `organismKey` / `contributingSourceKey=panda` |
| Named consumer missing fact? | **No** |
| Escalation C? | **No** — **A + B** |

Gene/personality/bamboo remain vanilla (**A**). Live contribution route is identity (**B not C**).
