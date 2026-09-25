TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent B docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/llama.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Llama — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register or unregister Llama as a conclusion of this investigation.** Llama is already in `vanilla_hosts.living_biological`. Registration is participation, not extra biology.

Method (every behavior): existing gameplay → actual owner → meaningful biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied independently: `AbstractHorse` / `AbstractChestedHorse` ≠ clade; shared Host Registry list ≠ horse/camel/donkey column; heritable/persistent variant ≠ required BP dimension; strength/carrying NBT ≠ carrying BP without a named BioCraft consumer; spit projectile ≠ Llama anatomy field; wolf-target AI ≠ predator-prey BP; tag ≠ diet; spawn ≠ origin; interesting behavior ≠ consumer; live `contributingSourceKey=llama` is **B**, not **C**.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey` (Model A Chestburster/Drone), optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

**Default: NO new BP field.** Do **not** absorb Horse, Camel, Donkey, Mule, or TraderLlama conclusions.

---

## Phase 1 gate (confirmed before probing)

| Required source / consumer | Status |
|----------------------------|--------|
| `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/Llama.java` | **PRESENT** |
| `.tmp_mc_sources/net/minecraft/world/entity/projectile/LlamaSpit.java` | **PRESENT** |
| `.tmp_mc_sources/net/minecraft/world/entity/ai/goal/LlamaFollowCaravanGoal.java` | **PRESENT** (referenced from `Llama.registerGoals`) |
| `AbstractHorse.java` / `AbstractChestedHorse.java` | **PRESENT** (parent chain) |
| Loot / tags / biomes under `.tmp_mc_sources/data/` | **PRESENT** (`loot_table/entities/llama.json`, `tags/item/llama_food.json`, `llama_tempt_items.json`, biome creature lists, `dismounts_underwater`) |
| BioCraft `hosts.json` + `BiologicalProfileResolver` / Analyzer / `contributingSourceKey` consumers | **PRESENT** (`hosts.json` includes `"llama"`; resolver + `GestationManager.writeContributingSource` + `DnaSampleFromOccupant` + `BiologicalProfileDnaAnalysisPort`) |

Gate result: proceed (not UNKNOWN from missing Phase 1 sources).

---

## Subject

Llama (`minecraft:llama`) — living Llama identity on Minecraft Java **1.21.1**. Scope: EntityType registration, `Llama` / `AbstractChestedHorse` / `AbstractHorse` gameplay owners, variant NBT, strength NBT vs chest inventory columns, carpet decor, spit projectile ownership, wolf-target AI, caravan AI, breeding within Llama, food/tempt tags, biome spawn, Host Registry `living_biological`, and BioCraft identity routing (`MobHostRegistry`, `GestationManager.writeContributingSource`, `BiologicalProfileResolver`, `DnaSampleFromOccupant`).

Out of scope as organisms: Horse, Donkey, Mule, Camel, TraderLlama. Those types appear only as **negative controls** (distinct keys / shared parent ≠ clade / TraderLlama subclass reuse ≠ Llama investigation).

---

## Version

Minecraft Java **1.21.1** only. Mapped sources in `.tmp_mc_sources/` are authoritative. Wiki is orientation / disagreement discovery only; **source wins**.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:llama` |
| `EntityType` | `EntityType.LLAMA` — `EntityType.java` **477–483**: `register("llama", Builder.of(Llama::new, MobCategory.CREATURE).sized(0.9F, 1.87F).eyeHeight(1.7765F).passengerAttachments(new Vec3(0.0, 1.37, -0.3)).clientTrackingRange(10))` |
| Related type (not absorbed) | `EntityType.LLAMA_SPIT` — **484–486** `MobCategory.MISC`, 0.25×0.25; `EntityType.TRADER_LLAMA` — distinct key **681+** |
| Fire / lava | Builder does **not** call `.fireImmune()` |
| Class | `Llama extends AbstractChestedHorse implements VariantHolder<Llama.Variant>, RangedAttackMob` (`Llama.java` **65**). `AbstractChestedHorse extends AbstractHorse`. `isTraderLlama()` returns **false** (**83–85**) |
| Category | `MobCategory.CREATURE` |
| Dimensions | Adult **0.9 × 1.87**, eyeHeight **1.7765**. Baby: `BABY_DIMENSIONS` scale **0.5** (`Llama.java` **69–72**, **457–459**) |
| Hierarchy vs Donkey/Mule | Sibling `AbstractChestedHorse` subclasses. Donkey/Mule use fixed `getInventoryColumns() → 5` when chested (`AbstractChestedHorse.java` **191–193**). Llama **overrides** columns to `getStrength()` when chested (`Llama.java` **286–288**). Distinct EntityTypes / registry keys. Shared parent ≠ clade |
| Host Registry | **REGISTERED.** `hosts.json` `vanilla_hosts.living_biological.mobs` includes `"llama"` (**6–8**). Group `default_dna`: `baseline_biological` (**4**). `MobHostRegistry.getHostType("llama")` → `HostType.LIVING_BIOLOGICAL`. `isSuitableForXenomorph("llama")` → **true**. `variant_mappings` has **no** llama entry (**47–52**) |
| Suitability | Registered `LIVING_BIOLOGICAL` → currently suitable for xenomorph hosting. Registered ≠ extra biology ≠ BP field |

