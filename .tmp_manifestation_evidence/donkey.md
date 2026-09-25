TEMPORARY EVIDENCE — NOT PROJECT SSOT

Do not treat this file as canonical design documentation.
Do not promote into manifestations/donkey.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Donkey — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register or unregister Donkey as a conclusion of this investigation.** Donkey is already in `vanilla_hosts.living_biological`. Registration is participation, not extra biology.

Method (every behavior): owner → meaningful biological input? → existing composition? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied independently: `AbstractHorse` / `AbstractChestedHorse` ≠ clade; shared HostType / `hosts.json` list ≠ clade; hybrid name (Mule) ≠ ancestry; spawn ≠ origin; tag ≠ clade; Host Registry presence ≠ automatic A (presence is participation; classify per consumer); interesting chest/pack behavior ≠ consumer.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey` (Model A Chestburster/Drone), optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

**Default: NO new BP field.** Horse / Mule / Camel / Llama / Trader Llama are **not absorbed**. Prior adjacency (`implementations/minecraft/AlienCraft/docs/design/biological/manifestations/horse.md`, temp `.tmp_manifestation_evidence/horse.md`) used only as claim checklists — every Donkey owner below was re-read from 1.21.1 mapped sources. Horse’s locked Horse+Donkey→Mule **distinct-key factory** is **cross-checked**, not reopened as C for Horse.

---

## Phase 1 gate

| Required artifact | Status |
|-------------------|--------|
| `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/Donkey.java` | **PRESENT** |
| `AbstractChestedHorse.java` | **PRESENT** |
| `AbstractHorse.java` | **PRESENT** |
| `Horse.java` | **PRESENT** |
| Related loot/tags/biomes under `.tmp_mc_sources/data/` | **PRESENT** (`loot_table/entities/donkey.json`; `#horse_food` / `#horse_tempt_items`; `#dismounts_underwater`; biome creature lists) |
| BioCraft `hosts.json` | **PRESENT** — `implementations/minecraft/AlienCraft/biocraft-alien/src/main/resources/data/biocraft_alien/systems/hosts.json` |
| `BiologicalProfileResolver` | **PRESENT** — `.../layer_2_systems/level_0/biology/BiologicalProfileResolver.java` |
| Analyzer path | **PRESENT** — `BoundaryBootstrap` wires `BiologicalProfileDnaAnalysisPort(new BiologicalProfileResolver())` into `DnaAnalysisServices` |
| Gestation `contributingSourceKey` path | **PRESENT** — `GestationManager.writeContributingSource` (**164–175**) |

No gate probe marked UNKNOWN from superclass inference.

---

## Subject

Donkey (`minecraft:donkey`) — living Donkey identity on Minecraft Java **1.21.1**. Scope: EntityType registration, `Donkey` / `AbstractChestedHorse` / `AbstractHorse` gameplay owners, chest inventory flag, food/tempt (via AbstractHorse + `#horse_food` / `#horse_tempt_items`), plains/savanna/meadow spawn placement, Host Registry `living_biological`, BioCraft identity routing (`HostEligibilityService`, `GestationManager.writeContributingSource`, `BiologicalProfileResolver` / Analyzer), and a **mandatory separate reproduction probe** (mate eligibility, parent combinations, offspring EntityType selection, attribute state transfer).

Out of scope as organisms: Horse, Mule, Camel, Llama, Trader Llama, Skeleton Horse, Zombie Horse. Those types appear only as **negative controls** / mate-symmetry / offspring-factory endpoints.

---

## Version

Minecraft Java **1.21.1** only. Mapped sources in `.tmp_mc_sources/` are authoritative. Wiki is orientation / disagreement discovery only; **source wins**.

