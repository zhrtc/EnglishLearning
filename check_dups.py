import re

def extract_words(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    words = re.findall(r'<span class="word">([^<]+)</span>', content)
    return words

pet_files = ['vocabulary2/pet-p1.html', 'vocabulary2/pet-p2.html', 'vocabulary2/pet-p3.html', 'vocabulary2/pet-p4.html']
gaokao_files = ['vocabulary2/gaokao-p1.html', 'vocabulary2/gaokao-p2.html', 'vocabulary2/gaokao-p3.html', 'vocabulary2/gaokao-p4.html']

all_pet_words = {}
for f in pet_files:
    words = extract_words(f)
    all_pet_words[f] = [w.strip().lower() for w in words]
    print(f'{f}: {len(words)} words')

# Check duplicates within PET
pet_all = []
for words in all_pet_words.values():
    pet_all.extend(words)
pet_dups = set([w for w in pet_all if pet_all.count(w) > 1])
if pet_dups:
    print(f'Duplicates within PET: {pet_dups}')
else:
    print('No duplicates within PET')

all_gaokao_words = {}
for f in gaokao_files:
    words = extract_words(f)
    all_gaokao_words[f] = [w.strip().lower() for w in words]
    print(f'{f}: {len(words)} words')

gaokao_all = []
for words in all_gaokao_words.values():
    gaokao_all.extend(words)
gaokao_dups = set([w for w in gaokao_all if gaokao_all.count(w) > 1])
if gaokao_dups:
    print(f'Duplicates within Gaokao: {gaokao_dups}')
else:
    print('No duplicates within Gaokao')

pet_set = set(pet_all)
gaokao_set = set(gaokao_all)
overlap = pet_set & gaokao_set
print(f'Overlap between PET and Gaokao: {len(overlap)} words')
for w in sorted(overlap):
    print(f'  {w}')

print(f'\nPET unique words: {len(pet_set)}')
print(f'Gaokao unique words: {len(gaokao_set)}')