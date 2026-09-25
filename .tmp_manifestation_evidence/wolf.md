TEMPORARY EVIDENCE — NOT PROJECT SSOT

# Wolf — temporary manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not unregister Wolf as a conclusion of this investigation.** Wolf is already in `vanilla_hosts.living_biological`. Registration is participation, not extra biology.

Method: existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient **for that consumer** |
| **C** | Named live consumer needs a missing biological distinction — STOP |

Closed leaps: `Animal` parent ≠ clade; predator→prey AI ≠ shared biology; Host Registry ≠ eligibility ≠ manifestation; variant/state ≠ BP merely because persistent/heritable/visual; tame/collar ≠ biological capability field by assumption; item production ≠ composition. Identity-route `organismKey`/`contributingSourceKey` is **B for that consumer only** — do **not** blanket tame / wolf-variant / anger as B because the identity route exists. Do not invent consumers. Do not pre-decide variants/taming are non-biological.

---

## Subject

Wolf (`minecraft:wolf`) — Minecraft Java **1.21.1**. Nine-entry `WolfVariant` registry (biome-assigned, NBT-persistent, parent-inherited). Separate domestication/state surface (untamed/tamed, owner, sit, follow, collar, anger, target memory, breeding gate, offspring copy). Untamed hunt AI (sheep / rabbit / fox / baby land turtle) plus always-on skeleton targeting. Host Registry **LIVE** `living_biological`. BioCraft identity contribution via encodeId path `"wolf"`.

Out of scope: Fox, Sheep, Rabbit, Cat, Llama, Polar Bear as investigation subjects; minting `DESIGN-BIO-MANIFEST-004`; Java/`hosts.json`/BP architecture edits.

---

## Version

Minecraft Java **1.21.1** / NeoForge **21.1.208**. Authority: mapped sources extracted under `.tmp_mc_sources/` from `biocraft-alien/build/moddev/artifacts/neoforge-21.1.208-sources.jar` (and datapack JSON already cached / extracted). Wiki = orientation only; **source wins**. If a required class had been missing, that mechanic would be **UNKNOWN** — none were.

