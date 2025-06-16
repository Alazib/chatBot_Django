from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Usuario, Conversacion, Mensaje, Estado
from .chatbot_logic import generate_bot_response
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.shortcuts import render

def chat_view(request):
    return render(request, 'chatbot/chat.html')

@csrf_exempt
def enviar_mensaje(request):
    if request.method == 'POST':
        datos = json.loads(request.body)

        usuario_id = datos.get('usuario_id')
        mensaje_usuario = datos.get('mensaje')

        usuario = get_object_or_404(Usuario, id=usuario_id)

        # Obtener conversación activa o crear una nueva
        conversacion = Conversacion.objects.filter(usuario=usuario, fecha_fin__isnull=True).first()
        if not conversacion:
            conversacion = Conversacion.objects.create(usuario=usuario)
            Estado.objects.create(conversacion=conversacion, estado_actual='inicial')

        # Guardar mensaje del usuario
        Mensaje.objects.create(conversacion=conversacion, texto=mensaje_usuario, remitente='usuario')

        # Obtener respuesta del chatbot
        respuesta_chatbot = generate_bot_response(mensaje_usuario)

        # Guardar mensaje del chatbot
        Mensaje.objects.create(conversacion=conversacion, texto=respuesta_chatbot, remitente='bot')

        return JsonResponse({'respuesta': respuesta_chatbot})

    return JsonResponse({'error': 'Solo se permiten solicitudes POST.'}, status=400)
