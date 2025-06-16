import spacy

nlp = spacy.load("es_core_news_sm") 

INTENTOS = {
    "saludo": ["hola", "buenos días", "buenas tardes", "qué tal", "saludos", "cómo estás", "cómo te va", "qué onda"],
    "despedida": ["adiós", "hasta luego", "nos vemos", "chao", "hasta pronto", "cuídate"],
    "pregunta": ["cómo", "qué", "por qué", "dónde", "quién", "cuándo"],
}

def analizar_texto(texto):
    """Procesa el texto con spaCy y detecta la intención (saludo, pregunta, etc.)."""
    # Procesar el texto con spaCy
    doc = nlp(texto.lower())
       # Analizamos si alguna palabra del texto coincide con las palabras clave para cada intención
    for token in doc:
        for intent, keywords in INTENTOS.items():
            if token.text in keywords:
                return intent
            
    # Si no encontramos coincidencias exactas, usamos similitud semántica
    for intent, keywords in INTENTOS.items():
        for keyword in keywords:
            keyword_doc = nlp(keyword)
            similarity = doc.similarity(keyword_doc)
            if similarity > 0.7:  # Si la similitud es mayor a 0.7, lo consideramos una coincidencia
                return intent
    return "desconocido"  # Si no detectamos ninguna intención