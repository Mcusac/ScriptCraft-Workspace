# CRITICAL MISPLACED FILES: QUICK REFERENCE

## Layer 0 Domain - 24 files need relocation

### Ports (should be level_0 or level_1 based on imports)
| File | Current | Should Be | Imports From |
|------|---------|-----------|--------------|
| AttachmentStatePort | level_1 | level_0 | layer_0_domain.level_0 only |
| EffectApplicationPort | level_1 | level_0 | layer_0_domain.level_0 only |
| MaturationStatePort | level_1 | level_0 | layer_0_domain.level_0 only |
| WorldMutationPort | level_1/2 | level_0 | layer_0_domain.level_0 only |
| WorldQueryPort | level_1/2 | level_0 | layer_0_domain.level_0 only |
| EntitySpawnPort | level_2 | level_0 | layer_0_domain.level_0 only |
| XenomorphFormQueryPort | level_2 | level_0 | layer_0_domain.level_0 only |

### Type Definitions (should be level_0)
| File | Current | Should Be | Imports From |
|------|---------|-----------|--------------|
| HumanType | level_1 | level_0 | layer_0_domain.level_0 only |
| XenomorphType | level_1 | level_0 | layer_0_domain.level_0 only |
| HumanEntityType | level_1 | level_0 | layer_0_domain.level_0 only |
| DomainEffectKey | level_1 | level_0 | layer_0_domain.level_0 only |
| EffectApplyOptions | level_1 | level_0 | layer_0_domain.level_0 only |
| EffectState | level_1 | level_0 | layer_0_domain.level_0 only |
| StandardMobEffectKey | level_1 | level_0 | layer_0_domain.level_0 only |

### Rules & Business Logic (should be level_0 as they have no same-layer deps)
| File | Current | Should Be | Imports From |
|------|---------|-----------|--------------|
| AttachmentRules | level_1/2 | level_0 | layer_0_domain.level_0 only |
| SpawnContext | level_1/2 | level_0 | layer_0_domain.level_0 only |
| XenomorphTypeHelper | level_1/2 | level_0 | layer_0_domain.level_0 only |
| AttachmentConfigHelper | level_2 | level_0 | layer_0_domain.level_1 + level_0 |
| ParasiteFormPolicy | level_2 | level_0 | no same-layer imports |

---

## Layer 1 Infrastructure - 37 files need relocation from level_1+

### Config Loaders (all should be level_0)
| File | Current | Should Be | Reason |
|------|---------|-----------|--------|
| ConfigLoader | level_1 | level_0 | No same-layer deps |
| ConfigLoaderBase | level_1 | level_0 | No same-layer deps |
| ConfigLoaderRegistry | level_1 | level_0 | No same-layer deps |
| BlockConfigLoader | level_1 | level_0 | No same-layer deps |
| EntityConfigLoader | level_1 | level_0 | No same-layer deps |
| HostConfigLoader | level_1 | level_0 | No same-layer deps |
| CombatConfigLoader | level_1 | level_0 | No same-layer deps |
| MobEntityConfigLoader | level_1 | level_0 | No same-layer deps |

### Config Parsers (all should be level_0)
| File | Current | Should Be | Reason |
|------|---------|-----------|--------|
| BlockConfigParser | level_1 | level_0 | No same-layer deps |
| EffectConfigParser | level_1 | level_0 | No same-layer deps |
| MobEntityConfigParser | level_1 | level_0 | No same-layer deps |
| EntityConfigParser | level_2 | level_0 | No same-layer deps |

### Utilities & Helpers (all should be level_0)
| File | Current | Should Be | Reason |
|------|---------|-----------|--------|
| ResourceLoader | level_1 | level_0 | No same-layer deps |
| JsonParsingHelper | level_1 | level_0 | No same-layer deps |
| ConfigStorage | level_1 | level_0 | No same-layer deps |
| ResourceLoadingHelper | level_1 | level_0 | No same-layer deps |
| EntityConfigValidator | level_1 | level_0 | No same-layer deps |
| EntityConfigContracts | level_1 | level_0 | No same-layer deps |
| ConfigLoaderRegistrationHelper | level_2 | level_0 | No same-layer deps |

### Config Helpers (all should be level_0)
| File | Current | Should Be | Reason |
|------|---------|-----------|--------|
| AIContextThresholdsConfigHelper | level_1 | level_0 | No same-layer deps |
| AnimationTransitionConfigHelper | level_1 | level_0 | No same-layer deps |
| CombatProfileConfigHelper | level_1 | level_0 | No same-layer deps |
| NestProfileConfigHelper | level_1 | level_0 | No same-layer deps |

**Total Level 1 → 0: 37 files**

---

## Layer 2 Systems - 32 files need relocation

All files in level_1+ should be at level_0 because they have NO same-layer imports.

