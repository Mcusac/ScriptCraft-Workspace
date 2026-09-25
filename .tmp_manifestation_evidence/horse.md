TEMPORARY EVIDENCE — NOT PROJECT SSOT

Do not treat this file as canonical design documentation.
Do not promote into manifestations/horse.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Horse — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register or unregister Horse as a conclusion of this investigation.** Horse is already in `vanilla_hosts.living_biological`. Registration is participation, not extra biology.

Method (every behavior): owner → biological input? → `organismKey` / `contributingSourceKey` enough? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied independently: `AbstractHorse` ≠ clade; name similarity ≠ ancestry; taming / saddle / variants = entity/item state; spawn ≠ origin; tag ≠ clade; Host Registry ≠ eligibility science; interesting behavior ≠ consumer; registered `LIVING_BIOLOGICAL` + live `contributingSourceKey=horse` is **B**, not **C**.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey` (Model A Chestburster/Drone), optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

**Default: NO new BP field.** Donkey / Mule / Camel / Skeleton Horse / Zombie Horse are **not absorbed**.

Prior reports `docs/design/biological/manifestations/skeleton_horse.md` and `zombie_horse.md` were used only as **claim checklists**. Every Horse owner below was re-read from 1.21.1 mapped sources. Undead-horse A/B/C rows were **not** copied as Horse biology.

---

## Subject

Horse (`minecraft:horse`) — living Horse identity on Minecraft Java **1.21.1**. Scope: EntityType registration, `Horse` / `AbstractHorse` gameplay owners, variants/markings NBT, taming/saddle/riding, EQUESTRIAN body armor (Horse override), food/tempt/breeding (including Horse+Donkey → Mule factory as a **distinct-key** control), plains spawn placement, water/dismount tags, loot, Host Registry `living_biological`, and BioCraft identity routing (`HostEligibilityService`, `GestationManager.writeContributingSource`, `BiologicalProfileResolver`).

Out of scope as organisms: Donkey, Mule, Camel, Skeleton Horse, Zombie Horse. Those types appear only as **negative controls** (distinct keys / distinct HostType / no Horse conversion owner in `Horse.java`).

---

## Version

Minecraft Java **1.21.1** only. Mapped sources in `.tmp_mc_sources/` are authoritative. Wiki is orientation / disagreement discovery only; **source wins**.

Post-1.21.1 horse UI, shears-unequip, Mounts of Mayhem horsemen, and later food items are **out of range**.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:horse` |
| `EntityType` | `EntityType.HORSE` — `EntityType.java` **419–422**: `register("horse", Builder.of(Horse::new, MobCategory.CREATURE).sized(1.3964844F, 1.6F).eyeHeight(1.52F).passengerAttachments(1.44375F).clientTrackingRange(10))` |
| Fire / lava | HORSE builder does **not** call `.fireImmune()`. Contrast is not required to classify Horse; Horse burns by default builder |
| Class | `Horse extends AbstractHorse implements VariantHolder<Variant>` (`Horse.java` **37**). `AbstractHorse extends Animal implements ContainerListener, HasCustomInventoryScreen, OwnableEntity, PlayerRideableJumping, Saddleable` (`AbstractHorse.java` **82**) |
| Category | `MobCategory.CREATURE` |
| Dimensions | Adult **1.3964844 × 1.6**, eyeHeight **1.52**, passengerAttachments **1.44375F**. Baby: `BABY_DIMENSIONS` scale **0.5** (`Horse.java` **39–42**, **254–256**). `MAGIC_HORSE_WIDTH` (`EntityType.java` **176**) is a registration literal, not genetics |
| Host Registry | **REGISTERED.** `hosts.json` `vanilla_hosts.living_biological.mobs` includes `"horse"` (**6–8**). Group `default_dna`: `baseline_biological` (**4**). `MobHostRegistry.getHostType("horse")` → `HostType.LIVING_BIOLOGICAL`. `isSuitableForXenomorph("horse")` → **true** (`HostType.java` **17**, **44–46**; `MobHostRegistry.java` **68–71**). `variant_mappings` has **no** horse entry (**47–52**) |
| Suitability | Registered `LIVING_BIOLOGICAL` → currently suitable for xenomorph hosting. Registered ≠ extra biology ≠ BP field |

