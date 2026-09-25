TEMPORARY EVIDENCE — NOT PROJECT SSOT

# Frog — temporary manifestation evidence packet

## Subject
- Inventory key: `frog`
- Minecraft id: `minecraft:frog`
- Authority set: NeoForge 21.1.208 mapped sources (Java 1.21.1) + client-extra resources + live BioCraft `biocraft-alien` code/resources/tests
- Scope: research/design-evidence only; no Java/hosts/BP/canonical manifestation edits

## Version
Minecraft Java **1.21.1** (NeoForge **21.1.208** sources + resources jars)

## Target identity
| Fact | Evidence |
|------|----------|
| Hierarchy | `Frog extends Animal implements VariantHolder<Holder<FrogVariant>>` → `AgeableMob` → `PathfinderMob` → `Mob` → `LivingEntity` |
| Registration | `EntityType.FROG` in `EntityType.java`: `Builder.of(Frog::new, MobCategory.CREATURE).sized(0.5F, 0.5F).passengerAttachments(...).clientTrackingRange(10)` |
| Dimensions | width **0.5**, height **0.5** |
| Category | `MobCategory.CREATURE` |
| Package | `net.minecraft.world.entity.animal.frog.Frog` |
| Inventory row (locked design) | `vanilla_organism_inventory.md`: bio-organic, **unregistered**, manifestation pending — treated as orientation only for Host Registry status |

---

## Behavior ownership table

Method per row: **owner → biological input? → existing BP composition? → named live BioCraft consumer? → A/B/C**

| Behavior | Actual owner | 1.21.1 evidence | Biological input? | Existing BP representation? | BioCraft consumer? | A/B/C |
|----------|--------------|-----------------|-------------------|-----------------------------|--------------------|-------|
| Entity type / identity | Vanilla `EntityType` + `Frog` class | `EntityType.FROG` registration; class hierarchy above | Identity key only if BioCraft admits organism | Sparse resolve by `organismKey` string (no frog-specific fields) | **None** named for frog (no module refs) | **A** |
| Variant (temperate/warm/cold) | Vanilla `FrogVariant` registry + `Frog` synched/NBT + spawn biome tags | `FrogVariant` record = **texture** path only (`TEMPERATE`/`WARM`/`COLD`); `DATA_VARIANT_ID`; NBT `"variant"`; `finalizeSpawn` sets from `BiomeTags.SPAWNS_COLD_VARIANT_FROGS` / `SPAWNS_WARM_VARIANT_FROGS` else temperate default | Visual/spawn-cosmetic + **vanilla loot gate** when frog kills magma cube (froglight color). Not adaptation/trait | No BP variant/adaptation field; `organismKey` alone | **None** independent of `organismKey` | **A** |
| Tongue targeting | `FrogAttackablesSensor` → `MemoryModuleType.NEAREST_ATTACKABLE` / `ATTACK_TARGET` | Sensor matches `Frog.canEat` + path reachability memory; range 10 | Prey-selection AI, not anatomy schema | No tongue/anatomy field in `CompiledBiologicalProfile` | **None** | **A** |
| Tongue extension / pose / sync | `ShootTongue` + `Frog` synched tongue target + `Pose.USING_TONGUE` | `setTongueTarget` / `DATA_TONGUE_TARGET_ID`; pose drives client `tongueAnimationState`; sounds `FROG_TONGUE` / `FROG_EAT` | Presentation + attack sequencing | No | **None** | **A** |
| Target transport (pull) | `ShootTongue` tick | On catch: sets target delta toward frog (`normalize().scale(0.75)`); then `doHurtTarget` | Combat/VFX, not feeding trait | No | **None** | **A** |
| Tongue gameplay effect (kill / eat) | `ShootTongue.eatEntity` → `Mob.doHurtTarget` (ATTACK_DAMAGE 10) | Kills `#frog_food` entities; may `remove(KILLED)` after death | Vanilla combat outcome | No | **None** | **A** |
| Slimeball from frog “eating” | **Slime loot table**, not frog entity loot | `data/minecraft/loot_table/entities/frog.json` is **empty** (no pools). `slime.json`: size-1 slime drops `slime_ball`; frog-as-`source_entity` forces count **1** | Loot rule, not frog anatomy | No | **None** | **A** |
| Froglight from magma cube | **Magma cube loot table** gated by **frog variant** | `magma_cube.json`: warm→`pearlescent_froglight`, cold→`verdant_froglight`, temperate→`ochre_froglight` when damage source is that frog variant | Vanilla loot mapping variant→item; not BP subtype | No | **None** | **A** |
| Tempt / breed food item | `ItemTags.FROG_FOOD` + `Frog.isFood` / `FrogAi.getTemptations` | Tag values: `minecraft:slime_ball` only; sensors `FROG_TEMPTATIONS` | Breeding item gate | No | **None** | **A** |
| Prey entity AI (`#frog_food`) | `EntityTypeTags.FROG_FOOD` + `Frog.canEat` | Tag: `slime`, `magma_cube`; `canEat` rejects slime size ≠ 1 | Hunt target filter | No | **None** | **A** |
| Land / water movement | `Frog` move/nav + `FrogAi` IDLE/SWIM/LONG_JUMP | `AmphibiousPathNavigation` + `FrogNodeEvaluator`; `SmoothSwimmingMoveControl`; water path malus; `travel` water branch; activities `SWIM` / `TryFindLand` / long-jump on land | Amphibious **AI/pathfinding**, not `#aquatic` membership | No aquatic BP field exists to fill; would be leap if invented | **None** | **A** |
| Underwater breathing | `#minecraft:can_breathe_under_water` → `LivingEntity.canBreatheUnderwater()` | Frog **is** in tag; drowning skip uses tag | Tag-driven drowning exemption | No | **None** | **A** |
| Fall damage mitigation | `Frog.calculateFallDamage` (−5) | Class override; **not** `#fall_damage_immune` | Numeric damage tweak | No | **None** | **A** |
| Breeding → pregnancy memory | `Frog.spawnChildFromBreeding` | Calls `finalizeSpawnChildFromBreeding(..., null)` then sets `MemoryModuleType.IS_PREGNANT` (no baby frog entity from love) | Lifecycle memory | No | **None** | **A** |
| Frogspawn placement | `TryLaySpawnOnWaterNearLand` + `FrogAi` `LAY_SPAWN` | Places `Blocks.FROGSPAWN` beside water when pregnant + on land | Block spawn behavior | No | **None** | **A** |
| Tadpole spawn from hatch | `FrogspawnBlock.hatchFrogspawn` / `spawnTadpoles` | Creates `EntityType.TADPOLE` (2–5), not `Frog`; frogspawn tick delay | **Separate entity** lifecycle owned by block | Out of frog BP composition; do not absorb tadpole here | **None** (frog path) | **A** |
| Host Registry participation | BioCraft `hosts.json` / `MobHostRegistry` | `"frog"` **absent** from all host lists | Participation ≠ biology fact | Soft-fail resolve: `hostType` empty for unknown keys | Resolver may be called with arbitrary key; **no frog-specific consumer** | **A** (absence ≠ missing BP) |

