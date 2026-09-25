```text
TEMPORARY EVIDENCE — NOT PROJECT SSOT
Minecraft Java 1.21.1 mapped-source version-gate (absence)
Do not treat this file as canonical design documentation.
Do not mint DESIGN-BIO-MANIFEST-004. Do not write docs/design/biological/manifestations/happy_ghast.md from this packet.
```

# Happy Ghast — 1.21.1 version-gate (absence)

**State:** Version-gate complete. **Not** an implementation plan. **Not** an A/B closeout of a live 1.21.1 organism. **Not** a Biological Profile conclusion.

**Tracking:** None — intentionally untracked docs-only investigation. Do **not** mint `DESIGN-BIO-MANIFEST-004`.

**Version constraint:** Minecraft Java **1.21.1** / NeoForge **21.1.208** mapped source and vanilla data are authoritative. Later Minecraft Happy Ghast behavior is **out of range** and was **not** researched; do not import it as 1.21.1 evidence.

**Pattern mirror:** AlienCraft canonical absence pattern — [`copper_golem.md`](../implementations/minecraft/AlienCraft/docs/design/biological/manifestations/copper_golem.md) (version-gate absence; absence ≠ A).

**Jars:**
- Sources: `implementations/minecraft/AlienCraft/biocraft-alien/build/moddev/artifacts/neoforge-21.1.208-sources.jar` (also Gradle cache `neoforge-21.1.208-sources.jar`)
- Resources: `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar`
- Extract cache (not SSOT): `.tmp_mc_sources/`

**Inventory:** [`vanilla_organism_inventory.md`](../implementations/minecraft/AlienCraft/docs/design/biological/vanilla_organism_inventory.md) **§9.3 only**

**Question:** does Minecraft Java 1.21.1 contain a Happy Ghast organism whose behavior, composition, eligibility, or manifestation can be established? If not, does ordinary `ghast` or any BioCraft key substitute for that organism evidence?

---

## Subject / Version / Inventory context

| Field | Finding |
|-------|---------|
| Subject | Happy Ghast (`happy_ghast`) |
| Version | Minecraft Java **1.21.1** / NeoForge **21.1.208** |
| Inventory | **§9.3 post-1.21.1 draft only.** Draft key `happy_ghast`, draft category `bio-organic`, notes `After 1.21.1`. Explicitly “Not current candidates.” |
| §4 current table | **Absent** — not a current-version candidate |
| Target identity | **Not present.** No `EntityType.HAPPY_GHAST` / `"happy_ghast"` / `HappyGhast` class in 1.21.1 |
| Host Registry | **No** `happy_ghast` key in `hosts.json`. Ordinary `"ghast"` is registered under `unsuitable.elemental` — **do not treat Happy Ghast as that entry** |
| Manifestation | Version-gate complete. **No manifestation investigation is applicable in 1.21.1.** **C not earned** (no organism to escalate). Not A/B of a live organism |
| Adjacency | Ordinary `ghast` exists in 1.21.1 and remains a **separate, pending** inventory subject. Its existence does **not** create Happy Ghast |

Inventory §9.3 is reusable future-version accounting. It is **not** LIVE 1.21.1 organism evidence, Host Registry membership, manifestation authorization, or a Biological Profile subject.

## Scope and non-goals

This packet is a **version-gated absence** record. It confirms that 1.21.1 jars contain no Happy Ghast entity, class, registry id, loot table, spawn egg, or entity-tag member under `happy_ghast` / `HappyGhast` / `HAPPY_GHAST`.

Out of scope: designing later-version Happy Ghast; researching post-1.21.1 Happy Ghast mechanics as biological evidence; inferring Happy Ghast biology/classification/manifestation from ordinary Ghast; editing `hosts.json`, BP schema, BACKLOG, inventory, or Java; minting `DESIGN-BIO-MANIFEST-004`; writing canonical `manifestations/`; drawing A/B/C Biological Profile conclusions from absence alone.

## Method

```text
owner → meaningful biological input? → existing composition?
      → named live BioCraft consumer? → A / B / C
```

A/B/C methodology for organism behaviors requires a 1.21.1 organism. Inventory listing and ordinary Ghast adjacency are not substitutes.

**Absence ≠ A.** “No evidence” is not Biological Profile result A. **C is not earned** because there is no 1.21.1 organism to escalate — this is version absence, not an A/B closeout.

## Entity identity (1.21.1)

**Not present.**

| Check | Result | Evidence |
|-------|--------|----------|
| `EntityType.HAPPY_GHAST` / `"happy_ghast"` / `HappyGhast` | **ABSENT** | Grep of `.tmp_mc_sources/net/minecraft/world/entity/EntityType.java` for `HAPPY_GHAST`, `happy_ghast`, `HappyGhast`: **no matches** |
| Sources jar namelist | **ABSENT** | `jar tf` `neoforge-21.1.208-sources.jar` (build/moddev/artifacts + Gradle cache) for `happy_ghast` / `HappyGhast`: **NONE** (grep exit 1). Re-verified this pass |
| Client-extra / resources jar namelist | **ABSENT** | `jar tf` `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar` for `happy_ghast` / `HappyGhast`: **NONE** (grep exit 1). Re-verified this pass |
| `.tmp_mc_sources` tree | **ABSENT** | Workspace grep for `HAPPY_GHAST` / `happy_ghast` / `HappyGhast` under `.tmp_mc_sources`: **NONE** |

1.21.1 **does** register ordinary Ghast (anti-conflation only — see next section). That does not create a Happy Ghast organism.

