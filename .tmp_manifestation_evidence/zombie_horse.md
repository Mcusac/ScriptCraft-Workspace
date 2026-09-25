```text
TEMPORARY EVIDENCE — NOT PROJECT SSOT
Minecraft Java 1.21.1 mapped-source investigation
Do not treat this file as canonical design documentation.
```

# Temporary evidence packet — Zombie Horse

**Status:** Investigation notes only. Not a manifestation report. Not project SSOT.  
**Do not** mint `DESIGN-BIO-MANIFEST-004`, Feature IDs, BP fields, traits, profiles, or Host Registry entries from this file.

**Authoritative source:** Minecraft Java **1.21.1** mapped sources from `implementations/minecraft/AlienCraft/biocraft-alien/build/moddev/artifacts/neoforge-21.1.208-sources.jar` and vanilla data from `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar`.  
**Temporary extract cache:** `.tmp_mc_sources/` (not project SSOT).  
**Comparison input (read-only, not a substitute):** `implementations/minecraft/AlienCraft/docs/design/biological/manifestations/skeleton_horse.md`. Every Zombie Horse claim below was re-checked against 1.21.1 source.

**Grouping note:** This organism was investigated in the same evidence-management batch as Phantom and Camel Husk. That is **not** a biological cluster. No relationship to those organisms is inferred here.

**Later-version exclusion:** Java **1.21.11 / Mounts of Mayhem** zombie-horse horsemen, sun-burn, hostile-cap, mushroom-tempt, horse-armor, and plains/savanna natural spawn are **out of range**. They are recorded only as wiki/web disagreements. They are not 1.21.1 evidence.

---

## Subject

Zombie Horse

## Version

Minecraft Java 1.21.1 (`minecraft_version_range=[1.21.1,1.22)`)

## Target identity

| Axis | 1.21.1 fact | Citation |
|------|-------------|----------|
| Registry name | `zombie_horse` | `EntityType.java:776-783` |
| EntityType field | `EntityType.ZOMBIE_HORSE` | same |
| Factory / category | `EntityType.Builder.of(ZombieHorse::new, MobCategory.CREATURE)` | same |
| Dimensions | `sized(1.3964844F, 1.6F)`, `eyeHeight(1.52F)`, `passengerAttachments(1.31875F)`, `clientTrackingRange(10)` | same |
| Fire immunity | **Not** `fireImmune()` on the builder | same (contrast `Zoglin` at `EntityType.java:761-764`) |
| Class | `public class ZombieHorse extends AbstractHorse` | `ZombieHorse.java:26` |
| Hierarchy | `ZombieHorse` → `AbstractHorse` → `Animal` → `AgeableMob` → `PathfinderMob` → `Mob` → `LivingEntity` | `ZombieHorse.java:26`; `AbstractHorse.java:82` |
| Interfaces via `AbstractHorse` | `ContainerListener`, `HasCustomInventoryScreen`, `OwnableEntity`, `PlayerRideableJumping`, `Saddleable` | `AbstractHorse.java:82` |
| Not a parent | Does **not** extend `Zombie`, `Monster`, `AbstractSkeleton`, or `SkeletonHorse` | class headers |
| Default attributes | `ZombieHorse.createAttributes()` → health **15**, movement **0.2**; jump randomized only | `ZombieHorse.java:36-51`; `DefaultAttributes.java:171` |
| Baby scale | Half-scale of adult Zombie Horse dimensions | `ZombieHorse.java:27-30,83-86` |
| Spawn egg | `Items.ZOMBIE_HORSE_SPAWN_EGG` | `Items.java:1526-1527` |
| Renderer | `UndeadHorseRenderer` + `ModelLayers.ZOMBIE_HORSE`; texture `textures/entity/horse/horse_zombie.png` | `EntityRenderers.java:205`; `UndeadHorseRenderer.java:16-23`; `ModelLayers.java:180` |

Ordinary Horse for contrast: same adult width/height/eyeHeight, **different** passenger attachment (`1.44375F`), same `CREATURE` category (`EntityType.java:419-422`). Ordinary Horse default attributes come from `AbstractHorse.createBaseHorseAttributes()` (health 53 / speed 0.225) then spawn-time randomization of health, speed, and jump (`DefaultAttributes.java:122`; `Horse.java:48-53`).

