/**
 * English Learning Website - Common JavaScript
 * Features:
 *   1. Column toggle for self-test (hide inflections/meanings/translations)
 *   2. Scroll position auto-save (every 3 seconds) and restore on page load
 *   3. TTS (Text-To-Speech) for clickable English words and example sentences
 */

// ======================== 1. Column Toggle (Self-Test) ========================

function toggleExam(className, buttonId, textLabel) {
    const container = document.getElementById('vocabulary-content');
    const button = document.getElementById(buttonId);

    const isHidden = container.classList.toggle(className);
    button.classList.toggle('active', isHidden);

    if (isHidden) {
        button.innerHTML = `👁️‍🗨️ 显示${textLabel}`;
    } else {
        button.innerHTML = `👁️ 隐藏${textLabel}`;
    }
}

// Tri-state toggle for the "例句" button: show all → hide translations → hide entire example column → show all
var _exampleState = 0; // 0=all visible, 1=translations hidden, 2=examples hidden

function toggleExampleColumn(buttonId) {
    const container = document.getElementById('vocabulary-content');
    const button = document.getElementById(buttonId);

    container.classList.remove('hide-translations');
    container.classList.remove('hide-examples');

    _exampleState = (_exampleState + 1) % 3;

    if (_exampleState === 1) {
        container.classList.add('hide-translations');
        button.innerHTML = '👁️ 隐藏例句';
        button.className = 'btn-toggle active';
    } else if (_exampleState === 2) {
        container.classList.add('hide-examples');
        button.innerHTML = '👁️ 显示例句';
        button.className = 'btn-toggle';
    } else {
        button.innerHTML = '👁️ 隐藏翻译';
        button.className = 'btn-toggle';
    }
}

// ======================== 2. Scroll Position Save/Restore ========================

(function initScrollSave() {
    const pageKey = window.location.pathname.split('/').pop().replace('.html', '') || 'index';
    var lastSavedY = -1;

    function saveScroll() {
        var currentY = window.scrollY;
        if (currentY !== lastSavedY) {
            localStorage.setItem('scrollPos_' + pageKey, currentY);
            lastSavedY = currentY;
        }
    }

    function restoreScroll() {
        var saved = localStorage.getItem('scrollPos_' + pageKey);
        if (saved) {
            setTimeout(function () {
                window.scrollTo(0, parseInt(saved, 10));
                lastSavedY = parseInt(saved, 10);
            }, 100);
        }
    }

    window.addEventListener('load', restoreScroll);
    window.addEventListener('pageshow', function (e) {
        if (e.persisted) restoreScroll();
    });

    setInterval(saveScroll, 3000);
    window.addEventListener('beforeunload', saveScroll);

    document.addEventListener('visibilitychange', function () {
        if (document.hidden) saveScroll();
    });

    document.addEventListener('click', function (e) {
        var link = e.target.closest('a, [onclick*="window.location.href"]');
        if (link) saveScroll();
    }, true);
})();

// ======================== 3. TTS (Text-To-Speech) ========================
// Strategy: Use native Web Speech API when available.
// Fallback: Use Google Translate TTS audio URL (works on all browsers including Android).

