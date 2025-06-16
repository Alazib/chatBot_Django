# Importación de librerías necesarias:

import spacy  # Librería para el procesamiento del lenguaje natural
import re  # Librería para expresiones regulares, usada para limpiar el texto
import dateparser  # Librería para el análisis y parseo de fechas en texto

# Cargamos el modelo de lenguaje en español de spaCy
nlp = spacy.load("es_core_news_md")

# Definimos una lista de posibles saludos que el bot puede reconocer
SALUDOS = ["hola", "buenos días", "buenas tardes", "qué tal", "hey", "saludos"]

# Definimos una lista de posibles afirmaciones que el bot puede reconocer
AFIRMACIONES = ["sí", "claro", "vale", "de acuerdo", "por supuesto", "sí quiero", "ok"]

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
    Esta función verifica si el texto del usuario contiene alguna afirmación reconocida.
    Si el texto contiene alguna de las palabras en la lista AFIRMACIONES, devuelve True.
    """
    texto = texto.lower()  # Convertimos el texto a minúsculas para normalizar la comparación
    return any(af in texto for af in AFIRMACIONES)  # Comprobamos si alguna afirmación está en el texto

# Función para extraer una fecha de un texto dado

def extraer_fecha(user_input):
    """
    Esta función intenta extraer una fecha del texto introducido por el usuario.
    Primero elimina palabras irrelevantes como 'el', 'la', 'del', etc.
    Luego usa la librería dateparser para intentar parsear la fecha.
    Si la fecha es válida, se devuelve en formato: 'Día de la semana DD de Mes'.
    Si no se puede extraer una fecha, retorna None.
    """
    # Eliminamos palabras innecesarias del texto usando expresiones regulares
    frase_limpia = re.sub(r"\bel\b|\bla\b|\blo\b|\bdel\b|\bde\b", "", user_input.lower())
    # Usamos dateparser para intentar extraer la fecha del texto limpio
    fecha = dateparser.parse(frase_limpia.strip(), languages=["es"])
    if fecha:
        # Si se encontró una fecha, la formateamos y la devolvemos
        return fecha.strftime("%A %d de %B")
    return None  # Si no se pudo extraer la fecha, devolvemos None