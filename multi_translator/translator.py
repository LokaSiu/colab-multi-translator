# Save this as translator.py

from IPython.display import HTML, display

class TranslatorInterface:
    def __init__(self):
        # Previous JS code remains the same (self.js_code, self.js_code2, self.js_code3)

        self.html_template = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                /* Note the double curly braces for CSS rules */
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
                    margin-bottom: 30px;
                }}
                .title {{
                    color: #2196F3;
                    font-size: 24px;
                    margin-bottom: 10px;
                }}
                .subtitle {{
                    color: #666;
                    font-size: 16px;
                }}
                .input-section {{
                    margin-bottom: 25px;
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
                .language-select {{
                    margin-bottom: 15px;
                }}
                select {{
                    padding: 8px;
                    border-radius: 4px;
                    border: 1px solid #ddd;
                    font-size: 14px;
                    width: 200px;
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
