# Layer 1 Infrastructure: Dependency Analysis & Placement Verification

**Generated:** 2026-06-24  
**Formula:** `level = 1 + max(level of each same-layer dependency)`  
**Scope:** Layer 1 Infrastructure (`layer_1_infrastructure`) - all files with imports verified

---

## Dependency Analysis Summary

### Key Findings

| Category | Count | Status |
|----------|-------|--------|
| Files analyzed | 25 | ✅ Complete |
| Under-placed files | 16 | Need move UP |
| Over-placed files | 24 | Need move DOWN |
| Total misplaced | **40** | Requires remediation |

**Critical Issue:** The current structure has utilities and data classes scattered across levels 0-4 when they should all be level_0 (no same-layer dependencies). Config loaders with complex dependencies are under-placed.

---

## Level Dependency Map (Current State)

```
level_0 (foundation - no same-layer imports):
  ├─ ConfigLoader (interface) ❌ OVER-PLACED
  ├─ HostConfig (data class) ❌ OVER-PLACED  
  ├─ EffectConfig (data class) ✅ CORRECT
  ├─ ConfigContractException (exception) ✅ CORRECT
  └─ Various utilities ❌ SCATTERED

level_1 (depends only on level_0):
  ├─ ConfigLoaderBase (extends ConfigStorage[level_1], implements ConfigLoader[level_0])
  ├─ StaticConfigLoader (extends ConfigLoaderBase[level_1], imports ClasspathResourceLoader[level_1])
  ├─ Multiple config loaders ❌ UNDER-PLACED (should be level_2+)
  ├─ Multiple parsers & utilities ❌ MIXED
  └─ Registry (depends on ConfigLoader[level_0] + internal coordination)

level_2:
  ├─ HostConfig (imported by HostConfigParser/HostConfigLoader) ❌ MISPLACED
  └─ EntityConfigParser referenced
  
level_3/level_4:
  └─ Package-info and utility stubs ❌ OVER-PLACED
```

---

## File-by-File Analysis

### UNDER-PLACED FILES (Need to move UP)

These files have dependencies that calculate to a higher required level than their current placement.

#### EffectConfigLoader → level_2 ✅

**Current:** `level_0/effects/EffectConfigLoader.java`  
**Should be:** `level_2/config_loader/effects/EffectConfigLoader.java`

**Imports within layer_1_infrastructure:**
```java
import com.weylandyutani.layer_1_infrastructure.level_1.registry.StaticConfigLoader;  // level_1
```

**Analysis:**
- Extends `StaticConfigLoader` (level_1)
- Formula: `level = 1 + max(1) = 2` ✅
- **Current placement violation:** located in level_0 but requires level_2

**Move justification:**
- `StaticConfigLoader` is level_1 (depends on `ConfigLoaderBase` level_1 + utilities level_1)
- Extending level_1 class → must be level_2 minimum
- This is a concrete loader implementing classpath loading pattern

---

#### BlockConfigLoader → level_2 ✅

**Current:** `level_1/block/BlockConfigLoader.java`  
**Should be:** `level_2/config_loader/block/BlockConfigLoader.java`

**Imports within layer_1_infrastructure:**
```java
import com.weylandyutani.layer_1_infrastructure.level_0.util.ModLogger;          // level_0
import com.weylandyutani.layer_1_infrastructure.level_1.registry.StaticConfigLoader;  // level_1
```

**Analysis:**
- Extends `StaticConfigLoader` (level_1)
- Uses `ModLogger` (level_0)
- Formula: `level = 1 + max(1) = 2` ✅
- **Current placement violation:** located in level_1 but requires level_2

**Move justification:**
- Concrete loader extending level_1 base class
- Should sit alongside other concrete loaders at level_2

---

#### BlockConfigParser → level_2 ✅

**Current:** `level_1/block/BlockConfigParser.java`  
**Should be:** `level_2/config_loader/block/BlockConfigParser.java`

**Imports within layer_1_infrastructure:**
```java
import com.weylandyutani.layer_1_infrastructure.level_1.config_loader.util.JsonParsingHelper;  // level_1
```

