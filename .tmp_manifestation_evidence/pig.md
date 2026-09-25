TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Pig docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/pig.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Pig — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register or unregister Pig as a conclusion of this investigation.** Pig is already in `vanilla_hosts.living_biological`. Registration is participation, not extra biology.

Method (every behavior): existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied independently: pig/hoglin/piglin **name** ≠ ancestry; shared `Animal`/`ItemSteerable`/`Saddleable` ≠ clade; tag ≠ clade; lightning conversion ≠ inheritance; spawn biome ≠ origin; Host Registry ≠ eligibility science; interesting behavior ≠ consumer; registered host ≠ extra biology; shared livestock column with cow/horse rejected.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey` (Model A Chestburster/Drone), optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

This organism is investigated independently. Do **not** absorb Hoglin, Piglin, Piglin Brute, Zombified Piglin, Strider, Cow, or Horse as Pig biology. Working hypothesis only — prefer disprove **C**.

---

## 1. Subject / Version / Target identity

### Subject

Pig (`minecraft:pig`, living Pig) — identity, `#pig_food` food/tempt/breed, same-type piglet, saddle + carrot-on-a-stick `ItemSteerable`, lightning→`ZombifiedPiglin` replacement, loot porkchop, `#dismounts_underwater`, Host Registry LIVE `living_biological` + `HostType.LIVING_BIOLOGICAL` + `baseline_biological`, and BioCraft gestation `contributingSourceKey` identity routing.

Out of scope as organisms: Hoglin, Piglin, Piglin Brute, Zombified Piglin (destination only), Strider, Cow, Horse. Cited only as **adjacency / negative controls**.

### Version

Minecraft Java **1.21.1** only. Mapped NeoForge **21.1.208** sources under `.tmp_mc_sources/` are authoritative. Wiki = orientation/disagreement only; **source wins**. Missing required source → **UNKNOWN** (no wiki/superclass/sibling inference).

Temporary source cache (not SSOT): `.tmp_mc_sources/`.

### Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:pig` |
| `EntityType` | `EntityType.PIG` — `EntityType.java` **533–535**: `register("pig", Builder.of(Pig::new, MobCategory.CREATURE).sized(0.9F, 0.9F).passengerAttachments(0.86875F).clientTrackingRange(10))` |
| Fire / lava | **No** `.fireImmune()` on PIG. Builder default false. Destination `ZOMBIFIED_PIGLIN` **does** call `.fireImmune()` (`EntityType.java` **793–801**) — destination flag ≠ Pig biology |
| Class | `Pig extends Animal implements ItemSteerable, Saddleable` (`Pig.java` **49**) |
| Category | `MobCategory.CREATURE` |
| Summonable | Builder does **not** call `noSummon()` |
| Attributes | `DefaultAttributes` binds `EntityType.PIG` → `Pig.createAttributes()` (`DefaultAttributes.java` **134**). `Pig.createAttributes` (`Pig.java` **71–73**): `MAX_HEALTH` **10.0**, `MOVEMENT_SPEED` **0.25** |
| Dimensions | Adult hitbox **0.9 × 0.9**, passengerAttachments **0.86875F**. Baby: AgeableMob scale path (no Pig-specific `getDefaultDimensions` override in `Pig.java`) |
| Host Registry | **REGISTERED.** `hosts.json` `vanilla_hosts.living_biological.mobs` includes `"pig"` (**6**). `default_dna`: `baseline_biological` (**4**). `variant_mappings` has **no** pig entry (**47–52**). `"zombified_piglin"`, `"piglin"`, `"hoglin"` **absent** from `hosts.json` |
| Suitability | Registered living_biological → currently suitable for xenomorph hosting via `HostEligibilityService` → `MobHostRegistry.isSuitableForXenomorph`. Registered ≠ extra biology ≠ BP field |

Independent existence paths (not origin): spawn egg (`Items.PIG_SPAWN_EGG`, `Items.java` **1452**), `/summon` (`canSummon` default true), CREATURE biome spawn (Minecraft-owned; spawn biome ≠ origin), breeding `Pig.getBreedOffspring` → `EntityType.PIG.create`.

Adjacent vanilla types (identity / negative control only; **not** investigated here as organisms):

