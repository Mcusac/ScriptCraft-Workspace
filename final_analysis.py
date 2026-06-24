import os
import re
from pathlib import Path
from collections import defaultdict

base_path = Path('implementations/minecraft/AlienCraft/weyland-yutani-core/src/main/java/com/weylandyutani')

# Comprehensive analysis of ALL layers
all_files_by_layer = defaultdict(lambda: defaultdict(list))
misplaced_files = []

for java_file in sorted(base_path.rglob('*.java')):
    rel_str = str(java_file.relative_to(base_path)).replace('\\', '/')
    parts = rel_str.split('/')
    
    if len(parts) < 2:
        continue
    
    layer = parts[0]
    level_part = parts[1]
    
    # Skip if not a level directory
    if not level_part.startswith('level_'):
        continue
    
    level_num = int(level_part.split('_')[1])
    classname = java_file.stem
    
    try:
        with open(java_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue
    
    # Extract package
    pkg_match = re.search(r'package\s+([\w\.]+);', content)
    package = pkg_match.group(1) if pkg_match else ''
    
    # Find all imports within same layer
    all_imports = re.findall(r'import\s+com\.weylandyutani\.([^\s;]+);', content)
    
    # Categorize imports
    same_layer_imports = [imp for imp in all_imports if imp.startswith(layer + '/')]
    cross_layer_imports = [imp for imp in all_imports if any(imp.startswith(f'layer_{i}_') for i in range(4)) and not imp.startswith(layer + '/')]
    
    # Calculate required level based on same-layer dependencies
    required_level = 0
    if same_layer_imports:
        max_imported_level = 0
        for imp in same_layer_imports:
            match = re.search(r'/level_(\d+)/', imp)
            if match:
                max_imported_level = max(max_imported_level, int(match.group(1)))
        required_level = max_imported_level + 1
    
    file_info = {
        'classname': classname,
        'file': java_file.name,
        'path': rel_str,
        'package': package,
        'actual_level': level_num,
        'required_level': required_level,
        'correct': required_level == level_num,
        'same_layer_imports': same_layer_imports,
        'cross_layer_imports': cross_layer_imports,
    }
    
    all_files_by_layer[layer][level_num].append(file_info)
    
    # Track misplaced files
    if not file_info['correct'] and classname != 'package-info':
        misplaced_files.append((layer, level_num, required_level, classname, rel_str))

# Print comprehensive analysis
print("=" * 90)
print("LAYER 0 DOMAIN - COMPLETE ANALYSIS")
print("=" * 90)

layer_0_stats = {'correct': 0, 'wrong': 0}
for level_num in sorted(all_files_by_layer['layer_0_domain'].keys()):
    files = all_files_by_layer['layer_0_domain'][level_num]
    correct = sum(1 for f in files if f['correct'])
    wrong = sum(1 for f in files if not f['correct'])
    
    print(f"\nlevel_{level_num}: {len(files)} files ({correct} correct, {wrong} wrong)")
    
    # Show misplaced files
    misplaced = [f for f in files if not f['correct']]
    for f in sorted(misplaced, key=lambda x: x['file'])[:10]:
        if 'package-info' not in f['file']:
            print(f"  [XX] {f['file']:40} -> level_{f['required_level']}")
            if f['cross_layer_imports']:
                print(f"       crosses to: {f['cross_layer_imports'][0]}")
    
    layer_0_stats['correct'] += correct
    layer_0_stats['wrong'] += wrong

print(f"\nLayer 0 Domain TOTAL: {layer_0_stats['correct']} correct, {layer_0_stats['wrong']} wrong")
print(f"  Correctness: {100*layer_0_stats['correct']/(layer_0_stats['correct']+layer_0_stats['wrong']):.0f}%")

print("\n" + "=" * 90)
print("LAYER 1 INFRASTRUCTURE - COMPLETE ANALYSIS")
print("=" * 90)

layer_1_stats = {'correct': 0, 'wrong': 0}
for level_num in sorted(all_files_by_layer['layer_1_infrastructure'].keys()):
    files = all_files_by_layer['layer_1_infrastructure'][level_num]
    correct = sum(1 for f in files if f['correct'])
    wrong = sum(1 for f in files if not f['correct'])
    
    print(f"\nlevel_{level_num}: {len(files)} files ({correct} correct, {wrong} wrong)")
    
    # Show misplaced files (excluding package-info for cleaner output)
    misplaced = [f for f in files if not f['correct'] and 'package-info' not in f['file']]
    for f in sorted(misplaced, key=lambda x: x['file'])[:8]:
        print(f"  [XX] {f['file']:40} -> level_{f['required_level']}")
    
    if len(misplaced) > 8:
        print(f"  ... and {len(misplaced)-8} more")
    
    layer_1_stats['correct'] += correct
    layer_1_stats['wrong'] += wrong

print(f"\nLayer 1 Infrastructure TOTAL: {layer_1_stats['correct']} correct, {layer_1_stats['wrong']} wrong")
print(f"  Correctness: {100*layer_1_stats['correct']/(layer_1_stats['correct']+layer_1_stats['wrong']):.0f}%")

# Analyze higher layers
print("\n" + "=" * 90)
print("LAYER 2 SYSTEMS - COMPLETE ANALYSIS")
print("=" * 90)

layer_2_exists = len(all_files_by_layer['layer_2_systems']) > 0
if layer_2_exists:
    layer_2_stats = {'correct': 0, 'wrong': 0}
    for level_num in sorted(all_files_by_layer['layer_2_systems'].keys()):
        files = all_files_by_layer['layer_2_systems'][level_num]
        correct = sum(1 for f in files if f['correct'])
        wrong = sum(1 for f in files if not f['correct'])
        
        print(f"\nlevel_{level_num}: {len(files)} files ({correct} correct, {wrong} wrong)")
        
        misplaced = [f for f in files if not f['correct'] and 'package-info' not in f['file']]
        for f in sorted(misplaced, key=lambda x: x['file'])[:5]:
            print(f"  [XX] {f['file']:40} -> level_{f['required_level']}")
        
        layer_2_stats['correct'] += correct
        layer_2_stats['wrong'] += wrong
    
    print(f"\nLayer 2 Systems TOTAL: {layer_2_stats['correct']} correct, {layer_2_stats['wrong']} wrong")
    if layer_2_stats['correct'] + layer_2_stats['wrong'] > 0:
        print(f"  Correctness: {100*layer_2_stats['correct']/(layer_2_stats['correct']+layer_2_stats['wrong']):.0f}%")
else:
    print("Layer 2 Systems: NOT FOUND")

print("\n" + "=" * 90)
print("LAYER 3 MINECRAFT - COMPLETE ANALYSIS")
print("=" * 90)

layer_3_exists = len(all_files_by_layer['layer_3_minecraft']) > 0
if layer_3_exists:
    layer_3_stats = {'correct': 0, 'wrong': 0}
    for level_num in sorted(all_files_by_layer['layer_3_minecraft'].keys()):
        files = all_files_by_layer['layer_3_minecraft'][level_num]
        correct = sum(1 for f in files if f['correct'])
        wrong = sum(1 for f in files if not f['correct'])
        
        print(f"\nlevel_{level_num}: {len(files)} files ({correct} correct, {wrong} wrong)")
        
        misplaced = [f for f in files if not f['correct'] and 'package-info' not in f['file']]
        for f in sorted(misplaced, key=lambda x: x['file'])[:5]:
            print(f"  [XX] {f['file']:40} -> level_{f['required_level']}")
        
        layer_3_stats['correct'] += correct
        layer_3_stats['wrong'] += wrong
    
    print(f"\nLayer 3 Minecraft TOTAL: {layer_3_stats['correct']} correct, {layer_3_stats['wrong']} wrong")
    if layer_3_stats['correct'] + layer_3_stats['wrong'] > 0:
        print(f"  Correctness: {100*layer_3_stats['correct']/(layer_3_stats['correct']+layer_3_stats['wrong']):.0f}%")
else:
    print("Layer 3 Minecraft: NOT FOUND")

# Summary of misplaced files needing relocation
print("\n" + "=" * 90)
print("CRITICAL: FILES NEEDING RELOCATION")
print("=" * 90)

# Group by layer
misplaced_by_layer = defaultdict(list)
for layer, actual, required, classname, path in misplaced_files:
    if classname != 'package-info':
        misplaced_by_layer[layer].append((actual, required, classname, path))

for layer in ['layer_0_domain', 'layer_1_infrastructure', 'layer_2_systems', 'layer_3_minecraft']:
    if misplaced_by_layer[layer]:
        print(f"\n{layer}: {len(misplaced_by_layer[layer])} files")
        print("-" * 90)
        for actual, required, classname, path in sorted(misplaced_by_layer[layer])[:10]:
            print(f"  {classname:40} level_{actual} -> level_{required}")
        if len(misplaced_by_layer[layer]) > 10:
            print(f"  ... and {len(misplaced_by_layer[layer])-10} more")

total_misplaced = sum(len(v) for v in misplaced_by_layer.values())
print(f"\nTOTAL MISPLACED: {total_misplaced} files")

# Dependencies summary
print("\n" + "=" * 90)
print("CROSS-LAYER DEPENDENCY PATTERNS")
print("=" * 90)

cross_layer_patterns = defaultdict(int)
for layer in all_files_by_layer:
    for level_num in all_files_by_layer[layer]:
        for f in all_files_by_layer[layer][level_num]:
            if f['cross_layer_imports']:
                for imp in f['cross_layer_imports']:
                    target_layer = imp.split('/')[0]
                    key = f"{layer} -> {target_layer}"
                    cross_layer_patterns[key] += 1

print("\nDependency directions:")
for key in sorted(cross_layer_patterns.keys()):
    print(f"  {key}: {cross_layer_patterns[key]} references")