Ordinary Zombie for contrast: `Zombie extends Monster`, `MobCategory.MONSTER`, different dimensions (`EntityType.java:767-775`; `Zombie.java:67`).

---

## Behavior ownership table

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP representation? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|----------------------------|--------------------|-------|
| Registry identity | `EntityType.ZOMBIE_HORSE` | `EntityType.java:776-783` | Identity only | `organismKey = zombie_horse` via Host Registry lookup | Analyzer / resolver identity projection | **B** |
| Class / horse implementation | `ZombieHorse extends AbstractHorse` | `ZombieHorse.java:26`; `AbstractHorse.java:82` | No. Inheritance ≠ ancestry | Identity sufficient | None needing a horse-undead field | **A/B** |
| Attributes | `ZombieHorse.createAttributes` + jump roll | health 15, speed 0.2; jump via `generateJumpStrength` (`ZombieHorse.java:36-51`) | No missing fact | Identity sufficient | None | **A/B** |
| Goals | `AbstractHorse.registerGoals`; Zombie Horse empties `addBehaviourGoals` | Panic, crazy-run, breed, follow-parent, stroll, look (`AbstractHorse.java:161-175`); **no** `FloatGoal` / `TemptGoal` (`ZombieHorse.java:79-81`) | No | Not needed | None | **A** |
| Ordinary untamed interaction | `ZombieHorse.mobInteract` | Untamed → `InteractionResult.PASS` (`ZombieHorse.java:75-77`) | No | Identity sufficient | None | **A/B** |
| Ride-to-tame path | `RunAroundLikeCrazyGoal` **exists** on `AbstractHorse`, but cannot start from ordinary interact | Goal requires `isVehicle()` (`RunAroundLikeCrazyGoal.java:24-37`); untamed interact never calls `doPlayerRide` | No | Not needed | None | **A** |
| Programmatic tame / trap | **No Zombie Horse owner** | No trap field/goal. Thunder path creates **only** `SkeletonHorse` (`ServerLevel.java:491-497`) | No | Not needed | None | **A** |
| Saddle | `AbstractHorse.isSaddleable` + `SaddleItem` | Saddleable only if alive, adult, **and tamed** (`AbstractHorse.java:253-255`; `SaddleItem.java:20-21`) | No | Identity sufficient | None | **A** |
| Horse armor / BODY slot | `Mob.canUseSlot` default (Zombie Horse does not override) | `Mob.java:931-933` returns `slot != BODY`; only `Horse.canUseSlot` returns true (`Horse.java:224-226`) | No | Not needed | None | **A** |
| Riding / jump / inventory UI when already tamed | Inherited `AbstractHorse` | `mobInteract` defers to super only if `isTamed()` (`ZombieHorse.java:75-77`; `AbstractHorse.java:708-730`) | No | Identity sufficient | None | **A/B** |
| Mating | `AbstractHorse.canMate` | **Always `false`**; Zombie Horse does not override (`AbstractHorse.java:898-900`) | No live reproduction | Not needed | None | **A** |
| Offspring factory | `ZombieHorse.getBreedOffspring` | `EntityType.ZOMBIE_HORSE.create(level)` (`ZombieHorse.java:70-72`) | Construction capability only; gated by `canMate` | Identity sufficient | None | **A/B** |
| Ordinary horse breeding | `Horse.canMate` / donkey cross | Horse mates Horse or Donkey only (`Horse.java:173-178`) — Zombie Horse is neither | No conversion/hybrid | Not needed | None | **A** |
| Natural biome / structure spawn | **No 1.21.1 worldgen owner** | Resource-jar byte scan: `zombie_horse` appears only in lang, loot, `#zombies`, `#dismounts_underwater`. No biome, structure, or advancement JSON | No | Not needed | None | **A** |
| Spawn *placement* (egg/spawner/command) | `SpawnPlacements` + `ZombieHorse.checkZombieHorseSpawnRules` | ON_GROUND (`SpawnPlacements.java:153`); non-spawner uses `Animal.checkAnimalSpawnRules` (grass + light > 8) (`ZombieHorse.java:40-46`; `Animal.java:104-112`) | Placement predicate, not ecology | Not needed | None | **A** |
| Thunder / trap / rider encounter | **Absent** | `ServerLevel.tickChunk` constructs Skeleton Horse only (`ServerLevel.java:483-497`). `ZombieHorse` has no trap NBT/goal | No | Not needed | None | **A** |
| Zombie conversion | **Absent** | `Zombie.convertToZombieType` takes `EntityType<? extends Zombie>` (`Zombie.java:275-276`). No `convertTo(ZOMBIE_HORSE)` anywhere | Name/tag only | Not needed | None | **A** |
| Sun burn | **Absent** | Sun sensitivity lives on `Zombie.isSunSensitive` / zombie AI, not inherited | No immunity fact consulted | Not needed | None | **A** |
| Water breathing | `#minecraft:can_breathe_under_water` via `#undead` | `LivingEntity.canBreatheUnderwater` (`LivingEntity.java:382-384`; tag composition `EntityTypeTagsProvider.java:65-66,40`) | Tag rule, not anatomy | Not needed | None | **A** |
| Water riding / dismount | `#minecraft:dismounts_underwater` **includes** Zombie Horse | `Entity.dismountsUnderwater` (`Entity.java:2335-2337`; tag JSON line 14). Skeleton Horse is **absent** from that tag | No | Not needed | None | **A** |
| Water slowdown | Default `LivingEntity.getWaterSlowDown` = **0.8F** | `LivingEntity.java:2206-2208`. Skeleton Horse overrides to 0.96; Zombie Horse does not | No | Identity sufficient | None | **A** |
| Undead effect/combat tags | `#zombies` → `#undead` consumers | poison/regen ignore, inverted heal/harm, wither friends, smite, armadillo fear | Gameplay taxonomy | Not needed | None | **A** |
| `#minecraft:zombies` itself | Tag membership only | `EntityTypeTags.ZOMBIES` is **only** read to compose `#undead` (`EntityTypeTagsProvider.java:28-40`). No other 1.21.1 Java gameplay reader | Taxonomy grouping | Not needed | None | **A** |
| Loot | `loot_table/entities/zombie_horse.json` | 0–2 rotten flesh + looting | Presentation/drop, not anatomy | Not needed | None | **A** |
| Sounds | Zombie Horse sound events | ambient/death/hurt only; **no** water-specific sounds (`ZombieHorse.java:54-66`; `SoundEvents.java:1597-1599`) | Presentation | Not needed | None | **A** |
| Renderer / texture | Shared undead-horse renderer family, distinct texture | `UndeadHorseRenderer` map (`UndeadHorseRenderer.java:16-23`) | Presentation | Not needed | None | **A** |
| Persistence | `Animal.removeWhenFarAway` = false | `Animal.java:121-123` (CREATURE, not monster despawn) | No | Not needed | None | **A** |
| Freeze | Not in `#freeze_immune_entity_types` | `Entity.canFreeze` (`Entity.java:3584-3586`) | No | Not needed | None | **A** |
| Wind-charge anger | Not in `#no_anger_from_wind_charge` | tag JSON lists Zombie/Husk/Skeleton/etc., not Zombie Horse | No | Not needed | None | **A** |
| Advancements | `kill_a_mob` / `kill_all_mobs` omit this type | No `zombie_horse` / `skeleton_horse` in those JSONs | No | Not needed | None | **A** |
| BioCraft Host Registry | `hosts.json` `vanilla_hosts.undead` includes `"zombie_horse"` | `hosts.json:13-18`; parser `HostConfigParser.java:97-98,141-143`; bind `HostConfigLoader.java:119-122` | Participation key | `organismKey` + optional `HostType.UNDEAD` | Resolver / Analyzer | **B** |
| BioCraft eligibility | `HostType.UNDEAD.isSuitableForXenomorph() == false` | `HostType.java:20,44-46`; `MobHostRegistry.java:68-70`; facehugger `HostValidationHelper.java:14-20` | Suitability bucket, **locked** | Existing HostType | Lifecycle gate (reject) | **B** |
| BioCraft contribution copy | Generic `GestationManager.writeContributingSource` | Would copy host registry path if gestation ran (`GestationManager.java:164-176`) | Source identity, not new biology | existing `contributingSourceKey` | Machinery **LIVE**, production path **lifecycle-blocked** | **B** |