**Source-completeness gate (passed before probes):** `Wolf.java` plus directly referenced helper/goal/state/factory types were present or extracted this pass: `WolfVariant`, `WolfVariants`, `TamableAnimal`, `NeutralMob`, `VariantHolder`, `BegGoal`, `SitWhenOrderedToGoal`, `FollowOwnerGoal`, `NonTameRandomTargetGoal`, `OwnerHurtByTargetGoal`, `OwnerHurtTargetGoal`, `ResetUniversalAngerTargetGoal`, inner `WolfAvoidEntityGoal` / `WolfPackData`, `Crackiness` (**extracted this pass**), `ArmorMaterials`, `EntityType.WOLF`, `EntityDataSerializers.WOLF_VARIANT`, `Turtle.BABY_ON_LAND_SELECTOR`, `ItemTags.WOLF_FOOD`, `BlockTags.WOLVES_SPAWNABLE_ON`, `DamageTypeTags.BYPASSES_WOLF_ARMOR`, loot/recipe/tag JSON, `WolfRenderer` / `WolfCollarLayer` / `WolfArmorLayer`.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:wolf` |
| `EntityType` | `EntityType.WOLF` — `EntityType.java` **755–762**: `MobCategory.CREATURE`, `sized(0.6F, 0.85F)`, `eyeHeight(0.68F)`, `passengerAttachments(0.0, 0.81875, -0.0625)`, tracking **10** |
| Fire / lava | **No** `.fireImmune()` |
| Class | `Wolf extends TamableAnimal implements NeutralMob, VariantHolder<Holder<WolfVariant>>` (`Wolf.java` **90**) |
| Attributes | Movement **0.3F**, max health **8.0**, attack **4.0** (`createAttributes` **160–162**). Tame side-effect sets max health **40** (`applyTamingSideEffects` **416–423**) |
| Host Registry | **REGISTERED.** `hosts.json` `vanilla_hosts.living_biological.mobs` includes `"wolf"`. `default_dna: baseline_biological`. `variant_mappings.wolf` = `"neutral"` |
| Suitability | Registered `LIVING_BIOLOGICAL` → currently suitable via HostType path. Registered ≠ extra biology; eligibility ≠ manifestation |

---

## Behavior ownership table

Method: **owner → biological input? → existing composition? → named live BioCraft consumer? → A/B/C**

| Behavior | Actual owner | Manifestation class | 1.21.1 evidence | Bio input? | Existing composition | Named BioCraft consumer | Result |
|----------|--------------|---------------------|-----------------|------------|----------------------|-------------------------|--------|
| Identity / CREATURE / size | `EntityType.WOLF` | identity | Registry id `"wolf"` **755–762** | Identity | `organismKey=wolf` | Resolver + Analyzer + eligibility (generic encodeId) | **B** |
| Host contribution | `hosts.json` + `GestationManager.writeContributingSource` | actual biological input consumed by BioCraft | `encodeId` → `minecraft:wolf` → `HostRegistryPaths.registryPath` → `"wolf"` onto offspring | Identity only | `contributingSourceKey=wolf` + `baseline_biological` | **LIVE** generic writer / Analyzer / `HostEffectManager` DNA-id lookup; **no** wolf-named unit test | **B** |
| Wolf variant (9 keys) | `DATA_VARIANT_ID` + `WolfVariant` registry | persistent entity state | Synched `Holder<WolfVariant>`; NBT `"variant"` resource location (`Wolf.java` **93**, **181–197**) | Presentation + spawn biome match | Identity covers organism | **None** reading pale/spotted/… as biology | **A** |
| Variant assignment (spawn) | `finalizeSpawn` + `WolfVariants.getSpawnVariant` | environmental interaction | First biome-matching variant, else `DEFAULT=PALE`; pack `WolfPackData` shares holder (**207–218**, `WolfVariants.java` **47–55**, **57–67**) | Encounter presentation | Not needed | None | **A** |
| Variant after creation | `setVariant` via spawn / breed / NBT | persistent entity state | No thunder/environment mutate path in `Wolf.java` | Fixed after set unless NBT/commands | Not needed | None | **A** |
| Variant breeding | `getBreedOffspring` | persistent entity state | Offspring variant = random this vs partner (**598–605**) — **not** biome re-roll | Heritable state ≠ BP field by itself | Not needed | None | **A** |
| Variant → gameplay besides render | `getTexture` only | rendering | Wild / tame / angry texture **paths** chosen from the same variant (`Wolf.java` **143–150**). Goals, damage, food, hunt set do **not** branch on variant | Presentation | Not needed | None | **A** |
| Untamed / tamed flag | `TamableAnimal` `DATA_FLAGS_ID` bit 4 | persistent entity state | NBT `"Owner"` implies tame; `setTame` (**TamableAnimal.java** **138–153**) | Entity tame state | Not a domestication BP field unless a consumer needs it | None reading tame as biology | **A** |
| Owner UUID | `DATA_OWNERUUID_ID` | player relationship | Synched optional UUID; NBT `"Owner"` | Relationship, not anatomy | Not needed | None | **A** |
| Tame health 8→40 | `applyTamingSideEffects` | persistent entity state | Attribute base max-health rewrite (**416–423**) | Vanilla tame side-effect | Not a vitality Profile | None | **A** |
| Bone taming | `tryToTame` + `Items.BONE` | player relationship | 1/3 chance if not angry (**493–516**); food tag is **not** the tame item | Interaction | Not needed | None | **A** |
| Ordered sit / sitting pose | `orderedToSit` + sit flag + `SitWhenOrderedToGoal` | transient gameplay state (order) + persistent entity state (NBT `"Sitting"`) | Owner interact toggle (**481–487**); pose bit 1 | AI / command | Not a posture trait | None | **A** |
| Following / teleport-to-owner | `FollowOwnerGoal` + `TamableAnimal` teleport helpers | transient gameplay state / player relationship | Follow **6**; sit blocks follow (`unableToMoveToOwner`) | AI | Not a loyalty Profile | None | **A** |
| Collar dye | `DATA_COLLAR_COLOR` | persistent entity state / rendering | Default red; owner + `DyeItem`; NBT `"CollarColor"`; `WolfCollarLayer` if tame | Presentation | Not pigmentation biology | None | **A** |
| Persistent anger time | `DATA_REMAINING_ANGER_TIME` + `NeutralMob` | persistent entity state | Uniform 20–39 s; NBT `"AngerTime"`; `updatePersistentAnger` in `aiStep` | Vanilla anger timer | Not an aggression Profile | None | **A** |
| Anger target memory | `persistentAngerTarget` UUID | persistent entity state | NBT `"AngryAt"`; player target goal uses `isAngryAt` (**136**, **574–583**) | Target memory | Not needed | None | **A** |
| Hunt sheep / rabbit / fox | `NonTameRandomTargetGoal` + `PREY_SELECTOR` | transient gameplay state | Untamed only; `EntityType.SHEEP/RABBIT/FOX` (**95–98**, **137**) | Hunt AI ≠ shared-hunt clade | Distinct organism keys | None | **A** |
| Hunt baby land turtle | `NonTameRandomTargetGoal` + `Turtle.BABY_ON_LAND_SELECTOR` | transient gameplay state | Untamed; baby and not in water (**138**, `Turtle.java` **78**) | Hunt AI | Distinct `turtle` key | None | **A** |
| Skeleton targeting | `NearestAttackableTargetGoal<AbstractSkeleton>` | transient gameplay state | **Not** gated on untamed (**139**) — tamed wolves still attack skeletons | Combat AI | Distinct skeleton keys | None | **A** |
| Llama avoidance | inner `WolfAvoidEntityGoal` | transient gameplay state | Untamed only; llama `getStrength() >= random(5)` (**124**, **686–714**) | Combat AI | Distinct `llama` key | None | **A** |
| Owner assist goals | `OwnerHurtByTargetGoal` / `OwnerHurtTargetGoal` | transient gameplay state / player relationship | Tame and not ordered-to-sit; `wantsToAttack` exclusions (**133–134**, **648–668**) | AI | Not needed | None | **A** |
| Pack-hurt alert | `HurtByTargetGoal.setAlertOthers` | transient gameplay state | Goal **135** — vanilla alert, not a pack-biology consumer | AI | Not needed | None | **A** |
| Beg / interested | `BegGoal` + `DATA_INTERESTED_ID` | transient gameplay state / rendering | Bone or `#wolf_food` in player hand; head-roll angle | Presentation | Not a social Profile | None | **A** |
| Wet / shake | client/server flags `isWet` / `isShaking` | transient gameplay state / rendering | Water/rain; splash particles; `WolfRenderer` wet shade | Presentation | Not a water-metabolism field | None | **A** |
| Food / heal / breed item | `#item/wolf_food` → `#meat` | item/block production | `isFood` **550–552**; tame heal uses nutrition ×2 (**436–442**) | Tag ≠ diet genetics | Child remains `wolf` | None | **A** |
| Breeding eligibility | `canMate` | reproduction state | Both must be `Wolf`, **both tame**, partner not sitting, both in love (**629–641**) | Vanilla gate | Identity sufficient | None consuming the tame-gate as biology | **A** |
| Offspring type / age | `getBreedOffspring` + `Animal.spawnChildFromBreeding` | entity/state transformation | Child `EntityType.WOLF.create`; `setBaby(true)` → age **-24000**; parents age **6000** | Vanilla lifecycle | Identity already `wolf` | None reading Age/ForcedAge as biology | **A** |
| Offspring tame/owner/collar | `getBreedOffspring` if `this.isTame()` | player relationship + persistent entity state | Copies owner UUID, `setTame(true, true)`, random parent collar (**607–615**). Does **not** copy sit, anger, armor, or biome | Vanilla birth copy | Not needed | None | **A** |
| Wolf armor | `Items.WOLF_ARMOR` + body slot + `Crackiness.WOLF_ARMOR` | item/block production / rendering | Owner equip/shear/repair with armadillo scute while sitting; `AnimalArmorItem.BodyType.CANINE` is an armor mesh enum | Equipment | Not canine anatomy | None | **A** |
| Death loot | `loot_table/entities/wolf.json` | item/block production | Empty pools in this extract (type + `random_sequence` only) | Loot | Not anatomy | None | **A** |
| Spawn floor | `checkWolfSpawnRules` + `#wolves_spawnable_on` | environmental interaction | grass_block / snow / snow_block / coarse_dirt / podzol + brightness (**680–684**) | Encounter | Not origin field | None | **A** |
| `hosts.json` `variant_mappings.wolf=neutral` | `HostConfigParser` → `MobHostRegistry.VARIANTS` | BioCraft config (not vanilla) | String map `"wolf"→"neutral"` | Folder/temperament **label**, not `WolfVariant` | Identity already represented | **PARSE-ONLY**: `MobHostRegistry.getVariant` only reached from unused `SpecializedXenomorphManager.getSpecializedVariant` (no gameplay caller) | **A** |
| Mob-based `wolf.json` xenomorph catalog | `MobEntityConfigLoader` + `SpecializedXenomorphManager` | BioCraft config keyed by identity | `variant_id: wolf`, `pack_behavior`, `enhanced_senses`, multipliers; bootstrap in `mob_catalog.json` | Identity-keyed **tuning JSON**, not a read of vanilla variant/tame/anger | Would be identity **B** if a live unit applied it | **PARSE-ONLY**: loaded at init; `getSpecializedConfig` / abilities / properties have **no** callers outside the manager | **A** |