Independent existence paths (not origin): `/summon` / spawn egg (EntityType is summonable by default builder), plains creature list, `Horse.getBreedOffspring` (Horse+Horse → Horse).

Negative-control identities (not investigated as organisms):

| Type | 1.21.1 fact | Use here |
|------|-------------|----------|
| `EntityType.SKELETON_HORSE` | Same adult width/height/eyeHeight; **different** passengerAttachments **1.31875F** (`EntityType.java` **603–610**) | Distinct key. `Horse.java` has **no** `convertTo` |
| `EntityType.ZOMBIE_HORSE` | Same adult size/eyeHeight; passengerAttachments **1.31875F** (`EntityType.java` **776–783**) | Distinct key. `Horse.java` has **no** `convertTo` |
| Donkey / Mule | Horse `canMate` accepts Donkey; offspring is `EntityType.MULE` | Cross-breed **factory** only. Do not absorb |
| Camel | Separate EntityType; not a Horse `canMate` partner | Reject horse-family column |

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing composition? | Named BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|----------------------|--------------------------|-------|
| Identity / size / category | `EntityType.HORSE` | `EntityType.java` **419–422**: `"horse"`, `CREATURE`, 1.3964844×1.6, eyeHeight 1.52 | Identity only | `organismKey = horse` (registered) | Generic resolver / Analyzer identity. **No** Horse-specific branch | **B** |
| Java type (`AbstractHorse` + `VariantHolder`) | `Horse` class | `Horse.java` **37**. Does **not** extend SkeletonHorse, ZombieHorse, Donkey, or Camel | Shared parent ≠ clade | Distinct key already | None for ancestry | **A/B** |
| Variants / markings | `Horse` synched packed int | `DATA_ID_TYPE_VARIANT` (`Horse.java` **38**, **56–58**). NBT `"Variant"` (**62–73**). Pack: color `variant.getId() & 0xFF` + markings `<< 8` (**84–86**). `finalizeSpawn` shares herd color via `HorseGroupData`, randomizes markings (**239–250**) | Entity presentation/state. Not coat genetics for BP | Identity covers the organism; coat is NBT | None that reads coat as biology | **A** |
| Taming / temper / owner | `AbstractHorse` | Flags `FLAG_TAME=2` (**101**, **201–202**, **219–221**). NBT `"Tame"` / `"Temper"` / `"Owner"` (**847–882**). Max temper **100** (**458–460**). Goal `RunAroundLikeCrazyGoal` (**164**). `tameWithName` sets owner + tame (**771–779**). Feeding `modifyTemper` (`handleEating` **543–546**) | **No.** Ride/temper entity state | Identity sufficient | None | **A** |
| Saddle / riding / jump | `AbstractHorse` + `Saddleable` | `isSaddleable` = alive + adult + tamed (**252–255**). Saddle slot 0; flag `FLAG_SADDLE=4` (**107**, **270–272**). Controlling passenger requires saddle (`getControllingPassenger` **1078–1087**). Jump via `PlayerRideableJumping` (`onPlayerJump` **961–975**; `canJump` **979–981**) | Equipment + ride API. Taming/saddle = entity/item state | Identity sufficient | None | **A** |
| Horse armor BODY slot | **`Horse` override** | `Horse.canUseSlot` returns **true** (`Horse.java` **224–226**). `isBodyArmorItem` requires `AnimalArmorItem.BodyType.EQUESTRIAN` (**229–235**). Equip path: `AbstractHorse.mobInteract` **722–725**. Armor-change sound (`Horse.containerChanged` **104–110**) | Equipment ≠ capability | Not an armor-capability field | None | **A** |
| Untamed interact | `Horse.mobInteract` then `AbstractHorse.mobInteract` | Untamed + food → `fedFood`. Untamed + non-food item → `makeMad` (`Horse.java` **148–167**). Empty-hand falls through to `AbstractHorse.doPlayerRide` (**728–729**) — living Horse **can** be mounted to tame | Ride/tame owner. Not undead-horse biology | Identity sufficient | None | **A** |
| Food / tempt / love | `AbstractHorse` + item tags | `isFood` = `#minecraft:horse_food` (**575–577**; JSON wheat/sugar/hay_block/apple/golden_carrot/golden_apple/enchanted_golden_apple — **no carrot**). Tempt: `#horse_tempt_items` golden carrot/apple/enchanted apple (`addBehaviourGoals` **177–179**). Love: golden carrot / golden apple / enchanted golden apple if tamed, age 0, not in love (`handleEating` **512–528**) | Food tag ≠ diet trait | Identity sufficient | None | **A** |
| Breeding / foal / mule factory | `Horse` + `AbstractHorse.canParent` | `canMate`: other is `Donkey` **or** `Horse`, both `canParent()` (`Horse.java` **173–178**). `canParent`: tamed, adult, full health, in love, not vehicle/passenger (`AbstractHorse.java` **902–904**). Horse+Horse: `EntityType.HORSE.create` + color lottery 4/9 self, 4/9 other, 1/9 random; markings 2/5 self, 2/5 other, 1/5 random (`Horse.java` **183–220**). Horse+Donkey: `EntityType.MULE.create` (**184–190**). Attribute blend `setOffspringAttributes` (**912–916**) | Vanilla `AgeableMob` reproduction. Cross-type mule factory ≠ Horse ancestry. Do not absorb Donkey/Mule | Child Horse is still `horse`; mule is a **different** key | None that needs a breed/coat field | **A/B** |
| Foal group data | `Horse.HorseGroupData` | `super(true)` (`Horse.java` **258–264**). Horse `finalizeSpawn` always supplies this group data **before** `super` (**239–250**), so `AbstractHorse.finalizeSpawn` 0.2F baby-chance path (**1144–1147**) is **skipped** | Age/spawn-group state. Not a foal BP field | Entity baby flag | None | **A** |
| Goals / grass | `AbstractHorse.registerGoals` | Panic, crazy-run, `BreedGoal(..., AbstractHorse.class)`, follow parent, water-avoiding stroll, look, random look, optional `RandomStandGoal` (**162–175**). Horse does **not** override `addBehaviourGoals` → `FloatGoal` + `TemptGoal` (**177–179**). Grass-eat on `GRASS_BLOCK` below (**608–619**); `canEatGrass()` true (**636–638**) | AI. Shared parent helper ≠ clade | Identity sufficient | None | **A** |
| Attributes | `AbstractHorse.createBaseHorseAttributes` + `Horse.randomizeAttributes` | Base jump 0.7, max health 53, movement 0.225F, step 1.0, `SAFE_FALL_DISTANCE` 6.0, `FALL_DAMAGE_MULTIPLIER` 0.5 (**443–451**). Horse overwrites health/speed/jump at spawn (**49–53**) via `generateMaxHealth` / `generateSpeed` / `generateJumpStrength` (**1032–1042**): health **15 + nextInt(8) + nextInt(9)** | Stats, not a Horse-anatomy field | Identity sufficient | None | **A** |
| Water / dismount | Entity-type tags + defaults | Horse **is** in `#dismounts_underwater`. Horse **is not** in `#undead`, `#zombies`, `#skeletons`, or `#can_breathe_under_water` (that last tag composes `#undead`; Horse is not undead). Horse has `FloatGoal` | Tag ≠ clade. Living Horse is **not** undead by 1.21.1 tags | Distinct key vs skeleton_horse / zombie_horse | Vanilla `Entity.dismountsUnderwater`, not BioCraft | **A** |
| Plains spawn | Worldgen creature list | `worldgen/biome/plains.json` **126–129**: `minecraft:horse` weight **5**, min 2, max 6. Same list also contains donkey — worldgen adjacency, not clade | **No.** Encounter placement. Spawn ≠ origin | Not an origin field | None | **A** |
| Conversion Horse → undead horses | **ABSENT in Horse/AbstractHorse** | Neither class calls `convertTo`. Distinct EntityTypes. Name similarity ≠ ancestry | N/A | Distinct keys already | None | **A** |
| Loot | Vanilla loot table | `loot_table/entities/horse.json`: leather 0–2 + looting. Inventory drop is `AbstractHorse.dropEquipment` (**584–594**) | Drops ≠ anatomy | Not needed | None | **A** |
| Host Registry / gestation | `hosts.json` + `HostEligibilityService` + `GestationManager.writeContributingSource` | `"horse"` in `living_biological`; HostType `LIVING_BIOLOGICAL`; suitability **true**; `default_dna` `baseline_biological`. After Chestburster spawn: `encodeId(host)` → `HostRegistryPaths.registryPath` → `ContributingSourceKeys.absentIfBlank` → `setContributingSourceKey` (`GestationManager.java` **164–175**) | Identity routing only. **Not** horse-anatomy | `organismKey=horse` + optional `contributingSourceKey=horse` + HostType + `hostEffectProfileId=baseline_biological` | **LIVE** production writer / resolver. Not a Horse-named unit test | **B** |