Default remains **A/B**. **C is not earned.**

---

## Configuration audit

Independently verified. Skeleton Horse’s contribution status was **not** copied; the same files were re-read for `zombie_horse`.

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` key `"zombie_horse"` | **LIVE** | `vanilla_hosts.undead.mobs` includes `"zombie_horse"` (`hosts.json:16-17`) | Registered participation. Registration ≠ eligibility ≠ manifestation |
| HostType | **LIVE** | Parser maps undead group → `HostType.UNDEAD` (`HostConfigParser.java:98,141-143`) | Suitability bucket, not ancestry |
| `HostType.UNDEAD.isSuitableForXenomorph()` | **LIVE / locked false** | `HostType.java:20,44-46` | Current lifecycle rejects xenomorph hosting. Do not reopen |
| `MobHostRegistry` bind | **LIVE** | `HostConfigLoader.java:119-122` | `zombie_horse` is queryable after load |
| Resolver identity | **LIVE** | `BiologicalProfileResolver.java:41-56` looks up `organismKey` in Host Registry | `resolve("zombie_horse")` yields `organismKey=zombie_horse`, `HostType.UNDEAD`, `hostEffectProfileId=undead`, empty form/behavior |
| `contributingSourceKey` machinery | **LIVE, lifecycle-blocked** | Port/payload (`BiologicalProfilePort.java:32-37`; `CompiledBiologicalProfile.java:117-124`); copy (`GestationManager.java:164-176`); Analyzer projection (`BiologicalProfileDnaAnalysisPort.java:39-42`) | Not DEAD and not absent. Facehugger/ovomorph will not start this host (`HostEligibilityService.java:19-44`). No new field needed |
| Analyzer | **LIVE** | `DnaAnalysisReport` is a dumb projection of compiled refs (`DnaAnalysisReport.java:14-18`) | Identity consumer only |
| Capture | **LIVE (generic)** | Alive non-player (`CaptureEligibilityPolicy.java:19-21`) | A spawned Zombie Horse can be captured. Capture ≠ gestation eligibility |
| Host-effect pack `undead.json` | **LIVE pack, not organism-specific** | `default_dna: "undead"` (`hosts.json:14`); pack file `parasite/host_effects/undead.json`; names `HostEffectProfileNames.UNDEAD` | Shared undead attachment pack. Not Zombie Horse biology. Attachment currently blocked by suitability |
| Zombie Horse-specific entity/AI/lifecycle/render JSON | **ABSENT** | No `zombie_horse` under `biocraft-alien/src/main/resources` except `hosts.json` | Vanilla remains gameplay owner |
| Adjacent `entity/xenomorph/mob-based/hostile/undead/zombie.json` | **STUB / DEAD-UNUSED** | Stub `variant_id: zombie`; `mob_catalog.json` `bootstrap_entries` loads only spider, creeper, wolf, enderman | Ordinary-Zombie stub. **Not transferable** to Zombie Horse |
| `deep_mob_configs` | **PLANNING ONLY** | Lists `zombie` / `skeleton`, **not** `zombie_horse` (`mob_catalog.json:9-30`) | Planning matrix; loader uses `bootstrap_entries` |
| `rangedAttacks` | **ABSENT for this organism** | No Zombie Horse ranged owner in vanilla or BioCraft | Do not invent a consumer |
| Identity-specific tests | **TEST coverage absent** | `BiologicalProfileResolverTest` asserts undead for `skeleton` / `husk` / `drowned`, **not** `zombie_horse` | Generic resolver would still match the registered key; no C-level contract |
| Inventory row | **PLANNING ONLY** | `vanilla_organism_inventory.md` category `undead`, manifestation `next` | Accounting label, not HostType or BP |

**Contribution verdict (do not collapse):** registration is **LIVE**; resolver participation is **LIVE**; genetic-contribution *production from this host* is **lifecycle-blocked** by locked UNDEAD unsuitability; it is **not absent**.

---

## Tags: membership to named 1.21.1 consumer

| Tag | Membership | Named 1.21.1 consumer | Meaning |
|-----|------------|----------------------|---------|
| `#minecraft:zombies` | Direct (`zombies.json`) | **No Java gameplay reader** except composing `#undead` (`EntityTypeTagsProvider.java:28-40`) | Grouping only |
| `#minecraft:undead` | Via `#zombies` | Armadillo fear (`Armadillo.java:237-238`); wither targeting via `#wither_friends` | Gameplay taxonomy |
| `#minecraft:can_breathe_under_water` | Via `#undead` | `LivingEntity.canBreatheUnderwater` | Runtime capability |
| `#minecraft:ignores_poison_and_regen` | Via `#undead` | `LivingEntity.canBeAffected` | Effect rule |
| `#minecraft:inverted_healing_and_harm` | Via `#undead` | `LivingEntity.isInvertedHealAndHarm` | Effect rule |
| `#minecraft:sensitive_to_smite` | Via `#undead` | Smite damage predicate (`Enchantments.java` uses `SENSITIVE_TO_SMITE`) | Combat rule |
| `#minecraft:wither_friends` | Via `#undead` | `WitherBoss` targeting exclusion | Combat relationship |
| `#minecraft:dismounts_underwater` | Direct | `Entity.dismountsUnderwater` | Rider dismounts in water. **Diverges from Skeleton Horse** |
| `#minecraft:skeletons` | **Absent** | Creeper disc loot (Skeleton Horse path) | Not a skeleton-tag member |
| `#minecraft:freeze_immune_entity_types` | Absent | `Entity.canFreeze` | Normal freeze |
| `#minecraft:no_anger_from_wind_charge` | Absent | LivingEntity retaliation bookkeeping | Normal anger path |
| `#minecraft:fall_damage_immune` | Absent | Fall-damage tag consumer | Normal fall damage |

