import firebase_admin
from firebase_admin import credentials, firestore
import colorama
from colorama import Fore, Style
from .create_collection import inicializar_firebase

# Inicialización de colorama
colorama.init()

def obtener_paquetes():
    """Obtiene todos los paquetes registrados en Firestore"""
    db = inicializar_firebase()
    if not db:
        return []
    
    try:
        # Obtener documentos de la colección packages (excepto 'info')
        packages_ref = db.collection('packages')
        docs = packages_ref.stream()
        
        # Convertir a lista y filtrar documento 'info'
        paquetes = []
        for doc in docs:
            if doc.id != 'info':
                data = doc.to_dict()
                data['id'] = doc.id  # Añadir ID como campo
                paquetes.append(data)
        
        return paquetes
    
    except Exception as e:
        print(f"{Fore.RED}❌ Error al obtener paquetes: {str(e)}{Style.RESET_ALL}")
        return []

def obtener_paquete(package_id):
    """Obtiene un paquete específico por su ID"""
    db = inicializar_firebase()
    if not db:
        return None
    
    try:
        doc_ref = db.collection('packages').document(package_id)
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        else:
            print(f"{Fore.YELLOW}⚠️ No se encontró el paquete con ID: {package_id}{Style.RESET_ALL}")
            return None
    
    except Exception as e:
        print(f"{Fore.RED}❌ Error al obtener paquete {package_id}: {str(e)}{Style.RESET_ALL}")
        return None

def agregar_paquete(package_id, nombre, datos_adicionales=None):
    """Agrega un nuevo paquete a Firestore"""
    db = inicializar_firebase()
    if not db:
        return False
    
    try:
        # Crear datos base
        datos = {
            'nombre': nombre,
            'creado': firestore.SERVER_TIMESTAMP,
            'actualizado': firestore.SERVER_TIMESTAMP,
        }
        
        # Añadir datos adicionales si se proporcionaron
        if datos_adicionales and isinstance(datos_adicionales, dict):
            datos.update(datos_adicionales)
        
        # Guardar en Firestore
        db.collection('packages').document(package_id).set(datos)
        print(f"{Fore.GREEN}✅ Paquete '{nombre}' añadido correctamente{Style.RESET_ALL}")
        return True
    
    except Exception as e:
        print(f"{Fore.RED}❌ Error al agregar paquete {package_id}: {str(e)}{Style.RESET_ALL}")
        return False

def actualizar_campo_map(coleccion, documento_id, campo_map, nuevos_datos):
    """
    Actualiza un campo de tipo map en un documento
    
    Args:
        coleccion (str): Nombre de la colección
        documento_id (str): ID del documento
        campo_map (str): Nombre del campo map
        nuevos_datos (dict): Nuevos datos a establecer
    """
    db = inicializar_firebase()
    if not db:
        return False
    
    try:
        doc_ref = db.collection(coleccion).document(documento_id)
        
        # Verificar si el documento existe
        doc = doc_ref.get()
        if not doc.exists:
            # Crear documento con el campo map
            doc_ref.set({
                campo_map: nuevos_datos,
                'creado': firestore.SERVER_TIMESTAMP,
                'actualizado': firestore.SERVER_TIMESTAMP
            })
            print(f"{Fore.GREEN}✅ Creado documento {documento_id} con map {campo_map}{Style.RESET_ALL}")
        else:
            # Actualizar el campo map en el documento existente
            datos_actualizacion = {
                campo_map: nuevos_datos,
                'actualizado': firestore.SERVER_TIMESTAMP
            }
            doc_ref.update(datos_actualizacion)
            print(f"{Fore.GREEN}✅ Actualizado map {campo_map} en documento {documento_id}{Style.RESET_ALL}")
        
        return True
    
    except Exception as e:
        print(f"{Fore.RED}❌ Error al actualizar map {campo_map}: {str(e)}{Style.RESET_ALL}")
        return False

def agregar_campo_map(coleccion, documento_id, campo_map, nuevos_datos):
    """
    Agrega un campo de tipo map si no existe o lo actualiza si ya existe
    
    Args:
        coleccion (str): Nombre de la colección
        documento_id (str): ID del documento
        campo_map (str): Nombre del campo map
        nuevos_datos (dict): Datos a agregar
    """
    return actualizar_campo_map(coleccion, documento_id, campo_map, nuevos_datos)

def eliminar_datos(coleccion, documento_id):
    """Elimina un documento completo de una colección"""
    db = inicializar_firebase()
    if not db:
        return False
    
    try:
        db.collection(coleccion).document(documento_id).delete()
        print(f"{Fore.GREEN}✅ Documento {documento_id} eliminado de {coleccion}{Style.RESET_ALL}")
        return True
    
    except Exception as e:
        print(f"{Fore.RED}❌ Error al eliminar documento {documento_id}: {str(e)}{Style.RESET_ALL}")
        return False

# Para pruebas directas
if __name__ == "__main__":
    colorama.init()
    print(f"{Fore.CYAN}🔄 Probando funciones de Firestore...{Style.RESET_ALL}")
    
    # Ejemplo de uso
    paquetes = obtener_paquetes()
    print(f"Paquetes encontrados: {len(paquetes)}")
    
    # Ver IDs de paquetes
    for p in paquetes:
        print(f"- {p.get('id')}: {p.get('nombre', 'Sin nombre')}")