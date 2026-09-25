TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent GlowSquid docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/glow_squid.md until synthesis authorizes.

# Glow Squid — biological-manifestation evidence packet

**Status:** Temporary investigator packet. **Not** project SSOT.

Method: existing gameplay → actual owner → biological input? → existing composition sufficient? → named live BioCraft consumer? → **A / B / C**.

Closed leaps: Squid parent ≠ biological clade; glow / dark-ticks / dark spawn ≠ bioluminescence BP without named consumer; glow-ink item/sign ≠ organism light composition; aquatic tag ≠ aquatic BP; registration alone ≠ manifestation evidence.

Existing BP composition checked: `organismKey`, optional `contributingSourceKey`, optional `HostType`, `xenomorphFormKey`, `hostEffectProfileId`, `behaviorTypeKey`.

Default: **NO** new BP field.

---

## Subject

Glow Squid (`minecraft:glow_squid`) — `GlowSquid extends Squid` (implementation sharing only); dark-ticks entity state; client render brightness; ambient `GLOW` particles; glow-ink loot + sign applicator; deep dark-water spawn; Host Registry **LIVE** `living_biological`.

---

## Version

Minecraft Java **1.21.1** only. `.tmp_mc_sources/` (from `neoforge-21.1.208-sources.jar` / client-extra resources) authoritative. Wiki orientation only.

---

## Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:glow_squid` |
| Inventory key | `glow_squid` |
| `EntityType` | `EntityType.GLOW_SQUID` — `EntityType.java` **402–404**: `register("glow_squid", Builder.of(GlowSquid::new, MobCategory.UNDERGROUND_WATER_CREATURE).sized(0.8F, 0.8F).eyeHeight(0.4F).clientTrackingRange(10))` |
| Class | `GlowSquid extends Squid` (`GlowSquid.java` **19**); `Squid extends WaterAnimal` — **inheritance = code reuse, not clade** |
| Category | `MobCategory.UNDERGROUND_WATER_CREATURE` (distinct from Squid’s `WATER_CREATURE`) |
| Attributes | Via `Squid.createAttributes()` — max health **10.0** (`Squid.java` **54–56**; `DefaultAttributes` binds `GlowSquid.createAttributes()`) |
| Spawn placement | `SpawnPlacements` **116**: `IN_WATER` + `MOTION_BLOCKING_NO_LEAVES` + `GlowSquid::checkGlowSquidSpawnRules` |
| Host Registry | **LIVE** — `hosts.json` `vanilla_hosts.living_biological.mobs` includes `"glow_squid"`; HostType `LIVING_BIOLOGICAL`; `default_dna` → `baseline_biological` |

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 / live evidence | Biological input? | Existing BP? | BioCraft consumer? | A/B/C |
|----------|--------------|------------------------|-------------------|--------------|--------------------|-------|
| Identity / size / category | `EntityType.GLOW_SQUID` | **402–404** | Identity | `organismKey=glow_squid` | Resolver + Analyzer + host | **B** |
| Squid locomotion / flee / ink squirt base | `Squid` (inherited) | Goals, `aiStep`, `spawnInk` in `Squid.java` | Entity movement / FX | Identity sufficient | None | **A** |
| Extends Squid | Class hierarchy | `GlowSquid extends Squid` **19** | Implementation sharing | Distinct key already | None treating as clade | **A** |
| Dark-ticks entity state | `DATA_DARK_TICKS_REMAINING` | Synched int; NBT `"DarkTicksRemaining"`; set **100** on successful hurt; decrement in `aiStep` (`GlowSquid.java` **20**, **58–78**, **87–101**) | Entity state | Not needed | **None** | **A** |
| Client entity brightness (“glow”) | `GlowSquidRenderer.getBlockLightLevel` | Lerp 0→15 from `1 - darkTicks/10`; max with super (`GlowSquidRenderer.java` **23–26**) — **client rendering only** | Rendering | Not bioluminescence BP | **None** | **A** |
| World light emission | — | No `getLightEmission` / LightEngine registration on GlowSquid; renderer light ≠ block light | Not present as world light | — | — | **A** |
| Ambient glow particles | `GlowSquid.aiStep` | Always `ParticleTypes.GLOW` at random offsets (**80**) — independent of dark-ticks gate | Particle FX | Not needed | **None** | **A** |
| Ink particle override | `getInkParticle` | Returns `ParticleTypes.GLOW_SQUID_INK` (**27–29**); client pink via `SquidInkParticle.GlowInkProvider` | Particle FX | Not needed | **None** | **A** |
| Glow sounds | Sound overrides | `GLOW_SQUID_*` ambient/hurt/death/squirt (**38–55**) | Presentation | Not needed | None | **A** |
| Glow-ink **drop** | Loot table | `entities/glow_squid.json` / `VanillaEntityLoot` **334–345**: `Items.GLOW_INK_SAC` count 1–3 + looting | Item production | Item ≠ BP composition | **None** | **A** |
| Glow-ink **item use** | `GlowInkSacItem` | `SignApplicator` → `SignText.setHasGlowingText(true)` (`GlowInkSacItem.java` **16–22**) | Block/sign text flag | Sign state ≠ organism glow | **None** | **A** |
| Spawn rules | `checkGlowSquidSpawnRules` | Y ≤ seaLevel−33 **and** `getRawBrightness(pos,0)==0` **and** block is `WATER` (**104–110**) | Encounter conditions | Not origin/adaptation | None | **A** |
| Biome spawn weight | `BiomeDefaultFeatures.caveSpawns` | `UNDERGROUND_WATER_CREATURE` weight 10, count 4–6 (**409**) | Encounter density | Not composition | None | **A** |
| Tags (`#aquatic`, breathe underwater, axolotl hunt, not scary for pufferfish) | Vanilla entity_type tags | Membership only | Tag-driven AI / mechanics | Tag ≠ aquatic BP / clade | Vanilla consumers only | **A** |
| Host contribution | `hosts.json` → eligibility → gestation writer | `"glow_squid"` living_biological; `isSuitableForXenomorph=true` | Identity only | `contributingSourceKey=glow_squid` | **LIVE** generic writer / Resolver / Analyzer | **B** |

