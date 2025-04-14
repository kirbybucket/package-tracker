import os
import json
import sys
import colorama
from colorama import Fore, Style

class Config:
    """Clase que representa la configuración del programa"""
    def __init__(self):
        self.TELEFONO_DESTINO = ""
        self.PACKAGE_IDS = {}
        self.NOTIFICACIONES_WHATSAPP = True
        self.INTERVALO_MINUTOS = 15  # Valor predeterminado de 15 minutos
        self.FIREBASE_CREDS = self.get_firebase_path()
        self.BASE_DIR = self.get_base_dir()
    
    def get_base_dir(self):
        """Obtiene el directorio base de la aplicación"""
        if getattr(sys, 'frozen', False):
            # Si estamos en un ejecutable
            return os.path.dirname(sys.executable)
        else:
            # Si estamos en desarrollo
            return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    def get_firebase_path(self):
        """Obtiene la ruta al archivo de credenciales de Firebase"""
        if getattr(sys, 'frozen', False):
            # Si estamos en un ejecutable
            return os.path.join(os.path.dirname(sys.executable), "firebase-creds.json")
        else:
            # Si estamos en desarrollo
            return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "firebase-creds.json")

class ConfigHandler:
    """Gestor de configuración que maneja archivo JSON"""
    @staticmethod
    def get_config_path():
        """Obtiene la ruta del archivo de configuración"""
        if getattr(sys, 'frozen', False):
            # Si estamos en un ejecutable
            return os.path.join(os.path.dirname(sys.executable), "config.json")
        else:
            # Si estamos en desarrollo
            return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
    
    @staticmethod
    def load_config():
        """Carga la configuración desde el archivo o crea una por defecto"""
        config = Config()
        config_path = ConfigHandler.get_config_path()
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                config.TELEFONO_DESTINO = data.get('TELEFONO_DESTINO', '')
                config.PACKAGE_IDS = data.get('PACKAGE_IDS', {})
                config.NOTIFICACIONES_WHATSAPP = data.get('NOTIFICACIONES_WHATSAPP', True)
                config.INTERVALO_MINUTOS = data.get('INTERVALO_MINUTOS', 15)
                
                return config
            except Exception as e:
                print(f"{Fore.RED}❌ Error al leer archivo de configuración: {str(e)}{Style.RESET_ALL}")
                # En caso de error, continuamos con la configuración por defecto
        
        return config
    
    @staticmethod
    def save_config(config):
        """Guarda la configuración en un archivo JSON"""
        config_path = ConfigHandler.get_config_path()
        try:
            data = {
                'TELEFONO_DESTINO': config.TELEFONO_DESTINO,
                'PACKAGE_IDS': config.PACKAGE_IDS,
                'NOTIFICACIONES_WHATSAPP': config.NOTIFICACIONES_WHATSAPP,
                'INTERVALO_MINUTOS': config.INTERVALO_MINUTOS
            }
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ Error al guardar configuración: {str(e)}{Style.RESET_ALL}")
            return False
    
    @staticmethod
    def create_interactive_config():
        """Crea una configuración interactivamente"""
        config = Config()
        
        print(f"\n{Fore.CYAN}🔧 Configuración inicial requerida 🔧{Style.RESET_ALL}")
        
        # Pedir datos interactivamente
        config.TELEFONO_DESTINO = input(f"{Fore.CYAN}📱 Ingresa tu número (formato internacional +591XXXXXXXX): {Style.RESET_ALL}").strip()
        
        print(f"\n{Fore.CYAN}🆔 Define tus paquetes (nombre : ID){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Escribe 'FIN' en el nombre para terminar{Style.RESET_ALL}")
        
        while True:
            nombre = input(f"\n{Fore.CYAN}Nombre del paquete (ej: 'micas_dragon'): {Style.RESET_ALL}").strip()
            if nombre.upper() == "FIN": 
                break
            if not nombre: 
                continue
                
            package_id = input(f"{Fore.CYAN}ID de seguimiento para {nombre}: {Style.RESET_ALL}").strip()
            config.PACKAGE_IDS[nombre] = package_id
        
        # Guardar configuración
        if ConfigHandler.save_config(config):
            print(f"\n{Fore.GREEN}✅ Configuración creada y guardada exitosamente{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}❌ Error al guardar la configuración{Style.RESET_ALL}")
        
        return config
    
    @staticmethod
    def update_config(config, **kwargs):
        """Actualiza la configuración con nuevos valores"""
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        ConfigHandler.save_config(config)
        return config