Post-1.21.1 mount UI / later food changes are **out of range**.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:donkey` |
| `EntityType` | `EntityType.DONKEY` — `EntityType.java` **279–286**: `register("donkey", Builder.of(Donkey::new, MobCategory.CREATURE).sized(1.3964844F, 1.5F).eyeHeight(1.425F).passengerAttachments(1.1125F).clientTrackingRange(10))` |
| Fire / lava | DONKEY builder does **not** call `.fireImmune()` |
| Class | `Donkey extends AbstractChestedHorse` (`Donkey.java` **13**). `AbstractChestedHorse extends AbstractHorse` (`AbstractChestedHorse.java` **26**). `AbstractHorse extends Animal` (+ ride/saddle/ownable interfaces) |
| Category | `MobCategory.CREATURE` |
| Dimensions | Adult **1.3964844 × 1.5**, eyeHeight **1.425**, passengerAttachments **1.1125F**. Baby: `AbstractChestedHorse` builds scaled baby dims with passenger attach at `height - 0.15625F`, scale **0.5** (`AbstractChestedHorse.java` **33–35**, **62–64**) |
| Contrast (not absorbed) | Horse adult height **1.6** / eyeHeight **1.52** / passengerAttachments **1.44375F**. Mule adult height **1.6** / eyeHeight **1.52** / passengerAttachments **1.2125F** (`EntityType.java` mule **506–509**) — distinct registration literals |
| Default attributes | `DefaultAttributes` maps `EntityType.DONKEY` → `AbstractChestedHorse.createBaseChestedHorseAttributes()` (`DefaultAttributes.java` **106**): base horse attrs + movement **0.175F**, jump **0.5** (`AbstractChestedHorse.java` **49–51**). Spawn randomizes **only** `MAX_HEALTH` via `generateMaxHealth` (**39–41**) |
| Host Registry | **REGISTERED.** `hosts.json` `vanilla_hosts.living_biological.mobs` includes `"donkey"` (**6–8**). Group `default_dna`: `baseline_biological` (**4**). `MobHostRegistry.getHostType("donkey")` → `HostType.LIVING_BIOLOGICAL`. `isSuitableForXenomorph("donkey")` → **true**. `variant_mappings` has **no** donkey entry (**47–52**) |
| Suitability | Registered `LIVING_BIOLOGICAL` → currently suitable for xenomorph hosting. Registered ≠ extra biology ≠ BP field |

Independent existence paths (not origin): `/summon` / spawn egg (summonable by default builder), biome creature lists, `Donkey.getBreedOffspring` (Donkey+Donkey → Donkey).

Negative-control identities (not investigated as organisms):

| Type | 1.21.1 fact | Use here |
|------|-------------|----------|
| `EntityType.HORSE` | Mate-eligible partner; Horse→Donkey offspring is `MULE` | Cross-breed **factory** only. Do not absorb |
| `EntityType.MULE` | Offspring when other parent is Horse; Mule does **not** override `canMate` → inherits `AbstractHorse.canMate` **false** (sterile gate) | Distinct key. Hybrid name ≠ Donkey ancestry |
| Camel / Llama | Separate EntityTypes; not Donkey `canMate` partners | Reject pack-animal / AbstractHorse clade |

---

## Behavior ownership table

Columns include **refined manifestation classification** (`identity` | `persistent entity state` | `transient gameplay state` | `environmental interaction` | `item/block production` | `effect application` | `entity/state transformation` | `actual biological input consumed by BioCraft`).

| Behavior | Refined manifestation classification | Actual owner | 1.21.1 evidence | Biological input? | Existing composition? | Named BioCraft consumer? | A/B/C |
|----------|--------------------------------------|--------------|-----------------|-------------------|----------------------|--------------------------|-------|
| Identity / size / category | **identity** | `EntityType.DONKEY` | `EntityType.java` **279–286**: `"donkey"`, `CREATURE`, 1.3964844×1.5, eyeHeight 1.425, passengerAttachments 1.1125 | Identity only | `organismKey = donkey` (registered) | Generic resolver / Analyzer identity. **No** Donkey-specific branch | **B** |
| Java type (`AbstractChestedHorse`) | **identity** (implementation reuse ≠ biology) | `Donkey` class | `Donkey.java` **13**. Does **not** extend Horse, Mule, Camel, or Llama | Shared parent ≠ clade | Distinct key already | None for ancestry | **A/B** |
| Chest flag / inventory columns | **persistent entity state** + **item/block production** (chest block drop) | `AbstractChestedHorse` | Synched `DATA_ID_CHEST` (**27**, **53–58**). NBT `"ChestedHorse"` + `"Items"` (**79–116**). Equip `Items.CHEST` in `mobInteract` (**167–170**, **179–184**). `getInventoryColumns` → **5** if chested else **0** (**191–193**). Drop chest block on death (**67–75**). Equip sound `DONKEY_CHEST` (**186–188**) | **No.** Item/equipment + container gameplay | Identity sufficient | None that reads chest as anatomy | **A** |
| `canGallop = false` | **transient gameplay state** | `AbstractChestedHorse` ctor | Sets `this.canGallop = false` (**32**) | Ride/animation flag. Not anatomy | Identity sufficient | None | **A** |
| Taming / temper / owner | **persistent entity state** | `AbstractHorse` | Flags `FLAG_TAME=2`; NBT `"Tame"` / `"Temper"` / `"Owner"`; max temper **100**; `RunAroundLikeCrazyGoal`; feeding `modifyTemper` | **No.** Ride/temper entity state | Identity sufficient | None | **A** |
| Saddle / riding / jump | **transient gameplay state** (+ equipment) | `AbstractHorse` + `Saddleable` | `isSaddleable` = alive + adult + tamed (**253–255**). Controlling passenger requires saddle (`getControllingPassenger` **1078–1087**). Jump via `PlayerRideableJumping`; Donkey overrides jump sound (`Donkey.java` **57–59**) | Equipment + ride API | Identity sufficient | None | **A** |
| BODY / EQUESTRIAN armor | **transient gameplay state** (equipment refusal) | **ABSENT on Donkey** | `Mob.canUseSlot` returns `slot != BODY` (**931–933**). Donkey/AbstractChestedHorse do **not** override (Horse does). `Mob.isBodyArmorItem` default **false** (**939–941**) | Equipment gate. Contrast with Horse only — do not absorb Horse armor | Not an armor-capability field | None | **A** |
| Untamed / chested interact | **transient gameplay state** | `AbstractChestedHorse.mobInteract` then `AbstractHorse` | Food → `fedFood`. Untamed + non-food → `makeMad` (**162–165**). Tamed + CHEST → equip. Else `super` → ride (`AbstractHorse` **728–729**) | Ride/tame/chest owners | Identity sufficient | None | **A** |
| Food / tempt / love | **environmental interaction** | `AbstractHorse` + item tags | `isFood` = `#minecraft:horse_food` (**575–577**; wheat/sugar/hay_block/apple/golden_carrot/golden_apple/enchanted_golden_apple — **no carrot**). Tempt: `#horse_tempt_items` golden carrot/apple/enchanted apple (`addBehaviourGoals` **177–179**). Love: golden carrot / golden apple / enchanted golden apple if tamed, age 0, not in love (`handleEating` **512–528**) | Food tag ≠ diet trait. Shared tag name ≠ Horse clade | Identity sufficient | None | **A** |
| Mate eligibility | **entity/state transformation** (breeding gate) | `Donkey.canMate` (+ Horse symmetry) | Self rejected; other must be `Donkey` **or** `Horse`; both `canParent()` (`Donkey.java` **48–54**). Horse mirror (`Horse.java` **173–178**). `canParent`: tamed, adult, full health, in love, not vehicle/passenger (`AbstractHorse.java` **902–904**). `BreedGoal` still calls `canMate` (`BreedGoal.java` **72**) | Vanilla mate gate. Cross-type eligibility ≠ shared ancestry BP | Distinct keys | None for a hybrid-eligibility field | **A** |
| Offspring EntityType selection | **entity/state transformation** (creation) | `Donkey.getBreedOffspring` / `Horse.getBreedOffspring` | Donkey: `otherParent instanceof Horse ? MULE : DONKEY` then `create` + `setOffspringAttributes` (`Donkey.java` **63–70**). Horse: Donkey partner → `MULE`; else Horse+coat lottery (`Horse.java` **183–220**) | **Reproduction/creation mechanic** (EntityType factory). Not inherited composition unless a live BioCraft consumer requires it — **none does** | Child Donkey = `donkey`; Mule = **different** key | None that needs breed/hybrid BP | **A/B** |
| Offspring attribute transfer | **persistent entity state** (child stats) | `AbstractHorse.setOffspringAttributes` | Blends `MAX_HEALTH`, `JUMP_STRENGTH`, `MOVEMENT_SPEED` within min/max clamps (**912–916**). **No** chest flag / inventory / tame / saddle copy in this path | Transient breeding math → child entity attributes | Identity sufficient | None | **A** |
| Foal / spawn group | **persistent entity state** (age) + spawn math | `AbstractHorse.finalizeSpawn` | If no group data: `AgeableMobGroupData(0.2F)` then `randomizeAttributes` (**1144–1150**). Donkey does **not** supply Horse-style always-adult group data | Age/spawn-group state | Entity baby flag | None | **A** |
| Goals / grass | **environmental interaction** + AI | `AbstractHorse.registerGoals` | Panic, crazy-run, `BreedGoal(..., AbstractHorse.class)`, follow parent, water-avoiding stroll, look, random look, optional stand (**162–175**). Donkey does **not** override `addBehaviourGoals` → Float + Tempt. `canEatGrass()` true | AI. Shared parent helper ≠ clade | Identity sufficient | None | **A** |
| Attributes | **persistent entity state** (stats) | `createBaseChestedHorseAttributes` + health randomize | Jump **0.5**, movement **0.175F**, step/fall from base horse attrs; spawn overwrites health only (**39–41**, **49–51**) | Stats, not anatomy BP | Identity sufficient | None | **A** |
| Water / dismount | **environmental interaction** | Entity-type tags + defaults | Donkey **is** in `#dismounts_underwater`. Donkey **is not** in `#undead` (entity_type tag grep: only dismounts_underwater). Has `FloatGoal` | Tag ≠ clade | Distinct key | Vanilla `Entity.dismountsUnderwater`, not BioCraft | **A** |
| Biome spawn | **environmental interaction** | Worldgen creature lists | `plains.json` / `sunflower_plains.json`: weight **1**, min 1, max 3. `savanna` / `savanna_plateau` / `windswept_savanna`: weight **1**, min 1, max 1. `meadow.json`: weight **1**, min 1, max 2. Same plains list also has horse — **adjacency**, not clade | **No.** Encounter placement. Spawn ≠ origin | Not an origin field | None | **A** |
| Sounds | **transient gameplay state** (presentation) | `Donkey` overrides | Ambient/angry/death/eat/hurt/jump → `SoundEvents.DONKEY_*` (`Donkey.java` **19–42**, **57–59**). Chest equip sound on AbstractChestedHorse uses `DONKEY_CHEST` | Presentation | Identity sufficient | None | **A** |
| Loot | **item/block production** | Vanilla loot table | `loot_table/entities/donkey.json`: leather 0–2 + looting. Inventory/chest drop via `AbstractChestedHorse.dropEquipment` / `AbstractHorse.dropEquipment` | Drops ≠ anatomy | Not needed | None | **A** |
| Host Registry / gestation / Analyzer | **actual biological input consumed by BioCraft** (**identity** key only) | `hosts.json` + eligibility + `writeContributingSource` + resolver | `"donkey"` in `living_biological`; HostType `LIVING_BIOLOGICAL`; suitability **true**; `default_dna` `baseline_biological`. After Chestburster spawn: encode host id → registry path → `setContributingSourceKey` (`GestationManager.java` **164–175**). Resolver passes `organismKey` + optional `contributingSourceKey` (`BiologicalProfileResolver.java` **35–56**) | Identity routing only. **Not** donkey-anatomy / chest / mule-factory | `organismKey=donkey` + optional `contributingSourceKey=donkey` + HostType + `hostEffectProfileId=baseline_biological` | **LIVE** production writer / resolver / Analyzer port. Not a Donkey-named unit test | **B** |

