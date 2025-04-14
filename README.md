# 📦 Package Tracker

Sistema de seguimiento de paquetes hacia Bolivia con notificaciones WhatsApp en tiempo real.

## 🚀 Características

- ✅ Seguimiento automático de múltiples paquetes
- ✅ Notificaciones por WhatsApp cuando el paquete llega
- ✅ Gestión de paquetes desde interfaz de consola interactiva
- ✅ Almacenamiento de historial en Firestore
- ✅ Configuración personalizable
- ✅ Intervalo configurable entre verificaciones
- ✅ Interfaz intuitiva con códigos de colores

## 📋 Requisitos previos

- Python 3.8 o superior
- Cuenta de Firebase con Firestore habilitado
- Archivo de credenciales de Firebase (`firebase-creds.json`)
- WhatsApp instalado en tu dispositivo

## 🛠️ Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/package-tracker.git
   cd package-tracker
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Coloca tu archivo `firebase-creds.json` en la carpeta raíz del proyecto

4. Ejecuta el programa por primera vez para crear la configuración:
   ```bash
   python main.py
   ```

## ⚙️ Configuración

La configuración se almacena en un archivo JSON que se crea automáticamente en el primer inicio:

- **Número de teléfono**: Formato internacional `+591XXXXXXXX` para recibir notificaciones
- **Paquetes a rastrear**: Lista de paquetes con nombres descriptivos e IDs de seguimiento
- **Notificaciones WhatsApp**: Activar/desactivar notificaciones
- **Intervalo de verificación**: Tiempo entre verificaciones (mínimo 3 minutos)

La configuración se puede modificar desde la interfaz del programa en la opción "Configuración avanzada".

### Uso con el ejecutable (.exe)

Si estás utilizando la versión ejecutable:

1. Coloca el archivo `firebase-creds.json` en la misma carpeta que el ejecutable
2. El archivo de configuración `config.json` se creará automáticamente en la misma carpeta

## 🖥️ Uso

1. Ejecuta el programa principal:
   ```bash
   python main.py
   ```

2. Navega por el menú interactivo:
   - Gestionar paquetes (agregar/eliminar)
   - Ver estado de paquetes
   - Iniciar seguimiento automático
   - Configuración avanzada (número de teléfono, notificaciones, intervalo)

3. Para el seguimiento automático, el programa verificará periódicamente el estado de tus paquetes y enviará notificaciones vía WhatsApp cuando lleguen.

## 📂 Estructura del proyecto

```
package-tracker/
├── core/                 # Funcionalidad principal
│   ├── config_handler.py # Gestión de configuración JSON
│   ├── messenger.py      # Envío de notificaciones
│   └── tracker.py        # Seguimiento de paquetes
├── firestore/            # Integración con Firebase
│   ├── create_collection.py
│   └── get_packages.py
├── utils/                # Utilidades
│   ├── helpers.py        # Funciones auxiliares
│   └── ui.py             # Interfaz de usuario
├── main.py               # Punto de entrada
└── requirements.txt      # Dependencias
```

## 🔐 Seguridad

- El archivo `firebase-creds.json` contiene credenciales sensibles y está incluido en `.gitignore`
- No compartas tu configuración (`config.json`) ya que contiene tu número telefónico personal

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
- **Ejecutable no encuentra credenciales**: Coloca `firebase-creds.json` en la misma carpeta que el .exe

---

⭐ ¡Si encuentras útil este proyecto, no dudes en darle una estrella! ⭐