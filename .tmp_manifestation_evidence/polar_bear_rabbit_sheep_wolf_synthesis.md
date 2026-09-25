TEMPORARY EVIDENCE — NOT PROJECT SSOT
Skeptical synthesis — Polar Bear / Rabbit / Sheep / Wolf
Do not treat this file as canonical design documentation.
Do not mint DESIGN-BIO-MANIFEST-004.

# Skeptical synthesis — Polar Bear / Rabbit / Sheep / Wolf

**Primary objective:** find why a new BP representation is **not** earned. Prefer disprove **C**. Majority agreement among packets is **not** evidence.

**Version:** Minecraft Java **1.21.1** / NeoForge **21.1.208**.

**Packets (independently re-checked, not absorbed as authority):** [polar_bear.md](./polar_bear.md) · [rabbit.md](./rabbit.md) · [sheep.md](./sheep.md) · [wolf.md](./wolf.md)

This quartet is an **evidence-management** batch, **not** a livestock / canine / cold-biome / predator–prey clade.

Formal C gate (re-applied): C is earned **only** when an existing production BioCraft consumer’s behavior currently depends on an organism-specific biological fact that existing composition (`organismKey` / `contributingSourceKey` / sparse compiled fields) cannot express without loss. Vanilla mechanic, persistent/heritable state, item production, tag membership, Host Registry row, PARSE-ONLY JSON, or planned catalog **never** earns C.

Identity-route `contributingSourceKey` is **B for that consumer only** — not a blanket for wool, coat, Killer Bunny, tame, `WolfVariant`, or freeze tags.

---

## Independent spot-checks (load-bearing)

### Polar Bear freeze / powder snow / swim / breed / contribution

Re-opened `EntityType.java` **563–564**: `POLAR_BEAR` builder `.immuneTo(Blocks.POWDER_SNOW)` — `isBlockDangerous` returns false when the block is in `immuneTo` (**1117–1119**). That is **block-danger**, not walk-on-powder-snow.

Re-opened `data/minecraft/tags/entity_type/freeze_immune_entity_types.json`: includes `minecraft:polar_bear`. `Entity.canFreeze()` (**3584–3585**) is `!type.is(FREEZE_IMMUNE_ENTITY_TYPES)`. `LivingEntity.canFreeze` (**3686–3695**) additionally requires freeze-immune wearables; Polar Bear still fails the type-tag gate first.

Re-opened `powder_snow_walkable_mobs.json`: rabbit / endermite / silverfish / fox — **no polar_bear**. Freeze immunity ≠ powder-snow walk.

Re-opened `PolarBear.java`: `getWaterSlowDown()` **0.98F** (**240–242**) vs `LivingEntity` default **0.8F** (**2206–2208**). `isFood` always **false** (**78–80**). **No** `BreedGoal`. `getBreedOffspring` still `EntityType.POLAR_BEAR.create` (**70–72**). Cub protection is `PolarBearAttackPlayersGoal` adult + baby in inflate 8×4×8 (**253–279**). Spawn biomes / alternate ice floor are encounter placement, not organism NBT.

Live `writeContributingSource` (`GestationManager.java` **164–175**) writes `encodeId` → registry path. Hosts list includes `"polar_bear"`. `polar_bear.json` xenomorph stub exists; `mob_catalog.json` `bootstrap_entries` lists spider/creeper/**wolf**/enderman only — **polar_bear not loaded**. `deep_mob_configs.neutral` listing is PLANNING.

**C?** No. Freeze/`immuneTo` are real EntityType/tag facts with **no** BioCraft reader. Identity contribution is **B**, not freeze biology.

### Rabbit coats / Killer Bunny / Toast / contribution

Re-opened `Rabbit.Variant`: BROWN…SALT ids 0–5 plus `EVIL(99, "evil")` (**615–622**). Same `EntityType.RABBIT`. `setVariant(EVIL)` installs armor 8, +5 attack modifier, melee/target goals, hostile sound (**354–365**). `getRandomRabbitVariant` never returns EVIL. `getBreedOffspring` (**321–337**) 5% biome re-roll else parent variant — **EVIL can inherit**. NBT `"RabbitType"`.

Re-opened `RabbitRenderer.getTextureLocation` (**29–42**): stripped name `"Toast"` → `toast.png` **before** variant switch. Not a `Variant`. `getBreedOffspring` does not copy custom name.

Live contribution: `"rabbit"` in `hosts.json`; no `variant_mappings` rabbit; no rabbit xenomorph JSON. Encode-id path does **not** read `RabbitType`.