**No row is C.** Live `contributingSourceKey=donkey` is identity already represented — **B**, not C. Host Registry participation is **B**, not automatic A and not C. No **effect application** row earned for Donkey (no Donkey-owned status effect).

---

## Mandatory reproduction probe (separate traces)

### 1. Mate eligibility

| Path | Owner | Fact |
|------|-------|------|
| Donkey → other | `Donkey.canMate` **48–54** | Reject self. Accept only `instanceof Donkey` **or** `instanceof Horse`, and both `canParent()` |
| Horse → Donkey (symmetry) | `Horse.canMate` **173–178** | Same gate mirrored |
| Shared parent gate | `AbstractHorse.canParent` **902–904** | Tamed, not baby, full health, in love, not vehicle/passenger |
| Default AbstractHorse | `AbstractHorse.canMate` **898–900** | Returns **false** — subclasses must opt in |
| BreedGoal still respects gate | `BreedGoal.java` **72** | Targets may be `AbstractHorse.class`, but mating requires `canMate` |

**Biological input?** No. Vanilla love/tame/age gate.

### 2. Parent combinations

| Combination | Eligible? | Who decides |
|-------------|-----------|-------------|
| Donkey × Donkey | **Yes** | Either parent's `canMate` |
| Donkey × Horse | **Yes** | Either parent's `canMate` |
| Donkey × Mule / Camel / Llama / other | **No** | Failed `instanceof` filters |
| Mule × anyone | **No** | Mule does not override `canMate` → AbstractHorse default **false** (sterility gate; Mule not absorbed as organism) |