| Type | 1.21.1 fact | This packet’s use |
|------|-------------|-------------------|
| `EntityType.ZOMBIFIED_PIGLIN` | Distinct key `"zombified_piglin"`; `ZombifiedPiglin extends Zombie`; MONSTER + `.fireImmune()` (`EntityType.java` **793–801**) | Lightning **destination** only. Conversion ≠ inheritance. Unregistered in `hosts.json` |
| `EntityType.PIGLIN` / `PIGLIN_BRUTE` / `HOGLIN` | Separate registry ids; name substring overlap only | Name ancestry **rejected**. `PreferredFoodRules` explicitly avoids `pig`→`piglin` substring |
| `EntityType.STRIDER` | Also `ItemSteerable` + `Saddleable`; binds `WARPED_FUNGUS_ON_A_STICK` | Shared interface ≠ shared mount biology |
| `EntityType.COW` / horse family | Separate livestock / rideable owners | Shared farm column **rejected** |

```text
Pig does X
    → Minecraft entity / Animal / interact / spawn owns X?
    → Pig biological composition contributes something to X?
    → a live AlienCraft consumer needs that distinction beyond organismKey / contributingSourceKey?
```

---

## 2. Source-completeness table

| Source path | Status | Role in this packet |
|-------------|--------|---------------------|
| `.tmp_mc_sources/net/minecraft/world/entity/animal/Pig.java` | **PRESENT** | Goals, food, saddle/steering, offspring, `thunderHit` |
| `.tmp_mc_sources/net/minecraft/world/entity/monster/ZombifiedPiglin.java` | **PRESENT** | Destination class; no reverse→Pig path found in file |
| `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` | **PRESENT** | `PIG` **533–535**, `ZOMBIFIED_PIGLIN` **793–801** |
| `.tmp_mc_sources/net/minecraft/world/entity/ItemSteerable.java` | **PRESENT** | Interface = `boolean boost()` only |
| `.tmp_mc_sources/net/minecraft/world/entity/ItemBasedSteering.java` | **PRESENT** | Synched saddle + boost timers; NBT `"Saddle"` |
| `.tmp_mc_sources/net/minecraft/world/entity/Saddleable.java` | **PRESENT** | Saddleable contract; default horse saddle sound |
| `.tmp_mc_sources/net/minecraft/world/item/FoodOnAStickItem.java` | **PRESENT** | Boost item owner; EntityType-parameterized |
| `.tmp_mc_sources/net/minecraft/world/item/Items.java` (carrot stick / pig egg lines) | **PRESENT** | `CARROT_ON_A_STICK` → `EntityType.PIG` (**884**); spawn egg (**1452**) |
| `.tmp_mc_sources/net/minecraft/world/entity/animal/Animal.java` | **PRESENT** | `canMate`, `spawnChildFromBreeding`, love/food interact |
| `.tmp_mc_sources/net/minecraft/world/entity/AgeableMob.java` | **PRESENT** | `setBaby` → age **−24000** (**161–163**) |
| `.tmp_mc_sources/net/minecraft/world/entity/ai/attributes/DefaultAttributes.java` | **PRESENT** | Pig attribute bind **134** |
| `.tmp_mc_sources/data/minecraft/loot_table/entities/pig.json` | **PRESENT** | Porkchop + smelt-on-fire + looting |
| `.tmp_mc_sources/data/minecraft/tags/item/pig_food.json` | **PRESENT** | carrot, potato, beetroot |
| `.tmp_mc_sources/data/minecraft/tags/entity_type/dismounts_underwater.json` | **PRESENT** | Includes `minecraft:pig` |
| `.tmp_mc_sources/net/minecraft/tags/ItemTags.java` | **PRESENT** | `PIG_FOOD` bind **77** |
| `.tmp_mc_sources/net/minecraft/data/tags/VanillaItemTagsProvider.java` | **PRESENT** | Datagen `#pig_food` **446** |
| `.tmp_mc_sources/net/minecraft/data/tags/EntityTypeTagsProvider.java` | **PRESENT** | `#dismounts_underwater` includes PIG **110** |
| `.tmp_mc_sources/net/minecraft/world/entity/SpawnPlacements.java` | **PRESENT** | Pig ON_GROUND + `Animal::checkAnimalSpawnRules` **127** |
| AlienCraft `hosts.json` | **PRESENT** | `"pig"` living_biological |
| AlienCraft `GestationManager.java` | **PRESENT** | `writeContributingSource` **164–175** |
| AlienCraft `BiologicalProfileResolver.java` | **PRESENT** | Sparse profile; no pig-specific branch |
| AlienCraft Analyzer / DNA vial / report lines | **PRESENT** | Generic `organismKey` + optional `contributingSourceKey` |
| AlienCraft `PreferredFoodRules.java` + tests | **PRESENT** | Token match; anti-`pig`→`piglin` — **not** vanilla `#pig_food` consumer |
| AlienCraft `entity/.../pig.json` xenomorph stub | **PRESENT** | Catalog stub; **not** in `mob_catalog.json` `bootstrap_entries` |
| Reverse ZombifiedPiglin→Pig conversion source | **ABSENT** in searched `ZombifiedPiglin.java` / Pig reverse path | Recorded as **no reverse owner found** (not inferred) |
| Pig-specific baby dimension override | **ABSENT** in `Pig.java` | Baby size via AgeableMob defaults — **UNKNOWN** exact baby eyeHeight if needed beyond `setBaby` |
| Passenger fate on `discard()` during lightning | **UNKNOWN** beyond “not copied onto destination” | `thunderHit` has no passenger transfer; exact rider dismount semantics owned by `Entity.discard` (not re-read this pass) |