Independent existence paths (not origin): `/summon` / spawn egg (summonable by default builder), biome creature lists, `Llama.getBreedOffspring` (Llama+Llama → `EntityType.LLAMA.create` via `makeNewLlama`).

Negative-control identities (not investigated as organisms):

| Type | 1.21.1 fact | Use here |
|------|-------------|----------|
| `EntityType.TRADER_LLAMA` | `TraderLlama extends Llama`; `isTraderLlama()` true; own despawn/defend goals | Distinct key. Do not absorb |
| Donkey / Mule | `AbstractChestedHorse` siblings; fixed 5-column chest | Hierarchy adjacency only |
| Horse / Camel | `AbstractHorse` siblings (Camel/Horse not chested-llama path) | Shared parent ≠ clade |

---

## Behavior ownership table

Refined manifestation classification values: **identity** | **persistent entity state** | **transient gameplay state** | **environmental interaction** | **item/block production** | **effect application** | **entity/state transformation** | **actual biological input consumed by BioCraft**.

| Behavior | Actual owner | 1.21.1 evidence | Refined classification | Biological input? | Existing composition? | Named BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|------------------------|-------------------|----------------------|--------------------------|-------|
| Identity / size / category | `EntityType.LLAMA` | `EntityType.java` **477–483** | identity | Identity only | `organismKey = llama` (registered) | Generic resolver / Analyzer / `DnaSampleFromOccupant`. **No** Llama-specific branch | **B** |
| Java type (`AbstractChestedHorse` + `VariantHolder`) | `Llama` class | `Llama.java` **65**. Does **not** extend Horse/Camel/Donkey | identity (implementation reuse) | Shared parent ≠ clade | Distinct key already | None for ancestry | **A/B** |
| **Variant** (creamy/white/brown/gray) | `Llama` synched `DATA_VARIANT_ID` + `Llama.Variant` | Define **141–142**; get/set **145–151**; NBT `"Variant"` **103**, **114**; enum **503–531**. Spawn: random or herd `LlamaGroupData` (**229–241**). Breed: 50/50 parent pick (**341**). Client texture only (`LlamaRenderer.getTextureLocation` **26–32**) | persistent entity state | Presentation/state. Heritable ≠ required BP dimension | Identity covers organism; coat is NBT | **None** that reads Llama variant as biology | **A** |
| **Strength** | `Llama` synched `DATA_STRENGTH_ID` | Define **141**; clamp 1–5 (**87–88**); NBT `"Strength"` **104**, **112**; spawn `setRandomStrength` (**91–94**, **231**): 4% → `1+nextInt(5)`, else `1+nextInt(3)`; breed lottery (**335–340**) | persistent entity state | Entity inventory-sizing state, not a BioCraft trait | Identity sufficient | **None** that reads Strength/carrying | **A** |
| Strength → inventory columns / slots | `Llama.getInventoryColumns` + `AbstractHorse.getInventorySize` | Columns = `hasChest() ? getStrength() : 0` (**286–288**). Slots = `columns * 3 + 1` (`AbstractHorse.java` **335–341**). Donkey/Mule fixed 5 columns when chested — different owner path | persistent entity state (derived UI capacity) | Strength **is** the column count when chested; slot count is derived (`3×columns+1`). Not an independent second stat | Not a carrying BP field | **None** | **A** |
| Chest equip flag | `AbstractChestedHorse` | `DATA_ID_CHEST` / NBT `"ChestedHorse"`; equip chest item (**167–183**). Llama uses same path; inventory recreate uses Llama column override | persistent entity state | Equipment/container flag | Identity sufficient | None | **A** |
| Carpet / decor (“swag”) | `Llama` BODY armor + client layer | `isBodyArmorItem` = `#wool_carpets` (**296–298**); `getSwag` DyeColor from carpet (**306–314**); `isSaddleable` **false** (**301–303**). `LlamaDecorLayer` renders carpet color or trader decor (**58–68**) | persistent entity state (item) + presentation | Equipment ≠ biology | Identity sufficient | None | **A** |
| Spit attack | `Llama.spit` / `performRangedAttack` + `RangedAttackGoal` | Goal **122**; `performRangedAttack` → `spit` (**448–450**, **352–375**). Creates `new LlamaSpit(level, this)` with owner Llama | transient gameplay state + entity spawn | Combat AI / projectile factory | Identity sufficient | None | **A** |
| Spit projectile damage | **`LlamaSpit`** (not Llama body) | Constructor sets owner (**26–33**); `onHitEntity` applies `damageSources().spit(this, livingentity)` for **1.0F** (**68–76**). Owner entity is Llama; damage owner class is LlamaSpit | environmental interaction / combat | Projectile mechanic | Identity sufficient | None | **A** |
| Wolf-targeted AI | `Llama.LlamaAttackWolfGoal` | Target `Wolf.class`, untamed only (**467–470**); follow distance ×0.25 (**472–475**). Registered on Llama (**131**) | transient gameplay state | AI targeting. Trace ownership = Llama goal, not Wolf biology | Identity sufficient | None | **A** |
| Hurt-by / spit interrupt | `Llama.LlamaHurtByTargetGoal` | Clears continue when `didSpit` (**487–500**); `didSpit` field **73**, set in spit (**374**) | transient gameplay state | AI flag | Identity sufficient | None | **A** |
| Caravan follow | `LlamaFollowCaravanGoal` + runtime head/tail fields | Goal **121**; joins nearby leashed / caravan Llama or TraderLlama (**24–69**); `caravanHead`/`caravanTail` (**75–77**, **401–425**) — **not** written to NBT in `addAdditionalSaveData` | transient gameplay state | Runtime leash-chain AI | Identity sufficient | None | **A** |
| Breeding (within Llama) | `Llama.canMate` / `getBreedOffspring` | Mate only other `Llama` with `canParent` (**325–327**). Offspring `makeNewLlama()` → `EntityType.LLAMA.create` (**348–350**). Strength + variant inheritance as above | entity/state transformation (vanilla birth) | Same-type birth; child remains `llama` | Child key still `llama` | None that needs breed/strength/variant fields | **A/B** |
| Food / tempt / love | `Llama` + item tags | `isFood` = `#llama_food` (**157–159**; wheat + hay_block). Tempt `#llama_tempt_items` = hay_block only (**125**). Love only on hay_block when tamed/age0 (**171–178**) | environmental interaction / item use | Tag ≠ diet trait | Identity sufficient | None | **A** |
| Taming / temper / ride | `AbstractHorse` + Llama overrides | Max temper **30** (**317–319**); wheat/hay temper path in `handleEating` (**195–199**). `isSaddleable` false — no saddle mount path like Horse | persistent entity state | Temper/tame entity state | Identity sufficient | None | **A** |
| Fall damage threshold | `Llama.causeFallDamage` | Applies hurt only if fallDistance ≥ **6.0F** (**382–398**) | environmental interaction | Fall rules, not anatomy BP | Identity sufficient | None | **A** |
| Attributes | `Llama.createAttributes` | `createBaseChestedHorseAttributes()` + FOLLOW_RANGE **40** (**134–136**). Chested base: speed 0.175F, jump 0.5 (`AbstractChestedHorse.java` **49–51**) | persistent entity state (stats) | Stats ≠ Llama-anatomy field | Identity sufficient | None | **A** |
| Biome spawn | Worldgen creature lists | `savanna_plateau` weight **8**, min/max **4** (**144–147**); `windswept_hills` / `windswept_gravelly_hills` / `windswept_forest` weight **5**, min **4**, max **6** | environmental interaction (encounter) | Spawn ≠ origin | Not an origin field | None | **A** |
| Water / dismount tag | Entity-type tag | `#dismounts_underwater` includes `minecraft:llama` (and trader_llama) | environmental interaction | Tag ≠ clade | Distinct key | Vanilla dismount, not BioCraft | **A** |
| Loot | Vanilla loot table | `loot_table/entities/llama.json`: leather 0–2 + looting | item/block production | Drops ≠ anatomy | Not needed | None | **A** |
| Host Registry / gestation contribution | `hosts.json` + `GestationManager.writeContributingSource` | `"llama"` living_biological; HostType `LIVING_BIOLOGICAL`; suitability **true**; `default_dna` `baseline_biological`. After Chestburster spawn: encode host id → registry path → `setContributingSourceKey` (`GestationManager.java` **164–175**) | actual biological input consumed by BioCraft | Identity routing only. **Not** variant/strength | `organismKey=llama` + optional `contributingSourceKey=llama` + HostType + `hostEffectProfileId=baseline_biological` | **LIVE** writer / resolver / Analyzer / occupant sample. No Llama-named unit | **B** |

