TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent B independent 1.21.1 biological-manifestation investigation (rewritten from sources this pass; older `rabbit.md` not absorbed).
Do not treat this file as canonical design documentation.
Do not promote into manifestations/rabbit.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Rabbit — temporary manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register or unregister Rabbit as a conclusion of this investigation.** Rabbit is already in `vanilla_hosts.living_biological`. Registration is participation, not extra biology.

Method: existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient **for that consumer** |
| **C** | Named live consumer needs a missing biological distinction — STOP |

Closed leaps applied independently: `Animal` parent ≠ lagomorph clade; wolf/cat/fox hunt goals ≠ shared biology; Host Registry ≠ eligibility science ≠ manifestation; persistent/heritable/visual variant ≠ BP field; Killer Bunny behavioral distinctness ≠ C without a named consumer; name/easter-egg ≠ genetics; item production ≠ composition; registered host ≠ extra biology.

Existing BP composition (no invented fields): `organismKey`, optional `contributingSourceKey`, optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

Wiki = orientation only; **source wins**. Missing required source → **UNKNOWN** (no wiki / superclass-alone / mappings / sibling-packet inference).

---

## Subject

Rabbit (`minecraft:rabbit`) — `Rabbit.Variant` coats, Killer Bunny (`EVIL` / `RabbitType` 99), Toast nametag texture, hop locomotion, carrot-garden raid, `#rabbit_food` breed/tempt, same-type kits, wolf/cat/fox predator adjacency, Host Registry LIVE `living_biological`, BioCraft gestation identity routing.

Out of scope as organisms: Wolf, Cat, Fox (cited only as **adjacency / negative controls**).

---

## Version

Minecraft Java **1.21.1** only (NeoForge **21.1.208** mapped sources). Authority: `biocraft-alien/build/moddev/artifacts/neoforge-21.1.208-sources.jar` + `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar` extracts under `.tmp_mc_sources/` (NON-SSOT) > live BioCraft > vanilla JSON > design inventory.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:rabbit` |
| `EntityType` | `EntityType.RABBIT` — `EntityType.java` **572–574**: `register("rabbit", Builder.of(Rabbit::new, MobCategory.CREATURE).sized(0.4F, 0.5F).clientTrackingRange(8))` |
| Fire / lava | **No** `.fireImmune()` on RABBIT builder |
| Summonable | Builder does **not** call `noSummon()` |
| Class | `Rabbit extends Animal implements VariantHolder<Rabbit.Variant>` (`Rabbit.java` **69**) |
| Category | `MobCategory.CREATURE` |
| Attributes | `DefaultAttributes.java` **141** binds `EntityType.RABBIT` → `Rabbit.createAttributes()` (`Rabbit.java` **268–270**): health **3.0**, movement **0.3F**, attack **3.0** |
| Dimensions | Adult hitbox **0.4 × 0.5**. No Rabbit-specific `getDefaultDimensions`; baby uses `AgeableMob.setBaby` → age **-24000** |
| Host Registry | **REGISTERED.** `hosts.json` `vanilla_hosts.living_biological.mobs` includes `"rabbit"` (**7**). `default_dna`: `baseline_biological` (**4**). `variant_mappings` has **no** rabbit entry (**47–52**) |
| Suitability | Registered `LIVING_BIOLOGICAL` → `HostType.LIVING_BIOLOGICAL` `suitableForXenomorph=true` (`HostType.java` **17**) via `MobHostRegistry` / `HostEligibilityService`. Registered ≠ extra biology ≠ BP field |

Independent existence paths (not origin): spawn egg `Items.RABBIT_SPAWN_EGG` (`Items.java` **1466**), `/summon` (default summonable), CREATURE biome spawners, `Rabbit.getBreedOffspring` → `EntityType.RABBIT.create`. Spawn biome ≠ origin.

There is **no** second rabbit `EntityType` in 1.21.1 sources. Killer Bunny is **not** a separate registry identity.

---

## Source-completeness gate

Probes began only after `Rabbit.java` plus directly referenced helper/goal/state/factory types existed under `.tmp_mc_sources/`. Inner classes (`RabbitAvoidEntityGoal`, `RabbitGroupData`, `RabbitJumpControl`, `RabbitMoveControl`, `RabbitPanicGoal`, `RaidGardenGoal`, `Variant`) live **in** `Rabbit.java`. Missing parents extracted this pass from `neoforge-21.1.208-sources.jar`.

| Source path | Status | Role |
|-------------|--------|------|
| `.../animal/Rabbit.java` | **PRESENT** (647 lines) | Subject |
| `.../ai/control/JumpControl.java` | **PRESENT** (extracted this pass) | Jump-control parent |
| `.../ai/control/MoveControl.java` | **PRESENT** | Move-control parent |
| `.../ai/goal/{AvoidEntity,Breed,ClimbOnTopOfPowderSnow,Float,LookAtPlayer,MeleeAttack,MoveToBlock,Panic,Tempt,WaterAvoidingRandomStroll}Goal.java` | **PRESENT** | Direct goal parents |
| `.../ai/goal/target/{HurtBy,NearestAttackable}TargetGoal.java` | **PRESENT** | EVIL target parents |
| `.../level/block/CarrotBlock.java` | **PRESENT** (extracted this pass) | Garden-raid crop |
| `.../level/block/CropBlock.java` | **PRESENT** (`isMaxAge` **76–77**) | `CarrotBlock` parent used by raid |
| `.../level/block/FarmBlock.java` | **PRESENT** (extracted this pass) | Raid `instanceof FarmBlock` |
| `.../entity/animal/{Animal,Wolf}.java` | **PRESENT** | Breed parent; wolf prey adjacency |
| `.../entity/{AgeableMob,EntityType,VariantHolder,SpawnPlacements,DefaultAttributes}.java` | **PRESENT** | Identity / spawn / age |
| `.../client/renderer/entity/RabbitRenderer.java` | **PRESENT** | Variant + Toast + EVIL textures |
| `.../client/model/RabbitModel.java` | **PRESENT** | Hop presentation |
| `.../Cat.java`, `.../Fox.java` | **PRESENT** | Predator adjacency owners |
| Loot / `#rabbit_food` / biome variant tags / `#rabbits_spawnable_on` | **PRESENT** | Spawn / food / drops |
| `CookieItem`-style absent helper | **N/A** — no missing required class after extract | — |

