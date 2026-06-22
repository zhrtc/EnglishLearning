import re

def get_ket_words():
    """Get all words from existing KET/中考 vocabulary"""
    files = [
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
    words = set()
    for f in files:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()
        found = re.findall(r'<span class="word">([^<]+)</span>', content)
        words.update([w.strip().lower() for w in found])
    return words

def create_page(title_prefix, subtitle, page_num, total_pages, prev_page, next_page, words_data, ket_words):
    """Generate a vocabulary HTML page filtering out KET words"""
    lines = []
    lines.append('<!DOCTYPE html>')
    lines.append('<html lang="zh-CN">')
    lines.append('<head>')
    lines.append('    <meta charset="UTF-8">')
    lines.append('    <meta name="referrer" content="same-origin">')
    lines.append(f'    <title>{title_prefix} - 第{page_num}页/共{total_pages}页</title>')
    lines.append('    <link rel="stylesheet" href="../css/common.css">')
    lines.append('    <script defer src="../js/common.js"></script>')
    lines.append('</head>')
    lines.append('<body>')
    lines.append('')
    lines.append('<div class="container">')
    lines.append(f'    <h1>{title_prefix} 速记表</h1>')
    lines.append(f'    <p style="text-align: center;">📖 {subtitle} | 第{page_num}页 / 共{total_pages}页</p>')
    lines.append('')
    lines.append('    <!-- 自测控制面板 -->')
    lines.append('    <div class="control-panel">')
    lines.append('        <button class="btn-toggle" id="btn-words"')
    lines.append('            onclick="toggleExam(\'hide-words\', \'btn-words\', \'单词\')">👁️ 隐藏单词</button>')
    lines.append('        <button class="btn-toggle" id="btn-inflections"')
    lines.append('            onclick="toggleExam(\'hide-inflections\', \'btn-inflections\', \'特殊变形\')">👁️ 隐藏变形</button>')
    lines.append('        <button class="btn-toggle" id="btn-meanings"')
    lines.append('            onclick="toggleExam(\'hide-meanings\', \'btn-meanings\', \'中文释义\')">👁️ 隐藏释义</button>')
    lines.append('        <button class="btn-toggle" id="btn-translations"')
    lines.append('            onclick="toggleExampleColumn(\'btn-translations\')">👁️ 隐藏翻译</button>')
    
    nav_buttons = []
    if prev_page:
        nav_buttons.append(f'<button class="btn-toggle btn-nav" onclick="window.location.href=\'{prev_page}\'">⬅ P{page_num-1}</button>')
    if next_page:
        nav_buttons.append(f'<button class="btn-toggle btn-nav" onclick="window.location.href=\'{next_page}\'">P{page_num+1} ➡</button>')
    nav_buttons.append('<button class="btn-toggle btn-nav" onclick="window.location.href=\'../index.html\'">🔙 返回</button>')
    
    for btn in nav_buttons:
        lines.append(f'        {btn}')
    
    lines.append('    </div>')
    lines.append('')
    lines.append('    <div id="vocabulary-content">')
    lines.append(f'        <h2>{"PET核心词汇" if "PET" in title_prefix else "高考核心词汇"} {"(非KET重复)" if page_num <= 4 else ""}</h2>')
    lines.append('        <table>')
    lines.append('            <thead>')
    lines.append('                <tr>')
    lines.append('                    <th style="width: 15%;">单词 & 音标</th>')
    lines.append('                    <th style="width: 20%;">特殊变形 / 提示</th>')
    lines.append('                    <th style="width: 25%;">中文释义</th>')
    lines.append('                    <th style="width: 40%;">典型例句</th>')
    lines.append('                </tr>')
    lines.append('            </thead>')
    lines.append('            <tbody>')
    
    count = 0
    for word, ipa, inflection, meaning, example, example_cn in words_data:
        w_lower = word.strip().lower()
        # Handle compound words like "many/much", "video game"
        w_clean = w_lower.split(' / ')[0].split(' /')[0].split('(')[0].strip()
        if w_clean in ket_words:
            continue  # Skip words already in KET
        count += 1
        lines.append('                <tr>')
        lines.append(f'                    <td><span class="word">{word}</span><br><span class="ipa">{ipa}</span></td>')
        lines.append(f'                    <td class="inflection">{inflection}</td>')
        lines.append(f'                    <td class="meaning">{meaning}</td>')
        lines.append(f'                    <td>')
        lines.append(f'                        <span class="example">{example}</span>')
        lines.append(f'                        <span class="example-cn">{example_cn}</span>')
        lines.append(f'                    </td>')
        lines.append('                </tr>')
    
    lines.append('            </tbody>')
    lines.append('        </table>')
    lines.append('        ')
    lines.append('    </div>')
    lines.append('</div>')
    lines.append('')
    lines.append('</body>')
    lines.append('</html>')
    
    return '\n'.join(lines), count

print("Script loaded - ready to use")
print("KET words will be loaded at runtime")