```text
TEMPORARY EVIDENCE — NOT PROJECT SSOT
Skeptical synthesis of a docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
```

# Skeptical synthesis — Phantom, Zombie Horse, Camel Husk

**Status:** Temporary reviewer synthesis. **Not** project SSOT. **Not** DESIGN-BIO-MANIFEST-004.  
**Version gate:** Minecraft Java **1.21.1** (`minecraft_version_range=[1.21.1,1.22)`, NeoForge 21.1.208).  
**Grouping:** These three organisms were investigated together for **evidence-management only**. They are **not** a biological cluster, undead-flying category, horse clade, desert/hybrid abstraction, or Phantom→Bat/Ghast generalization.

**Independent re-check:** Agent packets were treated as claims. Load-bearing 1.21.1 classes and tags were re-read or re-extracted from `neoforge-21.1.208-sources.jar` / `neoforge-21.1.208-client-extra-aka-minecraft-resources.jar` into `.tmp_mc_sources/`. AlienCraft `hosts.json`, `HostType`, `BiologicalProfileResolver`, and `HostEligibilityService` were re-read.

---

## Independent verification of tempting claims

| Tempting claim | Independent 1.21.1 / repo finding | Verdict |
|----------------|-----------------------------------|---------|
| Phantom flight is biological flight composition | `Phantom extends FlyingMob`; constructor installs `Phantom.PhantomMoveControl`, **not** `FlyingMoveControl`. Jar-wide `extends FlyingMob`: **Phantom and Ghast only**. Bat is `AmbientCreature`. | **Reject as BP flight.** Vanilla movement/AI. **A** |
| Insomnia spawn is Phantom biological origin | `PhantomSpawner` + `GameRules.RULE_DOINSOMNIA` (`doInsomnia`) + `Stats.TIME_SINCE_REST`; reset on sleep (`ServerPlayer` ~1044) and death (~739). Spawner installed only on Overworld `ServerLevel`. | **Reject origin.** Player/world spawn gate. **A** |
| `#minecraft:undead` is undead-flying biology | `undead.json`: `#skeletons`, `#zombies`, `wither`, `phantom`. Phantom is listed **beside** `#zombies`, not inside it. Named consumers are vanilla combat/effect/AI. | **Reject undead-flying.** Taxonomy. **A** / identity **B** |
| Zombie Horse name/tags = Zombie ancestry | `ZombieHorse extends AbstractHorse`. `Zombie.convertToZombieType` requires `EntityType<? extends Zombie>`. Jar-wide: **no** `convertTo`/`convertToZombieType` site involving `ZOMBIE_HORSE`. | **Reject ancestry.** **A/B** |
| Zombie Horse / Skeleton Horse sibling `AbstractHorse` = biological relationship | Shared parent and renderer **class**; different textures. Skeleton Horse has trap; Zombie Horse does not. Thunder path creates **Skeleton Horse only** (`ServerLevel.tickChunk`). `#dismounts_underwater` includes Zombie Horse, **not** Skeleton Horse. Water slowdown 0.96 is Skeleton Horse-only. Tags: `#zombies` vs `#skeletons`. | **Reject clade.** Parallel implementation. **A/B** |
| `camel_husk` inventory listing = 1.21.1 organism | `EntityType` registers `CAMEL` and `HUSK` separately. Jar scan of sources + resources: **zero** `camel_husk` / `CamelHusk` / `CAMEL_HUSK`. | **Not present.** No A/B/C subject |
| `hosts.json` registration = eligibility or manifestation | `"phantom"` and `"zombie_horse"` are in `vanilla_hosts.undead`. `HostType.UNDEAD.isSuitableForXenomorph() == false`. Resolver is generic identity. | **Reject.** Participation ≠ eligibility ≠ manifestation |
| Transfer Skeleton Horse contribution status onto Zombie Horse | Re-read `hosts.json` / `HostType` / resolver independently. Same **pattern** (LIVE registration, lifecycle-blocked contribution machinery), not copied conclusions. | Pattern holds; **not** a clade transfer |
| 1.21.11+ horsemen / sun-burn / mushroom-tame / plains spawn as 1.21.1 | Resources-jar content scan: `zombie_horse` only in lang, loot, `#zombies`, `#dismounts_underwater` (plus spawn-egg model). **No** biome/structure/event JSON. No sun-sensitive override on `ZombieHorse`. Health 15. Untamed `mobInteract` is `PASS`. | **Exclude later-version mechanics** |

Minor packet completeness (does not change results): resources also contain `zombie_horse_spawn_egg` item model. That is presentation, not worldgen.

**C is not earned for any organism in this group.**

---

## Consolidated matrix

