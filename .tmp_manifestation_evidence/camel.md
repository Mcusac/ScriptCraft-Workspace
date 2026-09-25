TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Camel docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/camel.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Camel — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not register Camel as a conclusion of this investigation.** Camel is **ABSENT** from `hosts.json`. Unregistered ≠ missing biology ≠ permission to register.

Method (every behavior): existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps: shared `AbstractHorse` ≠ clade; sit/dash/ride ≠ movement/size/mount BP fields; tag ≠ diet; spawn ≠ origin; unregistered ≠ C; camel_husk post-1.21.1 ≠ this organism; interesting mount ≠ consumer.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey`, optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

Do **not** absorb Donkey, Mule, Horse, or camel_husk. Do **not** share architectural decisions with Cat/Chicken except the shared A/B/C method.

Default: **NO** new BP field. Unregistered identity remains fail-soft `organismKey=camel` **B**.

---

## Subject

Camel (`minecraft:camel`) — sitting/standing pose FSM, dash jump, dual passenger ride, cactus food/breeding, desert village encounter, `AbstractHorse` inheritance, Host Registry **ABSENCE**, and BioCraft consumers.

Out of scope as organisms: Horse, Donkey, Mule, camel_husk (no 1.21.1 organism), Cat, Chicken.

---

## Version

Minecraft Java **1.21.1** only. Mapped sources in `.tmp_mc_sources/` are authoritative. Wiki is orientation only; **source wins**.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:camel` |
| `EntityType` | `EntityType.CAMEL` — `EntityType.java` **236–238**: `register("camel", Builder.of(Camel::new, MobCategory.CREATURE).sized(1.7F, 2.375F).eyeHeight(2.275F).clientTrackingRange(10))` |
| Fire / lava | **No** `.fireImmune()` |
| Class | `Camel extends AbstractHorse implements PlayerRideableJumping, Saddleable` (`Camel.java` **53**) |
| Category | `MobCategory.CREATURE` |
| Summonable | Builder does **not** call `noSummon()` |
| Attributes | `Camel.createAttributes` (**106–112**): health **32**, movement **0.09F**, jump **0.42F**, step height **1.5** via `createBaseHorseAttributes()` |
| Dimensions | Adult **1.7 × 2.375**, eyeHeight **2.275**. Sitting: height − **1.43F**, eyeHeight **0.845F** (`SITTING_DIMENSIONS`, **72–73**). Baby age scale **0.45F** (**54**, **492–494**) |
| Host Registry | **ABSENT.** `hosts.json` living_biological list has horse/donkey/mule/llama but **no** `"camel"` (**6–10**). Do **not** register from this packet |
| Suitability | Unregistered → not a live xenomorph host via current registry path |

```text
Camel does X
    → Minecraft entity / AbstractHorse / brain / ride owns X?
    → Camel biological composition contributes something to X?
    → a live AlienCraft consumer needs that distinction beyond organismKey?
```

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP representation? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|----------------------------|--------------------|-------|
| Identity / CREATURE / size | `EntityType.CAMEL` | `EntityType.java` **236–238** | Identity only | `organismKey = camel` | Generic resolver (fail-soft) | **B** |
| `AbstractHorse` parent | class hierarchy | Shared with Horse/Donkey/Mule/undead horses | Shared parent ≠ clade | Distinct keys | None for ancestry | **A** |
| Brain / AI | `CamelAi` | Empty `registerGoals`; brain CORE+IDLE; `RandomSitting`, panic stands up (`CamelAi.java`) | Entity AI | Identity sufficient | None | **A** |
| Sit / stand pose | `LAST_POSE_CHANGE_TICK` + `Pose.SITTING` | `sitDown` / `standUp` / `refuseToMove` (`Camel.java` **242–244**, **554–593**) | Pose/state FSM | Not a movement BP field | None | **A** |
| Dash / jump | `PlayerRideableJumping` + `executeRidersJump` | Cooldown **55**; dash sync `DASH`; requires saddle + ground (`Camel.java` **268–293**) | Ride API | Not a jump trait | None | **A** |
| Riding / 2 passengers | `mobInteract` + `canAddPassenger` | Adults: up to **2** passengers (`Camel.java` **364–366**, **544–546**) | Mount API | Not a mountability field | None | **A** |
| Always “tamed” | `isTamed()` override | Returns **true** (`Camel.java` **623–625**) | Horse-tame flag override | Not domestication biology | None | **A** |
| Food / breed | `#camel_food` + `canMate` | Cactus only (`camel_food.json`); mate only other Camel (`Camel.java` **347–455**) | Tag ≠ diet; same-type birth | Child remains `camel` | None | **A** |
| Spawn / village | worldgen + EntityType | Desert village template pool `village/desert/camel.json`; CREATURE | Encounter ≠ origin | Not origin field | None | **A** |
| Sand step sound | `BlockTags.CAMEL_SAND_STEP_SOUND_BLOCKS` | `playStepSound` (`Camel.java` **335–340**) | Presentation | Not needed | None | **A** |
| Loot | `entities/camel.json` | Empty entity table (type only; no pools) | Drops ≠ anatomy | Not needed | None | **A** |
| Host contribution | Host Registry | **ABSENT** `"camel"` | N/A — cannot originate live contribution | Fail-soft `organismKey` | No production camel writer | **B** |

