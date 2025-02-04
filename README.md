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
!git clone https://github.com/LokaSiu/colab-multi-translator.git
%cd colab-multi-translator
!pip install -e .

# After installation, run:
from multi_translator import create_translator
create_translator("Hello World!")