## Ordinary Ghast existence note (anti-conflation only)

Ordinary `ghast` is a **registered 1.21.1 identity**. It must **not** be conflated with absent Happy Ghast. This section establishes existence of that separate registry id only. It does **not** infer Happy Ghast biology, classification, HostType, eligibility, composition, or manifestation from Ghast.

```381:390:.tmp_mc_sources/net/minecraft/world/entity/EntityType.java
    public static final EntityType<Ghast> GHAST = register(
        "ghast",
        EntityType.Builder.of(Ghast::new, MobCategory.MONSTER)
            .fireImmune()
            .sized(4.0F, 4.0F)
            .eyeHeight(2.6F)
            .passengerAttachments(4.0625F)
            .ridingOffset(0.5F)
            .clientTrackingRange(10)
    );
```

Sources jar contains ordinary Ghast class/renderer/model only (`Ghast.java`, `GhastRenderer.java`, `GhastModel.java`). Resources jar has ordinary ghast assets (`loot_table/entities/ghast.json`, `ghast_spawn_egg` model, ghast textures, etc.). **None** of those entries are Happy Ghast.

Inventory: ordinary `ghast` is a **§4 current-table** row (pending). Happy Ghast is **§9.3 only**.

Host Registry: `"ghast"` appears under `vanilla_hosts.unsuitable.elemental` in `hosts.json`. **`happy_ghast` must not be treated as that entry.**

## Behavior ownership

No organism-specific behavior table is applicable. There is no target-version Happy Ghast whose gameplay could be owned, composed, or manifested.

| Concern | 1.21.1 owner | Result |
|---------|--------------|--------|
| Entity / class / loot / egg / tags for Happy Ghast | **Absent** | No organism to classify as A/B |
| Later-version Happy Ghast mechanics | **Out of range** | Not researched; not imported |
| Ordinary `ghast` | Separate registered organism | Anti-conflation only; **not** Happy Ghast evidence |
| BioCraft key `happy_ghast` | **Absent** from `hosts.json` | No Host Registry substitute for organism evidence |
| Shared / new Biological Profile seam | Cannot be earned by an absent entity | **C not earned** (version absence; no organism to escalate) |

## AlienCraft configuration audit

Tracking only. Nothing was modified.

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `vanilla_organism_inventory.md` §4 | **absent** from current-version rows | Not in §4 | Not a current candidate |
| `vanilla_organism_inventory.md` §9.3 | **PLANNING ONLY** | Draft key `happy_ghast`, draft category `bio-organic`, `After 1.21.1` | Reusable future accounting |
| `hosts.json` `"happy_ghast"` | **ABSENT** | No key in living/undead/unsuitable lists | Do not invent one; do not edit |
| `hosts.json` `"ghast"` | **LIVE** under `unsuitable.elemental` | `"mobs": ["ghast", "blaze"]` | Ordinary Ghast Host Registry entry only. **Not** Happy Ghast |
| Mob-based / targeting / tests | **ABSENT** for `happy_ghast` | No `happy_ghast` under resources or tests | No C-level contract |

## Skeptical rejected interpretations

- Treating §9.3 inventory listing as 1.21.1 organism evidence.
- Drawing Biological Profile result **A** (or any A/B/C conclusion) from absence alone — **absence ≠ A**.
- Back-projecting later Happy Ghast as 1.21.1 facts (not researched).
- Collapsing ordinary `EntityType.GHAST` / Host Registry `"ghast"` into Happy Ghast.
- Inferring Happy Ghast biology, classification, or manifestation from ordinary Ghast.
- Editing `hosts.json`, inventory, BACKLOG, BP schema, or Java in this pass.
- Minting `DESIGN-BIO-MANIFEST-004` or writing canonical `manifestations/happy_ghast.md`.
- Treating Copper Golem absence as a family column that includes Happy Ghast (pattern only; not shared biology).

## Stop gate and recommendation

**Hard stop — version-gate only.**

| Gate | Result |
|------|--------|
| Version-gate | **Complete** — no Happy Ghast in 1.21.1 mapped sources / jar namelists |
| Manifestation investigation applicable in 1.21.1 | **NO** — no target-version organism |
| A/B conclusion from absence | **NOT DRAWN** — absence ≠ A; no live organism to A/B |
| C / architectural escalation | **NOT EARNED** — no organism to escalate (version absence, not A/B closeout) |
| New BP field / seam from absence | **NO** |
| Implementation / Host Registry / inventory edit | **NO** |

```
Target-version status: not present
Version-gate: complete
1.21.1 manifestation investigation: not applicable
BP A/B/C from absence: not drawn (absence ≠ A; C not earned — no organism to escalate)
No BP representation earned from this gate
No implementation or architecture change
```

**Next evidence dependency:** ordinary `ghast` remains a **pending** current-version inventory subject when that queue reaches it. Do not continue by inventing Happy Ghast biology. Do not jump to post-1.21.1 Happy Ghast.

## Related

- Pattern: [`copper_golem.md`](../implementations/minecraft/AlienCraft/docs/design/biological/manifestations/copper_golem.md) (canonical version-gate absence)
- Inventory §9.3: [`vanilla_organism_inventory.md`](../implementations/minecraft/AlienCraft/docs/design/biological/vanilla_organism_inventory.md)
- Ordinary `ghast`: remains **pending** in inventory §4 — separate subject; do not conflate
- Parallel temporary absence packet style: [`.tmp_manifestation_evidence/camel_husk.md`](./camel_husk.md)
