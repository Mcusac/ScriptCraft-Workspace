TEMPORARY EVIDENCE — NOT PROJECT SSOT

# Fox — temporary manifestation evidence packet

**Isolation:** Authoritative Minecraft Java 1.21.1 / NeoForge 21.1.208 mapped sources, live BioCraft, locked docs, and this packet’s own reads only. Goat / Mooshroom / Ocelot packets were **not** read or absorbed.

**Version:** Minecraft Java **1.21.1** (NeoForge **21.1.208**). Wiki = orientation only; **source wins**.

**Temp cache:** `.tmp_mc_sources/` (NON-SSOT).

---

## Identity

| Fact | Evidence |
|------|----------|
| Hierarchy | `Fox extends Animal implements VariantHolder<Fox.Type>` |
| Registration | `EntityType.FOX` — `"fox"`, `MobCategory.CREATURE`, `sized(0.6F, 0.7F)`, `eyeHeight(0.4F)`, tracking **8** (`EntityType.java` **364–370**) |
| Attributes | health **10**, movement **0.3F**, follow **32**, attack **2**, safe fall **5** |
| Baby dims | `BABY_DIMENSIONS` = FOX dims ×0.5, eyeHeight **0.2975F** |
| Host Registry | `"fox"` in `hosts.json` `vanilla_hosts.living_biological` — **LIVE** participation route |

---

## Behavior ownership table

Method: **owner → biological input? → existing composition? → named live BioCraft consumer? → A/B/C**

| Behavior | Actual owner | Category | 1.21.1 evidence | Bio input? | Existing composition | Named BioCraft consumer | Result |
|----------|--------------|----------|-----------------|------------|----------------------|-------------------------|--------|
| Identity / CREATURE / dimensions | `EntityType.FOX` | identity | Registry id `"fox"` | Identity | `organismKey=fox` | Resolver + Analyzer + gestation writer (generic) | **B** |
| Host contribution | `hosts.json` + `GestationManager.writeContributingSource` | BioCraft-consumed biological input | encodeId → registry path `"fox"` onto offspring | Identity only | `contributingSourceKey=fox` | **LIVE** generic path; **no** fox-named unit test | **B** |
| Variant RED/SNOW | `Fox.Type` + `DATA_TYPE_ID` + NBT `"Type"` | persistent entity state | Synched int; `setVariant`/`getVariant`; NBT persist | Presentation + spawn/AI priority | Identity covers organism | **None** reading variant as biology | **A** |
| Variant assignment (spawn) | `finalizeSpawn` + `Fox.Type.byBiome` | environmental interaction | `BiomeTags.SPAWNS_SNOW_FOXES` → SNOW else RED; group data can share type | Encounter presentation | Not needed | None | **A** |
| Variant after creation | `setVariant` only via spawn/breed/NBT | persistent entity state | No thunder/environment mutate path in `Fox.java` | Fixed after set unless NBT/commands | Not needed | None | **A** |
| Variant breeding | `getBreedOffspring` | persistent entity state | Offspring type = random parent A or B variant (not biome) | Heritable state ≠ BP field | Not needed | None | **A** |
| Variant → prey goal priority | `setTargetGoals` | transient gameplay state / AI | RED: land/turtleEgg pri 4, fish 6; SNOW: fish 4, land/turtleEgg 6 | AI priority only | Not diet/subtype Profile | None | **A** |
| Sleep / sit / crouch / pounce flags | `DATA_FLAGS_ID` bits + goals | transient gameplay state | SleepGoal, FLAG_SLEEPING, etc. | AI presentation | Not sleep Profile | None | **A** |
| Trust UUIDs (0/1) | synched Optional UUID + NBT `"Trusted"` | persistent gameplay state | Avoid players if not trusted; DefendTrustedTargetGoal; breed/egg add love-cause UUIDs | Entity relationship state | Not social/domestication Profile | None | **A** |
| Held item / eat | mainhand pickup + `canEat` FOOD component | item/block production / AI | `setCanPickUpLoot(true)`; eat after 600 ticks | Item AI | Not metabolism field | None | **A** |
| Food / breed | `#fox_food` | item/block production | sweet_berries, glow_berries | Tag ≠ diet trait | Not needed | None | **A** |
| Prey AI | NearestAttackableTargetGoal chicken/rabbit/fish/baby turtle | AI/gameplay | Class predicates + AbstractFish school | Hunt AI ≠ shared-hunt clade | Distinct keys | None | **A** |
| Berry bush eat | `FoxEatBerriesGoal` | environmental interaction | Moves to sweet berry / cave vines | World interact | Not needed | None | **A** |
| Powder snow climb | `ClimbOnTopOfPowderSnowGoal` + tag | environmental interaction | Fox in `#powder_snow_walkable_mobs` | Path rule | Not needed | None | **A** |
| Spawn floor | `#foxes_spawnable_on` | environmental interaction | `checkFoxSpawnRules` | Encounter | Not origin field | None | **A** |
| Death loot | `loot_table/entities/fox.json` | item/block production | Empty pools in this extract | Loot | Not anatomy | None | **A** |

