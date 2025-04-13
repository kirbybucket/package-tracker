import os
import firebase_admin
from firebase_admin import credentials, firestore
import colorama
from colorama import Fore, Style

# Inicialización de colorama
colorama.init()

def inicializar_firebase():
    """Inicializa la conexión con Firebase si no está ya inicializada"""
    try:
        # Comprobar si Firebase ya está inicializado
        firebase_admin.get_app()
    except ValueError:
        # Si no está inicializado, inicializarlo
        try:
            # Busca el archivo de credenciales en la raíz del proyecto
            cred_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "firebase-creds.json")
            
            if not os.path.exists(cred_path):
                print(f"{Fore.RED}❌ Error: No se encuentra el archivo de credenciales de Firebase{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Por favor, coloca 'firebase-creds.json' en la carpeta raíz del proyecto{Style.RESET_ALL}")
                return None
            
            # Inicializar con credenciales
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print(f"{Fore.GREEN}✅ Firebase inicializado correctamente{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Error al inicializar Firebase: {str(e)}{Style.RESET_ALL}")
            return None
    
    # Devolver instancia de Firestore
    return firestore.client()

def crear_coleccion_paquetes():
    """Crea la colección de paquetes si no existe"""
    # Inicializar Firebase
    db = inicializar_firebase()
    if not db:
        return False
    
    try:
        # Verificar si ya existe la colección
        packages_ref = db.collection('packages')
        
        # En Firestore, las colecciones se crean implícitamente al añadir documentos
        # Por lo tanto, verificamos si hay algún documento
        docs = packages_ref.limit(1).stream()
        collection_exists = len(list(docs)) > 0
        
        if not collection_exists:
            print(f"{Fore.YELLOW}ℹ️ Inicializando colección de paquetes en Firestore...{Style.RESET_ALL}")
            # Crear un documento "info" para identificar la colección
            packages_ref.document('info').set({
                'created_at': firestore.SERVER_TIMESTAMP,
                'description': 'Colección de seguimiento de paquetes',
                'version': '1.0.0'
            })
            print(f"{Fore.GREEN}✅ Colección 'packages' creada correctamente{Style.RESET_ALL}")
        else:
            print(f"{Fore.BLUE}ℹ️ La colección 'packages' ya existe en Firestore{Style.RESET_ALL}")
        
        return True
    
    except Exception as e:
        print(f"{Fore.RED}❌ Error al crear colección en Firestore: {str(e)}{Style.RESET_ALL}")
        return False

# Para pruebas directas
if __name__ == "__main__":
    colorama.init()
    print(f"{Fore.CYAN}🔄 Inicializando estructuras de Firestore...{Style.RESET_ALL}")
    resultado = crear_coleccion_paquetes()
    if resultado:
        print(f"{Fore.GREEN}✅ Proceso completado exitosamente{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ El proceso falló. Revisa los errores anteriores{Style.RESET_ALL}")