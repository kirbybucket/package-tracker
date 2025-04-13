import re
import datetime
import colorama
from colorama import Fore, Style

class Helpers:
    @staticmethod
    def validar_package_id(package_id):
        """Valida el formato de ID de paquete (RP + 11 caracteres alfanuméricos)"""
        if not package_id:
            return False
        return bool(re.match(r'^RP\d{11}MU$', package_id))
    
    @staticmethod
    def validar_telefono(telefono):
        """Valida formato de número de teléfono internacional (+XXXXXXXXXXXX)"""
        if not telefono:
            return False
        return bool(re.match(r'^\+\d{10,15}$', telefono))
    
    @staticmethod
    def get_timestamp():
        """Retorna fecha y hora actual formateadas"""
        now = datetime.datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")
    
    @staticmethod
    def log_info(mensaje):
        """Registra un mensaje informativo con timestamp"""
        timestamp = Helpers.get_timestamp()
        print(f"{Fore.CYAN}[INFO] [{timestamp}] {mensaje}{Style.RESET_ALL}")
    
    @staticmethod
    def log_error(mensaje):
        """Registra un mensaje de error con timestamp"""
        timestamp = Helpers.get_timestamp()
        print(f"{Fore.RED}[ERROR] [{timestamp}] {mensaje}{Style.RESET_ALL}")
    
    @staticmethod
    def log_success(mensaje):
        """Registra un mensaje de éxito con timestamp"""
        timestamp = Helpers.get_timestamp()
        print(f"{Fore.GREEN}[ÉXITO] [{timestamp}] {mensaje}{Style.RESET_ALL}")