import datetime
import time
import requests
import colorama
from colorama import Fore, Style
from tenacity import retry, stop_after_attempt, wait_fixed

# Funciones de seguimiento
class PackageTracker:
    @staticmethod
    def construir_url(package_id):
        """Construye la URL de seguimiento para un ID de paquete"""
        base_url = "https://ips.correos.gob.bo/ipswebtracking/IPSWeb_item_events.aspx"
        return f"{base_url}?itemid={package_id}&Submit=Buscar"
    
    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def verificar_texto(url, texto):
        """Verifica si un texto específico aparece en la URL proporcionada"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return texto in response.text
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}⚠️ Error al verificar {url}: {str(e)}{Style.RESET_ALL}")
            return False
    
    @staticmethod
    def iniciar_seguimiento(config, get_packages, enviar_whatsapp):
        """Inicia el seguimiento automático de paquetes"""
        # Construir URLs para todos los paquetes
        urls = {PackageTracker.construir_url(id): nombre for nombre, id in config.PACKAGE_IDS.items()}
        
        texto_busqueda = "Enviar envío a ubicación nacional (entrada)"
        coleccion = 'packages'
        campo = 'steps'
        nuevos_datos = {f'step{i}': True for i in range(1, 11)}
        
        print(f"\n{Fore.GREEN}🔍 Iniciando seguimiento automático de {len(urls)} paquetes{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Presiona Ctrl+C para detener{Style.RESET_ALL}")
        
        intentos = 0
        
        while True:
            now = datetime.datetime.now()
            formatted_datetime = now.strftime("%d/%m/%Y %H:%M")
            
            # Mostrar intento actual
            print(f"\n{Fore.CYAN}**INTENTO #{intentos + 1}**{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Hora de INICIO: {formatted_datetime}{Style.RESET_ALL}")
            
            # Verificar cada paquete
            for url, nombre in urls.items():
                package_id = config.PACKAGE_IDS[nombre]
                print(f"{Fore.YELLOW}Verificando: {nombre} ({package_id}){Style.RESET_ALL}")
                
                if PackageTracker.verificar_texto(url.strip(), texto_busqueda):
                    mensaje = f"📦 ¡Tu paquete '{nombre}' llegó a Oruro!"
                    print(f"{Fore.GREEN}{mensaje}{Style.RESET_ALL}")
                    
                    # Actualizar en Firestore
                    get_packages.actualizar_campo_map(coleccion, package_id, campo, nuevos_datos)
                    
                    # Enviar notificación WhatsApp
                    enviar_whatsapp(config.TELEFONO_DESTINO, mensaje)
                else:
                    print(f"{Fore.BLUE}El paquete '{nombre}' aún no ha llegado{Style.RESET_ALL}")
            
            # Esperar antes del próximo intento
            espera_minutos = 15
            print(f"\n{Fore.YELLOW}Esperando {espera_minutos} minutos para el próximo intento...{Style.RESET_ALL}")
            time.sleep(espera_minutos * 60)
            intentos += 1
    
    @staticmethod
    def mostrar_estado_paquetes(config):
        """Muestra el estado actual de los paquetes configurados"""
        try:
            print(f"\n{Fore.CYAN}📊 Estado actual de los paquetes:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{'-' * 50}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{'NOMBRE':<20} {'ID':<15} {'ESTADO':<15}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{'-' * 50}{Style.RESET_ALL}")
            
            texto_busqueda = "Enviar envío a ubicación nacional (entrada)"
            
            for nombre, package_id in config.PACKAGE_IDS.items():
                url = PackageTracker.construir_url(package_id)
                estado = "Llegó a Oruro" if PackageTracker.verificar_texto(url, texto_busqueda) else "En tránsito"
                estado_color = Fore.GREEN if estado == "Llegó a Oruro" else Fore.BLUE
                print(f"{Fore.CYAN}{nombre:<20}{Style.RESET_ALL} {package_id:<15} {estado_color}{estado}{Style.RESET_ALL}")
            
            print(f"{Fore.YELLOW}{'-' * 50}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Error al mostrar estado: {str(e)}{Style.RESET_ALL}")