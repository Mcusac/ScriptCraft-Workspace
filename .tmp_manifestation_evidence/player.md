TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Player docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/player.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004 until synthesis.

**Isolation:** Minecraft Java **1.21.1** / NeoForge **21.1.208** mapped sources under `.tmp_mc_sources/`, live BioCraft under `biocraft-alien/src`, and this packet’s own reads only. Panda / Parrot packets were **not** absorbed as evidence.

**Hard constraints:** `player` ≠ `human` ≠ `villager`. Confirm `Player` is **not** a `Mob`. Do not assume B from `hosts.json` registration. TRACE live callers for `organismKey` / `contributingSourceKey`.

Method: owner → biological input? → existing composition? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft / existing gameplay owner is sufficient |
| **B** | `organismKey` / `contributingSourceKey` already sufficient **for that proven route** |
| **C** | Named consumer needs a missing biological fact |

---

## 1. Subject / Version / Target identity

### Subject

Vanilla Player organism-state vs controller/actor state; BioCraft host participation vs capture/UI actor role.

### Version

Minecraft Java **1.21.1** / NeoForge **21.1.208**. Wiki = orientation only; **source wins**.

### Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:player` |
| `EntityType` | `EntityType.PLAYER` — `EntityType.java` **803–812**: `Builder.<Player>createNothing(MobCategory.MISC).noSave().noSummon().sized(0.6F, 1.8F).eyeHeight(1.62F).vehicleAttachment(Player.DEFAULT_VEHICLE_ATTACHMENT).clientTrackingRange(32).updateInterval(2)` |
| Class | `public abstract class Player extends LivingEntity implements IPlayerExtension` (`Player.java` **116**) — **not** `Mob` |
| Concrete type | `ServerPlayer extends Player` |
| Category | `MobCategory.MISC` (not CREATURE/MONSTER) |
| Persistence of type | `noSave()` / `noSummon()` — player data is not ordinary entity chunk NBT |
| Attributes | `createAttributes` from `LivingEntity.createLivingAttributes()` plus attack **1.0**, movement **0.1F**, attack speed, luck, block/entity interaction ranges, mining attrs, `NeoForgeMod.CREATIVE_FLIGHT` (**228–241**). Named constant `Player.MAX_HEALTH = 20` (**121**). `createAttributes` does **not** pass an explicit MAX_HEALTH numeric override (uses living default attribute). |
| Host Registry | **REGISTERED** `vanilla_hosts.living_biological` `"player"`; HostType `LIVING_BIOLOGICAL`; `default_dna: baseline_biological` |
| Distinct keys | `villager` is a **separate** living_biological list entry. `human` is **modded_hosts.biocraft_alien.living_biological**, not `EntityType.PLAYER`. |

`EntityKind` (BioCraft domain): `PLAYER`, `VILLAGER`, `ANIMAL`, `MOD_XENOMORPH`, `OTHER` are distinct. `NeoForgeEntityQueryAdapter.classify`: `instanceof Player` → `EntityKind.PLAYER` (**120–121**). `isPlayer` is the same instanceof check (**62–63**).

---

## 2. Source-completeness table

| Source | Status | Role |
|--------|--------|------|
| `Player.java` | **PRESENT** | Organism + actor mixed surface |
| `ServerPlayer.java` | **PRESENT** | Server player |
| `FoodData.java` | **PRESENT** | Hunger/regen/starve |
| `Abilities.java` | **PRESENT** | Gamemode-driven abilities |
| `Inventory.java` | **PRESENT** | Player inventory |
| `GameType.java` | **PRESENT** | Survival/creative/adventure/spectator |
| `PlayerList.java` | **PRESENT** | Respawn replacement |
| `SleepStatus.java` | **PRESENT** | Sleep list helper |
| `ServerPlayerGameMode.java` | **PRESENT** | Gamemode |
| `LivingEntity.java` | **PRESENT** | Health, air, effects |
| `EntityType.java` | **PRESENT** | PLAYER registration |
| `can_breathe_under_water.json` | **PRESENT** | Player **not** a member |
| `loot_table/entities/player.json` | **PRESENT** | Empty pools (type + random_sequence only) |
| `CaptureEligibilityPolicy.java` | **PRESENT** | `canCapture(alive && !player)` |
| `HostEffectManager.java` | **PRESENT** | `requiresPlayerSpecificEffects` LIVE branch |
| `GestationManager.java` | **PRESENT** | Player duration ×3; writeContributingSource |

