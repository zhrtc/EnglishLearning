# -*- coding: utf-8 -*-
import re
import os

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
    return words

def remove_ket_duplicates(html_file, ket_words):
    """Remove rows where the word exists in KET vocabulary"""
    with open(html_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Read entire file
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all <tr> blocks containing vocabulary rows
    # Each row is: <tr>\n<td><span class="word">WORD</span>...
    # We need to find rows where the word is in KET
    rows = re.findall(r'<tr>\n                    <td><span class="word">([^<]+)</span>.*?</tr>', content, re.DOTALL)
    
    removed_count = 0
    total_count = 0
    for row_match in re.finditer(r'<tr>(.*?)</tr>', content, re.DOTALL):
        row = row_match.group(0)
        word_match = re.search(r'<span class="word">([^<]+)</span>', row)
        if word_match:
            total_count += 1
            w = word_match.group(1).strip().lower()
            if w in ket_words:
                content = content.replace(row, '', 1)
                removed_count += 1
    
    # Fix duplicate newlines
    content = content.replace('\n\n\n', '\n\n')
    content = content.replace('\n                \n', '\n                \n')
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return removed_count, total_count - removed_count

print("Getting KET words...")
ket = get_ket_words()
print(f"KET has {len(ket)} unique words")

pet_files = ['vocabulary2/pet-p1.html', 'vocabulary2/pet-p2.html', 
             'vocabulary2/pet-p3.html', 'vocabulary2/pet-p4.html']
gaokao_files = ['vocabulary2/gaokao-p1.html', 'vocabulary2/gaokao-p2.html',
                'vocabulary2/gaokao-p3.html', 'vocabulary2/gaokao-p4.html']

for f in pet_files + gaokao_files:
    removed, remaining = remove_ket_duplicates(f, ket)
    print(f"{f}: removed {removed} KET words, {remaining} remaining")