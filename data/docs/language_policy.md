# Language Handling Policy: Call and Survey Text
Supported languages: English, Hindi, Kannada, Tamil, Telugu, Malayalam, Marathi, Bengali, Gujarati, Punjabi.
Rules:
- Detect language first; store it in language_code.
- Sentiment and journey are classified in the ORIGINAL language. English translations are produced only for display in dashboards.
- Hinglish (Hindi in Latin script) is treated as Hindi.
- Code-mixed text uses the language of the majority of words.
- Budget note: non-English text uses more tokens per word, so cost estimates are calculated per language.