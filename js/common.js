/**
 * English Learning Website - Common JavaScript
 * Features:
 *   1. Service Worker registration (offline support)
 *   2. Column toggle for self-test (hide inflections/meanings/translations)
 *   3. Scroll position auto-save (every 3 seconds) and restore on page load
 *   4. TTS (Text-To-Speech) for clickable English words and example sentences
 */

// ======================== 0. Service Worker (Offline Support) ========================

// SW version - increment this when publishing updates to force re-caching
var _SW_VERSION = '2026-06-22-02';

(function registerSW() {
    if ('serviceWorker' in navigator) {
        // Determine SW path based on page location
        var swPath = window.location.pathname.indexOf('/grammar/') === 0
            ? '../sw.js'
            : (window.location.pathname.indexOf('/vocabulary/') === 0
                ? '../sw.js'
                : (window.location.pathname.indexOf('/vocabulary2/') === 0
                    ? '../sw.js'
                    : 'sw.js'));

        // Add version query param for cache busting
        navigator.serviceWorker.register(swPath + '?v=' + _SW_VERSION).then(function (reg) {
            // Check if there's a new version waiting
            if (reg.waiting) {
                // New SW is waiting — tell it to take over
                reg.waiting.postMessage({ action: 'skipWaiting' });
            }
        }).catch(function (err) {
            // SW registration failed — offline support won't work but page still functions
            console.warn('SW registration failed:', err);
        });

        // Listen for messages from the Service Worker
        navigator.serviceWorker.addEventListener('message', function (event) {
            if (event.data && event.data.type === 'CONTENT_UPDATED') {
                // Content was updated in the background — reload to show new version
                window.location.reload();
            }
        });

        // Detect network status changes for UI feedback
        function updateOnlineStatus() {
            var indicator = document.getElementById('tts-status');
            if (navigator.onLine) {
                document.body.classList.remove('offline');
                // The TTS indicator will be managed by initTTS() below
            } else {
                document.body.classList.add('offline');
                if (indicator) {
                    indicator.textContent = '📵';
                    indicator.title = '离线模式';
                    indicator.style.backgroundColor = '#fdf2e9';
                    indicator.style.border = '2px solid #e74c3c';
                }
            }
        }

        window.addEventListener('online', updateOnlineStatus);
        window.addEventListener('offline', updateOnlineStatus);
        // Initial check
        updateOnlineStatus();
    }
})();

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

// Dynamically inject referrer policy meta tag at runtime as a safety net.
(function ensureReferrerPolicy() {
    if (!document.querySelector('meta[name="referrer"]')) {
        var meta = document.createElement('meta');
        meta.name = 'referrer';
        meta.content = 'same-origin';
        document.head.appendChild(meta);
    }
})();

