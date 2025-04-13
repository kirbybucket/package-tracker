# 📦 Package Tracker

Sistema de seguimiento de paquetes hacia Bolivia con notificaciones WhatsApp en tiempo real.

## 🚀 Características

- ✅ Seguimiento automático de múltiples paquetes
- ✅ Notificaciones por WhatsApp cuando el paquete llega
- ✅ Gestión de paquetes desde interfaz de consola interactiva
- ✅ Almacenamiento de historial en Firestore
- ✅ Configuración personalizable
- ✅ Interfaz intuitiva con códigos de colores

## 📋 Requisitos previos

- Python 3.8 o superior
- Cuenta de Firebase con Firestore habilitado
- Archivo de credenciales de Firebase (`firebase-creds.json`)
- WhatsApp instalado en tu dispositivo

## 🛠️ Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/kirbybucket/package-tracker.git
   cd package-tracker
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Coloca tu archivo firebase-creds.json en la carpeta raíz del proyecto

4. Ejecuta el programa por primera vez para crear la configuración:
   ```bash
   python main.py
   ```

## ⚙️ Configuración

El archivo de configuración config.py se generará automáticamente en el primer inicio. También puedes crear uno manualmente basado en config_example.py:

```python
import os

# Número de teléfono para recibir notificaciones
TELEFONO_DESTINO = "+591XXXXXXXX"

# Paquetes a rastrear (formato: "nombre_descriptivo": "ID_SEGUIMIENTO")
PACKAGE_IDS = {
    "mi_paquete": "RP123456789MU",
    # Agrega más paquetes aquí
}

# Activar/desactivar notificaciones WhatsApp
NOTIFICACIONES_WHATSAPP = True

# Configuración avanzada (no modificar)
FIREBASE_CREDS = os.path.join(os.path.dirname(__file__), "firebase-creds.json")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
```

## 🖥️ Uso

1. Ejecuta el programa principal:
   ```bash
   python main.py
   ```

2. Navega por el menú interactivo:
   - Gestionar paquetes (agregar/eliminar)
   - Ver estado de paquetes
   - Iniciar seguimiento automático
   - Configuración avanzada

3. Para el seguimiento automático, el programa verificará periódicamente el estado de tus paquetes y enviará notificaciones vía WhatsApp cuando lleguen.

## 📂 Estructura del proyecto

```
package-tracker/
├── core/                 # Funcionalidad principal
│   ├── config_manager.py # Gestión de configuración
│   ├── messenger.py      # Envío de notificaciones
│   └── tracker.py        # Seguimiento de paquetes
├── firestore/            # Integración con Firebase
│   ├── create_collection.py
│   └── get_packages.py
├── utils/                # Utilidades
│   ├── helpers.py        # Funciones auxiliares
│   └── ui.py             # Interfaz de usuario
├── config_example.py     # Ejemplo de configuración
├── main.py               # Punto de entrada
└── requirements.txt      # Dependencias
```

## 🔐 Seguridad

- El archivo firebase-creds.json contiene credenciales sensibles y está incluido en .gitignore
- No compartas tu configuración (`config.py`) ya que contiene tu número telefónico personal

## 🤝 Contribución

1. Haz un fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/amazing-feature`)
3. Haz commit de tus cambios (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 🔧 Solución de problemas

- **WhatsApp no envía mensajes**: Asegúrate de tener WhatsApp Web configurado y autenticado
- **Error de Firebase**: Verifica que tu archivo de credenciales sea válido y esté en la ubicación correcta
- **ID de paquete no reconocido**: Los IDs deben seguir el formato `RP` + 11 dígitos + `MU`

---

⭐ ¡Si encuentras útil este proyecto, no dudes en darle una estrella! ⭐