**No row is C.** Live `contributingSourceKey=llama` is identity already represented — **B**, not C.

---

## Mandatory probe findings

### 1. Llama variant probe

| Question | Finding |
|----------|---------|
| Assignment | Spawn: random `Util.getRandom(Variant.values())` unless `LlamaGroupData` shares herd variant (`finalizeSpawn` **229–241**). Four values: creamy/white/brown/gray (**503–507**) |
| Persistence | Synched `DATA_VARIANT_ID` + NBT `"Variant"` (**103**, **114**, **145–151**) |
| Breeding inheritance | Offspring: `random.nextBoolean() ? this : other` parent variant (**341**). No environmental re-roll at birth |
| Environmental / spawn contribution | Herd group data only; biome spawn does **not** pick variant by biome |
| Gameplay vs rendering | **Rendering only** in 1.21.1 sources (`LlamaRenderer` texture switch). No combat/inventory/AI branch on variant |
| Live BioCraft consumption | **None.** Resolver/Analyzer/DnaSample paths do not read Variant NBT |

**Classification:** persistent entity state / presentation. Heritable ≠ required BP dimension. **A.**

### 2. Llama strength probe

| Question | Finding |
|----------|---------|
| Ownership | `Llama` only (`DATA_STRENGTH_ID`, private `setStrength`, public `getStrength`) |
| Assignment / randomization | `setRandomStrength` at `finalizeSpawn` (**231**): with probability **0.04** use upper bound 5 else 3; then `1 + nextInt(i)` → spawn range typically 1–3, rarely 1–5 |
| Persistence | Synched + NBT `"Strength"`; clamped **1–5** on set (**87–88**) |
| Inheritance | Breed: `nextInt(max(parentStrengths)) + 1`, then **3%** chance `i++` (**335–340**); clamp still applies via `setStrength` |
| Gameplay consumers | **(1)** `getInventoryColumns()` when `hasChest()` (**286–288**); **(2)** breeding lottery input. No AI, spit damage, wolf range, or renderer consumer |
| Strength vs inventory slot count | Strength = **column count** when chested. Slot count = `strength * 3 + 1` (`AbstractHorse.getInventorySize`). They are **linked**, not independent stats: strength is the persisted field; slots are derived. Unchested → columns **0** regardless of strength |
| BioCraft | **No** named consumer of Strength / carrying capacity. Without that consumer, **no** strength/carrying BP |