No row is **C**. Live `contributingSourceKey=glow_squid` is identity already represented.

---

## Glow probe (categories kept separate)

| Category | Present? | Owner | Notes |
|----------|----------|-------|-------|
| Entity-state | **Yes** | `DATA_DARK_TICKS_REMAINING` / NBT | Hurt → 100 ticks “dark”; counts down |
| Rendering | **Yes** | `GlowSquidRenderer.getBlockLightLevel` | Entity-model brightness only (`@OnlyIn(Dist.CLIENT)`) |
| World light-emission | **No** | — | Does not add block/sky light to the world |
| Gameplay effect (non-render) | **Limited** | Dark ticks gate render lerp; ambient `GLOW` particles always | No damage/buff/light-block gameplay tied to glow state |
| Distinct biological input consumed by BioCraft | **No** | — | No named consumer of dark-ticks / glow / bioluminescence |

**Do not** mint a bioluminescent BP field from this packet.

---

## Glow-ink probe (separate from organism glow state)

| Concern | Owner | Downstream | Relation to organism light |
|---------|-------|------------|----------------------------|
| Item / drop production | Loot `glow_ink_sac` 1–3 | Inventory / crafting / signs | **Separate** from `DATA_DARK_TICKS_REMAINING` |
| Particle / squirt FX | `GLOW_SQUID_INK` particle | Client-only colored ink cloud | Presentation; not light emission |
| Block / entity interaction | `GlowInkSacItem` → sign `hasGlowingText` | Sign text render flag | Item effect on **sign**, not organism composition |
| Biological capability | — | No BioCraft reader of glow ink as BP fact | Item production ≠ automatic biological composition |

---

## Spawn-condition probe

Exact 1.21.1 predicate owner: `GlowSquid.checkGlowSquidSpawnRules` (`GlowSquid.java` **104–110**), registered in `SpawnPlacements` **116**.

```
pos.getY() <= level.getSeaLevel() - 33
  && level.getRawBrightness(pos, 0) == 0
  && level.getBlockState(pos).is(Blocks.WATER)
```

Placement type: `SpawnPlacementTypes.IN_WATER`. Category: `UNDERGROUND_WATER_CREATURE`. Biome feature: `BiomeDefaultFeatures.caveSpawns` weight 10 / 4–6.

**Encounter conditions ≠ organism origin / adaptation / composition.** Dark spawn does not earn a light-adaptation BP field without a named BioCraft consumer.

---

## Host Registry path (LIVE contribution route)

Confirmed chain (registration **and** consumer route):

