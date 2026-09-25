TEMPORARY EVIDENCE — NOT PROJECT SSOT
Independent skeptical synthesis — Fox / Goat / Mooshroom / Ocelot
Do not treat this file as project SSOT. Do not mint DESIGN-BIO-MANIFEST-004.

# Fox / Goat / Mooshroom / Ocelot — skeptical synthesis

**Role:** Independent reviewer. Re-opened load-bearing mapped 1.21.1 sources and live BioCraft participation paths. Did **not** accept packet consensus without re-checks. Majority A/B among packets is **not** evidence.

**Version:** Minecraft Java **1.21.1** / NeoForge **21.1.208** mapped cache under `.tmp_mc_sources/`.

**Primary objective:** find why **C is not earned**. Mooshroom is the **highest-scrutiny C candidate**.

---

## Re-verification anchors

| Claim | Re-check |
|-------|----------|
| Fox identity | `EntityType.java` **364–370**: `"fox"`, CREATURE, **0.6×0.7**, eyeHeight **0.4** |
| Goat identity | **405–406**: `"goat"`, **0.9×1.3** |
| Mooshroom identity | **502–504**: `"mooshroom"`, **0.9×1.4**, eyeHeight **1.3** (Cow-size literals; distinct id) |
| Ocelot identity | **510–511**: `"ocelot"`, **0.6×0.7** |
| hosts.json | `"fox"` + `"goat"` present in living_biological; `"mooshroom"` + `"ocelot"` **ABSENT** |
| Fox variant | `Fox.Type` RED/SNOW; spawn `byBiome(SPAWNS_SNOW_FOXES)`; breed random parent; `setTargetGoals` priority swap |
| Goat screaming | `IsScreamingGoat`; spawn 0.02; breed parent-or-0.02; `TIME_BETWEEN_RAMS_SCREAMER` 100–300 |
| Mooshroom lightning | `thunderHit` toggles RED↔BROWN; **no** EntityType change; **no** Cow create |
| Mooshroom breed type | same-type 1/1024 flip else random parent; offspring always `MOOSHROOM` |
| Mooshroom shear | discard + `EntityType.COW.create` + mushroom drops |
| Mooshroom bowl / milk | bowl→stew; `super.mobInteract` still reaches Cow bucket→milk |
| Ocelot trust | boolean `Trusting`; 1/3 on food; not `TamableAnimal`; offspring does not inherit trust |
| BioCraft named refs | Module `rg` (src): organism strings only in `hosts.json` for fox/goat; **zero** mooshroom/ocelot code hits |
| `CompiledBiologicalProfile` | organismKey, hostType, xenomorphFormKey, hostEffectProfileId, behaviorTypeKey, contributingSourceKey — **no** variant/trust/scream/stew fields |
| Gestation writer | `encodeId(host)` → registry path only — identity |

---

## Refined manifestation category matrix

| Organism | Mechanic | Category | Owner | Result |
|----------|----------|----------|-------|--------|
| Fox | Registry identity | identity | `EntityType.FOX` | **B** |
| Fox | Live host contribution | BioCraft-consumed biological input | hosts + gestation encodeId | **B** (identity only) |
| Fox | RED/SNOW variant | persistent entity state | `Fox.Type` + NBT | **A** |
| Fox | Variant prey priority | transient gameplay / AI | `setTargetGoals` | **A** |
| Fox | Sleep / crouch / pounce flags | transient gameplay state | `DATA_FLAGS_ID` | **A** |
| Fox | Trusted UUIDs | persistent gameplay state | synched UUID slots | **A** |
| Fox | Berries / prey / powder-snow | environmental / AI / item | goals + tags | **A** |
| Goat | Registry identity + contribution | identity / BioCraft input | `EntityType.GOAT` + hosts | **B** |
| Goat | Screaming flag | persistent entity state | synched + NBT | **A** |
| Goat | Ram cooldown / sounds | transient gameplay / combat | `GoatAi` | **A** |
| Goat | Horn drop | item/block production | `dropHorn` + `#snaps_goat_horn` | **A** |
| Goat | Bucket milk | item/block production | `mobInteract` | **A** |
| Goat | Long jump / powder-snow malus | movement / environmental | brain + path | **A** |
| Mooshroom | Distinct identity | identity | `EntityType.MOOSHROOM` | **A** (unregistered; soft key sufficient) |
| Mooshroom | `extends Cow` | implementation reuse | Java hierarchy | **A** — not ancestry |
| Mooshroom | Red/brown | persistent entity state | `MushroomType` | **A** |
| Mooshroom | Lightning swap | entity/state transformation | `thunderHit` | **A** |
| Mooshroom | Breed type | persistent state / breeding determination | `getOffspringType` | **A** |
| Mooshroom | Bowl stew / flower charge | item production / effect application | `mobInteract` | **A** |
| Mooshroom | Shear→Cow | entity/state transformation | `shear` discard+create | **A** |
| Mooshroom | Host Registry | — | **ABSENT** | not A/B by itself; no other consumer → no C |
| Ocelot | Distinct identity | identity | `EntityType.OCELOT` | **A** (unregistered; soft key sufficient) |
| Ocelot | Trust boolean | persistent gameplay state | `DATA_TRUSTING` | **A** |
| Ocelot | Avoid / tempt / despawn | AI / spawn rules | goals | **A** |
| Ocelot | `OcelotAttackGoal` | AI code reuse | shared with Cat | **A** — not ancestry |
| Ocelot | Host Registry | — | **ABSENT** | not A/B by itself; no other consumer → no C |