### 3. Offspring EntityType selection

| Caller | Other parent | Created type | Evidence |
|--------|--------------|--------------|----------|
| `Donkey.getBreedOffspring` | `Horse` | `EntityType.MULE` | `Donkey.java` **64** |
| `Donkey.getBreedOffspring` | `Donkey` (else branch) | `EntityType.DONKEY` | **64** |
| `Horse.getBreedOffspring` | `Donkey` | `EntityType.MULE` | `Horse.java` **184–190** |
| `Horse.getBreedOffspring` | `Horse` | `EntityType.HORSE` (+ coat lottery) | **191–220** — Horse-only; not Donkey biology |

**Established:** Donkey×Donkey → Donkey; Donkey×Horse → Mule (either caller). Cross-check with Horse report: Horse+Donkey→Mule remains a **distinct-key factory** — **A/B**, not C for Horse or Donkey.

**Classification:** offspring EntityType selection is a **reproduction/creation mechanic**. It is **not** “inherited composition” for BioCraft unless a live consumer requires breed ancestry — **ABSENT**. Do **not** absorb Mule as Donkey biology. Hybrid name ≠ ancestry.

### 4. State transfer

| Transferred | Owner | Fact |
|-------------|-------|------|
| `MAX_HEALTH` / `JUMP_STRENGTH` / `MOVEMENT_SPEED` | `AbstractHorse.setOffspringAttributes` **912–916** | Blended within clamp ranges |
| Chest / inventory / ChestedHorse | **Not** transferred by breed path | Child starts without chest unless later equipped |
| Tame / saddle / temper / owner | **Not** transferred by this create path | New entity defaults |
| Coat/variant | N/A on Donkey | Donkey has no Horse `VariantHolder` |

