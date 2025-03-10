import os
import datetime
import time
import json
import logging
from pathlib import Path

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("sky_app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SkyClientSystem")

# Constantes
BASE_DIR = Path(__file__).resolve().parent
CLIENTS_DIR = BASE_DIR / "clientes"

class Cliente:
    def __init__(self, nombre, tipo_cliente):
        self.nombre = nombre
        self.tipo_cliente = tipo_cliente
        self.fecha_registro = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.servicios = []
        
    def agregar_servicio(self, tipo_servicio, fecha_solicitud=None):
        if fecha_solicitud is None:
            fecha_solicitud = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        nuevo_servicio = {
            "tipo": tipo_servicio,
            "fecha_solicitud": fecha_solicitud
        }
        
        self.servicios.append(nuevo_servicio)
        return nuevo_servicio

    def to_string(self):
        cliente_str = f"Nombre: {self.nombre}\n"
        cliente_str += f"Tipo: {self.tipo_cliente}\n"
        cliente_str += f"Fecha de registro: {self.fecha_registro}\n"
        cliente_str += "Servicios:\n"
        
        for i, servicio in enumerate(self.servicios, 1):
            cliente_str += f"  {i}. Tipo: {servicio['tipo']}, Fecha: {servicio['fecha_solicitud']}\n"
        
        return cliente_str
    
    def to_dict(self):
        """Convierte el cliente a un diccionario para JSON"""
        return {
            "nombre": self.nombre,
            "tipo_cliente": self.tipo_cliente,
            "fecha_registro": self.fecha_registro,
            "servicios": self.servicios
        }

    def guardar(self):
        try:
            # Crear directorio de clientes si no existe
            os.makedirs(CLIENTS_DIR, exist_ok=True)
            
            # Guardar en formato TXT (requerido)
            nombre_archivo_txt = CLIENTS_DIR / f"{self.nombre.replace(' ', '_').lower()}.txt"
            with open(nombre_archivo_txt, "w", encoding="utf-8") as archivo:
                archivo.write(f"Nombre: {self.nombre}\n")
                archivo.write(f"Tipo: {self.tipo_cliente}\n")
                archivo.write(f"Fecha de registro: {self.fecha_registro}\n")
                archivo.write("Servicios:\n")
                
                for servicio in self.servicios:
                    archivo.write(f"- Tipo: {servicio['tipo']}, Fecha: {servicio['fecha_solicitud']}\n")
            
            # También guardar en formato JSON para respaldo y facilidad de procesamiento
            nombre_archivo_json = CLIENTS_DIR / f"{self.nombre.replace(' ', '_').lower()}.json"
            with open(nombre_archivo_json, "w", encoding="utf-8") as archivo:
                json.dump(self.to_dict(), archivo, ensure_ascii=False, indent=2)
                
            logger.info(f"Cliente '{self.nombre}' guardado correctamente")
            return True
        except Exception as e:
            logger.error(f"Error al guardar cliente '{self.nombre}': {str(e)}")
            return False

def cargar_cliente(nombre):
    try:
        nombre_archivo = CLIENTS_DIR / f"{nombre.replace(' ', '_').lower()}.txt"
        
        if not nombre_archivo.exists():
            logger.warning(f"No se encontró el cliente '{nombre}'")
            return None
        
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
        
        # Extraer información del cliente
        nombre_cliente = lineas[0].split("Nombre: ")[1].strip()
        tipo_cliente = lineas[1].split("Tipo: ")[1].strip()
        fecha_registro = lineas[2].split("Fecha de registro: ")[1].strip()
        
        # Crear objeto cliente
        cliente = Cliente(nombre_cliente, tipo_cliente)
        cliente.fecha_registro = fecha_registro
        
        # Agregar servicios
        for i in range(4, len(lineas)):
            if lineas[i].startswith("- Tipo:"):
                partes = lineas[i].split(", Fecha: ")
                tipo_servicio = partes[0].split("- Tipo: ")[1].strip()
                fecha_solicitud = partes[1].strip()
                cliente.agregar_servicio(tipo_servicio, fecha_solicitud)
        
        logger.info(f"Cliente '{nombre}' cargado correctamente")
        return cliente
    except Exception as e:
        logger.error(f"Error al cargar cliente '{nombre}': {str(e)}")
        return None

def listar_clientes():
    """Retorna una lista de nombres de todos los clientes registrados"""
    try:
        clientes = []
        if CLIENTS_DIR.exists():
            for archivo in CLIENTS_DIR.glob("*.txt"):
                nombre_cliente = archivo.stem.replace("_", " ")
                clientes.append(nombre_cliente)
        return clientes
    except Exception as e:
        logger.error(f"Error al listar clientes: {str(e)}")
        return []

def limpiar_pantalla():
    """Limpia la pantalla de la terminal de forma compatible con diferentes OS"""
    # Esta función es compatible con entornos de terminal y CI/CD
    print("\n" * 100)

