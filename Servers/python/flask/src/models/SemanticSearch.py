import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime
import re

class SemanticSearchEnhancer:
    """
    Mejora la búsqueda semántica combinando sinopsis y palabras clave.
    """
    #En el model_name, se puede cambiar por cualquier otro modelo de embedding que se encuentre en HuggingFace.
    def __init__(self, model_name: str = 'distiluse-base-multilingual-cased-v1'):
        self.model = SentenceTransformer(model_name)
        self.answer_embeddings = None
        self.keyword_embeddings = None
        self.df = None

    def extract_keywords(self, text: str) -> str:
        """Extrae palabras clave del texto."""
        # Tokenización y eliminación de stopwords
        stop_words = set(stopwords.words('spanish'))
        tokens = word_tokenize(text.lower())
        keywords = [word for word in tokens if word not in stop_words]
        return ' '.join(keywords)

    def prepare_data(self, df: pd.DataFrame):
        """Prepara los datos generando embeddings de sinopsis y keywords."""
        # Combinar sinopsis con géneros
        enhanced_texts = [
            f"{row['answer']} "
            for _, row in df.iterrows()
        ]

        # Extraer y embeber keywords
        keywords = [self.extract_keywords(text) for text in enhanced_texts]

        # Generar embeddings
        print("Generando embeddings de las respuestas...")
        self.answer_embeddings = self.model.encode(enhanced_texts)
        print("Generando embeddings de keywords...")
        self.keyword_embeddings = self.model.encode(keywords)

        self.df = df
        return self

    def search(self, query: str, df: pd.DataFrame=None, top_k: int = 3,
              synopsis_weight: float = 0.7) -> List[Dict]:
        """
        Realiza búsqueda semántica mejorada combinando similitud de
        sinopsis y keywords.
        """
        # Generar embedding de la query
        query_embedding = self.model.encode([query])

        # Calcular similitudes
        synopsis_scores = cosine_similarity(query_embedding,
                                         self.answer_embeddings)[0]
        keyword_scores = cosine_similarity(query_embedding,
                                        self.keyword_embeddings)[0]

        # Combinar scores
        combined_scores = (synopsis_scores * synopsis_weight +
                         keyword_scores * (1 - synopsis_weight))

        # Obtener top_k resultados
        top_indices = np.argsort(combined_scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                'question': self.df.iloc[idx]['question'],
                'answer': self.df.iloc[idx]['answer'],
                'score': combined_scores[idx]
            })

        return results