---

## 3. Dedicated Pig lightning → zombified piglin full state-transition probe

**Owner method:** `Pig.thunderHit(ServerLevel, LightningBolt)` (`Pig.java` **211–234**).

### Causing event

- Server lightning hit on a Pig.
- Gates: `level.getDifficulty() != Difficulty.PEACEFUL` **and** `EventHooks.canLivingConvert(this, EntityType.ZOMBIFIED_PIGLIN, …)` (`Pig.java` **212**).
- If gate fails or `create` returns null → `super.thunderHit` (vanilla lightning damage path), **not** conversion.

### Whether Pig entity is removed

- **YES.** After successful spawn: `this.discard()` (`Pig.java` **227**).
- Pattern is **create new + discard old**, **not** `Mob.convertTo(...)`.

### Whether new entity created

- **YES.** `ZombifiedPiglin zombifiedpiglin = EntityType.ZOMBIFIED_PIGLIN.create(level)` then `level.addFreshEntity(zombifiedpiglin)` (`Pig.java` **213–226**).
- NeoForge: `EventHooks.onLivingConvert(this, zombifiedpiglin)` **before** add (**225**).

### Exact resulting EntityType

- **`EntityType.ZOMBIFIED_PIGLIN`** / registry id **`minecraft:zombified_piglin`** (`EntityType.java` **793–801**; create call `Pig.java` **213**).

### State transfer

| Fact | Transferred? | Evidence |
|------|--------------|----------|
| Position / rotation | **YES** | `moveTo(this.getX(), this.getY(), this.getZ(), this.getYRot(), this.getXRot())` (**216**) |
| `isNoAi` | **YES** | `setNoAi(this.isNoAi())` (**217**) |
| Baby / age flag | **YES** (via `setBaby`) | `setBaby(this.isBaby())` (**218**) — AgeableMob `setBaby` sets age −24000 or 0 |
| Custom name + visibility | **YES** if present | `hasCustomName` → copy name + `isCustomNameVisible` (**219–222**) |
| Persistence | **Forced on destination** | `zombifiedpiglin.setPersistenceRequired()` (**224**) — not “copy pig flag”; always set on convert |
| Mainhand equipment | **NOT from Pig** | Destination gets **new** `Items.GOLDEN_SWORD` in `MAINHAND` (**215**). Pig saddle/equipment **not** copied |
| Saddle / `ItemBasedSteering` | **NO** | No steering/saddle read in `thunderHit` |
| Passengers / riders | **NO copy** | No passenger transfer in `thunderHit`. Rider fate on `discard()`: **UNKNOWN** (not re-traced into `Entity.discard`) |
| Health / attributes / anger / pig NBT | **NO** | Not copied; destination is fresh ZombifiedPiglin + listed fields only |
| UUID / entity identity | **NO** | New entity |

### Whether any biological identity is retained

- **No Pig EntityType identity retained.** Old entity discarded; new type is `zombified_piglin`.
- Copied presentation/state bits (pose coords, baby flag, custom name, noAi) are **not** a retained biological composition key.
- Name substring “pig” in `zombified_piglin` is **not** ancestry evidence.

### Whether transformation is reversible

