TEMPORARY EVIDENCE — NOT PROJECT SSOT

Do not treat this file as canonical design documentation.
Do not promote into manifestations/mule.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Mule — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register or unregister Mule as a conclusion of this investigation.** Mule is already in `vanilla_hosts.living_biological`. Registration is participation, not extra biology. Host Registry presence ≠ automatic A (and ≠ C).

Method (every behavior): owner → biological input? → `organismKey` / `contributingSourceKey` enough? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied independently: `AbstractHorse` / `AbstractChestedHorse` ≠ clade; hybrid name ≠ ancestry; Horse+Donkey→Mule is a **distinct-key factory** (Horse report locked — **do not reopen as C**); shared `hosts.json` list ≠ clade; spawn ≠ origin; tag ≠ clade; Host Registry ≠ eligibility science; interesting sterility/chest ≠ consumer; registered `LIVING_BIOLOGICAL` + live `contributingSourceKey=mule` is **B**, not **C**.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey` (Model A Chestburster/Drone), optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

**Default: NO new BP field.** Horse / Donkey / Camel / Llama / Trader Llama are **not absorbed**. Prior temp packets (`horse.md`, `donkey.md`) are **adjacency / factory cross-check only** — every Mule owner below was re-read from 1.21.1 mapped sources. Focus: what **Mule itself** owns/consumes/manifests **after creation**.

---

## Subject

Mule (`minecraft:mule`) — living Mule identity on Minecraft Java **1.21.1**. Scope: EntityType registration; `Mule` / `AbstractChestedHorse` / `AbstractHorse` gameplay owners after the entity exists; chest inventory (vs Donkey baseline); **no natural mate path** (`AbstractHorse.canMate` default false); Host Registry `living_biological`; BioCraft identity routing (`HostEligibilityService`, `GestationManager.writeContributingSource`, `BiologicalProfileResolver`); and a **mandatory state-transfer probe** of Horse/Donkey → Mule factory (what survives creation vs inherited biological composition).

Out of scope as organisms: Horse, Donkey, Camel, Llama, Trader Llama, Skeleton Horse, Zombie Horse. Those types appear only as **factory parents** / negative controls. Horse’s locked “distinct-key factory not ancestry” conclusion is **accepted**, not re-litigated.

---

## Version

Minecraft Java **1.21.1** only. Mapped sources in `.tmp_mc_sources/` are authoritative. Wiki is orientation / disagreement discovery only; **source wins**.

Post-1.21.1 mount UI / later food changes are **out of range**.

---

## Phase 1 gate

| Required probe | Status |
|----------------|--------|
| `.tmp_mc_sources/.../horse/Mule.java` | **Present** |
| `Horse.java`, `Donkey.java`, `AbstractChestedHorse.java`, `AbstractHorse.java` (breed/factory) | **Present** |
| Related loot / tags | **Present** (`loot_table/entities/mule.json`; `#dismounts_underwater`; `#horse_food` / `#horse_tempt_items` via AbstractHorse) |
| BioCraft `hosts.json` + `BiologicalProfileResolver` / Analyzer path / `contributingSourceKey` | **Present** under `implementations/minecraft/AlienCraft/` |

