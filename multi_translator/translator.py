from IPython.display import HTML, display

class TranslatorInterface:
    def __init__(self):
        self.js_code = '''
        const windows = {
            googleWindow: null,
            deeplWindow: null,
            baiduWindow: null,
            closeWindow: null
        };

        const languageMapping = {
            'zh': {
                google: 'zh-TW',
                deepl: 'ZH',
                baidu: 'zh'
            },
            'en': {
                google: 'en',
                deepl: 'EN-US',
                baidu: 'en'
            },
            'ja': {
                google: 'ja',
                deepl: 'JA',
                baidu: 'jp'
            },
            'ko': {
                google: 'ko',
                deepl: 'KO',
                baidu: 'kor'
            }
        };

        const screenWidth = window.screen.availWidth;
        const screenHeight = window.screen.availHeight;
        const translatorWidth = Math.floor(screenWidth * 0.33);
        const translatorHeight = Math.floor(screenHeight * 0.75);
        const closeWindowWidth = Math.floor(screenWidth * 0.25);
        const closeWindowHeight = Math.floor(screenHeight * 0.15);

        function detectLanguage(text) {
            const hasHiragana = /[\\u3040-\\u309F]/.test(text);
            const hasKatakana = /[\\u30A0-\\u30FF]/.test(text);
            const hasKanji = /[\\u4E00-\\u9FFF]/.test(text);
            const hasHangul = /[\\u1100-\\u11FF\\u3130-\\u318F\\uA960-\\uA97F\\uAC00-\\uD7AF\\uD7B0-\\uD7FF]/.test(text);
            const hasChineseSpecific = /[\\u3007\\u3021-\\u3029\\u3038-\\u303B]/.test(text);
            
            if (hasHiragana || hasKatakana) return 'ja';
            if (hasHangul) return 'ko';
            if (hasChineseSpecific || hasKanji) return 'zh';
            return 'en';
        }

        function updatePreview(text) {
            const sourceTexts = document.querySelectorAll('.source-text');
            sourceTexts.forEach(el => el.textContent = text || 'Enter text above');
        }

        function closeWindow(windowName) {
            if (windows[windowName] && !windows[windowName].closed) {
                try {
                    windows[windowName].close();
                    windows[windowName] = null;
                } catch (error) {
                    console.error(`Error closing ${windowName}:`, error);
                }
            }
        }
        '''

        self.js_code2 = '''
        function closeAllWindows() {
            ['googleWindow', 'deeplWindow', 'baiduWindow', 'closeWindow'].forEach(name => {
                closeWindow(name);
            });
        }

        function createCloseAllWindow() {
            if (windows.closeWindow && !windows.closeWindow.closed) {
                windows.closeWindow.focus();
                return;
            }

            const left = (screenWidth - closeWindowWidth) / 2;
            const top = (screenHeight - closeWindowHeight) / 2;
            const features = `width=${closeWindowWidth},height=${closeWindowHeight},left=${left},top=${top}`;

            windows.closeWindow = window.open('', 'closeWindow', features);
            const doc = windows.closeWindow.document;
            
            doc.write(`
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Translation Control Panel</title>
                    <style>
                        body {
                            margin: 0;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            background: linear-gradient(135deg, #dc3545, #b02a37);
                            font-family: Arial, sans-serif;
                            color: white;
                        }
                        .title {
                            font-size: 20px;
                            margin-bottom: 20px;
                            text-align: center;
                        }
                        .close-button {
                            background: white;
                            color: #dc3545;
                            border: none;
                            padding: 15px 30px;
                            font-size: 18px;
                            border-radius: 8px;
                            cursor: pointer;
                            transition: all 0.3s;
                            font-weight: bold;
                            text-transform: uppercase;
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        }
                        .close-button:hover {
                            transform: translateY(-2px);
                            box-shadow: 0 6px 8px rgba(0,0,0,0.2);
                        }
                        .status {
                            margin-top: 20px;
                            font-size: 14px;
                            opacity: 0.9;
                        }
                    </style>
                </head>
                <body>
                    <div class="title">Translation Windows Control</div>
                    <button class="close-button" onclick="
                        window.opener.closeAllWindows();
                        window.close();
                    ">
                        Close All Windows
                    </button>
                    <div class="status">Press ESC to close all windows</div>
                </body>
                </html>
            `);

            windows.closeWindow.focus();
        }
        '''

        self.js_code3 = '''
        function openTranslatorWindow(url, name, position) {
            if (windows[name] && !windows[name].closed) {
                closeWindow(name);
            }

            const left = Math.floor((screenWidth / 2) - (translatorWidth * 1.5) + position * translatorWidth);
            const features = `width=${translatorWidth},height=${translatorHeight},left=${left},top=0`;
            
            setTimeout(() => {
                windows[name] = window.open(url, name, features);
                if (windows[name]) {
                    windows[name].focus();
                }
            }, 100);
        }

        function openGoogle() {
            const text = document.getElementById('sourceText').value;
            const sourceLang = detectLanguage(text);
            const targetLang = document.getElementById('targetLang').value;
            const mappedLang = languageMapping[targetLang]?.google || targetLang;
            const url = `https://translate.google.com/?sl=${sourceLang}&tl=${mappedLang}&text=${encodeURIComponent(text)}`;
            openTranslatorWindow(url, 'googleWindow', 0);
        }

        function openDeepL() {
            const text = document.getElementById('sourceText').value;
            const sourceLang = detectLanguage(text);
            const targetLang = document.getElementById('targetLang').value;
            const mappedLang = languageMapping[targetLang]?.deepl || targetLang;
            const url = `https://www.deepl.com/translator#${sourceLang}/${mappedLang}/${encodeURIComponent(text)}`;
            openTranslatorWindow(url, 'deeplWindow', 1);
        }

        function openBaidu() {
            const text = document.getElementById('sourceText').value;
            const sourceLang = detectLanguage(text);
            const targetLang = document.getElementById('targetLang').value;
            const mappedLang = languageMapping[targetLang]?.baidu || targetLang;
            const url = `https://fanyi.baidu.com/#${sourceLang}/${mappedLang}/${encodeURIComponent(text)}`;
            openTranslatorWindow(url, 'baiduWindow', 2);
        }

        function openAllTranslations() {
            const delay = 400;
            setTimeout(openGoogle, 0);
            setTimeout(openDeepL, delay);
            setTimeout(openBaidu, delay * 2);
            setTimeout(createCloseAllWindow, delay * 3);
        }

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                openAllTranslations();
            }
            if (e.key === 'Escape') {
                closeAllWindows();
            }
        });

        window.addEventListener('beforeunload', () => {
            closeAllWindows();
        });

        updatePreview("{text}");
        '''

        self.html_template = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
                    max-width: 800px;
                    margin: 20px auto;
                    padding: 0 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .title {{
                    color: #1a73e8;
                    font-size: 28px;
                    font-weight: 600;
                    margin-bottom: 10px;
                }}
                .subtitle {{
                    color: #5f6368;
                    font-size: 16px;
                    margin-bottom: 20px;
                }}
                .note {{
                    background: #fef7e0;
                    color: #594d26;
                    padding: 12px 16px;
                    margin-bottom: 24px;
                    border-radius: 8px;
                    font-size: 14px;
                    text-align: center;
                    border: 1px solid #feefc3;
                }}
                .input-section {{
                    margin-bottom: 20px;
                }}
                textarea {{
                    width: 100%;
                    min-height: 140px;
                    padding: 16px;
                    border: 2px solid #e8eaed;
                    border-radius: 8px;
                    font-size: 16px;
                    line-height: 1.6;
                    resize: vertical;
                    transition: all 0.3s;
                }}
                textarea:focus {{
                    border-color: #1a73e8;
                    outline: none;
                    box-shadow: 0 0 0 2px rgba(26,115,232,0.2);
                }}
                .language-selection {{
                    margin-bottom: 25px;
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }}
                select {{
                    padding: 8px 12px;
                    font-size: 16px;
                    border: 2px solid #e8eaed;
                    border-radius: 6px;
                    transition: all 0.3s;
                    background-color: white;
                }}
                select:focus {{
                    border-color: #1a73e8;
                    outline: none;
                    box-shadow: 0 0 0 2px rgba(26,115,232,0.2);
                }}
                .button-group {{
                    display: flex;
                    gap: 12px;
                    margin-bottom: 24px;
                    flex-wrap: wrap;
                }}
                .button {{
                    flex: 1;
                    min-width: 120px;
                    padding: 12px 20px;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.2s;
                    text-transform: uppercase;
                }}
                .button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }}
                .button:active {{
                    transform: translateY(0);
                }}
                .button.primary {{
                    background-color: #1a73e8;
                    color: white;
                }}
                .button.google {{
                    background-color: #4285f4;
                    color: white;
                }}
                .button.deepl {{
                    background-color: #042B48;
                    color: white;
                }}
                .button.baidu {{
                    background-color: #2932E1;
                    color: white;
                }}
                .button.close {{
                    background-color: #dc3545;
                    color: white;
                }}
                .preview-section {{
                    background-color: #f8f9fa;
                    padding: 16px;
                    border-radius: 8px;
                    margin-top: 24px;
                    border: 1px solid #e8eaed;
                }}
                .preview-title {{
                    color: #5f6368;
                    font-size: 14px;
                    margin-bottom: 12px;
                    font-weight: 500;
                }}
                .source-text {{
                    color: #202124;
                    font-size: 16px;
                    line-height: 1.6;
                }}
                .shortcuts {{
                    margin-top: 28px;
                    padding: 16px;
                    background-color: #e8f0fe;
                    border-radius: 8px;
                    border: 1px solid #d2e3fc;
                }}
                .shortcuts-title {{
                    color: #1967d2;
                    font-weight: 600;
                    margin-bottom: 12px;
                }}
                .shortcut-item {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin: 8px 0;
                    color: #3c4043;
                }}
                .key-combo {{
                    background-color: white;
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-family: 'SF Mono', SFMono-Regular, Consolas, monospace;
                    border: 1px solid #dadce0;
                    font-size: 13px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="title">Multi-Translator Interface</div>
                    <div class="subtitle">Compare translations from Google, DeepL, and Baidu</div>
                </div>
                <div class="note">
                    Note: For best performance, use Chrome and ensure pop-ups are allowed.<br>
                    注意：為獲得最佳效能，請使用Chrome並允許瀏覽器彈出視窗功能。
                </div>
                <div class="input-section">
                    <textarea 
                        id="sourceText" 
                        placeholder="Enter text to translate..."
                        oninput="updatePreview(this.value)"
                    >{text}</textarea>
                </div>

                <div class="language-selection">
                    <label for="targetLang">Target Language:</label>
                    <select id="targetLang">
                        <option value="en">English</option>
                        <option value="zh">Chinese</option>
                        <option value="ko">Korean</option>
                        <option value="ja">Japanese</option>
                    </select>
                </div>

                <div class="button-group">
                    <button class="button primary" onclick="openAllTranslations()">
                        Open All
                    </button>
                    <button class="button google" onclick="openGoogle()">
                        Google
                    </button>
                    <button class="button deepl" onclick="openDeepL()">
                        DeepL
                    </button>
                    <button class="button baidu" onclick="openBaidu()">
                        Baidu
                    </button>
                    <button class="button close" onclick="closeAllWindows()">
                        Close All
                    </button>
                </div>

                <div class="preview-section">
                    <div class="preview-title">Current Text:</div>
                    <div class="source-text"></div>
                </div>

                <div class="shortcuts">
                    <div class="shortcuts-title">Keyboard Shortcuts</div>
                    <div class="shortcut-item">
                        <span>Open all translators:</span>
                        <span class="key-combo">Ctrl/⌘ + Enter</span>
                    </div>
                    <div class="shortcut-item">
                        <span>Close all windows:</span>
                        <span class="key-combo">Esc</span>
                    </div>
                </div>
            </div>
            <script>
            {js_code}
            {js_code2}
            {js_code3}
            </script>
        </body>
        </html>
'''

    def create_page(self, text=""):
        return self.html_template.format(
            text=text.replace('"', '&quot;'),
            js_code=self.js_code,
            js_code2=self.js_code2,
            js_code3=self.js_code3
        )
    
    def display(self, text=""):
        display(HTML(self.create_page(text)))

def create_translator(initial_text=""):
    translator = TranslatorInterface()
    translator.display(initial_text)

if __name__ == "__main__":
    create_translator()
