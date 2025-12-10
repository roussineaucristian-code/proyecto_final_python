# Importa todas las funciones y clases del módulo helpers dentro del paquete utils.
# Se asume que este módulo contiene funciones de utilidad como validar_input_int o validar_input_string.
from utils.helpers import *

# Importa el módulo db_manager completo desde el paquete utils.
# Este módulo gestiona las interacciones con la base de datos (CRUD).
from utils import db_manager

# Importa el módulo sys, que proporciona acceso a algunas variables y funciones 
# que interactúan fuertemente con el intérprete de Python y el sistema operativo.
import sys

def mostrar_tabla(productos):
    """
    Muestra una lista de productos formateada como una tabla en la consola.

    Args:
        productos (list): Una lista de tuplas o listas, donde cada elemento representa un producto.
                          Se espera una estructura específica (ID, Nombre, Cantidad, Precio, Categ, Desc).
    """
    if not productos:
        print(("No se encontraron productos."))
        return
    # Imprime la cabecera de la tabla con alineación y ancho fijo para cada columna.
    print(f"{'ID':<5} {'Nombre':<20} {'descripcion':<20} {'Categoría':<15} {'Cantidad':<10} {'Precio':<10}")
    print("-" * 85)
    # Itera sobre cada producto en la lista proporcionada.
    for prod in productos:
        # Imprime los datos del producto actual, formateando la salida.
        # Nota: La correspondencia de índices (prod[0], prod[1], etc.) depende de cómo 
        # la función `db_manager.listar_productos()` devuelve los datos.
        print(f"{prod[0]:<5} {prod[1][:18]:<20} {prod[2][:18]:<20} {prod[5]:<15} {prod[3]:<10} {prod[4]:<10.2f}")
        print("-" * 85)  

def menu_registrar():
    """
    Guía al usuario a través del proceso de registro de un nuevo producto mediante inputs.
    Utiliza db_manager para guardar el nuevo producto en la base de datos.
    """
    print("Registrer nuevo producto")
    # Solicita los datos del producto al usuario.
    nombre = input("Nombre: ")
    desc = input("Descipcion: ").strip()
    cantidad = input("Cantidad: ")
    precio = input("Precio: ")
    categ = input("Categoria: ")
    # Llama a la función del gestor de base de datos para registrar.
    if db_manager.registrar_producto(nombre, desc, cantidad, precio, categ):
        print("Producto registrado con exito.")
    else:
        print("Error al registrar el producto.")

def menu_ver_productos():
    """
    Muestra todos los productos existentes en la base de datos.
    """
    print("Lista de productos")
    # Obtiene la lista completa de productos desde la base de datos.
    productos = db_manager.listar_productos()
    # Utiliza la función auxiliar mostrar_tabla para presentar los resultados.
    mostrar_tabla(productos)

def menu_actualizar():
    """
    Permite al usuario seleccionar un producto por ID y actualizar sus detalles.
    Permite dejar un campo vacío para mantener el valor actual.
    """
    print("Actualizar producto")
        # Muestra los productos actuales para que el usuario pueda ver los IDs disponibles.
    menu_ver_productos()
    # Valida que el input del usuario sea un entero (función asumida de utils.helpers).
    id_prod = validar_input_int("Ingrese el ID del producto a actualizar: ")
    # Busca el producto específico por ID.
    producto_actual = db_manager.buscar_producto_por_id(id_prod)
    if not producto_actual:
        print("Producto no encontrado.")
        return
    print(f"En edicion: {producto_actual[1]}")
    
    # manteniendo el valor original si el usuario solo presiona Enter.
    nuevo_nombre = input(f"Nuevo nombre de {producto_actual[1]}: ").strip() or producto_actual[1]
    nuevo_desc = input(f"Nueva descripcion de {producto_actual[2]}: ").strip() or producto_actual[2]
    nuevo_cantidad = input(f"Nueva cantidad de {producto_actual[3]}: ").strip() or producto_actual[3]
    nuevo_precio = input(f"Nuevo precio de {producto_actual[4]}: ").strip() or producto_actual[4]
    nuevo_categ = input(f"Nueva categoria de {producto_actual[5]}: ").strip() or producto_actual[5]
    
     # Intenta actualizar el registro en la base de datos con los valores nuevos o existentes.
    if db_manager.actualizar_producto(id_prod, nuevo_nombre, nuevo_desc, nuevo_cantidad, nuevo_precio, nuevo_categ):
        print("Producto actualizado con exito.")
    else:
        print("Error al actualizar producto.")