### Examples (showing pattern)
| File | Current | Should Be | Same-Layer Deps |
|------|---------|-----------|-----------------|
| BaseMaturationProcessor | level_1 | level_0 | None |
| BlockCombatHelper | level_1 | level_0 | None |
| HostEffectManager | level_1 | level_0 | None |
| GestationManager | level_2 | level_0 | None |
| BaseXenomorphTransformation | level_2 | level_0 | None |
| LifecycleBootstrap | level_2 | level_0 | None |

---

## Layer 3 Minecraft - 173+ files need relocation

**All files in level_1-10 should be consolidated to level_0 (infrastructure) or level_1-2 (implementation)**

### Current State: Extreme Level Inflation
```
level_0:  52 files [CORRECT]
level_1:  14 files → level_0
level_2:  25 files → level_0
level_3:  40 files → level_0/1
level_4:  27 files → level_0/1
level_5:  43 files → level_0/1
level_6:  44 files → level_0/1
level_7:  10 files → level_0/1
level_8:  14 files → level_0/1
level_9:  19 files → level_0/1
level_10: 12 files → level_0/1
```

### Samples of Misplaced Files
| File | Current | Should Be | Max Dep Level |
|------|---------|-----------|---------------|
| ChestbursterAI | level_6 | level_0-1 | 3 (cross-layer) |
| HumanRenderer | level_5 | level_0-1 | 2 (cross-layer) |
| BaseAnimationHelper | level_8 | level_0-1 | 1 (cross-layer) |
| AnimationSpeedHelper | level_7 | level_0-1 | 2 (cross-layer) |
| EntitySoundHelper | level_4 | level_0-1 | 2 (cross-layer) |
| DroneRenderer | level_10 | level_0-1 | 2 (cross-layer) |

**Pattern**: All level_1+ files in Layer 3 have:
- No same-layer dependencies, OR
- Only level_0 same-layer dependencies

Therefore, per the formula: `level = 1 + max(same-layer-deps)`, they should ALL be at level_0 or level_1.

---

## DUPLICATE CLASSES (Consolidation Priority)

| Class Name | Locations | Action |
|-----------|-----------|--------|
| AttachmentRules | layer_0/level_1, layer_0/level_2 | **DELETE level_2, keep level_1** |
| SpawnContext | layer_0/level_1, layer_0/level_2 | **DELETE level_2, keep level_1** |
| WorldMutationPort | layer_0/level_1, layer_0/level_2 | **DELETE level_2, keep level_1** |
| WorldQueryPort | layer_0/level_1, layer_0/level_2 | **DELETE level_2, keep level_1** |
| XenomorphTypeHelper | layer_0/level_1, layer_0/level_2 | **DELETE level_2, keep level_1** |
| ConfigLoaderRegistrationHelper | layer_1/level_0, level_1, level_2, level_4 | **Keep level_0 as source of truth, DELETE others** |
| AttachmentConfigHelper | layer_0/level_2, layer_1/level_4 | **Keep layer_0, DELETE layer_1** |

**Action**: Search and replace imports, delete duplicate files, run full rebuild.

---

## SUMMARY TABLE

| Layer | Total Files | Level 0 (correct) | Wrong Levels | % Correct | Action |
|-------|------------|------------------|--------------|-----------|--------|
| Layer 0 Domain | 85 | 45 | 40 | 53% | Move 24 from L1→L0, consolidate 16 L2 dups |
| Layer 1 Infra | 79 | 29 | 50 | 37% | Move 50 from L1-4→L0 |
| Layer 2 Systems | 100 | 50 | 50 | 50% | Move 50 from L1-4→L0 |
| Layer 3 Minecraft | 300 | 52 | 248 | 17% | Collapse levels 1-10 to 0-2 (move 248) |
| **TOTAL** | **564** | **176** | **388** | **31%** | **Relocate 264 files** |

---

## RELOCATION STRATEGY

### Phase 1: Eliminate Duplicates (Week 1)
1. Find all files with duplicate names across levels
2. Identify which is "authoritative" (usually level_0 or earliest)
3. Update all imports in codebase to point to canonical location
4. Delete duplicate files
5. **Impact**: Reduces scope by ~20 files

### Phase 2: Collapse to Correct Levels (Weeks 2-3)
Using automated tooling:
1. Calculate required level for each file
2. If wrong level, move file to correct level
3. Update package declarations
4. Rebuild and verify
5. Run full test suite
6. **Impact**: Fix 264 files per governance formula

### Phase 3: Governance Automation (Week 4)
Add build-time checks:
1. Maven/Gradle plugin to verify levels
2. Pre-commit hook to catch violations
3. Documentation in ARCHITECTURE.md
4. CI/CD gate to prevent future violations

---

**Analysis Date**: 2026-06-24  
**Status**: Ready for remediation