No required source marked **UNKNOWN**.

---

## Behavior ownership table

Method: **owner → biological input? → existing composition? → named live BioCraft consumer? → A/B/C**

| Behavior | Manifestation class | Actual owner | Category | 1.21.1 evidence | Bio input? | Existing composition | Named BioCraft consumer | A/B/C |
|----------|---------------------|--------------|----------|-----------------|------------|----------------------|-------------------------|-------|
| Identity / CREATURE / size | identity | `EntityType.RABBIT` | identity | `"rabbit"`, `0.4×0.5`, tracking 8 | Identity | `organismKey=rabbit` | Resolver + Analyzer + vial occupancy (generic) | **B** |
| Host contribution | actual biological input consumed by BioCraft | `GestationManager.writeContributingSource` + `HostRegistryPaths` | BioCraft-consumed identity | `encodeId(host)` → registry path onto chestburster (`GestationManager.java` **164–175**) | Identity only | `contributingSourceKey=rabbit` | **LIVE** generic writer; **no** rabbit-named unit test | **B** |
| Host eligibility | identity | `hosts.json` + `MobHostRegistry` + `HostEligibilityService` | BioCraft participation | `"rabbit"` living_biological → `isSuitableForXenomorph` | Participation ≠ extra fact | `HostType.LIVING_BIOLOGICAL` + `baseline_biological` | LIVE generic lookup | **B** |
| Normal variants (brown/white/black/white_splotched/gold/salt) | persistent entity state | `Rabbit.Variant` + `DATA_TYPE_ID` | persistent entity state | Enum ids 0–5 (`Rabbit.java` **615–622**); synched int; NBT `"RabbitType"` | Presentation + spawn/heritage | Identity covers organism | **None** reading coat as biology | **A** |
| Variant assignment (spawn) | environmental interaction | `finalizeSpawn` + `getRandomRabbitVariant` | environmental interaction | Biome tags + d100; `RabbitGroupData` shares variant (`375–397`) | Encounter presentation | Not needed | None | **A** |
| Variant after creation | persistent entity state | `setVariant` via spawn/breed/NBT only | persistent entity state | No in-class biome/thunder mutate | Fixed unless NBT/commands/breed child | Not needed | None | **A** |
| Variant breeding inheritance | persistent entity state | `getBreedOffspring` | persistent entity state | 1/20 biome re-roll else random parent variant (`321–339`) | Heritable state ≠ BP | Not needed | None | **A** |
| Variant rendering (normal) | persistent entity state | `RabbitRenderer.getTextureLocation` | presentation | Switch on `getVariant()` (`RabbitRenderer.java` **34–42**) | Client texture | Not needed | None | **A** |
| Killer Bunny selection/creation | persistent entity state | `setVariant(EVIL)` | persistent entity state | **Not** returned by `getRandomRabbitVariant`; **not** a new `EntityType`; Java callers of `Variant.EVIL` / `killer_bunny` exist **only** in `Rabbit.java` (sources-jar scan). Created when `RabbitType` 99 is loaded or `setVariant(EVIL)` runs (NBT/`/summon`/`/data`, or breed inherit) | Persistent rabbit state | Identity still `rabbit` | None reading EVIL | **A** |
| Killer Bunny persistence | persistent entity state | NBT `"RabbitType"` + synched `DATA_TYPE_ID` | persistent entity state | `add/readAdditionalSaveData` **273–287**; `byId` sparse map, unknown → BROWN (`624`) | Same field as coats; id **99** | Not needed | None | **A** |
| Killer Bunny combat/AI/audio | transient gameplay state (installed from persistent variant) | `setVariant(EVIL)` + `customServerAiStep` | transient gameplay state | Armor base **8**; attack modifier **+5** (`evil`); `MeleeAttackGoal` 1.4; `HurtByTargetGoal` alert; target Player + Wolf; avoid-goals skip EVIL; hostile sound source; attack sound; jump-at-target <16 (`354–368`, **196–204**, **309–318**, **437–438**) | Gameplay from variant, not a BioCraft input | Not a combat Profile | None | **A** |
| Killer Bunny breedability | persistent entity state / lifecycle | `BreedGoal` + `Animal.canMate` | persistent entity state | `BreedGoal` always registered (`100`); **no** EVIL `canMate`/`isFood` override; `canMate` is same-class + inLove (`Animal.java` **206–211**). Offspring `EntityType.RABBIT`; `setVariant` on child **can** apply EVIL if inherited | Can breed; kits remain rabbits | Identity sufficient | None | **A** |
| Toast | identity-adjacent presentation | `RabbitRenderer` name check | presentation / easter egg | `ChatFormatting.stripFormatting(getName())` equals `"Toast"` → `toast.png` **before** variant switch (`29–32`). Not a `Variant`. `getBreedOffspring` does **not** copy custom name | Name ≠ genetics | Not needed | None | **A** |
| Hop / jump locomotion | transient gameplay state | `RabbitJumpControl` + `RabbitMoveControl` + `jumpFromGround` / `customServerAiStep` | transient gameplay state | Hop delay from speed; jump power 0.2/0.3/0.5; entity event 1; `jumpTicks`/`jumpDuration` not NBT | Movement owner = Rabbit AI | Not locomotion BP | None | **A** |
| Hop presentation | transient gameplay state | `RabbitModel.setupAnim` | presentation | `getJumpCompletion` → haunch/leg angles (`RabbitModel.java` **167–179**) | Render | Not needed | None | **A** |
| Tempt / food | item/block production | `#item/rabbit_food` + `TemptGoal` + `isFood` | item/block production | carrot, golden_carrot, dandelion; `Rabbit.java` **101**, **346–348** | Tag ≠ diet trait | Not needed | None | **A** |
| Breed / love / age | persistent entity state / lifecycle | `BreedGoal` + `Animal` + `AgeableMob` | lifecycle | Food → love; child `setBaby(true)` age **-24000**; parents age **6000** (`Animal.java` **214–241**) | Vanilla lifecycle | Child remains `rabbit` | None reading kit state | **A** |
| Garden raid | environmental interaction | `RaidGardenGoal` + `CarrotBlock` | environmental interaction | Grief via `EventHooks.canEntityGrief`; mature carrots on farmland; age−1 or destroy; `moreCarrotTicks=40` (`532–612`) | World interact | Not metabolism | None | **A** |
| `MoreCarrotTicks` | transient gameplay state | NBT + `wantsMoreFood` | transient gameplay state (persisted) | Saved (`276`); raid cooldown | Not biology | Not needed | None | **A** |
| Avoid player / wolf / monster | transient gameplay state | `RabbitAvoidEntityGoal` | AI | Distances 8 / 10 / 4; **disabled when EVIL** (`102–104`, **437–438**) | Fear AI ≠ fear Profile | Not needed | None | **A** |
| Wolf hunts rabbit | environmental interaction (adjacency) | **Wolf** `PREY_SELECTOR` | AI owned by wolf | `EntityType.RABBIT` in wolf prey (`Wolf.java` **95–97**, **137**) | Predator AI ≠ rabbit biology | Distinct `wolf` key | None on rabbit | **A** |
| Cat hunts rabbit | environmental interaction (adjacency) | **Cat** `NonTameRandomTargetGoal` | AI owned by cat | Untamed cat → `Rabbit.class` (`Cat.java` **121**) | Hunt AI ≠ clade | Distinct `cat` key | None on rabbit | **A** |
| Fox hunts rabbit | environmental interaction (adjacency) | **Fox** `STALKABLE_PREY` / land target | AI owned by fox | `instanceof Rabbit` (`Fox.java` **111**, **144–146**) | Hunt AI ≠ clade | Distinct `fox` key | None on rabbit | **A** |
| Spawn floor / placement | environmental interaction | `checkRabbitSpawnRules` + `SpawnPlacements` | environmental interaction | `#rabbits_spawnable_on` (grass/snow/snow_block/sand) + brightness; ON_GROUND (`399–403`, `SpawnPlacements.java` **134**) | Encounter | Not origin | None | **A** |
| Biome spawn presence | environmental interaction | biome `spawners.creature` | environmental interaction | Resources-jar: rabbit spawners in cherry_grove, desert, flower_forest, grove, ice_spikes, meadow, old_growth_pine_taiga, old_growth_spruce_taiga, snowy_plains, snowy_slopes, snowy_taiga, taiga. Example weights: desert **4**, snowy_plains **10**, meadow **2** | Encounter ≠ origin | Not needed | None | **A** |
| Powder-snow walk | environmental interaction | `#entity_type/powder_snow_walkable_mobs` + `ClimbOnTopOfPowderSnowGoal` | environmental interaction | Tag includes `minecraft:rabbit`; goal registered (`98`) | Path rule | Not needed | None | **A** |
| Death loot | item/block production | `loot_table/entities/rabbit.json` | item/block production | rabbit_hide 0–1; raw rabbit 1 (smelt if fire/`#smelts_loot`); rabbit_foot 10% if player-kill + looting | Drops ≠ anatomy | Not needed | None | **A** |
| Spawn egg | identity | `Items.RABBIT_SPAWN_EGG` | identity/item | Colors 10051392 / 7555121; creates `EntityType.RABBIT` then `finalizeSpawn` (never EVIL from biome roll) | Item factory | Identity covers | None | **A** |

