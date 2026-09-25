```text
TEMPORARY EVIDENCE — NOT PROJECT SSOT
Skeptical synthesis of a docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
```

# Skeptical synthesis — Piglin Brute, Horse, Cow

**Status:** Temporary reviewer synthesis. **Not** project SSOT. **Not** DESIGN-BIO-MANIFEST-004.  
**Version gate:** Minecraft Java **1.21.1** (`minecraft_version_range=[1.21.1,1.22)`).  
**Grouping:** These three were an **evidence-management batch** (second `AbstractPiglin` conversion source; living `AbstractHorse` after undead-horse reports; registered livestock identity already used in Model A tests). They are **not** a piglin clade, horse family, livestock column, bovine column, Nether family, or bio-organic grouping.

**Independent re-check:** Packets were treated as claims. Load-bearing 1.21.1 classes (`EntityType.PIGLIN_BRUTE` / `HORSE` / `COW`, `PiglinBrute` / `AbstractPiglin`, `Horse` / `AbstractHorse`, `Cow`, `MushroomCow` adjacency), dimension types, biome spawn JSON, tags, loot, bastion NBT, and live AlienCraft `hosts.json` / `HostType` / `MobHostRegistry` / `HostEligibilityService` / `GestationManager.writeContributingSource` / `BiologicalProfileResolver` were re-read from `.tmp_mc_sources/` and the live tree.

**Primary objective:** find reasons a new Biological Profile representation is **not** earned.

**C is not earned for any organism in this group.**

Closed leaps re-applied: `AbstractPiglin` ≠ clade; `AbstractHorse` ≠ horse family; conversion ≠ inheritance; gold axe ≠ capability; milking ≠ composition; spawn ≠ origin; live `contributingSourceKey` = **B** not **C**; skeleton_horse / zombie_horse reports are adjacency not ancestry; `MushroomCow extends Cow` ≠ Cow ancestry.

---

## Independent verification of tempting claims

