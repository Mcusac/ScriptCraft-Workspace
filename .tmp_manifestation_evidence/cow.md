TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Cow docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/cow.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Cow — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register or unregister Cow as a conclusion of this investigation.** Cow is already in `vanilla_hosts.living_biological`. Registration is participation, not extra biology.

Method (every behavior): existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied independently: shared parent ≠ clade; tag ≠ clade; conversion ≠ inheritance; spawn biome ≠ origin; Host Registry ≠ eligibility science; interesting behavior ≠ consumer; registered host ≠ extra biology; `MushroomCow extends Cow` ≠ Cow ancestry; milking ≠ lactation trait; live `contributingSourceKey=cow` ≠ C.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey` (Model A Chestburster/Drone), optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

This organism is investigated independently. Do **not** absorb Mooshroom as Cow biology. Do **not** form a bovine column with Goat. Do **not** share architectural decisions with Horse/Villager except the already-named identity-source contract.

Default: **NO** new BP field. Live `contributingSourceKey=cow` is **B** (identity), not **C**.

---

## Subject

Cow (`minecraft:cow`, living Cow) — identity, adult bucket-milking, wheat-tag food/tempt/breed, same-type calf, CREATURE spawn/summon, Host Registry LIVE `living_biological` + `HostType.LIVING_BIOLOGICAL` + `baseline_biological`, and BioCraft gestation `contributingSourceKey` identity routing.

SPRINT Cow vs Human `contributingSourceKey` playtest is **TEST/PLAYTEST, identity only** — not a Cow anatomy/lactation/phenotype field.

Out of scope as organisms: Mooshroom (`minecraft:mooshroom`), Goat, Horse, Villager, Human (`biocraft_alien:human`). Mooshroom is cited only as **adjacency / negative control**.

---

## Version

Minecraft Java **1.21.1** only. Mapped sources in `.tmp_mc_sources/` are authoritative. Wiki is orientation and disagreement discovery only; **source wins**.

Temporary source cache (not SSOT): `.tmp_mc_sources/`.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:cow` |
| `EntityType` | `EntityType.COW` — `EntityType.java` **270–272**: `register("cow", Builder.of(Cow::new, MobCategory.CREATURE).sized(0.9F, 1.4F).eyeHeight(1.3F).passengerAttachments(1.36875F).clientTrackingRange(10))` |
| Fire / lava | **No** `.fireImmune()` on COW. Builder default fireImmune is false. |
| Class | `Cow extends Animal` (`Cow.java` **34**) |
| Category | `MobCategory.CREATURE` |
| Summonable | Builder does **not** call `noSummon()` |
| Attributes | `DefaultAttributes` binds `EntityType.COW` → `Cow.createAttributes()` (`DefaultAttributes.java` **103**). `Cow.createAttributes` (`Cow.java` **61–63**): `MAX_HEALTH` **10.0**, `MOVEMENT_SPEED` **0.2F** |
| Dimensions | Adult hitbox **0.9 × 1.4**, eyeHeight **1.3**, passengerAttachments **1.36875F**. Baby: `BABY_DIMENSIONS` = `EntityType.COW.getDimensions().scale(0.5F).withEyeHeight(0.665F)` (`Cow.java` **35**, **109–111**) |
| Host Registry | **REGISTERED.** `hosts.json` `vanilla_hosts.living_biological.mobs` includes `"cow"` (**6**). `default_dna`: `baseline_biological` (**4**). `variant_mappings` has **no** cow entry (**47–52**). `"mooshroom"` is **absent** from `hosts.json` |
| Suitability | Registered living_biological → currently suitable for xenomorph hosting via `HostEligibilityService` → `MobHostRegistry.isSuitableForXenomorph`. Registered ≠ extra biology ≠ BP field |
| Distinct non-merge | `EntityType.MOOSHROOM` register `"mooshroom"` — `EntityType.java` **502–505**: `Builder.of(MushroomCow::new, MobCategory.CREATURE).sized(0.9F, 1.4F).eyeHeight(1.3F).passengerAttachments(1.36875F).clientTrackingRange(10)`. Same adult size literals; **different** registry id and factory. `MushroomCow extends Cow` is Java parent sharing, not ancestry |

Independent existence paths (not origin): spawn egg, `/summon` (`canSummon` default true), CREATURE biome spawn (Minecraft-owned; spawn biome ≠ origin), breeding `Cow.getBreedOffspring` → `EntityType.COW.create`. Mooshroom shear **destination** is also `EntityType.COW.create` — conversion ≠ inheritance; do not treat as Cow biology.

