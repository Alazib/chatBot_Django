import json  # Importa la biblioteca json para trabajar con datos en formato JSON.
from django.http import JsonResponse  # Importa JsonResponse para devolver respuestas JSON a las solicitudes HTTP.
from django.shortcuts import render  # Importa render para renderizar plantillas HTML en Django.
from django.views.decorators.csrf import csrf_exempt  # Importa csrf_exempt para permitir solicitudes POST sin validación CSRF.
from .chatbot_logic import generate_bot_response # Importa la función get_response que maneja la lógica del chatbot.

# Memoria por sesión simulada
# Aquí almacenamos el estado de cada sesión para simular la memoria del chatbot.
session_memory = {}

def chatbot_view(request):
    """
    Esta vista se encarga de renderizar la plantilla HTML del chatbot, lo que permite 
    a los usuarios interactuar con el chatbot a través de una interfaz web.
    """
    return render(request, "chatbot/chat.html")  # Renderiza la plantilla "chat.html" para el frontend.

@csrf_exempt  # Decora la vista para deshabilitar la protección CSRF en esta función específica.
def chatbot_api(request):
    """
    Este endpoint maneja las solicitudes POST del usuario para interactuar con el chatbot.
    Recibe el mensaje del usuario y la session_id, y devuelve la respuesta del chatbot.
    """
    if request.method == "POST":  # Verifica que la solicitud sea de tipo POST.
        try:
            data = json.loads(request.body)  # Intenta cargar los datos JSON del cuerpo de la solicitud.
            print(data)
            user_message = data.get("mensaje", "").strip()  # Obtiene el mensaje del usuario.
            session_id = data.get("session_id", "default")  # Obtiene el ID de la sesión o usa "default" si no se proporciona.

            if not user_message:  # Si el mensaje está vacío.
                return JsonResponse({"response": "No recibí ningún mensaje."}, status=400)  # Responde con un error 400 si no hay mensaje.

            bot_response = generate_bot_response(user_message, session_id, session_memory)  # Llama a la función generate_bot_response para obtener la respuesta del bot.

            return JsonResponse({"response": bot_response})  # Devuelve la respuesta del bot en formato JSON.

        except json.JSONDecodeError:  # Si ocurre un error al intentar decodificar los datos JSON.
            return JsonResponse({"response": "Error: JSON no válido."}, status=400)  # Devuelve un error 400 si el JSON no es válido.

    return JsonResponse({"response": "Método no permitido"}, status=405)  # Si el método HTTP no es POST, devuelve un error 405 (Método no permitido).
