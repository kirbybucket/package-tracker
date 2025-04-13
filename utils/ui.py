import colorama
from colorama import Fore, Style

class UI:
    @staticmethod
    def mostrar_menu():
        """Muestra el menú principal de la aplicación"""
        print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'📦 SEGUIMIENTO DE PAQUETES':^50}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1.{Style.RESET_ALL} Gestionar paquetes")
        print(f"{Fore.GREEN}2.{Style.RESET_ALL} Ver estado de paquetes")
        print(f"{Fore.GREEN}3.{Style.RESET_ALL} Iniciar seguimiento automático")
        print(f"{Fore.GREEN}4.{Style.RESET_ALL} Configuración avanzada")
        print(f"{Fore.GREEN}5.{Style.RESET_ALL} Salir")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        
        return input(f"{Fore.YELLOW}Selecciona una opción: {Style.RESET_ALL}")
    
    @staticmethod
    def menu_configuracion():
        """Submenú para configuraciones avanzadas"""
        print(f"\n{Fore.CYAN}{'⚙️ CONFIGURACIÓN AVANZADA':^50}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1.{Style.RESET_ALL} Cambiar número telefónico")
        print(f"{Fore.GREEN}2.{Style.RESET_ALL} Gestionar notificaciones WhatsApp")
        print(f"{Fore.GREEN}3.{Style.RESET_ALL} Volver al menú principal")
        print(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}")
        
        return input(f"{Fore.YELLOW}Selecciona una opción: {Style.RESET_ALL}")
    
    @staticmethod
    def menu_gestion_paquetes():
        """Submenú para gestión de paquetes"""
        print(f"\n{Fore.CYAN}{'📦 GESTIÓN DE PAQUETES':^50}")
        print(f"{Fore.CYAN}{'-'*50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1.{Style.RESET_ALL} Agregar nuevo paquete")
        print(f"{Fore.GREEN}2.{Style.RESET_ALL} Eliminar paquete existente")
        print(f"{Fore.GREEN}3.{Style.RESET_ALL} Volver al menú principal")
        print(f"{Fore.CYAN}{'-'*50}{Style.RESET_ALL}")
        return input(f"{Fore.YELLOW}Selecciona una opción: {Style.RESET_ALL}")
    
    @staticmethod
    def mostrar_cabecera(config):
        """Muestra la cabecera con información del sistema"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{'📦 SISTEMA DE SEGUIMIENTO DE PAQUETES':^60}")
        print(f"{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}▪ Número de notificaciones: {config.TELEFONO_DESTINO}")
        print(f"▪ Paquetes registrados: {len(config.PACKAGE_IDS)}")
        print(f"▪ Estado notificaciones: {'ACTIVADAS' if config.NOTIFICACIONES_WHATSAPP else 'DESACTIVADAS'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")