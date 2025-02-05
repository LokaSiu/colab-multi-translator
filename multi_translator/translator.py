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
            const sourceLang = 'auto';  // Use auto-detect
            const targetLang = getTargetLanguage();
            const url = `https://translate.google.com/?sl=${sourceLang}&tl=${targetLang}&text=${encodeURIComponent(text)}`;
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
            const sourceLang = 'auto';  // Use auto-detect
            const targetLang = getTargetLanguage();
            const url = `https://fanyi.baidu.com/#${sourceLang}/${targetLang}/${encodeURIComponent(text)}`;
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
        self.css = '''
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 20px auto;
                padding: 0 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            .title {
                color: #2196F3;
                font-size: 24px;
                margin-bottom: 10px;
            }
            .subtitle {
                color: #666;
                font-size: 16px;
            }
            .input-section {
                margin-bottom: 25px;
            }
            textarea {
                width: 100%;
                min-height: 120px;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 16px;
                line-height: 1.5;
                resize: vertical;
                transition: border-color 0.3s;
            }
            textarea:focus {
                border-color: #2196F3;
                outline: none;
            }
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
            .button-group {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
                flex-wrap: wrap;
            }
            .button {
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
            }
            .button:hover {
                transform: translateY(-2px);
                opacity: 0.9;
            }
            .button:active {
                transform: translateY(0);
            }
            .button.primary {
                background-color: #2196F3;
                color: white;
            }
            .button.google {
                background-color: #4285f4;
                color: white;
            }
            .button.deepl {
                background-color: #042B48;
                color: white;
            }
            .button.baidu {
                background-color: #2932E1;
                color: white;
            }
            .button.close {
                background-color: #dc3545;
                color: white;
            }
            .preview-section {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin-top: 20px;
            }
            .preview-title {
                color: #666;
                font-size: 14px;
                margin-bottom: 10px;
            }
            .source-text {
                color: #333;
                font-size: 16px;
                line-height: 1.5;
            }
            .shortcuts {
                margin-top: 25px;
                padding: 15px;
                background-color: #e3f2fd;
                border-radius: 8px;
            }
            .shortcuts-title {
                color: #1976D2;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .shortcut-item {
                display: flex;
                justify-content: space-between;
                margin: 5px 0;
                color: #333;
            }
            .key-combo {
                background-color: #fff;
                padding: 2px 8px;
                border-radius: 4px;
                font-family: monospace;
                border: 1px solid #ccc;
            }
        '''

    def create_page(self, text=""):
        escaped_text = text.replace('"', '&quot;')
        return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
            {self.css}
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
                    >{escaped_text}</textarea>
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
            {self.js_code}
            {self.js_code2}
            {self.js_code3}
            </script>
        </body>
        </html>
        '''

    def display(self, text=""):
        display(HTML(self.create_page(text)))

def create_translator(initial_text=""):
    translator = TranslatorInterface()
    translator.display(initial_text)

if __name__ == "__main__":
    create_translator()