No row is **C**.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"camel"` | **ABSENT** | Not in living_biological / undead / unsuitable | Do **not** register. Unregistered ≠ C |
| Adjacent `"horse"` / `"donkey"` / `"mule"` | **LIVE** (not absorbed) | Same living_biological list | Distinct keys. Shared list ≠ camel clade |
| camel_husk | **ABSENT** organism in 1.21.1 | Inventory §9.3 only | Do not absorb |
| Resolver / Analyzer | **LIVE** generic / **UNKNOWN** sparse BP cores | Fail-soft unknown organism path documented elsewhere | Projects keys; no sit/dash field |
| Camel entity JSON | **ABSENT** | No production config | Vanilla owns behavior |
| Inventory camel row | **PLANNING** | Not edited by this packet | Docs ≠ live consumer |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails |
|----------------|--------------|
| Sit/stand needs a movement or size BP field | Pose + hitbox owner is Camel entity state. No BioCraft consumer | **A** |
| Dash/jump needs a locomotion trait | `PlayerRideableJumping` ride API. **A** |
| Two-passenger mountability is biology | `canAddPassenger` / ride helpers. **A** |
| `AbstractHorse` means horse-family / register with Horse | Distinct EntityType; Camel absent from hosts while Horse present. Shared parent ≠ clade |
| Always-tamed means domestication profile | Override returns true for horse inventory/ride path. **A** |
| Unregistered Camel earns C so we must register | Registration is Host Registry work, out of scope. Fail-soft identity is **B** |
| camel_husk is Camel undead form | No 1.21.1 organism. Inventory only |

---

## Potential biological relationships

### 1. Identity without Host Registry

- **Owner:** `EntityType.CAMEL` + fail-soft resolver.
- **Biological input?** Registry key only.
- **Named consumer:** Generic Analyzer/resolver for unknown/unregistered keys (**LIVE** generic / **UNKNOWN** sparse).
- **Result:** **B**.

### 2. Sitting / dash / ride

- **Owner:** `Camel` + `AbstractHorse` + `CamelAi.RandomSitting`.
- **Biological input?** No.
- **Named consumer:** None.
- **Result:** **A**.

### 3. Breeding / cactus food

- **Owner:** `#camel_food` + `getBreedOffspring` → `EntityType.CAMEL.create`.
- **Result:** **A**.

### 4. Adjacency to Horse / Donkey / Mule

- Shared `AbstractHorse` only. Distinct keys. Do **not** absorb.
- **Result:** **A**.

**C is not earned.**

---

## Wiki orientation disagreements

| Common orientation | 1.21.1 authority | Conclusion |
|--------------------|------------------|------------|
| Camel is a Horse variant | Distinct `"camel"`; `Camel extends AbstractHorse` | Shared parent ≠ clade |
| Sitting is a biological rest trait | Pose FSM + dimensions | Gameplay **A** |
| Camel must be registered because Horse is | Host Registry participation is separate | Do not register here |

---

## Final stop gate

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** (`organismKey=camel`) |
| Named missing-fact consumer | **NO** |
| Register Camel? | **NO** — out of scope; absences stay |
| Architectural escalation | **NO** |

**Closeout:** A = vanilla ownership for sit/dash/ride/food/breed/spawn; B = identity via `organismKey`; C = not earned.
