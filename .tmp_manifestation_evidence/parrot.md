TEMPORARY EVIDENCE — NOT PROJECT SSOT
Agent Parrot docs-only 1.21.1 manifestation investigation
Do not treat this file as canonical design documentation.
Do not promote into manifestations/parrot.md, inventory, BACKLOG, SPRINT, dna.md, system.md, or DESIGN-BIO-MANIFEST-004 until synthesis.

**Isolation:** Minecraft Java **1.21.1** / NeoForge **21.1.208** mapped sources under `.tmp_mc_sources/`, live BioCraft under `biocraft-alien/src`, and this packet’s own reads only. Panda / Player packets were **not** absorbed as evidence. Prior Bat/Allay/Phantom = **precedent only**, not predetermined flight/mimicry conclusions.

Method: owner → biological input? → existing composition? → named live BioCraft consumer? → **A / B / C**.

| Result | Meaning |
|--------|---------|
| **A** | Minecraft owns it; no biological input required |
| **B** | `organismKey` / `contributingSourceKey` already sufficient |
| **C** | Named consumer needs a missing biological fact |

---

## 1. Subject / Version / Target identity

### Subject

Parrot (`minecraft:parrot`) — color variant, tame/sit/shoulder, cookie poison, mimicry sounds, flight movement, Host Registry participation.

### Version

Minecraft Java **1.21.1** / NeoForge **21.1.208**. Sources under `.tmp_mc_sources/` from `neoforge-21.1.208-sources.jar` / client-extra resources. Wiki = orientation only; **source wins**.

### Target identity

| Field | 1.21.1 fact |
|-------|-------------|
| Registry id | `minecraft:parrot` |
| `EntityType` | `EntityType.PARROT` — `EntityType.java` **520–522**: CREATURE, sized **0.5×0.9**, eyeHeight **0.54F**, passengerAttachments **0.4625F**, tracking **8** |
| Class | `Parrot extends ShoulderRidingEntity implements VariantHolder<Parrot.Variant>, FlyingAnimal` (**69**) |
| Hierarchy | `ShoulderRidingEntity extends TamableAnimal` |
| Attributes | MAX_HEALTH **6.0**, FLYING_SPEED **0.4F**, MOVEMENT_SPEED **0.2F**, ATTACK_DAMAGE **3.0** (**162–167**) |
| Baby | `isBaby()` → **false** (**146–148**); `finalizeSpawn` uses `AgeableMobGroupData(false)` |
| Host Registry | **REGISTERED** `vanilla_hosts.living_biological`; HostType `LIVING_BIOLOGICAL`; `default_dna: baseline_biological` |

---

## 2. Source-completeness table

| Source | Status | Role |
|--------|--------|------|
| `Parrot.java` | **PRESENT** | Variant, cookie, tame, mimicry, flight |
| `ShoulderRidingEntity.java` | **PRESENT** | Shoulder sit discard→NBT on player |
| `TamableAnimal.java` | **PRESENT** | Owner/sit base |
| `FlyingAnimal.java` | **PRESENT** | `boolean isFlying()` marker only |
| `LandOnOwnersShoulderGoal.java` | **PRESENT** | Shoulder goal |
| `FlyingMoveControl.java` / `FlyingPathNavigation.java` | **PRESENT** | Flight control/nav |
| `WaterAvoidingRandomFlyingGoal.java` | **PRESENT** | Super of `ParrotWanderGoal` |
| `ParrotRenderer.java` | **PRESENT** | Variant textures only |
| `parrot_food.json` / `parrot_poisonous_food.json` | **PRESENT** | Seeds tame; cookie poison |
| `parrots_spawnable_on.json` | **PRESENT** | Spawn floor |
| `parrot.json` loot | **PRESENT** | Feathers 1–2 + looting |
| `parrot_imitations.json` + `ParrotImitation.java` | **PRESENT** | NeoForge data map overlay |
| `CookieItem.java` | **ABSENT from 1.21.1 sources jar** | Cookie is tag/`Items.COOKIE`, not a dedicated class — poison chain still gated by present `Parrot.java` + tag |
| BioCraft variant/cookie/mimicry/flight consumers | **ABSENT** | Identity only (`hosts.json`) |

