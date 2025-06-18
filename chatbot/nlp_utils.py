# Importación de librerías necesarias:

import spacy  # Librería para el procesamiento del lenguaje natural
import re  # Librería para expresiones regulares, usada para limpiar el texto
import dateparser  # Librería para el análisis y parseo de fechas en texto
from dateparser.search import search_dates
from datetime import datetime,timedelta
import difflib
import logging
from logging import Logger

# Cargamos el modelo de lenguaje en español de spaCy
nlp = spacy.load("es_core_news_md")

# Definimos una lista de posibles saludos que el bot puede reconocer
SALUDOS = ["hola", "buenos días", "buenas tardes", "qué tal", "hey", "saludos"]

# Definimos una lista de posibles afirmaciones que el bot puede reconocer
AFIRMACIONES = ["si", "claro", "vale", "de acuerdo", "por supuesto", "si quiero", "ok"]
NUMEROS_PALABRAS = {
    "uno": 1, "una": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
    "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
    "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15,
    "dieciséis": 16, "diecisiete": 17, "dieciocho": 18, "diecinueve": 19,
    "veinte": 20, "veintiuno": 21, "veintidós": 22, "veintitrés": 23,
    "veinticuatro": 24, "veinticinco": 25,
    "pareja": 2, "una pareja": 2
}

# Función para detectar la intención del usuario en base al texto introducido

def detectar_intencion(texto):
    """
    Esta función detecta si el texto introducido por el usuario corresponde a un saludo.
    Si se detecta un saludo, devuelve 'saludo'; de lo contrario, devuelve 'desconocida'.
    """
    texto = texto.lower()  # Convertimos el texto a minúsculas para normalizar la comparación
    for saludo in SALUDOS:
        if saludo in texto:  # Si uno de los saludos está presente en el texto
            return "saludo"  # Retornamos 'saludo' si se detecta un saludo
    return "desconocida"  # Si no se detecta un saludo, retornamos 'desconocida'

# Función para determinar si el texto del usuario contiene una afirmación

def es_afirmacion(texto):
    """
    Esta función verifica si el texto del usuario contiene alguna afirmación,
    permitiendo variaciones y utilizando similitud de texto para reconocer afirmaciones
    incluso si el usuario escribe algo como "claro que sí" o "sí por supuesto".
    """
    texto = texto.strip().lower()  # Normalizamos el texto a minúsculas

    # Normalizamos 'sí' a 'si'
    texto = texto.replace("sí", "si")

    # Eliminar palabras repetidas y limpiar espacios extra
    texto = " ".join(sorted(set(texto.split()), key=texto.split().index))  # Eliminar repeticiones
    
    # 1. Coincidencia exacta directa
    if texto in AFIRMACIONES:
        return True

    # 2. Contiene alguna palabra clave
    for afirm in AFIRMACIONES:
        if afirm in texto:
            return True

    # 3. Similitud con alguna afirmación (por si acaso)
    for afirm in AFIRMACIONES:
        similitud = difflib.SequenceMatcher(None, texto, afirm).ratio()
        if similitud > 0.8:
            return True

    return False

# Función para extraer una fecha de un texto dado

def limpiar_input_fecha(texto):
    texto = texto.lower().strip()
    
    # Detecta "el jueves que viene" y cambia por "próximo jueves"
    match = re.match(r"(el\s+)?(?P<dia>\w+)\s+que\s+viene", texto)
    if match:
        dia = match.group("dia")
        texto = f"próximo {dia}"
    
    # "este jueves" → "jueves"
    texto = re.sub(r"\beste\b\s+(lunes|martes|miércoles|jueves|viernes|sábado|domingo)\b", r"", texto)
    
    # Casos simples: "el próximo lunes" → "próximo lunes"
    texto = re.sub(r"\bel\b", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    
    return texto

def extraer_fecha(user_input):
    limpio = limpiar_input_fecha(user_input)
    print(f"[DEBUG] Fecha interpretada: '{limpio}'")
    
    # Usamos search_dates para detectar fechas relativas
    resultados = search_dates(
         limpio,
         languages=["es"],
         settings={
             "PREFER_DATES_FROM": "future",
             "RELATIVE_BASE": datetime.now()
         }
    )

    if not resultados:
        return False, None

    # Tomamos la primera fecha que encuentre
    _, fecha = resultados[0]  # Obviamos el primer valor (que es el texto original)
    
    # Validación de la fecha para asegurar que sea razonable
    hoy = datetime.now()
    
    if fecha.year < hoy.year - 1 or fecha.year > hoy.year + 2:
        return False, None

    return True, fecha  # Devuelvo la fecha sin formatear

def formatear_fecha_es(fecha):
    # Diccionarios para los días y meses en español
    dias = {
        "Monday": "lunes", "Tuesday": "martes", "Wednesday": "miércoles",
        "Thursday": "jueves", "Friday": "viernes", "Saturday": "sábado", "Sunday": "domingo"
    }  
    meses = {
        "January": "enero", "February": "febrero", "March": "marzo",
        "April": "abril", "May": "mayo", "June": "junio", "July": "julio",
        "August": "agosto", "September": "septiembre", "October": "octubre",
        "November": "noviembre", "December": "diciembre"
    }
    
    # Convertir la fecha al formato adecuado en español
    dia_en = fecha.strftime("%A")
    mes_en = fecha.strftime("%B")
    dia = dias[dia_en]
    mes = meses[mes_en]  
    
    return f"{dia} {fecha.day} de {mes}"


def extraer_personas(texto):
    texto = texto.lower().strip()

    # Primero intentamos encontrar un número escrito con dígitos
    match_num = re.search(r"\b(\d{1,3})\b", texto)
    if match_num:
        num = int(match_num.group(1))
        if 1 <= num <= 25:
            return True, num
        else:
            return False, None  # Fuera de rango

    # Si no hay dígitos, buscamos palabras
    for palabra, valor in NUMEROS_PALABRAS.items():
        if palabra in texto:
            if 1 <= valor <= 25:
                return True, valor
            else:
                return False, None  # También fuera de rango

    # Nada útil encontrado
    return False, None
import re

def limpiar_y_validar_telefono(user_input):
    """
    Limpia el input y valida si es un número de teléfono español válido (9 dígitos).
    Devuelve (True, telefono_limpio) si es válido, o (False, None) si no.
    """
    if not user_input:
        return False, None

    # Convertimos a string, eliminamos todo excepto dígitos
    telefono_limpio = re.sub(r"\D", "", str(user_input))

    # Validamos que tenga exactamente 9 dígitos
    if len(telefono_limpio) == 9:
        return True, telefono_limpio
    return False, None

import json

def normalizar_mensaje(raw_message, session_id=None, logger=None):
    """
    Convierte un mensaje entrante en un string plano.
    Si es un dict tipo {"message": "texto"}, extrae el valor.
    Si es un JSON stringificado, lo parsea.
    """
    try:
        if isinstance(raw_message, str) and raw_message.strip().startswith("{"):
            # Intenta decodificar si parece JSON
            raw_message = json.loads(raw_message)
            if logger and session_id:
                logger.debug(f"[{session_id}] Mensaje JSON decodificado correctamente.")
    except Exception as e:
        if logger and session_id:
            logger.warning(f"[{session_id}] No se pudo parsear el JSON: {e}")
        pass

    if isinstance(raw_message, dict):
        return str(raw_message.get("message", "")).strip()
    return str(raw_message).strip()

