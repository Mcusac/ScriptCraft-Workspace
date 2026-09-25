```text
TEMPORARY EVIDENCE — NOT PROJECT SSOT
Minecraft Java 1.21.1 mapped-source existence investigation
Do not treat this file as canonical design documentation.
```

# Camel Husk — 1.21.1 existence investigation

**Authority:** Minecraft Java **1.21.1** / NeoForge **21.1.208** mapped sources only.  
**Jar:** `implementations/minecraft/AlienCraft/biocraft-alien/build/moddev/artifacts/neoforge-21.1.208-sources.jar`  
**Resources jar (loot/tags/worldgen/assets):** `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar`  
**Extract cache (not SSOT):** `.tmp_mc_sources/`  
**Scope:** version existence gate. Later-version Camel Husk behavior was **not** investigated.

---

## Subject

Camel Husk

## Version

Minecraft Java 1.21.1

## Target identity

**Not present.** There is no usable Minecraft Java 1.21.1 organism/entity named Camel Husk.

### EntityType registration (1.21.1)

`EntityType.java` in the 1.21.1 mapped sources registers living **Camel** and zombie-variant **Husk** as **separate** types. It does **not** register `CAMEL_HUSK` / `camel_husk`.

Grep of `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` for `CAMEL_HUSK`, `camel_husk`, and `CamelHusk`: **no matches**.

Present 1.21.1 registrations that must not be collapsed into a Camel Husk identity:

```236:238:.tmp_mc_sources/net/minecraft/world/entity/EntityType.java
    public static final EntityType<Camel> CAMEL = register(
        "camel", EntityType.Builder.of(Camel::new, MobCategory.CREATURE).sized(1.7F, 2.375F).eyeHeight(2.275F).clientTrackingRange(10)
    );
```

```423:431:.tmp_mc_sources/net/minecraft/world/entity/EntityType.java
    public static final EntityType<Husk> HUSK = register(
        "husk",
        EntityType.Builder.of(Husk::new, MobCategory.MONSTER)
            .sized(0.6F, 1.95F)
            .eyeHeight(1.74F)
            .passengerAttachments(2.075F)
            .ridingOffset(-0.7F)
            .clientTrackingRange(8)
    );
```

`Items.java` follows the same split: `CAMEL_SPAWN_EGG` (`EntityType.CAMEL`) and `HUSK_SPAWN_EGG` (`EntityType.HUSK`). No `CAMEL_HUSK_SPAWN_EGG` / `camel_husk_spawn_egg`.

### Class, loot, tags, worldgen (same 1.21.1 jars)

`jar tf` of `neoforge-21.1.208-sources.jar` for `CAMEL_HUSK` / `camel_husk` / `CamelHusk`: **no entries** (grep exit 1).

Camel-named source entries in that jar are the living camel only:

- `net/minecraft/world/entity/animal/camel/Camel.java`
- `net/minecraft/world/entity/animal/camel/CamelAi.java`
- `net/minecraft/client/model/CamelModel.java`
- `net/minecraft/client/renderer/entity/CamelRenderer.java`
- `net/minecraft/client/animation/definitions/CamelAnimation.java`

Husk-named source entries in that jar are the zombie variant only:

- `net/minecraft/world/entity/monster/Husk.java`
- `net/minecraft/client/renderer/entity/HuskRenderer.java`

No `CamelHusk` class.

`jar tf` of `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar` for `camel_husk` / `CamelHusk`: **no entries**. Camel resource entries are living-camel only (`loot_table/entities/camel.json`, desert village camel spawn/template pool, `camel_food`, `camel_sand_step_sound_blocks`, camel texture, `camel_spawn_egg` model). Extracted `data/minecraft/loot_table/entities/husk.json` exists; no `camel_husk` loot table.

Grep of `.tmp_mc_sources` (`*.java`, `*.json`, `*.nbt`) for `camel_husk` / `CAMEL_HUSK` / `CamelHusk`: **no matches**. Same for `EntityTypeTags`, `SpawnPlacements.java`, and `net/minecraft/tags`.

**Identity result:** Camel Husk is not a 1.21.1 `EntityType`, class, loot table, tag member, spawn-egg item, or worldgen subject. Living Camel and Husk remaining in 1.21.1 does not create a Camel Husk organism.

## Behavior ownership table

No organism-specific behavior table is applicable. There is no target-version Camel Husk organism whose gameplay could be owned, composed, or manifested.

A/B/C methodology was **not** applied. Existing gameplay / owner / biological-input tests require a 1.21.1 organism. Inventory listing and the compound name are not substitutes.

## Configuration audit

Tracking only. Nothing was modified.

| Surface | Status | Evidence |
|---------|--------|----------|
| `vanilla_organism_inventory.md` §4 current table | **absent** from current-version rows | `camel_husk` is not in §4.1–§4.5 |
| `vanilla_organism_inventory.md` §9.3 | **PLANNING ONLY** — After 1.21.1 | Draft key `camel_husk`, category `undead`, notes `After 1.21.1`. Explicitly “Not current candidates.” |
| `hosts.json` | **absent** | No `camel_husk` key. Undead `mobs` list is `zombie`, `skeleton`, `wither_skeleton`, `stray`, `husk`, `drowned`, `phantom`, `wither`, `zombie_villager`, `skeleton_horse`, `zombie_horse`. Living `camel` is also unregistered; that is unrelated 1.21.1 Camel tracking, not Camel Husk. |

Inventory §9.3 is reusable future-version accounting. It is **not** LIVE 1.21.1 organism evidence, Host Registry membership, manifestation authorization, or a Biological Profile subject.

Do not promote planning to SSOT. Do not create a BP field, Host Registry entry, or inventory-status change from later-version knowledge.

## Tempting but rejected interpretations

- **Treating the After-1.21.1 inventory listing as 1.21.1 organism evidence.** §9.3 is out-of-range draft context. A catalog/inventory entry does not turn a future-version organism into a 1.21.1 evidence subject.
- **Back-projecting later Camel Husk** (current wiki, later Minecraft APIs, later mapped sources) as if it were 1.21.1. Later-version implementation was not researched.
- **Inferring Husk/Camel hybrid biology from the name** (camel biology, Husk genetics, desert/heat adaptation, undead camel biology, Husk-derived or Camel-derived genetics). Name compounding is not 1.21.1 source evidence.
- **Collapsing 1.21.1 `EntityType.CAMEL` and `EntityType.HUSK` into a Camel Husk.** Those are two registered organisms; neither is Camel Husk.
- **Treating Phantom, Zombie Horse, or other undead investigations as a cluster that includes Camel Husk.** These are not a biological cluster. This packet does not inherit their conclusions.
- **Creating a manifestation report, BP field, or Host Registry row** for an organism that does not exist in the target version.

## Potential biological relationships

No target-version relationship tests are applicable. Camel vs Husk vs Camel Husk comparison, undead-tag membership, spawn/conversion, and BioCraft catalog consumption all require a 1.21.1 Camel Husk organism.

1.21.1 Camel and 1.21.1 Husk remain separate inventory subjects (`camel` in §4.1; `husk` in §4.4). They are not evidence that Camel Husk exists or shares genetics.

## Final evidence conclusion

```
New BP field earned: NO
Existing composition sufficient: N/A  (no target-version organism)
Named consumer exists: NO
Architectural escalation required: NO
```

```
Target-version status: not present / not established
1.21.1 biological manifestation conclusion: No target-version organism evidence available.
No BP representation earned.
No implementation or architecture change.
```

**Hard stop.** Later-version Camel Husk implementation was not investigated.
