TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Cat docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/cat.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Cat — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not unregister Cat as a conclusion of this investigation.** Cat is already in `vanilla_hosts.living_biological`. Registration is participation, not extra biology.

Method: existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP |

Closed leaps: variant ≠ subtype biology; taming ≠ domestication BP field; lying/sleep/beg ≠ sleep/fear traits; `OcelotAttackGoal` ≠ Ocelot ancestry; tag ≠ diet; spawn structure ≠ origin; registered ≠ C; live `contributingSourceKey=cat` ≠ C.

Do **not** absorb Ocelot. Do **not** form a feline column with Ocelot.

Default: **NO** new BP field. Live contribution identity is **B**, not **C**.

---

## Subject

Cat (`minecraft:cat`) — `CatVariant` coat, taming/owner/collar, sit/lie/relax-on-owner, avoid-player when wild, rabbit/baby-turtle hunt, morning gift loot, village/`CatSpawner`, Host Registry LIVE `living_biological`, BioCraft gestation identity routing.

Out of scope: Ocelot, Wolf, Camel, Chicken.

---

## Version

Minecraft Java **1.21.1** only. `.tmp_mc_sources/` authoritative.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:cat` |
| `EntityType` | `EntityType.CAT` — `EntityType.java` **239–241**: `sized(0.6F, 0.7F).eyeHeight(0.35F).passengerAttachments(0.5125F).clientTrackingRange(8)` |
| Fire / lava | **No** `.fireImmune()` |
| Class | `Cat extends TamableAnimal implements VariantHolder<Holder<CatVariant>>` (`Cat.java` **76**) |
| Category | `MobCategory.CREATURE` |
| Attributes | Health **10**, movement **0.3F**, attack **3.0** (`Cat.java` **241–243**) |
| Host Registry | **REGISTERED.** `hosts.json` living_biological includes `"cat"` (**6**). `default_dna: baseline_biological`. No `variant_mappings` cat entry |
| Suitability | Registered living_biological → currently suitable via HostType path. Registered ≠ extra biology |

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP representation? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|----------------------------|--------------------|-------|
| Identity / CREATURE / size | `EntityType.CAT` | `EntityType.java` **239–241** | Identity | `organismKey = cat` | Resolver / Analyzer / host lookup | **B** |
| Coat variant | `DATA_VARIANT_ID` + `CatVariant` registry | Texture holders; spawn from `#cat_variant/default_spawns` or full moon / swamp black (`Cat.java` **344–356**) | Presentation/state | Identity covers organism | None reading coat as biology | **A** |
| Taming / owner | `TamableAnimal` + `tryToTame` | 1/3 chance on food; sets sit (`Cat.java` **441–448**) | Entity tame state | Not domestication field | None | **A** |
| Collar dye | `DATA_COLLAR_COLOR` | Owner + dye item (`Cat.java` **364–373**) | Presentation | Not needed | None | **A** |
| Ordered sit | `SitWhenOrderedToGoal` + `mobInteract` toggle | Owner interact (`Cat.java` **110**, **387–388**) | AI state | Not needed | None | **A** |
| Lie / relax on sleeping owner | `CatRelaxOnOwnerGoal` + `IS_LYING` / `RELAX_STATE_ONE` | Bed adjacency; morning gift loot (`Cat.java` **475–611**) | AI / loot | Not sleep trait | None | **A** |
| Beg / tempt | `CatTemptGoal` + beg sound | Untamed only; `#cat_food` (`Cat.java` **107**, **257–259**, **614–643**) | AI | Not fear/social field | None | **A** |
| Avoid players (wild) | `CatAvoidEntityGoal` | Added when untamed (`Cat.java` **430–438**) | AI | Not fear field | None | **A** |
| Hunt rabbit / baby turtle | `NonTameRandomTargetGoal` | Untamed only (`Cat.java` **121–122**) | AI targeting | Not needed | None | **A** |
| Attack goal reuse | `OcelotAttackGoal` | Goal class reused (`Cat.java` **118**) | Code reuse ≠ Ocelot ancestry | Distinct `ocelot` key | None | **A** |
| Food / breed | `#cat_food` + `BreedGoal` | Cod/salmon; both must be tame to mate (`Cat.java` **334–340**, **415–417**) | Tag ≠ diet | Child remains `cat` | None | **A** |
| Offspring variant/collar | `getBreedOffspring` | Random parent variant; copies tame/owner/collar if tame (`Cat.java` **307–327**) | Vanilla birth | Identity sufficient | None | **A** |
| Structure black cat | `StructureTags.CATS_SPAWN_AS_BLACK` | All-black + persistence (`Cat.java` **350–353**) | Encounter ≠ origin | Not origin field | None | **A** |
| Village cat spawn | `CatSpawner` | NPC spawner owner | Encounter | Not origin | None | **A** |
| Morning gift | `BuiltInLootTables.CAT_MORNING_GIFTS` | Loot on leave bed goal | Loot table | Not needed | None | **A** |
| Loot on death | `entities/cat.json` | String 0–2 | Drops ≠ anatomy | Not needed | None | **A** |
| Host → contributingSourceKey | Host Registry + gestation | `"cat"` living_biological → encode path `"cat"` | Identity only | `organismKey` + `contributingSourceKey=cat` + `baseline_biological` | **LIVE** generic writer/Analyzer (same as Cow/Horse path; no Cat-named unit test found) | **B** |