(function initTTS() {
    var ttsMode = 'none'; // 'native' | 'google' | 'none'

    // Save/load TTS preference site-wide (same across ALL pages)
    var PREF_KEY = 'ttsPreference';

    function loadPreference() {
        return localStorage.getItem(PREF_KEY);
    }

    function savePreference(mode) {
        localStorage.setItem(PREF_KEY, mode);
    }

    // --- UI: Floating indicator (clickable to toggle mode) ---
    function showTTSIndicator(mode) {
        var el = document.getElementById('tts-status');
        if (el) el.parentNode.removeChild(el);

        el = document.createElement('div');
        el.id = 'tts-status';
        el.style.cssText = 'position:fixed;bottom:12px;right:12px;z-index:9999;' +
            'width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;' +
            'font-size:18px;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.15);' +
            'transition:transform 0.2s;';

        if (mode === 'native') {
            el.textContent = '🔊';
            el.style.backgroundColor = '#e8f8f5';
            el.style.border = '2px solid #27ae60';
            el.title = '点击切换TTS模式（当前: 系统语音）';
        } else if (mode === 'google') {
            el.textContent = '🔊';
            el.style.backgroundColor = '#fff3cd';
            el.style.border = '2px solid #f39c12';
            el.title = '点击切换TTS模式（当前: 在线TTS）';
        } else {
            el.textContent = '🔇';
            el.style.backgroundColor = '#fdf2e9';
            el.style.border = '2px solid #e67e22';
            el.title = 'TTS 不可用';
        }

        // Hover effect
        el.addEventListener('mouseenter', function () {
            this.style.transform = 'scale(1.15)';
        });
        el.addEventListener('mouseleave', function () {
            this.style.transform = 'scale(1)';
        });

        // Click to toggle mode: native ↔ google (persist across pages)
        el.addEventListener('click', function (e) {
            e.stopPropagation();
            if (ttsMode === 'native') {
                ttsMode = 'google';
                savePreference('google');
                showTTSIndicator('google');
            } else if (ttsMode === 'google') {
                // Only switch back if native is available
                if ('speechSynthesis' in window) {
                    ttsMode = 'native';
                    savePreference('native');
                    showTTSIndicator('native');
                }
            }
        });

        document.body.appendChild(el);
        if (!window._ttsIndicatorShown) {
            window._ttsIndicatorShown = true;
            setTimeout(function () { if (el.parentNode) el.style.opacity = '0.3'; }, 5000);
        }
    }

    // --- TTS mode detection ---
    // On Android Chrome, speechSynthesis exists but voices may arrive late.
    // We try native by default and only fallback to Google if sendUtterance() fails at runtime.
    // Voice loading detection is unreliable on Android, so we just attempt both.
    function detectTTSMode() {
        // Check for saved user preference first
        var saved = loadPreference();
        if (saved === 'google') {
            ttsMode = 'google';
            showTTSIndicator('google');
            return;
        }

        // No saved preference (or saved as 'native'): try native speechSynthesis
        if ('speechSynthesis' in window) {
            ttsMode = 'native';
            var voices = window.speechSynthesis.getVoices();
            if (voices.length > 0) {
                showTTSIndicator('native');
                return;
            }
            window.speechSynthesis.onvoiceschanged = function () {
                var v = window.speechSynthesis.getVoices();
                if (v.length > 0) {
                    window.speechSynthesis.onvoiceschanged = null;
                    showTTSIndicator('native');
                }
            };
            showTTSIndicator('native');
        } else {
            ttsMode = 'google';
            showTTSIndicator('google');
        }
    }
    detectTTSMode();

    // Keep a reference to the current Google Audio element so we can stop it
    var _currentGoogleAudio = null;

    // Global reference to prevent garbage collection of speech objects on Android Chrome
    window._activeUtterance = null;

    // Helper: Find appropriate speech engine voice by language code
    function findVoice(langCode) {
        if (!('speechSynthesis' in window)) return null;
        var voices = window.speechSynthesis.getVoices();

        // Exact match (normalizing Android underscores like en_US to en-US)
        var match = voices.find(function (v) {
            return v.lang.replace('_', '-').toLowerCase() === langCode.toLowerCase();
        });
        // General fallback match (e.g. starts with "en")
        if (!match) {
            match = voices.find(function (v) {
                return v.lang.toLowerCase().indexOf(langCode.split('-')[0].toLowerCase()) === 0;
            });
        }
        return match;
    }

    // Helper: fall back to Google Online TTS (called on native error)
    function fallbackToGoogle(text, lang) {
        if (_currentGoogleAudio) {
            _currentGoogleAudio.pause();
            _currentGoogleAudio.src = '';
            _currentGoogleAudio = null;
        }

        var googleLang = lang.startsWith('zh') ? 'zh-CN' : 'en';
        var audio = new Audio();
        audio.referrerPolicy = 'no-referrer';
        audio.src = 'https://translate.google.com/translate_tts?ie=UTF-8&q=' +
            encodeURIComponent(text) + '&tl=' + googleLang + '&client=tw-ob';

        _currentGoogleAudio = audio;
        audio.play().catch(function () {
            _currentGoogleAudio = null;
        });
    }

    // --- Speak function: respects user's TTS mode selection ---
    function speakText(text, lang) {
        if (!text) return;
        lang = lang || 'en-US';

        if (ttsMode === 'native' || ttsMode === 'none') {
            // Stop any running Google audio first
            if (_currentGoogleAudio) {
                _currentGoogleAudio.pause();
                _currentGoogleAudio.src = '';
                _currentGoogleAudio = null;
            }

            if ('speechSynthesis' in window) {
                if (window.speechSynthesis.speaking) window.speechSynthesis.cancel();

                try {
                    var utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = lang;
                    utterance.rate = lang.startsWith('zh') ? 0.85 : 0.9;

                    // Match best available voice profile
                    var voice = findVoice(lang);
                    if (voice) {
                        utterance.voice = voice;
                    }

                    // Chromium Garbage Collection workaround (essential for Android Chrome)
                    window._activeUtterance = utterance;

                    // Trigger fallback on actual failures, but NOT on 'interrupted' or 'canceled'
                    // which are benign (user clicked something else, or new utterance started).
                    utterance.onerror = function (event) {
                        if (event.error === 'interrupted' || event.error === 'canceled') {
                            return;
                        }
                        console.warn('Native speech failed, trying online fallback...', event.error);
                        fallbackToGoogle(text, lang);
                    };

                    window.speechSynthesis.speak(utterance);
                } catch (e) {
                    console.warn('Native speech error, falling back:', e);
                    fallbackToGoogle(text, lang);
                }
            }
        } else if (ttsMode === 'google') {
            // Stop previous Google audio if still playing
            if (_currentGoogleAudio) {
                _currentGoogleAudio.pause();
                _currentGoogleAudio.src = '';
                _currentGoogleAudio = null;
            }

            // Also cancel native speech if it was playing
            if ('speechSynthesis' in window && window.speechSynthesis.speaking) {
                window.speechSynthesis.cancel();
            }

            fallbackToGoogle(text, lang);
        }
    }

    // --- Elements to make clickable ---
    // Added .meaning so Chinese definitions can also be read aloud.
    var ttsElements = document.querySelectorAll('.word, .inflection, .meaning, .example, .rule, .mini-table td, .compare-col .ex, .formula-box');

    // Helper: prepare text for TTS.
    // Steps:
    //   1) Remove actual IPA notation: content between slashes containing stress markers (ˈˌ) or phonetic characters.
    //   2) Replace remaining slashes with ". " (period = longer TTS pause ≈ 0.5s).
    //   3) For English-only text, strip Chinese characters/punctuation.
    //   4) Clean up extra whitespace/commas.
    function prepareForTTS(text) {
        // Step 1 — Remove IPA notation: pattern " word /ipa/; " or " word /ipa/"
        // IPA is a word between slashes preceded by a space and followed by punctuation or end-of-string.
        // This correctly preserves separator slashes like "am/is/are" (no spaces around them).
        text = text.replace(/\s+\/[ˈˌəæɑɔɪʊʌɛθðŋʃʒɡa-zA-Z:]+\s*[;,\)\]\.]/g, '');
        text = text.replace(/\s+\/[ˈˌəæɑɔɪʊʌɛθðŋʃʒɡa-zA-Z:]+$/g, '');

        // Step 2 — Replace remaining "/" (non-IPA separators like "can/could/may") 
        // with ". " (period = sentence-ending pause ≈ 0.5s)
        text = text.replace(/\//g, '. ');

        // Step 3 — Detect if text contains Chinese
        var hasChinese = /[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]/.test(text);

        if (hasChinese) {
            // Clean up extra spaces and punctuation
            text = text.replace(/,+/g, ',').replace(/\s+/g, ' ').trim();
            text = text.replace(/,\s*,/g, ',').replace(/^,+|,+$/g, '').trim();
        } else {
            // For English-only: strip Chinese characters and punctuation
            text = text.replace(/[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]/g, '');
            text = text.replace(/[，。！？、；：“”【】（）《》——…·\u3000-\u303f\uff00-\uffef]/g, '');
            text = text.replace(/,+/g, ',').replace(/\s+/g, ' ').trim();
            text = text.replace(/,\s*,/g, ',').replace(/^,+|,+$/g, '').trim();
        }
        return text;
    }

    ttsElements.forEach(function (el) {
        var fullText = el.textContent || '';
        var prepared = prepareForTTS(fullText);

        // Show clickable style if there's anything to read (English OR Chinese)
        if (prepared.length > 0) {
            el.classList.add('tts-clickable');
        }

        el.addEventListener('click', function (e) {
            e.stopPropagation();
            var clickedText = this.textContent.trim();
            var toSpeak = prepareForTTS(clickedText);
            if (toSpeak.length > 0) {
                // Detect if text contains Chinese → use zh-CN, otherwise en-US
                var targetLang = /[\u4e00-\u9fff]/.test(toSpeak) ? 'zh-CN' : 'en-US';
                speakText(toSpeak, targetLang);
            }
        });
    });
})();