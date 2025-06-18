# Importación de funciones necesarias
from .nlp_utils import detectar_intencion, extraer_fecha, es_afirmacion
import random  # Importamos la librería random para seleccionar respuestas aleatorias
# Definimos algunas respuestas iniciales para saludar al usuario
saludos_iniciales = [
    "Hola �� ¿Quieres ver el menú o hacer una reserva?",
    "¡Bienvenido! �� ¿Te muestro el menú o prefieres reservar?",
    "Hola, ¿en qué puedo ayudarte hoy? ¿Menú o reserva?",
    "¡Hola! �� ¿Deseas consultar el menú o hacer una reserva?"
]
# Respuestas de despedida cuando se ha realizado una reserva
despedidas_reserva = [
    "¡Gracias por tu visita! �� Que tengas un buen día.",
    "¡Reserva anotada! Disfruta tu jornada ��",
    "Perfecto, nos vemos el día acordado. ¡Cuídate!",
    "¡Todo listo! Te esperamos con gusto. ��"
]
# Respuestas de despedida cuando no se ha realizado una reserva
despedidas_sin_reserva = [
    "¡Gracias por tu visita! �� Que tengas un buen día.",
    "¡Hasta la próxima! ��",
    "Encantado de ayudarte. ¡Nos vemos!",
    "Que tengas un buen día. ¡Adiós!"
]

# Respuesta a ubicación
ubicación = "Calle Inventada, Nº12. Madrid"
    



# Función principal para gestionar las respuestas del chatbot
def generate_bot_response(user_input, session_id, memory):
   
    user_input = user_input.lower().strip()  # Normalizamos la entrada del usuario a minúsculas y eliminamos espacios innecesarios
    # Inicializamos la memoria de la sesión si es la primera vez que interactúan
    if session_id not in memory:
        memory[session_id] = {"estado": "inicio"}  # Si no existe la sesión, comenzamos en el estado "inicio"
    estado = memory[session_id]["estado"]  # Recuperamos el estado actual de la conversación
   # Definimos las posibles afirmaciones y despedidas que el bot puede reconocer
    afirmaciones = ["sí", "si", "claro", "por supuesto", "vale", "ok"]
    despedidas = ["adiós", "adios", "hasta luego", "nos vemos", "chao", "chau", "bye", "no gracias", "no, gracias", "no"]
    
    
       # --- Manejo de despedidas ---
    # Verificamos si el usuario ha solicitado despedirse
    # Sólo permitimos despedidas si no estamos en medio de una reserva
    if user_input.lower() in despedidas and estado not in [
        "esperando_dia", "esperando_personas", "esperando_nombre", "esperando_detalles"
    ]:
        memory[session_id]["estado"] = "despedida"  # Cambiamos el estado a "despedida"
        reserva = memory[session_id].get("reserva", {})  # Recuperamos la reserva si existe
       # Si existe una reserva, mostramos un resumen de la misma
        if reserva:
            resumen = (
                f"Reserva para {reserva.get('personas')} personas el {reserva.get('dia')}, "
                f"a nombre de {reserva.get('nombre')}. Detalles: {reserva.get('detalles', 'ninguno')}."
            )
            # Seleccionamos una despedida con el resumen de la reserva
            mensaje = random.choice(despedidas_reserva).format(resumen=resumen)
            return mensaje
        else:
            # Si no hay reserva, mostramos una despedida genérica
            return random.choice(despedidas_sin_reserva)
        
        
        
   # --- Manejo de afirmaciones "sí" ---
    if user_input in afirmaciones:
        if estado == "ofrecido_menu":
            memory[session_id]["estado"] = "esperando_dia"  # Si ya se ofreció el menú, preguntamos por la fecha
            return "Genial. ¿Para qué día quieres la reserva?"
        elif estado == "inicio":
            return "¿Puedes especificar si quieres ver el menú o hacer una reserva?"  # Preguntamos si desea menú o reserva
        else:
            return "Vale, dime más detalles por favor."
        
    # --- Manejo de ubicación ---  
    if any(palabra in user_input.lower() for palabra in ['ubicación', 'ubicacion', 'lugar', 'dónde', 'donde']):
        return ubicación
        
        
        
    # --- FLUJO PRINCIPAL: Manejo de solicitudes del usuario ---
    
    # Si el usuario menciona "menú", se le ofrece el menú
    if "menu" in user_input:
        memory[session_id]["estado"] = "ofrecido_menu"  # Actualizamos el estado a "ofrecido_menu"
        return "�� Aquí tienes el menú: - Ensalada mixta - Pizza margarita - Pasta carbonara - Tarta de queso. ¿Quieres hacer una reserva?"
    
   # Si el usuario menciona "reserva", comenzamos el flujo de reserva
    if "reserva" in user_input:
        memory[session_id]["estado"] = "esperando_dia"  # Actualizamos el estado a "esperando_dia"
        return "Perfecto. ¿Para qué día quieres hacer la reserva?"
    
   # --- Flujo reserva---
    # Si estamos esperando una fecha, guardamos la fecha y preguntamos por el número de personas
    if estado == "esperando_dia":
        memory[session_id]["estado"] = "esperando_personas"
        memory[session_id]["fecha"] = user_input
        return "¿Para cuántas personas será la reserva?"
    
   # Si estamos esperando el número de personas, lo guardamos y preguntamos por el nombre
    if estado == "esperando_personas":
        memory[session_id]["estado"] = "esperando_nombre"
        memory[session_id]["personas"] = user_input
        return "¿A nombre de quién estará la reserva?"
    
 # Si estamos esperando el nombre, lo guardamos y preguntamos por las preferencias
    if estado == "esperando_nombre":
        memory[session_id]["estado"] = "esperando_preferencias"
        memory[session_id]["nombre"] = user_input
        return "¿Desea una reserva en nuestra zona de patio o en el interior?"
    
   # Si estamos esperando preferencias las guardamos y preguntamos por los detalles de la reserva
    if estado == "esperando_preferencias":
        memory[session_id]["estado"] = "esperando_detalles"
        memory[session_id]["preferencias"] = user_input
        return "¿Hay algo que debamos tener en cuenta? Alergias, niños, etc."
    
   # Si estamos esperando detalles, completamos la reserva y mostramos un resumen
    if estado == "esperando_detalles":
        memory[session_id]["estado"] = "reserva_completa"
        memory[session_id]["detalles"] = user_input
        memory[session_id]["reserva"] = {
            "dia": memory[session_id].get("fecha"),
            "personas": memory[session_id].get("personas"),
            "nombre": memory[session_id].get("nombre"),
            "preferencias": memory[session_id].get("preferencias"),
            "detalles": memory[session_id].get("detalles")
        }
       # Resumen de la reserva y una respuesta final
        return (
            f"Reserva completa para {memory[session_id]['personas']} personas el {memory[session_id]['fecha']} en {memory[session_id]['preferencias']}  "
            f"a nombre de {memory[session_id]['nombre']}. Detalles: {memory[session_id]['detalles']}.\n"
            "¿Deseas hacer otra cosa?"
        )
        
   # Si no se detecta ninguna de las condiciones anteriores, respondemos con un saludo inicial aleatorio
    return random.choice(saludos_iniciales)