Tag membership is combat/effect/loot taxonomy, not ancestry.

---

## Controlled relationship tests

Each test run separately. Skeleton Horse report used only to **test claimed relationships**, not to copy conclusions.

### 1. Zombie ↔ Zombie Horse

| Question | Result |
|----------|--------|
| 1. Actual source-level relationship? | **Tag + name + rotten-flesh loot + shared undead tag consumers.** No class, conversion, or spawn coupling |
| 2. Implementation inheritance? | **No.** `Zombie extends Monster`; `ZombieHorse extends AbstractHorse` |
| 3. Entity conversion? | **No.** `convertToZombieType` requires `EntityType<? extends Zombie>` (`Zombie.java:275`). No `ZOMBIE_HORSE` conversion site |
| 4. Spawning/encounter coupling? | **No** in 1.21.1. No horseman, no biome co-spawn, no structure NBT |
| 5. Gameplay taxonomy? | **Yes.** Direct `#minecraft:zombies` → `#undead` |
| 6. Actual biological evidence? | **No** |
| 7. Named BioCraft consumer needing that as a biological fact? | **No.** Distinct `organismKey` values (`zombie` vs `zombie_horse`). Shared HostType `UNDEAD` is a suitability bucket |

**Result: A/B. Reject Zombie ancestry and Zombie Profile inheritance.**