**No row is C.** Live `contributingSourceKey=rabbit` is identity already in Model A. Killer Bunny and coat variants were **not** pre-dismissed; they fail C because **no named live consumer** reads `RabbitType` / `EVIL` / Toast.

---

## Probe 1 — Rabbit variant (normal coats)

Dedicated probe; not collapsed into Killer Bunny or Toast.

| Probe question | Outcome |
|----------------|---------|
| Normal variants | `BROWN(0)`, `WHITE(1)`, `BLACK(2)`, `WHITE_SPLOTCHED(3)`, `GOLD(4)`, `SALT(5)` — `Rabbit.java` **616–621**. `EVIL` is Probe 2. |
| Assignment | `finalizeSpawn`: `getRandomRabbitVariant(level, blockPos)` unless `RabbitGroupData` already holds a variant (**375–384**). Group data constructor `super(1.0F)` → subsequent group members can be babies at 100% chance (`AgeableMobGroupData` **183–185**) while **sharing the same variant**. |
| Biome/spawn weights | `#spawns_white_rabbits` (snowy_plains, ice_spikes, frozen_ocean, snowy_taiga, frozen_river, snowy_beach, frozen_peaks, jagged_peaks, snowy_slopes, grove): **80% WHITE / 20% WHITE_SPLOTCHED**. `#spawns_gold_rabbits` (**desert only**): **100% GOLD**. Else: **50% BROWN / 40% SALT / 10% BLACK** (`387–396`). Function **never** returns `EVIL`. |
| Persistence | Synched `DATA_TYPE_ID` (default BROWN id) + NBT int `"RabbitType"`. |
| Change after creation | No environment-driven `setVariant` in `Rabbit.java`. Commands/NBT/`setVariant` only. |
| Breeding inheritance | Start with biome roll at **this** parent's block position; if `nextInt(20) != 0` (95%), take partner variant 50% else this variant. **Not** Mendelian; **not** always biome. Child `setVariant` (**321–337**). |
| Rendering | `RabbitRenderer` maps each non-Toast variant to `textures/entity/rabbit/{brown,white,black,gold,salt,white_splotched}.png`. |
| Gameplay consequence beyond spawn/render | **None** for ids 0–5 in `Rabbit.java` (goals/attributes/sounds do not branch on coat). Coat is persistent presentation + heritage. |
| BioCraft consumer | **None** variant-specific. Host path consumes encode-id `"rabbit"` only. `MobHostRegistry.getVariant("rabbit")` is `hosts.json` `variant_mappings` (aggressive/neutral), **not** `Rabbit.Variant`. |