Required probe classes for this packet are cached. Broader Player mechanics (advancements, recipes, combat formulas) are **out of minimum organism-state pass** and not inferred.

---

## 3. Vanilla organism-state pass (minimum)

Classify mixed capabilities explicitly. Do not bundle them as one biological category.

| Candidate | Owner | Classification | Notes |
|-----------|-------|----------------|-------|
| Identity | `EntityType.PLAYER` / `Player extends LivingEntity` | identity | Not Mob; MISC; createNothing/noSave/noSummon |
| Hunger / food | `Player.foodData` (`FoodData`) ticked from `Player.tick` (**292**); NBT via `foodData.read/addAdditionalSaveData` | persistent entity state (physiology-like) **and** gameplay | Exhaustion → saturation → foodLevel; starve damage; natural regen gated on food + gamerule. Vanilla owner. |
| Health / damage | `LivingEntity` health + `Player.hurt` (abilities.invulnerable bypass) | organism state **and** gameplay | Creative invulnerability is **controller/game-rule**, not a second health biology |
| Sleep | `startSleepInBed` / `sleepCounter` / `isSleepingLongEnough`; `SleepStatus` / `ServerLevel` sleep list | transient gameplay state | Bed interaction + world skip; not a sleep-Profile input |
| Respiration / water | `LivingEntity.baseTick` air; `canBreatheUnderwater()` = `getType().is(EntityTypeTags.CAN_BREATHE_UNDER_WATER)` (**382–384**). Player **absent** from that tag. | environmental interaction / living air | Physiological-looking; still vanilla LivingEntity owner. Not a BP respiration field without consumer. |
| Regeneration / healing | Peaceful + `RULE_NATURAL_REGENERATION` in `Player.aiStep` (**538–549**); `FoodData.tick` saturation/food regen | transient gameplay / FoodData | |
| Effects | `LivingEntity` mob effects; player NBT includes effects via living save | transient/persistent effect application | Not player-unique biology |
| Inventory / equipment | `Player.inventory` (`Inventory`); NBT `"Inventory"` / `"SelectedItemSlot"` | player-owned gameplay state | Not organism composition |
| Experience | `experienceLevel` / `experienceProgress` / `totalExperience` NBT | gameplay progression | Not biological age |
| Age / breeding | Player is not `AgeableMob`/`Animal`. No `getBreedOffspring`. | reproduction **absent** | Do not invent player breeding |
| Gamemode | `GameType.updatePlayerAbilities` sets mayfly/instabuild/invulnerable/flying/mayBuild (**57–75**) | external game-rule / controller state | |
| Respawn / death | `Player.die` → drop inventory; `Player.respawn()` empty stub (**1454–1455**). **Live owner:** `PlayerList.respawn` **new** `ServerPlayer`, `restoreFrom`, same connection (**456–526**) | entity/state transformation (replacement) + lifecycle/system | Not retained organism identity for BioCraft beyond the new Player instance |
| Dimensions | 0.6×1.8, eye 1.62 | identity | |
| Persistent state | Player data file / NBT: inventory, food, abilities, XP, sleep timer — **not** chunk entity save (`noSave`) | mixed persistent gameplay + organism-like | |
| Loot | `entities/player.json` empty pools | item production absent in this table | KeepInventory is a gamerule, not biology |

---

## 4. Organism vs actor split (required)

| Dimension | Player organism | Player actor |
|-----------|-----------------|--------------|
| Entity identity | `EntityType.PLAYER` / `instanceof Player` | N/A |
| Biological composition | Relevant **if** sampled or used as gestation host (identity key) | Not relevant merely from being the caller |
| UI/menu interaction | no | yes (Analyzer, admission screens, inventory owner) |
| Capture policy | Target-side: `CaptureEligibilityPolicy.canCapture(alive, player)` → **false if player** | Actor-side: player **uses** Capture Net on others |
| Analyzer interaction | Organism only if the Player entity is the sample occupant | Actor controlling the machine |
| Containment interaction | Organism only if admitted (capture currently forbids) | Operator/player of pen/pod menus |
| Decision/permission | no | yes — `DESIGN-BIO-CONSEQUENCE-001` STASIS/extract/cleanse decision is **actor-side** |

Do not invent “player biology”, “sentience”, or a humanoid clade (`player`+`villager`+`human`).