### 2. Skeleton Horse ↔ Zombie Horse

| Question | Result |
|----------|--------|
| 1. Actual source-level relationship? | **Sibling `AbstractHorse` subclasses** with parallel class shape (empty `addBehaviourGoals`, gated `mobInteract`, offspring factory, similar attributes/dimensions). Shared **renderer class**, different textures. **Different tags** (`#skeletons` vs `#zombies`). **Different water/dismount owners.** Skeleton Horse has trap; Zombie Horse does not |
| 2. Implementation inheritance? | **Shared parent `AbstractHorse` only.** Neither extends the other |
| 3. Entity conversion? | **No** |
| 4. Spawning/encounter coupling? | **No.** Thunder trap is Skeleton Horse exclusive (`ServerLevel.java:491-497`) |
| 5. Gameplay taxonomy? | Both reach `#undead` by **different** tag branches. `UndeadHorseRenderer` is a client map of two `EntityType`s, not a clade |
| 6. Actual biological evidence? | **No.** Parallel horse implementation ≠ undead-horse biology |
| 7. Named BioCraft consumer? | **No.** Separate registered keys |

**Result: A/B. Reject Skeleton Horse ancestry, undead-horse clade, and shared-horse-mechanic lineage.**

Independently confirmed divergences vs Skeleton Horse (not copied from that report):