**No row is C.** Live `contributingSourceKey=fox` is identity already in Model A.

---

## Fox variant probe (dedicated)

| Probe question | Outcome |
|----------------|---------|
| Assignment | `finalizeSpawn`: `byBiome(SPAWNS_SNOW_FOXES)` or group `FoxGroupData.type` |
| Persistence | Synched `DATA_TYPE_ID` + NBT `"Type"` string name |
| Change after creation | No in-class environment mutate; only `setVariant` / NBT / breed child set |
| Breeding | Random choice of this vs partner variant — **not** biome re-roll |
| Environment | Biome tag at spawn only |
| Behavior beyond render | Prey goal **priority order** differs RED vs SNOW (`setTargetGoals`) |
| Gameplay beyond spawn/render | Same prey set; priority swap only |
| BioCraft consumers | **None** variant-specific; host path consumes `"fox"` id only |

**Verdict:** Variant is persistent entity state + spawn/AI owner (**A**). Heritability alone does **not** earn a BP field. No live consumer requires RED/SNOW distinction.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"fox"` | **LIVE** | living_biological list | Participation; can originate contribution |
| fox-named Java/tests | **ABSENT** | `rg` under biocraft-alien (excl. build) → hosts.json only | No fox-specific consumer |
| Resolver / Analyzer / gestation | **LIVE** generic | Same Model A path as Cow/Cat | Identity **B not C** |
| `variant_mappings` fox | **ABSENT** | No entry | No aggressive/neutral override |
| Fox entity JSON | **ABSENT** | No production config | Vanilla remains owner |
| Inventory / planning | **PLANNING** | inventory pending row | Not a live consumer |

---

## Rejected temptations

| Temptation | Why rejected |
|------------|--------------|
| Feline clade with Cat/Ocelot | Distinct EntityTypes; hunt goals are Fox-owned predicates; shared prey classes ≠ ancestry |
| Sleep / trust / diet Profiles | Flags, UUID list, item tags — no named BioCraft consumer |
| Variant BP from heritability / snow biome | Spawn + AI priority only; no BioCraft variant reader |
| Treat live `contributingSourceKey=fox` as C | Identity already represented |

---

## Potential relationships

| Relation | Status |
|----------|--------|
| Fox ↔ Cat/Ocelot | Prey/AI adjacency only — **not** feline column |
| Fox ↔ Wolf/PolarBear | Avoid goals — combat AI |
| Fox ↔ chicken/rabbit/fish/turtle egg | Prey selectors — not shared biology |
| Host DNA | Live identity contribution via `"fox"` |

---

## Final evidence conclusion

| Question | Answer |
|----------|--------|
| **New BP field earned?** | **NO** |
| **Existing composition sufficient?** | **YES** — `organismKey` / `contributingSourceKey=fox` |
| **Named live BioCraft consumer (missing fact)?** | **NO** — identity consumer exists; not missing-fact |
| **Architectural escalation?** | **NO** — do not mint `DESIGN-BIO-MANIFEST-004` |

### A/B/C summary
- Vanilla behaviors (variant, sleep, trust, diet, prey, berries, spawn): **A**
- Identity + live host contribution: **B**
- **C:** not earned
ckUpLoot`; `pickUpItem` / `canHoldItem` food preference (**478–517**); eat after 600 ticks if FOOD component (**193–209**); spit/drop on death (**483–493**, **679–687**); default equipment loot-like items 20% (**240–259**) | Equipment / AI | Not metabolism field | None | **A** |
| Berry food / breed (**item-block production** / food gate) | `#item/fox_food` + `FoxEatBerriesGoal` | Tag: sweet_berries, glow_berries; `isFood` (**558–560**); grief pick sweet/glow berries under `MOBGRIEFING` (**882–953**); EntityType immune to sweet berry bush | Tag ≠ diet genetics; block interaction | Child remains `fox` | None | **A** |
| Avoid wolf / polar bear / untamed players | `AvoidEntityGoal`s | (**157–164**) | AI | Not fear Profile | None | **A** |
| Client texture / held-item layer | `FoxRenderer` + `FoxHeldItemLayer` | RED/SNOW + sleep textures (**FoxRenderer.java** **16–39**); MAINHAND render (**FoxHeldItemLayer**) | Presentation | Not needed | None | **A** |
| Loot on death | `entities/fox.json` | Empty pools (type + `random_sequence` only); datapack `VanillaEntityLoot` adds empty table for FOX | Drops ≠ anatomy | Not needed | None | **A** |
| Host → contributingSourceKey (**BioCraft-consumed biological input**) | Host Registry + `GestationManager.writeContributingSource` | `"fox"` living_biological → `encodeId` → `HostRegistryPaths.registryPath` → `"fox"` (**GestationManager.java** **164–175**); Analyzer/resolver project identity + optional source | **Identity string only** — not variant, sleep, trust, diet | `organismKey` + `contributingSourceKey=fox` + `baseline_biological` | **LIVE** generic writer / Resolver / DnaAnalysisPort (no fox-named branch; no fox unit test) | **B** |

