import pywhatkit as kit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os
import sys
import time

# Redirigir la salida estándar y los errores para evitar mostrar mensajes en la consola
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

# Función para mostrar la ayuda
def mostrar_ayuda():
    print("""
    Uso del script: enviar_mensaje [opciones] <contacto/número> <mensaje>

    Opciones:
    /?, /help     Muestra esta ayuda.

    Argumentos:
    <contacto/número>    Puede ser el nombre del contacto guardado en WhatsApp o un número de teléfono con el código de país.
                        Ejemplo de número: +1234567890 (sin el símbolo '+').
    <mensaje>            El texto del mensaje que se enviará al contacto o número de teléfono especificado.

    Ejemplos de uso:
    1. Enviar un mensaje a un contacto guardado:
       enviar_mensaje "Nombre del Contacto" "Hola, este es un mensaje de prueba!"
    
    2. Enviar un mensaje a un número de teléfono:
       enviar_mensaje +1234567890 "Hola, este es un mensaje de prueba!"
    """)

# Función para enviar el mensaje
def enviar_mensaje(contacto_o_numero, mensaje):
    print("Trabajando en el envío automatizado...")

    # Usar pywhatkit para abrir WhatsApp Web y escribir el mensaje
    kit.sendwhatmsg_instantly(contacto_o_numero, mensaje)

    # Esperar unos segundos para asegurarse de que pywhatkit abra WhatsApp Web correctamente
    time.sleep(5)

    # Configuración para Microsoft Edge en modo headless (oculto)
    options = Options()
    options.use_chromium = True  # Usar Chromium para Edge

    # Ejecutar en modo headless para que no se muestre la ventana
    options.add_argument("--headless")  # Ejecutar en modo oculto
    options.add_argument("--disable-gpu")  # Necesario para evitar errores en modo headless
    options.add_argument("--disable-dev-shm-usage")  # Mejorar el rendimiento en entornos de contenedores
    options.add_argument("--no-sandbox")  # Evitar problemas de permisos en modo headless
    options.add_argument("--disable-infobars")  # Evitar mensajes de "controlado por Selenium"
    options.add_argument("--disable-extensions")  # Desactivar extensiones del navegador
    options.add_argument("--disable-crash-reporter")  # Desactivar el reporte de fallos de Edge
    options.add_argument("--remote-debugging-port=0")  # Desactivar DevTools y depuración
    options.add_argument("--log-level=3")  # Reducir la cantidad de mensajes de la consola

    # Iniciar Microsoft Edge con Selenium en modo headless
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

    try:
        # Cargar WhatsApp Web
        driver.get("https://web.whatsapp.com")

        # Esperar hasta que WhatsApp Web esté completamente cargado (reducir el tiempo de espera)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="6"]'))
        )

        # Escribir y enviar el mensaje
        message_box = driver.find_element(By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="6"]')
        message_box.send_keys(Keys.ENTER)

        print(f"Mensaje enviado a {contacto_o_numero}")

    except Exception as e:
        print("Trabajando en el envío automatizado...")

    finally:
        # Intentar cerrar el navegador de manera normal y forzar si es necesario
        driver.quit()

        # Forzar el cierre de Microsoft Edge si sigue abierto, redirigiendo la salida a NUL para evitar los mensajes en consola
        os.system("taskkill /f /im msedge.exe >nul 2>&1")  # Suprimir los mensajes de cierre del proceso

# Restaurar la salida estándar y errores después de completar el script
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

# Verificar los parámetros
if len(sys.argv) < 2:
    print("Error: Se requieren más argumentos. Usa '/?' o '/help' para ver las opciones.")
    sys.exit(1)

# Mostrar ayuda si se pasa el parámetro /? o /help
if sys.argv[1] in ["/?", "/help"]:
    mostrar_ayuda()
    sys.exit(0)

# Verificar que se proporcionen el contacto/número y el mensaje
if len(sys.argv) != 3:
    print("Error: Faltan argumentos. Usa '/?' o '/help' para ver las opciones.")
    sys.exit(1)

# Obtener los parámetros
contacto_o_numero = sys.argv[1]
mensaje = sys.argv[2]

# Enviar el mensaje
enviar_mensaje(contacto_o_numero, mensaje)