**No row is C.** Live `contributingSourceKey=wolf` is identity already in Model A. Identity B does **not** reclassify tame / coat variant / anger.

**A/B/C counts:** **A = 31**, **B = 2**, **C = 0**. **C was not earned.**

---

## Wolf variant/state probe (dedicated)

Do **not** collapse this into domestication.

| Probe question | Outcome |
|----------------|---------|
| Meaningful 1.21.1 system? | **Yes.** Registry `Registries.WOLF_VARIANT` with nine keys: `pale` (DEFAULT), `spotted`, `snowy`, `black`, `ashen`, `rusty`, `woods`, `chestnut`, `striped` (`WolfVariants.java` **17–26**). Codec stores wild/tame/angry texture ids + biome `HolderSet` (`WolfVariant.java` **18–27**) |
| Assignment | `finalizeSpawn`: if pack `WolfPackData` present, copy `type`; else `getSpawnVariant(registry, biome)` = first variant whose `biomes()` contains the spawn biome, else `PALE` (`Wolf.java` **207–218**, `WolfVariants.java` **47–55**). Bootstrap biome ties: pale→TAIGA, spotted→`#is_savanna`, snowy→GROVE, black→OLD_GROWTH_PINE_TAIGA, ashen→SNOWY_TAIGA, rusty→`#is_jungle`, woods→FOREST, chestnut→OLD_GROWTH_SPRUCE_TAIGA, striped→`#is_badlands` (**57–67**) |
| Persistence | Synched `DATA_VARIANT_ID` (`EntityDataSerializers.WOLF_VARIANT`); NBT string `"variant"` = resource-key location |
| Change after creation | No in-class environment/lightning mutate. `setVariant` from spawn, breed child, NBT/commands only |
| Inheritance / offspring | Random choice of this vs partner holder — **not** biome re-roll (`Wolf.java` **601–605**) |
| Rendering / gameplay consequences | `getTexture()` selects **that variant’s** wild vs tame vs angry PNG (`Wolf.java` **143–150**; `WolfRenderer.getTextureLocation` delegates). Ambient sound / tail angle / hunt goals / health / food **do not** switch on variant. Contrast: Fox RED/SNOW swaps prey **priority**; Wolf variant does **not** |
| Pack spawn | `WolfPackData` carries the holder so clustered spawns share variant; `super(false)` so pack group-data does **not** request baby spawns (`Wolf.java` **716–722**) |
| Live BioCraft consumers | **None** variant-specific. Host/Analyzer path consumes encodeId `"wolf"` only. `hosts.json` `"neutral"` is **not** a `WolfVariant` key |

