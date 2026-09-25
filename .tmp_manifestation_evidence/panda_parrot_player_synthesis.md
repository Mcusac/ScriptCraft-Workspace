TEMPORARY EVIDENCE — NOT PROJECT SSOT
Skeptical synthesis: panda / parrot / player
Do not treat this file as canonical design documentation.
Do not mint DESIGN-BIO-MANIFEST-004.

**Authority:** Minecraft Java **1.21.1** / NeoForge **21.1.208** mapped sources + live BioCraft production code. Agent packets treated as **claims** and re-checked against sources.

**Primary goal:** disprove **C**. Prefer no new BP field.

**Batch nature:** evidence-management trio, **not** a clade. Player organism vs actor is first-class and is **not** collapsed.

---

## Spot-checks (load-bearing claims)

| Claim | Independent check | Outcome |
|-------|-------------------|---------|
| Panda genes synched + NBT MainGene/HiddenGene | Re-read `Panda.java` **78–79**, **241–252** | **Hold** |
| Recessive expression: both alleles or NORMAL | `Gene.getVariantFromGenes` **765–770**; BROWN/WEAK recessive **734–736** | **Hold** |
| Breeding copies random parent alleles + 1/32 mutation | `setGeneFromParents` **593–616** | **Hold** |
| BioCraft reads panda genes | `rg` biocraft-alien/src: panda only in `hosts.json` | **Hold** (absent consumer) |
| Parrot breeding disabled | `canMate` false, `getBreedOffspring` null, `isFood` false **299–325** | **Hold** |
| Cookie: POISON 900 + MAX_VALUE hurt on parrot | `Parrot.mobInteract` **274–289**; tag = cookie only | **Hold** |
| `CookieItem.java` missing | `jar tf` 1.21.1 sources: no such class | **Hold** — not UNKNOWN for the chain; tag+Parrot owner present |
| Flight owner is move/nav, `isFlying=!onGround` | `Parrot.java` **128**, **449–450**; `FlyingAnimal` marker only | **Hold** |
| Player is not Mob | `Player extends LivingEntity` **116**; EntityType `createNothing` MISC `noSave`/`noSummon` **803–812** | **Hold** |
| `player` ≠ `human` ≠ `villager` | `hosts.json` three distinct list entries; `EntityKind.PLAYER` vs `VILLAGER`; human is `modded_hosts.biocraft_alien` | **Hold** |
| Registration ≠ B | Plan constraint; B earned only via `GestationManager.writeContributingSource` encodeId + occupant `organismKey` | **Hold** |
| Capture ban is gameplay | `CaptureEligibilityPolicy.canCapture(alive && !player)` | **Hold** — not BP |
| `requires_player_specific_effects` LIVE | `HostEffectManager` **63–65** + pose adapter | **Hold** — routing, not missing composition |
| CONSEQUENCE-001 decision UX | Sprint: player decides STASIS/extract/cleanse | **Hold** — actor-side |

No load-bearing claim failed. No **C** survived.

---

## Consolidated A/B/C matrix

| Organism | Distinctive vanilla owner | Host Registry | Live `contributingSourceKey` | A | B | C |
|----------|---------------------------|---------------|------------------------------|---|---|---|
| Panda | Main/hidden genes → personality → AI/attrs/textures; bamboo food/tempt/breed/env | `LIVING_BIOLOGICAL` | Generic encodeId `"panda"` | Vanilla genes/bamboo/AI | Identity key | **Not earned** |
| Parrot | Variant (visual); cookie poison; mimicry sounds; flying nav; tame/shoulder; **no breed** | `LIVING_BIOLOGICAL` | Generic encodeId `"parrot"` | Vanilla variant/cookie/flight/mimicry/tame | Identity key | **Not earned** |
| Player | Non-Mob living entity; hunger/air/health vanilla; respawn replacement; actor UI | `LIVING_BIOLOGICAL` | Generic encodeId `"player"` **if** gestated host (eligible); capture typically blocks occupant sampling | Hunger/air/sleep/inventory/gamemode/respawn/capture/effects pose | Identity key **on that host/sample route only** | **Not earned** |

Existing composition (identity + Model A source key) is sufficient. No new representation is required.

---

## Shared findings (genuine only)

1. All three are `hosts.json` living_biological participants. Registration is setup, not manifestation science.
2. Live contribution, when it fires, is **encodeId → registry path** — identity **B**, not gene/variant/hunger **C**.
3. Jungle spawn co-occurrence of panda and parrot is **encounter**, not origin and not a clade.
4. Persistent visible or heritable vanilla state (panda genes, parrot color) does not earn a BP dimension without a named consumer.

Nothing else is genuinely shared. Player is not a Mob and is not a tame/breed animal.

---

## Important differences

| Dimension | Panda | Parrot | Player |
|-----------|-------|--------|--------|
| Hierarchy | `Animal` | `ShoulderRidingEntity` → `TamableAnimal` | `LivingEntity` only (not Mob) |
| Persistent internal distinction | Main/hidden genes + derived personality (AI + texture + attrs) | Color variant (texture only in class) | Hunger/food/XP/inventory — mixed physiology and gameplay |
| Inheritance | Random parental alleles + 1/32 re-roll | Breeding **absent** | Reproduction **absent** |
| Player relationship | Avoid (worried); breed food from player | Tame/sit/shoulder on player | **Is** the player |
| Flight | No | Flying nav; fall damage suppressed | Creative/spectator `Abilities.mayfly` (controller) |
| BioCraft extra LIVE | Generic host path only | Generic host path only | Capture forbid; gestation ×3; attachment pose if effect-profile flag |

---

## Rejected abstractions

Do **not** add: jungle clade, pet/tame clade, bear family, flight Profile from this trio, humanoid clade, speech-organ field, Genome field from Minecraft `Panda.Gene`, player+villager+human column, sentience.

Do **not** queue: polar_bear (panda adjacency), wolf (parrot tame adjacency), human (player adjacency).

---

## Player organism vs actor (preserved)

| | Organism | Actor |
|--|----------|-------|
| Identity | `PLAYER` entity | Caller of machines/UI |
| Composition | Identity key if host/sampled | Irrelevant from being caller |
| Capture | Target banned | Operator of net |
| Analyzer / containment menus | Only if admitted (currently banned as capture target) | Operator |
| CONSEQUENCE-001 | N/A | Decision UX |

---

## Whether C survives

**No.** Highest-scrutiny candidates:

- **Panda genes** — persistent, heritable, manifested. No BioCraft consumer needs panda-vs-panda composition. **C disproved.**
- **Parrot cookie/mimicry/flight/variant** — owners traced; no BioCraft consumer. **C disproved.**
- **Player hunger/respiration/capture-ban/player-specific effects** — vanilla or gameplay/effect-routing. Identity already gates `isPlayer` / `organismKey=player`. **C disproved.**

If C had survived, the minimum missing fact + named consumer would be documented and this synthesis would **stop** at the architectural boundary. It did not survive.

---

## Recommended next

Independent **Sheep** (inventory pointer). No evidence dependency from this batch. Do not queue polar_bear, wolf, or human.

---

## UNKNOWNs

- Numeric default of `Attributes.MAX_HEALTH` when `Player.createAttributes()` adds the living attribute without an explicit override: Player also names `MAX_HEALTH = 20`. Not load-bearing for A/B/C.
- Full Player combat/recipe/advancement surface: out of the required organism-state pass; not inferred.
