# KET + 中考 词汇备考通

剑桥 A2 级别与九年义务教育中考考纲全覆盖复习方案。一个纯静态的英语学习网站，包含词汇表、语法讲解、知识点专项，支持离线浏览和语音朗读。

## 📁 项目结构

```
EnglishLearning/
├── index.html              # 主导航页面（分类入口）
├── sw.js                   # Service Worker（离线支持）
├── js/common.js            # 公共 JavaScript（SW注册、自测切换、滚动保存、TTS）
├── css/
│   ├── common.css           # 公共样式
│   └── grammar.css          # 语法页面卡片样式
├── grammar/                 # 语法与考点专项（19 页）
│   ├── tenses.html          # 八大时态
│   ├── passive-voice.html   # 被动语态
│   ├── articles.html        # 冠词
│   ├── comparatives.html    # 比较级与最高级
│   ├── pronouns.html        # 代词
│   ├── questions.html       # 疑问句
│   ├── numerals.html        # 数词
│   ├── conjunctions.html    # 连词
│   ├── word-formation.html  # 构词法
│   ├── verb-collocations.html   # 动词固定搭配
│   ├── prepositions.html    # 介词
│   ├── confusable-words.html    # 易混词辨析
│   ├── clauses.html         # 三大从句
│   ├── non-finite-verbs.html    # 非谓语动词
│   ├── modal-verbs.html     # 情态动词与虚拟语气
│   ├── sentence-patterns.html   # 特殊句型
│   ├── subject-verb-agreement.html # 主谓一致
│   ├── direct-indirect-speech.html # 直接/间接引语
│   └── writing-connectors.html   # 写作连接词
└── vocabulary/              # 词汇分类表（11 页）
    ├── core-vocabulary-p1.html  # 原版核心 P1（核心动词·人物·家庭·学校·食物）
    ├── core-vocabulary-p2.html  # P2（时间·交通·描述·运动·健康·工作）
    ├── core-vocabulary-p3.html  # P3（家居·购物·自然·科技·副词·介词）
    ├── core-vocabulary-p4.html  # P4（代词·动作·数量·社交·抽象·心理）
    ├── core-vocabulary-p5.html  # P5（城镇·日用品·语法词·地理·量词）
    ├── core-vocabulary-p6.html  # P6（情感·方位·程度·媒体·连接词）
    ├── verbs-a-l.html           # 动词 A-L
    ├── verbs-m-z.html           # 动词 M-Z
    ├── adjectives-adverbs.html   # 形容词与副词
    ├── nouns-life-scene.html    # 生活与场景名词
    └── nouns-society-function.html # 社会与功能词
```

## ✨ 功能特性

### 1. 自测模式（词汇表页面专有）
每个词汇表页面顶部有控制面板，支持：
- **隐藏单词** — 遮盖英语单词，测试拼写记忆
- **隐藏变形** — 遮盖特殊变形（过去式、复数等）
- **隐藏释义** — 遮盖中文释义，测试词义理解
- **隐藏翻译** — 三级切换：隐藏翻译 → 隐藏整个例句列 → 全部显示

### 2. 语音朗读 (TTS)
点击任何带有虚线下划线的英语文字即可朗读：
- **系统语音 (Native)** — 使用设备的语音引擎（**离线可用**）
- **在线语音 (Google)** — 使用 Google 翻译 TTS（需要网络）
- 可通过右下角浮动按钮切换两种模式，选择会跨页面持久保存
- 自动识别中/英文，使用合适的语言引擎

### 3. 离线浏览
基于 Service Worker 实现：
- 首次访问时自动缓存所有页面
- 之后即使断网也可以正常浏览全部内容
- 页面更新时自动通知刷新

### 4. 滚动位置保存
每 3 秒自动保存滚动位置，返回页面时自动恢复。

## 🚀 使用方式

### 本地访问
直接用浏览器打开 `index.html` 即可。

### 在线部署
上传整个项目到任何静态文件服务器（GitHub Pages、Nginx、Apache 等）。

> **注意**：Service Worker 需要 HTTPS 或 `localhost` 环境才能注册。如果通过 `file://` 协议打开，离线功能不可用，但页面浏览和 TTS 仍然正常。

## 📝 技术栈

- 纯 HTML5 + CSS3 + JavaScript（无外部依赖）
- 响应式设计，适配桌面和移动设备
- Web Speech API（TTS 语音朗读）
- Service Worker API（离线缓存）
- localStorage（用户偏好存储）

## 🎯 内容覆盖

共 30 个学习页面：

| 类别 | 数量 | 内容 |
|------|------|------|
| 📖 词汇分类表 | 11 页 | 约 1,000+ 核心词汇，含音标、变形、释义、例句 |
| 📚 语法与考点 | 19 页 | 覆盖 KET + 中考全部语法考点 |

## 📄 License

MIT