- **No reverse owner found** in `ZombifiedPiglin.java` (no `EntityType.PIG` create / convert-back). `convertsInWater()` returns **false** (**92–94**) — blocks drowned-style water conversion on this class; does **not** restore Pig.
- Piglin→zombified uses separate `AbstractPiglin.convertTo(ZOMBIFIED_PIGLIN)` path — **not** Pig reverse.
- **Working conclusion:** one-way entity replacement under investigated sources. Full “cure” search across all classes: **not exhaustively proven absent repo-wide**; no Pig-restore path observed in primary files → treat as **non-reversible for Pig**.

### Whether BioCraft sees or consumes the transition

- Grep of AlienCraft `biocraft-alien/src/main` for `thunderHit` / `LivingConvert` / `ZombifiedPiglin` / `zombified_piglin` / lightning convert hooks: **no matches**.
- Host Registry: `"pig"` registered; `"zombified_piglin"` **absent**.
- Gestation/Analyzer consume host **identity key** if a living pig is gestated **before** conversion; they do **not** subscribe to this lightning replacement.

### Ownership classification (after evidence only)

| Label | Applies? | Why |
|-------|----------|-----|
| Biological transformation | **No** | No retained organism biology / DNA / BP fact; EntityType changes; BioCraft does not consume |
| Gameplay conversion | **Partial wording only** | NeoForge `canLivingConvert` / `onLivingConvert` gates exist, but Minecraft implementation is discard+create |
| **Entity replacement rule** | **YES — primary** | Explicit `EntityType.ZOMBIFIED_PIGLIN.create` + copy sparse fields + `discard` Pig |

**Pre-A/B/C manifestation class:** `entity/state transformation` (implemented as **entity replacement**).

**A/B/C:** **A** — Minecraft owns the replacement. No BioCraft named consumer needs a lightning-convert biological field. Prefer disprove C: **C not earned**.

---

## 4. Dedicated Pig reproduction probe