---

## 3. Variant probe (mandatory)

Treat color/variant with the same discipline as Fox/Llama/Rabbit-style probes. Persistent visible distinction ≠ BP dimension without a consumer.

| Probe | Outcome | Classification |
|-------|---------|----------------|
| Assignment | Constructor: `Util.getRandom(Variant.values(), …)` (**137**); `finalizeSpawn` also random (**137**) | persistent entity state |
| Values | RED_BLUE, BLUE, GREEN, YELLOW_BLUE, GRAY (**512–517**) | identity presentation |
| Persistence | Synched `DATA_VARIANT_ID` + NBT `"Variant"` int (**419–445**) | persistent entity state |
| Mutable after creation | `setVariant` public; no biome/thunder/environment flip found in `Parrot.java` | persistent entity state |
| Breeding / offspring | `canMate` → **false**; `getBreedOffspring` → **null**; `isFood` → **false** (**299–325**) | reproduction **absent** |
| Spawn vs origin | `checkParrotSpawnRules` + `#parrots_spawnable_on` (grass/air/leaves/logs). Biome spawners: jungle + bamboo_jungle weight **40**. Encounter floor ≠ origin. | environmental interaction |
| Render vs gameplay | `ParrotRenderer.getTextureLocation` switches on variant only. No gameplay branch on color found in `Parrot.java` | persistent entity state (visual) |
| BioCraft | Consumes `"parrot"` identity only — not color | identity / actual biological input (key) |

---

## 4. Cookie poison probe (mandatory)

Trace **input → immediate effect → target → persistence → biological state → BioCraft consumer**.

| Step | Evidence |
|------|----------|
| Input | `itemstack.is(ItemTags.PARROT_POISONOUS_FOOD)` — tag JSON values = **`minecraft:cookie` only** |
| Trigger | `mobInteract` when the held stack **is** poisonous food (else tame-food / sit / super) (**246–292**) |
| Immediate effect | Consume 1 cookie; `addEffect(MobEffects.POISON, 900)` on the Parrot; then `hurt(playerAttack, Float.MAX_VALUE)` unless `player.isCreative() \|\| !this.isInvulnerable()` (**285–289**) |
| Target | **Parrot only** (not the feeder) |
| Poison tick owner | `PoisonMobEffect.applyEffectTick`: 1 damage while health `> 1.0F` (NeoForge poison damage type) — redundant with MAX_VALUE hit in normal survival |
| Cookie class | `CookieItem.java` **does not exist** in the 1.21.1 sources jar. Interaction is Parrot + item tag, not a cookie-item override. |
| Special to Parrot? | Yes in this owner: tag + `Parrot.mobInteract`. Not a general cookie-poison world rule. |
| Persistence | Transient MobEffect + lethal damage. No surviving gene/variant/NBT biological residue from the cookie. |
| Biological state | None retained for BioCraft |
| BioCraft consumer | **None** |

Classification: **effect application** + entity death. Result **A**. Do not promote “poison isn’t a trait” as a slogan; the evidence is: owner exists, effect is transient, no BioCraft consumer.

---

## 5. Mimicry / flight / tame (owners first)

### Mimicry

- Ambient: `getAmbient` / `getAmbient(Level, Random)` — on non-PEACEFUL, 1/1000 chance pick imitated mob sound (**333–342**).
- Nearby: `aiStep` 1/400 → `imitateNearbyMobs` plays `getImitatedSound` (**186–187**, **225–233**).
- Sound map: static `MOB_SOUND_MAP` plus NeoForge `PARROT_IMITATIONS` data map (`ParrotImitation` record + `parrot_imitations.json`).
- Shoulder ambient: `Player.playShoulderEntityAmbientSound` only if stored id is `EntityType.PARROT` (`Player.java` **595–609**).
- Classification: transient gameplay / presentation (sound).
- BioCraft: **none**. Result **A** — not a speech-organ BP field without a named consumer. Do not pre-conclude mimicry can never have biological significance; it simply has no live BioCraft consumer here.