**Verdict:** Normal variant is persistent entity state + spawn/render/heritage owner (**A**). Heritability and biome correlation do **not** earn a BP field. No live consumer requires coat distinction.

---

## Probe 2 — Killer Bunny (EVIL)

Dedicated probe; **not** dismissed as flavor. A/B/C proved below.

| Probe question | Outcome |
|----------------|---------|
| How created / selected | `Rabbit.Variant.EVIL` id **99**, serialized name `"evil"` (`622`). `setVariant(EVIL)` is the **only** installer (`354–365`). `getRandomRabbitVariant` **cannot** select it. `finalizeSpawn` therefore **cannot** natural-spawn it. Sources-jar scan: `killer_bunny` / `Variant.EVIL` appear **only** in `Rabbit.java`. Practical creation: NBT `RabbitType:99` (summon/data/reload), or **breed inherit** via `getBreedOffspring` → `setVariant`. Spawn egg uses `finalizeSpawn` → biome coats only. |
| Separate EntityType? | **No.** Same `EntityType.RABBIT`. Lang `entity.minecraft.killer_bunny` = "The Killer Bunny" is applied as **custom name** when EVIL is set and the rabbit has no custom name (`363–365`, `Util.makeDescriptionId("entity", killer_bunny)`). Name is presentation on the same type. |
| Persistent rabbit state vs type | Persistent **variant** on the rabbit: synched int + `"RabbitType"` 99. Same field as coats. Sparse `byId` unknown ids → BROWN, so 99 is a **first-class** enum id, not a crash/unknown. |
| Can it breed? | **Yes, as far as Rabbit/Animal APIs go.** `BreedGoal` and `TemptGoal` remain registered for all rabbits. `isFood` is `#rabbit_food` with no EVIL branch. `Animal.canMate` requires same class + both in love — EVIL is still `Rabbit`. Avoid-player is off for EVIL, which changes *approach* but does not remove love/breed. **Absence of a breed-block is recorded as evidence.** |
| Does EVIL persist? | **Yes** — NBT + synched data. Reloading calls `setVariant` again, re-installing combat goals/modifiers. |
| Behavioral changes | Armor 8; attack damage +5 transient modifier (`evil`); melee + hurt-by-alert + player/wolf targeting; skip flee goals; `SoundSource.HOSTILE`; attack SFX; close-range hop-to-target. These are **vanilla gameplay** owned by `setVariant(EVIL)`, not a second organism. |
| Offspring | Still `EntityType.RABBIT.create`. Inheritance uses the same 5% biome re-roll / 95% parent-pick as coats, so an EVIL parent **can** pass `EVIL` to the kit; biome re-roll **cannot** introduce EVIL. Kit `setVariant(EVIL)` re-applies killer setup (including default name if unnamed). |
| BioCraft consumption | `DnaSampleFromOccupant` / `GestationManager.writeContributingSource` encode **entity type path** only (`HostRegistryPaths.registryPath`). EVIL rabbit → `"rabbit"`. Analyzer/vials store `organismKey` + optional `contributingSourceKey`. **No** Java/JSON reads `RabbitType`, `evil`, or `killer_bunny`. |