| Tempting claim | Independent 1.21.1 / repo finding | Verdict |
|----------------|-----------------------------------|---------|
| Piglin Brute is the same organism as Piglin / “elite piglin” | Distinct `EntityType.PIGLIN_BRUTE` **545–553**. Same size/eyeHeight literals as `PIGLIN` **536–544**. Brute: `canHunt()==false`, always `GOLDEN_AXE`, `PiglinBruteAi` CORE/IDLE/FIGHT only, `PIGLIN_BRUTE_SPECIFIC_SENSOR`. Piglin implements `CrossbowAttackMob`/`InventoryCarrier` and hunts/barters | **Reject merge.** Registration duplication ≠ genetics |
| `AbstractPiglin` is a biological clade | Shared Java parent owns conversion, doors, fire path malus. Distinct brains, sensors, hunt gate, equipment, baby/inventory | **Reject clade.** Parent ≠ organism |
| Brute conversion preserves brute biology on ZP / is ancestry | `AbstractPiglin.finishConversion` → `convertTo(ZOMBIFIED_PIGLIN, true)`. Brute does not override. Destination builder has `.fireImmune()`; brute builder does **not** (`EntityType.java` **545–553** vs **793–796**). Brain discarded | **Reject inheritance.** Replacement |
| Gold axe is a BP combat/gold capability | `populateDefaultEquipmentSlots` always MAINHAND `GOLDEN_AXE`; `wantsToPickUp` accepts only that item | **Reject capability.** Spawn/pickup equipment |
| Gold-armor neutrality / barter apply to brutes | Those are `PiglinAi` / `PiglinSpecificSensor`. Brute player memory is `NEAREST_VISIBLE_ATTACKABLE_PLAYER` within **12.0**, not gold-gated | **Reject copy.** Piglin-owned |
| Hoglin hunting / piglin–hoglin ancestry on brute | `PiglinBrute.canHunt()` returns **false**. `PiglinAi.broadcastAngerTarget` skips hoglin broadcast when `!canHunt()` | **Reject.** Hunt-gate override, not Hoglin genetics |
| Bastion / Nether spawn is organism origin | No `SpawnPlacements` `PIGLIN_BRUTE` row. `crimson_forest.json` / `nether_wastes.json` list **piglin**, not brute. Gzip `bastion/mobs/melee_piglin.nbt` **does** contain `minecraft:piglin_brute`. `PiglinBruteAi.initMemories` sets HOME to spawn block | **Reject origin.** Structure encounter + stationing |
| `AbstractHorse` is a horse-family clade (Donkey/Mule/Camel/undead horses) | Horse `canMate` accepts only `Horse` or `Donkey`. Camel is a different EntityType. Skeleton/Zombie Horse are not Horse mates. **No** `convertTo` in `Horse.java` or `AbstractHorse.java` | **Reject clade.** Shared parent ≠ family |
| Skeleton Horse / Zombie Horse names or undead tags prove Horse ancestry | Living Horse is **absent** from `#undead` / `#skeletons` / `#zombies`. Horse **is** in `#dismounts_underwater`. Prior undead-horse reports are adjacency checklists | **Reject ancestry.** Distinct keys + HostType `UNDEAD` vs `LIVING_BIOLOGICAL` |
| Horse armor / saddle / jump / coat are Horse anatomy | `Horse.canUseSlot` returns **true** (all slots); `isBodyArmorItem` requires `EQUESTRIAN`. Saddle/jump are `AbstractHorse` / `Saddleable` / `PlayerRideableJumping`. Coat is packed NBT `"Variant"` | **Reject anatomy fields.** Equipment + presentation |
| Horse+Donkey → Mule proves a reproductive clade | `Horse.getBreedOffspring` creates `EntityType.MULE` when the other parent is `Donkey`. Distinct registered key | **Reject absorption.** Cross-type factory |
| Wiki 20% baby horses | Horse always supplies `HorseGroupData` before `AbstractHorse.finalizeSpawn`, skipping the **0.2F** constructor. `HorseGroupData` calls `super(true)` → `AgeableMobGroupData` baby chance **0.05F**. First of a group is never a baby (`getGroupSize() > 0`) | **Reject wiki 20%.** Still vanilla spawn math, not a BP field |
| Live `contributingSourceKey=horse` earns C | `hosts.json` `"horse"` living_biological; `HostType.LIVING_BIOLOGICAL`; `GestationManager.writeContributingSource` writes registry path. Resolver has **no** Horse branch. No Horse-named unit test | **Reject C.** Identity already represented (**B**) |
| Bucket milking is a lactation / composition trait | `Cow.mobInteract`: adult + `Items.BUCKET` → `MILK_BUCKET`. No BioCraft milk consumer | **Reject.** Item interact (**A**) |
| `MushroomCow extends Cow` / shear→Cow is Cow ancestry | Distinct `EntityType.MOOSHROOM` **502–505**. `MushroomCow.shear` creates `EntityType.COW` then discards Mooshroom. Offspring is `MOOSHROOM`. `"mooshroom"` **absent** from `hosts.json`. Cow.java has **no** Mooshroom branch | **Reject ancestry.** Conversion destination ≠ Cow biology. Do **not** queue Mooshroom from this batch |
| Mooshroom bowl stew is Cow milking | Bowl → mushroom/suspicious stew, not `MILK_BUCKET` | **Reject merge** |
| Plains / CREATURE spawn is origin | `plains.json` creature list: cow weight **8** (4–4), horse weight **5** (2–6), donkey weight **1**. Co-listing is worldgen | **Reject origin.** Spawn ≠ origin. Shared list ≠ livestock clade |
| Live `contributingSourceKey=cow` / Cow vs Human playtest earns C | `hosts.json` `"cow"`; `GestationManager.writeContributingSource`; resolver tests `cowResolvesLivingBiologicalHostReferences` and `droneCompositionDistinguishesCowFromHumanWithoutChangingExistingFields`. SPRINT fact is that the **key** differs | **Reject C.** Named consumers ask for identity already supplied (**B** / **TEST**) |
| Unregistered brute must be registered to finish | Fail-soft `unknownKeyPreservesOrganismKeyWithEmptyOptionals`. `MobHostRegistry.getHostType("piglin_brute")` → null → suitability false | **Reject.** Unregistered ≠ ineligible forever; do not register here |
| This batch is a piglin / horse / livestock clade | Three unrelated evidence threads. Different parents (`AbstractPiglin` / `AbstractHorse` / `Animal`). Different Host Registry participation. Different conversion facts | **Reject grouping.** Administrative batch only |

Minor packet notes (do not change results): Horse `canUseSlot` is unconditional `true`, not BODY-only; BODY still gated by `isBodyArmorItem(EQUESTRIAN)`. Mapped `MushroomCow.mobInteract` disables the shears branch with `if (false && …)` (NeoForge `IShearable`); conversion owner remains `MushroomCow.shear`. `PiglinBruteSpecificSensor` also fills `NEARBY_ADULT_PIGLINS` with adult `AbstractPiglin` — shared helper typing, not a clade.

---

## Consolidated matrix

