# Colab Multi-Translator

An open-source educational project that demonstrates how to create a multi-translator interface for Google Colab. This project allows users to compare translations from Google Translate, DeepL, and Baidu Translate simultaneously while learning about web interfaces in Colab environments.

## Features

- Compare translations from multiple services simultaneously:
  - Google Translate
  - DeepL
  - Baidu Translate
- Automatic language detection (Chinese ↔ English)
- Responsive design that adapts to screen size
- Keyboard shortcuts for enhanced productivity
- Clean and intuitive user interface
- Built specifically for Google Colab environment

## Quick Start

```python
# Clone the repository
!git clone https://github.com/LokaSiu/colab-multi-translator.git
%cd colab-multi-translator

# Install the package in development mode
!pip install -e .

# Restart the runtime (necessary after installing new packages)
import IPython
IPython.Application.instance().kernel.do_shutdown(True)

# After restart, import and use:
from multi_translator import create_translator

# Test the translator with sample text
create_translator("Hello World!")
