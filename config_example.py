"""
Ejemplo de archivo de configuración
Copia este archivo como 'config.py' y ajusta los valores según tus necesidades
"""
import os

# =========== CONFIGURACIÓN OBLIGATORIA ===========
# Número de teléfono para recibir notificaciones (Formato internacional con +)
TELEFONO_DESTINO = "+59100000000"

# Paquetes a rastrear (formato: "nombre_descriptivo": "ID_SEGUIMIENTO")
PACKAGE_IDS = {
    "paquete1": "RP000000000MU",  # Ejemplo: RP + 11 dígitos + MU
    "paquete2": "RP111111111MU",
    # Agrega todos los paquetes que necesites
}

# =========== CONFIGURACIÓN OPCIONAL ===========
# True = Enviar notificaciones por WhatsApp, False = Solo mostrar en consola
NOTIFICACIONES_WHATSAPP = True

# =========== CONFIGURACIÓN AVANZADA ===========
# Ruta al archivo de credenciales de Firebase (No modificar a menos que sea necesario)
FIREBASE_CREDS = os.path.join(os.path.dirname(__file__), "firebase-creds.json")

# Directorio base del proyecto (No modificar)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =========== INSTRUCCIONES ===========
# 1. Guarda este archivo como "config.py"
# 2. Actualiza el número de teléfono y los paquetes
# 3. Asegúrate que tu archivo de credenciales de Firebase se llama "firebase-creds.json"
#    y está en la carpeta raíz del proyecto