**C?** No. Killer Bunny is persistent same-type state with combat consequence; no named consumer needs EVIL vs brown.

### Sheep wool / shear / jeb_ / wololo / contribution

Re-opened `Sheep.java` `DATA_WOOL_ID`: color nibble + sheared bit; NBT `"Color"` / `"Sheared"`. Dye uses same `setColor`. Shear drops `ITEM_BY_DYE.get(this.getColor())` without clearing color. `ate()` `setSheared(false)`. Offspring `getOffspringColor` via dye **crafting recipes** or random parent.

Re-opened `SheepFurLayer.java` **56–65**: `jeb_` name → rainbow lerp; **does not** `setColor`. Workspace search of `.tmp_mc_sources` `jeb_` hits this layer only — **no** item-drop `jeb_` path in mapped 1.21.1 sources (wiki claims not imported).

Re-opened `EvokerWololoSpellGoal`: selector `getColor() == BLUE` (**302–304**); `setColor(RED)` (**340–344**). Evoker-owned.

Live: `"sheep"` in hosts; `BiologicalProfileResolverTest.sheepResolvesLivingBiologicalHostReferences` is **TEST identity**. Admission tests use `"minecraft:sheep"` string + fake extents 0.9×0.9 (not EntityType 0.9×1.3). **No** production Java reads DyeColor / wool.

**C?** No. Color is persistent/heritable/loot-relevant and **unconsumed**. Identity B does **not** represent Color.

### Wolf variant / tame / PARSE-ONLY catalog / contribution

Re-opened `WolfVariants`: nine keys pale/spotted/snowy/black/ashen/rusty/woods/chestnut/striped. Spawn = first biome match else PALE. Breed = random parent holder (**598–605**), not biome re-roll. `getTexture()` wild/tame/angry paths of **same** variant (**143–150**). Goals do **not** branch on variant.

Re-opened `canMate` (**629–641**): both tame Wolves, partner not sitting. Offspring copies variant always; owner/tame/collar only if calling parent tame.

`hosts.json` `variant_mappings.wolf` = `"neutral"` — folder label, **not** `WolfVariant`. `wolf.json` is in `bootstrap_entries` (parsed at init). `getSpecializedVariant` / `getSpecialAbilities` / `getVariantProperties`: **no callers** outside `SpecializedXenomorphManager` (PARSE-ONLY). `pack_behavior` is not a read of vanilla pack hunt (`HurtByTargetGoal.setAlertOthers` is hurt-alert; `WolfPackData` shares spawn variant only).

Live contribution: `"wolf"` encode-id path. Identity B does **not** cover pale vs snowy or tame.

**C?** No.

---

## Consolidated matrix