**Verdict:** Variant is persistent, heritable, biome-assigned entity state + rendering owner (**A**). Heritability / visual distinctiveness / nine keys do **not** earn a BP field. No live consumer requires pale vs snowy (etc.). Do not treat identity-route B as covering this mechanic; the mechanic is **A** because **no consumer asks for the distinction**.

---

## Wolf domestication/state probe (dedicated)

Traced **separately** from variant. Do **not** collapse player relationship, sit, collar, anger, or variant into a generic “domestication” or “canine” field.

| Mechanic | Classification | 1.21.1 owner | BioCraft consumption |
|----------|----------------|--------------|----------------------|
| Untamed / tamed | persistent entity state | `TamableAnimal.isTame` flag; bone `tryToTame`; hunt goals `NonTameRandomTargetGoal` require **not** tame | **None** as biology. Identity consumer does not read the flag |
| Owner | player relationship | UUID synched + NBT `"Owner"`; assist goals and collar/armor/sit require `isOwnedBy` | **None** |
| Sitting (ordered + pose) | ordered sit = persistent (`NBT Sitting`) / pose = transient presentation | Owner empty-hand toggle; `SitWhenOrderedToGoal`; blocks follow and owner-assist | **None** |
| Following | transient gameplay state + player relationship | `FollowOwnerGoal` (start 10 / stop 2); teleport ≥144 if not `unableToMoveToOwner` | **None** |
| Collar | persistent entity state + rendering | Dye by owner; default red; `WolfCollarLayer` if tame; inherited only if breeding parent is tame | **None** |
| Anger remaining time | persistent entity state | Synched int; 20–39 s sample; growl / tail / unleashability | **None** |
| Target memory (`AngryAt`) | persistent entity state | UUID; `NearestAttackableTargetGoal` player via `isAngryAt`; `ResetUniversalAngerTargetGoal` if universal-anger gamerule | **None** |
| Breeding eligibility | reproduction state (gated by tame, not by variant) | `canMate`: both tame Wolves, partner not sitting, both in love. Untamed **cannot** breed | **None** as a missing-fact. Gate is vanilla |
| Offspring state | entity/state transformation + copied relationship | Child `WOLF`; baby age; random **variant**; if this parent tame: owner+tame+collar. Anger/sit/armor **not** copied | Identity of child is still `"wolf"` (**B** for identity consumer only) |
| Variant (re-stated, not folded) | persistent entity state / rendering | Independent of tame. Tame only swaps which **texture file** of the same variant is used | **None** |

