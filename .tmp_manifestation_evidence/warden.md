TEMPORARY EVIDENCE — NOT PROJECT SSOT

Do not treat this file as canonical design documentation.
Do not promote into manifestations/warden.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004 without the authorized Phase 3 pass.

# Warden — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT. **Not** a canonical manifestation report. **Not** permission to edit Host Registry, eligibility, Model A, vials, Analyzer, lifecycle, AI, rendering, registries, Java, `hosts.json`, BACKLOG, SPRINT, ROADMAP, dna.md, system.md, inventory, classification docs, or `DESIGN-BIO-MANIFEST-004`.

Method (every behavior): owner → biological input? → `organismKey` / `contributingSourceKey` enough? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / optional `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact — STOP, document minimum, do not design |

Closed leaps applied independently:

- Inventory **bio-organic** and HostType **INORGANIC** are **INDEPENDENTLY OWNED**. Determine what each means from SSOT. **Do not reconcile.** Do **not** conclude inventory or HostType is “wrong.”
- **boss is NOT a biological category.** `deep_mob_configs.boss` / mob_catalog boss list = **PLANNING**.
- Sonic boom ≠ organ field without a named consumer.
- Sculk shrieker encounter ≠ origin.
- Shared `INORGANIC` list with slime/guardian/shulker ≠ clade.

Existing BP composition used (no invented fields): `organismKey`, optional `contributingSourceKey`, optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

**Default: NO new BP field.** Creeper / Ghast / Witch / Guardian / Wither are **not absorbed**.

---

## Subject

Warden (`minecraft:warden`) — living Warden identity on Minecraft Java **1.21.1**. Scope: EntityType; `Warden extends Monster implements VibrationSystem`; anger; sonic boom; darkness; digging/emerging poses; sculk shrieker triggered spawn; Host Registry `unsuitable.inorganic`; inventory bio-organic label; `warden.json` catalog stub vs bootstrap.

Out of scope as organisms: Creeper, Ghast, Witch, Guardian, Elder Guardian, Wither, Ender Dragon.

---

## Version

Minecraft Java **1.21.1** only. Mapped sources in `.tmp_mc_sources/` are authoritative. Wiki is orientation / disagreement discovery only; **source wins**.

---

## Phase 1 gate

| Required probe | Status |
|----------------|--------|
| `.tmp_mc_sources/.../warden/Warden.java` | **Present** (679 lines) |
| `WardenAi.java` / `SonicBoom.java` / anger / spawn tracker | **Present** |
| `SculkShriekerBlockEntity.java` | **Present** |
| Related loot / tags | **Present** (`loot_table/entities/warden.json`; `#warden_can_listen`) |
| BioCraft `hosts.json` + `warden.json` + `mob_catalog.json` | **Present** |