**A/B/C legend (this packet):** **A** = vanilla-owned; no earned BioCraft BP field / no named frog consumer. **B** = existing sparse composition sufficient for a named live consumer. **C** = new BP field earned by named live consumer needing a missing fact.

---

## Configuration audit table

| Surface | Frog presence | Classification | Notes |
|---------|---------------|----------------|-------|
| `data/biocraft_alien/systems/hosts.json` | **Absent** (`frog` not in any `mobs` array; not in `variant_mappings`) | **LIVE** config, frog **unregistered** | Matches inventory “unregistered”; not a BP gap |
| `MobHostRegistry.getHostType("frog")` | Returns `null` via `getOrDefault` | **LIVE** | Soft absence |
| `BiologicalProfileResolver` | No frog branch; generic soft-fail for unknown keys | **LIVE** | Preserves `organismKey`, empty optionals — not frog-specific biology |
| `CompiledBiologicalProfile` fields | No tongue/variant/aquatic/adaptation fields | **LIVE** sparse composition | Identity + host/form/effect/behavior/contributingSource only |
| `MobBucketSpecimenSource` | Maps `TADPOLE_BUCKET` → `EntityType.TADPOLE`; **no** frog bucket item | **LIVE**; frog path **DEAD**/N/A | `Frog` does **not** implement `Bucketable`; no frog bucket in vanilla map |
| Java/resources/tests under `biocraft-alien` | `rg -i frog` → **zero hits** | **DEAD** / absent | No STUB, PARSE-ONLY, TEST, or PLANNING frog hooks found |
| Vanilla frog loot JSON | Present, empty pools | Vanilla **LIVE** | Confirms slimeballs are not frog-entity drops |
| Design inventory / dna.md frog mentions | Inventory row + “do not queue Frog” batch notes | **PLANNING** / locked process notes only | Not live gameplay consumers |

---

## Tempting but rejected interpretations