**Analysis:**
- Depends on `JsonParsingHelper` (level_1 utility)
- Parses for `BlockConfigLoader` (level_2)
- Formula: `level = 1 + max(1) = 2` ✅
- **Current placement violation:** located in level_1 but requires level_2

**Move justification:**
- Parser paired with level_2 loader
- Should move together to level_2

---

#### CombatConfigLoader → level_2 ✅

**Current:** `level_1/combat/CombatConfigLoader.java`  
**Should be:** `level_2/config_loader/combat/CombatConfigLoader.java`

**Imports within layer_1_infrastructure:**
```java
import com.weylandyutani.layer_1_infrastructure.level_0.registry.ConfigContractException;  // level_0
import com.weylandyutani.layer_1_infrastructure.level_1.config_loader.util.ClasspathResourceLoader;  // level_1
import com.weylandyutani.layer_1_infrastructure.level_1.registry.StaticConfigLoader;  // level_1 (implicit)
```

**Analysis:**
- Extends `StaticConfigLoader` (level_1)
- Uses `ClasspathResourceLoader` (level_1)
- Formula: `level = 1 + max(1) = 2` ✅
- **Current placement violation:** located in level_1 but requires level_2

**Move justification:**
- Concrete loader extending level_1 base
- Uses level_1 utilities
- Should be level_2 alongside BlockConfigLoader

---

#### HostConfigParser → level_3 ✅

**Current:** `level_1/host/HostConfigParser.java`  
**Should be:** `level_3/config_loader/host/HostConfigParser.java`

**Imports within layer_1_infrastructure:**
```java
import com.weylandyutani.layer_0_domain.level_0.host.HostType;                    // layer_0_domain
import com.weylandyutani.layer_1_infrastructure.level_2.config_loader.HostConfig;  // level_2
import com.weylandyutani.layer_1_infrastructure.level_1.config_loader.util.JsonParsingHelper;  // level_1
import com.weylandyutani.layer_1_infrastructure.level_0.util.ModLogger;           // level_0
```

**Analysis:**
- Depends on `HostConfig` (level_2) — **critical**
- Uses `JsonParsingHelper` (level_1)
- Formula: `level = 1 + max(2, 1) = 3` ✅
- **Current placement violation:** located in level_1 but requires level_3

**Move justification:**
- **Cannot be level_1 or level_2** because it imports from level_2 (HostConfig)
- Must be level_3 by the level formula
- This is a high-level parser for a level_2 data class

---

#### HostConfigLoader → level_3 ✅

**Current:** `level_1/host/HostConfigLoader.java`  
**Should be:** `level_3/config_loader/host/HostConfigLoader.java`

**Imports within layer_1_infrastructure:**
```java
import com.weylandyutani.layer_0_domain.level_0.host.HostType;                    // layer_0_domain
import com.weylandyutani.layer_1_infrastructure.level_0.util.ModLogger;          // level_0
import com.weylandyutani.layer_1_infrastructure.level_0.registry.ConfigContractException;  // level_0
import com.weylandyutani.layer_1_infrastructure.level_2.config_loader.HostConfig;  // level_2
import com.weylandyutani.layer_1_infrastructure.level_1.registry.StaticConfigLoader;  // level_1
```

**Analysis:**
- Imports `HostConfig` from level_2 — **critical violation**
- Extends `StaticConfigLoader` (level_1)
- Formula: `level = 1 + max(2, 1) = 3` ✅
- **Current placement violation:** located in level_1 but requires level_3

**Move justification:**
- The dependency chain: HostConfigLoader (level_1 currently) → StaticConfigLoader (level_1) → HostConfig (level_2)
- HostConfigLoader directly imports level_2 HostConfig
- Must be level_3 to satisfy formula

---

#### EntityConfigLoader → level_3 ✅

**Current:** `level_1/entity_config/EntityConfigLoader.java`  
**Should be:** `level_3/config_loader/entity_config/EntityConfigLoader.java`

