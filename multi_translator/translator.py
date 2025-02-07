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

        const screenWidth = window.screen.availWidth;
        const screenHeight = window.screen.availHeight;
        const translatorWidth = Math.floor(screenWidth * 0.33);
        const translatorHeight = Math.floor(screenHeight * 0.75);
        const closeWindowWidth = Math.floor(screenWidth * 0.25);
        const closeWindowHeight = Math.floor(screenHeight * 0.15);

        // Auto-detect source language based on the text content.
        function detectLanguage(text) {
            return /[\\u4E00-\\u9FFF]/.test(text) ? 'zh' : 'en';
        }

        // Update the preview area with the current text.
        function updatePreview(text) {
            const sourceTexts = document.querySelectorAll('.source-text');
            sourceTexts.forEach(el => el.textContent = text || 'Enter text above');
        }

        // Try to close a given window.
        function closeWindow(windowName) {
            if (windows[windowName] && !windows[windowName].closed) {
                try {
                    windows[windowName].close();
                    windows[windowName] = null;
                } catch (error) {
                    console.error('Direct close failed for', windowName, error);
                    try {
                        windows[windowName].focus();
                        setTimeout(() => {
                            try {
                                windows[windowName].close();
                                windows[windowName] = null;
                            } catch (err) {
                                console.error('Fallback close failed for', windowName, err);
                            }
                        }, 100);
                    } catch (err) {
                        console.error('Fallback focusing failed for', windowName, err);
                    }
                }
                // Additional attempt for googleWindow if still open
                if(windowName === 'googleWindow' && windows[windowName] && !windows[windowName].closed) {
                    setTimeout(() => {
                        if(windows[windowName] && !windows[windowName].closed) {
                            try {
                                windows[windowName].focus();
                                windows[windowName].close();
                                windows[windowName] = null;
                            } catch(e) {
                                console.error('Second attempt close failed for googleWindow', e);
                            }
                        }
                    }, 500);
                }
            }
        }

        // Close all translator windows sequentially.
        function closeAllWindows() {
            const windowNames = Object.keys(windows);
            let index = 0;
            
            function closeNext() {
                if (index < windowNames.length) {
                    // Skip 'closeWindow' (the control panel) to avoid closing it prematurely.
                    if(windowNames[index] === 'closeWindow') {
                        index++;
                        closeNext();
                        return;
                    }
                    closeWindow(windowNames[index]);
                    index++;
                    setTimeout(closeNext, 200);
                }
            }
            
            closeNext();
        }
'''
        self.js_code2 = '''
        // Create a control panel that can trigger closing all translator windows.
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
                        setTimeout(() => window.close(), 300);
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
        // Open a Google Translate window using auto-detected source language with a user-selected target language.
        function openGoogle() {
            const text = document.getElementById('sourceText').value;
            const sourceLang = detectLanguage(text);
            const targetLang = document.getElementById('targetLang').value;
            const url = `https://translate.google.com/?sl=${sourceLang}&tl=${targetLang}&text=${encodeURIComponent(text)}`;
            return openTranslatorWindow(url, 'googleWindow', 0);
        }

        // Open a DeepL window using a similar approach.
        function openDeepL() {
            const text = document.getElementById('sourceText').value;
            const sourceLang = detectLanguage(text);
            const targetLang = document.getElementById('targetLang').value;
            const url = `https://www.deepl.com/en/translator#${sourceLang}/${targetLang}/${encodeURIComponent(text)}`;
            return openTranslatorWindow(url, 'deeplWindow', 1);
        }

        // Open a Baidu translation window.
        function openBaidu() {
            const text = document.getElementById('sourceText').value;
            const sourceLang = detectLanguage(text);
            const targetLang = document.getElementById('targetLang').value;
            const url = `https://fanyi.baidu.com/#${sourceLang}/${targetLang}/${encodeURIComponent(text)}`;
            return openTranslatorWindow(url, 'baiduWindow', 2);
        }

        // Open all translator windows in succession.
        function openAllTranslations() {
            Promise.resolve()
                .then(() => {
                    const g = openGoogle();
                    if (g) g.focus();
                    return new Promise(resolve => setTimeout(resolve, 400));
                })
                .then(() => {
                    const d = openDeepL();
                    if (d) d.focus();
                    return new Promise(resolve => setTimeout(resolve, 400));
                })
                .then(() => {
                    const b = openBaidu();
                    if (b) b.focus();
                    return new Promise(resolve => setTimeout(resolve, 400));
                })
                .then(() => {
                    createCloseAllWindow();
                });
        }

        // Update the preview area with the initial text.
        updatePreview("{text}");

        // Keyboard shortcuts for user convenience.
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

        // Periodically check the status of opened windows.
        setInterval(() => {
            Object.keys(windows).forEach(windowName => {
                if (windows[windowName] && windows[windowName].closed) {
                    windows[windowName] = null;
                }
            });
        }, 1000);

        // Helper function to open a translator window at a calculated screen position.
        function openTranslatorWindow(url, name, position) {
            // Center the three translator windows horizontally.
            const left = Math.floor((screenWidth / 2) - (translatorWidth * 1.5) + position * translatorWidth);
            const features = `width=${translatorWidth},height=${translatorHeight},left=${left},top=0,screenX=${left},screenY=0`;

            if (windows[name] && !windows[name].closed) {
                windows[name].close();
            }

            windows[name] = window.open(url, name, features);
            if (windows[name]) {
                windows[name].focus();
                windows[name].moveTo(left, 0);
                windows[name].addEventListener('beforeunload', () => {
                    windows[name] = null;
                });
                windows[name].opener = window;
            }
            return windows[name];
        }