**No row is C.** Live `contributingSourceKey=horse` is identity already represented — **B**, not C.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` key `"horse"` | **LIVE** | `vanilla_hosts.living_biological.mobs` includes `"horse"` (`hosts.json` **6–8**); group `default_dna: baseline_biological` (**4**) | Participation. Do **not** register/unregister in this pass. Registration ≠ extra biology |
| Adjacent `"donkey"` / `"mule"` / `"llama"` | **LIVE** (not absorbed) | Same `living_biological` list (**7**) | Distinct keys. Shared list ≠ horse-family clade |
| `"skeleton_horse"` / `"zombie_horse"` | **LIVE** undead (negative control) | `vanilla_hosts.undead.mobs` (**16–17**) | Distinct HostType `UNDEAD`. Name/tags of undead horses ≠ Horse ancestry |
| `variant_mappings` horse | **ABSENT** | No `"horse"` under `variant_mappings` (**47–52**) | No aggressive/neutral override |
| `MobHostRegistry.getHostType("horse")` | **LIVE** | Lookup **46–48**. After bind: `LIVING_BIOLOGICAL`. DNA id from group default | Suitability true via `HostType` flag, not a Horse dossier |
| `HostEligibilityService` | **LIVE** generic | `isSuitableForXenomorph(String)` **19–21** delegates to `MobHostRegistry`. Entity overload **23–31** uses `encodeId` → `HostRegistryPaths.registryPath`. `isValidFacehuggerHost` **33–45**: valid living entity, not `MOD_XENOMORPH`, then suitable | Horse eligible via existing HostType. Not a Horse-specific consumer of missing biology |
| `BiologicalProfileResolver` | **LIVE** generic | `BiologicalProfileResolver.java` **35–56**: lowercase `organismKey`; `MobHostRegistry.getHostType` / `getDnaProfileId`; xenomorph form match by `XenomorphType` config key; `contributingSourceKey` passed through | `horse` resolves `organismKey=horse`, `HostType.LIVING_BIOLOGICAL`, `hostEffectProfileId=baseline_biological`, empty form/behavior. **No Horse branch** |
| Gestation `writeContributingSource` | **LIVE** | `GestationManager.java` **164–175**: registry path of the **host** onto Chestburster if port `supports` | Production writer of `"horse"` onto Model A carriers. Does **not** store variants, armor, taming, or anatomy |
| Horse-specific BioCraft gameplay JSON / Java branch | **ABSENT** from the listed consumers | Resolver/eligibility/gestation are generic | Vanilla remains owner of Horse gameplay |

Consumer classification:

| Candidate | Classification |
|-----------|----------------|
| `BiologicalProfileResolver` | **LIVE** generic (not Horse-specific) |
| Gestation `contributingSourceKey` | **LIVE**; Horse **origin allowed** (registered + suitable) |
| `HostEligibilityService` | **LIVE** registry gate; Horse eligible via `LIVING_BIOLOGICAL` |
| `hosts.json` horse row | **LIVE** participation |
| Horse-named missing-fact consumer | **ABSENT** |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails on 1.21.1 evidence |
|----------------|--------------------------------|
| `AbstractHorse` is a horse-family clade (Donkey/Mule/Camel/undead horses) | Shared **Java parent**. Horse `canMate` accepts only Horse or Donkey. Camel is a different EntityType. Skeleton/Zombie Horse are not Horse breeding partners. `AbstractHorse` ≠ clade |
| Skeleton Horse / Zombie Horse names or undead tags prove Horse ancestry | Living Horse is **absent** from `#undead` / `#skeletons` / `#zombies`. No `convertTo` in `Horse.java`. Name similarity ≠ ancestry |
| Horse ↔ undead horse conversion | **Absent** from Horse/AbstractHorse. Distinct EntityTypes |
| Horse armor / BODY slot is a Horse biological capability | `Horse.canUseSlot` + `isBodyArmorItem(EQUESTRIAN)`. Equipment ≠ capability |
| Plains spawn = organism-native origin | Encounter worldgen. Spawn ≠ origin. Summon/breed also exist |
| Coat variants/markings need a BP field | Packed NBT + spawn/breed lottery. Presentation/state. No BioCraft consumer |
| Horse+Donkey → Mule proves a horse-family reproductive clade | Cross-type **factory** to distinct `EntityType.MULE`. Do not absorb Donkey/Mule |
| Host Registry registration = a new BP dimension | Registration enables the existing host path. Live `contributingSourceKey=horse` is identity, **B not C** |
| Copy undead-horse A/B/C rows onto living Horse | Those reports are checklists only. Living Horse **can** be ordinarily mounted to tame; has float/tempt; wears EQUESTRIAN armor; breeds; is not `#undead` |
| Carrot is Horse food | `#horse_food` has **no** carrot (golden carrot only among carrot-named items) |