No row is **C**.

---

## Required variant probe (Fox.Type RED / SNOW)

| Probe question | Finding |
|----------------|---------|
| Assignment | Natural spawn: `finalizeSpawn` → biome holder → `Fox.Type.byBiome` (`#spawns_snow_foxes` → SNOW else RED). Same spawn group shares type via `FoxGroupData`. |
| Persistence | Synched `DATA_TYPE_ID` (int id) + NBT `"Type"` (`"red"` / `"snow"`). Reloaded on `readAdditionalSaveData`; then `setTargetGoals()` re-added on server. |
| Change after creation? | **No** vanilla gameplay mutator after spawn/breed. External NBT/`setVariant` can change; not a live BioCraft concern. |
| Breeding | Offspring type = **random parent** (50/50 this vs partner). **Not** re-derived from birth biome. |
| Biome/spawn | Snow foxes only via `#spawns_snow_foxes` at finalize; spawn floor `#foxes_spawnable_on`. |
| Behavioral consequences beyond render/spawn | **Yes, limited:** `setTargetGoals` changes **priority** of land vs fish target goals. Same prey classes remain targetable. |
| Gameplay effects | Prey-priority skew; texture/sleep texture; no separate loot/attributes/damage by type found in `Fox.java` / fox loot JSON. |
| Live BioCraft consumers of distinction | **None.** Resolver does not read type; gestation writes registry path `"fox"` only; no `variant_mappings` fox entry; module string `"fox"` appears only in `hosts.json` among live sources searched. |

**Verdict:** Variant is **A**. Heritable ≠ earned BP field. Do **not** mint a fox-variant composition fact.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"fox"` | **LIVE** | living_biological **7** | Participation. Can originate contribution |
| `variant_mappings` fox | **ABSENT** | No entry (only spider/creeper/wolf/enderman) | No aggressive/neutral override |
| `MobHostRegistry.getHostType("fox")` | **LIVE** after bind | Returns `LIVING_BIOLOGICAL` | Soft registry lookup |
| `BiologicalProfileResolver` | **LIVE** generic | No fox branch; hostType + `baseline_biological` via registry; optional `contributingSourceKey` passthrough | Identity only → **B** |
| `GestationManager.writeContributingSource` | **LIVE** generic | Encodes host entity type path | Writes `"fox"` for fox hosts |
| `HostEligibilityService` / `HostEffectManager` | **LIVE** generic | Suitability by HostType; effects by dna profile id | No fox-named special case |
| Analyzer / vial helpers | **LIVE** generic | `organismKey` + optional `contributingSourceKey` | Display/persist identity |
| Java/resources/tests fox-named | **DEAD** / absent beyond hosts list | `rg -i fox` under `biocraft-alien` → **only** `hosts.json` line | No STUB, PARSE-ONLY, TEST, or PLANNING fox hooks |
| Vanilla fox loot / tags / client | Vanilla **LIVE** | JSON + `FoxRenderer` / `FoxHeldItemLayer` / `FoxModel` | Minecraft ownership |
| Inventory fox row | **PLANNING** | pending manifestation | Docs ≠ consumer |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails |
|----------------|
| RED/SNOW need a BP variant / biome-adaptation field | Synched enum + spawn tag + texture + prey **priority**. Heritable from parents. No BioCraft consumer of the distinction. **A** |
| Invent variant BP because breeding copies type | Heritability alone does not earn C; consumer must need the missing fact |
| Day sleep / night activity need Sleep Profile | `SleepGoal` + flags. No named consumer. **A** |
| Trust UUIDs need social/domestication field | Persistent entity state for avoid/defend. Not `TamableAnimal`. No BioCraft consumer. **A** |
| `#fox_food` / berry eating need Diet Profile | Item tag + grief goal. Tag ≠ diet genetics. **A** |
| Prey goals ⇒ feline / shared hunt with Cat/Ocelot | Fox-owned AI predicates/goals. Distinct EntityTypes/keys. Do **not** form feline clade. **Closed leap** |
| Live `contributingSourceKey=fox` earns C | Identity already represented by composition. **B** |
| Registered living_biological ⇒ biological sufficiency / C | Registration = participation. Sufficiency for contribution is identity **B**, not new fields |