Gate **PASS** — proceed (not UNKNOWN).

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:warden` |
| `EntityType` | `EntityType.WARDEN` — `EntityType.java` **720–728**: `register("warden", Builder.of(Warden::new, MobCategory.MONSTER).sized(0.9F, 2.9F).passengerAttachments(3.15F).attach(EntityAttachment.WARDEN_CHEST, 0.0F, 1.6F, 0.0F).clientTrackingRange(16).fireImmune())` |
| Fire / lava | **`fireImmune()`** |
| Class | `Warden extends Monster implements VibrationSystem` (`Warden.java` **77**) |
| Category | `MobCategory.MONSTER` |
| Dimensions | **0.9 × 2.9**, tracking **16**; digging/emerging pose height forced to **1.0F** (`Warden.java` **549–551**) |
| Default attributes | `DefaultAttributes.java` **163**: health **500**, speed **0.3F**, knockback resistance **1.0**, attack knockback **1.5**, attack damage **30** (`Warden.java` **181–187**) |
| Spawn placement | `SpawnPlacements.java` **174**: `NO_RESTRICTIONS`, `Mob::checkMobSpawnRules` |
| Natural biome list | **No** `minecraft:warden` in cached `worldgen/biome/*.json` |
| Host Registry | **REGISTERED** under `vanilla_hosts.unsuitable.inorganic.mobs` with slime, magma_cube, shulker, guardian, elder_guardian (`hosts.json` **25–28**). Group `default_dna: inorganic` |
| Suitability | `HostType.INORGANIC` → `isSuitableForXenomorph("warden")` **false** (`HostType.java` **26**, **44–45**) |
| Inventory baseline | Inventory category **bio-organic**; HostType **INORGANIC**. **Do not collapse columns.** |

---

## Independently owned labels (mandatory — do not reconcile)

| Label | SSOT | What it means | Participates in a live BioCraft decision? |
|-------|------|----------------|-------------------------------------------|
| Inventory **bio-organic** | `vanilla_organism_inventory.md` (planning accounting) | Provisional planning category. Explicitly **not** HostType, eligibility, ancestry, or manifestation | **No.** Inventory is not a runtime registry. Facehugger / resolver / Analyzer do **not** read this document |
| HostType **INORGANIC** | `hosts.json` `unsuitable.inorganic` → `HostType.INORGANIC` | Domain suitability taxonomy: “Purely inorganic materials - unsuitable for biological parasites” (`HostType.java` **26**). `suitableForXenomorph = false` | **Yes.** `MobHostRegistry.isSuitableForXenomorph` / `HostEligibilityService.isValidFacehuggerHost` use HostType. Resolver projects `hostType` + `hostEffectProfileId=inorganic` |

These answers **coexist**. This packet does **not** judge which label “should” win. HostType is routing, not biology. Inventory is accounting, not biology. **Neither earns C.**

`boss` is **not** a biological category. Catalog `deep_mob_configs.boss.mobs` includes `"warden"` beside ender_dragon/wither (**27–30**) — **PLANNING** comment: “Full temperament × material × mob matrix for content planning; bootstrap_entries is what loads at init.”

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing composition? | Named BioCraft consumer? | Refined manifestation classification | A/B/C |
|----------|--------------|-----------------|-------------------|----------------------|--------------------------|--------------------------------------|-------|
| Identity / size / `fireImmune` | `EntityType.WARDEN` | `EntityType.java` **720–728** | Identity only | `organismKey = warden` | Generic resolver | **identity** | **B** |
| Vibration listening | `VibrationSystem` + `WARDEN_CAN_LISTEN` | Listener radius 16; tag `GameEventTags.WARDEN_CAN_LISTEN` (`Warden.java` **602–619**) | Sensing AI | Identity sufficient | None | **transient gameplay state** / AI | **A** |
| Anger | `AngerManagement` NBT `"anger"` | Levels CALM/AGITATED/ANGRY (0/40/80) (`AngerLevel.java`); ticked every 20 (`Warden.java` **295–297**, **420–454**) | Combat memory, not genetics | Identity sufficient | None | **persistent entity state** (vanilla anger) | **A** |
| Sonic boom | `SonicBoom` behavior | FIGHT activity; 10 damage `sonicBoom` source; knockback; particles (`SonicBoom.java` **18–85**; `WardenAi.java` **186**) | Combat AI. **Not** an organ field without consumer | Identity sufficient | **None** | **combat** | **A** |
| Melee | `MeleeAttack` + attributes | Attack damage 30; `doHurtTarget` sets sonic cooldown 40 (`Warden.java` **222–227**) | Combat | Identity sufficient | None | **combat** | **A** |
| Darkness aura | `applyDarknessAround` | Every 120 ticks, radius 20, duration 260 (`Warden.java` **291–293**, **414–417**) | Effect application | Identity sufficient | None | **effect application** | **A** |
| Dig / emerge poses | Brain activities + `MobSpawnType.TRIGGERED` | Triggered spawn sets EMERGING (`Warden.java` **511–517`); DIG activity (`WardenAi.java` **130–136`) | Pose / AI | Identity sufficient | None | **transient gameplay state** | **A** |
| Sculk shrieker summon | `SculkShriekerBlockEntity.trySummonWarden` | Warning level ≥ 4; `SpawnUtil.trySpawnMob(EntityType.WARDEN, TRIGGERED, ...)` (`SculkShriekerBlockEntity.java` **190–194**) | **Encounter / creation mechanism.** Not origin, not sculk ancestry | Distinct key | None | **entity/state transformation** (creation) / encounter | **A** |
| Player warning tracker | `WardenSpawnTracker` on player | Codec on player; not Warden NBT | Player/world state | Not Warden biology | None | **transient gameplay state** | **A** |
| Sculk catalyst loot | Vanilla loot table | Single `sculk_catalyst` (`warden.json`) | Drop ≠ origin / ≠ anatomy | Not needed | None | **item/block production** | **A** |
| Natural biome spawn | **ABSENT** from biome JSON | Existence via shrieker / summon / egg | Spawn absence ≠ origin BP | Not an origin field | None | **environmental interaction** (none in biomes) | **A** |
| `#undead` | **ABSENT** | `undead.json` has no warden | Tag ≠ HostType | Distinct key | None | — | **A** |
| Host Registry / HostType | `hosts.json` inorganic | LIVE lookup `INORGANIC`; suitability **false** | Participation + routing. HostType never earns C | `organismKey=warden` + HostType + `hostEffectProfileId=inorganic` | **LIVE** eligibility gate | **identity** + eligibility routing | **B** |
| Inventory bio-organic | Planning table only | Not read by Java | Accounting | N/A | **No live consumer** | planning label | (not A/B/C of a consumer) |
| Gestation contribution | Blocked by suitability | Facehugger requires suitable HostType | Blocked origin ≠ missing sonic fact | Identity still sufficient if sampled | None missing | **identity** (blocked) | **B** |

**No row is C.** Sonic boom has **no** named BioCraft consumer → **A**, not an organ field.

---

## AlienCraft configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"warden"` | **LIVE** | `unsuitable.inorganic.mobs` (**27**) | Participation. Shared list ≠ clade. Do not call this “wrong” vs inventory |
| `MobHostRegistry.getHostType("warden")` | **LIVE** | `HostType.INORGANIC` | Suitability **false** — live BioCraft decision |
| Inorganic host-effect pack | **LIVE pack, not Warden-specific** | `parasite/host_effects/inorganic.json`; empty attachment effects | Attachment routing |
| Resolver identity | **LIVE** generic | `organismKey=warden`, `HostType.INORGANIC`, `hostEffectProfileId=inorganic` | Identity sufficient |
| `entity/.../boss/inorganic/warden.json` | **DEAD / not bootstrapped** | File exists (`variant_id` warden, `host_type` inorganic, 1.0 multipliers). **Not** in `bootstrap_entries` (only spider/creeper/wolf/enderman). `MobEntityConfigLoader` loads catalog entries only | On-disk stub. Planned config never earns C |
| `deep_mob_configs.boss` | **PLANNING** | Catalog `_comment` + boss list includes warden; `host_types` organic/undead/construct — **does not even list inorganic** | Planning matrix ≠ runtime. **boss ≠ biological category** |
| Warden-named Analyzer / sonic / sculk branch | **ABSENT** | No production Java | Vanilla remains owner |

---

## Tempting but rejected interpretations

| Tempting claim | Why it fails on 1.21.1 evidence |
|----------------|--------------------------------|
| Inventory bio-organic vs HostType INORGANIC must be fixed / one is wrong | Independently owned. Inventory is not runtime. HostType is suitability. Do not reconcile |
| boss catalog / warden.json ⇒ boss biology | boss is not a biological category; file not loaded |
| Sonic boom ⇒ sonic organ / Anatomy field | Combat behavior; no named consumer |
| Sculk catalyst drop / shrieker spawn ⇒ sculk origin / lineage | Encounter + loot. No parentage NBT |
| Shared INORGANIC with Guardian/Shulker ⇒ inorganic clade | Shared HostType bucket ≠ composition |
| `fireImmune` + darkness ⇒ elemental/undead | EntityType flag + effect. Not in `#undead` |
| Unsuitable ⇒ no biology | Resolver still projects identity (**B**) |

---

## Potential biological relationships (hypotheses only — after ownership)

### 1. Warden identity / HostType INORGANIC routing

- **Owner:** `hosts.json` + `HostType.INORGANIC` + resolver.
- **Live decision?** Yes — facehugger suitability false.
- **Missing BP fact?** No. HostType never earns C.
- **Result:** **B**.

### 2. Inventory bio-organic vs HostType INORGANIC

- **Not a relationship to collapse.** Two SSOTs, two questions.
- **Result:** record coexistence. **No C.** **No registry edit.**

### 3. Sonic boom / vibration as anatomy

- **Owner:** `SonicBoom` / `VibrationSystem`.
- **Named consumer?** None.
- **Result:** **A**.

### 4. Sculk encounter as origin

- **Owner:** `SculkShriekerBlockEntity` triggered create.
- **Result:** **A**. Encounter ≠ origin.

**C is not earned for any relationship.**

---

## Wiki disagreements

| Orientation claim | 1.21.1 authority | Conclusion |
|-------------------|------------------|------------|
| Warden is a “boss” biologically / boss-bar peer of Wither/Dragon | No entity boss-bar in `Warden.java`; catalog boss list is PLANNING | **boss ≠ biology** |
| Warden originates from sculk as a life cycle | Shrieker `TRIGGERED` spawn; no developmental inheritance | **Encounter** |
| Blindness / echolocation organ for BP | Vibration game events + anger AI | **A**; no consumer |

---

## Final evidence conclusion

| Gate | Result |
|------|--------|
| New BP field | **No** |
| Existing composition sufficient | **Yes** — `organismKey=warden` + `HostType.INORGANIC` |
| Named consumer of a missing fact | **None** |
| Architectural escalation | **None** |

**A + B; C not earned.** Do not edit Host Registry. Do not “fix” inventory vs HostType.
