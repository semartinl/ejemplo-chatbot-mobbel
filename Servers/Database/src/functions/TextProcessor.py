from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import nltk

# Descarga de recursos necesarios
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

class TextPreprocessor:

    @classmethod
    def preprocess(cls, text: str, lang='spanish') -> str:
        text = text.lower()
        # Tokenizar usando NLTK
        tokens = word_tokenize(text)
        # Eliminar stopwords usando NLTK
        stop_words = set(stopwords.words(lang))
        tokens = [t for t in tokens if t not in stop_words]

        return ' '.join(tokens)