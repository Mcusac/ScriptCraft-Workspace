TEMPORARY EVIDENCE — NOT PROJECT SSOT

# Mooshroom — temporary manifestation evidence packet

**Isolation:** Authoritative Minecraft Java 1.21.1 / NeoForge 21.1.208 mapped sources, live BioCraft, locked docs, and this packet’s own reads only. Fox / Goat / Ocelot packets were **not** read. `Cow.java` read **only** as parent-implementation evidence (`extends` ≠ ancestry).

**Version:** Minecraft Java **1.21.1** (NeoForge **21.1.208**). Wiki = orientation only; **source wins**.

**Highest-scrutiny C candidate** — distinct identity + Cow inheritance + red/brown variant + breeding + lightning + shear→Cow + stew production. Default: prove why **C is not earned**.

**Temp cache:** `.tmp_mc_sources/` (NON-SSOT).

---

## Identity

| Fact | Evidence |
|------|----------|
| Hierarchy | `MushroomCow extends Cow implements Shearable, VariantHolder<MushroomType>` |
| Registration | `EntityType.MOOSHROOM` — `"mooshroom"`, `CREATURE`, `sized(0.9F, 1.4F)`, `eyeHeight(1.3F)` (`EntityType.java` **502–504**) — **same size literals as Cow; distinct registry id/factory** |
| Implementation inheritance | Extends `Cow` = code reuse only; **not** ancestry or Cow BP subtype |
| Host Registry | `"mooshroom"` **ABSENT** from `hosts.json` |

### Host Registry rule application
- ABSENT → **do not register** from this investigation
- Absence is **not** itself evidence for A or B
- Other live BioCraft consumers hunted: module `rg` for mooshroom/mushroom → **zero** hits outside inventory/docs planning
- Classify from ownership + consumer evidence only

---

## Behavior ownership table

| Behavior | Actual owner | Category | 1.21.1 evidence | Bio input? | Existing composition | Named BioCraft consumer | Result |
|----------|--------------|----------|-----------------|------------|----------------------|-------------------------|--------|
| Identity / dimensions | `EntityType.MOOSHROOM` | identity | Distinct `"mooshroom"` | Identity (if ever composed) | Fail-soft `organismKey=mooshroom` would suffice | **None** live route (unregistered) | **A** for gameplay; soft identity representable without new field |
| Extends Cow | Java inheritance | identity / implementation | Class hierarchy | Shared parent ≠ clade | Distinct key | None | **A** |
| Red/brown variant | `DATA_TYPE` + NBT `"Type"` + `MushroomType` | persistent entity state | RED/BROWN; default RED; blockState for shear drops | Persistent presentation + interact gate | Not BP subtype | **None** | **A** |
| Lightning transform | `thunderHit` | entity/state transformation | Swaps RED↔BROWN if bolt UUID new; **EntityType unchanged**; plays convert sound | Variant flip on same entity | Not ancestry / not Cow create | **None** | **A** |
| Breeding offspring type | `getBreedOffspring` + `getOffspringType` | persistent state / breeding determination | Creates `MOOSHROOM`; type = random parent if differ; if same, 1/1024 flip else random parent | Heritable state | Not BP requirement | **None** | **A** |
| Bowl stew | `mobInteract` bowl branch | item/block production | Bowl → `MUSHROOM_STEW` or `SUSPICIOUS_STEW` if `stewEffects` set | Item interact ≠ milk Profile | Not needed | None | **A** |
| Cow milk via super | `super.mobInteract` → `Cow.mobInteract` | item/block production | After bowl/shears/flower branches fail, Cow bucket→`MILK_BUCKET` still reachable | Same outcome ≠ merge into Cow Profile | Distinct EntityType | None | **A** |
| Brown flower stew charge | brown + `#small_flowers` | effect application / persistent stew state | Sets `stewEffects` from flower; NBT `stew_effects` | Transient charged state on entity | Not needed | None | **A** |
| Shear → Cow | `shear` | entity/state transformation | Discard Mooshroom; `EntityType.COW.create`; copy health/rot/name/persistence/invuln; drop 5× variant mushroom block | Conversion **destination** Cow — not ancestry | Distinct keys | **None**; do not register; do not absorb into Cow | **A** |
| Mycelium preference | `getWalkTargetValue` | environmental interaction | Mycelium walk target 10 | Path preference | Not origin | None | **A** |
| Spawn floor | `#mooshrooms_spawnable_on` | environmental interaction | `checkMushroomSpawnRules` | Encounter | Not origin | None | **A** |
| Death loot | `mooshroom.json` | item/block production | leather + beef (cow-like pools) | Loot ≠ anatomy | Not needed | None | **A** |
| Host contribution | hosts.json | — | **ABSENT** | — | Do not register | No mooshroom writer path | Absence ≠ A/B; no other consumer → no C |