Adjacent vanilla type (identity / negative control only; **not** investigated here as an organism):

| Type | 1.21.1 fact | This packet’s use |
|------|-------------|-------------------|
| `EntityType.MOOSHROOM` | Distinct key `"mooshroom"`; `MushroomCow extends Cow`; bowl-stew interact; shear → `EntityType.COW.create`; offspring `EntityType.MOOSHROOM.create`; **not** in `hosts.json` | Do **not** absorb Mooshroom as Cow biology. Shared parent ≠ clade. Conversion destination ≠ ancestry |

```text
Cow does X
    → Minecraft entity / Animal / interact / spawn owns X?
    → Cow biological composition contributes something to X?
    → a live AlienCraft consumer needs that distinction beyond organismKey / contributingSourceKey?
```

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP representation? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|----------------------------|--------------------|-------|
| Identity / dimensions / CREATURE | `EntityType.COW` | `EntityType.java` **270–272**: `"cow"`, `CREATURE`, `0.9F×1.4F`, eyeHeight `1.3F` | Identity only | `organismKey = cow` | Resolver / Analyzer / host registry lookup | **B** |
| Goals / panic / stroll | `Cow.registerGoals` | Float, Panic **2.0**, Breed **1.0**, Tempt **1.25** `#cow_food`, FollowParent **1.25**, WaterAvoidingRandomStroll **1.0**, LookAtPlayer **6.0F**, RandomLookAround (`Cow.java` **42–51**) | **No.** Entity AI | Identity sufficient | None | **A** |
| Food / tempt | `Cow.isFood` + `TemptGoal` | `stack.is(ItemTags.COW_FOOD)` (`Cow.java` **57–59**, **46**) | **No.** Item tag. Tag ≠ diet trait | Not needed | None | **A** |
| Attributes / sounds | `Cow.createAttributes` + sound overrides | Health **10**, speed **0.2F** (`Cow.java` **61–63**). Ambient/hurt/death/step; volume **0.4F** (`Cow.java` **66–88**) | **No.** Vanilla stats/SFX | Not needed | None | **A** |
| **Milking** | `Cow.mobInteract` | Adult + `Items.BUCKET` → `Items.MILK_BUCKET` + `SoundEvents.COW_MILK` (`Cow.java` **91–100**). Babies cannot milk (`!this.isBaby()`). Super handles love/food | **No.** Item interact. Milking ≠ lactation BP field | Not needed | None | **A** |
| **Breeding / calf** | `Cow.getBreedOffspring` + `BreedGoal` / `Animal` | Offspring is `EntityType.COW.create(level)` (`Cow.java` **104–106**). Same-type vanilla `AgeableMob` path | Vanilla reproduction of same `EntityType`. Not xenomorph contribution | Identity sufficient; child is still `cow` | None that needs a breed trait | **A** |
| Baby dimensions | `Cow.getDefaultDimensions` | Scale **0.5**, eyeHeight **0.665F** (`Cow.java` **35**, **109–111**) | Age/pose presentation | Entity baby flag | None | **A** |
| **Spawn / summon / egg** | `EntityType` + worldgen / items | `CREATURE` builder; summon default true. Encounter placement is Minecraft-owned. **Spawn biome ≠ origin.** Egg/summon/breed also exist | **No** | Not an origin field | None | **A** |
| Java parent `Animal` | Class inheritance | Shared with many creatures | Shared parent ≠ clade | Distinct keys | None | **A** |
| Mooshroom Java parent | `MushroomCow extends Cow` | `MushroomCow.java` **45**. Separate `EntityType.MOOSHROOM` **502–505** | Implementation sharing ≠ ancestry | Distinct keys `cow` vs `mooshroom` | None | **A** |
| Mooshroom bowl “milk” | `MushroomCow.mobInteract` | Bowl → mushroom/suspicious stew, **not** `Items.BUCKET` / `MILK_BUCKET` (`MushroomCow.java` **89–113**). Falls through to `super.mobInteract` only for non-bowl/non-flower cases (**162–163**) | Mooshroom interact, not Cow biology | Do not merge | None | **A** |
| Mooshroom shear → Cow | **`MushroomCow.shear`** | `EntityType.COW.create` then copy pose/health/name and `discard` Mooshroom (`MushroomCow.java` **168–183**). Conversion ≠ inheritance | Cow is a **destination** of Mooshroom shear, not Cow composition | Distinct keys already | None in BioCraft | **A** |
| Mooshroom offspring | `MushroomCow.getBreedOffspring` | `EntityType.MOOSHROOM.create(level)` (`MushroomCow.java` **245–246**) | Mooshroom stays Mooshroom | Distinct key | None | **A** |
| Lightning on Mooshroom | `MushroomCow.thunderHit` | Red↔brown variant swap (`MushroomCow.java` **73–79**). Does **not** create Cow | Mooshroom variant, not Cow | N/A | None | **A** |
| **Live host → contributingSourceKey** | Host Registry + gestation + Analyzer | See Configuration audit. `hosts.json` `"cow"` → living_biological. `GestationManager.writeContributingSource` writes registry path `"cow"` onto Chestburster/Drone. SPRINT Cow vs Human is identity differencing only | Source **identity** only. Not milk, not calf, not Mooshroom | Existing `contributingSourceKey` | **LIVE** named consumers: eligibility, gestation copy, Analyzer. Playtest is **TEST/PLAYTEST** | **B** |

