import os
import re
from pathlib import Path
from collections import defaultdict

base_path = Path('implementations/minecraft/AlienCraft/weyland-yutani-core/src/main/java/com/weylandyutani')

# Collect all classes/interfaces and what they depend on
classes_info = {}
cross_layer_dependencies = defaultdict(set)
missing_implementations = set()

for java_file in sorted(base_path.rglob('*.java')):
    rel_str = str(java_file.relative_to(base_path)).replace('\\', '/')
    
    try:
        with open(java_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue
    
    # Extract class/interface name
    class_match = re.search(r'(?:public\s+)?(?:class|interface|enum)\s+(\w+)', content)
    if not class_match:
        continue
    
    classname = class_match.group(1)
    
    # Extract package
    pkg_match = re.search(r'package\s+([\w\.]+);', content)
    package = pkg_match.group(1) if pkg_match else ''
    
    # Extract all weylandyutani imports
    all_imports = re.findall(r'import\s+com\.weylandyutani\.([^\s;]+);', content)
    
    # Categorize by layer
    same_layer = [imp for imp in all_imports if imp.split('/')[0] in ['layer_0_domain', 'layer_1_infrastructure'] and imp.startswith(rel_str.split('/')[0] + '/')]
    cross_layer = [imp for imp in all_imports if imp.split('/')[0] in ['layer_0_domain', 'layer_1_infrastructure'] and not imp.startswith(rel_str.split('/')[0] + '/')]
    
    classes_info[classname] = {
        'file': java_file.name,
        'path': rel_str,
        'package': package,
        'same_layer': same_layer,
        'cross_layer': cross_layer,
    }
    
    # Track cross-layer deps
    for imp in cross_layer:
        cross_layer_dependencies[classname].add(imp)

print("=" * 80)
print("CROSS-LAYER DEPENDENCIES (Layer 0 Domain / Layer 1 Infrastructure)")
print("=" * 80)

# Organize by dependency pattern
print("\nClasses in Layer 1 Infrastructure depending on Layer 0 Domain:")
print("-" * 80)

layer_1_depends_on_layer_0 = []
for classname, info in sorted(classes_info.items()):
    for dep in info['cross_layer']:
        if dep.startswith('layer_0_domain/'):
            layer_1_depends_on_layer_0.append((classname, info['path'], dep))

for classname, path, dep in sorted(layer_1_depends_on_layer_0):
    # Extract what it depends on
    parts = dep.split('/')
    level = parts[1] if len(parts) > 1 else '?'
    print(f"{classname:40} -> {level} ({dep})")

print(f"\nTotal: {len(layer_1_depends_on_layer_0)} dependencies")

print("\n" + "=" * 80)
print("ANALYZING MISSING RESPONSIBILITIES")
print("=" * 80)

# Check what patterns of cross-layer deps we see
layer_1_to_level_0_domain = defaultdict(int)
layer_1_to_level_1_domain = defaultdict(int)

for classname, info in classes_info.items():
    for dep in info['cross_layer']:
        if dep.startswith('layer_0_domain/'):
            parts = dep.split('/')
            if len(parts) > 1:
                level = parts[1]
                layer_1_to_level_0_domain[level] += 1

print("\nLayer 1 Infrastructure dependencies breakdown:")
for level in sorted(layer_1_to_level_0_domain.keys()):
    count = layer_1_to_level_0_domain[level]
    print(f"  {level}: {count} references")

# Look for specific missing responsibilities
print("\n" + "=" * 80)
print("PORT/ADAPTER PATTERN ANALYSIS")
print("=" * 80)

# Find all port/adapter definitions
ports = [name for name, info in classes_info.items() if 'Port' in name or 'Adapter' in name]

print(f"\nFound {len(ports)} Port/Adapter classes:")
for name in sorted(ports):
    info = classes_info[name]
    path = info['path']
    layer = path.split('/')[0]
    level = path.split('/')[1] if len(path.split('/')) > 1 else '?'
    print(f"  {name:40} @ {layer}/{level}")
    
    # Show what it imports
    if info['cross_layer']:
        print(f"     -> imports from: {info['cross_layer'][0]}")

print("\n" + "=" * 80)
print("LEVEL INFLATION: Files at Wrong Levels (not same-layer deps)")
print("=" * 80)

print("\nLayer 0 Domain - files in level_1/level_2 but only importing level_0:")
for classname, info in sorted(classes_info.items()):
    if 'layer_0_domain' in info['path']:
        path_parts = info['path'].split('/')
        if len(path_parts) > 1 and path_parts[1] in ['level_1', 'level_2']:
            # Check if they only import level_0
            has_level_0_deps = any('level_0' in dep for dep in info['same_layer'])
            has_higher_deps = any('level_1' in dep or 'level_2' in dep for dep in info['same_layer'])
            
            if has_level_0_deps and not has_higher_deps:
                print(f"  {classname:40} @ {path_parts[1]}")
                print(f"     path: {info['path']}")
                if info['same_layer']:
                    print(f"     imports: {info['same_layer'][0]}")

print("\n" + "=" * 80)
print("DUPLICATED/MISPLACED CLASSES")
print("=" * 80)

# Find classes that appear in multiple places
filename_count = defaultdict(list)
for classname, info in classes_info.items():
    filename_count[info['file']].append((classname, info['path']))

duplicates = {fname: classes for fname, classes in filename_count.items() if len(classes) > 1}

print(f"\nFiles with multiple classes: {len(duplicates)}")
for fname, classes in sorted(duplicates.items())[:5]:
    print(f"\n{fname}:")
    for classname, path in classes:
        print(f"  {classname} @ {path}")

# Find classes that appear in different locations with same name
classname_locations = defaultdict(list)
for classname, info in classes_info.items():
    classname_locations[classname].append(info['path'])

duplicated_names = {name: paths for name, paths in classname_locations.items() if len(paths) > 1}

print(f"\n\nClasses with same name in multiple locations: {len(duplicated_names)}")
for classname, paths in sorted(duplicated_names.items()):
    print(f"  {classname}:")
    for path in sorted(paths):
        print(f"    - {path}")

print("\n" + "=" * 80)
print("SUMMARY: ROOT CAUSES OF MISPLACED FILES")
print("=" * 80)

print("""
1. CROSS-LAYER DEPENDENCIES (files must be in same layer to use port pattern)
   - Layer 1 infra classes depend on Layer 0 domain types
   - This is CORRECT per layered architecture
   - But then those Layer 1 classes should be at level_0 if they don't depend on other Layer 1 classes

2. LEVEL INFLATION
   - Most Layer 1 classes placed in level_1+ but have NO same-layer dependencies
   - They should all be level_0 (infrastructure at the data layer)
   - Level inflation happens when files import cross-layer types

3. DUPLICATE DEFINITIONS
   - Same class names in multiple locations (AttachmentRules, SpawnContext, etc.)
   - May indicate copy-paste or unfinished refactoring
   - Should consolidate to single location

4. MISSING LAYER 2/3
   - No application or orchestration layer files found
   - This is intentional (domain + infrastructure only so far)
""")
