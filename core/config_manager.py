import os
import importlib
import colorama
from colorama import Fore, Style

# Clase para manejar la configuración
class ConfigManager:
    @staticmethod
    def validar_configuracion(config):
        """Verifica que todas las variables requeridas existan en config.py"""
        required_vars = [
            'TELEFONO_DESTINO', 
            'PACKAGE_IDS', 
            'NOTIFICACIONES_WHATSAPP', 
            'FIREBASE_CREDS',
            'BASE_DIR'
        ]
        
        missing = [var for var in required_vars if not hasattr(config, var)]
        if missing:
            print(f"{Fore.RED}❌ Faltan variables en config.py: {', '.join(missing)}{Style.RESET_ALL}")
            return False
        return True
    
    @staticmethod
    def crear_configuracion():
        """Crea el archivo config.py interactivamente"""
        print(f"\n{Fore.CYAN}🔧 Configuración inicial requerida 🔧{Style.RESET_ALL}")
        
        # Crear config.py interactivamente
        telefono = input(f"{Fore.CYAN}📱 Ingresa tu número (formato internacional +591XXXXXXXX): {Style.RESET_ALL}").strip()
        
        print(f"\n{Fore.CYAN}🆔 Define tus paquetes (nombre : ID){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Escribe 'FIN' en el nombre para terminar{Style.RESET_ALL}")
        
        paquetes = {}
        while True:
            nombre = input(f"\n{Fore.CYAN}Nombre del paquete (ej: 'micas_dragon'): {Style.RESET_ALL}").strip()
            if nombre.upper() == "FIN": 
                break
            if not nombre: 
                continue
                
            package_id = input(f"{Fore.CYAN}ID de seguimiento para {nombre}: {Style.RESET_ALL}").strip()
            paquetes[nombre] = package_id
        
        # Generar archivo config.py
        ConfigManager.escribir_configuracion({
            'TELEFONO_DESTINO': telefono,
            'PACKAGE_IDS': paquetes,
            'NOTIFICACIONES_WHATSAPP': True
        })
        
        print(f"\n{Fore.GREEN}✅ Config.py creado! Edítalo si necesitas cambios.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⚠️ Recuerda colocar tu archivo firebase-creds.json en la carpeta{Style.RESET_ALL}")
    
    @staticmethod
    def escribir_configuracion(config_data):
        """Escribe el archivo config.py con los datos proporcionados"""
        with open("config.py", "w") as f:
            f.write('import os\n\n')
            
            # Escribir TELEFONO_DESTINO
            if 'TELEFONO_DESTINO' in config_data:
                f.write(f'TELEFONO_DESTINO = "{config_data["TELEFONO_DESTINO"]}"\n\n')
            
            # Escribir PACKAGE_IDS
            if 'PACKAGE_IDS' in config_data:
                f.write('PACKAGE_IDS = {\n')
                for k, v in config_data['PACKAGE_IDS'].items():
                    f.write(f'    "{k}": "{v}",\n')
                f.write('}\n\n')
            
            # Escribir NOTIFICACIONES_WHATSAPP
            if 'NOTIFICACIONES_WHATSAPP' in config_data:
                f.write(f'NOTIFICACIONES_WHATSAPP = {config_data["NOTIFICACIONES_WHATSAPP"]}\n\n')
            
            # Escribir rutas estándar
            f.write('FIREBASE_CREDS = os.path.join(os.path.dirname(__file__), "firebase-creds.json")\n')
            f.write('BASE_DIR = os.path.dirname(os.path.abspath(__file__))\n')
    
    @staticmethod
    def actualizar_configuracion(config_module, **kwargs):
        """Actualiza configuraciones específicas manteniendo el resto"""
        # Cargar configuración actual
        config_data = {
            'TELEFONO_DESTINO': getattr(config_module, 'TELEFONO_DESTINO', ''),
            'PACKAGE_IDS': getattr(config_module, 'PACKAGE_IDS', {}),
            'NOTIFICACIONES_WHATSAPP': getattr(config_module, 'NOTIFICACIONES_WHATSAPP', True)
        }
        
        # Actualizar con nuevos valores
        for key, value in kwargs.items():
            if key in config_data:
                config_data[key] = value
        
        # Escribir configuración actualizada
        ConfigManager.escribir_configuracion(config_data)
        
        # Recargar el módulo
        return importlib.reload(config_module)