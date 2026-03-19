# BritEng Corrector

BritEng Corrector is an AI-powered text correction system that improves grammar and spelling while ensuring output follows **UK English standards**. It also supports **automatic US-to-UK conversion** and offers a second mode for **rephrasing text** to improve clarity and fluency.

## Features

- Corrects grammar and spelling mistakes
- Converts US English to UK English
- Supports two modes:
  - **Correction Mode** for precise fixes
  - **Rephrase Mode** for improved clarity and fluency
- Uses LLM-based validation for better output quality
- Includes a custom US-to-UK dictionary
- Available through:
  - **Streamlit web app**
  - **Flask REST API**

## Tech Stack

- Python
- LangChain
- Gemini 2.0 Flash
- Flask
- Streamlit

## How It Works

1. User enters text
2. The system identifies grammar/spelling issues
3. US English words and spellings are converted to UK English where needed
4. Based on the selected mode, the text is either:
   - corrected with minimal changes, or
   - rephrased for better readability
5. The final output is validated