**Classification:** persistent entity state driving container UI size. **A.** Do not mint carrying BP.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"llama"` | **LIVE** | `living_biological.mobs` line **7** | Participation / HostType routing. Not manifestation proof |
| `HostType.LIVING_BIOLOGICAL` | **LIVE** | Enum + registry parse | Suitability vocabulary |
| Group `default_dna: baseline_biological` | **LIVE** | `hosts.json` **4** | Host-effect pack id. Shared pack ≠ shared organism fact |
| `MobHostRegistry.isSuitableForXenomorph("llama")` | **LIVE path** | Registered living_biological → true | Can originate contribution when gestated |
| `variant_mappings` llama | **ABSENT** | `hosts.json` **47–52** | No aggressive/neutral remap |
| Llama-named BioCraft Java | **ABSENT** | Module rg: no production `llama`/`Llama` references outside inventory docs | Generic identity path only |
| `BiologicalProfileResolver` | **LIVE** generic | Resolves HostType / hostEffect / xenomorph form / behaviorType from key; accepts optional `contributingSourceKey`; does not read Variant/Strength | Projects existing composition |
| Analyzer / occupant sample | **LIVE** generic | `DnaSampleFromOccupant` → `organismKey` + optional contributing source; `BiologicalProfileDnaAnalysisPort` projects compiled profile | Identity observation only |
| Llama entity JSON (mod) | **ABSENT** | No production llama config | Vanilla owns behavior |
| Inventory llama row | **PLANNING** | `vanilla_organism_inventory.md` pending | Docs ≠ live consumer; this packet does not edit it |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails (after ownership tracing) |
|----------------|----------------------------------------|
| Variant is a required Biological Profile dimension because it is heritable/persistent | Owner is Llama NBT + client texture. No BioCraft consumer. Heritable ≠ BP requirement. **A** |
| Strength/carrying capacity needs a BP field | Owner is Llama Strength → inventory columns. No named BioCraft consumer of Strength. **A** |
| Strength and slot count are two biology facts | Slot count is derived (`3×columns+1`); columns = strength when chested. One persisted field |
| `AbstractChestedHorse` / list adjacency with Donkey/Mule/Horse/Camel means one clade | Distinct EntityTypes and keys. Llama alone overrides columns via Strength. Shared parent/list ≠ clade |
| Spit is Llama anatomy / secretion BP | Projectile entity `LlamaSpit` owns hit damage; Llama owns spawn/AI. **A** |
| Wolf-targeting proves predator-prey biology for BP | `LlamaAttackWolfGoal` is Llama AI ownership. **A** |
| Caravan is social-structure biology | Runtime head/tail pointers + goal; not NBT-persisted. Transient AI. **A** |
| Carpet decor is fleece/wool biology | BODY equipment via `#wool_carpets` + render layer. **A** |
| Live `contributingSourceKey=llama` earns C | Consumer already has the organism-definition key. Identity **B**, not missing-fact **C** |
| Absorb TraderLlama / Horse / Camel conclusions | Out of scope; distinct keys; TraderLlama subclass reuse ≠ Llama BP |