**Tame is not assumed non-biological.** It was checked: no named live BioCraft unit reads tame/owner/collar/anger as a missing biological distinction. Therefore **A**, not C. Identity B does not absorb these rows.

---

## Reproduction / lifecycle minimum

| Question | Evidence |
|----------|----------|
| Breeding exists? | **Yes.** `BreedGoal` + `isFood(#wolf_food)` + `canMate` |
| Who can mate? | Two **tamed** `Wolf`s, not self, partner not in sitting pose, both in love (`Wolf.java` **629–641**) |
| Offspring `EntityType` | `EntityType.WOLF` (`getBreedOffspring` **598–599**) |
| Age | Child `setBaby(true)` → `AgeableMob.setAge(-24000)`; parents `setAge(6000)` after breed (`Animal.java` **228**, **240–241**; `AgeableMob.java` **161–162**). Age/ForcedAge NBT on `AgeableMob`. **Absence of BioCraft age consumer recorded** |
| Inherited / persistent state | Random parent **variant**; if calling parent tame: owner UUID, tame+side-effects, random parent **collar**. **Not** inherited: sit, anger, armor, wet/shake, interested |
| Variant inheritance | **Yes** — random parent A or B holder; not biome |
| BioCraft consumption of breed/age/variant/tame copy | **None** beyond identity of the resulting `wolf` entity |

---

## Hunt AI (including rabbit / sheep)