No row is **C**. Live `contributingSourceKey=cow` is identity already represented — not C.

---

## Configuration audit

Statuses used: **LIVE** / **STUB** / **PARSE-ONLY** / **DEAD** / **PLANNING** / **TEST** / **UNKNOWN**.

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` key `"cow"` under `vanilla_hosts.living_biological` | **LIVE** | `hosts.json` **6**; group `default_dna: baseline_biological` (**4**) | Registered participation. Can originate production contribution. **Not** a milk/breed/Mooshroom field |
| `hosts.json` key `"mooshroom"` | **ABSENT** | No `"mooshroom"` in `hosts.json` (full file read) | Unregistered ≠ merge into Cow. Do not register from this packet |
| `hosts.json` key `"human"` | **LIVE** separate key | `modded_hosts.biocraft_alien.living_biological` `"human"` (`hosts.json` **40–44**) | Distinct from `"cow"`. SPRINT Cow vs Human compares these **keys**, not anatomy |
| `variant_mappings` cow | **ABSENT** | No `"cow"` under `variant_mappings` (`hosts.json` **47–52**) | No aggressive/neutral override |
| `HostEligibilityService` | **LIVE** generic | `isSuitableForXenomorph` / `isValidFacehuggerHost` (`HostEligibilityService.java` **19–45**): `encodeId` → `HostRegistryPaths.registryPath` (`minecraft:cow` → `cow`) → `MobHostRegistry` | Named live gate. Cow passes because registered `LIVING_BIOLOGICAL`. Mooshroom path `mooshroom` is unregistered → not this packet’s host |
| `GestationManager.writeContributingSource` | **LIVE** | `GestationManager.java` **147–175**: spawn Chestburster then `encodeId(host)` → `HostRegistryPaths.registryPath` → `ContributingSourceKeys.absentIfBlank` → `ContributingSourcePort.setContributingSourceKey` | **Production writer.** A gestated Cow host yields `contributingSourceKey="cow"` on Model A carriers. Same machinery as Villager/Human. Identity only. **Not C** |
| Analyzer / DNA projection | **LIVE** generic | SPRINT implemented consumers: Model A `contributingSourceKey` on Chestburster/Drone; Analyzer + DNA-page projection (`FEATURE-DNA-003` / `FEATURE-DNA-UI-002`) | Projects the key. Does not need milk, calf, or Mooshroom facts |
| Cow vs Human source differencing | **TEST** + **PLAYTEST** | SPRINT `DESIGN-BIO-CONSEQUENCE-001`: fact `contributingSourceKey` differs (Cow vs Human; Bat playtested). Owner in-game playtest remains the gameplay gate. Automated tests = contract confidence | **Identity only.** Do not mint phenotype/anatomy/`Genome`/004 for this slice |
| Cow entity JSON / DNA / behavior_type in BioCraft | **ABSENT** | Not in listed host/gestation/eligibility sources as a Cow-named catalog | Vanilla remains behavior owner |
| Inventory / manifestation row | **PLANNING** | Planning inventory is not edited by this packet | Docs are not live consumers |

Consumer classification for this organism:

| Candidate | Classification |
|-----------|----------------|
| `BiologicalProfileResolver` / compiled profile | **LIVE** generic (not Cow-specific) |
| Analyzer / DNA-page projection | **LIVE** generic projection |
| Gestation `contributingSourceKey` | **LIVE** xenomorph machinery; Cow **origin allowed** (registered + suitable) |
| `HostEligibilityService` | **LIVE** registry gate; Cow eligible via `LIVING_BIOLOGICAL` |
| `hosts.json` cow row | **LIVE** participation |
| Cow vs Human lab slice | **TEST** (contract) / **PLAYTEST** (owner Minecraft gate; identity only) |
| Cow production JSON | **ABSENT** |
| Inventory `cow` row | **PLANNING** |
| Mooshroom as Cow host/source | **ABSENT** (unregistered; do not absorb) |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails on 1.21.1 evidence |
|----------------|--------------------------------|
| Live `contributingSourceKey=cow` earns C / a new BP field | Named consumers already take the organism-definition key. SPRINT forbids adding phenotype, anatomy, trait registry, `Genome`, or 004 for the Cow vs Human proof. **B, not C** |
| Bucket milking is Cow biology / a lactation trait | `Cow.mobInteract` item swap. No BioCraft consumer of milk as composition. **A** |
| Breeding / wheat food is a diet or genetics field | `#cow_food` + `BreedGoal` + `EntityType.COW.create`. Tag ≠ diet trait. Same-type calf. **A** |
| CREATURE spawn biomes are organism origin | Encounter placement. Egg/summon/breed also exist. Spawn biome ≠ origin. **A** |
| `MushroomCow extends Cow` means Mooshroom is Cow / Cow ancestry | Shared **Java parent**. Distinct `EntityType.MOOSHROOM` `"mooshroom"`. Offspring is Mooshroom. Mooshroom **not** in `hosts.json`. Shared parent ≠ clade |
| Mooshroom shear → Cow is ancestry or a conversion-source clade | `MushroomCow.shear` replaces Mooshroom with `EntityType.COW`. Conversion ≠ inheritance. Cow does **not** convert to Mooshroom in `Cow.java` |
| Mooshroom bowl stew is Cow milking | Different item (`BOWL` vs `BUCKET`), different products (stew vs `MILK_BUCKET`), Mooshroom sounds. Not Cow `mobInteract` |
| Host Registry registration = extra eligibility science or a Cow dossier | Registration enables the existing host path. Suitability is `HostType.LIVING_BIOLOGICAL`. Not a milk/breed field |
| Cow vs Human playtest needs Cow anatomy so Analyzer can differ | SPRINT: the **fact** is the key differs. Enacting systems already exist. Identity only |
| Same size literals as Mooshroom = same organism | Registration duplication ≠ clade. Factories and registry ids differ |
| Interesting farm-animal behavior earns C | Interesting ≠ consumer. No named live consumer needs a missing Cow biological fact |

