TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Chicken docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/chicken.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004.

# Chicken — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

**Do not unregister Chicken as a conclusion of this investigation.** Chicken is already in `vanilla_hosts.living_biological`. Registration is participation, not extra biology.

Method: existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP |

Closed leaps: slow fall ≠ Flight Profile / `canFly`; egg timer ≠ oviparity/reproductive-strategy BP field; seeds tag ≠ diet genetics; jockey flag ≠ subtype; `Animal` parent ≠ clade; spawn ≠ origin; registered ≠ C; live `contributingSourceKey=chicken` ≠ C.

Do **not** invent flight/oviparity/inheritance abstractions. Bee/Phantom/Allay flight failures already close the flight leap.

Default: **NO** new BP field. Live contribution identity is **B**, not **C**.

---

## Subject

Chicken (`minecraft:chicken`) — airborne fall damping + flap presentation, ground navigation, egg lay timer → `Items.EGG`, seed food/breeding, chicken-jockey flag, CREATURE spawn, Host Registry LIVE `living_biological`, BioCraft gestation identity routing.

Out of scope: Parrot, Bee, Phantom, Camel, Cat, Duck (absent).

---

## Version

Minecraft Java **1.21.1** only. `.tmp_mc_sources/` authoritative.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:chicken` |
| `EntityType` | `EntityType.CHICKEN` — `EntityType.java` **252–259**: `CREATURE`, `sized(0.4F, 0.7F)`, `eyeHeight(0.644F)`, passengerAttachments `(0.0, 0.7, -0.1)`, tracking **10** |
| Fire / lava | **No** `.fireImmune()` |
| Class | `Chicken extends Animal` (`Chicken.java` **38**). **Not** `FlyingMob`. **Not** `FlyingAnimal` |
| Category | `MobCategory.CREATURE` |
| Attributes | Health **4**, movement **0.25** (`Chicken.java` **71–73**) |
| Baby | Scale **0.5**, eyeHeight **0.2975F** (`BABY_DIMENSIONS`, **39**, **67–68**) |
| Host Registry | **REGISTERED.** `hosts.json` living_biological includes `"chicken"` (**6**). `default_dna: baseline_biological`. No chicken `variant_mappings` |
| Suitability | Registered living_biological → currently suitable. Registered ≠ extra biology |

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP representation? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|----------------------------|--------------------|-------|
| Identity / CREATURE / size | `EntityType.CHICKEN` | `EntityType.java` **252–259** | Identity | `organismKey = chicken` | Resolver / Analyzer / host lookup | **B** |
| Goals / panic / stroll | `Chicken.registerGoals` | Float, Panic **1.4**, Breed, Tempt `#chicken_food`, FollowParent, stroll, look (`Chicken.java` **55–64**) | Entity AI | Identity sufficient | None | **A** |
| Fall damping / “glide” | `aiStep` delta multiply | When airborne and `y < 0`, multiply Y by **0.6** (`Chicken.java` **88–90**). Flap fields for presentation (**78–92**) | Locomotion tweak on Animal | **Not** flight. Not `FlyingMoveControl` | None | **A** |
| Water path malus | constructor | `PathType.WATER` malus **0.0F** (`Chicken.java` **51**) | Navigation | Not needed | None | **A** |
| Egg lay | `eggTime` in `aiStep` | Adult non-jockey: countdown; spawn `Items.EGG`; reset 6000–12000 (`Chicken.java` **46**, **93–98**). NBT `EggLayTime` | Item production timer | Not oviparity/genetics field | None | **A** |
| Chicken jockey flag | `isChickenJockey` | NBT `IsChickenJockey`; skip egg; XP **10**; `removeWhenFarAway` true (`Chicken.java` **145–171**, **181–189**) | Encounter/state flag | Not subtype biology | None | **A** |
| Food / breed | `#chicken_food` + `BreedGoal` | Seeds/pods (`chicken_food.json`); offspring `EntityType.CHICKEN.create` (**132–134**, **140–142**) | Tag ≠ diet trait | Child remains `chicken` | None | **A** |
| Rider positioning | `positionRider` | Sync passenger body rot (`Chicken.java` **174–178**) | Mount helper for jockey cases | Not mountability BP | None | **A** |
| Spawn / summon / egg item | EntityType + worldgen / items | CREATURE biomes; spawn egg; thrown egg can hatch (Minecraft item owner; not re-traced here as BP) | Encounter ≠ origin | Not origin field | None | **A** |
| Loot | `entities/chicken.json` | Feathers 0–2; raw/cooked chicken | Drops ≠ anatomy | Not needed | None | **A** |
| Host → contributingSourceKey | Host Registry + gestation | `"chicken"` → path `"chicken"` | Identity only | `organismKey` + `contributingSourceKey=chicken` + `baseline_biological` | **LIVE** generic writer/Analyzer | **B** |

No row is **C**.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"chicken"` | **LIVE** | living_biological **6** | Participation. Can originate contribution |
| `variant_mappings` chicken | **ABSENT** | No entry | No override |
| Resolver / Analyzer / gestation | **LIVE** generic | Same Model A identity path as Cow; sparse cores may be **UNKNOWN** | Identity only. **B not C** |
| Chicken entity JSON | **ABSENT** | No production config | Vanilla owns egg/AI/fall |
| Inventory chicken row | **PLANNING** | Not edited here | Docs ≠ consumer |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails |
|----------------|--------------|
| Chicken can fly → Flight Profile / `canFly` | No `FlyingMob`/`FlyingAnimal`; only fall Y damping **0.6**. Bee/Phantom/Allay already failed flight generalization. **A** |
| Egg laying is oviparity / reproductive strategy BP | Timer + `spawnAtLocation(Items.EGG)`. Item production. **A** |
| Seeds food is diet genetics | `#chicken_food` tag. Tag ≠ diet trait. **A** |
| Chicken jockey is a biological subtype | Boolean NBT + spawn/XP/despawn. **A** |
| Live `contributingSourceKey=chicken` earns C | Identity already represented. **B** |
| Small hitbox needs a size field | `EntityType` dimensions. Identity **B** / presentation **A** |

---

## Potential biological relationships

### 1. Live xenomorph host / Model A source

- **Owner:** hosts + eligibility + gestation writer + Analyzer.
- **Biological input?** Key `"chicken"` only.
- **Result:** **B**.

### 2. Fall damping / flap

- **Owner:** `Chicken.aiStep`.
- **Named consumer:** None.
- **Result:** **A**. Reject flight abstraction.

### 3. Egg timer

- **Owner:** `Chicken.aiStep` + NBT.
- **Named consumer:** None needing oviparity fact.
- **Result:** **A**.

### 4. Breeding / food / spawn

- **Owner:** Animal goals + EntityType + worldgen.
- **Result:** **A**.

**C is not earned.**

---

## Wiki orientation disagreements

| Common orientation | 1.21.1 authority | Conclusion |
|--------------------|------------------|------------|
| Chickens fly / are flying animals | `Animal` + fall damping only | Not flight; **A** |
| Egg laying is biological reproduction of eggs as offspring | Spawns item `EGG`, not an entity baby | Item production **A**; babies come from `BreedGoal` |
| Health 4 | `MAX_HEALTH` **4.0** | Agrees |

---

## Final stop gate

| Gate | Result |
|------|--------|
| New BP field earned | **NO** |
| Existing composition sufficient | **YES** |
| Named missing-fact consumer | **NO** |
| Architectural escalation | **NO** |

**Closeout:** A = vanilla ownership for fall/egg/food/breed/jockey/spawn; B = identity including live `contributingSourceKey=chicken`; C = not earned.