**A/B/C proof (Killer Bunny):**

- Minecraft owns creation, persistence, combat, and heritage → **not missing Minecraft evidence**.
- Biological input for BioCraft identity routing is still `minecraft:rabbit` → existing `organismKey` / `contributingSourceKey=rabbit` suffice for the **identity consumers** → those consumers are **B**, already counted on the identity rows.
- Distinction EVIL vs brown would be **C only if a named live consumer needed it**. Audit found **no** such consumer.
- Therefore the Killer Bunny **mechanic rows are A**. C is **not** earned. This is proof, not a pre-decision that Killer Bunny is “non-biological.”

---

## Probe 3 — Toast

Dedicated probe; naming/rendering/easter-egg, **not** genetics.

| Probe question | Outcome |
|----------------|---------|
| What Toast is | Client texture override in `RabbitRenderer.getTextureLocation`: stripped custom/display name equals `"Toast"` → `textures/entity/rabbit/toast.png` (`29–32`). Check runs **before** the variant switch, so a named Toast killer bunny would show Toast, not `caerbannog.png`. |
| Not a variant | No `Variant.TOAST`. Not written to `"RabbitType"`. |
| Persistence | Vanilla entity custom name (nametag / NBT `CustomName`), not rabbit genetics. |
| Breeding | `getBreedOffspring` sets variant only; **does not** copy custom name. Toast is **not** inherited. |
| Gameplay | Texture only. No AI/attribute branch on the string `"Toast"`. |
| BioCraft | No consumer of display name as biology. Name ≠ `organismKey`. |