---

## Potential biological relationships

### 1. Cow as live xenomorph host / Model A contributing source

- **Relationship:** Facehugger/ovomorph may select Cow; gestation copies host registry path onto Chestburster/Drone; Analyzer displays it; SPRINT playtests Cow vs Human key difference.
- **Owner:** `hosts.json` + `HostEligibilityService` + `GestationManager.writeContributingSource` + Analyzer projection.
- **Biological input?** Only the organism-definition key `"cow"`.
- **Existing composition:** `organismKey` on the Cow sample; optional `contributingSourceKey="cow"` on Model A offspring. `HostType.LIVING_BIOLOGICAL` + `hostEffectProfileId=baseline_biological` already resolve.
- **Named consumer:** **LIVE** — eligibility, gestation writer, Analyzer. Playtest classification **TEST/PLAYTEST**, identity only.
- **Result:** **B**. Not C.

### 2. Adult bucket milking

- **Relationship:** Player uses empty bucket on adult Cow → milk bucket.
- **Owner:** `Cow.mobInteract` (`Cow.java` **91–100**).
- **Biological input?** No. Item interact.
- **Existing composition:** Not needed.
- **Named consumer:** None in BioCraft.
- **Result:** **A**.

### 3. Breeding / calf

- **Relationship:** Love + `#cow_food`; offspring Cow.
- **Owner:** `BreedGoal` + `Cow.getBreedOffspring` (`Cow.java` **45**, **104–106**).
- **Biological input?** Vanilla same-type reproduction.
- **Existing composition:** Child key remains `cow`.
- **Named consumer:** None.
- **Result:** **A**.

### 4. Spawn / summon / egg

- **Relationship:** Natural CREATURE spawn, spawn egg, `/summon`.
- **Owner:** `EntityType.COW` + Minecraft spawn/item systems.
- **Biological input?** No. Spawn biome ≠ origin.
- **Existing composition:** Not needed as origin.
- **Named consumer:** None.
- **Result:** **A**.

### 5. Cow ↔ Mooshroom (adjacency only)