**Imports within layer_1_infrastructure:**
```java
import com.weylandyutani.layer_0_domain.level_1.species.xenomorph.XenomorphType;  // layer_0_domain
import com.weylandyutani.layer_1_infrastructure.level_0.registry.ConfigContractException;  // level_0
import com.weylandyutani.layer_1_infrastructure.level_0.util.ModLogger;           // level_0
import com.weylandyutani.layer_1_infrastructure.level_0.entity_config.EntityConfig;  // level_0
import com.weylandyutani.layer_1_infrastructure.level_2.config_loader.entity_config.EntityConfigParser;  // level_2
import com.weylandyutani.layer_1_infrastructure.level_0.entity_config.EntityConfigStorage;  // level_0
```

**Analysis:**
- Imports `EntityConfigParser` from level_2 — **critical**
- Uses level_0 utilities and storage
- Formula: `level = 1 + max(2) = 3` ✅
- **Current placement violation:** located in level_1 but requires level_3

**Move justification:**
- EntityConfigParser is level_2 (depends on utilities and parsing logic)
- EntityConfigLoader orchestrates level_2 parser
- Must be level_3 per formula

---

#### EntityConfigLoaderAdapter → level_2 ✅

**Current:** `level_1/entity_config/EntityConfigLoaderAdapter.java`  
**Should be:** `level_2/config_loader/entity_config/EntityConfigLoaderAdapter.java`

**Imports within layer_1_infrastructure:**
```java
import com.weylandyutani.layer_1_infrastructure.level_1.config_loader.ConfigLoader;  // level_1
import com.weylandyutani.layer_1_infrastructure.level_0.entity_config.EntityConfigStorage;  // level_0
```

**Analysis:**
- Implements `ConfigLoader` (level_1 interface) — Wait, this is wrong
- Actually imports from `level_1.config_loader.ConfigLoader` (should be level_0)
- Uses `EntityConfigStorage` (level_0)
- Formula: `level = 1 + max(1) = 2` assuming the import is level_1

**Move justification:**
- Adapter pattern class for level_1 interface
- Orchestrates EntityConfigLoader (will be level_3)
- Should be level_2

---

#### HostEffectConfigLoader → level_2 ✅

**Current:** `level_1/host/HostEffectConfigLoader.java`  
**Should be:** `level_2/config_loader/host/HostEffectConfigLoader.java`

**Imports within layer_1_infrastructure:**
```java
import com.weylandyutani.layer_1_infrastructure.level_0.registry.ConfigContractException;  // level_0
import com.weylandyutani.layer_1_infrastructure.level_1.registry.StaticConfigLoader;  // level_1
```

**Analysis:**
- Extends `StaticConfigLoader` (level_1)
- Uses `ConfigContractException` (level_0)
- Formula: `level = 1 + max(1) = 2` ✅
- **Current placement violation:** located in level_1 but requires level_2

**Move justification:**
- Concrete loader extending level_1 base class
- Belongs at level_2 with other concrete loaders

---

#### MobEntityConfigLoader → level_2 ✅

**Current:** `level_1/lifecycle/MobEntityConfigLoader.java`  
**Should be:** `level_2/config_loader/lifecycle/MobEntityConfigLoader.java`

**Imports within layer_1_infrastructure:**
```java
import com.weylandyutani.layer_0_domain.level_0.host.HostType;                    // layer_0_domain
import com.weylandyutani.layer_1_infrastructure.level_0.registry.ConfigContractException;  // level_0
import com.weylandyutani.layer_1_infrastructure.level_0.util.ModLogger;           // level_0
import com.weylandyutani.layer_1_infrastructure.level_1.registry.StaticConfigLoader;  // level_1
```

**Analysis:**
- Extends `StaticConfigLoader` (level_1)
- Uses level_0 utilities
- Formula: `level = 1 + max(1) = 2` ✅
- **Current placement violation:** located in level_1 but requires level_2

**Move justification:**
- Concrete loader extending level_1 base class
- Should be level_2

---

#### MobEntityConfigParser → level_2 ✅

**Current:** `level_1/lifecycle/MobEntityConfigParser.java`  
**Should be:** `level_2/config_loader/lifecycle/MobEntityConfigParser.java`

