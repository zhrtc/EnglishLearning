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
├── 📄 index.html              ← Navigation hub
├── 📄 core-vocabulary.html    ← 6 vocabulary word list files
├── 📄 verbs-a-l.html
├── 📄 verbs-m-z.html
├── 📄 adjectives-adverbs.html
├── 📄 nouns-life-scene.html
├── 📄 nouns-society-function.html
├── 📄 sw.js                   ← Service Worker (offline + update)
├── 📁 css/
│   ├── common.css             ← Shared styles (vocabulary tables)
│   └── grammar.css            ← Card layout (grammar pages)
├── 📁 js/
│   └── common.js              ← TTS / scroll-save / toggle / SW registration
└── 📁 grammar/                ← 11 grammar topic pages
    ├── tenses.html
    ├── passive-voice.html
    ├── non-finite-verbs.html
    ├── clauses.html
    ├── modal-verbs.html
    ├── sentence-patterns.html
    ├── verb-collocations.html
    ├── prepositions.html
    ├── confusable-words.html
    ├── subject-verb-agreement.html
    ├── direct-indirect-speech.html
    └── writing-connectors.html
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