| Organism | Interesting behavior | Actual owner | Biological input | Existing composition sufficient? | Named consumer | Result |
|----------|----------------------|--------------|------------------|-----------------------------------|----------------|--------|
| Phantom | Aerial travel / swoop | `FlyingMob.travel` + `Phantom.PhantomMoveControl` + inner goals | No | `organismKey=phantom` already distinguishes it from Bat/Ghast/Bee | None needing a flight field. `vanilla_compatibility.md` flight row is **PLANNING**, Bat-centric | **A/B** |
| Phantom | Insomnia / time-since-rest spawn | `PhantomSpawner` + `doInsomnia` + player `TIME_SINCE_REST` | No. Spawn ≠ origin | Not an organism-origin fact | None | **A** |
| Phantom | `#minecraft:undead` + sunlight burn | Tag composition; `Phantom.aiStep` + `Mob.isSunBurnTick` (not tag-driven) | Tag/gameplay, not tissue | HostType `UNDEAD` is routing only | Vanilla Smite/effects/Wither; BioCraft suitability false | **A** / identity **B** |
| Phantom | Membrane loot / Slow Falling / Elytra repair | Loot table + brewing / anvil | No | Not anatomy | None in BioCraft | **A** |
| Phantom | Host Registry row | `hosts.json` undead list | Identity / routing | `organismKey` + `HostType.UNDEAD` | Resolver / Analyzer identity; eligibility blocked | **B** |
| Zombie Horse | Name / `#minecraft:zombies` / rotten flesh | Tag grouping (Java reader of `EntityTypeTags.ZOMBIES` = **tag provider only**) + loot | No ancestry | Distinct `organismKey` vs `zombie` | None | **A/B** |
| Zombie Horse | Sibling of Skeleton Horse | Shared `AbstractHorse` + `UndeadHorseRenderer` map | No. Shared parent ≠ clade | Distinct keys | None | **A/B** |
| Zombie Horse | Horse mechanics / gated tame / no trap | `AbstractHorse` + Zombie Horse `PASS` interact; thunder is Skeleton Horse-only | No | Identity sufficient | None | **A** |
| Zombie Horse | Host Registry row | `hosts.json` undead list | Identity / routing | `organismKey` + `HostType.UNDEAD` | Resolver identity; contribution machinery LIVE but lifecycle-blocked | **B** |
| Camel Husk | Compound name / §9.3 inventory row | **No 1.21.1 EntityType** | N/A | N/A | None | **No target-version organism evidence** |

---

## Shared findings (genuine shared evidence only)

These are **not** a clade:

1. **Same evidence-management batch** — administrative, not biological.
2. **Both Phantom and Zombie Horse are registered `hosts.json` undead keys** with `HostType.UNDEAD` and current xenomorph suitability **false**. That is **routing**, already represented. It does not make them related to each other or to Camel Husk.
3. **Both reach `#minecraft:undead`**, but by **different** composition: Phantom is a **direct** undead member; Zombie Horse is via `#zombies`. Direct vs via-zombies is a difference that **disproves** a uniform undead-flying or undead-horse abstraction.
4. **No live BioCraft consumer** in this group needs a missing biological fact. Generic `BiologicalProfileResolver` already projects `organismKey` + optional HostType / host-effect pack id.

---

## Important differences that disprove overly broad abstractions

| Abstraction that would collapse them | Disproof |
|---------------------------------------|----------|
| Undead-flying | Phantom flies via `FlyingMob` + custom move control. Zombie Horse is a ground `AbstractHorse` `CREATURE`. Wither is also `#undead` but uses `FlyingMoveControl`, which Phantom does **not**. |
| Horse clade / undead-horse | Skeleton Horse has trap + water slowdown 0.96 + `#skeletons`. Zombie Horse has no trap, default water slowdown, `#zombies`, `#dismounts_underwater`. |
| Zombie family from `#minecraft:zombies` | Tag has **no** 1.21.1 Java gameplay reader except composing `#undead`. Zombie Horse does not extend `Zombie`. Ordinary Zombie conversion bound cannot accept `ZOMBIE_HORSE`. |
| Desert / Husk / camel hybrid | Camel Husk **does not exist** in 1.21.1. Living `CAMEL` and `HUSK` remain separate types. |
| Phantom → Bat / Ghast flight trait | Shared aerial **outcome** ≠ shared cause. Bat is not `FlyingMob`. Ghast shares the Java parent only. Compatibility sketch naming Bat is not a Phantom consumer. |

---

## Answers to the 12 synthesis questions

1. **Does Phantom require any biological representation beyond existing identity/composition?**  
   **No.** Flight, spawn, tags, loot, size, and sun-burn are vanilla-owned. `organismKey=phantom` plus existing Host Registry routing already distinguish it.

2. **Does Zombie Horse have any biologically meaningful relationship to Zombie?**  
   **No.** Name, `#minecraft:zombies`, rotten-flesh loot, and shared `#undead` consumers are taxonomy/presentation. No class, conversion, or spawn coupling.

3. **Does Zombie Horse have any biologically meaningful relationship to Skeleton Horse?**  
   **No.** Sibling `AbstractHorse` implementation and a shared renderer class are not ancestry. Trap, water, tags, loot, and tame owner diverge. Locked [skeleton_horse.md](../../implementations/minecraft/AlienCraft/docs/design/biological/manifestations/skeleton_horse.md) is consistent with this; no factual error found that would require rewriting it.

4. **Does Camel Husk actually exist in Minecraft Java 1.21.1?**  
   **No.** No `EntityType`, class, loot table, tag member, spawn egg, or worldgen subject.

