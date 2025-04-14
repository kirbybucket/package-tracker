import os
import sys
import signal
import importlib
import colorama
from colorama import Fore, Style

# Inicializar colorama para colores en consola
colorama.init()

# Limpiar pantalla
os.system('cls' if os.name == 'nt' else 'clear')

# Configurar rutas de importación
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar módulos propios
from core.config_handler import ConfigHandler
from core.tracker import PackageTracker
from core.messenger import MessageSender
from utils.ui import UI
from firestore import get_packages, create_collection

# Manejador de señales para salir con Ctrl+C
def signal_handler(sig, frame):
    print(f"\n{Fore.YELLOW}Deteniendo el proceso...{Style.RESET_ALL}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Función para verificar credenciales
def verificar_credenciales():
    """Verifica que el archivo de credenciales exista"""
    from firestore.create_collection import get_credentials_path
    
    cred_path = get_credentials_path()
    if not cred_path:
        print(f"\n{Fore.RED}{'=' * 60}")
        print(f"{Fore.RED}❌ ERROR: No se encontró el archivo firebase-creds.json{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Por favor, coloca el archivo 'firebase-creds.json' en la misma carpeta")
        print(f"que el ejecutable de Package Tracker.{Style.RESET_ALL}")
        print(f"{Fore.RED}{'=' * 60}{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Presiona Enter para salir...{Style.RESET_ALL}")
        sys.exit(1)
    return True

# Función para gestionar la agregar paquetes
def agregar_paquete(config):
    """Agrega un nuevo paquete a la configuración"""
    try:        
        print(f"\n{Fore.CYAN}📦 Agregar nuevo paquete{Style.RESET_ALL}")
        
        nombre = input(f"{Fore.CYAN}Nombre del paquete: {Style.RESET_ALL}").strip()
        if not nombre:
            print(f"{Fore.RED}❌ Nombre inválido{Style.RESET_ALL}")
            return
            
        package_id = input(f"{Fore.CYAN}ID de seguimiento: {Style.RESET_ALL}").strip()
        if not package_id.startswith("RP") or len(package_id) != 13:
            print(f"{Fore.RED}❌ ID inválido (debe ser RP + 11 dígitos){Style.RESET_ALL}")
            return
        
        # Actualizar el diccionario en memoria
        paquetes_actualizados = config.PACKAGE_IDS.copy()
        paquetes_actualizados[nombre] = package_id
        
        # Actualizar configuración
        config = ConfigHandler.update_config(config, PACKAGE_IDS=paquetes_actualizados)
        print(f"{Fore.GREEN}✅ Paquete agregado correctamente{Style.RESET_ALL}")
        
        # Crear en Firestore
        coleccion = 'packages'
        campo = 'steps'
        datos = {f'step{i}': False for i in range(1, 11)}
        get_packages.agregar_campo_map(coleccion, package_id, campo, datos)
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error al agregar paquete: {str(e)}{Style.RESET_ALL}")
    
    return config

# Función para eliminar paquetes
def eliminar_paquete(config):
    """Elimina un paquete de la configuración y Firestore"""
    if not config.PACKAGE_IDS:
        print(f"{Fore.YELLOW}⚠️ No hay paquetes registrados{Style.RESET_ALL}")
        return config

    print(f"\n{Fore.CYAN}📦 Paquetes registrados:{Style.RESET_ALL}")
    for nombre, package_id in config.PACKAGE_IDS.items():
        print(f"{Fore.YELLOW}▪ {nombre}: {package_id}{Style.RESET_ALL}")
    
    package_id = input(f"\n{Fore.CYAN}Ingrese ID del paquete a eliminar: {Style.RESET_ALL}").strip()
    
    # Buscar paquete por ID
    paquete = [nombre for nombre, pid in config.PACKAGE_IDS.items() if pid == package_id]
    
    if not paquete:
        print(f"{Fore.RED}❌ No se encontró el paquete con ID {package_id}{Style.RESET_ALL}")
        return config
    
    nombre_paquete = paquete[0]
    
    # Confirmación
    confirmar = input(f"{Fore.RED}⚠️ ¿Eliminar {nombre_paquete} ({package_id})? (s/n): {Style.RESET_ALL}").lower()
    if confirmar != 's':
        print(f"{Fore.YELLOW}Operación cancelada{Style.RESET_ALL}")
        return config
    
    # Eliminar de configuración
    nuevos_paquetes = {k:v for k,v in config.PACKAGE_IDS.items() if v != package_id}
    
    # Actualizar configuración
    config = ConfigHandler.update_config(config, PACKAGE_IDS=nuevos_paquetes)
    
    # Eliminar de Firestore
    try:
        get_packages.eliminar_datos('packages', package_id)
        print(f"{Fore.GREEN}✅ Paquete eliminado correctamente{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error al eliminar de Firestore: {str(e)}{Style.RESET_ALL}")
    
    return config

# Función para cambiar el número telefónico
def cambiar_numero_telefonico(config):
    """Permite actualizar el número de teléfono en la configuración"""
    print(f"\n{Fore.CYAN}📱 Número actual: {config.TELEFONO_DESTINO}{Style.RESET_ALL}")
    nuevo_numero = input(f"{Fore.CYAN}Ingrese nuevo número (formato +591XXXXXXXX): {Style.RESET_ALL}").strip()
    
    if not nuevo_numero.startswith("+"):
        print(f"{Fore.RED}❌ Formato inválido. Debe comenzar con '+' seguido del código de país{Style.RESET_ALL}")
        return config
    
    # Actualizar configuración
    config = ConfigHandler.update_config(config, TELEFONO_DESTINO=nuevo_numero)
    print(f"{Fore.GREEN}✅ Número actualizado correctamente{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}ℹ️ Los cambios surtirán efecto en el próximo seguimiento{Style.RESET_ALL}")
    
    return config

# Función para gestionar notificaciones
def gestionar_notificaciones(config):
    """Permite activar/desactivar notificaciones"""
    print(f"\n{Fore.CYAN}🔔 Estado actual: {'ACTIVADAS' if config.NOTIFICACIONES_WHATSAPP else 'DESACTIVADAS'}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}1. Activar notificaciones")
    print(f"2. Desactivar notificaciones{Style.RESET_ALL}")
    
    opcion = input(f"{Fore.YELLOW}Selecciona una opción: {Style.RESET_ALL}")
    
    nuevo_estado = config.NOTIFICACIONES_WHATSAPP  # Mantener valor actual por defecto
    
    if opcion == "1":
        nuevo_estado = True
    elif opcion == "2":
        nuevo_estado = False
    else:
        print(f"{Fore.RED}❌ Opción inválida{Style.RESET_ALL}")
        return config
    
    # Actualizar configuración
    config = ConfigHandler.update_config(config, NOTIFICACIONES_WHATSAPP=nuevo_estado)
    print(f"{Fore.GREEN}✅ Notificaciones {'activadas' if nuevo_estado else 'desactivadas'}{Style.RESET_ALL}")
    
    return config

# Añadir esta función después de gestionar_notificaciones

def configurar_intervalo(config):
    """Permite al usuario configurar el intervalo entre verificaciones"""
    INTERVALO_MINIMO = 3  # Mínimo 3 minutos para evitar sobrecarga
    
    print(f"\n{Fore.CYAN}⏱️ Configuración de intervalo entre verificaciones{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Intervalo actual: {config.INTERVALO_MINUTOS} minutos{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Nota: El intervalo mínimo permitido es de {INTERVALO_MINIMO} minutos{Style.RESET_ALL}")
    
    try:
        nuevo_intervalo = int(input(f"{Fore.CYAN}Nuevo intervalo en minutos: {Style.RESET_ALL}"))
        
        if nuevo_intervalo < INTERVALO_MINIMO:
            print(f"{Fore.RED}❌ El intervalo no puede ser menor a {INTERVALO_MINIMO} minutos{Style.RESET_ALL}")
            return config
        
        # Actualizar configuración
        config = ConfigHandler.update_config(config, INTERVALO_MINUTOS=nuevo_intervalo)
        print(f"{Fore.GREEN}✅ Intervalo actualizado a {nuevo_intervalo} minutos{Style.RESET_ALL}")
    
    except ValueError:
        print(f"{Fore.RED}❌ Valor inválido. Debe ser un número entero.{Style.RESET_ALL}")
    
    return config

# Función principal
def main():
    """Función principal del programa"""
    # Verificar credenciales de Firebase
    verificar_credenciales()
    
    # Crear colección inicial
    create_collection.crear_coleccion_paquetes()
    
    # Cargar configuración
    config = ConfigHandler.load_config()
    if not config.TELEFONO_DESTINO:
        print(f"{Fore.YELLOW}No se encontró configuración. Creando una nueva...{Style.RESET_ALL}")
        config = ConfigHandler.create_interactive_config()

    # Bucle principal con recarga dinámica
    while True:
        config = ConfigHandler.load_config()  # Recarga en cada iteración
        
        # Mostrar cabecera
        UI.mostrar_cabecera(config)

        # Mostrar menú principal
        opcion = UI.mostrar_menu()

        # 1. Gestión de paquetes
        if opcion == "1":
            while True:
                sub_opcion = UI.menu_gestion_paquetes()
                
                if sub_opcion == "1":
                    config = agregar_paquete(config)
                elif sub_opcion == "2":
                    config = eliminar_paquete(config)
                elif sub_opcion == "3":
                    break
                else:
                    print(f"{Fore.RED}❌ Opción inválida{Style.RESET_ALL}")
                
                input(f"\n{Fore.YELLOW}Presiona Enter para continuar...{Style.RESET_ALL}")
                config = ConfigHandler.load_config()  # Recarga inmediata tras cambios

        # 2. Ver estado de paquetes
        elif opcion == "2":
            if not config.PACKAGE_IDS:
                print(f"{Fore.YELLOW}⚠️ No hay paquetes registrados{Style.RESET_ALL}")
            else:
                PackageTracker.mostrar_estado_paquetes(config)

        # 3. Iniciar seguimiento automático
        elif opcion == "3":
            if not config.PACKAGE_IDS:
                print(f"{Fore.RED}❌ Error: Primero registra paquetes en la opción 1{Style.RESET_ALL}")
                continue
            print(f"\n{Fore.CYAN}🔄 Iniciando seguimiento automático...{Style.RESET_ALL}")
            try:
                # Crear función lambda para simplificar la llamada
                enviar_whatsapp = lambda telefono, mensaje: MessageSender.enviar_whatsapp(
                    telefono, mensaje, config.NOTIFICACIONES_WHATSAPP
                )
                PackageTracker.iniciar_seguimiento(config, get_packages, enviar_whatsapp)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}🔇 Seguimiento automático detenido{Style.RESET_ALL}")

        # 4. Configuración avanzada
        elif opcion == "4":
            while True:
                sub_opcion = UI.menu_configuracion()
                
                # 4.1 Cambiar número
                if sub_opcion == "1":
                    config = cambiar_numero_telefonico(config)
                
                # 4.2 Gestionar notificaciones
                elif sub_opcion == "2":
                    config = gestionar_notificaciones(config)
                
                # 4.3 Configurar intervalo
                elif sub_opcion == "3":
                    config = configurar_intervalo(config)
                
                # 4.4 Volver al menú principal
                elif sub_opcion == "4":
                    break
                
                else:
                    print(f"{Fore.RED}❌ Opción inválida{Style.RESET_ALL}")
                
                input(f"\n{Fore.YELLOW}Presiona Enter para continuar...{Style.RESET_ALL}")

        # 5. Salir del programa
        elif opcion == "5":
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{'🚪 SALIENDO DEL SISTEMA':^60}")
            print(f"{'='*60}{Style.RESET_ALL}")
            break

        # Opción inválida
        else:
            print(f"{Fore.RED}❌ Opción no válida{Style.RESET_ALL}")

        # Pausa entre operaciones
        input(f"\n{Fore.YELLOW}Presiona Enter para volver al menú...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()