| Target | Gate | Owner |
|--------|------|-------|
| Sheep, rabbit, fox | Untamed only (`NonTameRandomTargetGoal` + `PREY_SELECTOR`) | `Wolf.java` **95–98**, **137** |
| Baby turtle on land | Untamed; `Turtle.BABY_ON_LAND_SELECTOR` | **138** |
| `AbstractSkeleton` | **Always** (no tame gate) | **139** |
| Player | Persistent anger (`isAngryAt`) | **136** |
| Llama | Untamed avoid if llama strength ≥ `random(5)` | **124**, **699–701** |

Predator→prey AI is **not** shared biology with sheep/rabbit/fox/turtle/skeleton. Distinct `EntityType`s remain distinct organism keys.

Vanilla **does not** implement a pack-hunt goal. `HurtByTargetGoal.setAlertOthers` is hurt-alert AI. `WolfPackData` shares **spawn variant** only. BioCraft `wolf.json` `"pack_behavior": true` is **not** a read of a vanilla pack mechanic.

---

## Host contribution

| Step | Evidence |
|------|----------|
| Participation | `hosts.json` living_biological `"wolf"` + `default_dna: baseline_biological` |
| Eligibility | `HostEligibilityService` encodeId → registry path `"wolf"` → `MobHostRegistry.isSuitableForXenomorph` (HostType `LIVING_BIOLOGICAL` is suitable) |
| Host effects | `HostEffectManager` resolves `MobHostRegistry.getDnaProfileId("wolf")` → `baseline_biological` — **identity profile id**, not tame/variant |
| Gestation write | `GestationManager.writeContributingSource`: `encodeId(host)` → `HostRegistryPaths.registryPath` → `setContributingSourceKey(offspring, "wolf")` |
| Resolver | `BiologicalProfileResolver` looks up `organismKey` only; `XenomorphType` enum has **no** `wolf` form (`ovomorph`…`queen`) |
| Host Registry ≠ eligibility ≠ manifestation | Registered and eligible. Manifestation (new BP field / C) **not** earned |

---

## BioCraft consumer audit

Search: `biocraft-alien/src` (Java, JSON, tests). Classify LIVE / STUB / PARSE-ONLY / DEAD / PLANNING / TEST / UNKNOWN.

| Surface | Class | Notes |
|---------|-------|-------|
| `hosts.json` living_biological `"wolf"` | **LIVE** | Participation + `baseline_biological` id |
| `hosts.json` `variant_mappings.wolf = "neutral"` | **PARSE-ONLY** | Bound into `MobHostRegistry.VARIANTS`. `getVariant` / `getSpecializedVariant` have **no** gameplay callers |
| `entity/xenomorph/mob-based/neutral/organic/wolf.json` | **PARSE-ONLY** | Loaded because `mob_catalog.json` `bootstrap_entries` lists `neutral/organic` / `wolf`. Parsed by `MobEntityConfigParser` (`pack_behavior`, `enhanced_senses`, multipliers). `SpecializedXenomorphManager.initializeFromConfig` registers `wolf_xenomorph`. Getters unused outside the manager |
| `mob_catalog.json` `bootstrap_entries` wolf | **LIVE** parse (init load of the JSON above) | Load ≠ gameplay apply |
| `mob_catalog.json` `deep_mob_configs.neutral.mobs` includes wolf | **PLANNING** | File comment: “content planning”; bootstrap_entries is what loads |
| `GestationManager` / `DnaSampleFromOccupant` / Analyzer / Resolver | **LIVE** generic identity | Consumes `"wolf"` path only |
| `HostEffectManager` / `HostEligibilityService` | **LIVE** generic identity | Same encodeId path |
| Wolf-named Java | **DEAD / ABSENT** | No `Wolf` / `wolf` identifiers under `src/main/java` |
| Tests | **ABSENT** | `src/test` has no wolf hits |
| Inventory row `wolf` manifestation pending | **PLANNING** | Design inventory; not a live consumer |
| `AnimalArmorItem.BodyType.CANINE` | vanilla enum | Not a BioCraft consumer |

