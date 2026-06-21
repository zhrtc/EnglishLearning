# English Learning Website - Agent Instructions

## About This Project
KET + 中考英语学习网站，包含词汇表和语法考点专项页面。
所有页面使用 `css/common.css` + `js/common.js` 作为公共资源。

## Service Worker Version Management

### ⚠️ Critical Rule: Always increment SW version when modifying files

When you make ANY changes to HTML/CSS/JS files that are served to users, you MUST update the SW version.

The version variable is located in:
- **File:** `js/common.js`
- **Line:** `var _SW_VERSION = 'YYYY-MM-DD-NN';`
- **Format:** `YYYY-MM-DD-NN` where NN is a sequential number (01, 02, 03...)

### When to Increment
- ✅ Modified any `.html` file (vocabulary or grammar pages)
- ✅ Modified `css/common.css` or `css/grammar.css`
- ✅ Modified `js/common.js`
- ✅ Added new pages (need to add to SW precache list)
- ✅ Modified `sw.js` itself
- ❌ NO need to change if editing only non-served files like this `CLAUDE.md`

### How to Increment
1. Open `js/common.js`
2. Find `_SW_VERSION` 
3. Increment the date or sequence number
   - Same day, multiple edits: `2026-06-21-01` → `2026-06-21-02`
   - Next day: `2026-06-22-01`

### Adding New Pages
If you add a new HTML page, also add it to the `PRECACHE_URLS` array in `sw.js`:
```javascript
const PRECACHE_URLS = [
  // ... existing entries ...
  '/grammar/new-page.html',  // <-- ADD HERE
];
```

### Why This Matters
The Service Worker uses **Stale-While-Revalidate** strategy:
- Old cached content is shown instantly on first visit after update
- Background fetch updates the cache
- When content changes are detected, the page auto-refreshes to show new version
- The version query param (`?v=...`) ensures the SW script itself is refreshed

## File Structure
```
📁 EnglishLearning/
├── 📄 index.html              # 主导航页面（分类入口）
├── 📄 sw.js                   # Service Worker（离线支持）
├── 📄 js/common.js            # 公共 JavaScript（SW注册、自测切换、滚动保存、TTS）
├── 📁 css/
│   ├── common.css             # 公共样式
│   └── grammar.css            # 语法页面卡片样式
├── 📁 grammar/                # 语法与考点专项（22 页）
├── 📁 vocabulary/             # 词汇分类表（11 页）
│   ├── core-vocabulary-p1.html  # 原版核心 P1（核心动词·人物·家庭·学校·食物）
│   ├── core-vocabulary-p2.html  # P2（时间·交通·描述·运动·健康·工作）
│   ├── core-vocabulary-p3.html  # P3（家居·购物·自然·科技·副词·介词）
│   ├── core-vocabulary-p4.html  # P4（代词·动作·数量·社交·抽象·心理）
│   ├── core-vocabulary-p5.html  # P5（城镇·日用品·语法词·地理·量词）
│   ├── core-vocabulary-p6.html  # P6（情感·方位·程度·媒体·连接词）
│   ├── verbs-a-l.html           # 动词 A-L
│   ├── verbs-m-z.html           # 动词 M-Z
│   ├── adjectives-adverbs.html   # 形容词与副词
│   ├── nouns-life-scene.html    # 生活与场景名词
│   └── nouns-society-function.html # 社会与功能词
└── 📁 grammar/                ← 22 grammar topic pages
    ├── tenses.html              # 八大时态
    ├── passive-voice.html       # 被动语态
    ├── articles.html            # 冠词
    ├── comparatives.html        # 比较级与最高级
    ├── pronouns.html            # 代词
    ├── questions.html           # 疑问句
    ├── numerals.html            # 数词
    ├── conjunctions.html        # 连词
    ├── word-formation.html      # 构词法
    ├── verb-collocations.html   # 动词固定搭配
    ├── prepositions.html        # 介词
    ├── confusable-words.html    # 易混词辨析
    ├── clauses.html             # 三大从句
    ├── non-finite-verbs.html    # 非谓语动词
    ├── modal-verbs.html         # 情态动词与虚拟语气
    ├── sentence-patterns.html   # 特殊句型
    ├── subject-verb-agreement.html # 主谓一致
    ├── direct-indirect-speech.html # 直接/间接引语
    ├── writing-connectors.html  # 写作连接词
    ├── countable-uncountable.html # 🔢 可数与不可数名词
    ├── quantifiers.html         # 📊 量词与限定词
    └── functional-english.html  # 💬 功能英语·情景交际
```

## Common Patterns

### All Pages Include
```html
<link rel="stylesheet" href="css/common.css">
<link rel="stylesheet" href="css/grammar.css">  <!-- grammar pages only -->
<script defer src="js/common.js"></script>
```

### Control Panel (vocabulary pages)
```html
<div class="control-panel">
  <button onclick="toggleExam(...)">👁️ 隐藏释义</button>
  <button onclick="toggleExampleColumn('btn-translations')">👁️ 隐藏翻译</button>
  <button onclick="window.location.href='index.html'">🔙 返回</button>
</div>
```

### Grammar Cards (grammar pages)
Use `grammar.css` classes:
- `.grammar-hero` - Purple gradient banner
- `.study-card` - White card with shadow
- `.card-grid / .card-grid-2 / .card-grid-1` - Responsive grid
- `.formula-box` - Dark terminal-style syntax
- `.rule / .rule.warn / .rule.success` - Info blocks
- `.example / .example-cn` - Example sentences
- `.mini-table` - Compact data table
- `.compare-row / .compare-col` - Side-by-side comparison
- `.tip-box / .tip-box.warn` - Tips and warnings

### TTS (Text-to-Speech)
Elements with classes `.word`, `.inflection`, `.example`, `.rule`, `.mini-table td`, `.compare-col .ex`, `.formula-box` are automatically made clickable for pronunciation if they contain English text (a-zA-Z). Pure Chinese elements are skipped.

### Scroll Position
Saved every 3 seconds to localStorage. Restored on page load and back-navigation.

## Agent Coordination

When making changes that affect user-facing files:
1. ✅ Increment `_SW_VERSION` in `js/common.js`
2. ✅ If adding new page, add to `sw.js` PRECACHE_URLS
3. ✅ Update `index.html` navigation cards
4. ✅ Commit changes with descriptive message