**C surviving?** **None.**

---

## Mooshroom highest-scrutiny C challenge

| Candidate “missing fact” | Why C fails |
|--------------------------|-------------|
| Mooshroom ≠ Cow in composition | Distinct registry id already models identity; no live consumer requires a richer fact |
| Red/brown must be BP | Stew charge, shear drops, lightning, breed — all vanilla; `CompiledBiologicalProfile` has no slot and no reader |
| Lightning / shear as inheritance field | Lightning = same-entity variant flip; shear = discard+create Cow destination |
| Stew / suspicious effects as biology | Item + entity NBT; no BioCraft consumer |
| Register to “complete” Cow adjacency | Host Registry edit out of scope; investigation does not authorize registration |

Interesting combination of mechanics does **not** earn C without a named live BioCraft consumer that needs a fact Model A cannot express. **None found.**

---

## Rejected abstractions (must stay closed)

| Abstraction | Why rejected |
|-------------|--------------|
| Feline clade (Fox/Ocelot/Cat) | Distinct EntityTypes; shared prey/goal code ≠ ancestry |
| Bovine ancestry (Mooshroom/Cow/Goat) | Distinct ids; milk outcome parallel; `extends Cow` = implementation |
| Milk-as-shared-biology | Item interact owners; Cow already closed milk-as-field |
| Shared-goal clade (`OcelotAttackGoal`) | Code reuse only |
| Register-from-investigation | Forbidden; absence stays for mooshroom/ocelot |
| Heritability-as-BP-field | Fox/Goat/Mooshroom heritable states remain **A** |
| Trust-as-domestication | Ocelot boolean ≠ `TamableAnimal` |
| Live `contributingSourceKey` as C | Fox/Goat identity only — **B not C** |

---

## Consumer audit (skeptical)

| Candidate | Status | Survives as C? |
|-----------|--------|----------------|
| Generic resolver / Analyzer projecting keys | **LIVE** generic | No — **B** |
| Gestation `contributingSourceKey` for fox/goat | **LIVE** generic encodeId | No — **B** |
| Fox/goat-named unit tests | **ABSENT** | Does not invent C |
| Mooshroom / ocelot host contribution | **ABSENT** registration | No — do not register; no alternate consumer |
| Variant / scream / trust / stew fields | Not in `CompiledBiologicalProfile` | No consumer → no C |
| Inventory / planning rows | **PLANNING** | No |

---

## Gate decision

| Gate | Result |
|------|--------|
| Any C survived? | **NO** |
| Proceed to Phase 3 canonical docs? | **YES** (A/B only) |
| Mint DESIGN-BIO-MANIFEST-004? | **NO** |
| Java / hosts / BP / BACKLOG changes? | **NO** |

---

## Next evidence branch (recommendation)

Choose from remaining **pending** inventory by **demonstrated evidence dependency**. This batch does **not** open Donkey/Mule/Sheep/Wolf/Panda/Parrot from adjacency. Independent **Strider** remains a valid inventory-sequence candidate (not earned by this batch’s mechanics). Do not treat this quartet as a feline/bovine/livestock column.