- **Relationship:** Java subclass; identical adult size literals; shear converts Mooshroom **to** Cow; Mooshroom breeds Mooshroom.
- **Owner:** `MushroomCow` + `EntityType.MOOSHROOM`. Cow.java has **no** Mooshroom branch.
- **Biological input?** Shared parent ≠ clade. Conversion ≠ inheritance.
- **Existing composition:** Distinct keys. Mooshroom unregistered as host.
- **Named consumer:** None that needs a bovine-family field. **Do not absorb Mooshroom.**
- **Result:** **A**. Mooshroom ≠ Cow ancestry.

**C is not earned for any relationship.**

---

## Wiki orientation disagreements

Wiki not fetched this pass. Orientation only; **1.21.1 mapped source wins**.

| Common orientation | 1.21.1 authority | Conclusion |
|--------------------|------------------|------------|
| Mooshroom is a Cow variant / same organism | Distinct `EntityType.MOOSHROOM` `"mooshroom"`; `MushroomCow extends Cow` is Java sharing | **Do not merge.** Shared parent ≠ clade |
| Cow milking / wheat breeding as biological identity | `mobInteract` bucket swap; `ItemTags.COW_FOOD`; `EntityType.COW.create` | Gameplay **A**. Identity is the registry key |
| Health 10 | `Cow.createAttributes` `MAX_HEALTH` **10.0** | **Agrees** |
| Adult bucket → milk bucket; babies cannot be milked | `itemstack.is(Items.BUCKET) && !this.isBaby()` | **Agrees** |
| Shear Mooshroom becomes Cow | `MushroomCow.shear` → `EntityType.COW.create` | Conversion **destination**, not Cow ancestry |
| Cow vs Human as a genetics/phenotype sprint | SPRINT `DESIGN-BIO-CONSEQUENCE-001`: keys differ; do not add phenotype/anatomy/`Genome`/004 | Identity **B** / **TEST/PLAYTEST** only |

---

## Final stop gate

Cow is a 1.21.1 `Animal` creature identity (`minecraft:cow`, 0.9×1.4, eyeHeight 1.3, not fire-immune). Minecraft owns milking, food/tempt, breeding, baby size, goals, sounds, and spawn/summon. Mooshroom is a **different** EntityType; Java subclass + shear conversion do **not** make Mooshroom Cow ancestry.

BioCraft already registers `cow` as `LIVING_BIOLOGICAL` / `baseline_biological` and can write `contributingSourceKey=cow` on Model A carriers. That consumer asks only for the existing organism-definition key. SPRINT Cow vs Human is **TEST/PLAYTEST, identity only**.

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** |
| Named consumer exists | **YES** (live host/gestation/Analyzer identity-source path). **NO** named consumer of a **missing** Cow biological fact |
| Architectural escalation required | **NO** |

**Stop.** A = vanilla ownership (milking / breeding / spawn); B = existing identity/composition including live Model A source identity; C = not earned. Do **not** change Host Registry. Do **not** mint a Cow/milk/breed/Mooshroom Profile. Do **not** absorb Mooshroom. Do **not** treat registration or live `contributingSourceKey=cow` as C.

### A/B/C summary

- **A:** milking, `#cow_food` / tempt, breeding/calf, baby dimensions, goals, attributes/sounds, CREATURE spawn/summon, `Animal` parent, Mooshroom adjacency (subclass, stew, shear→Cow, Mooshroom offspring).
- **B:** registry identity `organismKey=cow` (LIVE registered); `HostType.LIVING_BIOLOGICAL`; `hostEffectProfileId=baseline_biological`; optional Model A `contributingSourceKey=cow` already representable (identity only, not milk/anatomy). Cow vs Human playtest is this B.
- **C:** none.

### 1.21.1 authority anchors

- `.tmp_mc_sources/net/minecraft/world/entity/animal/Cow.java` — class, goals, food, attributes, sounds, milking, offspring, baby dimensions
- `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` **270–272** (`COW`), **502–505** (`MOOSHROOM`)
- `.tmp_mc_sources/net/minecraft/world/entity/ai/attributes/DefaultAttributes.java` **103**
- `.tmp_mc_sources/net/minecraft/world/entity/animal/MushroomCow.java` — adjacency only (extends Cow; stew; shear→Cow; `MOOSHROOM` offspring)
- AlienCraft: `hosts.json`; `HostEligibilityService.java`; `GestationManager.java` `writeContributingSource` **164–175**; `docs/development/SPRINT.md` Cow vs Human `DESIGN-BIO-CONSEQUENCE-001`
