TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Goat (B) docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/goat.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Goat — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register or unregister Goat as a conclusion of this investigation.** Goat is already in `vanilla_hosts.living_biological`. Registration is participation, not extra biology.

Method (every behavior): existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied independently: shared parent ≠ clade; tag ≠ clade; spawn biome ≠ origin; Host Registry ≠ eligibility science; interesting behavior ≠ consumer; registered host ≠ extra biology; milking ≠ lactation trait; screaming flag ≠ biological subtype; horn flags ≠ anatomy field; live `contributingSourceKey=goat` ≠ C; same milk item as Cow ≠ shared lactation BP.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey` (Model A Chestburster/Drone), optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

This organism is investigated independently. Do **not** absorb Cow/Sheep as livestock clade. Do **not** treat fox/mooshroom/ocelot peer packets as evidence.

Default: **NO** new BP field. Live `contributingSourceKey=goat` is **B** (identity), not **C**.

---

## Subject

Goat (`minecraft:goat`, living Goat) — identity, Brain AI (ram / long-jump), screaming flag, horn flags / horn item drop, bucket milking, wheat-tag food/tempt/breed, CREATURE mountain-style spawn, Host Registry LIVE `living_biological` + `HostType.LIVING_BIOLOGICAL` + `baseline_biological`, and BioCraft gestation `contributingSourceKey` identity routing.

Out of scope as organisms: Cow, Sheep, Fox, Mooshroom, Ocelot. Cited only as **adjacency / negative control** where needed to reject leaps.

---

## Version

Minecraft Java **1.21.1** only. Mapped sources in `.tmp_mc_sources/` are authoritative. Wiki is orientation only; **source wins**.

Temporary source cache (not SSOT): `.tmp_mc_sources/`.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:goat` |
| `EntityType` | `EntityType.GOAT` — `EntityType.java` **405–407**: `register("goat", Builder.of(Goat::new, MobCategory.CREATURE).sized(0.9F, 1.3F).passengerAttachments(1.1125F).clientTrackingRange(10))` |
| Fire / lava | **No** `.fireImmune()` on GOAT. Builder default fireImmune is false. |
| Class | `Goat extends Animal` (`Goat.java` **56**) |
| Category | `MobCategory.CREATURE` |
| Summonable | Builder does **not** call `noSummon()` |
| Attributes | `DefaultAttributes.java` **119**: `EntityType.GOAT` → `Goat.createAttributes()`. Health **10.0**, movement **0.2F**, attack damage **2.0** (`Goat.java` **119–121**). Baby attack damage base **1.0** via `ageBoundaryReached` (**124–131**) |
| Dimensions | Adult hitbox **0.9 × 1.3**, passengerAttachments **1.1125F**. Long-jump pose: `LONG_JUMPING_DIMENSIONS` = scalable(0.9F, 1.3F).scale(0.7F) (`Goat.java` **57**, **255–257**) |
| Eye height | **Not** set on `EntityType.GOAT` builder (no `.eyeHeight(...)`). Default eye-height behavior is EntityType/Entity machinery — **not** inventing a BP field |
| Host Registry | **REGISTERED.** `hosts.json` `vanilla_hosts.living_biological.mobs` includes `"goat"` (line **9**). `default_dna`: `baseline_biological` (**4**). `variant_mappings` has **no** goat entry (**47–52**) |
| Suitability | Registered living_biological → suitable via `HostEligibilityService` → `MobHostRegistry.isSuitableForXenomorph`. Registered ≠ extra biology ≠ BP field |
| Inventory row (orientation only) | `vanilla_organism_inventory.md`: bio-organic, **registered**, `LIVING_BIOLOGICAL`, manifestation pending — not live consumer |

Independent existence paths (not origin): spawn egg, `/summon`, CREATURE biome spawn (Minecraft-owned; spawn biome ≠ origin), breeding `Goat.getBreedOffspring` → `EntityType.GOAT.create`.