---

## 5. Live BioCraft call-chain audit (prove, do not assume)

### 5.1 Host Registry `"player"` ≠ B by itself

`hosts.json` lists `"player"` under `vanilla_hosts.living_biological`. That is **participation setup**. `HostEligibilityService.isSuitableForXenomorph("player")` → `MobHostRegistry` HostType `LIVING_BIOLOGICAL` → `isSuitableForXenomorph()==true`. Facehugger `HostValidationHelper.isValidHostForFacehugger` uses that path. Registration still does not by itself prove `contributingSourceKey` consumption.

### 5.2 `contributingSourceKey` / `organismKey` live callers

| Caller | What it does | Player-specific? | Consumes player identity as composition? |
|--------|--------------|------------------|------------------------------------------|
| `GestationManager.writeContributingSource` | `encodeId(host)` → `HostRegistryPaths.registryPath` → `setContributingSourceKey(offspring, sourceKey)` | No — generic. If host is Player, key is **`player`**. | **YES — LIVE generic route.** This is identity **B** for that route, not C. |
| `DnaSampleFromOccupant.organismKey` | Xenomorph form **or** `encodeId` → registry path | No — generic. Occupant Player would yield `"player"`. | **Conditional LIVE** if a Player is ever an occupant. Capture currently forbids Player as net target (below). |
| `BiologicalProfileResolver.resolve` | Lookup HostType + dna profile id by organismKey | Lookup `"player"` → `LIVING_BIOLOGICAL` + `baseline_biological` same as cow/villager group default | Identity / HostType routing — **not** a missing-fact consumer |
| Analyzer UI (`DnaAnalysisReportLines`) | Displays `organismKey` / `contributingSourceKey` | Actor uses UI; payload is sample identity | Display of existing keys |

**Do not assume B from hosts.json.** The earned **B** is the generic gestation writer (and occupant sampling) using encodeId `"minecraft:player"` → `"player"`. That is the same Model A identity already used for cow/pig — **B not C**.

Tests (`BiologicalProfileDnaAnalysisPortTest`) contrast `contributingSourceKey` **cow vs human** (modded host), **not** vanilla Player vs Villager. Do not collapse `player` and `human`.

### 5.3 CaptureEligibilityPolicy

```text
canCapture(alive, player) = alive && !player
CaptureEligibilityAdapter: entity instanceof Player
```

This answers **“May a transport carrier capture this entity?”** — a **gameplay rule**. It does **not** demonstrate a biological property of the Player organism that Biological Profile must store. Classification: gameplay / handling policy. Result **A** (do not promote capture-ban to BP). Capture-ban also means Player is typically **not** a specimen-pod occupant; that absence is not a missing BP field.

### 5.4 `requires_player_specific_effects` — LIVE vs PARSE-ONLY

| Layer | Evidence |
|-------|----------|
| Parse | `HostEffectProfileParser` reads `host_effects.requires_player_specific_effects` into `LoadedHostEffectProfile.requiresPlayerSpecificEffects`. `baseline_biological.json` and `undead.json` are **true**; construct/elemental/inorganic/spiritual are **false**. |
| Forbidden on hosts.json | `HostConfigParser.FORBIDDEN_BIOLOGY_KEYS` includes this key — Host Registry must not own it. |
| LIVE consumer | `HostEffectManager.applyHostImmobilization` **63–65**: `if (profile.requiresPlayerSpecificEffects && entityQuery.isPlayer(host)) { presentation.applyPlayerAttachmentPose(host); }` |
| Pose adapter | `NeoForgeEntityPresentationAdapter.applyPlayerAttachmentPose`: pitch 90, stop sprint/swim/jump, lock creative flight, force `invulnerable=false`, `mayBuild=false`. Restore on `removeHostEffects` for `isPlayer`. |

**Verdict: LIVE**, not parse-only. Interpretation: **effect-routing / attachment presentation policy** when the host entity is a Player. The flag lives on the **host-effect profile** (shared `baseline_biological` for all living_biological hosts including pig/cow/villager), then the live branch additionally requires `isPlayer`. That is **not** a biological distinction of Player composition that existing identity cannot already gate. Do **not** promote to a BP field. Result **A** (policy) with identity already available if a consumer needed “is this host a player?” (`instanceof Player` / `organismKey=player`).

### 5.5 Other player-host gameplay (not BP)