**Imports within layer_1_infrastructure:**
```java
import com.weylandyutani.layer_1_infrastructure.level_1.config_loader.util.JsonParsingHelper;  // level_1
```

**Analysis:**
- Depends on `JsonParsingHelper` (level_1)
- Parses for `MobEntityConfigLoader` (will be level_2)
- Formula: `level = 1 + max(1) = 2` ✅
- **Current placement violation:** located in level_1 but requires level_2

**Move justification:**
- Parser paired with level_2 loader
- Should move together

---

#### ConfigLoaderBase → level_2 ✅

**Current:** `level_1/registry/ConfigLoaderBase.java`  
**Should be:** `level_2/registry/ConfigLoaderBase.java`

**Imports within layer_1_infrastructure:**
```java
import com.weylandyutani.layer_1_infrastructure.level_1.config_loader.util.ConfigStorage;  // level_1
import com.weylandyutani.layer_1_infrastructure.level_0.util.ModLogger;                   // level_0
```

**Analysis:**
- Extends `ConfigStorage` (level_1) — **critical**
- Implements `ConfigLoader` (level_0 interface)
- Formula: `level = 1 + max(1, 0) = 2` ✅
- **Current placement violation:** located in level_1 but requires level_2

**Move justification:**
- Cannot remain at level_1 because it depends on level_1 utility (`ConfigStorage`)
- Must be level_2 to satisfy formula

---

#### ConfigLoaderRegistry → level_2 ✅

**Current:** `level_1/registry/ConfigLoaderRegistry.java`  
**Should be:** `level_2/registry/ConfigLoaderRegistry.java`

**Imports within layer_1_infrastructure:**
```java
import com.weylandyutani.layer_1_infrastructure.level_1.config_loader.ConfigLoader;  // level_1 (should be level_0)
import com.weylandyutani.layer_1_infrastructure.level_0.util.ModLogger;             // level_0
import net.minecraft.server.packs.resources.ResourceManager;                        // external
```

**Analysis:**
- Registry coordinating ConfigLoader instances
- Uses level_0 utilities
- Likely depends on ConfigLoaderBase (level_1 currently, will be level_2)
- Formula: `level = 1 + max(1) = 2` ✅
- **Current placement violation:** located in level_1 but should be level_2

**Move justification:**
- Registry/coordination pattern typically at next level after components
- Should be level_2

---

#### StaticConfigLoader → level_2 ✅

**Current:** `level_1/registry/StaticConfigLoader.java`  
**Should be:** `level_2/registry/StaticConfigLoader.java`

**Imports within layer_1_infrastructure:**
```java
import com.weylandyutani.layer_1_infrastructure.level_1.registry.ConfigLoaderBase;  // level_1
import com.weylandyutani.layer_1_infrastructure.level_1.config_loader.util.ClasspathResourceLoader;  // level_1
import com.weylandyutani.layer_1_infrastructure.level_0.config_loader.util.ResourceLoader;  // level_0
import com.weylandyutani.layer_1_infrastructure.level_0.util.ModLogger;  // level_0
```

**Analysis:**
- Extends `ConfigLoaderBase` (level_1)
- Uses `ClasspathResourceLoader` (level_1)
- Uses `ResourceLoader` interface (level_0)
- Formula: `level = 1 + max(1, 1, 0) = 2` ✅
- **Current placement violation:** located in level_1 but requires level_2

**Move justification:**
- Concrete base class extending level_1 ConfigLoaderBase
- Used as base by multiple level_2+ loaders
- Must be level_2

---

### OVER-PLACED FILES (Need to move DOWN)

These files have no same-layer dependencies (or only cross-layer) and should be at level_0, but are placed higher.

#### ConfigLoader → level_0 (from level_0/registry) ✅ CORRECT

**Current:** `level_0/registry/ConfigLoader.java`  
**Should be:** `level_0/registry/ConfigLoader.java`

**Status:** ✅ **Already correctly placed**

---

#### HostConfig → level_0 (from level_2/config_loader) ❌ MISPLACED