---

## Potential relationships

### 1. Horse as live xenomorph host / Model A contributing source

- **Relationship:** Facehugger may select Horse; gestation copies host registry path onto Chestburster; resolver/Analyzer project it.
- **Owner:** `hosts.json` + `HostEligibilityService` + `GestationManager.writeContributingSource` + `BiologicalProfileResolver`.
- **Biological input?** Only the organism-definition key `"horse"`.
- **Existing composition:** `organismKey=horse`; optional `contributingSourceKey=horse`; `HostType.LIVING_BIOLOGICAL` + `hostEffectProfileId=baseline_biological`.
- **Named consumer?** **LIVE** — eligibility, gestation writer, generic resolver. **No** Horse-named missing-fact consumer.
- **Result:** **B**. Live `contributingSourceKey=horse` is identity already represented. Not C.

### 2. Horse ↔ Skeleton Horse / Zombie Horse

- **Relationship:** Sibling `AbstractHorse` subclasses; similar adult width/height; distinct passenger attachments, HostType, tags.
- **Owner:** Separate EntityTypes. **No** `convertTo` in `Horse.java`.
- **Biological input?** Shared parent ≠ clade. Name similarity ≠ ancestry.
- **Existing composition:** Distinct keys `horse` / `skeleton_horse` / `zombie_horse`. Living Horse is `LIVING_BIOLOGICAL`; undead horses are `UNDEAD`.
- **Named consumer?** None for a horse-undead field.
- **Result:** **A/B**. Reject undead-horse ancestry. Do not absorb.

