TEMPORARY EVIDENCE — NOT PROJECT SSOT

# Ocelot — temporary manifestation evidence packet

**Isolation:** Authoritative Minecraft Java 1.21.1 / NeoForge 21.1.208 mapped sources, live BioCraft, locked docs, and this packet’s own reads only. Fox / Goat / Mooshroom packets were **not** read. Cat adjacency = **negative control only** (shared `OcelotAttackGoal` ≠ ancestry); Cat conclusions are not Ocelot evidence.

**Version:** Minecraft Java **1.21.1** (NeoForge **21.1.208**). Wiki = orientation only; **source wins**.

**Temp cache:** `.tmp_mc_sources/` (NON-SSOT).

---

## Identity

| Fact | Evidence |
|------|----------|
| Hierarchy | `Ocelot extends Animal` — **not** `TamableAnimal` |
| Registration | `EntityType.OCELOT` — `"ocelot"`, `CREATURE`, `sized(0.6F, 0.7F)`, passengerAttachments **0.6375F**, tracking **10** (`EntityType.java` **510–511**) |
| Attributes | health **10**, movement **0.3F**, attack **3.0** |
| Host Registry | `"ocelot"` **ABSENT** from `hosts.json` |

### Host Registry rule application
- ABSENT → **do not register** (including “because Cat is registered”)
- Absence ≠ A/B evidence by itself
- Other live consumers hunted: module `rg` ocelot → **zero** hits in biocraft-alien (excl. build)
- Then classify from ownership + consumers

---

## Behavior ownership table

| Behavior | Actual owner | Category | 1.21.1 evidence | Bio input? | Existing composition | Named BioCraft consumer | Result |
|----------|--------------|----------|-----------------|------------|----------------------|-------------------------|--------|
| Identity / dimensions | `EntityType.OCELOT` | identity | Distinct `"ocelot"` vs `"cat"` | Identity if composed | Fail-soft `organismKey` | **None** live host route | **A** (gameplay); soft identity OK without new field |
| Trust flag | `DATA_TRUSTING` + NBT `"Trusting"` | persistent gameplay state | Boolean; **no owner UUID** | Not TamableAnimal domestication | Not social Profile | **None** | **A** |
| Avoid players | `OcelotAvoidEntityGoal` | AI / transient | Added when **not** trusting | AI | Not fear field | None | **A** |
| Tempt / food trust attempt | `mobInteract` + `OcelotTemptGoal` | persistent gameplay state | Food within 9; 1/3 `setTrusting(true)` | Flag flip | Not temperament BP | None | **A** |
| Tempt scare | `OcelotTemptGoal.canScare` | transient | Scare only if not trusting | AI | Not needed | None | **A** |
| Despawn | `removeWhenFarAway` | persistent gameplay / spawn | Despawns if **not** trusting and tickCount > 2400 | Persistence rule | Not needed | None | **A** |
| Hunt chicken / baby turtle | target goals | AI/gameplay | `NearestAttackableTargetGoal` | Hunt AI | Not feline clade | None | **A** |
| `OcelotAttackGoal` | shared goal class with Cat | AI code reuse | Same class used by Cat | Code reuse ≠ ancestry | Distinct EntityType | None | **A** |
| Food / breed | `#ocelot_food` (cod, salmon) | item/block production | `isFood` + tempt | Tag ≠ diet Profile | Not needed | None | **A** |
| Breeding offspring | `getBreedOffspring` | identity | `EntityType.OCELOT.create` — **trust not copied** | Same-type birth | Child remains ocelot | None | **A** |
| Spawn rules | `checkOcelotSpawnRules` / obstruction | environmental interaction | 2/3 pass random; grass/leaves above sea level | Encounter | Not origin | None | **A** |
| Fall damage tag | `#fall_damage_immune` member | environmental / damage | Tag membership | Tag exemption | Not flight field | None | **A** |
| Death loot | `ocelot.json` | item/block production | Empty pools in this extract | Loot | Not anatomy | None | **A** |
| Host contribution | hosts.json | — | **ABSENT** | — | Do not register | No ocelot writer | No alternate consumer → no C |

**No row is C.**

---

## Trust-state probe (dedicated)

| Probe question | Outcome |
|----------------|---------|
| Ownership | `Ocelot` `DATA_TRUSTING` boolean |
| Persistence | NBT `"Trusting"`; synched |
| Player association | **Boolean only** — no owner UUID / no collar / not `TamableAnimal` |
| Assignment | Food interact while tempting & not trusting & dist²&lt;9; `nextInt(3)==0` → true |
| Reset | No in-class reset-to-false path found (stays trusting once set unless NBT) |
| Behavioral consequences | Removes avoid-player goal; tempt no longer scares; stops far-away despawn |
| Breeding / inheritance | Offspring `OCELOT.create` — **does not** set trusting from parents |
| BioCraft | **None** |

**Verdict:** Persistent gameplay state (**A**). Do **not** translate to domestication / temperament / social biology without a named consumer.

---

## Configuration audit

| Finding | Status | Evidence | Interpretation |
|---------|--------|----------|----------------|
| `hosts.json` `"ocelot"` | **ABSENT** | Not in file | Do not register; do not absorb Cat |
| `hosts.json` `"cat"` | **LIVE** (adjacency only) | Separate key | Negative control — not Ocelot evidence |
| ocelot-named Java/tests | **ABSENT** | Zero module hits | No alternate consumer |
| Resolver | **LIVE** fail-soft | Generic | Soft identity without new field |
| Inventory | **PLANNING** | pending | Not consumer |

---

## Rejected temptations

| Temptation | Why rejected |
|------------|--------------|
| Feline / domestication Profile | Not `TamableAnimal`; trust ≠ tame/owner |
| Absorb into Cat / register because Cat registered | Distinct EntityType; Host Registry edit out of scope |
| Trust → social / temperament BP | Boolean AI flag; no BioCraft consumer |
| Shared `OcelotAttackGoal` ⇒ ancestry | Code reuse only |
| Cat report conclusions as Ocelot proof | Negative-control adjacency only |

---

## Potential relationships

| Relation | Status |
|----------|--------|
| Ocelot ↔ Cat | Shared attack goal class; similar food tags — **not** family column |
| Ocelot ↔ chicken/turtle | Prey AI only |
| Host DNA | Unregistered — no contribution route |

---

## Final evidence conclusion

| Question | Answer |
|----------|--------|
| **New BP field earned?** | **NO** |
| **Existing composition sufficient?** | **YES** for soft identity |
| **Named missing-fact consumer?** | **NO** |
| **Register ocelot?** | **NO** |
| **Architectural escalation?** | **NO** |

### A/B/C summary
- Trust, avoid, hunt, food, spawn, shared goal: **A**
- Soft identity representable without new field
- **C:** not earned