| Question | 1.21.1 fact |
|----------|-------------|
| Mate eligibility | `Animal.canMate` (`Animal.java` **206–212**): other must be **same class** (`Pig`), both `isInLove()`, not self. No Pig override. |
| Food / breeding inputs | `Pig.isFood` → `stack.is(ItemTags.PIG_FOOD)` (`Pig.java` **268–270**). Tag JSON: carrot, potato, beetroot. Tempt: `#pig_food` **and** separate `TemptGoal` for `Items.CARROT_ON_A_STICK` (`Pig.java` **63–64**) — stick tempts but is **not** in `#pig_food` (food ≠ stick). |
| Offspring EntityType / creation | `Pig.getBreedOffspring` → `EntityType.PIG.create(level)` (`Pig.java` **260–262**). Always Pig; **no** variant/genotype. |
| Age transfer / init | Parents do **not** copy age onto child. `Animal.spawnChildFromBreeding` sets `ageablemob.setBaby(true)` then places at parent coords (`Animal.java` **227–231`). `AgeableMob.setBaby(true)` → age **−24000** (**161–163**). Parents then `setAge(6000)` cooldown in `finalizeSpawnChildFromBreeding` (**240–241**). |
| Parent state influence | Love cause for stats/advancement only (`finalizeSpawnChildFromBreeding` **236–238**). **No** saddle, custom name, or other Pig fields copied to offspring in Pig/Animal breeding path. |
| Inherited variant / state | **None.** Pig has no variant synched data beyond saddle/boost (equipment, not genetics). Offspring is plain new `EntityType.PIG`. |
| Live BioCraft consumers of breed distinctions | **None** that need a breed/diet/piglet trait. Child identity remains `pig` if sampled/hosted. Gestation `contributingSourceKey` is host path, not breeding. |

**Pre-A/B/C manifestation class:** vanilla reproduction → `identity` (same EntityType) + `persistent entity state` (baby age) — both Minecraft-owned.

**A/B/C:** **A** (breeding mechanics). Identity of offspring already covered by `organismKey=pig` if ever sampled → **B** only for identity, not for a breed field. **C not earned**.

---

## 5. ItemSteerable ownership trace

| Layer | Actual owner | Evidence |
|-------|--------------|----------|
| Interface | `ItemSteerable` | **Only** `boolean boost();` (`ItemSteerable.java` **3–5**). Sharing this interface ≠ biology. |
| Saddle state machine | `ItemBasedSteering` held by Pig | Synched `DATA_SADDLE_ID` + `DATA_BOOST_TIME` (`Pig.java` **50–52**). NBT key `"Saddle"` (`ItemBasedSteering.java` **54–59**). |
| Saddleable contract | `Pig` implements `Saddleable` | `isSaddleable` adult alive (**155–157**); `equipSaddle` sets steering + `PIG_SADDLE` sound (**172–178**); `isSaddled` → `steering.hasSaddle()` (**168–170**); death `dropEquipment` drops `Items.SADDLE` (**160–165**). Default interface saddle sound is horse (`Saddleable.java` **14–16**) — Pig overrides via explicit `PIG_SADDLE` play in `equipSaddle`. |
| Ride start | `Pig.mobInteract` | If saddled, not food, not already vehicle → `player.startRiding(this)` (**136–142**). Else super (food/love) or saddle item `interactLivingEntity` (**144–150**). |
| Controlling passenger | `Pig.getControllingPassenger` | Requires saddled + first passenger `Player` **holding** `Items.CARROT_ON_A_STICK` (**77–81**). |
| Boost item consumer | `FoodOnAStickItem` bound to **`EntityType.PIG`** | `Items.java` **884**: `new FoodOnAStickItem<>(…durability(25), EntityType.PIG, 7)`. `use` boosts only if controlled vehicle type **equals** `canInteractWith` and `ItemSteerable.boost()` (`FoodOnAStickItem.java` **33–37**). Damage **7** per boost; break → fishing rod. |
| Ridden motion | `Pig.tickRidden` / `getRiddenInput` / `getRiddenSpeed` | Forward-only input; speed = movement × **0.225** × `steering.boostFactor()` (`Pig.java` **236–252**). |
| Strider contrast (negative control) | Separate binding | Strider uses `WARPED_FUNGUS_ON_A_STICK` + `EntityType.STRIDER`. Same helpers, **different** EntityType parameter and control item. |

**Do not treat interface sharing as biology.** Pre-A/B/C class: `transient gameplay state` (boost) + equipment/interact (`persistent entity state` for saddle NBT only as vanilla equipment).

**A/B/C:** **A**. No BioCraft consumer of saddle/steering. **C not earned**.

---

## 6. Baseline: food/breeding, loot, tags, Host Registry vs BioCraft consumers

### Food / breeding / loot

| Concern | Owner | Notes |
|---------|-------|-------|
| Food tag | `#minecraft:pig_food` | carrot, potato, beetroot (`pig_food.json`) |
| Tempt extras | `CARROT_ON_A_STICK` TemptGoal | Separate from `isFood` |
| Breed goal | `BreedGoal` priority 3 (`Pig.java` **62**) | Animal love path |
| Loot | `loot_table/entities/pig.json` | `minecraft:porkchop` 1–3 + looting; furnace_smelt if on fire / smelts_loot attacker |
| Saddle drop | `dropEquipment` | Not loot-table anatomy |

### Tags with named consumers

| Tag | Pig member? | Named 1.21.1 consumer (this pass) |
|-----|-------------|-----------------------------------|
| `#minecraft:pig_food` (item) | N/A (items) | `Pig.isFood` + TemptGoal |
| `#minecraft:dismounts_underwater` (entity_type) | **YES** | `Entity.dismountsUnderwater` (tag consumer; membership with horse/strider ≠ clade) |
| `#undead` / `#zombies` | Pig **not** listed in searched undead/zombies extracts for pig | Zombified piglin is in `#zombies` — destination only |

### Host Registry participation vs eligibility vs other live BioCraft consumers

| Concern | Status | Meaning |
|---------|--------|---------|
| `hosts.json` `"pig"` | **LIVE participation** | In `living_biological`; `baseline_biological` |
| Eligibility | **LIVE generic gate** | Suitable because registered `LIVING_BIOLOGICAL` — not a Pig dossier |
| `GestationManager.writeContributingSource` | **LIVE** | Writes registry path `"pig"` onto Chestburster/Drone when pig host gestates |
| `BiologicalProfileResolver` | **LIVE generic** | Resolves HostType/DNA id from registry; no pig branch |
| Analyzer / DNA vial / report | **LIVE generic** | Projects `organismKey` + optional `contributingSourceKey` |
| `PreferredFoodRules` | **LIVE utility** | Exact/token match so configured food name `pig` does **not** match `piglin` — **not** a consumer of `#pig_food` biology |
| `entity/.../organic/pig.json` | **STUB / PARSE-ONLY planning artifact** | Multipliers + description; **not** in `mob_catalog.json` `bootstrap_entries` (only spider/creeper/wolf/enderman bootstrap) |
| `mob_catalog.json` deep_mob_configs passive list | **PARSE-ONLY planning** | Lists `"pig"` under passive/organic planning matrix — not runtime bootstrap |
| Lightning convert | **ABSENT** BioCraft consumer | See §3 |

Participation ≠ eligibility science ≠ manifestation evidence beyond identity **B**.

---

## 7. Manifestation classification BEFORE A/B/C

For every interesting manifestation (classification only — not yet A/B/C):

| Manifestation | Pre-A/B/C class |
|---------------|-----------------|
| Registry identity `minecraft:pig` | **identity** |
| Host Registry / Model A `contributingSourceKey=pig` | **actual biological input consumed by BioCraft** (organism-definition key only) |
| Goals / panic / stroll / follow parent | **transient gameplay state** (AI) |
| `#pig_food` / tempt / love | **environmental interaction** (item tags) |
| Breeding → new Pig baby | **identity** (same type) + **persistent entity state** (age) |
| Saddle NBT | **persistent entity state** (equipment flag) |
| Carrot-stick control / boost | **transient gameplay state** |
| Lightning → zombified piglin | **entity/state transformation** (entity replacement rule) |
| Loot porkchop / cooked on fire | **item/block production** |
| `#dismounts_underwater` | **environmental interaction** (tag-driven vehicle rule) |
| Sounds / attributes / hitbox | **identity** presentation / vanilla stats (not BioCraft biology) |
| CREATURE biome spawn / egg / summon | **environmental interaction** / encounter placement (spawn ≠ origin) |

---

## 8. Behavior ownership table (pre-A/B/C + A/B/C)

| Behavior | Actual owner | Pre-A/B/C class | Biological input? | Existing BP? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|--------------|--------------------|-------|
| Identity / size / CREATURE | `EntityType.PIG` | identity | Identity only | `organismKey=pig` | Resolver / Analyzer / host lookup | **B** |
| Goals / AI | `Pig.registerGoals` | transient gameplay state | No | Identity sufficient | None | **A** |
| Food / tempt | `isFood` + TemptGoals + `#pig_food` | environmental interaction | No. Tag ≠ diet trait | Not needed | None for tag | **A** |
| Attributes / sounds | `createAttributes` + sound overrides | identity / presentation | No | Not needed | None | **A** |
| Breeding / piglet | `getBreedOffspring` + `Animal` | identity + persistent age | Vanilla same-type only | Child still `pig` | None needing breed field | **A** (+ identity **B** if sampled) |
| Saddle / ride | `Saddleable` + `ItemBasedSteering` + `mobInteract` | persistent equipment / interact | No | Not needed | None | **A** |
| ItemSteerable / carrot stick | `FoodOnAStickItem(EntityType.PIG)` + Pig ridden ticks | transient gameplay state | No. Interface ≠ biology | Not needed | None | **A** |
| Lightning → zombified piglin | `Pig.thunderHit` discard+create | entity/state transformation | No retained Pig biology | Distinct destination key | **None** | **A** |
| Loot porkchop | loot table | item/block production | No | Not needed | None | **A** |
| `#dismounts_underwater` | entity-type tag + Entity | environmental interaction | No. Tag ≠ clade | Identity sufficient | None | **A** |
| Spawn / summon / egg | EntityType + spawn systems | environmental / encounter | No. Spawn ≠ origin | Not origin field | None | **A** |
| Java `Animal` / shared interfaces | class/implements | — | Shared parent/interface ≠ clade | Distinct keys | None | **A** |
| Live host → contributingSourceKey | Host Registry + gestation + Analyzer | actual biological input (key) | Source **identity** only | existing `contributingSourceKey` | **LIVE** eligibility, gestation, Analyzer | **B** |
| PreferredFoodRules `pig` token | domain matcher | — | Prevents pig→piglin false positive | Key tokens | Config food lists (generic) | **A/B** (utility; not pig manifestation C) |
| Xenomorph `pig.json` stub | catalog file | — | Planning multipliers | N/A | **Not bootstrapped** | **A** ignore / STUB |

**No row is C.** Live `contributingSourceKey=pig` is identity already represented — **B, not C**.

---

## 9. Configuration audit

Statuses: **LIVE** / **STUB** / **PARSE-ONLY** / **DEAD** / **PLANNING** / **TEST** / **ABSENT** / **UNKNOWN**.

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` key `"pig"` | **LIVE** | `hosts.json` **6**; `default_dna: baseline_biological` | Participation. Can originate contribution. Not saddle/lightning field |
| `hosts.json` `"zombified_piglin"` / `"piglin"` / `"hoglin"` | **ABSENT** | Full `hosts.json` read | Do not merge via name; do not register from this packet |
| `variant_mappings` pig | **ABSENT** | No pig override | No aggressive/neutral override |
| `HostEligibilityService` / `MobHostRegistry` | **LIVE** generic | Tests: `HostConfigContractTest` / `MobHostRegistryTest` assert pig → `LIVING_BIOLOGICAL` + baseline | Gate via registration |
| `GestationManager.writeContributingSource` | **LIVE** | **164–175** | Production writer → `contributingSourceKey="pig"` |
| Analyzer / DNA projection | **LIVE** generic | `DnaAnalysisReportLines`, vial helpers | Projects keys only |
| `BiologicalProfileResolver` | **LIVE** generic | No pig-specific branch | Sparse composition |
| `PreferredFoodRules` | **LIVE** | Explicit anti-substring pig/piglin | Matcher hygiene, not `#pig_food` |
| `entity/.../pig.json` | **STUB** | Exists; not in bootstrap_entries | Not live xenomorph form load |
| `mob_catalog` deep passive `"pig"` | **PARSE-ONLY** | Planning matrix | Not bootstrap |
| Inventory / manifestation canonical row | **PLANNING** | Not edited by this packet | Docs ≠ live consumer |
| Lightning BioCraft hook | **ABSENT** | No main-src matches | Minecraft-only replacement |

Consumer classification:

| Candidate | Classification |
|-----------|----------------|
| Resolver / Analyzer / gestation source | **LIVE** generic identity |
| Host eligibility | **LIVE** registry gate |
| `hosts.json` pig row | **LIVE** participation |
| Pig xenomorph JSON | **STUB** (unbootstrapped) |
| Lightning convert | **ABSENT** |
| Inventory pig row | **PLANNING** |

---

## 10. Tempting but rejected

| Tempting claim | Why it fails on 1.21.1 evidence |
|----------------|--------------------------------|
| pig / piglin / hoglin name ancestry | Distinct EntityTypes; PreferredFoodRules forbids substring; lightning destination ≠ inheritance |
| Shared livestock column with cow/horse | Separate owners; different sizes/foods/interacts; no shared BioCraft livestock trait |
| Host Registry membership = manifestation evidence / eligibility science | Participation enables existing path only; suitability is HostType, not saddle/lightning biology |
| Shared `ItemSteerable` / saddle = shared mount biology with Strider/Horse | Interface is `boost()` only; stick item is EntityType-bound; Horse is not ItemSteerable |
| Lightning convert earns C / retained biology / reversible pig identity | Discard+create; sparse copy; no BioCraft consumer; no reverse→Pig owner in primary sources |
| Breeding / `#pig_food` is a diet or genetics BP field | Tag + same-type `EntityType.PIG.create`. Tag ≠ diet trait |
| Carrot-on-a-stick is pig food biology | Separate TemptGoal; **not** in `#pig_food`; steering item owner is `FoodOnAStickItem` |
| Porkchop loot = anatomy trait | Loot table production |
| Live `contributingSourceKey=pig` earns C | Named consumers already take organism-definition key → **B** |
| Interesting farm-animal / thunder behavior earns C | Interesting ≠ consumer |

---

## 11. Potential biological relationships

### 1. Pig as live xenomorph host / Model A contributing source

- **Relationship:** Facehugger may select Pig; gestation copies `"pig"` onto Chestburster/Drone; Analyzer displays it.
- **Owner:** `hosts.json` + eligibility + `GestationManager.writeContributingSource` + Analyzer.
- **Biological input?** Only organism-definition key `"pig"`.
- **Existing composition:** `organismKey` / optional `contributingSourceKey="pig"`; `HostType.LIVING_BIOLOGICAL` + `baseline_biological`.
- **Named consumer:** **LIVE**.
- **Result:** **B**. Not C.

### 2. Lightning → zombified piglin

- **Relationship:** Thunder replaces Pig with new ZombifiedPiglin (golden sword, sparse state copy, discard).
- **Owner:** `Pig.thunderHit`.
- **Biological input?** No retained Pig biology for BioCraft.
- **Existing composition:** Not needed; destination is a different unregistered key.
- **Named consumer:** **None**.
- **Result:** **A**. Entity replacement rule.

### 3. Breeding / piglet

- **Relationship:** Love + `#pig_food`; offspring Pig baby age −24000.
- **Owner:** `BreedGoal` + `Pig.getBreedOffspring` + `Animal.spawnChildFromBreeding`.
- **Biological input?** Vanilla same-type reproduction.
- **Named consumer:** None needing breed trait.
- **Result:** **A**.

### 4. Saddle / ItemSteerable / carrot stick

- **Relationship:** Equipment + EntityType-bound stick boost.
- **Owner:** Pig + `ItemBasedSteering` + `FoodOnAStickItem(EntityType.PIG)`.
- **Biological input?** No.
- **Named consumer:** None.
- **Result:** **A**.

### 5. Adjacency negatives (Hoglin / Piglin / Strider / Cow)

- **Relationship:** Name or interface overlap only.
- **Owner:** Separate EntityTypes / AI / convert paths.
- **Result:** **A**. Do not form clade. **C not earned.**

**C is not earned for any relationship.**

---

## 12. Final YES/NO gates + A/B/C counts

Pig is a 1.21.1 `Animal` creature (`minecraft:pig`, 0.9×0.9, not fire-immune) that Minecraft owns for food/tempt, breeding, saddle/steering, loot, tags, and lightning **entity replacement** into `minecraft:zombified_piglin`. BioCraft already registers `pig` and can write `contributingSourceKey=pig` — identity only.

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** |
| Named consumer exists | **YES** (live host/gestation/Analyzer identity path). **NO** named consumer of a **missing** Pig biological fact |
| Architectural escalation required | **NO** |
| Lightning retains Pig biological identity | **NO** |
| Lightning reversible to Pig | **NO** (no reverse owner in primary sources) |
| Any **C** earned | **NO** |

**Stop.** Do **not** change Host Registry. Do **not** mint DESIGN-BIO-MANIFEST-004 / Pig Profile. Do **not** absorb piglin/hoglin/strider/cow. Do **not** treat registration or live `contributingSourceKey=pig` as C.

### A/B/C summary counts

| Bucket | Count (rows / relationships) | Contents |
|--------|------------------------------|----------|
| **A** | **11+** behavior rows | Goals, food/tempt, attributes/sounds, breeding mechanics, saddle/steering, lightning replacement, loot, dismounts tag, spawn/egg, Java parent/interfaces, xenomorph stub ignore |
| **B** | **2–3** | Registry `organismKey=pig`; HostType + baseline profile; live Model A `contributingSourceKey=pig` |
| **C** | **0** | None |

### 1.21.1 authority anchors

- `.tmp_mc_sources/net/minecraft/world/entity/animal/Pig.java` — goals, food, saddle/steering, offspring, `thunderHit` **211–234**
- `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` **533–535** (`PIG`), **793–801** (`ZOMBIFIED_PIGLIN`)
- `.tmp_mc_sources/net/minecraft/world/entity/ItemSteerable.java`, `ItemBasedSteering.java`, `Saddleable.java`
- `.tmp_mc_sources/net/minecraft/world/item/FoodOnAStickItem.java`, `Items.java` **884**
- `.tmp_mc_sources/net/minecraft/world/entity/animal/Animal.java` **206–248**, `AgeableMob.java` **161–163**
- `.tmp_mc_sources/data/minecraft/loot_table/entities/pig.json`, `tags/item/pig_food.json`
- AlienCraft: `hosts.json`; `GestationManager.writeContributingSource`; `BiologicalProfileResolver`; Analyzer/vial projection; `PreferredFoodRules`

### UNKNOWN facts (explicit)

1. Exact passenger/rider teardown semantics on `discard()` during lightning (not copied; `Entity.discard` path not fully re-read).
2. Exact Pig baby eyeHeight/dimensions if a number is required beyond AgeableMob `setBaby` (no Pig override).
3. Exhaustive repo-wide proof that **no** mod/vanilla cure restores Pig from ZombifiedPiglin outside primary files searched.