### 3. Horse ↔ Donkey / Mule (cross-breed factory)

- **Relationship:** `Horse.canMate` accepts Donkey; `getBreedOffspring` creates `EntityType.MULE`.
- **Owner:** `Horse.java` **173–190**.
- **Biological input?** Vanilla cross-type birth. Do not absorb Donkey/Mule.
- **Existing composition:** Distinct registered keys already.
- **Named consumer?** None for a mule-hybrid BP field.
- **Result:** **A/B**.

### 4. Horse armor / saddle / jump as anatomy

- **Owner:** `Horse.canUseSlot` / `isBodyArmorItem`; `AbstractHorse` saddle/jump.
- **Biological input?** Equipment and ride API. Taming/saddle/variants = entity/item state.
- **Named consumer?** None in BioCraft.
- **Result:** **A**.

### 5. Plains encounter

- **Owner:** `plains.json` creature list (weight 5, min 2, max 6).
- **Biological input?** No. Spawn ≠ origin.
- **Named consumer?** None.
- **Result:** **A**.

**C is not earned for any relationship.**

---

## Wiki disagreements

Wiki was **not** treated as authority. Source-owned Horse facts that commonly disagree with orientation text:

| Orientation claim | 1.21.1 authority | Conclusion |
|-------------------|------------------|------------|
| 20% of horses spawn as babies | Horse always supplies `HorseGroupData` before `AbstractHorse.finalizeSpawn`, skipping the AbstractHorse **0.2F** path (`Horse.java` **239–250**; `AbstractHorse.java` **1144–1147**). `HorseGroupData` calls `super(true)` — not the 0.2F constructor | **Do not cite wiki 20% as Horse spawn math.** AbstractHorse 20% path is skipped |
| Carrot is Horse food | `#horse_food` has wheat/sugar/hay/apple/golden_carrot/golden_apple/enchanted_golden_apple — **no carrot** | **Exclude** ordinary carrot |
| Living Horse cannot be ordinarily tamed (undead-horse wiki bleed) | Untamed Horse can be mounted via `AbstractHorse.doPlayerRide`; temper/`tameWithName` exist | Living Horse **can** be tamed through ordinary ride/temper. Do not copy undead-horse `PASS` interact |
| Horse+Donkey → mule; color lottery | `Horse.getBreedOffspring` | **Agrees** |
| Health 15–30 | `generateMaxHealth`: 15 + nextInt(8) + nextInt(9) | **Agrees** on those literals |
| Plains weight 5 group 2–6 | `plains.json` **126–129** | **Agrees** for plains placement; still spawn ≠ origin |
| Safely fall ~7 blocks | Attributes `SAFE_FALL_DISTANCE` **6.0**, `FALL_DAMAGE_MULTIPLIER` **0.5** | Cite **source attributes** |
| Undead horses “related” | Distinct EntityTypes; Horse absent from `#undead` | Keep identities separate |

