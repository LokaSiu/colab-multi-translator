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

        function detectLanguage(text) {
            // Basic detection for Chinese, Japanese, Korean
            if (/[\\u4E00-\\u9FFF]/.test(text)) return 'zh';
            if (/[\\u3040-\\u30FF]/.test(text)) return 'ja';
            if (/[\\u3131-\\uD79D]/.test(text)) return 'ko';
            
            // Default to English for other scripts
            return 'en';
        }

        function updatePreview(text) {
            const sourceTexts = document.querySelectorAll('.source-text');
            sourceTexts.forEach(el => el.textContent = text || 'Enter text above');
        }

        function forceCloseWindow(windowObj) {
            if (windowObj && !windowObj.closed) {
                try {
                    windowObj.opener = null;
                    windowObj.open('', '_self');
                    windowObj.close();
                    return true;
                } catch (e) {
                    console.error('Failed to force close window:', e);
                    return false;
                }
            }
            return true;
        }

        function closeWindow(windowName) {
            if (windows[windowName]) {
                const closed = forceCloseWindow(windows[windowName]);
                if (closed) {
                    windows[windowName] = null;
                }
            }
        }

        function closeAllWindows() {
            for (let windowName in windows) {
                closeWindow(windowName);
            }
            // Force garbage collection
            for (let windowName in windows) {
                windows[windowName] = null;
            }
        }
'''

        self.js_code2 = '''
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

        function openTranslatorWindow(url, name, position) {
            const left = position * translatorWidth;
            const features = `width=${translatorWidth},height=${translatorHeight},left=${left},top=0,screenX=${left},screenY=0`;

            closeWindow(name);

            windows[name] = window.open(url, name, features);
            if (windows[name]) {
                windows[name].focus();
                windows[name].moveTo(left, 0);
                windows[name].opener = window;
            }
            return windows[name];
        }
'''

        self.js_code3 = '''
        function getTargetLanguage() {
            return document.getElementById('targetLang').value;
        }

        function openGoogle() {
            const text = document.getElementById('sourceText').value;
            const sourceLang = detectLanguage(text);
            const targetLang = getTargetLanguage();
            const url = `https://translate.google.com/?sl=auto&tl=${targetLang}&text=${encodeURIComponent(text)}`;
            return openTranslatorWindow(url, 'googleWindow', 0);
        }

        function openDeepL() {
            const text = document.getElementById('sourceText').value;
            const targetLang = getTargetLanguage();
            const url = `https://www.deepl.com/translator#auto/${targetLang}/${encodeURIComponent(text)}`;
            return openTranslatorWindow(url, 'deeplWindow', 1);
        }

        function openBaidu() {
            const text = document.getElementById('sourceText').value;
            const targetLang = getTargetLanguage();
            const url = `https://fanyi.baidu.com/#auto/${targetLang}/${encodeURIComponent(text)}`;
            return openTranslatorWindow(url, 'baiduWindow', 2);
        }

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

        updatePreview("{text}");

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

        setInterval(() => {
            for (let windowName in windows) {
                if (windows[windowName] && windows[windowName].closed) {
                    windows[windowName] = null;
                }
            }
        }, 1000);
'''

        self.html_template = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                /* Previous styles remain the same */
                .language-select {
                    margin-bottom: 15px;
                }
                select {
                    padding: 8px;
                    border-radius: 4px;
                    border: 1px solid #ddd;
                    font-size: 14px;
                    width: 200px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="title">Multi-Translator Interface</div>
                    <div class="subtitle">Compare translations from Google, DeepL, and Baidu</div>
                </div>
                
                <div class="language-select">
                    <select id="targetLang">
                        <option value="en">English</option>
                        <option value="zh">Chinese</option>
                        <option value="ja">Japanese</option>
                        <option value="ko">Korean</option>
                        <option value="es">Spanish</option>
                        <option value="fr">French</option>
                        <option value="de">German</option>
                        <option value="ru">Russian</option>
                    </select>
                </div>

                <div class="input-section">
                    <textarea 
                        id="sourceText" 
                        placeholder="Enter text to translate... (Source language will be auto-detected)"
                        oninput="updatePreview(this.value)"
                    >{text}</textarea>
                </div>

                <!-- Rest of the HTML remains the same -->
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