| Organism | Interesting behavior | Manifestation class | Owner | Biological input? | Existing composition | Named live consumer | A/B/C |
|----------|----------------------|---------------------|-------|-------------------|----------------------|---------------------|-------|
| Polar Bear | Identity / host path | identity / BioCraft-consumed key | `EntityType.POLAR_BEAR` + hosts + `writeContributingSource` | Identity only | `organismKey` / `contributingSourceKey=polar_bear` + `baseline_biological` | LIVE generic | **B** |
| Polar Bear | `#freeze_immune_entity_types` | environmental interaction (type tag) | `Entity.canFreeze` | Type flag, not instance NBT | Identity does **not** encode freeze | **None** | **A** |
| Polar Bear | `immuneTo(POWDER_SNOW)` | environmental interaction | `EntityType.isBlockDangerous` | Danger set ≠ walk | Not needed | **None** | **A** |
| Polar Bear | Powder-snow walk | environmental interaction | `#powder_snow_walkable_mobs` — **absent** | Negative control vs Rabbit | Not needed | **None** | **A** |
| Polar Bear | Water slowdown 0.98 | transient movement | `PolarBear.getWaterSlowDown` | Numeric travel | Not needed | **None** | **A** |
| Polar Bear | Cub protect / anger / fox hunt | transient AI + NeutralMob NBT | Inner PolarBear goals | Combat AI | Not needed | **None** | **A** |
| Polar Bear | Food breed / BreedGoal | **absence** | `isFood` false; no BreedGoal | Recorded absence | Identity sufficient | **None** | **A** |
| Polar Bear | Spawn snow/ice | environmental encounter | biome JSON + `checkPolarBearSpawnRules` | Spawn ≠ origin | Not needed | **None** | **A** |
| Polar Bear | `polar_bear.json` stub | STUB / DEAD file | on-disk; not `bootstrap_entries` | N/A | N/A | **Not loaded** | **A** |
| Rabbit | Identity / host path | identity | hosts + gestation | Identity only | `contributingSourceKey=rabbit` | LIVE generic | **B** |
| Rabbit | Coat variants 0–5 | persistent entity state | `Rabbit.Variant` + `"RabbitType"` | Presentation + heritage | Identity ≠ coat | **None** | **A** |
| Rabbit | Killer Bunny EVIL 99 | persistent state → combat install | `setVariant(EVIL)` same EntityType | Gameplay from variant | Identity still `rabbit` | **None** reading EVIL | **A** |
| Rabbit | Toast | rendering / easter egg | `RabbitRenderer` name `"Toast"` | Name ≠ genetics | Not needed | **None** | **A** |
| Rabbit | Hop / garden raid | transient AI / env interact | Rabbit controls + `RaidGardenGoal` | Movement / grief | Not needed | **None** | **A** |
| Rabbit | Powder-snow walk | environmental interaction | tag + `ClimbOnTopOfPowderSnowGoal` | Path rule | Not needed | **None** | **A** |
| Sheep | Identity / host path | identity | hosts + gestation + resolver TEST | Identity only | `contributingSourceKey=sheep` | LIVE generic; TEST host refs | **B** |
| Sheep | Wool Color | persistent entity state | `DATA_WOOL_ID` + NBT `"Color"` | Heritable vanilla Color; **not** BioCraft-consumed | `organismKey` does **not** encode Color | **None** | **A** |
| Sheep | Dye / shear / regrowth / color loot | item interact + item production + state | DyeItem / Sheep.shear / ate / loot switch | Production ≠ composition | Not needed | **None** | **A** |
| Sheep | `jeb_` | name-gated client render | `SheepFurLayer` | Does not mutate Color | Not needed | **None** | **A** |
| Sheep | Evoker wololo | entity/state transformation | Evoker spell | Other-entity owner | Not needed | **None** | **A** |
| Wolf | Identity / host path | identity | hosts + gestation | Identity only | `contributingSourceKey=wolf` | LIVE generic | **B** |
| Wolf | Nine `WolfVariant` | persistent entity state + render | registry + NBT `"variant"` | Biome spawn / parent inherit / textures; **no AI branch** | Identity ≠ variant | **None** | **A** |
| Wolf | Tame / owner / sit / follow / collar | player relationship + persistent flags | `TamableAnimal` + Wolf interact | Relationship, not anatomy | Identity does **not** encode tame | **None** | **A** |
| Wolf | Anger / hunt / armor | persistent anger + AI + equipment | NeutralMob + goals + `WOLF_ARMOR` | Combat / gear | Not needed | **None** | **A** |
| Wolf | `variant_mappings.wolf=neutral` | PARSE-ONLY config | `MobHostRegistry.getVariant` unused | Folder label ≠ coat | Identity already | **No gameplay caller** | **A** |
| Wolf | `wolf.json` catalog | PARSE-ONLY (loaded, unused) | `MobEntityConfigLoader` + unused getters | Identity-keyed tuning | Would still not need pale/tame | **No apply caller** | **A** |

**No row is C.**

---

## Shared findings (survive skepticism)

1. All four are registered `LIVING_BIOLOGICAL` with live generic identity routing (`encodeId` → `contributingSourceKey`). That is **B for identity consumers only**.
2. Persistent / heritable / visual vanilla state (wool Color, rabbit coats, EVIL, `WolfVariant`) exists in 1.21.1 and is **still A** because no named live BioCraft unit reads the distinction.
3. Item production (wool blocks, rabbit loot, polar-bear fish) has vanilla owners and is not stored composition.
4. Host Registry membership and on-disk xenomorph JSON do **not** prove every manifestation is represented. Polar Bear stub is **DEAD** (not bootstrapped). Wolf JSON is **PARSE-ONLY**.
5. Freeze tag, powder-snow `immuneTo`, and powder-snow **walkable** are three different owners. Polar Bear has the first two, not the third. Rabbit has walkable, not freeze-immune. Co-membership of tags ≠ clade.

## Important differences (block over-broad abstractions)