5. **If it exists, is Camel/Husk relationship biological composition or merely implementation/conversion/taxonomy?**  
   **N/A.** It does not exist in the target version. Do not back-project later-version Camel Husk. Do not collapse 1.21.1 Camel + Husk into a hybrid.

6. **Does any organism require a biological input not already represented?**  
   **No** for Phantom and Zombie Horse. Camel Husk has no organism to represent.

7. **Does any finding justify a new Biological Profile field?**  
   **No.** No named live consumer needs a missing fact.

8. **Does any finding justify an undead, flying, horse, desert, camel, or hybrid abstraction?**  
   **No.** Differences above disprove those collapses.

9. **Does any finding justify a Host Registry change?**  
   **No.** Phantom and Zombie Horse are already registered. Camel Husk is correctly absent. Registration remains ≠ eligibility. Do not edit `hosts.json`.

10. **Does any finding justify a new manifestation consumer?**  
    **No.** Identity consumers already work. Planning matrices are not consumers.

11. **What interpretations must remain explicitly rejected?**  
    See rejected list below.

12. **What is the next evidence dependency after this group?**  
    **Zombie Villager** (this group’s earned leftover).  
    Why (evidence, not inventory checklist): ordinary Zombie’s 1.21.1 `killedEntity` path constructs `EntityType.ZOMBIE_VILLAGER` (`Zombie.java`), and `ZombieVillager extends Zombie`. That is a **named conversion + subclass relationship** that this group’s Zombie Horse pass just showed is **absent** for Zombie Horse. The locked Zombie report deferred a full Zombie Villager investigation as “relationship test only.” Phantom flight does **not** authorize Bat/Ghast. Camel Husk creates **no** follow-up. Zoglin / Zombified Piglin remain later undead nodes (different conversion pairs: Hoglin / Piglin) and are **not** earned by this batch.

If a later parallel pass has already written Zombie Villager / Zombified Piglin / Zoglin reports, this group’s next is **satisfied**; remaining live next is whatever that later pass recorded (typically **undead reassessment**). This packet does not reopen those reports.

Zombie / Husk / Drowned reports already exist and stay closed. This group does not reopen them.

---

## Rejected abstractions

- Biological Profile flight / nocturnal / insomnia-adaptation / membrane-anatomy fields
- Undead-flying category; Phantom→Bat/Ghast/Wither flight clade
- Player insomnia as Phantom origin; Overworld spawner as organism-native origin
- `#minecraft:undead` or `HostType.UNDEAD` as undead tissue composition
- Zombie ancestry of Zombie Horse (name, tags, loot, HostType)
- Skeleton Horse ancestry / undead-horse clade from sibling `AbstractHorse` or `UndeadHorseRenderer`
- Transferring Skeleton Horse contribution conclusions without independent check (checked; still B, not a clade)
- 1.21.11+ horsemen, sun-burn, mushroom tame, horse armor, plains spawn as 1.21.1 evidence
- `camel_husk` inventory / later-version wiki as 1.21.1 organism evidence
- Collapsing 1.21.1 Camel + Husk into Camel Husk
- Host Registry membership as eligibility or manifestation
- Investigating these three together as a biological cluster
- Minting `DESIGN-BIO-MANIFEST-004`, Feature IDs, BACKLOG IDs, or sprint-scope change

---

## Biological Profile result

| Organism | A | B | C |
|----------|---|---|---|
| Phantom | Vanilla owns flight, spawn, tags, loot, size, sun-burn, model | `organismKey=phantom` + existing UNDEAD routing | **Not earned** |
| Zombie Horse | Vanilla owns horse mechanics, absence of trap/conversion/natural spawn, tags, loot | `organismKey=zombie_horse` + existing UNDEAD routing; contributing-source machinery LIVE but lifecycle-blocked | **Not earned** |
| Camel Husk | No 1.21.1 organism | N/A | **Not earned** — no subject |

```
New BP field earned: NO
Existing composition sufficient: YES (Phantom, Zombie Horse); N/A (Camel Husk)
Named missing-fact consumer exists: NO
Architectural escalation required: NO
Implementation: NOT AUTHORIZED
```

---

## Next evidence dependency

**Zombie Villager** — leftover conversion/subclass relationship from the already-complete Zombie investigation, now contrast-tested by Zombie Horse (name/tags ≠ ancestry). Do not jump to Bat, Ghast, Creeper, End/boss/flying comparisons, or post-1.21.1 `parched` / `camel_husk` / `zombie_nautilus` / `happy_ghast`.

If a later parallel pass has already written Zombie Villager / Zombified Piglin / Zoglin reports, this group’s next is **satisfied**; remaining live next is whatever that later pass recorded (typically **undead reassessment**).

---

## Phase B authorization

Evidence is complete. Canonical reports for Phantom and Zombie Horse are earned as **docs-only A/B closeouts**. Camel Husk: inventory version-boundary note only. No Java, `hosts.json`, eligibility, Model A, classification runtime, Feature ID, BACKLOG ID, or sprint-scope change.
