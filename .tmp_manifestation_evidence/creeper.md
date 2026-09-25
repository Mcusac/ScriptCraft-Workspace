TEMPORARY EVIDENCE — NOT PROJECT SSOT

Do not treat this file as canonical design documentation.
Do not promote into manifestations/creeper.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004 without the authorized Phase 3 pass.

# Creeper — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

Method (every behavior): owner → biological input? → `organismKey` / `contributingSourceKey` enough? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied independently: `PowerableMob` / charged / fuse / swell / explosion / lightning are **ENTITY MECHANICS** first; do **not** mint `explosiveCapability`; `dna.md` already forbids recreating Creeper fuse/explosion in a profile; `variant_mappings` / mob-based `creeper.json` are xenomorph **gameplay** configs, not BP fields; Host Registry presence ≠ automatic A and ≠ C; shared `PowerableMob` with Wither ≠ clade.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey` (Model A Chestburster/Drone), optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

**Default: NO new BP field.** Ghast / Warden / Witch / Wither are **not absorbed**.

---

## Subject

Creeper (`minecraft:creeper`) — living Creeper identity on Minecraft Java **1.21.1**. Scope: EntityType; `Creeper extends Monster implements PowerableMob`; fuse/swell/ignite/explode; lightning-powered flag; cat/ocelot avoid; goat target refusal; loot; Host Registry `living_biological`; BioCraft identity routing; creeper xenomorph variant JSON / bootstrap.

Out of scope as organisms: Ghast, Warden, Witch, Wither, Cat, Ocelot, Goat.

---

## Version

Minecraft Java **1.21.1** only. Mapped sources in `.tmp_mc_sources/` are authoritative (`neoforge-21.1.208-sources.jar` / client-extra resources). Wiki is orientation / disagreement discovery only; **source wins**.

---

## Phase 1 gate

| Required probe | Status |
|----------------|--------|
| `.tmp_mc_sources/.../monster/Creeper.java` | **Present** (290 lines) |
| `PowerableMob.java` | **Present** (5 lines) |
| Related loot / tags | **Present** (`loot_table/entities/creeper.json`; `#creeper_igniters`; `#creeper_drop_music_discs`) |
| BioCraft `hosts.json` + `creeper.json` + `MobEntityConfigLoader` + `BiologicalProfileResolverTest` | **Present** |

