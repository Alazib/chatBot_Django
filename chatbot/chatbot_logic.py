from .nlp_utils import analizar_texto

def generate_bot_response(user_message):
    
    """Devuelve una respuesta según la intención detectada dinámicamente."""
    intent = analizar_texto(user_message)
       # Respuestas para diferentes intenciones
    responses = {
        "saludo": "¡Hola! ¿Cómo puedo ayudarte?",
        "despedida": "¡Hasta luego! Que tengas un buen día.",
        "pregunta": "¡Parece que tienes una pregunta! ¿En qué puedo ayudarte?",
        "desconocido": "No entiendo tu mensaje, ¿puedes reformularlo?",
    }

    return responses.get(intent, "No entiendo tu mensaje, ¿puedes reformularlo?")