---

## Potential biological relationships

### 1. Identity + Host Registry contribution

- **Owner:** `EntityType.LLAMA` + `hosts.json` `"llama"` + `GestationManager.writeContributingSource` + `BiologicalProfileResolver` / `DnaSampleFromOccupant`.
- **Biological input?** Registry key / HostType / optional contributing-source observation only.
- **Named consumer:** LIVE generic writer/resolver/Analyzer.
- **Result:** **B**. Live `contributingSourceKey=llama` is identity already represented. Not C.

### 2. Variant coat

- **Owner:** `Llama.Variant` + renderer.
- **Biological input?** No meaningful BioCraft input.
- **Named consumer?** None.
- **Result:** **A**.

### 3. Strength / chest capacity

- **Owner:** `Llama` Strength + `getInventoryColumns` + `AbstractHorse` inventory sizing.
- **Biological input?** No BioCraft consumer of Strength.
- **Named consumer?** None.
- **Result:** **A**. Reject carrying BP without named consumer.

### 4. Spit / wolf AI / caravan

- **Owner:** `Llama` goals + `LlamaSpit` projectile + caravan goal/fields.
- **Biological input?** No.
- **Named consumer?** None.
- **Result:** **A**.

### 5. Adjacency to Donkey / Mule / Horse / Camel / TraderLlama

- Shared `AbstractHorse` / `AbstractChestedHorse` or subclass reuse only.
- Distinct keys. Do **not** absorb.
- **Result:** **A/B** (identity already separated by key).

**C is not earned for any relationship.**

---

## Wiki orientation disagreements

| Common orientation | 1.21.1 authority | Conclusion |
|--------------------|------------------|------------|
| Llama “strength” is a separate carrying stat from chest slots | Strength → columns; slots = `3×columns+1` | Linked derived capacity, one NBT field |
| All coat variants change gameplay | Renderer texture switch only | Presentation **A** |
| Llamas are “horses” / same as camelids column | Distinct `"llama"`; Camel/Horse separate EntityTypes | Shared parent ≠ clade |
| Spit is a Llama body ability only | `LlamaSpit` entity owns damage application | Split ownership Llama vs LlamaSpit |
| Trader Llama is the same organism investigation | `EntityType.TRADER_LLAMA` + overrides | Distinct key; do not absorb |

