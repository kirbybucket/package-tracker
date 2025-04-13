import pywhatkit
import colorama
from colorama import Fore, Style

class MessageSender:
    @staticmethod
    def enviar_whatsapp(telefono, mensaje, notificaciones_activadas=True):
        """Envía un mensaje de WhatsApp si las notificaciones están activas"""
        if not notificaciones_activadas:
            print(f"{Fore.YELLOW}⚠️ Notificaciones WhatsApp desactivadas{Style.RESET_ALL}")
            return False
        try:
            print(f"{Fore.CYAN}📱 Enviando WhatsApp a {telefono}: {mensaje}{Style.RESET_ALL}")
            # Quitar espacios del número de teléfono
            telefono_limpio = telefono.replace(" ", "")
            pywhatkit.sendwhatmsg_instantly(
                telefono_limpio, 
                mensaje,
                wait_time=15,  # Espera 15 segundos antes de enviar
                tab_close=True  # Cierra la pestaña después de enviar
            )
            print(f"{Fore.GREEN}✅ WhatsApp enviado correctamente{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ Error al enviar WhatsApp: {str(e)}{Style.RESET_ALL}")
            return False