| Axis | Skeleton Horse | Zombie Horse |
|------|----------------|--------------|
| Parent / category | `AbstractHorse` / `CREATURE` | same |
| Trap | Yes (`SkeletonTrapGoal` + `ServerLevel`) | **None** |
| Water slowdown / sounds | Override 0.96 + water sounds | Default 0.8; dry sounds only |
| `#dismounts_underwater` | Absent | **Present** |
| Minecraft tag branch | `#skeletons` | `#zombies` |
| Loot | bones | rotten flesh |
| Ordinary untamed interact | PASS | PASS |
| Programmatic tame owner | Trap `setTamed(true)` | **None** |

### 3. Zombie Horse ↔ ordinary horse mechanics

| Question | Result |
|----------|--------|
| 1. Actual source-level relationship? | **Yes: `AbstractHorse` inheritance** (inventory, saddle API, jump, goals, NBT tame/owner) |
| 2. Implementation inheritance? | **Yes** |
| 3. Entity conversion? | **No** Horse↔ZombieHorse |
| 4. Spawning/encounter coupling? | **No.** Ordinary Horse uses biome animal spawn; Zombie Horse has placement rules but no biome list |
| 5. Gameplay taxonomy? | Both `CREATURE`. Zombie Horse is **also** `#zombies`/`#undead`. Ordinary Horse is in `#dismounts_underwater` with Zombie Horse; that is a mount-water rule, not undeath |
| 6. Actual biological evidence? | Horse **mechanics** are inherited. That is not Horse→ZombieHorse descent and not an undead-horse trait |
| 7. Named BioCraft consumer? | **No** horse-anatomy / undead-horse field consumer |

Important inherited-but-gated facts:

- Ordinary Horse **can** start riding while untamed (`Horse` uses super `mobInteract` after variant/food handling). Zombie Horse **cannot**.
- Ordinary Horse **canMate** with Horse/Donkey. `AbstractHorse.canMate` is `false`; Zombie Horse keeps that gate.
- Ordinary Horse **can** use BODY armor (`Horse.canUseSlot`). Zombie Horse cannot.
- Ordinary Horse randomizes three attributes; Zombie Horse fixes health/speed and randomizes jump only.

**Result: A. Vanilla horse owners plus Zombie Horse gates. No BP field.**

---

## Tempting but rejected interpretations

Reject unless a named consumer later proves otherwise (none did):

1. **Zombie ancestry** because of the name `ZombieHorse` / registry `zombie_horse`
2. **Zombie Profile inheritance** because both are HostType `UNDEAD` or share `default_dna: "undead"`
3. **Skeleton Horse ancestry** or an **undead-horse clade** because of sibling `AbstractHorse` classes, shared `UndeadHorseRenderer`, similar attributes, or similar interaction gates
4. **Horse undead trait** / **undead horse biology** as a BP dimension
5. **Lineage from `#minecraft:zombies`** (no Java gameplay reader except `#undead` composition)
6. **Conversion/transformation** Horse→Zombie Horse or Zombie→Zombie Horse (no `convertTo` site; type bound forbids `ZOMBIE_HORSE` in `convertToZombieType`)
7. **Trap/thunder/rider encounter** analog of Skeleton Horse (source creates Skeleton Horse only)
8. **Natural plains/savanna horsemen, sun-burn, hostile-cap, mushroom tempt, horse armor, 25 HP** — those are **1.21.11+ / Mounts of Mayhem**, not 1.21.1
9. **Live reproduction** from `getBreedOffspring` while `canMate` is false
10. **Taming like a normal horse in survival** — untamed `mobInteract` is PASS; no trap sets tame
11. **Inventory category `undead`** as ancestry, HostType, or manifestation
12. **Shared undead/horse mechanics** as biological composition
13. **Transferring Skeleton Horse contribution status without checking** — checked independently; similar pattern, not copied
14. **Relationship to Phantom or Camel Husk** from the evidence-management grouping
15. **Stub `zombie.json` xenomorph catalog** as a Zombie Horse owner
16. **Loot (rotten flesh) or texture (`horse_zombie.png`)** as anatomy/clade authority
17. **CREATURE category** as proof of animal biology that BioCraft must encode
18. Inventing a consumer because unused spawn-placement rules or gated horse APIs are interesting