'''
        # The updated HTML template now includes a language selection dropdown,
        # additional language options, and a note advising best browser usage.
        self.html_template = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 20px auto;
                    padding: 0 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 10px;
                }}
                .title {{
                    color: #2196F3;
                    font-size: 24px;
                    margin-bottom: 10px;
                }}
                .subtitle {{
                    color: #666;
                    font-size: 16px;
                    margin-bottom: 20px;
                }}
                .note {{
                    background: #ffeb3b;
                    color: #333;
                    padding: 10px;
                    margin-bottom: 20px;
                    border-radius: 6px;
                    font-size: 14px;
                    text-align: center;
                }}
                .input-section {{
                    margin-bottom: 15px;
                }}
                textarea {{
                    width: 100%;
                    min-height: 120px;
                    padding: 12px;
                    border: 2px solid #e0e0e0;
                    border-radius: 8px;
                    font-size: 16px;
                    line-height: 1.5;
                    resize: vertical;
                    transition: border-color 0.3s;
                }}
                textarea:focus {{
                    border-color: #2196F3;
                    outline: none;
                }}
                .language-selection {{
                    margin-bottom: 25px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                select {{
                    padding: 8px 12px;
                    font-size: 16px;
                    border: 2px solid #e0e0e0;
                    border-radius: 6px;
                    transition: border-color 0.3s;
                }}
                select:focus {{
                    border-color: #2196F3;
                    outline: none;
                }}
                .button-group {{
                    display: flex;
                    gap: 10px;
                    margin-bottom: 20px;
                    flex-wrap: wrap;
                }}
                .button {{
                    flex: 1;
                    min-width: 120px;
                    padding: 12px 20px;
                    border: none;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                    cursor: pointer;
                    transition: transform 0.2s, opacity 0.2s;
                    text-transform: uppercase;
                }}
                .button:hover {{
                    transform: translateY(-2px);
                    opacity: 0.9;
                }}
                .button:active {{
                    transform: translateY(0);
                }}
                .button.primary {{
                    background-color: #2196F3;
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
                    padding: 15px;
                    border-radius: 8px;
                    margin-top: 20px;
                }}
                .preview-title {{
                    color: #666;
                    font-size: 14px;
                    margin-bottom: 10px;
                }}
                .source-text {{
                    color: #333;
                    font-size: 16px;
                    line-height: 1.5;
                }}
                .shortcuts {{
                    margin-top: 25px;
                    padding: 15px;
                    background-color: #e3f2fd;
                    border-radius: 8px;
                }}
                .shortcuts-title {{
                    color: #1976D2;
                    font-weight: bold;
                    margin-bottom: 10px;
                }}
                .shortcut-item {{
                    display: flex;
                    justify-content: space-between;
                    margin: 5px 0;
                    color: #333;
                }}
                .key-combo {{
                    background-color: #fff;
                    padding: 2px 8px;
                    border-radius: 4px;
                    font-family: monospace;
                    border: 1px solid #ccc;
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
