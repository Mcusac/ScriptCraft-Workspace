import os
import re
from pathlib import Path
from collections import defaultdict

base_path = Path('implementations/minecraft/AlienCraft/weyland-yutani-core/src/main/java/com/weylandyutani')

# First pass: collect all files and their packages
file_packages = {}
for java_file in base_path.rglob('*.java'):
    rel_str = str(java_file.relative_to(base_path)).replace('\\', '/')
    try:
        with open(java_file, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'package\s+([\w\.]+);', content)
            if match:
                file_packages[java_file] = match.group(1)
    except:
        pass

# Second pass: analyze dependencies in detail
layer_0_files = defaultdict(list)
layer_1_files = defaultdict(list)

for java_file in sorted(base_path.rglob('*.java')):
    rel_str = str(java_file.relative_to(base_path)).replace('\\', '/')
    parts = rel_str.split('/')
    
    if len(parts) < 2 or not parts[1].startswith('level_'):
        continue
    
    layer = parts[0]
    level = parts[1]
    level_num = int(level.split('_')[1])
    classname = java_file.stem
    
    try:
        with open(java_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue
    
    # Extract package
    pkg_match = re.search(r'package\s+([\w\.]+);', content)
    package = pkg_match.group(1) if pkg_match else ''
    
    # Find all imports
    all_imports = re.findall(r'import\s+com\.weylandyutani\.([^\s;]+);', content)
    
    # Categorize: same-layer vs cross-layer
    same_layer_imports = []
    cross_layer_imports = []
    
    for imp in all_imports:
        # Format: layer_X_name/level_Y/...
        if imp.startswith(layer + '/'):
            same_layer_imports.append(imp)
        elif imp.startswith('layer_'):
            cross_layer_imports.append(imp)
    
    # Calculate required level
    required_level = 0
    if same_layer_imports:
        max_imported_level = 0
        for imp in same_layer_imports:
            match = re.search(r'/level_(\d+)/', imp)
            if match:
                max_imported_level = max(max_imported_level, int(match.group(1)))
        required_level = max_imported_level + 1
    
    file_info = {
        'file': java_file.name,
        'path': rel_str,
        'package': package,
        'actual_level': level_num,
        'required_level': required_level,
        'correct': required_level == level_num,
        'same_layer': same_layer_imports,
        'cross_layer': cross_layer_imports,
    }
    
    if layer == 'layer_0_domain':
        layer_0_files[level_num].append(file_info)
    elif layer == 'layer_1_infrastructure':
        layer_1_files[level_num].append(file_info)

print("=" * 80)
print("LAYER 0 DOMAIN - DEPENDENCY ANALYSIS")
print("=" * 80)

layer_0_summary = {0: {'correct': 0, 'wrong': 0}, 1: {'correct': 0, 'wrong': 0}, 2: {'correct': 0, 'wrong': 0}}

for level_num in sorted(layer_0_files.keys()):
    files = layer_0_files[level_num]
    print(f"\nlevel_{level_num}: {len(files)} files")
    print("-" * 80)
    
    for f in sorted(files, key=lambda x: x['file']):
        status = "[OK]" if f['correct'] else "[XX]"
        print(f"{status} {f['file']:40} actual=level_{f['actual_level']} required=level_{f['required_level']}")
        
        if f['same_layer']:
            max_shown = min(3, len(f['same_layer']))
            for i, imp in enumerate(f['same_layer'][:max_shown]):
                prefix = "   " if i < max_shown - 1 else "   "
                print(f"{prefix} -> {imp}")
            if len(f['same_layer']) > 3:
                print(f"   ... and {len(f['same_layer'])-3} more")
        
        if f['cross_layer']:
            print(f"   [X-LAYER] {f['cross_layer'][0]}")
        
        if f['correct']:
            layer_0_summary[level_num]['correct'] += 1
        else:
            layer_0_summary[level_num]['wrong'] += 1

print("\nLayer 0 Domain Summary:")
for level_num in sorted(layer_0_summary.keys()):
    correct = layer_0_summary[level_num]['correct']
    wrong = layer_0_summary[level_num]['wrong']
    if correct + wrong > 0:
        pct = 100 * correct / (correct + wrong)
        print(f"  level_{level_num}: {correct}/{correct+wrong} correct ({pct:.0f}%)")

print("\n" + "=" * 80)
print("LAYER 1 INFRASTRUCTURE - DEPENDENCY ANALYSIS")
print("=" * 80)

layer_1_summary = {0: {'correct': 0, 'wrong': 0}, 1: {'correct': 0, 'wrong': 0}, 2: {'correct': 0, 'wrong': 0}, 3: {'correct': 0, 'wrong': 0}, 4: {'correct': 0, 'wrong': 0}}

for level_num in sorted(layer_1_files.keys()):
    files = layer_1_files[level_num]
    print(f"\nlevel_{level_num}: {len(files)} files")
    print("-" * 80)
    
    for f in sorted(files, key=lambda x: x['file']):
        status = "[OK]" if f['correct'] else "[XX]"
        print(f"{status} {f['file']:40} actual=level_{f['actual_level']} required=level_{f['required_level']}")
        
        if f['same_layer']:
            max_shown = min(2, len(f['same_layer']))
            for imp in f['same_layer'][:max_shown]:
                print(f"   -> {imp}")
            if len(f['same_layer']) > 2:
                print(f"   ... and {len(f['same_layer'])-2} more")
        
        if f['correct']:
            if level_num not in layer_1_summary:
                layer_1_summary[level_num] = {'correct': 0, 'wrong': 0}
            layer_1_summary[level_num]['correct'] += 1
        else:
            if level_num not in layer_1_summary:
                layer_1_summary[level_num] = {'correct': 0, 'wrong': 0}
            layer_1_summary[level_num]['wrong'] += 1

print("\nLayer 1 Infrastructure Summary:")
total_correct = 0
total_wrong = 0
for level_num in sorted(layer_1_summary.keys()):
    correct = layer_1_summary[level_num]['correct']
    wrong = layer_1_summary[level_num]['wrong']
    total_correct += correct
    total_wrong += wrong
    if correct + wrong > 0:
        pct = 100 * correct / (correct + wrong)
        print(f"  level_{level_num}: {correct}/{correct+wrong} correct ({pct:.0f}%)")

print(f"\n  TOTAL: {total_correct}/{total_correct+total_wrong} correct ({100*total_correct/(total_correct+total_wrong):.0f}%)")

print("\n" + "=" * 80)
print("FILES NEEDING RELOCATION")
print("=" * 80)

misplaced = []
for level_num in sorted(layer_0_files.keys()):
    for f in layer_0_files[level_num]:
        if not f['correct']:
            misplaced.append(('layer_0_domain', level_num, f['required_level'], f['file'], f['path']))

for level_num in sorted(layer_1_files.keys()):
    for f in layer_1_files[level_num]:
        if not f['correct']:
            misplaced.append(('layer_1_infrastructure', level_num, f['required_level'], f['file'], f['path']))

for layer, actual, required, fname, path in sorted(misplaced, key=lambda x: (x[0], x[1])):
    print(f"{fname:40} {layer}/level_{actual} -> {layer}/level_{required}")

print(f"\nTotal files needing relocation: {len(misplaced)}")