---

## Potential biological relationships

### Ordinary Zombie

| Item | Finding |
|------|---------|
| Relationship | Gameplay taxonomy (`#zombies` → `#undead`) + presentation (name, rotten flesh). **No** inheritance, conversion, or spawn coupling |
| Owner | Vanilla tags / loot / `Zombie` class (separate) |
| Biological input? | No missing biological fact |
| Existing composition | Distinct `organismKey` (`zombie` vs `zombie_horse`) |
| Named consumer | None that needs Zombie Horse to be “made of Zombie” |
| Result | **A/B — reject ancestry** |

### Skeleton Horse

| Item | Finding |
|------|---------|
| Relationship | Sibling `AbstractHorse` implementation + shared renderer **class** + parallel gates. Divergent trap, water, tags, loot, tame owner |
| Owner | Vanilla horse package / client renderer map |
| Biological input? | No |
| Existing composition | Distinct `organismKey` (`skeleton_horse` vs `zombie_horse`) |
| Named consumer | None needing an undead-horse clade |
| Result | **A/B — reject clade / ancestry** |

### Ordinary Horse

| Item | Finding |
|------|---------|
| Relationship | **Implementation inheritance** of horse mechanics; several mechanics gated or omitted |
| Owner | `AbstractHorse` / `Horse` |
| Biological input? | No horse-anatomy or undeath trait required |
| Existing composition | Distinct keys (`horse` is `LIVING_BIOLOGICAL`; `zombie_horse` is `UNDEAD`) |
| Named consumer | None |
| Result | **A — vanilla owners sufficient** |

---

## Wiki / later-version disagreements

Wiki and current web results are **orientation only**. 1.21.1 source wins.

| Claim encountered | 1.21.1 authority | Conclusion |
|-------------------|------------------|------------|
| 1.21.11: natural plains/savanna spawn with zombie spear horsemen | No biome/structure/event JSON contains `zombie_horse`; thunder path is Skeleton Horse only | **Exclude.** Later version |
| 1.21.11: burns in sunlight, hostile cap, despawns like monsters | `CREATURE`; no `Zombie.isSunSensitive`; `Animal.removeWhenFarAway=false`; EntityType not fire-immune | **Exclude.** Later version |
| 1.21.11: tame like a horse; red mushrooms; horse armor; 25 HP | Untamed interact PASS; `addBehaviourGoals` empty (no tempt); BODY slot false; health 15 | **Exclude.** Later version |
| Historical “does not spawn naturally / creative only” | Placement rules exist for egg/spawner/command; **no** worldgen/event selector | Keep **construction possible** vs **no natural/event owner** distinct |
| “Cannot breed” | `canMate=false` | Agrees; callable offspring factory is not a live path |
| “Cannot be tamed” (survival) | Untamed `PASS`; no trap `setTamed` | Agrees for ordinary interaction. NBT/commands can still set `Tame` because `AbstractHorse` persists that flag |
| Shared “undead horse” wiki grouping | Renderer map + sibling classes only | Presentation/implementation, not biology |

---

## 1.21.1 authority anchors

- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/ZombieHorse.java:26-86` — hierarchy, attributes, spawn-placement predicate, sounds, offspring factory, gated interact, empty behaviour goals, baby dimensions
- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/AbstractHorse.java:82,161-180,253-255,708-730,898-910` — horse goals, saddleable-if-tamed, riding UI, `canMate=false`, default offspring `null`
- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/Horse.java:37,48-53,173-178,224-226` — ordinary horse randomization, mating, BODY armor
- `.tmp_mc_sources/net/minecraft/world/entity/animal/horse/SkeletonHorse.java` — sibling comparison only (trap/water/sounds); re-read, not copied
- `.tmp_mc_sources/net/minecraft/world/entity/monster/Zombie.java:67,267-276` — separate Monster hierarchy; conversion bound `EntityType<? extends Zombie>`
- `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java:419-422,767-783` — Horse / Zombie / Zombie Horse registration
- `.tmp_mc_sources/net/minecraft/world/entity/SpawnPlacements.java:153` — placement registration
- `.tmp_mc_sources/net/minecraft/world/entity/animal/Animal.java:104-123` — animal spawn light/grass; no despawn
- `.tmp_mc_sources/net/minecraft/server/level/ServerLevel.java:483-497` — thunder creates Skeleton Horse only
- `.tmp_mc_sources/net/minecraft/world/entity/ai/goal/RunAroundLikeCrazyGoal.java:24-73` — tame-while-ridden; unreachable via ordinary Zombie Horse interact
- `.tmp_mc_sources/net/minecraft/world/item/SaddleItem.java:20-21` — requires `isSaddleable()`
- `.tmp_mc_sources/net/minecraft/world/entity/Mob.java:931-933` — BODY slot false by default
- `.tmp_mc_sources/net/minecraft/world/entity/LivingEntity.java:382-384,1002-1028,2206-2208` — undead tag consumers; default water slowdown
- `.tmp_mc_sources/net/minecraft/world/entity/Entity.java:2335-2337,3584-3586` — dismounts underwater; freeze
- `.tmp_mc_sources/net/minecraft/data/tags/EntityTypeTagsProvider.java:28-40,65-66,102-116,138-156` — tag composition including Zombie Horse in zombies + dismounts
- `.tmp_mc_sources/data/minecraft/tags/entity_type/zombies.json` — direct membership
- `.tmp_mc_sources/data/minecraft/tags/entity_type/dismounts_underwater.json` — direct membership
- `.tmp_mc_sources/data/minecraft/loot_table/entities/zombie_horse.json` — rotten flesh 0–2
- `.tmp_mc_sources/net/minecraft/client/renderer/entity/UndeadHorseRenderer.java:16-23` — texture map
- `.tmp_mc_sources/net/minecraft/client/renderer/entity/EntityRenderers.java:172,205` — renderer registration
- AlienCraft: `hosts.json:13-18`; `HostType.java:20,44-46`; `HostConfigParser.java:98`; `HostConfigLoader.java:119-122`; `BiologicalProfileResolver.java:41-56`; `HostEligibilityService.java:19-44`; `GestationManager.java:164-176`

Vanilla resource-jar content scan (all bytes): `zombie_horse` occurs only in `en_us.json`, entity loot, `#zombies`, and `#dismounts_underwater`.

---

## Final evidence conclusion

```
New BP field earned: NO
Existing composition sufficient: YES
Named consumer exists: NO
Architectural escalation required: NO
```

`Named consumer exists` here means a named live BioCraft consumer that needs a **missing biological fact** (C). Analyzer/resolver already consume **identity** (`organismKey = zombie_horse`); that is B, not C.

```
A = vanilla owns spawn placement, horse mechanics, tags, loot, rendering, water/dismount, mating gate, absence of trap/conversion/sun-burn
B = organismKey / HostType / contributingSourceKey machinery distinguish this organism; lifecycle currently blocks production
C = not earned
```

No minimum new biological fact. Stop.

---

## Inventory context (non-authority)

Provisional inventory label `undead`; Host Registry registered `UNDEAD`; eligibility undetermined at inventory layer but **current** `HostType.UNDEAD` suitability is false and locked. Manifestation investigation (this packet) does not change inventory, Host Registry, or eligibility policy.