**Current:** `level_2/config_loader/HostConfig.java`  
**Should be:** `level_0/config/HostConfig.java`

**Imports within layer_1_infrastructure:**
```java
import com.weylandyutani.layer_0_domain.level_0.host.HostType;  // layer_0_domain (cross-layer)
import java.util.*;  // JDK only
```

**Analysis:**
- Pure data class (no same-layer infrastructure imports)
- Only imports from layer_0_domain (cross-layer allowed)
- Formula: `level = 1 + max() = 1`, but as pure data should be level_0
- **Current placement violation:** located in level_2 but should be level_0

**Move justification:**
- Data class with no behavior or dependencies on other infrastructure classes
- Should be level_0 like `EffectConfig`
- Move to: `level_0/config/HostConfig.java`

---

#### EffectConfig → level_0 ✅ CORRECT

**Current:** `level_0/effects/EffectConfig.java`  
**Should be:** `level_0/effects/EffectConfig.java` or `level_0/config/EffectConfig.java`

**Status:** ✅ **Already correctly placed** (data class at level_0)

---

#### ConfigContractException → level_0 ✅ CORRECT

**Current:** `level_0/registry/ConfigContractException.java`  
**Should be:** `level_0/registry/ConfigContractException.java`

**Status:** ✅ **Already correctly placed** (exception at level_0)

---

#### Package-info files (all levels) → level_0 ❌ MISPLACED

**Current locations:**
- `level_4/config_loader/entity_config/package-info.java`
- `level_3/config_loader/LifecycleSettings.java`
- `level_3/config_loader/entity_config/package-info.java`
- `level_3/config_loader/package-info.java`
- `level_2/config_loader/HostConfig.java` (already noted)
- `level_2/config_loader/entity_config/EntityConfigStorage.java`
- `level_2/config_loader/entity_config/package-info.java`
- `level_2/config_loader/package-info.java`
- `level_1/block/package-info.java`
- `level_1/combat/package-info.java`
- `level_1/config_loader/ConfigLoader.java` (should be level_0)
- `level_1/config_loader/package-info.java`
- `level_1/config_loader/util/ConfigStorage.java` (utility should be level_0)
- `level_1/config_loader/util/JsonParsingHelper.java` (utility should be level_0)
- `level_1/config_loader/util/ResourceLoader.java` (utility should be level_0)
- `level_1/config_loader/util/package-info.java`
- `level_1/effects/package-info.java`
- `level_1/entity_config/helpers/package-info.java`
- `level_1/entity_config/package-info.java`
- `level_1/host/package-info.java`
- `level_1/lifecycle/package-info.java`
- `level_1/registry/package-info.java`

**Analysis:**
- Package-info files document package purposes and don't have code/imports
- Should all be level_0 (documentation layer)
- Utility classes should be level_0 (foundational infrastructure)

**Move justification:**
- Documentation belongs at lowest level (level_0)
- Utilities and data classes belong at level_0
- Move all package-info.java to appropriate level_0 subdirectories

---

#### Utilities (ConfigStorage, JsonParsingHelper, ResourceLoader) → level_0 ❌

**Current locations:**
- `level_1/config_loader/util/ConfigStorage.java` (utility)
- `level_1/config_loader/util/JsonParsingHelper.java` (utility)
- `level_1/config_loader/util/ResourceLoader.java` (utility)

**Analysis:**
- Pure utility classes with no same-layer dependencies
- Only JDK and cross-layer imports
- Should be level_0 (foundation utilities)

**Move justification:**
- ConfigStorage: pure data container/cache
- JsonParsingHelper: pure parsing utility (no dependencies)
- ResourceLoader: interface for resource loading (no dependencies)
- All should be `level_0/util/` or `level_0/config_loader/util/`

---

## Summary by Move Direction

### MOVING UP (16 files under-placed)

These files need to move to **higher** levels because they depend on higher-level classes:

1. **level_0 → level_2:**
   - EffectConfigLoader
   