Gate **PASS** — proceed (not UNKNOWN).

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:creeper` |
| `EntityType` | `EntityType.CREEPER` — `EntityType.java` **273–275**: `register("creeper", Builder.of(Creeper::new, MobCategory.MONSTER).sized(0.6F, 1.7F).clientTrackingRange(8))` |
| Fire / lava | CREEPER builder does **not** call `.fireImmune()` |
| Class | `Creeper extends Monster implements PowerableMob` (`Creeper.java` **44**) |
| Category | `MobCategory.MONSTER` |
| Dimensions | **0.6 × 1.7**, tracking **8** |
| Default attributes | `DefaultAttributes.java` **104**: `Creeper.createAttributes()` — monster attrs + movement **0.25** (`Creeper.java` **72–74**) |
| Spawn placement | `SpawnPlacements.java` **108**: `ON_GROUND`, `MOTION_BLOCKING_NO_LEAVES`, `Monster::checkMonsterSpawnRules` |
| Host Registry | **REGISTERED.** `hosts.json` `vanilla_hosts.living_biological.mobs` includes `"creeper"` (**9**). Group `default_dna`: `baseline_biological` (**4**). `variant_mappings` `"creeper": "aggressive"` (**49**) |
| Suitability | `HostType.LIVING_BIOLOGICAL` → `isSuitableForXenomorph("creeper")` **true** |
| Inventory baseline | `vanilla_organism_inventory.md`: bio-organic, registered, `LIVING_BIOLOGICAL` |

Independent existence: `/summon` / spawn egg; overworld biome monster lists (e.g. plains, swamp, jungle, desert — cached worldgen). Spawn ≠ origin.

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing composition? | Named BioCraft consumer? | Refined manifestation classification | A/B/C |
|----------|--------------|-----------------|-------------------|----------------------|--------------------------|--------------------------------------|-------|
| Identity / size / category | `EntityType.CREEPER` | `EntityType.java` **273–275** | Identity only | `organismKey = creeper` (registered) | Generic resolver / Analyzer. **No** Creeper-named branch | **identity** | **B** |
| Java type (`Monster` + `PowerableMob`) | `Creeper` class | `Creeper.java` **44**. `PowerableMob` is a 1-method interface (`isPowered()`) also implemented by `WitherBoss` | Shared interface ≠ clade / ≠ explosive anatomy | Distinct key already | None for PowerableMob as biology | **identity** (type hierarchy ≠ biology) | **A/B** |
| Fuse / swell countdown | `Creeper.tick` + synched `DATA_SWELL_DIR` | `maxSwell` default **30** (NBT `"Fuse"`); swell ticks to explode (`Creeper.java` **49–50**, **107**, **132–155**) | **No.** Combat timer | Identity sufficient | **None.** `dna.md` forbids recreating fuse in a profile | **transient gameplay state** | **A** |
| `SwellGoal` | Goal registered on Creeper | `registerGoals` priority 2 (`Creeper.java` **61**) | AI | Identity sufficient | None | **transient gameplay state** / AI | **A** |
| Ignite (flint/steel / fire charge) | `mobInteract` + `#creeper_igniters` | Tag = flint_and_steel, fire_charge (`creeper_igniters.json`). Sets `DATA_IS_IGNITED` | Item interact | Identity sufficient | None | **environmental interaction** | **A** |
| Explosion | `explodeCreeper` | Powered radius × **2** else × **1**; `Level.explode` MOB; linger cloud from active effects; `discard()` (`Creeper.java` **246–255**) | **No.** Entity death/combat mechanic | Not an `explosiveCapability` field | **None** in BioCraft gameplay | **combat consequence** / entity removal | **A** |
| Powered / charged | `DATA_IS_POWERED` + `thunderHit` | Lightning sets powered **true** (`Creeper.java` **219–222**). NBT `"powered"`. `isPowered()` implements `PowerableMob` | Persistent **entity flag**, not a second organism | Identity + vanilla NBT | None for charged biology | **persistent entity state** | **A** |
| Fall swell bump | `causeFallDamage` | Adds `fallDistance * 1.5` into swell, capped (`Creeper.java` **82–89**) | Combat/physics | Identity sufficient | None | **transient gameplay state** | **A** |
| Cat / ocelot avoid | `AvoidEntityGoal` | Avoid Ocelot and Cat 6 blocks (`Creeper.java` **62–63**) | AI. Shared goal ≠ feline clade | Distinct keys | None | **transient gameplay state** / AI | **A** |
| Goat target refusal | `setTarget` | Ignores `instanceof Goat` (`Creeper.java` **164–168**) | AI gate | Identity sufficient | None | **transient gameplay state** | **A** |
| Head drop | `dropCustomDeathLoot` | Charged Creeper killing Creeper may drop creeper head (`Creeper.java` **181–187**) | Item production | Identity sufficient | None | **item/block production** | **A** |
| Gunpowder / disc loot | Vanilla loot table | Gunpowder 0–2; disc tag if attacker `#skeletons` | Drops ≠ anatomy | Not needed | None | **item/block production** | **A** |
| Overworld spawn | Biome monster lists + placement | Present in many overworld biomes (cached JSON). Encounter ≠ origin | Spawn ≠ origin BP | Not an origin field | None | **environmental interaction** | **A** |
| Host Registry / gestation | `hosts.json` + eligibility + `writeContributingSource` | `"creeper"` in `living_biological`; HostType `LIVING_BIOLOGICAL`; suitability **true**; `default_dna` `baseline_biological`. Gestation encodes host path → `contributingSourceKey` (`GestationManager.java` **164–175**) | Identity routing only. Does **not** store fuse, powered, explosion radius | `organismKey=creeper` + optional `contributingSourceKey=creeper` + HostType + `hostEffectProfileId=baseline_biological` | **LIVE** production writer / resolver | **identity** (+ BioCraft participation) | **B** |

**No row is C.** Live `contributingSourceKey=creeper` is identity already represented — **B**, not C.

---

## PowerableMob / explosion probe (mandatory)

Treat PowerableMob / charged / fuse / swell / explosion / lightning as **entity mechanics** first.

| Probe | Outcome |
|-------|---------|
| Interface | `PowerableMob` = `boolean isPowered()` only (`PowerableMob.java` **3–5**) |
| Other implementer | `WitherBoss implements PowerableMob` — shared Java interface, **not** a Creeper/Wither explosive clade |
| Charged persistence | Synched boolean + NBT `"powered"`; set by `thunderHit` (does **not** replace the entity) |
| Contrast Pig/Villager lightning | Those paths `create` a **new** EntityType and `discard()` the source. Creeper lightning **mutates a flag on the same entity** |
| Fuse | Instance field `maxSwell`, NBT `"Fuse"`, not genetics |
| Explosion | `Level.explode` then discard. No BioCraft explosion consumer |
| `explosiveCapability` | **Must not be invented.** `dna.md` explicit: do not recreate Creeper fuse in a profile |

**Classification:** vanilla combat / entity state. **A**. Not a BP field.

---