1. **Participation:** `hosts.json` → `"glow_squid"` under `living_biological` with `default_dna: "baseline_biological"`.
2. **Load:** `HostConfigParser` → `MobHostRegistry.bind` → `HostType.LIVING_BIOLOGICAL` (`suitableForXenomorph=true`).
3. **Eligibility:** `HostEligibilityService.isSuitableForXenomorph` → `MobHostRegistry.isSuitableForXenomorph("glow_squid")` → **true**.
4. **Write route:** `GestationManager.writeContributingSource` — `encodeId(host)` → `HostRegistryPaths.registryPath` (`minecraft:glow_squid` → `glow_squid`) → `ContributingSourceKeys.absentIfBlank` → `ContributingSourcePort.setContributingSourceKey(offspring, "glow_squid")`.
5. **Read / project:** `BiologicalProfileResolver.resolve(ref, contributingSourceKey)` projects `organismKey`, `HostType`, `hostEffectProfileId=baseline_biological`, optional `contributingSourceKey`; `DnaSampleFromOccupant` observes the same Model A pair on carriers.

**B** is therefore justified for identity / contribution. Registration alone would not be enough; the gestation writer + Resolver/Analyzer path is confirmed. Still **B not C** — no glow/ink-specific composition consumer.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"glow_squid"` | **Present / LIVE** | living_biological list | Participation / identity |
| Organism-specific entity JSON | **ABSENT** | No `*glow*` / `*squid*` under biocraft entity configs | Vanilla remains owner of glow/ink/spawn |
| Organism-specific tests | **ABSENT** | No test references `glow_squid` | No dedicated BioCraft glow consumer tests |
| Glow / bioluminescence config keys | **ABSENT** | Host parser forbids biology tuning keys on hosts.json; no glow field elsewhere | Do not invent BP field |
| Resolver / Analyzer / DnaAnalysisPort | **LIVE** generic | Identity projection | Observability ≠ new composition |
| Gestation `writeContributingSource` | **LIVE** generic | Registry path → `glow_squid` | Identity **B** |

---

## Tempting but rejected interpretations

- `extends Squid` → squid/cephalopod biological clade
- Dark-ticks + renderer brightness → bioluminescence BP / light-emission capability
- Ambient `GLOW` particles → BioCraft-consumed glow trait
- `glow_ink_sac` loot or sign glowing text → organism glow composition
- Deep / brightness-0 spawn → cave-adapted light biology field
- `#aquatic` / underwater breathing tags → aquatic BP
- Host Registry registration alone → manifestation **C**
- Grouping with Squid (or other aquatics) from inheritance/tags → shared column

---

## Potential biological relationships

Evidence-only adjacency; **no auto-queue**:

| Peer | Link type | Implication |
|------|-----------|-------------|
| Squid | Shared Java parent + parallel ink loot pattern | Implementation sharing / item parallel — **not** clade or joint BP |
| Axolotl | `#axolotl_hunt_targets` includes glow_squid | Hunt AI tag only |
| Other `living_biological` aquatics | Same HostType bucket | Registry taxonomy, not physiology column |

---

## Final evidence conclusion

| Candidate | Result |
|-----------|--------|
| Identity / Host Registry / `contributingSourceKey=glow_squid` | **B** (LIVE route confirmed) |
| Squid inheritance, locomotion, dark-ticks, client glow render, particles, sounds, spawn, tags | **A** |
| Glow-ink drop / sign applicator | **A** (item/block FX; not organism BP) |
| New BP field (bioluminescence / aquatic / ink) | **NO** |
| **C** | **Not earned** |

**Verdict:** Existing composition (`organismKey` + optional `contributingSourceKey` + HostType / `baseline_biological` routing) is sufficient. Vanilla owns glow presentation, dark-ticks, spawn, and glow-ink. No named live BioCraft consumer requires a new biological field. **C was not earned.**

---

## Source anchors (1.21.1)

- `.tmp_mc_sources/net/minecraft/world/entity/GlowSquid.java`
- `.tmp_mc_sources/net/minecraft/world/entity/animal/Squid.java` (inheritance comparison only)
- `.tmp_mc_sources/net/minecraft/client/renderer/entity/GlowSquidRenderer.java`
- `.tmp_mc_sources/net/minecraft/world/item/GlowInkSacItem.java`
- `.tmp_mc_sources/net/minecraft/client/particle/SquidInkParticle.java`
- `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` / `SpawnPlacements.java`
- `.tmp_mc_sources/data/minecraft/loot_table/entities/glow_squid.json`
- `biocraft-alien/.../systems/hosts.json`
- `MobHostRegistry` / `HostEligibilityService` / `GestationManager.writeContributingSource` / `HostRegistryPaths` / `BiologicalProfileResolver`