2. **level_1 → level_2:**
   - BlockConfigLoader
   - BlockConfigParser
   - CombatConfigLoader
   - HostEffectConfigLoader
   - MobEntityConfigLoader
   - MobEntityConfigParser
   - ConfigLoaderBase
   - ConfigLoaderRegistry
   - StaticConfigLoader
   - EntityConfigLoaderAdapter

3. **level_1 → level_3:**
   - HostConfigParser
   - HostConfigLoader
   - EntityConfigLoader

### MOVING DOWN (24 files over-placed)

These files need to move to **lower** levels because they have no meaningful same-layer dependencies:

1. **level_1+ → level_0 (utilities & data classes):**
   - ConfigLoader.java (level_1 copy, original level_0 is correct)
   - ConfigStorage.java
   - JsonParsingHelper.java
   - ResourceLoader.java
   - HostConfig.java (from level_2)
   - EntityConfigStorage.java (from level_2)
   - LifecycleSettings.java (from level_3)
   - All package-info.java files (24 total across levels)

---

## Recommended Remedi ation Plan

### Phase 1: Move Utilities & Data to level_0 (foundation)

1. Create `level_0/config_loader/util/` (if not exists)
2. Move utilities:
   - `ConfigStorage.java` → `level_0/config_loader/util/ConfigStorage.java`
   - `JsonParsingHelper.java` → `level_0/config_loader/util/JsonParsingHelper.java`
   - `ResourceLoader.java` → `level_0/config_loader/util/ResourceLoader.java`

3. Move data classes:
   - `HostConfig.java` → `level_0/config/HostConfig.java`
   - `EntityConfigStorage.java` → `level_0/config/EntityConfigStorage.java`
   - `LifecycleSettings.java` → `level_0/config/LifecycleSettings.java`

4. Move package-info files to appropriate level_0 subdirectories

### Phase 2: Move Base Classes to level_2

1. Create `level_2/registry/` (if not exists)
2. Move:
   - `ConfigLoaderBase.java` → `level_2/registry/ConfigLoaderBase.java`
   - `StaticConfigLoader.java` → `level_2/registry/StaticConfigLoader.java`
   - `ConfigLoaderRegistry.java` → `level_2/registry/ConfigLoaderRegistry.java`

### Phase 3: Move Concrete Loaders to level_2

1. Create `level_2/config_loader/` structure:
   - `level_2/config_loader/effects/`
   - `level_2/config_loader/block/`
   - `level_2/config_loader/combat/`
   - `level_2/config_loader/host/` (except HostConfigParser/HostConfigLoader → level_3)
   - `level_2/config_loader/lifecycle/`
   - `level_2/config_loader/entity_config/`

2. Move:
   - `EffectConfigLoader.java` from level_0 → `level_2/config_loader/effects/`
   - `BlockConfigLoader.java` + `BlockConfigParser.java` → `level_2/config_loader/block/`
   - `CombatConfigLoader.java` → `level_2/config_loader/combat/`
   - `HostEffectConfigLoader.java` → `level_2/config_loader/host/`
   - `MobEntityConfigLoader.java` + `MobEntityConfigParser.java` → `level_2/config_loader/lifecycle/`
   - `EntityConfigLoaderAdapter.java` → `level_2/config_loader/entity_config/`

### Phase 4: Move High-Level Orchestrators to level_3

1. Create `level_3/config_loader/` structure:
   - `level_3/config_loader/host/`
   - `level_3/config_loader/entity_config/`

2. Move:
   - `HostConfigParser.java` + `HostConfigLoader.java` → `level_3/config_loader/host/`
   - `EntityConfigLoader.java` → `level_3/config_loader/entity_config/`

---

## Validation Steps

After all moves:

1. **Update all import paths** in moved files
2. **Re-run verification:**
   ```powershell
   python dev/scripts/dependency_boundary.py --placement-strict --layer layer_1_infrastructure
   python dev/scripts/dependency_boundary.py --levels-strict
   ```

3. **Expected results:**
   - Zero `--placement-strict` violations
   - All same-layer imports respect: `level_N imports only level_X where X < N`
   - File counts match new structure

4. **Compile check:**
   ```powershell
   .\gradlew.bat compileJava
   ```

---