---

## Potential biological relationships

### 1. Live xenomorph host / Model A source

- **Owner:** `hosts.json` + eligibility + `GestationManager.writeContributingSource` + Resolver/Analyzer.
- **Biological input?** Key `"fox"` only (registry path).
- **Result:** **B**.

### 2. Variant / sleep / trust / diet / prey AI

- **Owner:** `Fox` / goals / tags / client.
- **Named consumer:** None needing those as BP facts.
- **Result:** **A**.

### 3. Fox ↔ Cat / Ocelot

- Surface adjacency: small carnivore + chicken/rabbit hunt themes. **Ownership is separate.** Do **not** absorb or form a feline column from this packet.
- **Result:** **A** (adjacency only).

### 4. Fox ↔ prey entities (chicken, rabbit, fish, turtle)

- Vanilla AI coupling only. Not BioCraft family / shared hunt biology.
- **Result:** **A**.

**C is not earned.**

---

## Tag probe (membership → 1.21.1 consumer → behavior → biological meaning? → BioCraft consumer?)

| Tag | Fox member / role | Named 1.21.1 consumer | Behavior | Biological meaning for BP? | BioCraft consumer? |
|-----|-------------------|----------------------|----------|----------------------------|--------------------|
| `#item/fox_food` | N/A (food list) | `Fox.isFood` | Tempt/breed: sweet/glow berries | Item food gate | None |
| `#block/foxes_spawnable_on` | N/A (floor) | `Fox.checkFoxSpawnRules` | Natural spawn floor | Spawn rule | None |
| `#worldgen/biome/spawns_snow_foxes` | N/A (biome list) | `Fox.Type.byBiome` | Assign SNOW vs RED | Spawn cosmetic + prey priority skew | None |
| `#entity_type/powder_snow_walkable_mobs` | **Yes** (datapack provider) | Powder-snow walk path | Walk on powder snow | Locomotion exemption | None |

---

## Final stop gate

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** — identity (`organismKey` / `contributingSourceKey=fox` / `baseline_biological`) covers live contribution; nothing observed requires extending `CompiledBiologicalProfile` |
| Named missing-fact consumer | **NO** (identity consumer exists; not missing-fact). No fox-named code consumers beyond hosts list membership |
| Architectural escalation | **NO** — do not mint `DESIGN-BIO-MANIFEST-004` |

### A/B/C outcome summary

| Lane | Outcome |
|------|---------|
| Vanilla AI / variant / sleep / trust / diet / prey / loot / client | **A** |
| Host Registry identity + gestation contributing source + generic Resolver/Analyzer | **B** (proved: consumed fact is registry path `"fox"` only) |
| New BP field | **C not earned** |

**Closeout:** A = vanilla ownership for variant/sleep/trust/hold/berries/prey/spawn; B = identity including live `contributingSourceKey=fox`; C = not earned.

### UNKNOWN facts

| Item | Status |
|------|--------|
| Exact Overworld biome spawn weight lists beyond datapack `OverworldBiomes` samples seen | Partially evidenced (FOX spawn entries exist in biome data); not required for A/B/C — spawn ownership remains vanilla **A** |
| Whether any external datapack/command routinely mutates `"Type"` in play | UNKNOWN / out of scope; still no BioCraft consumer of type |

No load-bearing mapped source was missing for the identity, variant, or contribution conclusions above.
