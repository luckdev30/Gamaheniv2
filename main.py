import os
import random
import webbrowser
import wikipedia
import threading
from gtts import gTTS
from playsound import playsound
import time
import pyttsx3
import pywhatkit
import datetime
import speech_recognition as sr
import requests

#*Inicializar el motor de síntesis de voz
engine = pyttsx3.init()

#*Configurar la voz para que suene más natural
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  #*Índice 1 para una voz más natural
engine.setProperty('voice', 'spanish') #*configurar el idoma de la voz en español 
engine.setProperty('rate', 150)#*Ajustar la velocidad de habla (0.5 para lento, 1.0 para normal, 2.0 para rápido, etc.)


#*Establecer el idioma de Wikipedia a español
wikipedia.set_lang('es')

#*API Key de OpenWeatherMap (reemplazar la clave)
API_KEY = 'La clave Api a utilizar'

#*Se crea una clase para el asistente 
class Assistant:
    def __init__(self):
        self.r = sr.Recognizer()
        self.chistes = [
            "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
            "¿Qué le dice una abeja a otra abeja cuando se encuentran? ¡Hola, abeja!",
            "¿Cómo se llama el campeón de buceo japonés? Tokofondo.",
            "¿Por qué estás hablando con esas zapatillas? Porque pone Converse-ation",
            "¿Cuál es el colmo de un jardinero? Que su esposa se llame Rosa y su hija Margarita.",
        ]
#*Funcion para hablar
    def hablar(self, texto):
        print(texto)
        engine.say(texto)
        engine.runAndWait()
#*Funcion escuchar
    def escuchar(self):
        with sr.Microphone() as source:
            print("Escuchando...")
            audio = self.r.listen(source, phrase_time_limit=6)

            try:
                query = self.r.recognize_google(audio, language="es-ES")
                print("Has dicho: " + query)
                return query
            except sr.UnknownValueError:
                print("No se ha podido entender la voz")
                return ""
#*Funcion del temporizador para detener el asistente
    def iniciar_temporizador(self, duracion):
        def temporizador():
            mensaje_temporizador = f"Temporizador iniciado. Se detendrá en {duracion} segundos."
            self.hablar(mensaje_temporizador)
            time.sleep(duracion)
            mensaje_final = f"¡El tiempo programado de {duracion} segundos ha concluido!"
            self.hablar(mensaje_final)

        temporizador_hilo = threading.Thread(target=temporizador)
        temporizador_hilo.start()
#*Funcion para la conversion de unidades
    def convertir_unidades(self, query):
        unidades = {
            "metros a pies": 3.281,
            "pies a metros": 0.305,
            "kilómetros a millas": 0.621,
            "millas a kilómetros": 1.609,
            #*puedes agregar más conversiones según sea necesario
        }
#*Bucle para la conversion de factores
        for conversion, factor in unidades.items():
            if conversion in query:
                cantidad = float(query.replace(conversion, ""))
                resultado = cantidad * factor
                return f"{cantidad} {conversion} es igual a {resultado:.2f}"

        return "Lo siento, no puedo realizar esa conversión."
#*Funcion para obtener el clima usando la API
    def obtener_clima(self, ciudad):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric"
        respuesta = requests.get(url).json()
        if respuesta["cod"] == 200:
            clima = respuesta["main"]["temp"]
            descripcion = respuesta["weather"][0]["description"]
            return f"El clima en {ciudad} es de {clima} grados Celsius con {descripcion}."
        else:
            return "No se pudo obtener el clima para esa ciudad. Verifica el nombre de la ciudad e intenta de nuevo."
#*Funcion de bienvenida
    def bienvenida(self):
        texto_bienvenida = "Hola, soy Gamaeni, tu asistente virtual personal, ¿en qué puedo ayudarte?"
        self.hablar(texto_bienvenida)
#*Funcion para buscar en youtube
    def buscar_en_youtube(self, query):
        search_query = query[18:]
        print("Buscando en YouTube: " + search_query)
        pywhatkit.playonyt(search_query)
        respuesta = "Buscando en YouTube " + search_query
        self.hablar(respuesta)
#*Funcion para buscar en google
    def buscar_en_google(self, query):
        search_query = query[17:]
        print("Buscando en Google: " + search_query)
        pywhatkit.search(search_query)
        respuesta = "Buscar en Google " + search_query
        self.hablar(respuesta)
#*Funcion para enviar mensajes
    def enviar_mensaje(self, query):
        message = query[25:]
        print("Enviando mensaje de WhatsApp a Mauricio: " + message)
        pywhatkit.sendwhatmsg("+595981457154", message, datetime.datetime.now().hour, datetime.datetime.now().minute + 1)
        respuesta = "Enviando mensaje de WhatsApp a Mauricio"
        self.hablar(respuesta)
#*Funcion para mostrar hora
    def mostrar_hora(self):
        now = datetime.datetime.now()
        hora_actual = now.strftime("%H:%M:%S")
        respuesta = "La hora actual es " + hora_actual + ". ¿Deseas algo más?"
        self.hablar(respuesta)
#*Funcion para mostrar fecha
    def mostrar_fecha(self):
        now = datetime.datetime.now()
        fecha_actual = now.strftime("%d de %B de %Y")
        respuesta = "La fecha actual es " + fecha_actual + ". ¿Deseas algo más?"
        self.hablar(respuesta)
#*funcion para apagar el asistente
    def apagar_asistente(self):
        texto = "Espero haber sido de ayuda, nos vemos. Adiós."
        self.hablar(texto)
        exit()
#*funcion para hacer busquedas en sitios web
    def abrir_sitio_web(self, query):
        website = query[6:]
        print("Abriendo sitio web: " + website)
        webbrowser.open("https://" + website)
        respuesta = "Abriendo sitio web " + website
        self.hablar(respuesta)
#*Funcion para los chistes
    def contar_chiste(self):
        joke = random.choice(self.chistes)
        self.hablar(joke)
#*Funcion para las respuestas
    def obtener_respuesta(self, query):
        respuesta = "No te he entendido, ¿puedes volver a repetirlo?"
        if query in opciones_funciones:
            respuesta = opciones_funciones[query](query)
        return respuesta

#*Diccionario para mapear las intenciones del usuario con las funciones correspondientes
opciones_funciones = {
    "Buscar en YouTube": Assistant.buscar_en_youtube,
    "Buscar en Google": Assistant.buscar_en_google,
    "Enviar mensaje a Mauricio": Assistant.enviar_mensaje,
    "Mostrar hora": Assistant.mostrar_hora,
    "Mostrar fecha": Assistant.mostrar_fecha,
    "Apagar asistente": Assistant.apagar_asistente,
    "Abrir": Assistant.abrir_sitio_web,
    "Cuéntame un chiste": Assistant.contar_chiste,
    #*Agregar más intenciones y funciones según sea necesario
}

if __name__ == "__main__":
    assistant = Assistant()
    assistant.bienvenida()

    while True:
        query = assistant.escuchar()

        if query:
            respuesta = assistant.obtener_respuesta(query)
            #*Utilizamos gTTS para convertir el texto a voz en español
            tts = gTTS(text=respuesta, lang='es')
            tts.save('respuesta.mp3')
            os.system('mpg321 respuesta.mp3')  #*Reproducimos el audio