**A/B/C for reproduction block:** **A** (vanilla factory + attribute blend). Child Donkey identity remains **B** via `organismKey=donkey`. Mule factory endpoint is a **distinct key** — adjacency only. **No C.**

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` key `"donkey"` | **LIVE** | `vanilla_hosts.living_biological.mobs` includes `"donkey"` (`hosts.json` **6–8**); group `default_dna: baseline_biological` (**4**) | Participation. Do **not** register/unregister in this pass. Registration ≠ extra biology. Participation → **B**, not C |
| Adjacent `"horse"` / `"mule"` / `"llama"` | **LIVE** (not absorbed) | Same `living_biological` list (**7**) | Distinct keys. Shared list ≠ pack-animal / horse-family clade |
| `"camel"` | **ABSENT** | Not in living_biological list | Negative control only — do not absorb |
| Tags: `#horse_food` / `#horse_tempt_items` | **LIVE** vanilla | Item tag JSON under `.tmp_mc_sources/data/minecraft/tags/item/` | Shared AbstractHorse food/tempt — tag ≠ clade |
| Tag: `#dismounts_underwater` | **LIVE** | Includes `minecraft:donkey` | Tag ≠ clade |
| Loot `entities/donkey.json` | **LIVE** | Leather 0–2 + looting | Drops ≠ anatomy |
| Spawn biomes | **LIVE** | plains, sunflower_plains, savanna, savanna_plateau, windswept_savanna, meadow | Encounter ≠ origin |
| `variant_mappings` donkey | **ABSENT** | No `"donkey"` under `variant_mappings` (**47–52**) | No aggressive/neutral override |
| `MobHostRegistry.getHostType("donkey")` | **LIVE** | Lookup **46–48**. After bind: `LIVING_BIOLOGICAL`. DNA id from group default | Suitability true via `HostType` flag, not a Donkey dossier |
| `HostEligibilityService` | **LIVE** generic | `isSuitableForXenomorph(String)` **19–21** delegates to `MobHostRegistry`. Entity overload **23–31** uses `encodeId` → `HostRegistryPaths.registryPath`. `isValidFacehuggerHost` **33–45** | Donkey eligible via existing HostType. Not a Donkey-specific consumer of missing biology |
| `BiologicalProfileResolver` / Analyzer | **LIVE** generic | Resolver **35–56**; Analyzer wired in `BoundaryBootstrap` **59–60** | `donkey` resolves `organismKey=donkey`, `HostType.LIVING_BIOLOGICAL`, `hostEffectProfileId=baseline_biological`, empty form/behavior. **No Donkey branch** |
| Gestation `writeContributingSource` | **LIVE** | `GestationManager.java` **164–175**: registry path of the **host** onto Chestburster if port `supports` | Production writer of `"donkey"` onto Model A carriers. Does **not** store chest, mule-factory, taming, or attributes |
| Donkey-specific BioCraft gameplay JSON / Java branch | **ABSENT** from the listed consumers | Resolver/eligibility/gestation/Analyzer are generic | Vanilla remains owner of Donkey gameplay |