| Organism | Interesting behavior | Actual owner | Biological input | Existing composition sufficient? | Named consumer | Result |
| -------- | -------------------- | ------------ | ---------------- | -------------------------------- | -------------- | ------ |
| Piglin Brute | Identity / MONSTER / no `fireImmune` | `EntityType.PIGLIN_BRUTE` | Identity | `organismKey=piglin_brute` fail-soft | Generic resolver | **B** |
| Piglin Brute | Java parent `AbstractPiglin` | class hierarchy | Implementation reuse | Distinct `piglin` / `piglin_brute` keys | None for clade | **A** |
| Piglin Brute | `canHunt()==false` | `PiglinBrute` override | Hunt-gate, not Hoglin genetics | Distinct keys | None | **A** |
| Piglin Brute | Convert to ZP | `AbstractPiglin.customServerAiStep` / `finishConversion` (brute calls `super`) | Replacement via `!piglinSafe` + 300 ticks | Distinct `piglin_brute` / `zombified_piglin` keys | None live | **A/B** |
| Piglin Brute | Golden axe / pickup filter | `populateDefaultEquipmentSlots` / `wantsToPickUp` | Equipment | Identity sufficient | None | **A** |
| Piglin Brute | Melee / player / nemesis targeting | `PiglinBruteAi` + `PiglinBruteSpecificSensor` | Combat AI | Identity sufficient | None | **A** |
| Piglin Brute | HOME / bastion placement | `initMemories` + structure NBT | Encounter/stationing | Not origin | None | **A** |
| Piglin Brute | Host Registry | **ABSENT** | Participation missing | Fail-soft identity | Origin blocked | **B** |
| Horse | Identity / CREATURE | `EntityType.HORSE` | Identity | `organismKey=horse` registered | Generic resolver | **B** |
| Horse | `AbstractHorse` + coat NBT | class + packed `"Variant"` | Parent ≠ clade; coat is presentation | Distinct key; coat not needed | None for ancestry/coat | **A/B** |
| Horse | Tame / saddle / jump / EQUESTRIAN armor | `AbstractHorse` + `Horse` slot/armor overrides | Entity/item state | Identity sufficient | None | **A** |
| Horse | Food / tempt / love | `#horse_food` / `#horse_tempt_items` (no ordinary carrot) | Item tags | Not a diet field | None | **A** |
| Horse | Horse+Horse foal / Horse+Donkey mule | `getBreedOffspring` | Vanilla birth + distinct-key factory | Child `horse` or distinct `mule` | None | **A/B** |
| Horse | Plains spawn / water dismount | `plains.json`; `#dismounts_underwater` | Encounter / tag | Not origin; tag ≠ clade | None | **A** |
| Horse | Convert to undead horses | **ABSENT** | N/A | Distinct keys already | None | **A** |
| Horse | Host contribution | `hosts.json` + eligibility + `writeContributingSource` | Identity only | `contributingSourceKey=horse` already | **LIVE** generic identity | **B** |
| Cow | Identity / CREATURE | `EntityType.COW` | Identity | `organismKey=cow` registered | Resolver + Analyzer | **B** |
| Cow | Milking | `Cow.mobInteract` bucket swap | Item interact | Not needed | None | **A** |
| Cow | Food / breed / calf | `#cow_food` (wheat) + `EntityType.COW.create` | Vanilla animal loop | Child remains `cow` | None | **A** |
| Cow | Spawn / summon | EntityType + biome lists (incl. plains) | Encounter | Not origin | None | **A** |
| Cow | Mooshroom subclass / shear→Cow | `MushroomCow` + distinct `MOOSHROOM` | Shared parent ≠ clade; conversion ≠ inheritance | Distinct keys; mooshroom unregistered | None; do not queue Mooshroom | **A** |
| Cow | Host contribution / Cow vs Human | `hosts.json` + gestation + resolver tests | Identity only | `contributingSourceKey=cow` already | **LIVE** + **TEST** identity | **B** |

---

## Shared findings (genuine shared evidence only)

These are **not** a clade:

1. **Same evidence-management batch** — leftover AbstractPiglin source, living AbstractHorse after undead-horse adjacency reports, and a registered identity already used in Model A tests. Administrative, not biological.
2. **No new BP field.** Generic `BiologicalProfileResolver` already projects `organismKey` (+ HostType / host-effect id when registered; optional `contributingSourceKey` when supplied).
3. **Minecraft owns the interesting gameplay** (conversion, axe, armor, milking, breeding, spawn). Interesting behavior ≠ consumer.
4. **Host Registry participation differs** (brute unregistered; horse and cow `LIVING_BIOLOGICAL`). That is participation, not a biological grouping and not C.
5. **Plains creature co-listing** of horse and cow (and donkey) is worldgen adjacency. Spawn ≠ origin. Shared list ≠ livestock clade.