---

## Final evidence conclusion

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** (`organismKey=llama`, optional `contributingSourceKey=llama`, `HostType.LIVING_BIOLOGICAL`, `hostEffectProfileId=baseline_biological`) |
| Named consumer exists | **YES** (live host/gestation/resolver/Analyzer identity-source path). **NO** named consumer of a **missing** Llama biological fact (variant, strength, spit, caravan, wolf AI, carpet) |
| Architectural escalation required | **NO** |

**Stop.** A = vanilla ownership; B = existing identity/composition including live Model A source identity; C = not earned. Do **not** change Host Registry. Do **not** mint variant/strength/carrying/spit/caravan/wolf/carpet Profiles. Do **not** absorb Horse/Camel/Donkey/Mule/TraderLlama.

### A/B/C per mechanic + overall

| Mechanic | A/B/C |
|----------|-------|
| Identity / HostType / live `contributingSourceKey` | **B** |
| AbstractHorse/ChestedHorse hierarchy adjacency | **A** (ancestry claim) / **B** (distinct key) |
| Variant | **A** |
| Strength / inventory columns / slots | **A** |
| Chest / carpet decor / no-saddle | **A** |
| Spit (Llama factory + LlamaSpit damage) | **A** |
| Wolf-target AI / hurt-by spit flag | **A** |
| Caravan | **A** |
| Breeding within Llama | **A** (mechanics) / **B** (child identity remains llama) |
| Food / tempt tags | **A** |
| Biome spawn / dismount tag / loot / fall / attributes | **A** |
| **Overall** | **B** (identity live; no C; behaviors A) |

### UNKNOWN list

| Item | Why UNKNOWN |
|------|-------------|
| Sparse BP core contents for `baseline_biological` beyond host-effect id routing | Resolver returns `hostEffectProfileId`; full effect-pack internals not re-audited for this organism-specific packet |
| Playtest confirmation that gestating a Llama writes `contributingSourceKey=llama` in-world | Code path is LIVE generic (`writeContributingSource`); no Llama-named playtest cited here |
| Post-1.21.1 llama changes (if any) | Out of version range by mission |
| TraderLlama-specific despawn/defend as separate organism facts | Explicitly not absorbed; not probed as subject |

### 1.21.1 authority anchors (files actually read)

- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/Llama.java`
- `.tmp_mc_sources/net/minecraft/world/entity/projectile/LlamaSpit.java`
- `.tmp_mc_sources/net/minecraft/world/entity/ai/goal/LlamaFollowCaravanGoal.java`
- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/AbstractChestedHorse.java`
- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/AbstractHorse.java` (inventory sizing **335–341**, **1179–1181**)
- `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` **477–486**
- `.tmp_mc_sources/net/minecraft/client/renderer/entity/LlamaRenderer.java`
- `.tmp_mc_sources/net/minecraft/client/renderer/entity/layers/LlamaDecorLayer.java`
- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/TraderLlama.java` (negative control only)
- `.tmp_mc_sources/data/minecraft/loot_table/entities/llama.json`
- `.tmp_mc_sources/data/minecraft/tags/item/llama_food.json`, `llama_tempt_items.json`
- `.tmp_mc_sources/data/minecraft/tags/entity_type/dismounts_underwater.json`
- `.tmp_mc_sources/data/minecraft/worldgen/biome/savanna_plateau.json`, `windswept_hills.json`, `windswept_gravelly_hills.json`, `windswept_forest.json`
- `implementations/minecraft/AlienCraft/biocraft-alien/src/main/resources/data/biocraft_alien/systems/hosts.json`
- `BiologicalProfileResolver.java`; `BiologicalProfileDnaAnalysisPort.java`; `DnaSampleFromOccupant.java`
- `GestationManager.writeContributingSource` (`GestationManager.java` **164–175**)
- `HostType.java`; `MobHostRegistry.java`

Checklist-only (not copied as Llama biology): prior temporary Horse/Camel packets; inventory planning row for `llama`.
