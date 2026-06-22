# -*- coding: utf-8 -*-
import re

def get_ket_words():
    files = [
        'vocabulary/core-vocabulary-p1.html','vocabulary/core-vocabulary-p2.html',
        'vocabulary/core-vocabulary-p3.html','vocabulary/core-vocabulary-p4.html',
        'vocabulary/core-vocabulary-p5.html','vocabulary/core-vocabulary-p6.html',
        'vocabulary/verbs-a-l.html','vocabulary/verbs-m-z.html',
        'vocabulary/adjectives-adverbs.html','vocabulary/nouns-life-scene.html',
        'vocabulary/nouns-society-function.html'
    ]
    words = set()
    for f in files:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()
        found = re.findall(r'<span class="word">([^<]+)</span>', content)
        for w in found:
            w = w.strip().lower()
            words.add(w)
    # Handle compound words like "many/much", "waiter / waitress", "video game"
    expanded = set()
    for w in words:
        expanded.add(w)
        if ' / ' in w:
            for part in w.split(' / '):
                expanded.add(part.strip())
    return expanded

def process_file(filepath, ket_words):
    """Read file, remove rows with KET words, rewrite file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into lines for processing
    lines = content.split('\n')
    
    # Identify row boundaries
    new_lines = []
    in_row = False
    row_lines = []
    row_word = None
    kept = 0
    removed = 0
    
    for line in lines:
        if '<tr>' in line and not in_row:
            in_row = True
            row_lines = [line]
            row_word = None
            # Check if word is on the same line as <tr>
            wm = re.search(r'<span class="word">([^<]+)</span>', line)
            if wm:
                row_word = wm.group(1).strip().lower()
        elif in_row:
            row_lines.append(line)
            if not row_word:
                wm = re.search(r'<span class="word">([^<]+)</span>', line)
                if wm:
                    row_word = wm.group(1).strip().lower()
            if '</tr>' in line:
                # End of row - decide whether to keep
                keep = True
                if row_word:
                    # Check if word or any of its parts is in KET
                    parts = [row_word]
                    if ' / ' in row_word:
                        parts = [p.strip() for p in row_word.split(' / ')]
                    for p in parts:
                        if p in ket_words:
                            keep = False
                            break
                if keep:
                    new_lines.extend(row_lines)
                    kept += 1
                else:
                    removed += 1
                in_row = False
                row_lines = []
                row_word = None
        else:
            new_lines.append(line)
    
    # Write back
    result = '\n'.join(new_lines)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)
    
    return removed, kept

print("Getting KET words...")
ket = get_ket_words()
print(f"KET has {len(ket)} unique words (including expanded)")

pet_files = ['vocabulary2/pet-p1.html', 'vocabulary2/pet-p2.html', 
             'vocabulary2/pet-p3.html', 'vocabulary2/pet-p4.html']
gaokao_files = ['vocabulary2/gaokao-p1.html', 'vocabulary2/gaokao-p2.html',
                'vocabulary2/gaokao-p3.html', 'vocabulary2/gaokao-p4.html']

total_removed = 0
total_kept = 0

for f in pet_files + gaokao_files:
    removed, kept = process_file(f, ket)
    total_removed += removed
    total_kept += kept
    print(f"{f}: removed {removed} KET duplicates, kept {kept}")

print(f"\nTotal: removed {total_removed}, kept {total_kept}")

# Also count unique words remaining
all_remaining = set()
for f in pet_files + gaokao_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    found = re.findall(r'<span class="word">([^<]+)</span>', content)
    for w in found:
        all_remaining.add(w.strip().lower())

print(f"Total unique remaining words across all files: {len(all_remaining)}")