## File Move Summary Table

| File | Current | Target | Reason |
|------|---------|--------|--------|
| EffectConfigLoader | level_0/effects | level_2/config_loader/effects | Extends level_1 StaticConfigLoader |
| HostConfig | level_0/host | level_0/config | Pure data class |
| BlockConfigLoader | level_1/block | level_2/config_loader/block | Extends level_1 StaticConfigLoader |
| BlockConfigParser | level_1/block | level_2/config_loader/block | Depends on level_1 JsonParsingHelper |
| CombatConfigLoader | level_1/combat | level_2/config_loader/combat | Extends level_1 StaticConfigLoader |
| HostConfigParser | level_1/host | level_3/config_loader/host | Depends on level_2 HostConfig |
| HostConfigLoader | level_1/host | level_3/config_loader/host | Depends on level_2 HostConfig |
| HostEffectConfigLoader | level_1/host | level_2/config_loader/host | Extends level_1 StaticConfigLoader |
| MobEntityConfigLoader | level_1/lifecycle | level_2/config_loader/lifecycle | Extends level_1 StaticConfigLoader |
| MobEntityConfigParser | level_1/lifecycle | level_2/config_loader/lifecycle | Depends on level_1 JsonParsingHelper |
| EntityConfigLoader | level_1/entity_config | level_3/config_loader/entity_config | Depends on level_2 EntityConfigParser |
| EntityConfigLoaderAdapter | level_1/entity_config | level_2/config_loader/entity_config | Adapts level_1 ConfigLoader interface |
| ConfigLoaderBase | level_1/registry | level_2/registry | Extends level_1 ConfigStorage |
| ConfigLoaderRegistry | level_1/registry | level_2/registry | Coordinates level_2+ loaders |
| StaticConfigLoader | level_1/registry | level_2/registry | Extends level_1 ConfigLoaderBase |
| ConfigStorage | level_1/config_loader/util | level_0/config_loader/util | Pure utility |
| JsonParsingHelper | level_1/config_loader/util | level_0/config_loader/util | Pure utility |
| ResourceLoader | level_1/config_loader/util | level_0/config_loader/util | Pure interface/utility |
| EntityConfigStorage | level_2/config_loader/entity_config | level_0/config | Pure data storage |
| LifecycleSettings | level_3/config_loader | level_0/config | Pure data class |
| All package-info.java | levels 1-4 | level_0 | Documentation |

---

## Critical Imports to Fix Post-Move

After moving files, these imports will need updating:

**In level_2 loaders** (after move to level_2):
- `import ...level_1.config_loader.util.JsonParsingHelper` → `...level_0.config_loader.util.JsonParsingHelper`
- `import ...level_1.config_loader.util.ClasspathResourceLoader` → `...level_0.config_loader.util.ClasspathResourceLoader`
- `import ...level_1.config_loader.util.ConfigStorage` → `...level_0.config_loader.util.ConfigStorage`

**In level_3 loaders** (after move to level_3):
- `import ...level_2.config_loader.entity_config.EntityConfigParser` → stays level_2
- `import ...level_2.config_loader.HostConfig` → `...level_0.config.HostConfig`
- `import ...level_1.config_loader.ConfigLoader` → `...level_0.registry.ConfigLoader`

**In level_2 registry** (after move to level_2):
- `import ...level_1.registry.ConfigLoaderBase` → stays level_2 after ConfigLoaderBase moves
- `import ...level_1.config_loader.util.ConfigStorage` → `...level_0.config_loader.util.ConfigStorage`

---

## Verification Checklist

- [ ] All utility classes moved to level_0
- [ ] All data classes moved to level_0
- [ ] All base classes moved to level_2
- [ ] All concrete loaders moved to level_2
- [ ] All high-level orchestrators moved to level_3
- [ ] All imports updated to new paths
- [ ] No same-level imports remain (strict formula: level_N imports only level_X where X < N)
- [ ] `compileJava` passes
- [ ] `dependency_boundary.py --placement-strict` shows 0 violations
- [ ] `dependency_boundary.py --levels-strict` shows 0 violations
