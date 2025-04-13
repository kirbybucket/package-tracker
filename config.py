"""
Archivo de configuración principal
Este archivo será generado automáticamente si no existe
"""
import os

# Configuración obligatoria
TELEFONO_DESTINO = "+59112345678"
PACKAGE_IDS = {
    "micas_transparentes": "RP433122453MU",
    "micas_negras": "RP433246807MU",
    "micas_ivory": "RP433191578MU",
    "micas_dragon": "RP433091892MU",
    "deckbox": "RP125534746MU",
}

# Configuración opcional (valores por defecto)
NOTIFICACIONES_WHATSAPP = True

# Rutas de sistema (No modificar a menos que sea necesario)
FIREBASE_CREDS = os.path.join(os.path.dirname(__file__), "firebase-creds.json")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))