- `GestationManager.applyGestationEffect`: if `isPlayer(host)`, duration `*= 3` (accepted Java residual). Gameplay duration, not a missing biological fact.
- `OvomorphHostSelectionPolicy.isCreativePlayer`: skip/creative rule — controller state.
- `XenomorphTargetingHelper`: `EntityKind.PLAYER` targeting priority — AI gameplay.
- Admission menus take `player` as **inventory owner / operator** — actor.

### 5.6 DESIGN-BIO-CONSEQUENCE-001

Sprint text: host `contributingSourceKey` is lab-visible; **the player decides** STASIS / extract / cleanse. That decision UX is **actor-side**. It is not a Player-organism BP consumer.

---

## 6. Behavior ownership table

| Behavior | Actual owner | Classification | Biological input? | Existing composition | Named BioCraft consumer | Result |
|----------|--------------|----------------|-------------------|----------------------|-------------------------|--------|
| Identity | `EntityType.PLAYER` | identity | Identity | `organismKey=player` | LIVE generic encodeId if host/sample | **B** (that route) |
| Hunger / FoodData | `FoodData` + Player tick | persistent entity state / gameplay | Vanilla physiology owner | Identity sufficient | None needing hunger BP | **A** |
| Health | LivingEntity + Player.hurt | organism + gameplay | Vanilla | Identity sufficient | None | **A** |
| Respiration | LivingEntity air + tag (player not in `#can_breathe_under_water`) | environmental / living air | Vanilla | Identity sufficient | None | **A** |
| Sleep | Player bed + SleepStatus | transient gameplay | No | — | None | **A** |
| Inventory / XP / gamemode | Inventory, XP fields, GameType/Abilities | gameplay / controller | No | — | None | **A** |
| Respawn | `PlayerList.respawn` new ServerPlayer | entity/state transformation | No retained BioCraft player-biology | New instance identity | None | **A** |
| Breeding | Absent | — | Absent | — | None | **A** |
| Capture ban | `CaptureEligibilityPolicy` | gameplay rule | Not a BP fact | `instanceof Player` already | Capture Net adapter | **A** |
| `requires_player_specific_effects` | HostEffectManager + pose adapter | effect application / presentation | Routing, not missing composition | `isPlayer` / identity | LIVE pose, not BP | **A** |
| Gestation ×3 | GestationManager | transient gameplay duration | No | Identity already known | LIVE duration | **A** |
| Host contribution | hosts + writeContributingSource | actual biological input (key) | Identity only | `contributingSourceKey=player` | **LIVE** generic | **B** |
| Analyzer/containment UI | Screens/menus | actor | No | — | Actor caller | **A** |
| CONSEQUENCE-001 decision | Sprint UX | actor | No | Source key of **contained xenomorph** | Actor | **A** |

No row is **C**.

---

## 7. Configuration audit

| Finding | Status | Interpretation |
|---------|--------|----------------|
| `hosts.json` `"player"` | **LIVE** | Participation ≠ player biology |
| `hosts.json` `"human"` | **LIVE separate** | Modded organism; do not collapse |
| `hosts.json` `"villager"` | **LIVE separate** | Do not collapse |
| `requires_player_specific_effects` | **LIVE** on effect profiles | Pose routing; not BP |
| Player-named DNA/gene fields | **ABSENT** | Do not invent |
| Capture player | **LIVE forbid** | Gameplay eligibility |

---

## 8. Tempting but rejected

- Player = human = villager
- Capture-ban as biological unsuitability / BP field
- Hunger/respiration → automatic metabolism/respiration Profile
- Gamemode/creative → organism capability
- Respawn → lifecycle BP
- UI actor role → organism composition
- `requires_player_specific_effects` → player-specific biology
- Humanoid clade
- Sentience field
- Registration alone as B (B is earned only on proven encodeId routes)

---

## 9. Potential biological relationships

None earned. Do **not** queue `human` from player. Do **not** queue villager reassessment from this packet.

---

## 10. Final evidence conclusion

| Question | Answer |
|----------|--------|
| New BP field? | **No** |
| Existing composition? | **Yes** — identity keys on proven generic host/sample routes |
| Named consumer missing fact? | **No** |
| Escalation C? | **No** — **A + B** (B only for identity routes; actor/capture/effects remain A) |

Organism vs actor split is first-class and must survive synthesis.