**No row is C.**

---

## Lightning transformation probe (dedicated)

| Probe question | Outcome |
|----------------|---------|
| Cause | `LightningBolt` via `thunderHit(ServerLevel, LightningBolt)` |
| Owner | `MushroomCow.thunderHit` |
| EntityType change? | **No** — remains `MOOSHROOM`; does **not** create Cow |
| Variant | Toggle RED ↔ BROWN |
| Dedup | `lastLightningBoltUUID` prevents double-apply same bolt |
| Age / breeding / stew | Not cleared in `thunderHit` body (variant + UUID + sound only) |
| Reversibility Cow↔Mooshroom | Lightning does **not** produce Cow; shear produces Cow (one-way discard+create). Lightning is reversible red↔brown only |
| State transfer to Cow | N/A for lightning |
| BioCraft observes? | **No** |

**Verdict:** Entity/state transformation owned by vanilla (**A**). Not ancestry. Not a new BP field without a consumer.

---

## Breeding offspring-type probe (dedicated)

| Probe question | Outcome |
|----------------|---------|
| Offspring EntityType | Always `EntityType.MOOSHROOM.create` |
| Type derivation | `getOffspringType(partner)`: if parents same type and `nextInt(1024)==0` → opposite; else random this vs partner |
| Environment? | **No** biome in breed path |
| Persistence | Child `setVariant` → synched + later NBT |
| BioCraft | **None** |

**Verdict:** Breeding determination of persistent variant (**A**). Heritability ≠ BP field.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"mooshroom"` | **ABSENT** | Not in file | Do **not** register; absence ≠ A/B verdict alone |
| mooshroom-named Java/tests | **ABSENT** / **DEAD** | Zero module hits | No alternate live consumer |
| Resolver | **LIVE** generic fail-soft | Unknown keys keep `organismKey` | Soft identity possible without registration; still **no C** |
| Cow adjacency docs | **PLANNING** / prior report | Cow negative control | Do not absorb |
| Inventory | **PLANNING** | pending | Not consumer |

---

## Rejected temptations

| Temptation | Why rejected |
|------------|--------------|
| Bovine ancestry / absorb into Cow Profile | Distinct EntityType; extends = implementation only |
| Shear/lightning as inheritance | Shear = discard+create Cow; lightning = same-entity variant flip |
| Variant BP from breeding / stew gameplay | Vanilla owners; no BioCraft consumer |
| Queue Sheep/Pig from livestock feel | Out of scope; adjacency ≠ authorization |
| Register because investigated / because Cow registered | Host Registry edit forbidden; absence stays |
| Invent C from “interesting combination” of mechanics | C requires named live consumer needing missing fact — **none found** |

---

## Potential relationships

| Relation | Status |
|----------|--------|
| Mooshroom ↔ Cow | Shear destination + Java parent — **negative control / conversion**, not ancestry |
| Mooshroom ↔ Goat milk | Parallel milk outcome via Cow.super only — not clade |
| Host DNA | Unregistered — no contribution route |

---

## Highest-scrutiny C challenge (packet-level)

| Candidate missing fact | Why it fails C |
|------------------------|----------------|
| Need mooshroom≠cow in BP | Distinct `organismKey` string already sufficient if composed; no live consumer requires more |
| Need red/brown in BP | Stew/shear/lightning/breed are vanilla; no BioCraft reader |
| Need transformation field | Manifestation/state transition owned by entity methods |
| Need stew/effect field | Item + NBT on entity; no BioCraft consumer |

**Packet verdict: C not earned.**

---

## Final evidence conclusion

| Question | Answer |
|----------|--------|
| **New BP field earned?** | **NO** |
| **Existing composition sufficient?** | **YES** for soft identity (`organismKey`); no extra compiled fields required |
| **Named missing-fact consumer?** | **NO** |
| **Register mooshroom?** | **NO** — out of scope; absence stays |
| **Architectural escalation?** | **NO** |

### A/B/C summary
- All probed mechanics: **A**
- Soft identity representable without new field (not a Host Registry conclusion)
- **C:** not earned (highest-scrutiny challenge failed to find consumer)