## AlienCraft configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` key `"creeper"` | **LIVE** | `living_biological.mobs` (**9**); `default_dna: baseline_biological` | Participation. Registration ≠ extra biology |
| `variant_mappings` `"creeper": "aggressive"` | **LIVE parse / PARSE-ONLY query** | Parsed into `MobHostRegistry.VARIANTS`. Production callers of `getVariant` / `SpecializedXenomorphManager.getSpecializedVariant`: **none** outside the manager itself | Temperament string is not a BP trait. Unused query ≠ missing fact |
| `entity/.../hostile/organic/creeper.json` | **LIVE load / PARSE-ONLY abilities** | `mob_catalog.json` `bootstrap_entries` includes `{folder: hostile/organic, mob: creeper}` (**5**). `MobEntityConfigLoader.loadConfigs` loads listed files only (**91–111**). JSON: `variant_id` creeper, `host_type` living_biological, multipliers, `infection_spread: true` | Xenomorph **gameplay variant** SSOT (`system.md`: mob-based JSON ≠ Biological Profile). `infection_spread` aliases `explosive_ability` in parser — **not** a BP explosion field |
| `SpecializedXenomorphManager` | **STUB / PARSE-ONLY** | `ConfigLoaderBootstrap` **93** initializes from loaded variants. `infection_spread` → in-memory `"explosive_ability"` / `explosive_power` 3.0. **Zero** production callers of `getSpecialAbilities` / `getVariantProperties` | Init is not a named explosion consumer. Planned/unused config **never earns C** |
| `MobEntityConfigLoader` bootstrap | **LIVE** | Loads creeper.json because catalog lists it | Load ≠ biology |
| `BiologicalProfileResolver` | **LIVE** generic | Lowercase key; host type / DNA id; no Creeper branch | `organismKey=creeper`, `HostType.LIVING_BIOLOGICAL`, `hostEffectProfileId=baseline_biological` |
| `BiologicalProfileResolverTest.creeperResolvesLivingBiologicalHostReferences` | **TEST** | Asserts living-host identity only (**68–70**, **126–134**) | Test of existing composition, not a missing-fact consumer |
| `HostEligibilityService` | **LIVE** generic | Creeper eligible via `LIVING_BIOLOGICAL` | Not a Creeper-named missing-fact consumer |
| Gestation `writeContributingSource` | **LIVE** | Writes `"creeper"` when host is Creeper | Identity **B** |
| Creeper-named Analyzer / fuse / explosion branch | **ABSENT** | No production Java branch on fuse/powered/explosion | Vanilla remains owner |

Consumer classification:

| Candidate | Classification |
|-----------|----------------|
| `BiologicalProfileResolver` | **LIVE** generic |
| Gestation `contributingSourceKey` | **LIVE**; Creeper **origin allowed** |
| `HostEligibilityService` | **LIVE** registry gate |
| `creeper.json` / explosive_ability map | **PARSE-ONLY** (no gameplay decision) |
| `BiologicalProfileResolverTest` creeper | **TEST** |
| Creeper-named missing-fact consumer | **ABSENT** |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails on 1.21.1 evidence |
|----------------|--------------------------------|
| Fuse / explosion ⇒ `explosiveCapability` / Anatomy organ | Vanilla combat owner. `dna.md` forbids recreating fuse. No BioCraft consumer |
| `PowerableMob` ⇒ shared charged biology with Wither | 1-method interface. Wither is a separate organism |
| Lightning charge ⇒ conversion / ancestry | Same entity; flag only. Contrast Villager→Witch / Pig→ZP replacement |
| `creeper.json` `infection_spread` ⇒ live explosion consumer | Loaded DTO; no gameplay caller of derived abilities |
| `variant_mappings` aggressive ⇒ Trait | Unused temperament string |
| Cat avoid ⇒ feline relationship field | `AvoidEntityGoal` |
| Host Registry = automatic A or C | Registration is **B** participation |
| Gunpowder drop ⇒ explosive anatomy | Loot table |

---

## Potential biological relationships (hypotheses only — after ownership)

### 1. Creeper as live xenomorph host / Model A contributing source

- **Relationship:** Facehugger may select Creeper; gestation copies host registry path; resolver/Analyzer project it.
- **Owner:** `hosts.json` + `HostEligibilityService` + `GestationManager.writeContributingSource` + `BiologicalProfileResolver`.
- **Biological input?** Only the organism-definition key `"creeper"`.
- **Existing composition:** `organismKey=creeper`; optional `contributingSourceKey=creeper`; `HostType.LIVING_BIOLOGICAL` + `hostEffectProfileId=baseline_biological`.
- **Named consumer?** **LIVE** — eligibility, gestation writer, generic resolver. **No** Creeper-named missing-fact consumer.
- **Result:** **B**.

### 2. Explosion / fuse as biological capability

- **Owner:** `Creeper` tick + `explodeCreeper`.
- **Named consumer?** None. PARSE-ONLY `infection_spread` is not a consumer.
- **Result:** **A**. **No C.**

### 3. Charged state as genetics / second organism

- **Owner:** `thunderHit` flag.
- **Named consumer?** None.
- **Result:** **A**.

**C is not earned for any relationship.**

---

## Wiki disagreements

| Orientation claim | 1.21.1 authority | Conclusion |
|-------------------|------------------|------------|
| Charged Creeper is a separate mob / spawn | Same EntityType; `DATA_IS_POWERED` | **Flag, not a type** |
| Creeper is elemental / explosive species for BP | `Monster` + explosion mechanic; inventory bio-organic; HostType `LIVING_BIOLOGICAL` | Do not mint explosive BP |
| Fuse belongs in Biological Profile | `dna.md` + no consumer | **Reject** |

---

## Final evidence conclusion

| Gate | Result |
|------|--------|
| New BP field | **No** |
| Existing composition sufficient | **Yes** — `organismKey=creeper` + optional `contributingSourceKey=creeper` |
| Named consumer of a missing fact | **None** |
| Architectural escalation | **None** |

**A + B; C not earned.**
