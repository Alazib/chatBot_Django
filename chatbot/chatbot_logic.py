import logging
from datetime import datetime
from .models import Reserva
import dateparser
from .nlp_utils import detectar_intencion, extraer_fecha, es_afirmacion, extraer_personas, limpiar_y_validar_telefono, normalizar_mensaje
import re

# Configura el logger
logger = logging.getLogger("chatbot")
logger.setLevel(logging.DEBUG)

# Estados como constantes
STATE_SALUDO = 'saludo'
STATE_VER_MENU = 'ver_menu'
STATE_RESERVA = 'reserva'
STATE_NOMBRE = 'nombre'
STATE_FECHA = 'fecha'
STATE_PERSONAS = 'personas'
STATE_ALERGIAS = 'alergias'
STATE_TELEFONO = 'telefono'
STATE_CONFIRMACION = 'confirmacion'
STATE_DESPEDIDA = 'despedida'

def generate_bot_response(user_message, session_id, session_memory):
    try:        
        message_content = normalizar_mensaje(user_message, session_id, logger)
        logger.debug(f"[{session_id}] Contenido normalizado: {message_content} | Tipo: {type(message_content)}")

        state = session_memory.get('state', STATE_SALUDO)
        #logger.debug(f"[{session_id}] Estado actual: {state} | Mensaje recibido: {user_message}")
        logger.debug(f"[{session_id}] Estado actual: {state} | Input: {message_content} | Memoria: {session_memory}")
        responses = {
            STATE_SALUDO: "¡Bienvenido! ¿Deseas ver nuestro menú o prefieres hacer una reserva?",
            STATE_VER_MENU: "Aquí tienes nuestro menú. ¿Quieres reservar una mesa ahora?",
            STATE_RESERVA: "Perfecto, comencemos con tu reserva. ¿Cómo te llamas?",
            STATE_FECHA: "Gracias {nombre}. ¿Para qué día te gustaría reservar? (Por ejemplo: 'mañana', '15 de julio')",
            STATE_PERSONAS: "Entendido. ¿Para cuántas personas será la reserva? (Máximo 25 personas)",
            STATE_ALERGIAS: "¿Algún comensal tiene alergias alimentarias o necesidades especiales que debamos conocer?",
            STATE_TELEFONO: "Necesitamos un número de contacto para confirmar tu reserva (9 dígitos, por ejemplo: 612345678)",
            STATE_CONFIRMACION: "✅ Reserva confirmada! ¿Necesitas algo más?",
            STATE_DESPEDIDA: "¡Gracias por elegirnos! Esperamos verte pronto. ¡Buen día!"
}
        if state == STATE_SALUDO:
            if 'menu' in message_content.lower():
                session_memory['state'] = STATE_VER_MENU
                return responses[STATE_VER_MENU]
            elif 'reserva' in message_content.lower() or es_afirmacion(message_content):
                session_memory['state'] = STATE_RESERVA
                return responses[STATE_RESERVA]
            return responses[STATE_SALUDO]

        elif state == STATE_VER_MENU:
            if 'reserva' in message_content.lower() or es_afirmacion(message_content):
                session_memory['state'] = STATE_RESERVA
                print(f"[{session_id}] PAsa a Reserva??: {message_content}")
                return responses[STATE_RESERVA]
                
            return responses[STATE_VER_MENU]

        elif state == STATE_RESERVA:
            print(f"[{session_id}] Estado user_message: {message_content}")
            session_memory['nombre'] = message_content
            nombre= session_memory['nombre']
            session_memory['state'] = STATE_FECHA
            return f"Gracias {nombre}. ¿Para qué día te gustaría reservar? (Por ejemplo: 'mañana', '15 de julio')"#responses[STATE_FECHA]


        elif state == STATE_FECHA:
            
            valido, fecha = extraer_fecha(message_content)
            if not valido:
                logger.warning(f"[{session_id}] Fecha inválida: {message_content}")
                return "No entendí la fecha. Por favor usa un formato como '10 de mayo' o 'próximo lunes'"
    
            #session_memory['fecha'] = fecha
            session_memory['fecha'] = fecha.isoformat()  # o .strftime("%Y-%m-%d")
            print(f"[{session_id}] Fecha válida: {message_content}")
            session_memory['state'] = STATE_PERSONAS  # Pasar a personas después de fecha válida
            return responses[STATE_PERSONAS]  # "Perfecto, ¿Cuántas personas asistirán?"

        elif state == STATE_PERSONAS:  # Nuevo bloque para manejar número de personas
            valido, personas = extraer_personas(message_content)
            if not valido:
                return "Por favor indica un número entre 1 y 25 personas"
    
            session_memory['personas'] = personas
            session_memory['state'] = STATE_ALERGIAS
            return responses[STATE_ALERGIAS]

        elif state == STATE_ALERGIAS:
            session_memory['alergias'] = message_content
            session_memory['state'] = STATE_TELEFONO
            return responses[STATE_TELEFONO]

        elif state == STATE_TELEFONO:
            valido, telefono = limpiar_y_validar_telefono(message_content)
            if valido:
                session_memory['telefono'] = telefono
                session_memory['state'] = STATE_CONFIRMACION
                return responses[STATE_CONFIRMACION]
            else:
                return "Por favor, proporciona un número de teléfono válido."

        elif state == STATE_CONFIRMACION:
            nombre = session_memory.get('nombre', 'Anónimo')
            #fecha = session_memory.get('fecha')
            numero_personas = session_memory.get('personas')
            alergias = session_memory.get('alergias', '')
            telefono = session_memory.get('telefono')

            #fecha_str = fecha.strftime("%d/%m/%Y %H:%M") if fecha else "Fecha no proporcionada"
            fecha_str = session_memory.get('fecha')
            fecha_dt = datetime.fromisoformat(fecha_str) if fecha_str else None
            fecha_str = fecha_dt.strftime("%d/%m/%Y %H:%M") if fecha_dt else "Fecha no proporcionada"

            # Crear la reserva en la base de datos
            Reserva.objects.create(
                nombre=nombre,
                fecha=fecha_dt,
                numero_personas=numero_personas,
                alergias=alergias,
                telefono=telefono,
            )

            logger.info(f"[{session_id}] Reserva confirmada para {numero_personas} personas.")

            session_memory.clear()
            session_memory['state'] = STATE_SALUDO
            return f"¡Gracias! Tu reserva para {numero_personas} personas ha sido confirmada para el {fecha_str}."

        elif state == STATE_DESPEDIDA:
            return responses[STATE_DESPEDIDA]

        return "Lo siento, no entiendo esa solicitud."

    except Exception as e:
        logger.exception(f"[{session_id}] Error en el procesamiento del mensaje: {e}")
        session_memory['state'] = STATE_SALUDO
        return "Algo salió mal procesando tu mensaje. ¿Podrías intentarlo de nuevo?"