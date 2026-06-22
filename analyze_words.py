import re

def extract_words(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    words = re.findall(r'<span class="word">([^<]+)</span>', content)
    return [w.strip().lower() for w in words]

# Extract words from all existing KET/中考 files
ket_files = [
    'vocabulary/core-vocabulary-p1.html',
    'vocabulary/core-vocabulary-p2.html',
    'vocabulary/core-vocabulary-p3.html',
    'vocabulary/core-vocabulary-p4.html',
    'vocabulary/core-vocabulary-p5.html',
    'vocabulary/core-vocabulary-p6.html',
    'vocabulary/verbs-a-l.html',
    'vocabulary/verbs-m-z.html',
    'vocabulary/adjectives-adverbs.html',
    'vocabulary/nouns-life-scene.html',
    'vocabulary/nouns-society-function.html'
]

ket_words = set()
for f in ket_files:
    words = extract_words(f)
    ket_words.update(words)

print(f'Total unique KET/中考 words: {len(ket_words)}')

# Now extract PET and Gaokao words
pet_files = ['vocabulary2/pet-p1.html', 'vocabulary2/pet-p2.html', 'vocabulary2/pet-p3.html', 'vocabulary2/pet-p4.html']
gaokao_files = ['vocabulary2/gaokao-p1.html', 'vocabulary2/gaokao-p2.html', 'vocabulary2/gaokao-p3.html', 'vocabulary2/gaokao-p4.html']

pet_words = set()
for f in pet_files:
    words = extract_words(f)
    pet_words.update(words)

gaokao_words = set()
for f in gaokao_files:
    words = extract_words(f)
    gaokao_words.update(words)

# Words in PET that overlap with KET
pet_overlap = sorted(pet_words & ket_words)
print(f'\nPET words overlapping with KET/中考: {len(pet_overlap)}')
for w in pet_overlap:
    print(f'  {w}')

# Words in Gaokao that overlap with KET
gaokao_overlap = sorted(gaokao_words & ket_words)
print(f'\nGaokao words overlapping with KET/中考: {len(gaokao_overlap)}')
for w in gaokao_overlap:
    print(f'  {w}')

print(f'\nPET new (not in KET): {len(pet_words - ket_words)}')
print(f'Gaokao new (not in KET): {len(gaokao_words - ket_words)}')
print(f'PET total: {len(pet_words)}')
print(f'Gaokao total: {len(gaokao_words)}')