def mostrar_menu_principal():
    limpiar_pantalla()
    print("=" * 40)
    print("    SISTEMA DE GESTIÓN DE CLIENTES SKY")
    print("=" * 40)
    print("1. Crear nuevo cliente")
    print("2. Buscar cliente existente")
    print("3. Listar todos los clientes")
    print("4. Salir")
    print("=" * 40)
    return input("Seleccione una opción: ")

def mostrar_menu_servicios():
    limpiar_pantalla()
    print("=" * 40)
    print("    SELECCIÓN DE SERVICIO")
    print("=" * 40)
    print("1. Telefonía")
    print("2. Internet")
    print("3. TV de paga")
    print("4. Cancelar")
    print("=" * 40)
    opcion = input("Seleccione un servicio: ")
    
    if opcion == "1":
        return "Telefonía"
    elif opcion == "2":
        return "Internet"
    elif opcion == "3":
        return "TV de paga"
    else:
        return None

def crear_cliente():
    limpiar_pantalla()
    print("=" * 40)
    print("    CREAR NUEVO CLIENTE")
    print("=" * 40)
    
    nombre = input("Ingrese el nombre del cliente: ")
    
    # Validar que el nombre no esté vacío
    if not nombre.strip():
        print("\nEl nombre no puede estar vacío.")
        input("\nPresione Enter para continuar...")
        return
    
    # Verificar si el cliente ya existe
    if (CLIENTS_DIR / f"{nombre.replace(' ', '_').lower()}.txt").exists():
        print(f"\nYa existe un cliente con el nombre '{nombre}'.")
        print("Por favor, use un nombre diferente o actualice el cliente existente.")
        input("\nPresione Enter para continuar...")
        return
    
    print("\nTipo de cliente:")
    print("1. Persona")
    print("2. Negocio")
    tipo_opcion = input("Seleccione el tipo de cliente: ")
    
    if tipo_opcion == "1":
        tipo_cliente = "Persona"
    elif tipo_opcion == "2":
        tipo_cliente = "Negocio"
    else:
        print("Opción inválida. Se asignará como 'Persona' por defecto.")
        tipo_cliente = "Persona"
    
    cliente = Cliente(nombre, tipo_cliente)
    
    # Solicitar el tipo de servicio
    tipo_servicio = mostrar_menu_servicios()
    if tipo_servicio:
        cliente.agregar_servicio(tipo_servicio)
        
    # Guardar cliente
    if cliente.guardar():
        print("\nCliente creado exitosamente.")
        print(cliente.to_string())
    else:
        print("\nError al guardar el cliente. Verifique los permisos y vuelva a intentarlo.")
    
    input("\nPresione Enter para continuar...")

def buscar_cliente():
    limpiar_pantalla()
    print("=" * 40)
    print("    BUSCAR CLIENTE")
    print("=" * 40)
    
    nombre = input("Ingrese el nombre del cliente a buscar: ")
    cliente = cargar_cliente(nombre)
    
    if cliente:
        while True:
            limpiar_pantalla()
            print("=" * 40)
            print("    INFORMACIÓN DEL CLIENTE")
            print("=" * 40)
            print(cliente.to_string())
            print("\n1. Agregar nuevo servicio")
            print("2. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                tipo_servicio = mostrar_menu_servicios()
                if tipo_servicio:
                    cliente.agregar_servicio(tipo_servicio)
                    if cliente.guardar():
                        print(f"\nServicio '{tipo_servicio}' agregado correctamente.")
                    else:
                        print("\nError al guardar los cambios.")
                    time.sleep(2)
            elif opcion == "2":
                break
            else:
                print("Opción inválida.")
                time.sleep(1)
    else:
        print(f"\nNo se encontró ningún cliente con el nombre '{nombre}'.")
        input("\nPresione Enter para continuar...")

def listar_todos_clientes():
    limpiar_pantalla()
    print("=" * 40)
    print("    LISTADO DE CLIENTES")
    print("=" * 40)
    
    clientes = listar_clientes()
    
    if clientes:
        for i, cliente in enumerate(clientes, 1):
            print(f"{i}. {cliente}")
            
        print(f"\nTotal de clientes: {len(clientes)}")
    else:
        print("No hay clientes registrados en el sistema.")
    
    input("\nPresione Enter para continuar...")

def main():
    # Asegurar que el directorio de clientes existe
    os.makedirs(CLIENTS_DIR, exist_ok=True)
    
    logger.info("Iniciando Sistema de Gestión de Clientes Sky")
    
    while True:
        try:
            opcion = mostrar_menu_principal()
            
            if opcion == "1":
                crear_cliente()
            elif opcion == "2":
                buscar_cliente()
            elif opcion == "3":
                listar_todos_clientes()
            elif opcion == "4":
                limpiar_pantalla()
                print("Gracias por utilizar el Sistema de Gestión de Clientes Sky.")
                logger.info("Finalizando aplicación")
                break
            else:
                print("Opción inválida. Intente nuevamente.")
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Aplicación terminada por el usuario (Ctrl+C)")
            break
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            print(f"\nOcurrió un error inesperado: {str(e)}")
            print("El error ha sido registrado.")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()