```text
Goat does X
    → Minecraft entity / Animal / Brain / interact / spawn owns X?
    → Goat biological composition contributes something to X?
    → a live AlienCraft consumer needs that distinction beyond organismKey / contributingSourceKey?
```

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP representation? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|-----------------------------|--------------------|-------|
| Identity / dimensions / CREATURE | `EntityType.GOAT` | `EntityType.java` **405–407**: `"goat"`, `CREATURE`, `0.9F×1.3F`, passengerAttachments `1.1125F` | Identity only | `organismKey = goat` | Resolver / Analyzer / host registry lookup | **B** |
| Attributes / attack damage age gate | `Goat.createAttributes` + `ageBoundaryReached` | Health 10, speed 0.2, ADULT_ATTACK_DAMAGE 2 / BABY 1 (`Goat.java` **58–59**, **119–131**) | **No.** Vanilla stats | Not needed | None | **A** |
| Brain / sensors / memories | `Goat` + `GoatAi` | Sensor list incl. `GOAT_TEMPTATIONS`; memories for long-jump + ram (`Goat.java` **60–85**; `GoatAi.makeBrain`) | **No.** Entity AI | Identity sufficient | None | **A** |
| Food / tempt / breed item | `ItemTags.GOAT_FOOD` + `Goat.isFood` / `GoatAi.getTemptations` | Tag values: `minecraft:wheat` only; `isFood` → tag (`Goat.java` **211–213**; `goat_food.json`) | **No.** Item tag. Tag ≠ diet trait | Not needed | None | **A** |
| **Bucket milking** | `Goat.mobInteract` | Adult + `Items.BUCKET` → `Items.MILK_BUCKET` + `getMilkingSound()` (`Goat.java` **216–222**). Same outcome item as Cow path; **separate** class interact | **No.** Item interact. Same milk item ≠ shared lactation BP | Not needed | None | **A** |
| Fall damage reduction | `Goat.calculateFallDamage` | `super − 10` (`Goat.java` **86**, **135–137**). Constant `GOAT_FALL_DAMAGE_REDUCTION` | Numeric damage tweak | Not needed | None | **A** |
| Powder-snow path malus | `Goat` constructor | `PathType.POWDER_SNOW` / `DANGER_POWDER_SNOW` malus **−1.0F** (`Goat.java` **98–99**) | Movement/pathfinding | Not needed | None | **A** |
| Long jump activity | `GoatAi` + `LongJumpToRandomPos` / `LongJumpMidJump` | Cooldown `TIME_BETWEEN_LONG_JUMPS` 600–1200; height/width 5; velocity multiplier `3.5714288F`; pose `LONG_JUMPING` dims (`GoatAi.java` **46–49**, **114–136**; `Goat.java` **255–257**) | Movement AI | Not needed | None | **A** |
| Ram attack (combat) | `GoatAi` RAM activity + `PrepareRamNearestTarget` + `RamTarget` | Prepare 20 ticks; min/max distance 4–7; ram speed 3.0F; knockback adult 2.5 / baby 1.0; damage via `Attributes.ATTACK_DAMAGE`; targets non-goat living entities (`GoatAi.java` **38–57**, **139–172**; `RamTarget.java` **73–90**) | Combat AI | Not needed | None | **A** |
| Horn drop on block collision | `RamTarget` → `Goat.dropHorn` | Collision with `#snaps_goat_horn` → `dropHorn()` spawns `Items.GOAT_HORN` item entity (`RamTarget.java` **91–96**, **109–112**; `Goat.java` **314–338**) | World/item interaction | Not needed | None | **A** |
| Horn presence flags | `DATA_HAS_LEFT_HORN` / `DATA_HAS_RIGHT_HORN` | Synched + NBT `HasLeftHorn` / `HasRightHorn`; default both **true**; spawn unihorn 0.1 adult chance; baby `removeHorns`; adult `addHorns` (`Goat.java` **88–91**, **240–243**, **260–273**, **306–349**) | Presentation + drop eligibility | Not needed | Client `GoatModel` horn visibility only | **A** |
| **Screaming goat flag** | See dedicated probe below | Synched `DATA_IS_SCREAMING_GOAT`; NBT `IsScreamingGoat`; assignment/inheritance; ram cooldown + sounds + horn instrument tag | Vanilla entity state — **not** a BioCraft subtype without named consumer | Not needed as BP field | **None** named for screaming | **A** |
| Breeding / kid | `Goat.getBreedOffspring` + `AnimalMakeLove` | Offspring `EntityType.GOAT.create`; may set screaming per probe (`Goat.java` **164–174**; `GoatAi` IDLE love) | Vanilla same-type reproduction | Child key remains `goat` | None that needs breed/screaming trait | **A** |
| Entity loot | `loot_table/entities/goat.json` | Empty pools (`type: entity`, no pools). Horns are ram-drop items, not death loot | Loot absence | Not needed | None | **A** |
| Natural spawn floor | `Goat.checkGoatSpawnRules` + `#goats_spawnable_on` | Below block in tag + bright enough (`Goat.java` **363–367**; `SpawnPlacements` GOAT ON_GROUND). Tag includes `#animals_spawnable_on`, stone, snow, packed_ice, gravel | Spawn rule. Spawn biome ≠ origin | Not needed | None | **A** |
| Mountain biome spawn lists | `OverworldBiomes` | `EntityType.GOAT` CREATURE spawner data in mountain-style biome builders | Encounter placement | Not needed as origin | None | **A** |
| Client render / model | `GoatRenderer` + `GoatModel` | **One** texture `textures/entity/goat/goat.png`; horns visibility from horn flags; head rot from ram pose (`GoatRenderer.java` **12–19**; `GoatModel.java` **69–76**) | Presentation | Not needed | None | **A** |
| Datafix (legacy NBT) | `EntityGoatMissingStateFix` / `GoatHornIdFix` | Missing-state fix sets both horns true; horn id fix is item datafix — **not** gameplay biology | Migration only | N/A | None | **A** |
| **Live host → contributingSourceKey** | Host Registry + gestation + Analyzer | `"goat"` in `hosts.json` living_biological. `GestationManager.writeContributingSource` writes registry path onto Chestburster/Drone. Eligibility via `HostEligibilityService` | Source **identity** only. Not milk, ram, screaming, horns | Existing `contributingSourceKey` | **LIVE** named consumers: eligibility, gestation copy, Analyzer | **B** |