Consumer classification:

| Candidate | Classification |
|-----------|----------------|
| `BiologicalProfileResolver` | **LIVE** generic (not Donkey-specific) |
| DNA Analyzer port | **LIVE** generic via resolver |
| Gestation `contributingSourceKey` | **LIVE**; Donkey **origin allowed** (registered + suitable) |
| `HostEligibilityService` | **LIVE** registry gate; Donkey eligible via `LIVING_BIOLOGICAL` |
| `hosts.json` donkey row | **LIVE** participation |
| Donkey-named missing-fact consumer | **ABSENT** |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails on 1.21.1 evidence |
|----------------|--------------------------------|
| `AbstractHorse` / `AbstractChestedHorse` is a pack-animal / horse-family clade | Shared **Java parents**. Donkey `canMate` accepts only Donkey or Horse. Camel/Llama are different EntityTypes and not mate partners. Parent ≠ clade |
| Chest is Donkey anatomy → new BP field | `DATA_ID_CHEST` + CHEST item equip + inventory columns. Equipment/container state. **No** BioCraft consumer of chest anatomy |
| Absorb Horse conclusions (armor, coat, plains-as-horse-biology) as Donkey | Horse BODY armor / variants are **Horse overrides**. Donkey does not wear EQUESTRIAN armor; has no VariantHolder. Re-traced from Donkey owners only |
| Absorb Mule as Donkey biology because hybrid name | `EntityType.MULE` is a cross-breed **factory** product. Distinct registered key. Hybrid name ≠ ancestry |
| Shared `#horse_food` / `#horse_tempt_items` proves horse-family diet clade | Tag reused by AbstractHorse `isFood` / TemptGoal. Tag ≠ clade / diet BP |
| Plains co-spawn with Horse proves related origin | Worldgen adjacency. Spawn ≠ origin. Donkey also in savanna/meadow lists |
| Host Registry co-listing with horse/mule/llama = clade | Shared suitability list. List ≠ biology |
| Host Registry presence = automatic A | Presence is participation; vanilla owners are A; live identity consumer is **B** |
| Live `contributingSourceKey=donkey` earns C | Identity already represented — **B**, not C |
| Mule offspring needs inherited BioCraft composition field | No named live consumer of breed ancestry. EntityType factory is A |
| Reopen Horse+Donkey→Mule as C for Horse | Locked Horse report: distinct-key factory. Cross-check confirms; do not escalate |