No invented consumer. PARSE-ONLY wolf.json would be identity **B** for that catalog **if** a live unit applied `variant_id=wolf`; it does not currently, and it still would not need pale/tame/anger.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"wolf"` | **LIVE** | living_biological list | Participation; can originate contribution |
| `default_dna` | **LIVE** | `baseline_biological` | Host-effect profile id, not a new BP field |
| `variant_mappings` wolf | **PARSE-ONLY** | `"neutral"` | Temperament folder label ≠ `WolfVariant`; unused by gameplay |
| wolf-named Java/tests | **ABSENT** | rg under biocraft-alien src | No wolf-specific consumer |
| Resolver / Analyzer / gestation | **LIVE** generic | Same Model A path as Cow/Cat | Identity **B not C** |
| Mob-based `wolf.json` | **PARSE-ONLY** | bootstrap load + unused manager | Do not treat `pack_behavior` as earned pack biology |
| `XenomorphType` wolf form | **ABSENT** | enum has no wolf | Offspring form remains chestburster/drone path |
| Inventory / planning | **PLANNING** | inventory pending row | Not a live consumer |

---

## Tempting but rejected interpretations

| Temptation | Why rejected |
|------------|--------------|
| New BP field because 9 heritable biome variants exist | Persistent/heritable/visual ≠ consumer. No live unit reads `WolfVariant` |
| Tame/collar/owner as domestication or canine capability field | Player relationship + presentation + vanilla gates. Checked, not assumed; **no named consumer** |
| Identity B blankets tame/variant/anger | Forbidden. Those rows stay **A** |
| `variant_mappings.neutral` is wolf coat/anger biology | String is a xenomorph folder label; PARSE-ONLY; not `pale`/`angry` |
| `wolf.json` `pack_behavior` / `enhanced_senses` earn C | PARSE-ONLY; vanilla has no pack-hunt goal; even live would be identity-keyed xenomorph tuning, not a missing vanilla distinction |
| Hunt sheep/rabbit/fox ⇒ shared predator biology / queue those organisms | Prey selectors are Wolf-owned AI. Distinct EntityTypes |
| `TamableAnimal` shared with Cat/Parrot ⇒ pet clade | Implementation reuse, not biology |
| `AnimalArmorItem.BodyType.CANINE` ⇒ canine anatomy BP | Armor mesh enum for `WOLF_ARMOR` |
| Llama strength avoid ⇒ llama/wolf shared combat biology | Untamed AI only |
| Host registered + eligible ⇒ manifestation | Host Registry ≠ eligibility ≠ manifestation |
| Empty loot table ⇒ missing anatomy field | Loot ≠ composition |
| `#wolf_food` / `#meat` ⇒ diet Profile | Item tag |

---

## Potential biological relationships

| Relation | Status |
|----------|--------|
| Wolf ↔ Fox/Sheep/Rabbit/Turtle | Prey/AI adjacency only — **not** a hunt clade |
| Wolf ↔ Skeleton | Tamed combat AI — **not** undead biology |
| Wolf ↔ Llama | Untamed avoid vs strength — combat AI |
| Wolf ↔ Cat/Parrot | Shared `TamableAnimal` parent — **not** a pet column |
| Wolf ↔ Armadillo | Scute repairs wolf armor — item recipe, not conversion biology |
| Host DNA | Live identity contribution via `"wolf"` |

Do **not** queue Fox/Sheep/Rabbit/Cat from this packet’s adjacency.

---

## Final evidence conclusion

| Question | Answer |
|----------|--------|
| **New BP field earned?** | **NO** |
| **Existing composition sufficient?** | **YES** — `organismKey` / `contributingSourceKey=wolf` (+ `baseline_biological` host-effect id) |
| **Named live BioCraft consumer (missing fact)?** | **NO** — identity consumer exists; it does not need variant/tame/anger/collar/pack |
| **Architectural escalation?** | **NO** — do not mint `DESIGN-BIO-MANIFEST-004` |

### A/B/C summary
- **A = 31** — vanilla variant, domestication/state, hunt, armor, loot, spawn, plus PARSE-ONLY BioCraft wolf JSON / `neutral` mapping
- **B = 2** — identity + live host contribution / eligibility identity route
- **C = 0** — **C was not earned**
