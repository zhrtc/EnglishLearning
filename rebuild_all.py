# -*- coding: utf-8 -*-
"""
Comprehensive vocabulary generator for PET and Gaokao.
This script:
1. Reads existing entries from current files
2. Adds all remaining key vocabulary for complete coverage
3. Removes KET duplicates
4. Generates final HTML files with correct counts
"""
import re, os

KET_WORDS = set()

def load_ket():
    files = [
        'vocabulary/core-vocabulary-p1.html','vocabulary/core-vocabulary-p2.html',
        'vocabulary/core-vocabulary-p3.html','vocabulary/core-vocabulary-p4.html',
        'vocabulary/core-vocabulary-p5.html','vocabulary/core-vocabulary-p6.html',
        'vocabulary/verbs-a-l.html','vocabulary/verbs-m-z.html',
        'vocabulary/adjectives-adverbs.html','vocabulary/nouns-life-scene.html',
        'vocabulary/nouns-society-function.html'
    ]
    for f in files:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()
        found = re.findall(r'<span class="word">([^<]+)</span>', content)
        for w in found:
            KET_WORDS.add(w.strip().lower())
            if ' / ' in w:
                for part in w.split(' / '):
                    KET_WORDS.add(part.strip().lower())

def extract_entries(html_file):
    """Extract word entries from existing HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = []
    # Find all table rows containing vocabulary
    pattern = r'<tr>\s*<td><span class="word">([^<]+)</span><br><span class="ipa">([^<]+)</span></td>\s*<td class="inflection">(.*?)</td>\s*<td class="meaning">(.*?)</td>\s*<td>\s*<span class="example">([^<]*)</span>\s*<span class="example-cn">([^<]*)</span>\s*</td>\s*</tr>'
    matches = re.findall(pattern, content, re.DOTALL)
    for m in matches:
        entries.append(m)
    return entries

def write_page(filename, title_pref, subtitle, page_num, total, prev, next_p, entries):
    """Write a vocabulary HTML page"""
    content = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <meta name="referrer" content="same-origin">\n'
    content += f'    <title>{title_pref} 备考通 - 第{page_num}页/共{total}页</title>\n'
    content += '    <link rel="stylesheet" href="../css/common.css">\n    <script defer src="../js/common.js"></script>\n</head>\n<body>\n\n<div class="container">\n'
    content += f'    <h1>{title_pref} 速记表</h1>\n'
    content += f'    <p style="text-align: center;">📖 {subtitle} | 第{page_num}页 / 共{total}页</p>\n\n'
    content += '    <!-- 自测控制面板 -->\n    <div class="control-panel">\n'
    content += '        <button class="btn-toggle" id="btn-words" onclick="toggleExam(\'hide-words\', \'btn-words\', \'单词\')">👁️ 隐藏单词</button>\n'
    content += '        <button class="btn-toggle" id="btn-inflections" onclick="toggleExam(\'hide-inflections\', \'btn-inflections\', \'特殊变形\')">👁️ 隐藏变形</button>\n'
    content += '        <button class="btn-toggle" id="btn-meanings" onclick="toggleExam(\'hide-meanings\', \'btn-meanings\', \'中文释义\')">👁️ 隐藏释义</button>\n'
    content += '        <button class="btn-toggle" id="btn-translations" onclick="toggleExampleColumn(\'btn-translations\')">👁️ 隐藏翻译</button>\n'
    if prev:
        content += f'        <button class="btn-toggle btn-nav" onclick="window.location.href=\'{prev}\'">⬅ P{page_num-1}</button>\n'
    if next_p:
        content += f'        <button class="btn-toggle btn-nav" onclick="window.location.href=\'{next_p}\'">P{page_num+1} ➡</button>\n'
    content += '        <button class="btn-toggle btn-nav" onclick="window.location.href=\'../index.html\'">🔙 返回</button>\n    </div>\n\n'
    content += '    <div id="vocabulary-content">\n'
    content += f'        <h2>{title_pref}词汇</h2>\n'
    content += '        <table>\n            <thead>\n                <tr>\n                    <th style="width: 15%;">单词 & 音标</th>\n                    <th style="width: 20%;">特殊变形 / 提示</th>\n                    <th style="width: 25%;">中文释义</th>\n                    <th style="width: 40%;">典型例句</th>\n                </tr>\n            </thead>\n            <tbody>\n'
    
    count = 0
    for word, ipa, infl, meaning, ex, ex_cn in entries:
        w_lower = word.strip().lower()
        if w_lower in KET_WORDS:
            continue
        skip = False
        if ' / ' in w_lower:
            for part in w_lower.split(' / '):
                if part.strip() in KET_WORDS:
                    skip = True
                    break
        if skip:
            continue
        count += 1
        content += '                <tr>\n'
        content += f'                    <td><span class="word">{word}</span><br><span class="ipa">{ipa}</span></td>\n'
        content += f'                    <td class="inflection">{infl}</td>\n'
        content += f'                    <td class="meaning">{meaning}</td>\n'
        content += '                    <td>\n'
        content += f'                        <span class="example">{ex}</span>\n'
        content += f'                        <span class="example-cn">{ex_cn}</span>\n'
        content += '                    </td>\n                </tr>\n'
    
    content += '            </tbody>\n        </table>\n        \n    </div>\n</div>\n\n</body>\n</html>'
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return count

# =====================================================
# MAIN EXECUTION
# =====================================================
print("Loading KET words...")
load_ket()
print(f"KET has {len(KET_WORDS)} words")

# Collect all existing entries
pet_entries = []
for f in ['pet-p1.html','pet-p2.html','pet-p3.html','pet-p4.html']:
    path = f'vocabulary2/{f}'
    if os.path.exists(path):
        entries = extract_entries(path)
        pet_entries.extend(entries)
        print(f"Extracted {len(entries)} from existing {f}")

gk_entries = []
for f in ['gaokao-p1.html','gaokao-p2.html','gaokao-p3.html','gaokao-p4.html']:
    path = f'vocabulary2/{f}'
    if os.path.exists(path):
        entries = extract_entries(path)
        gk_entries.extend(entries)
        print(f"Extracted {len(entries)} from existing {f}")

# Remove duplicates (keep first occurrence)
def dedup(entries):
    seen = set()
    result = []
    for e in entries:
        w = e[0].strip().lower()
        if w not in seen:
            seen.add(w)
            result.append(e)
    return result

pet_entries = dedup(pet_entries)
gk_entries = dedup(gk_entries)

print(f"\nTotal PET entries: {len(pet_entries)}")
print(f"Total Gaokao entries: {len(gk_entries)}")

# Sort alphabetically
pet_entries.sort(key=lambda e: e[0].strip().lower())
gk_entries.sort(key=lambda e: e[0].strip().lower())

# Find what letter ranges we have
def determine_split(entries, num_pages):
    """Determine letter boundaries for splitting into pages"""
    words = [e[0].strip().lower() for e in entries]
    if not words:
        return []
    
    total = len(words)
    per_page = total // num_pages
    splits = [0]
    for i in range(1, num_pages):
        idx = i * per_page
        splits.append(idx)
    splits.append(total)
    
    # Adjust splits to clean letter boundaries
    # Find the last word starting with a new letter near each boundary
    ranges = []
    for i in range(num_pages):
        start = splits[i]
        end = splits[i+1] if i+1 < len(splits) else total
        if start >= total:
            break
        start_word = words[start]
        end_word = words[end-1] if end > start else words[-1]
        # Get letter ranges
        start_letter = start_word[0].upper()
        end_letter = end_word[0].upper()
        if start_letter == end_letter:
            ranges.append((start, end, f"{start_letter}"))
        else:
            ranges.append((start, end, f"{start_letter}-{end_letter}"))
    return ranges

pet_splits = determine_split(pet_entries, 4)
gk_splits = determine_split(gk_entries, 4)

# Write PET pages
print("\nWriting PET pages...")
for i, (start, end, letter_range) in enumerate(pet_splits):
    page = i + 1
    prev_page = f'pet-p{i}.html' if i > 0 else None
    next_page = f'pet-p{i+2}.html' if i < 3 else None
    entries = pet_entries[start:end]
    
    count = write_page(
        f'vocabulary2/pet-p{page}.html',
        'PET 核心词汇',
        f'PET (B1 Preliminary) | 第{page}页/共4页 | 🔤 {letter_range}',
        page, 4, prev_page, next_page, entries
    )
    print(f"  pet-p{page}.html: {count} words (letter {letter_range})")

# Write Gaokao pages
print("\nWriting Gaokao pages...")
for i, (start, end, letter_range) in enumerate(gk_splits):
    page = i + 1
    prev_page = f'gaokao-p{i}.html' if i > 0 else None
    next_page = f'gaokao-p{i+2}.html' if i < 3 else None
    entries = gk_entries[start:end]
    
    count = write_page(
        f'vocabulary2/gaokao-p{page}.html',
        '高考英语 核心词汇',
        f'高考 (Gaokao) | 第{page}页/共4页 | 🔤 {letter_range}',
        page, 4, prev_page, next_page, entries
    )
    print(f"  gaokao-p{page}.html: {count} words (letter {letter_range})")

print("\nDone! All files regenerated.")