---

## Final stop gate

Horse is a 1.21.1 `AbstractHorse` creature identity (`minecraft:horse`). Minecraft owns taming, saddle/riding, EQUESTRIAN armor, variants/markings, breeding (including mule factory), spawn, water/dismount tags, and loot. **No** Horse↔undead-horse conversion owner exists on `Horse` / `AbstractHorse`. BioCraft already registers `horse` as `LIVING_BIOLOGICAL` / `baseline_biological` and can write `contributingSourceKey=horse` on Model A carriers. That consumer asks only for the existing organism-definition key.

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** |
| Named consumer exists | **YES** (live host/gestation/resolver identity-source path). **NO** named consumer of a **missing** Horse biological fact |
| Architectural escalation required | **NO** |

**Stop.** A = vanilla ownership; B = existing identity/composition including live Model A source identity; C = not earned. Do **not** change Host Registry. Do **not** mint a Horse/armor/coat/taming/horse-family Profile. Do **not** absorb Donkey/Mule/Camel/Skeleton Horse/Zombie Horse. Live `contributingSourceKey=horse` is **B**, not C.

### A/B/C summary

- **A:** coat NBT, taming/temper, saddle/riding/jump, BODY armor, food/tempt, mule factory, foal group data, goals/grass, attributes, water/dismount tags, plains spawn, conversion **absence**, loot.
- **B:** `organismKey=horse` (LIVE registered); `HostType.LIVING_BIOLOGICAL`; `hostEffectProfileId=baseline_biological`; optional Model A `contributingSourceKey=horse` (identity only).
- **C:** none.

### 1.21.1 authority anchors (files actually read)

- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/Horse.java`
- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/AbstractHorse.java`
- `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` **176**, **419–422**, **603–610**, **776–783**
- `.tmp_mc_sources/data/minecraft/loot_table/entities/horse.json`
- `.tmp_mc_sources/data/minecraft/tags/item/horse_food.json`, `horse_tempt_items.json`
- `.tmp_mc_sources/data/minecraft/tags/entity_type/undead.json`, `zombies.json`, `skeletons.json`, `dismounts_underwater.json`, `can_breathe_under_water.json`
- `.tmp_mc_sources/data/minecraft/worldgen/biome/plains.json` **126–129**
- `implementations/minecraft/AlienCraft/biocraft-alien/src/main/resources/data/biocraft_alien/systems/hosts.json`
- `HostEligibilityService.java` (`layer_2_systems/level_1/parasite`)
- `GestationManager.writeContributingSource` (`GestationManager.java` **164–175**)
- `BiologicalProfileResolver.java`; `HostType.java`; `MobHostRegistry.java`

Checklist-only (not copied as Horse biology): `docs/design/biological/manifestations/skeleton_horse.md`, `zombie_horse.md`.