No row is **C**. Live `contributingSourceKey=goat` is identity already represented — not C.

---

## Required screaming-goat probe

| Question | 1.21.1 answer |
|----------|---------------|
| **Ownership** | Vanilla `Goat` entity state. Synched accessor `DATA_IS_SCREAMING_GOAT` (`Goat.java` **89**, **299–301**, **351–357**). **Not** a separate `EntityType`. **Not** a registry variant. |
| **Persistence** | Synched boolean + NBT key **`IsScreamingGoat`** written in `addAdditionalSaveData` / read in `readAdditionalSaveData` (`Goat.java` **260–270**). |
| **Spawn assignment** | `finalizeSpawn`: `setScreamingGoat(random.nextDouble() < 0.02)` — constant `GOAT_SCREAMING_CHANCE = 0.02` (`Goat.java` **87**, **235–238**). |
| **Breeding inheritance** | `getBreedOffspring`: pick **one** parent at random (`this` or partner); screaming if `(selected parent instanceof Goat && isScreamingGoat()) \|\| random < 0.02` (`Goat.java` **167–170`). Operator precedence: selected-parent screaming **OR** 2% roll — **not** “either parent screaming.” Partner screaming is ignored if not the selected parent. |
| **Behavioral / combat consequences** | `GoatAi`: ram cooldown after finish uses `TIME_BETWEEN_RAMS` (600–6000) vs `TIME_BETWEEN_RAMS_SCREAMER` (100–300) (`GoatAi.java` **50–51**, **145–146**). Prepare-fail cooldown min similarly branches (**157**). Impact / horn-break / prepare-ram / long-jump sounds branch on flag. **Knockback force and ram speed do not** branch on screaming (baby vs adult only for knockback). |
| **Initial ram memory nuance** | `GoatAi.initMemories` always samples **`TIME_BETWEEN_RAMS`** (not screamer range) for `RAM_COOLDOWN_TICKS` (`GoatAi.java` **59–61**). Screamer shorter cadence applies after ram finish / prepare-fail paths that consult the flag. |
| **Sound / rendering-only aspects** | Ambient, hurt, death, eat, milk, long-jump, prepare-ram, ram-impact, horn-break use screaming sound events when flag set (`Goat.java` **140–161**, **206–208**; `GoatAi` sound lambdas). **`GoatRenderer` uses one texture** — screaming is **not** a skin/variant texture. |
| **Horn instrument tag selection** | `createHorn()`: screaming → `InstrumentTags.SCREAMING_GOAT_HORNS` else `REGULAR_GOAT_HORNS` (`Goat.java` **102–106**). Tag contents: regular = ponder/sing/seek/feel; screaming = admire/call/yearn/dream. Parent tag `goat_horns` unions both. |
| **Breeding relevance** | Flag can be inherited via the selected-parent rule above; offspring is still `EntityType.GOAT`. No separate breed type. |
| **Live BioCraft consumption** | `rg -i goat` under `biocraft-alien` → **only** `hosts.json` key `"goat"`. **Zero** Java/test string consumers of screaming, horns, milk, or ram. No BioCraft field reads `IsScreamingGoat`. |
| **Subtype leap** | **Rejected.** Flag is vanilla state driving AI cadence / SFX / instrument loot mapping. Do **not** infer biological subtype / Genome / BP field from the flag alone without a named BioCraft consumer of a missing fact. |

**Probe outcome:** Screaming goat = **A** (vanilla-owned entity state with combat-cadence + presentation + instrument consequences). **Not B** as a distinct composition fact (identity remains `goat`). **Not C** (no named consumer needs a missing screaming fact).

---

## Configuration audit

Statuses used: **LIVE** / **STUB** / **PARSE-ONLY** / **DEAD** / **PLANNING** / **TEST** / **UNKNOWN**.

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` key `"goat"` under `vanilla_hosts.living_biological` | **LIVE** | `hosts.json` **9**; group `default_dna: baseline_biological` (**4**) | Registered participation. Can originate production contribution. **Not** a milk/ram/screaming/horn field |
| `variant_mappings` goat | **ABSENT** | No `"goat"` under `variant_mappings` (**47–52**) | No aggressive/neutral override |
| `HostEligibilityService` | **LIVE** generic | `isSuitableForXenomorph` / `isValidFacehuggerHost`: `encodeId` → `HostRegistryPaths.registryPath` (`minecraft:goat` → `goat`) → `MobHostRegistry` | Named live gate. Goat passes because registered `LIVING_BIOLOGICAL` |
| `MobHostRegistry.getHostType("goat")` | **LIVE** | Bound from hosts.json as `LIVING_BIOLOGICAL` | Participation lookup |
| `GestationManager.writeContributingSource` | **LIVE** | `GestationManager.java` **164–175**: spawn Chestburster then `encodeId(host)` → `HostRegistryPaths.registryPath` → `ContributingSourcePort.setContributingSourceKey` | **Production writer.** Gestated Goat host yields `contributingSourceKey="goat"`. Identity only. **Not C** |
| Analyzer / DNA projection | **LIVE** generic | Projects contributing source key when present; no goat-specific branch (`rg` zero goat Java hits) | Key projection, not screaming/milk/horns |
| Goat-named Java/resources/tests in `biocraft-alien` | **ABSENT** except hosts.json | `rg -i goat` → hosts.json only | No STUB/PARSE-ONLY/TEST goat hooks beyond registry participation |
| Goat entity JSON / DNA / behavior_type catalog | **ABSENT** | Not present as goat-named production biology | Vanilla remains behavior owner |
| Inventory / manifestation row | **PLANNING** | Inventory lists registered + pending; this packet does not edit it | Docs are not live consumers |

Consumer classification for this organism:

| Candidate | Classification |
|-----------|----------------|
| `BiologicalProfileResolver` / compiled profile | **LIVE** generic (not Goat-specific) |
| Analyzer / DNA-page projection | **LIVE** generic projection |
| Gestation `contributingSourceKey` | **LIVE** xenomorph machinery; Goat **origin allowed** (registered + suitable) |
| `HostEligibilityService` | **LIVE** registry gate; Goat eligible via `LIVING_BIOLOGICAL` |
| `hosts.json` goat row | **LIVE** participation |
| Screaming / horns / milk / ram consumers | **ABSENT** |
| Inventory `goat` row | **PLANNING** |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails on 1.21.1 evidence |
|----------------|--------------------------------|
| Live `contributingSourceKey=goat` earns C / a new BP field | Named consumers already take the organism-definition key. Identity only. **B, not C** |
| Milk Profile / lactation trait from bucket milking | `Goat.mobInteract` item swap → `MILK_BUCKET`. Same outcome as Cow does **not** imply shared lactation BP. No BioCraft milk consumer. **A** |
| Horn flags / horn item ⇒ anatomy BP field | Synched presentation + ram collision drop + instrument tags. No BioCraft anatomy consumer. **A** |
| Screaming ⇒ biological subtype / Genome / variant trait | Same `EntityType.GOAT`; one renderer texture; flag drives cooldown/SFX/instrument. No BioCraft named consumer of the flag. **Do not subtype from flag alone.** **A** |
| Livestock clade with Cow/Sheep (shared milk / wheat / Animal) | Shared parent/item adjacency ≠ clade. Distinct registry keys. This packet does not form a livestock column. **Closed leap** |
| Mountain spawn / long jump / powder-snow ⇒ mountain-adapted BP | Spawn rules + movement AI. Spawn biome ≠ origin. No BioCraft adaptation consumer. **A** |
| Host Registry registration = extra Goat dossier / eligibility science | Registration enables existing host path. Suitability is `HostType.LIVING_BIOLOGICAL`. Not ram/screaming/milk field |
| Interesting mountain combat earns C | Interesting ≠ consumer. No named live consumer needs a missing Goat biological fact |
| Empty entity loot ⇒ missing BioCraft drop profile | Horns come from `dropHorn` on `#snaps_goat_horn` collision, not death loot. Vanilla ownership |

---

## Potential biological relationships

### 1. Goat as live xenomorph host / Model A contributing source

- **Relationship:** Facehugger/ovomorph may select Goat; gestation copies host registry path onto Chestburster/Drone; Analyzer displays it.
- **Owner:** `hosts.json` + `HostEligibilityService` + `GestationManager.writeContributingSource` + Analyzer projection.
- **Biological input?** Only the organism-definition key `"goat"`.
- **Existing composition:** `organismKey` on the Goat sample; optional `contributingSourceKey="goat"` on Model A offspring. `HostType.LIVING_BIOLOGICAL` + `hostEffectProfileId=baseline_biological` already resolve.
- **Named consumer:** **LIVE** — eligibility, gestation writer, Analyzer.
- **Result:** **B**. Not C.

### 2. Screaming goat state

- **Relationship:** Rare spawn/breed flag altering ram cadence, sounds, and dropped horn instruments.
- **Owner:** `Goat` synched/NBT + `GoatAi` / `createHorn`.
- **Biological input?** Vanilla entity state. Not a BioCraft subtype without a named consumer.
- **Existing composition:** Identity remains `goat`; flag not represented in BP (and not needed).
- **Named consumer:** None in BioCraft.
- **Result:** **A**.

### 3. Adult bucket milking

- **Relationship:** Player uses empty bucket on adult Goat → milk bucket (screaming-aware milk SFX).
- **Owner:** `Goat.mobInteract` (`Goat.java` **216–222**).
- **Biological input?** No. Item interact. Same milk item as Cow ≠ shared lactation composition.
- **Named consumer:** None.
- **Result:** **A**.

### 4. Ram / horn drop / long jump / powder snow / mountain spawn

- **Relationship:** Combat AI, item drop on tagged blocks, movement, spawn floors/biomes.
- **Owner:** `GoatAi`, `RamTarget`, `LongJump*`, constructor path malus, `checkGoatSpawnRules` / biome spawn lists.
- **Biological input?** No for BP.
- **Named consumer:** None.
- **Result:** **A**.

### 5. Goat ↔ Cow (adjacency only / negative control)

- **Relationship:** Both milk to `MILK_BUCKET` via bucket interact; both wheat-tagged food; both `Animal` / CREATURE.
- **Owner:** Separate classes and EntityTypes.
- **Biological input?** Shared outcome ≠ shared lactation BP; shared parent ≠ clade.
- **Named consumer:** None that needs a livestock-family field.
- **Result:** **A**. Do **not** form livestock column.

**C is not earned for any relationship.**

---

## Tag probe (membership → 1.21.1 consumer → behavior → biological meaning? → BioCraft consumer?)

| Tag / surface | Goat member / role? | Named 1.21.1 consumer | Behavior | Biological meaning for BP? | BioCraft consumer? |
|---------------|---------------------|----------------------|----------|----------------------------|--------------------|
| `#item/goat_food` | Food tag (wheat) | `Goat.isFood`, temptations | Tempt/breed | Item food gate | None |
| `#block/goats_spawnable_on` | Spawn floor list | `Goat.checkGoatSpawnRules` | Natural spawn | Spawn rule | None |
| `#block/snaps_goat_horn` | Collision blocks | `RamTarget.hasRammedHornBreakingBlock` | Horn snap drop | World interact | None |
| `#instrument/regular_goat_horns` | Non-screaming drop pool | `Goat.createHorn` | Instrument on horn item | Item mapping | None |
| `#instrument/screaming_goat_horns` | Screaming drop pool | `Goat.createHorn` | Instrument on horn item | Item mapping | None |
| `#instrument/goat_horns` | Union of both | `Items.GOAT_HORN` InstrumentItem tag | Item definition | Item mapping | None |
| Entity-type undead/aquatic/etc. | **No goat hits** under `.tmp_mc_sources/.../tags/entity_type` for goat string this pass | N/A | N/A | Do not invent membership | None |

---

## Wiki orientation

Wiki not fetched this pass. Orientation only; **1.21.1 mapped source wins**.

| Common orientation | 1.21.1 authority | Conclusion |
|--------------------|------------------|------------|
| Screaming goat is a separate mob / subtype | Same `EntityType.GOAT`; boolean flag + NBT | **Not** a BioCraft subtype without consumer |
| Screaming has unique texture | `GoatRenderer` single `goat.png` | SFX/AI/instrument only for visuals beyond horns |
| 2% screaming spawn | `GOAT_SCREAMING_CHANCE = 0.02` in `finalizeSpawn` | **Agrees** |
| Screaming kids if either parent screams | Code picks **one** random parent; that parent screaming OR 2% | Nuance: not both-parent OR |
| Bucket milk like cows | Separate `Goat.mobInteract` → same `MILK_BUCKET` | Same outcome ≠ shared BP |
| Horns drop from killing | Entity loot empty; drop via ram into `#snaps_goat_horn` | Combat/world interact **A** |

---

## Final stop gate

Goat is a 1.21.1 `Animal` creature identity (`minecraft:goat`, 0.9×1.3, CREATURE, not fire-immune). Minecraft owns Brain AI (ram/long-jump), screaming flag, horn flags, milking, food/tempt, breeding, fall/powder-snow movement tweaks, spawn rules, sounds, and horn item creation.

BioCraft already registers `goat` as `LIVING_BIOLOGICAL` / `baseline_biological` and can write `contributingSourceKey=goat` on Model A carriers. That consumer asks only for the existing organism-definition key. No Java/test code in `biocraft-alien` references goat beyond `hosts.json`.

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** |
| Named consumer exists | **YES** (live host/gestation/Analyzer identity-source path). **NO** named consumer of a **missing** Goat biological fact |
| Architectural escalation required | **NO** |

**Stop.** A = vanilla ownership (milk / ram / screaming / horns / jump / spawn); B = existing identity/composition including live Model A source identity; C = not earned. Do **not** change Host Registry. Do **not** mint Milk Profile, horn anatomy, screaming subtype, or livestock clade. Do **not** mint `DESIGN-BIO-MANIFEST-004`. Do **not** treat registration or live `contributingSourceKey=goat` as C.

### A/B/C summary

- **A:** milking, `#goat_food` / tempt, breeding/kid, attributes/sounds, Brain ram/long-jump, horn flags + horn drop + instrument tags, screaming flag (persistence/assignment/cooldown/SFX/instruments), fall reduction, powder-snow path malus, spawn rules/biomes, empty entity loot, client single-texture render, datafixers.
- **B:** registry identity `organismKey=goat` (LIVE registered); `HostType.LIVING_BIOLOGICAL`; `hostEffectProfileId=baseline_biological`; optional Model A `contributingSourceKey=goat` already representable (**identity only** — proved: gestation writer + eligibility consume registry path string only; no screaming/milk/horn fields read).
- **C:** **none** / **not earned**.

### UNKNOWNs

- Exact default eye-height numeric for Goat when builder omits `.eyeHeight(...)` — not read from EntityType default math this pass; **UNKNOWN** as a literal; irrelevant to A/B/C (presentation, not BP).
- Full mountain biome id list for every Goat spawner entry beyond confirming `OverworldBiomes` adds `EntityType.GOAT` — spawn placement detail; spawn ≠ origin; not load-bearing for C.
- No load-bearing Phase 0 source was missing for ownership conclusions above.

### 1.21.1 authority anchors

- `.tmp_mc_sources/net/minecraft/world/entity/animal/goat/Goat.java`
- `.tmp_mc_sources/net/minecraft/world/entity/animal/goat/GoatAi.java`
- `.tmp_mc_sources/net/minecraft/world/entity/ai/behavior/RamTarget.java`
- `.tmp_mc_sources/net/minecraft/world/entity/ai/behavior/PrepareRamNearestTarget.java`
- `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` **405–407**
- `.tmp_mc_sources/net/minecraft/world/entity/ai/attributes/DefaultAttributes.java` **119**
- `.tmp_mc_sources/data/minecraft/loot_table/entities/goat.json` (empty)
- `.tmp_mc_sources/data/minecraft/tags/item/goat_food.json`, `tags/block/goats_spawnable_on.json`, `tags/block/snaps_goat_horn.json`, `tags/instrument/{regular,screaming,goat}_horns.json`
- AlienCraft: `biocraft-alien/.../systems/hosts.json`; `HostEligibilityService.java`; `GestationManager.java` `writeContributingSource` **164–175**; `HostRegistryPaths.java`