**Verdict:** **A**. Easter-egg presentation. Closed leap: name ≠ genetics.

---

## Reproduction / lifecycle minimum

| Topic | Evidence | BioCraft consumption |
|-------|----------|----------------------|
| Breeding gate | `#rabbit_food` + `TemptGoal` + `Animal.mobInteract` love (`Animal.java` **136–143**) | None (tag ≠ diet Profile) |
| Mate rule | `Animal.canMate`: same class, both in love. Rabbit does **not** override. EVIL included | None |
| Offspring `EntityType` | `EntityType.RABBIT.create(level)` (`Rabbit.java` **322**) | Identity already `rabbit` |
| Age | `spawnChildFromBreeding` → `setBaby(true)` → age **-24000** (`AgeableMob.java` **161–162**). Parents setAge **6000**. Food ages babies up. Rabbit has no extra age NBT | None |
| Inherited / persistent state | Variant (including possible EVIL) as above. Custom name / Toast **not** copied. `moreCarrotTicks` is entity cooldown, not inherited | None reading `RabbitType` |
| Recorded absences | No taming; no separate baby EntityType; no EVIL natural spawn; no Toast inheritance; no BioCraft kit/variant writer | Absence recorded |

---

## Hop / movement

Owned by Rabbit, not a BP locomotion field:

- Controls replaced in constructor: `RabbitJumpControl`, `RabbitMoveControl` (`88–92`).
- Ground movement is hop-gated: on-ground and not jumping → speed 0 until a jump (`492–493`); wanted speed cached as `nextJumpSpeed`.
- Jump delay 10 ticks if speed < 2.2 else 1 (`243–248`). EVIL uses the same hop engine plus targeted jump-in when a target is within 16 blocks (`196–204`).
- `getJumpPower` scales 0.2 / 0.3 / 0.5 from speed and path height (`111–129`).
- Client: entity event 1 syncs jump animation (`413–417`); `RabbitModel` uses `getJumpCompletion`.