---

## Potential biological relationships (evidence-grounded only)

### 1. Donkey as live xenomorph host / Model A contributing source

- **Relationship:** Facehugger may select Donkey; gestation copies host registry path onto Chestburster; resolver/Analyzer project it.
- **Owner:** `hosts.json` + `HostEligibilityService` + `GestationManager.writeContributingSource` + `BiologicalProfileResolver`.
- **Biological input?** Only the organism-definition key `"donkey"`.
- **Existing composition:** `organismKey=donkey`; optional `contributingSourceKey=donkey`; `HostType.LIVING_BIOLOGICAL` + `hostEffectProfileId=baseline_biological`.
- **Named consumer?** **LIVE** — eligibility, gestation writer, generic resolver/Analyzer. **No** Donkey-named missing-fact consumer.
- **Result:** **B**. Live `contributingSourceKey=donkey` is identity already represented. Not C.

### 2. Donkey ↔ Horse / Mule (cross-breed factory)

- **Relationship:** Mutual `canMate`; offspring may be `EntityType.MULE` when partners are mixed Donkey+Horse; Donkey×Donkey → Donkey.
- **Owner:** `Donkey.java` **48–70**; `Horse.java` **173–190** (symmetry / other-side factory).
- **Biological input?** Vanilla cross-type birth. Do not absorb Horse/Mule.
- **Existing composition:** Distinct registered keys already.
- **Named consumer?** None for a mule-hybrid BP field.
- **Result:** **A/B**.

### 3. Donkey ↔ Camel / Llama / AbstractChestedHorse “pack” column

- **Relationship:** Shared Java parents / chest helper class with Mule/Llama; Camel is AbstractHorse but not a mate partner.
- **Owner:** Class hierarchy only. **No** Donkey `canMate` with Camel/Llama.
- **Biological input?** Shared parent ≠ clade.
- **Named consumer?** None for a pack-animal field.
- **Result:** **A**. Reject pack-animal clade.

### 4. Chest / saddle / jump as anatomy

- **Owner:** `AbstractChestedHorse` chest; `AbstractHorse` saddle/jump.
- **Biological input?** Equipment and ride API.
- **Named consumer?** None in BioCraft.
- **Result:** **A**.

### 5. Biome encounter (plains / savanna / meadow)

- **Owner:** worldgen creature lists (weights above).
- **Biological input?** No. Spawn ≠ origin.
- **Named consumer?** None.
- **Result:** **A**.

**C is not earned for any relationship.**

---

## Wiki disagreements (orientation only)

Wiki was **not** treated as authority. Source-owned Donkey facts that commonly disagree with orientation text:

| Orientation claim (wiki) | 1.21.1 authority | Conclusion |
|--------------------------|------------------|------------|
| Carrot is Donkey food | `#horse_food` has **no** carrot (golden carrot only among carrot-named items) | **Exclude** ordinary carrot |
| Donkey wears horse armor | `Mob.canUseSlot` denies BODY; Donkey does not override like Horse | Living Donkey **cannot** use EQUESTRIAN BODY armor |
| Donkey+Horse → mule; Donkey+Donkey → donkey | `Donkey.getBreedOffspring` / Horse symmetry | **Agrees** |
| Health randomization like Horse (speed/jump too) | AbstractChestedHorse randomizes **health only**; jump/speed stay at chested base (**0.5** / **0.175F**) | Do not copy Horse `randomizeAttributes` triad onto Donkey |
| Plains-only spawn | Also savanna variants + meadow | Cite **all** biome JSON hits |
| Pack-animal family with camel/llama | Mate filter + distinct EntityTypes | Keep identities separate |

---

## Final evidence conclusion

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** (`organismKey=donkey`; optional `contributingSourceKey=donkey`; HostType + `baseline_biological`) |
| Named consumer exists | **YES** (live host/gestation/resolver/Analyzer identity-source path). **NO** named consumer of a **missing** Donkey biological fact |
| Architectural escalation required | **NO** |