| Temptation | Why rejected |
|------------|--------------|
| `#can_breathe_under_water` / swim AI ⇒ aquatic BP field | Frog is **not** in `#minecraft:aquatic` (tag lists turtle/axolotl/fish/squid/tadpole/… — **no frog**). Swim/land AI is pathfinding ownership. Aquatic tag’s Impaling consumer is irrelevant to frog. **Closed leap:** water AI ≠ aquatic BP. |
| Tongue ⇒ anatomy / feeding trait | Tongue is `ShootTongue` + pose/sync + `doHurtTarget`. No BioCraft anatomy consumer. Phenomenon ≠ representation need. |
| Variants ⇒ biome adaptation / subtype trait | Variant is texture registry + spawn biome tags + magma-cube froglight loot gate. **Do not** chain variant→biome→adaptation→trait without a BioCraft consumer. |
| Slimeball ⇒ frog anatomy / metabolism | Slimeball is **slime loot** (and breed **item** tag). Frog entity loot empty. |
| Axolotl hunt adjacency ⇒ amphibian family | `#axolotl_hunt_targets` includes **tadpole**, not frog. No shared BioCraft clade from hunt tags. **Closed leap.** |
| Host Registry absence ⇒ missing BP fact | Host participation is orthogonal to Biological Profile composition (`dna.md` locked split). Unregistered frog fails soft; does not earn fields. |
| Breeding creates baby frog / frog “is amphibian lifecycle BP” | Love sets pregnancy → frogspawn **block** → **tadpole** entities. Metamorphosis ownership is tadpole/block, investigated separately — not absorbed here. |
| Froglight loot ⇒ BioCraft variant consumer | Consumer is vanilla loot table; still no BioCraft named consumer. |

---

## Potential biological relationships

| Relation | Status for this packet |
|----------|------------------------|
| Frog ↔ tadpole / frogspawn | Vanilla lifecycle chain (breed → frogspawn → tadpole). Document ownership only; **do not** conclude tadpole BP from frog evidence. |
| Frog ↔ slime / magma cube | Prey + loot coupling (`#frog_food`, slimeball, froglights). Gameplay adjacency, not BioCraft family. |
| Frog ↔ axolotl | Shared inventory bio-organic + water-capable tags differ (axolotl aquatic+bucket; frog breathe-under-water only). **Not** a family column. |
| Frog ↔ `#aquatic` organisms | **Non-member**; reject aquatic BP inheritance. |
| Contributing-source / host DNA | No live frog host registration; no frog `contributingSourceKey` special case. |

---

## Tag probe (membership → 1.21.1 consumer → behavior → biological meaning? → BioCraft consumer?)

| Tag | Frog member? | Named 1.21.1 consumer | Behavior | Biological meaning for BP? | BioCraft consumer? |
|-----|--------------|----------------------|----------|----------------------------|--------------------|
| `#entity_type/can_breathe_under_water` | **Yes** | `LivingEntity.canBreatheUnderwater()` | Skip drown damage path | Drowning exemption only | None |
| `#entity_type/aquatic` | **No** | Impaling sensitivity via tag add | N/A for frog | Would be false aquatic leap | None |
| `#entity_type/frog_food` | N/A (prey list) | `Frog.canEat` / `FrogAttackablesSensor` | Tongue hunt targets | Prey filter | None |
| `#item/frog_food` | N/A | `Frog.isFood`, temptations | Breed/tempt with slimeball | Item food gate | None |
| `#block/frogs_spawnable_on` | N/A | `Frog.checkFrogSpawnRules` | Natural spawn floor | Spawn rule | None |
| `#block/frog_prefer_jump_to` | N/A | Long-jump / node evaluator | Prefer lily pad / dripleaf | Path preference | None |
| `#worldgen/biome/spawns_*_variant_frogs` | N/A | `Frog.finalizeSpawn` | Assign warm/cold variant | Spawn cosmetic | None |
| `#fall_damage_immune` | **No** | (other entities) | Frog uses −5 fall override instead | Not tag-based immunity | None |

---

## Final evidence conclusion

| Question | Answer |
|----------|--------|
| **New BP field earned?** | **NO** |
| **Existing composition sufficient?** | **Yes** for any future soft identity resolve (`organismKey` only); frog contributes **no** additional compiled fields today. Nothing observed requires extending `CompiledBiologicalProfile`. |
| **Named live BioCraft consumer?** | **None** for frog tongue, variant, slimeball, aquatic/amphibious semantics, or breeding chain. Module has **zero** frog string references. |
| **Architectural escalation?** | **None.** Do not mint `DESIGN-BIO-MANIFEST-004`. Host Registry absence is not escalation. Do not invent aquatic/anatomy/adaptation fields from vanilla AI/loot. |

### A/B/C outcome summary
- All probed frog behaviors: **A**.
- **B:** not applied (no named live frog consumer exercising existing composition beyond generic soft-fail).
- **C:** **not earned**.

### Probe checklist coverage
1. Identity/hierarchy/dimensions/category — done.  
2. Variant owner/persistence/consumers — done; no BioCraft consumer; froglight loot remains vanilla.  
3. Tongue targeting/extension/transport/effect — done; no anatomy trait.  
4. Slimeball loot, `#frog_food`, land/water, breeding→tadpole ownership — done.  
5. Tags — done.  
6. AlienCraft config audit — done (hosts absent; resolver generic; bucket tadpole-only; no frog refs).
