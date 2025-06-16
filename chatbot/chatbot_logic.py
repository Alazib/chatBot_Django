
def generate_bot_response(user_message):
    
    user_message = user_message.lower().strip()

    if user_message in ['hola', 'buenos días', 'buenas']:
        return '¡Hola! ¿Cómo puedo ayudarte?'
    elif 'adiós' in user_message or 'hasta luego' in user_message:
        return 'Adiós. ¡Que tengas un buen día!'
    elif 'gracias' in user_message:
        return '¡De nada! ¿En qué más puedo ayudarte?'
    else:
        return 'Lo siento, no he entendido tu mensaje. ¿Puedes reformularlo?'