| Seam | Polar Bear | Rabbit | Sheep | Wolf |
|------|------------|--------|-------|------|
| Reproduction | `isFood` false; **no** BreedGoal | `#rabbit_food` + BreedGoal; EVIL can inherit | Wheat + BreedGoal; Color mix via **dye recipes** | `#wolf_food`; **both must be tame** |
| Persistent “phenotype-like” state | **None** (anger/age only; no coat/cold NBT) | `RabbitType` incl. EVIL | Packed Color + Sheared | `WolfVariant` holder + tame/collar/anger |
| Combat-looking exception | Cub-protect AI (same type) | Killer Bunny same EntityType | None (Evoker mutates Color) | Untamed hunt + always-on skeleton target |
| Easter egg | None found | Toast **name → texture** | `jeb_` **name → fur lerp** (Color unchanged) | None equivalent |
| Powder snow | `immuneTo` + freeze-immune; **not** walkable | **Walkable**; not freeze-immune | Neither (default) | Path malus DANGER_POWDER_SNOW |
| BioCraft extra JSON | Stub **not** bootstrapped | Absent | Absent | Bootstrapped **PARSE-ONLY** |
| `variant_mappings` | Absent | Absent | Absent | `"neutral"` PARSE-ONLY |

## Explicit rejected abstractions

- **Livestock column** from `Animal` / wheat / wool / farm adjacency.
- **Canine clade** from `TamableAnimal`, `AnimalArmorItem.BodyType.CANINE`, or wolf hunt of sheep/rabbit.
- **Cold-biome origin / cold-adaptation Profile** from snowy spawn, freeze tag, or ice `isValidSpawn`.
- **Wool-as-BP-by-assumption** — Color is real persistent/heritable state; C still fails without a named consumer.
- **Tame-as-BP-by-assumption** — tame/owner/sit/collar checked, not dismissed a priori; no BioCraft reader.
- **Variant-as-composition-by-persistence** — coats, EVIL, nine wolf keys, Fox-style heritage ≠ BP field without a consumer.
- **Item-production-as-composition** — shear wool, loot fish/hide/mutton ≠ stored biology.
- **Identity-route blanket-B** — `contributingSourceKey=sheep|wolf|rabbit|polar_bear` does not represent Color / variant / tame / freeze.
- **Host Registry as manifestation completeness.**
- **Predator–prey clade** from Wolf→sheep/rabbit or PolarBear→Fox.
- **Mooshroom reopen** from shared `IShearable`.
- **PARSE-ONLY `pack_behavior` / `enhanced_senses` as pack biology.**

## New representation

**None earned.** No architectural escalation. Do not mint `DESIGN-BIO-MANIFEST-004`. Do not edit Java / `hosts.json` / BP ports / BACKLOG.

## A/B/C summary

| Organism | Packet claim | Independent result |
|----------|--------------|--------------------|
| Polar Bear | A30 / B3 / C0 | **A** dominates vanilla owners; **B** identity/contribution/eligibility; **C = 0** |
| Rabbit | A25 / B3 / C0 | Same pattern; Killer Bunny **A** (mechanic) + identity **B** |
| Sheep | A21 / B2 / C0 | Color **A** (unconsumed); identity **B**; **C = 0** |
| Wolf | A31 / B2 / C0 | Variant/tame **A**; catalog PARSE-ONLY **A**; identity **B**; **C = 0** |

Row counts in packets are investigator bookkeeping; the **gate** is C = 0 on every independently re-opened load-bearing row.

## Recommended next branch (evidence dependency)

Do **not** auto-queue Panda / Parrot / Sniffer / Ghast / Witch merely because they sit near this batch in the inventory table. Panda/Parrot/Ghast/Witch are **already investigated**.

Do **not** queue: Fox reopen from wolf hunt; Mooshroom from shear; Stray/Snow Golem/Wither from freeze-tag co-membership; Cat from `TamableAnimal`; Wandering Trader from trader_llama (still forbidden by that batch).

This pass’s unused-but-real **entity-state item production** (Sheep Color → wool items) is **A**. Remaining current-version bio-organic manifestation-pending rows after this accounting are **Sniffer** (unregistered) and **Wandering Trader** (unregistered).

**Next evidence-dependency candidate:** independent **Sniffer** — not table adjacency. Sniffer’s distinctive 1.21.1 owner is **world-search → item production** (seed drops from sniffing), a different production owner than Sheep’s **entity Color nibble → wool items**. That is the remaining contrast that can still fail (or, only if a named live consumer appears, earn) C on item-production vs composition. Wandering Trader stays deferred (trader_llama lifecycle adjacency is not a reason).

## UNKNOWN carried forward

- Polar Bear: forced-breeding via commands/other mods was not play-tested; source shows factory exists and food/BreedGoal do not.
- Wiki Killer Bunny summon syntax / `jeb_` drop myths: **not** used; mapped source wins.
- Whether a **future** xenomorph apply-path will read PARSE-ONLY `wolf.json` (today: no caller; still not a BP field).

## Path

`.tmp_manifestation_evidence/polar_bear_rabbit_sheep_wolf_synthesis.md`