Gate **PASS** — proceed (not UNKNOWN).

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:mule` |
| `EntityType` | `EntityType.MULE` — `EntityType.java` **506–509**: `register("mule", Builder.of(Mule::new, MobCategory.CREATURE).sized(1.3964844F, 1.6F).eyeHeight(1.52F).passengerAttachments(1.2125F).clientTrackingRange(8))` |
| Fire / lava | MULE builder does **not** call `.fireImmune()` |
| Class | `Mule extends AbstractChestedHorse` (`Mule.java` **12**). `AbstractChestedHorse extends AbstractHorse` (**26**). Does **not** extend Horse or Donkey |
| Category | `MobCategory.CREATURE` |
| Dimensions | Adult **1.3964844 × 1.6**, eyeHeight **1.52**, passengerAttachments **1.2125F**, clientTrackingRange **8**. Baby: `AbstractChestedHorse` scaled baby dims (**33–35**, **62–64**). Contrast Donkey height **1.5** / passengerAttachments **1.1125F** / tracking **10**; Horse height **1.6** / passengerAttachments **1.44375F** / tracking **10** |
| Default attributes | `DefaultAttributes.java` **129**: `EntityType.MULE` → `AbstractChestedHorse.createBaseChestedHorseAttributes()` — same supplier as Donkey (**107**): base horse attrs + movement **0.175F**, jump **0.5** (`AbstractChestedHorse.java` **49–51**). Spawn `randomizeAttributes` overwrites **MAX_HEALTH only** (**39–41**) |
| Host Registry | **REGISTERED.** `hosts.json` `vanilla_hosts.living_biological.mobs` includes `"mule"` (**6–8**). Group `default_dna`: `baseline_biological` (**4**). `MobHostRegistry.getHostType("mule")` → `HostType.LIVING_BIOLOGICAL`. `isSuitableForXenomorph("mule")` → **true**. `variant_mappings` has **no** mule entry (**47–52**) |
| Suitability | Registered `LIVING_BIOLOGICAL` → currently suitable for xenomorph hosting. Registered ≠ extra biology ≠ BP field |
| Inventory baseline | `vanilla_organism_inventory.md` **146**: bio-organic, registered, `LIVING_BIOLOGICAL`, pending investigation |

Independent existence paths (not origin): `/summon` / spawn egg (`Items.MULE_SPAWN_EGG`); Horse↔Donkey breeding factory → `EntityType.MULE`; **no** biome creature-list spawn entries for `minecraft:mule` under `.tmp_mc_sources/data/minecraft/worldgen/` (grep empty). `SpawnPlacements` still registers MULE ON_GROUND animal rules (summon/egg placement), not worldgen population.

Factory parents (not absorbed; Horse conclusion locked):

| Type | Role for Mule |
|------|----------------|
| `EntityType.HORSE` | Mate-eligible with Donkey; `Horse.getBreedOffspring` creates MULE + `setOffspringAttributes` when other is Donkey (`Horse.java` **184–190**) |
| `EntityType.DONKEY` | Mate-eligible with Horse; `Donkey.getBreedOffspring` creates MULE + `setOffspringAttributes` when other is Horse (`Donkey.java` **63–70**) |

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing composition? | Named BioCraft consumer? | Refined manifestation classification | A/B/C |
|----------|--------------|-----------------|-------------------|----------------------|--------------------------|--------------------------------------|-------|
| Identity / size / category | `EntityType.MULE` | `EntityType.java` **506–509**: `"mule"`, `CREATURE`, 1.3964844×1.6, eyeHeight 1.52, passengerAttachments 1.2125, tracking 8 | Identity only | `organismKey = mule` (registered) | Generic resolver / Analyzer identity. **No** Mule-specific branch | **identity** | **B** |
| Java type (`AbstractChestedHorse`) | `Mule` class | `Mule.java` **12**. Shared parent with Donkey/Llama ≠ clade | Shared parent ≠ ancestry | Distinct key already | None for hybrid ancestry | **identity** (type hierarchy ≠ biology) | **A/B** |
| Chest flag / inventory columns | `AbstractChestedHorse` | Synched `DATA_ID_CHEST`; NBT `"ChestedHorse"` + `"Items"`; equip `Items.CHEST`; `getInventoryColumns` → **5** if chested else **0**; drop chest block on death (`AbstractChestedHorse.java` **27–75**, **167–193**). Mule overrides equip sound → `MULE_CHEST` (`Mule.java` **49–51**) | **No.** Item/equipment + container state. Same chest helper as Donkey | Identity sufficient | None that reads chest as anatomy | **persistent entity state** + **item/block production** (chest drop) | **A** |
| Chest vs Donkey | Presentation + EntityType dims only | Same `AbstractChestedHorse` chest API. Donkey uses default `DONKEY_CHEST` sound (`AbstractChestedHorse` **186–188**); Mule overrides to `MULE_CHEST`. No Donkey-only chest columns | Contrast ≠ clade / ≠ missing BP | Distinct keys | None | **transient gameplay state** (sound) + shared container owner | **A** |
| `canGallop = false` | `AbstractChestedHorse` ctor | Sets `this.canGallop = false` (**32**) | Ride/animation flag | Identity sufficient | None | **transient gameplay state** | **A** |
| Taming / temper / owner | `AbstractHorse` | Flags / NBT `"Tame"` / `"Temper"` / `"Owner"`; max temper 100; crazy-run goal; feeding temper | **No.** Ride/temper entity state | Identity sufficient | None | **persistent entity state** | **A** |
| Saddle / riding / jump | `AbstractHorse` + `Saddleable` | Saddleable when alive + adult + tamed; controlling passenger needs saddle; jump API. Mule overrides jump sound (`Mule.java` **44–46**) | Equipment + ride API | Identity sufficient | None | **transient gameplay state** + equipment | **A** |
| BODY / EQUESTRIAN armor | **ABSENT on Mule** | `Mob.canUseSlot` denies BODY by default; Mule/AbstractChestedHorse do **not** override (Horse does). Contrast only — do not absorb Horse armor | Equipment gate | Not an armor-capability field | None | **transient gameplay state** (equipment refusal) | **A** |
| Food / tempt / love | `AbstractHorse` + item tags | `isFood` = `#minecraft:horse_food`; Tempt `#horse_tempt_items`; love golden carrot/apple/enchanted apple if tamed (`AbstractHorse` food/tempt/handleEating paths). Shared tag name ≠ Horse clade | Food tag ≠ diet trait | Identity sufficient | None | **environmental interaction** | **A** |
| Mate eligibility / natural breed | **`AbstractHorse.canMate` default** | Mule does **not** override `canMate`. `AbstractHorse.canMate` returns **false** (**898–900**). Horse/Donkey accept only Horse/Donkey partners — never Mule | **No.** Vanilla sterility gate. Hybrid name ≠ fertility BP | Distinct key; no mate field needed | None for a sterility Profile | **entity/state transformation** gate (blocked) | **A** |
| `Mule.getBreedOffspring` | `Mule` | Returns `EntityType.MULE.create(level)` **without** `setOffspringAttributes` (`Mule.java` **55–57`). Natural path unreachable because `canMate` is false | Dead natural path / create-only stub | Identity if ever created | None | **entity/state transformation** (unreachable naturally) | **A** |
| Horse/Donkey → Mule factory (creation) | `Horse` / `Donkey` `getBreedOffspring` | Cross-check both parents: Horse+Donkey → `EntityType.MULE.create` + `setOffspringAttributes` (`Horse.java` **184–190**; `Donkey.java` **63–70**). `BreedGoal` calls initiator `spawnChildFromBreeding` → that parent's `getBreedOffspring` (`BreedGoal.java` **82**; `Animal.java` **214–231**) | Distinct-key **factory** (Horse report locked). Not Mule ancestry BP | Child is `mule` key | None for hybrid ancestry field | **entity/state transformation** (creation) | **A/B** |
| Factory attribute blend | `AbstractHorse.setOffspringAttributes` | Blends `MAX_HEALTH`, `JUMP_STRENGTH`, `MOVEMENT_SPEED` within clamps (**912–916**). Applied by Horse/Donkey factory paths onto the new Mule | Transient breeding math → child stats. **Not** inherited BioCraft composition | Identity sufficient | **None** — BioCraft does not read mule attributes from parents | **persistent entity state** (stats on child) | **A** |
| Factory age / placement | `Animal.spawnChildFromBreeding` | `setBaby(true)`; `moveTo` initiator position; love reset / XP / bred trigger (**214–247**) | Age/spawn state | Entity baby flag | None | **persistent entity state** (age) + spawn placement | **A** |
| Goals / grass | `AbstractHorse.registerGoals` | Panic, crazy-run, `BreedGoal(..., AbstractHorse.class)`, follow parent, stroll, look; Float+Tempt via `addBehaviourGoals`. `canEatGrass()` true. BreedGoal may path toward AbstractHorse subtypes, but Mule `canMate` still rejects all partners | AI. Shared parent ≠ clade | Identity sufficient | None | **transient gameplay state** / AI | **A** |
| Attributes (post-creation / non-breed spawn) | Chested defaults + health randomize | Base jump 0.5 / move 0.175F; `finalizeSpawn` → `randomizeAttributes` health only | Stats ≠ anatomy BP | Identity sufficient | None | **persistent entity state** | **A** |
| Water / dismount | Entity-type tags | Mule **is** in `#dismounts_underwater`. Not in `#undead`. Has `FloatGoal` | Tag ≠ clade | Distinct key | Vanilla dismount, not BioCraft | **environmental interaction** | **A** |
| Natural biome spawn | **ABSENT** | No `minecraft:mule` in worldgen biome creature lists (grep empty). Existence via summon/egg/breed | Spawn absence ≠ origin BP / ≠ sterility field | Not an origin field | None | **environmental interaction** (none) | **A** |
| Sounds | `Mule` overrides | Ambient/angry/death/eat/hurt/jump/chest → `SoundEvents.MULE_*` (`Mule.java` **18–51**) | Presentation | Identity sufficient | None | presentation / **transient gameplay state** | **A** |
| Loot | Vanilla loot table | `loot_table/entities/mule.json`: leather 0–2 + looting. Chest/inventory via AbstractChestedHorse / AbstractHorse drop paths | Drops ≠ anatomy | Not needed | None | **item/block production** | **A** |
| Host Registry / gestation | `hosts.json` + eligibility + `writeContributingSource` | `"mule"` in `living_biological`; HostType `LIVING_BIOLOGICAL`; suitability **true**; `default_dna` `baseline_biological`. After Chestburster spawn: encode **host** id → registry path → `setContributingSourceKey` (`GestationManager.java` **164–175**) | Identity routing only. Does **not** store parent Horse/Donkey keys, chest, attributes, or factory history | `organismKey=mule` + optional `contributingSourceKey=mule` + HostType + `hostEffectProfileId=baseline_biological` | **LIVE** production writer / resolver. Not a Mule-named unit test | **identity** (+ BioCraft participation); Model A key = **actual biological input consumed by BioCraft** | **B** |

**No row is C.** Live `contributingSourceKey=mule` is identity already represented — **B**, not C. Inventory baseline: registered `LIVING_BIOLOGICAL` participation is **B**.

---

## Mandatory state-transfer probe (Horse/Donkey → Mule)

### Scope

Trace **all** biologically or behaviorally relevant state that survives Horse↔Donkey creation of a Mule. Distinguish **factory inputs** (vanilla breeding math / create path) from **inherited biological composition** for BioCraft. Identify what information is retained from Horse vs Donkey, and whether any resulting state is consumed by BioCraft.

### Creation callers (cross-check both parents)

| Initiator (`this` in `spawnChildFromBreeding`) | Partner | Offspring path | Evidence |
|------------------------------------------------|---------|----------------|----------|
| Horse | Donkey | `EntityType.MULE.create` + `this.setOffspringAttributes(otherParent, mule)` | `Horse.java` **184–190** |
| Donkey | Horse | `EntityType.MULE.create` + `this.setOffspringAttributes(otherParent, abstracthorse)` | `Donkey.java` **63–70** |
| Mule | any | Natural: **blocked** (`canMate` false). Stub: `MULE.create` **without** attribute blend | `Mule.java` **55–57**; `AbstractHorse.java` **898–900** |

`BreedGoal` always calls **the animal that reached breed distance** as initiator (`BreedGoal.java` **82**). Either parent can be initiator; both factory branches that produce Mule call `setOffspringAttributes`.

### What transfers into the new Mule

| State | Transfers? | Source | Detail |
|-------|------------|--------|--------|
| EntityType identity | **Replaced** | Factory | Child is always `minecraft:mule` — not Horse, not Donkey. Distinct-key factory (Horse locked conclusion) |
| `MAX_HEALTH` base | **Yes (blended)** | Both parents via `setOffspringAttributes` | `createOffspringAttribute(thisValue, parentValue, min, max, random)` (`AbstractHorse.java` **912–935**) |
| `JUMP_STRENGTH` base | **Yes (blended)** | Both parents | Same |
| `MOVEMENT_SPEED` base | **Yes (blended)** | Both parents | Same |
| Baby age | **Yes (forced)** | `Animal.spawnChildFromBreeding` | `ageablemob.setBaby(true)` (**228**) — not copied from a parent age value |
| World position / yaw | **Yes (initiator)** | `Animal.spawnChildFromBreeding` | `moveTo(this.getX/Y/Z, …)` (**229**) |
| Love-cause bred advancement | **Side effect on parents** | `finalizeSpawnChildFromBreeding` | Awards breed stats/criteria with baby present (**235–238**); `bred_all_animals` includes mule criterion |

### What does **not** transfer

| State | Horse side | Donkey side | Into Mule? |
|-------|------------|-------------|------------|
| Coat `Variant` / `Markings` | Horse-only `VariantHolder` NBT `"Variant"` | N/A (Donkey has none) | **No** — Horse mule branch does not call `setVariantAndMarkings` |
| `ChestedHorse` flag / inventory `Items` | Horse is **not** chested | May be chested | **No** — child starts unchested; chest is later gameplay |
| Tame / Temper / Owner UUID | May be set on parents | Same | **No** — new entity defaults |
| Saddle / BODY armor / held equipment | Horse may wear EQUESTRIAN BODY | Donkey cannot BODY | **No** |
| Passengers / vehicle linkage | Possible on parents | Same | **No** |
| Parent UUID / “hybrid ancestry” NBT | — | — | **No** dedicated parentage field on Mule |
| Sounds / EntityType dimensions | Horse dims differ | Donkey dims differ | Child uses **Mule** EntityType + Mule sounds |

### Factory inputs vs inherited biological composition

| Layer | What it is | BioCraft? |
|-------|------------|-----------|
| Factory inputs | EntityType selection `MULE`; blended attribute bases; baby flag; spawn position | Vanilla create path only |
| Inherited biological composition for BioCraft | **None.** No parent `organismKey` / `contributingSourceKey` / HostType is written onto the Mule or onto Model A from this path | Gestation writes the **host** registry path only when that host is infected later |

### BioCraft consumption of transferred state

| Candidate consumer | Reads mule factory attributes / parentage / chest / coat? | Reads mule identity? |
|--------------------|------------------------------------------------------------|----------------------|
| `BiologicalProfileResolver` | **No** | **Yes** — `organismKey` / optional `contributingSourceKey` pass-through (**35–56**) |
| `GestationManager.writeContributingSource` | **No** | **Yes** — if host is a Mule, writes `"mule"` (**164–175**) |
| `HostEligibilityService` / `MobHostRegistry` | **No** | **Yes** — `"mule"` → `LIVING_BIOLOGICAL` |
| Mule-named Analyzer / attribute / hybrid branch | **ABSENT** | N/A |

**Verdict:** Attribute blend and baby flag are **vanilla persistent entity state** after creation (**A**). They are **not** BioCraft biological composition. No named live consumer needs Horse/Donkey ancestry facts on Mule → **no C**. Do **not** invent hybrid BP from the name “mule”.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` key `"mule"` | **LIVE** | `vanilla_hosts.living_biological.mobs` includes `"mule"` (`hosts.json` **6–8**); group `default_dna: baseline_biological` (**4**) | Participation. Do **not** register/unregister. Registration ≠ extra biology. Inventory baseline → **B**, not C / not automatic A |
| Adjacent `"horse"` / `"donkey"` / `"llama"` | **LIVE** (not absorbed) | Same list (**7**) | Distinct keys. Shared list ≠ horse-family / hybrid clade |
| `"camel"` | **ABSENT** | Not in living_biological list | Negative control only |
| `variant_mappings` mule | **ABSENT** | No `"mule"` under `variant_mappings` (**47–52**) | No aggressive/neutral override |
| `MobHostRegistry.getHostType("mule")` | **LIVE** | Lookup **46–48**. After bind: `LIVING_BIOLOGICAL`. DNA id from group default | Suitability via HostType flag, not a Mule dossier |
| `HostEligibilityService` | **LIVE** generic | String/entity suitability **19–31**; facehugger gate **33–45** | Mule eligible via existing HostType. Not a Mule-specific missing-fact consumer |
| `BiologicalProfileResolver` | **LIVE** generic | **35–56**: lowercase `organismKey`; host type / DNA id; xenomorph form match; `contributingSourceKey` pass-through | `mule` resolves `organismKey=mule`, `HostType.LIVING_BIOLOGICAL`, `hostEffectProfileId=baseline_biological`, empty form/behavior. **No Mule branch** |
| Gestation `writeContributingSource` | **LIVE** | `GestationManager.java` **164–175** | Production writer of `"mule"` onto Model A carriers when host is Mule. Does **not** store Horse/Donkey parents, chest, or attributes |
| Mule-specific BioCraft gameplay JSON / Java branch | **ABSENT** | Grep under `biocraft-alien/src/main/java` for mule/Mule/MULE: **no hits** | Vanilla remains owner of Mule gameplay |

Consumer classification:

| Candidate | Classification |
|-----------|----------------|
| `BiologicalProfileResolver` | **LIVE** generic (not Mule-specific) |
| Gestation `contributingSourceKey` | **LIVE**; Mule **origin allowed** (registered + suitable) |
| `HostEligibilityService` | **LIVE** registry gate; Mule eligible via `LIVING_BIOLOGICAL` |
| `hosts.json` mule row | **LIVE** participation |
| Mule-named missing-fact consumer | **ABSENT** |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails on 1.21.1 evidence |
|----------------|--------------------------------|
| Hybrid name ⇒ invent hybrid / sterility / ancestry BP | Name ≠ biology. Factory is EntityType create. No BioCraft consumer of parentage |
| Reopen Horse “factory not ancestry” as C | Horse report **locked**. This packet treats it as settled distinct-key creation. Mule post-creation identity is independently **B** |
| `AbstractChestedHorse` / shared chest with Donkey = pack clade | Shared Java parent + container API. Mate filters and EntityTypes keep identities separate |
| Chest / saddle / jump = anatomy fields | Equipment and ride API. No BioCraft consumer |
| Attribute blend from Horse+Donkey = inherited BioCraft composition | Vanilla stat math only. Resolver/gestation ignore it |
| Live `contributingSourceKey=mule` earns C | Identity already represented — **B**, not C |
| Host Registry presence = automatic A | Registration is **B** participation for identity consumers; vanilla mechanics remain **A**. Presence does not invent facts |
| Mule can naturally breed because `getBreedOffspring` exists / advancement lists mule | `canMate` false blocks natural mating. Advancement is for **being born** via Horse+Donkey, not for Mule×Mule |
| No biome spawn ⇒ missing origin Profile | Spawn ≠ origin. Summon/egg/breed suffice as existence paths |
| Absorb Horse BODY armor / coat into Mule | Horse-only overrides; mule factory does not copy Variant; Mule cannot use BODY slot |

---

## Potential biological relationships (hypotheses only — after ownership)

### 1. Mule as live xenomorph host / Model A contributing source

- **Relationship:** Facehugger may select Mule; gestation copies host registry path onto Chestburster; resolver/Analyzer project it.
- **Owner:** `hosts.json` + `HostEligibilityService` + `GestationManager.writeContributingSource` + `BiologicalProfileResolver`.
- **Biological input?** Only the organism-definition key `"mule"`.
- **Existing composition:** `organismKey=mule`; optional `contributingSourceKey=mule`; `HostType.LIVING_BIOLOGICAL` + `hostEffectProfileId=baseline_biological`.
- **Named consumer?** **LIVE** — eligibility, gestation writer, generic resolver. **No** Mule-named missing-fact consumer.
- **Result:** **B**. Live `contributingSourceKey=mule` is identity already represented. Not C.

### 2. Horse ↔ Donkey factory producing Mule

- **Relationship:** Mutual `canMate` on Horse/Donkey; offspring EntityType `MULE`; attribute blend into child.
- **Owner:** `Horse.java` **173–190**; `Donkey.java` **48–70**; `AbstractHorse.setOffspringAttributes`.
- **Biological input?** Vanilla cross-type birth. Distinct-key factory (Horse locked). Do not absorb Horse/Donkey.
- **Existing composition:** Distinct registered keys already.
- **Named consumer?** None for hybrid ancestry / sterility / attribute-blend BP.
- **Result:** **A/B** (factory A; child identity B). **No C.**

### 3. Mule ↔ Donkey “chested horse” column

- **Relationship:** Shared `AbstractChestedHorse` chest inventory.
- **Owner:** Class hierarchy + chest flag.
- **Biological input?** Shared parent ≠ clade.
- **Named consumer?** None.
- **Result:** **A**. Reject pack-animal clade.

### 4. Mule natural sterility

- **Owner:** Absent `canMate` override → `AbstractHorse.canMate` false.
- **Biological input?** Vanilla mate gate.
- **Named consumer?** None for a fertility Profile.
- **Result:** **A**.

### 5. Chest / saddle / jump as anatomy

- **Owner:** `AbstractChestedHorse` / `AbstractHorse`.
- **Named consumer?** None in BioCraft.
- **Result:** **A**.

**C is not earned for any relationship.**

---

## Wiki disagreements

Wiki was **not** treated as authority. Source-owned Mule facts that commonly disagree with orientation text:

| Orientation claim | 1.21.1 authority | Conclusion |
|-------------------|------------------|------------|
| Mules breed / produce more mules in survival | `AbstractHorse.canMate` false; no Mule override | **No natural breed path** |
| Mule inherits Horse coat / armor | Factory does not copy Variant; BODY slot closed | **No** |
| Mule chest differs mechanically from Donkey | Same columns/API; sound + EntityType dims differ | Treat as **same chest owner**, distinct identity |
| Carrot is mule food | `#horse_food` has **no** ordinary carrot | **Exclude** ordinary carrot |
| Wild mule biome spawns | No worldgen creature entries | Summon / egg / Horse+Donkey only (plus placement rules for those) |
| Hybrid BP needed because name is hybrid | No BioCraft consumer of parentage | **Reject** invented hybrid field |

---

## Final evidence conclusion

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** (`organismKey=mule`; optional `contributingSourceKey=mule`; HostType + `baseline_biological`) |
| Named consumer exists | **YES** (live host/gestation/resolver identity-source path). **NO** named consumer of a **missing** Mule biological fact |
| Architectural escalation required | **NO** |

Mule is a 1.21.1 `AbstractChestedHorse` creature identity (`minecraft:mule`). After creation, Minecraft owns chest gameplay, taming, saddle/riding, food/tempt (via horse_* tags), **sterility** (no `canMate` override), water/dismount tags, sounds, loot, and (for breed-created instances) blended health/jump/speed bases. BioCraft already registers `mule` as `LIVING_BIOLOGICAL` / `baseline_biological` and can write `contributingSourceKey=mule` on Model A carriers. That consumer asks only for the existing organism-definition key. Horse+Donkey→Mule remains a **distinct-key factory** (Horse conclusion not reopened as C); transferred factory stats are not BioCraft composition.

**Stop.** A = vanilla ownership; B = existing identity/composition including live Model A source identity; C = not earned. Do **not** change Host Registry. Do **not** mint a Mule/hybrid/sterility/chest/pack Profile. Do **not** absorb Horse/Donkey/Camel/Llama. Live `contributingSourceKey=mule` is **B**, not C. Do **not** mint `DESIGN-BIO-MANIFEST-004`.

### A/B/C summary

- **A:** chest gameplay (vs Donkey: same API, different chest sound), `canGallop=false`, taming/temper, saddle/riding/jump, BODY-armor absence, food/tempt, **no natural mate path**, Horse/Donkey→Mule EntityType factory + attribute blend + baby/placement, goals/grass, non-breed attribute randomize, water/dismount tags, absent biome spawn, sounds, loot.
- **B:** `organismKey=mule` (LIVE registered); `HostType.LIVING_BIOLOGICAL`; `hostEffectProfileId=baseline_biological`; optional Model A `contributingSourceKey=mule` (identity only).
- **C:** **none.**

### Overall classification

**B** (registered live identity consumers of `mule`; no missing-fact C; vanilla post-creation mechanics A).

### UNKNOWN facts

| Probe | Status |
|-------|--------|
| Phase 1 gate sources (`Mule`, `Horse`, `Donkey`, `AbstractChestedHorse`, `AbstractHorse`, EntityType, DefaultAttributes, loot, tags, BioCraft hosts/resolver/gestation/eligibility/registry) | **Present** — **no UNKNOWN** required for this packet |
| Whether NeoForge `BabyEntitySpawnEvent` listeners elsewhere rewrite mule children | **Out of scope / not probed** in AlienCraft main tree for mule-specific rewrites (no mule Java hits). Not treated as a BioCraft missing-fact UNKNOWN |
| Post-1.21.1 mule changes | **Out of range** (not UNKNOWN within 1.21.1 scope) |

### 1.21.1 authority anchors (files actually read)

- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/Mule.java`
- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/Donkey.java`
- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/Horse.java` (factory / mate symmetry only — Horse conclusion not reopened)
- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/AbstractChestedHorse.java`
- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/AbstractHorse.java` (`canMate`, `canParent`, `setOffspringAttributes`, food/goals)
- `.tmp_mc_sources/net/minecraft/world/entity/animal/Animal.java` (`spawnChildFromBreeding`)
- `.tmp_mc_sources/net/minecraft/world/entity/ai/goal/BreedGoal.java`
- `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` **506–509**
- `.tmp_mc_sources/net/minecraft/world/entity/ai/attributes/DefaultAttributes.java` **107**, **129**
- `.tmp_mc_sources/data/minecraft/loot_table/entities/mule.json`
- `.tmp_mc_sources/data/minecraft/tags/item/horse_food.json`, `horse_tempt_items.json`
- `.tmp_mc_sources/data/minecraft/tags/entity_type/dismounts_underwater.json`
- `.tmp_mc_sources/data/minecraft/advancement/husbandry/bred_all_animals.json` (mule criterion — born, not Mule×Mule)
- `implementations/minecraft/AlienCraft/biocraft-alien/src/main/resources/data/biocraft_alien/systems/hosts.json`
- `HostEligibilityService.java`; `GestationManager.writeContributingSource` (**164–175**); `BiologicalProfileResolver.java`; `MobHostRegistry.java`

Adjacency-only (not copied as Mule biology): `.tmp_manifestation_evidence/horse.md`, `donkey.md`.