(function initTTS() {
    var ttsMode = 'none'; // 'native' | 'google' | 'none'

    // --- UI: Floating indicator ---
    function showTTSIndicator(mode) {
        var el = document.getElementById('tts-status');
        if (el) el.parentNode.removeChild(el);

        el = document.createElement('div');
        el.id = 'tts-status';
        el.style.cssText = 'position:fixed;bottom:12px;right:12px;z-index:9999;' +
            'width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;' +
            'font-size:18px;cursor:default;box-shadow:0 2px 8px rgba(0,0,0,0.15);';

        if (mode === 'native') {
            el.textContent = '🔊';
            el.style.backgroundColor = '#e8f8f5';
            el.style.border = '2px solid #27ae60';
            el.title = 'TTS 就绪 - 点击朗读';
        } else if (mode === 'google') {
            el.textContent = '🔊';
            el.style.backgroundColor = '#fff3cd';
            el.style.border = '2px solid #f39c12';
            el.title = '在线TTS - 点击朗读（需要网络）';
        } else {
            el.textContent = '🔇';
            el.style.backgroundColor = '#fdf2e9';
            el.style.border = '2px solid #e67e22';
            el.title = 'TTS 不可用';
        }
        document.body.appendChild(el);
        if (!window._ttsIndicatorShown) {
            window._ttsIndicatorShown = true;
            setTimeout(function () { if (el.parentNode) el.style.opacity = '0.3'; }, 5000);
        }
    }

    // --- Check native TTS availability ---
    function checkNativeAndInit() {
        if ('speechSynthesis' in window) {
            var voices = window.speechSynthesis.getVoices();
            if (voices.length > 0) {
                ttsMode = 'native';
                showTTSIndicator('native');
                return true;
            }
        }
        return false;
    }

    // Try native immediately; if voices load async, wait for event
    if (!checkNativeAndInit()) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.onvoiceschanged = function () {
                window.speechSynthesis.onvoiceschanged = null;
                if (checkNativeAndInit()) return;
                // Still no voices after event → fallback to Google
                ttsMode = 'google';
                showTTSIndicator('google');
            };
            // Timeout: if after 2s no voices, fallback to Google
            setTimeout(function () {
                if (ttsMode !== 'native') {
                    ttsMode = 'google';
                    showTTSIndicator('google');
                }
            }, 2000);
        } else {
            // No speechSynthesis API at all
            ttsMode = 'google';
            showTTSIndicator('google');
        }
    }

    // --- Elements to make clickable ---
    // Includes mixed-content elements (.rule, .mini-table td) so English text inside them can be clicked.
    // The .tts-clickable visual style is only added if the element CONTAINS English text.
    var ttsElements = document.querySelectorAll('.word, .inflection, .example, .rule, .mini-table td, .compare-col .ex, .formula-box');

    // --- Speak function: dispatches to native or Google ---
    function speakText(text) {
        if (!text) return;

        if (ttsMode === 'native') {
            if (window.speechSynthesis.speaking) window.speechSynthesis.cancel();

            // Edge workaround: first speak may be ignored
            if (!window._edgeWarmedUp) {
                window._edgeWarmedUp = true;
                var dummy = new SpeechSynthesisUtterance(' ');
                dummy.volume = 0;
                window.speechSynthesis.speak(dummy);
                setTimeout(function () {
                    window.speechSynthesis.cancel();
                    var u = new SpeechSynthesisUtterance(text);
                    u.lang = 'en-US';
                    u.rate = 0.9;
                    window.speechSynthesis.speak(u);
                }, 50);
                return;
            }

            var utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en-US';
            utterance.rate = 0.9;
            utterance.onerror = function () { showTTSIndicator('google'); ttsMode = 'google'; };
            window.speechSynthesis.speak(utterance);
        } else if (ttsMode === 'google') {
            // Google Translate TTS: works on ALL platforms including Android
            var audio = new Audio();
            audio.src = 'https://translate.google.com/translate_tts?ie=UTF-8&q=' +
                encodeURIComponent(text) + '&tl=en&client=tw-ob';
            audio.play().catch(function () {
                // If autoplay blocked, show a hint
                showTTSIndicator('none');
            });
        }
    }

    ttsElements.forEach(function (el) {
        // Only show the dotted-underline style if element contains English letters
        var text = el.textContent || '';
        if (/[a-zA-Z]/.test(text)) {
            el.classList.add('tts-clickable');
        }
        // Always attach click handler (clicking a "纯中文" element does nothing harm but also nothing useful)
        // Only speak if text actually has English content
        el.addEventListener('click', function (e) {
            e.stopPropagation();
            var txt = this.textContent.trim();
            if (/[a-zA-Z]/.test(txt)) {
                speakText(txt);
            }
        });
    });
})();