---

## Important differences that disprove overly broad abstractions

| Abstraction that would collapse them | Disproof |
|--------------------------------------|----------|
| Piglin / brute family column | Distinct EntityTypes, brains, sensors, hunt gate, equipment, baby/inventory, spawn (biome vs structure). Shared parent conversion only |
| Horse family / `AbstractHorse` column | No Horse→undead conversion. Mule is a factory to a different key. Camel is not a mate. Undead horses are `UNDEAD` and already independently investigated |
| Livestock / bovine column | Cow milks; Horse wears EQUESTRIAN armor and has temper. Different parents. Goat/Mooshroom/Sheep not absorbed |
| Nether-native biology | Horse and Cow are Overworld CREATURE. Brute is structure-placed, not biome-listed with Piglin |
| Shared conversion biology | Only brute converts (parent-owned to ZP). Horse has **no** `convertTo`. Cow does not convert; Mooshroom shear *into* Cow is the other type’s owner |
| Registered living host = extra composition | Horse/Cow registration enables Model A identity already designed. Brute remains representable fail-soft without registration |
| Live `contributingSourceKey` = missing fact | The writer copies `HostRegistryPaths.registryPath`. Cow vs Human tests distinguish keys. That is **B** |

---

## Rejected abstractions

- Piglin-family / `AbstractPiglin` clade
- Horse-family / `AbstractHorse` clade (Donkey, Mule, Camel, Skeleton Horse, Zombie Horse)
- Livestock / bovine column (Goat, Sheep, Mooshroom)
- Gold-axe / EQUESTRIAN-armor / milking Biological Profile dimensions
- Coat-variant genetics; temper/taming as biology
- Bastion / plains / CREATURE spawn as origin
- Conversion-source continuation from brute onto Pig lightning→ZP
- Treating unregistered brute as an ineligibility field
- Treating horse/cow registration or live `contributingSourceKey` as C
- Queuing Witch, Ravager, Wandering Trader, Ghast, Creeper, Bat, or Mooshroom from this batch

---

## Biological Profile result

```text
A/B/C summary
Piglin Brute: A (vanilla owners) + B (fail-soft identity). C not earned. Do not register.
Horse: A + B (registered identity / contributingSourceKey). Named consumer of identity exists; no missing-fact consumer. C not earned. Do not change Host Registry.
Cow: A + B (registered identity / contributingSourceKey). LIVE + TEST identity consumers; no missing-fact consumer. C not earned. Do not absorb Mooshroom.
```

### New representation

```text
None earned
```

### Named consumer nuance (Horse / Cow)

Live BioCraft consumers **do** exist for Horse and Cow: Host Registry + gestation suitability + Model A `contributingSourceKey`. Cow also has named resolver tests for the living-host path and Cow-vs-Human source keys. Those consumers need **organism identity**, which existing composition already supplies. C is only for a **missing** biological fact. Do not escalate identity routing into a new field.

Brute has the generic fail-soft identity consumer only. Origin is blocked by null HostType. That is **B**, not a missing brute dossier.

---

## Recommended next investigation

**Evidence dependency:** independent **Strider** (`minecraft:strider`). Remaining Nether **living CREATURE** after Hoglin/Piglin/Brute without jumping to Ghast. `EntityType.STRIDER` sets `.fireImmune()` on the **source** type (contrast brute/hoglin/piglin absence and ZP/Zoglin destination flags). Saddle/lava-walk without `AbstractHorse` (Horse already showed saddle is equipment/ride API). Unregistered in `hosts.json`. Crimson-forest creature list already places Strider beside hoglin/piglin **monster** spawn — worldgen adjacency, not a Nether clade.

Treat Strider as its own organism. Do **not** form a Nether-creature column. Do **not** copy Horse saddle conclusions. Do **not** treat warped-fungus food as Hoglin-repellent biology.

Then continue remaining current-version bio-organic rows independently. Do **not** queue Witch, Ravager, Wandering Trader, Ghast, Creeper, or Bat. Do **not** queue Mooshroom from Cow shear. Do **not** queue Donkey/Mule/Camel from `AbstractHorse`. Do **not** queue Goat from Cow. Do **not** queue Pig as a third ZP conversion source (lightning is a different owner; conversion-source clade remains rejected).

Undead reassessment remains **deferred**. Completing this evidence-management batch does **not** authorize a piglin, horse, or livestock column.