No row is **C**.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"cat"` | **LIVE** | living_biological **6** | Participation. Can originate contribution |
| `hosts.json` `"ocelot"` | **ABSENT** | Not in file | Do not absorb Ocelot; do not register from this packet |
| `variant_mappings` cat | **ABSENT** | No entry | No aggressive/neutral override |
| Resolver / Analyzer / gestation writer | **LIVE** generic | Same Model A path as Cow/Horse; sparse BP cores may be **UNKNOWN** | Identity only. **B not C** |
| Cat entity JSON | **ABSENT** | No production config | Vanilla owns AI/variants |
| Inventory cat row | **PLANNING** | Not edited here | Docs ≠ consumer |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails |
|----------------|--------------|
| Variants are Cat subtypes needing BP | Synched `CatVariant` texture registry. Presentation **A** |
| Taming needs domestication field | `TamableAnimal` state. No BioCraft consumer of tame as biology. **A** |
| Lying/sleeping/begging need sleep/fear/social fields | Goals + synched flags. **A** |
| `OcelotAttackGoal` means Cat is Ocelot / feline clade | Shared **goal class**. Distinct EntityTypes. Ocelot unregistered |
| Live `contributingSourceKey=cat` earns C | Identity already represented. **B** |
| Structure/village spawn is origin | Encounter placement. **A** |

---

## Potential biological relationships

### 1. Live xenomorph host / Model A source

- **Owner:** `hosts.json` + eligibility + `GestationManager.writeContributingSource` (documented LIVE path) + Analyzer.
- **Biological input?** Key `"cat"` only.
- **Result:** **B**.

### 2. Variant / tame / sit / lie / hunt

- **Owner:** `Cat` / `TamableAnimal` / goals / loot.
- **Named consumer:** None needing those as BP facts.
- **Result:** **A**.

### 3. Cat ↔ Ocelot

- Shared attack goal class only. Distinct keys. Do **not** absorb.
- **Result:** **A**.

**C is not earned.**

---

## Wiki orientation disagreements

| Common orientation | 1.21.1 authority | Conclusion |
|--------------------|------------------|------------|
| Cat is tamed Ocelot / same organism | Distinct `EntityType.CAT` vs `OCELOT` | Do not merge |
| Cat breeds are biology | `CatVariant` textures + tags | Presentation **A** |
| Health 10 / fish food | Attributes + `#cat_food` cod/salmon | Agrees; still **A** |

---

## Final stop gate

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** |
| Named missing-fact consumer | **NO** (identity consumer exists; not missing-fact) |
| Architectural escalation | **NO** |

**Closeout:** A = vanilla ownership for variant/tame/sit/lie/hunt/food/breed/spawn; B = identity including live `contributingSourceKey=cat`; C = not earned.