**A.** No BioCraft hop consumer.

---

## Predator adjacency

Owned by **other** entities’ AI, not rabbit biology:

| Predator | Owner evidence | Rabbit-side counterpart |
|----------|----------------|-------------------------|
| Wolf | `PREY_SELECTOR` includes `EntityType.RABBIT`; `NonTameRandomTargetGoal` (`Wolf.java` **95–97**, **137**) | Rabbit avoids `Wolf.class` at 10 blocks unless EVIL |
| Cat | Untamed `NonTameRandomTargetGoal<>(…, Rabbit.class, …)` (`Cat.java` **121**) | No cat-specific rabbit goal |
| Fox | `STALKABLE_PREY` / land `NearestAttackableTargetGoal` `instanceof Rabbit` (`Fox.java` **111**, **144–146**) | No fox-specific rabbit goal |
| Ocelot | **No** `Rabbit`/`RABBIT` reference in extracted `Ocelot.java` | — |

Closed leap: predator/prey AI ≠ shared biology. Wolf/Cat/Fox remain distinct `organismKey`s. Rabbit flee is Rabbit AI (**A**).

---

## Host contribution

LIVE generic path (same Model A as other living_biological hosts):

1. Facehugger eligibility: `encodeId` → `HostRegistryPaths.registryPath` → `"rabbit"` → `MobHostRegistry.isSuitableForXenomorph` (**true** via `LIVING_BIOLOGICAL`).
2. Gestation complete: `GestationManager.writeContributingSource` sets offspring `contributingSourceKey` to that path (`164–175`).
3. Analyzer / vials: `DnaSampleFromOccupant` organismKey from encode-id (non-xenomorph) or xenomorph form key; contributing source only if the occupant **supports** the genetics port (chestburster/drone), **not** from rabbit variant NBT.

EVIL / coat / Toast **do not** change the contributed key. Identity-route consumers are **B** for `rabbit` only. That is **not** C.

---

## BioCraft consumer audit

Search corpus: `biocraft-alien/src` (java/json/resources) + AlienCraft `docs` (excluding build). Hits:

| Hit | Classification | Notes |
|-----|----------------|-------|
| `hosts.json` `"rabbit"` in `living_biological.mobs` | **LIVE** | Parsed by `HostConfigParser.parseGroup` (`110+`) into `MobHostRegistry`. Participation + default_dna `baseline_biological` |
| `HostConfigLoader` / `MobHostRegistry` / `HostEligibilityService` | **LIVE** (generic) | No rabbit branch; key lookup |
| `GestationManager.writeContributingSource` | **LIVE** (generic) | encodeId path only |
| `BiologicalProfileResolver` | **LIVE** (generic) | `organismKey` lowercased → `getHostType` / `getDnaProfileId`; contributingSourceKey passed through, not interpreted as variant |
| `DnaSampleFromOccupant` / `DnaVialItemHelper` / Analyzer payload/lines | **LIVE** (generic) | Identity + optional contributing source; no `RabbitType` |
| `ChestbursterFoodHuntPolicy` / `XenomorphTargetingHelper` | **LIVE** (generic) | encodeId / host-registry membership; not rabbit-specific |
| `PreferredFoodRules` | **LIVE** (generic matcher) | Exact/token match; **no** rabbit food list or rabbit key in rules |
| `hosts.json` `variant_mappings` | **ABSENT** for rabbit | spider/creeper/wolf/enderman only |
| Rabbit-named Java | **ABSENT** | `rg -i rabbit` under `src/main/java` → no matches |
| Rabbit entity JSON under `data/biocraft_alien` (other than hosts list) | **ABSENT** | |
| `src/test` rabbit | **ABSENT** | `MobHostRegistryTest` asserts **pig**, not rabbit — **TEST** coverage of registry is pig-named; rabbit has **no** named test |
| `vanilla_organism_inventory.md` rabbit row | **PLANNING** | `pending` / `undetermined`; not a live consumer |
| Canonical `docs/design/biological/manifestations/rabbit.md` | **ABSENT** | This temp file is not that |