Donkey is a 1.21.1 `AbstractChestedHorse` creature identity (`minecraft:donkey`). Minecraft owns chest gameplay, taming, saddle/riding, food/tempt (via horse_* tags), breeding (including Mule factory), spawn, water/dismount tags, sounds, and loot. BioCraft already registers `donkey` as `LIVING_BIOLOGICAL` / `baseline_biological` and can write `contributingSourceKey=donkey` on Model A carriers. That consumer asks only for the existing organism-definition key.

**Stop.** A = vanilla ownership; B = existing identity/composition including live Model A source identity; C = not earned. Do **not** change Host Registry. Do **not** mint a Donkey/chest/pack-animal/mule-hybrid Profile. Do **not** absorb Horse/Mule/Camel/Llama. Live `contributingSourceKey=donkey` is **B**, not C. Do **not** mint `DESIGN-BIO-MANIFEST-004`.

### Explicit A/B/C per interesting mechanic

| Mechanic | A/B/C |
|----------|-------|
| EntityType / dimensions / CREATURE | **B** |
| `AbstractChestedHorse` / `AbstractHorse` parent | **A/B** (reuse ≠ clade) |
| Chest inventory gameplay | **A** |
| Taming / temper / owner | **A** |
| Saddle / ride / jump | **A** |
| BODY armor absence | **A** |
| `#horse_food` / tempt / love | **A** |
| Mate eligibility Donkey↔Donkey / Donkey↔Horse | **A** |
| Offspring EntityType (Donkey vs Mule factory) | **A/B** |
| Attribute blend on foal | **A** |
| Biome spawn / dismount tag / loot / sounds | **A** |
| Host Registry + gestation `contributingSourceKey` + resolver/Analyzer | **B** |
| Missing-fact consumer (any) | **C not earned** |

### Overall organism conclusion

**Overall: A + B; C not earned.** Vanilla owns gameplay; existing identity composition satisfies live BioCraft consumers.

### UNKNOWN facts

| Probe | Status |
|-------|--------|
| Required Phase 1 sources / BioCraft consumer paths listed above | **Present** — **no UNKNOWN** required for this packet |
| Whether any unshipped / disabled BioCraft branch would later consume mule-factory ancestry as composition | **UNKNOWN** beyond live tree (no live consumer found). Not a license to invent a field now |
| Post-1.21.1 donkey changes | **Out of range** (not UNKNOWN within 1.21.1 scope) |

### 1.21.1 authority anchors (files actually read)

- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/Donkey.java`
- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/AbstractChestedHorse.java`
- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/AbstractHorse.java`
- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/Horse.java` (mate symmetry / mule factory only)
- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/Mule.java` (sterility / offspring stub negative control only)
- `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` **279–286**, mule **506–509**
- `.tmp_mc_sources/net/minecraft/world/entity/ai/attributes/DefaultAttributes.java` **106**
- `.tmp_mc_sources/net/minecraft/world/entity/Mob.java` **931–941** (BODY slot default)
- `.tmp_mc_sources/net/minecraft/world/entity/ai/goal/BreedGoal.java` **72**
- `.tmp_mc_sources/data/minecraft/loot_table/entities/donkey.json`
- `.tmp_mc_sources/data/minecraft/tags/item/horse_food.json`, `horse_tempt_items.json`
- `.tmp_mc_sources/data/minecraft/tags/entity_type/dismounts_underwater.json`
- `.tmp_mc_sources/data/minecraft/worldgen/biome/plains.json`, `sunflower_plains.json`, `savanna.json`, `savanna_plateau.json`, `windswept_savanna.json`, `meadow.json`
- `implementations/minecraft/AlienCraft/biocraft-alien/src/main/resources/data/biocraft_alien/systems/hosts.json`
- `HostEligibilityService.java`; `GestationManager.writeContributingSource` (**164–175**); `BiologicalProfileResolver.java`; `BoundaryBootstrap.java` (**59–60**); `HostType.java`; `MobHostRegistry.java`

Adjacency-only (not copied as Donkey biology): `docs/design/biological/manifestations/horse.md`, `.tmp_manifestation_evidence/horse.md`.