### Flight

- `FlyingMoveControl(this, 10, false)`; `FlyingPathNavigation`; `ParrotWanderGoal extends WaterAvoidingRandomFlyingGoal`; `isFlying()` = `!onGround()` (**128**, **171–176**, **449–450**, **463**).
- `FlyingAnimal` interface = marker method only (no extra state).
- `checkFallDamage` empty (**310–311**). Descent damping when `!onGround && vec.y < 0` (**218–220**).
- Classification: transient gameplay / movement.
- Prior Bat/Allay/Phantom = precedent that flight often stays **A**; independently confirmed: no BioCraft flight consumer. Result **A**.

### Tame / sit / shoulder

- Tame via `#parrot_food` (wheat/melon/pumpkin/beetroot/torchflower seeds, pitcher pod) 1/10 unless tame event cancels (**248–271**).
- Sit toggle when tame+owned+not flying (**275–278**).
- Shoulder: `LandOnOwnersShoulderGoal` → `ShoulderRidingEntity.setEntityOnShoulder` saves encode id + `saveWithoutId` onto `ServerPlayer.setEntityOnShoulder`, then `discard()` (**ShoulderRidingEntity.java** **17–26**).
- Classification: persistent tame/owner state (`TamableAnimal`) + player-attached NBT storage after discard (not living anatomy).
- Shared `TamableAnimal` with Cat/Wolf = implementation reuse ≠ pet biology clade.
- Result **A**.

---

## 6. Behavior ownership table

| Behavior | Actual owner | Classification | Biological input? | Existing composition | Named BioCraft consumer | Result |
|----------|--------------|----------------|-------------------|----------------------|-------------------------|--------|
| Identity | `EntityType.PARROT` | identity | Identity | `organismKey=parrot` | LIVE generic encodeId | **B** |
| Color variant | `Parrot.Variant` synched/NBT | persistent entity state | Visual only here | Identity sufficient | None | **A** |
| Tame / sit / shoulder | Tamable + ShoulderRiding | persistent / transient | No anatomy BP | Identity sufficient | None | **A** |
| Cookie poison | Tag + `mobInteract` | effect application | No | Identity sufficient | None | **A** |
| Mimicry | Sound + data map | transient presentation | No | Identity sufficient | None | **A** |
| Flight | Flying move/nav | transient movement | No | Identity sufficient | None | **A** |
| Breeding | Explicitly disabled | reproduction absent | Absent | — | None | **A** |
| Loot feathers | loot table | item/block production | No | Identity sufficient | None | **A** |
| Jungle spawn | biome spawners + `#parrots_spawnable_on` | environmental interaction | Encounter ≠ origin | Not origin field | None | **A** |
| Host contribution | hosts + gestation writer | actual biological input (key) | Identity only | key + baseline | **LIVE** | **B** |

Registration ≠ B by itself. Live `GestationManager.writeContributingSource` + `DnaSampleFromOccupant.organismKey` generic `encodeId` → `"parrot"` proves identity **B**. No variant/cookie/mimicry/flight consumer → no **C**.

---

## 7. Configuration audit

| Finding | Status | Interpretation |
|---------|--------|----------------|
| `hosts.json` `"parrot"` | **LIVE** | Participation |
| Parrot-specific BioCraft Java | **ABSENT** beyond list membership | Identity only |
| Cookie/variant/flight/mimicry fields | **ABSENT** | Do not invent |
| `variant_mappings` parrot | **ABSENT** | No override |

---

## 8. Tempting but rejected

- Color → BP phenotype family
- Shoulder sit → anatomy
- Mimicry → speech organ
- Flight → Flight Profile from distinctiveness or from Bat/Allay/Phantom adjacency
- Tame adjacency → wolf/cat clade
- Jungle spawn with panda → clade

---

## 9. Final evidence conclusion

| Question | Answer |
|----------|--------|
| New BP field? | **No** |
| Existing composition? | **Yes** — identity keys |
| Named consumer missing fact? | **No** |
| Escalation C? | **No** — **A + B** |