def menu_eliminar():
    """
    Permite eliminar un producto de la base de datos después de una confirmación del usuario.
    """
    print("Eliminar un Producto")
    # Muestra los productos para referencia.
    menu_ver_productos()
    id_prod = validar_input_int("Ingrese el ID del producto a eliminar: ")
    # Pide confirmación al usuario.
    confirmar = input (f"¿Confirma que quiere borrar el producto ID {id_prod}? (s/n): ").lower()
    if confirmar == 's':
        if db_manager.eliminar_producto(id_prod):
                print("Producto eliminado con exito.")
    else:
        print("Operacion cancelada")

def menu_buscar():
    """
    Ofrece opciones para buscar productos por ID o por nombre/categoría.
    """
    print("Buscar un producto")
    print("1.Buscar por ID")
    print("2.Buscar por NOMBRE o CATEGORIA")
    opcion = input("Seleccione una opcion: ")
    if opcion == '1':
        id_prod = validar_input_int("ID: ")
        res = db_manager.buscar_producto_por_id(id_prod)
        if res:
            # Si encuentra un resultado (una sola tupla), lo envuelve en una lista para mostrar_tabla.
            mostrar_tabla([res])
    elif opcion == '2':
        termino = validar_input_string("Termino de busqueda: ")
        res = db_manager.buscar_producto_por_nombre(termino)
        # Muestra todos los resultados que coinciden con el término.
        mostrar_tabla(res)
    else:
        print("Opcion invalida.")

def menu_reporte():
    """
    Genera un reporte de productos cuyo stock es inferior a un límite especificado por el usuario.
    """
    print("Reporte de stock")
    limite = validar_input_int("Ingrese la cantidad limite del producto: ")
    # Obtiene los productos con stock bajo de la base de datos.
    res = db_manager.reporte_bajo_stock(limite)
    if res:
        print(f"Se encontraron {len(res)} productos en stock con una cantidad menor a {limite}")
        mostrar_tabla(res)
    else:
        print("No hay productos con un stock menor al indicado.")

def main():
    """
    Función principal que inicia la base de datos y presenta el menú interactivo principal.
    """
    # Se asegura de que la base de datos y las tablas necesarias estén inicializadas
    db_manager.inicializar_db()
    while True: # Bucle infinito para mantener la aplicación en ejecución hasta que el usuario decida salir.
        # Muestra el menú principal de opciones.
        print("═"*30)
        print("GESTION DE INVENTARIO")
        print("1. Registrar un producto")
        print("2. Mostrar productos")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Buscar producto")
        print("6. Reporte de bajo stock")
        print("7. Salir")
        print("═"*30)
        
        # Captura la opción del usuario y limpia espacios.
        opcion = input("\nSeleccione una opcion: ").strip()
        
        # Maneja las opciones del menú llamando a las funciones correspondientes.
        if opcion == '1':
            menu_registrar()
        elif opcion == '2':
            menu_ver_productos()
        elif opcion == '3':
            menu_actualizar()
        elif opcion == '4':
            menu_eliminar()
        elif opcion == '5':
            menu_buscar()
        elif opcion == '6':
            menu_reporte()
        elif opcion == '7':
            print("Preparando todo para salir...")
            sys.exit() # Termina la ejecución del programa.
        else:
            print("Seleccione una opcion valida.")

# Punto de entrada principal del script. 
# Esto asegura que la función main() se ejecute solo cuando el script se ejecuta directamente.
if __name__ == "__main__":
    main()