No STUB / PARSE-ONLY-without-load / DEAD rabbit-named type found. Inventory pending ≠ consumer.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"rabbit"` | **LIVE** | living_biological list **7** | Participation; can originate contribution |
| `default_dna` `baseline_biological` | **LIVE** | hosts.json **4**; parser **128–129** | Host-effect profile id, not a rabbit trait pack |
| `variant_mappings` rabbit | **ABSENT** | **47–52** | No aggressive/neutral override |
| Rabbit-named Java/tests | **ABSENT** | src + test rg | No rabbit-specific consumer |
| Resolver / Analyzer / gestation | **LIVE** generic | Same Model A path as other living hosts | Identity **B not C** |
| Rabbit entity JSON | **ABSENT** | biocraft_alien data | Vanilla remains owner |
| Inventory row | **PLANNING** | `vanilla_organism_inventory.md` **157** | Not live |

---

## Tempting but rejected interpretations

| Temptation | Why rejected |
|------------|--------------|
| Coat variant → BP subtype / genetics field | Persistent + heritable + visual, but **no** named BioCraft reader; spawn/render/heritage only for ids 0–5 |
| Killer Bunny is a different organism / needs a BP field because it fights | Same `EntityType`; identity consumers already have `rabbit`; **no** consumer needs EVIL vs brown. Behavioral richness ≠ C |
| Killer Bunny is non-biological because it is an easter egg | Rejected the opposite way: it **is** persistent state with combat/heritage. Still **A** for those mechanics, **B** for identity |
| Toast is a genetic morph | Renderer name string; not `RabbitType`; not inherited |
| Hop → locomotion Profile | Rabbit-owned AI/animation; no BioCraft hop consumer |
| Wolf/cat/fox prey list → shared hunt clade / lagomorph column | Other entities’ predicates; rabbit only flees (or EVIL attacks wolf) |
| `Animal` parent → mammalian/livestock column with cow/pig/sheep | Shared superclass ≠ clade |
| `#rabbit_food` / carrot raid / loot foot-hide-meat → diet or anatomy fields | Tags, grief AI, loot tables |
| Host Registry / suitability → extra biology | Participation + identity routing already **B** |
| Treat live `contributingSourceKey=rabbit` as C | Identity already represented |
| `MobHostRegistry.getVariant` could store coat/EVIL | That map is `hosts.json` variant_mappings (combat temperament strings), unused for rabbit |

---

## Potential biological relationships

| Relation | Status |
|----------|--------|
| Rabbit ↔ Wolf / Cat / Fox | Predator/prey **adjacency** only — not shared biology |
| Rabbit coats ↔ Killer Bunny | Same `Rabbit.Variant` enum / same NBT key; EVIL is a distinct id with combat install — **not** a separate species key |
| Toast ↔ coats/EVIL | Render override by name; orthogonal to variant |
| Host DNA | Live identity contribution via `"rabbit"` for **all** variants including EVIL |
| Livestock / `Animal` peers | Superclass adjacency only |

---

## Final evidence conclusion

| Question | Answer |
|----------|--------|
| **New BP field earned?** | **NO** |
| **Existing composition sufficient?** | **YES** — `organismKey` / `contributingSourceKey=rabbit` (+ registered `HostType.LIVING_BIOLOGICAL` / `baseline_biological`) |
| **Named live BioCraft consumer (missing fact)?** | **NO** — identity consumers exist; they do **not** lack a variant/EVIL/Toast fact |
| **Architectural escalation?** | **NO** — do not mint `DESIGN-BIO-MANIFEST-004` |

### A/B/C summary
- **A:** 25 (coat variants; spawn assignment; post-create immutability; coat heritage; coat render; Killer Bunny create/persist/combat/breed; Toast; hop + model; food/tempt; breed/age; garden raid + carrot ticks; flee AI; wolf/cat/fox adjacency; spawn floor; biome presence; powder snow; loot; spawn egg)
- **B:** 3 (identity `organismKey=rabbit`; live host contribution; live eligibility/HostType lookup — all identity-route, same key)
- **C:** **0 — not earned**

Killer Bunny was investigated as its own probe and remains **A** (mechanic) + **B** (identity consumers), not **C**.
