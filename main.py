from utils.helpers import *
from utils import db_manager
import sys

def mostrar_tabla(productos):
    if not productos:
        print(("No se encontraron productos."))
        return
    print(f"{'ID':<5} {'Nombre':<20} {'descripcion':<20} {'Categoría':<15} {'Cantidad':<10} {'Precio':<10}")
    print("-" * 65)
    for prod in productos:
        print(f"{prod[0]:<5} {prod[1][:18]:<20} {prod[5][:13]:<15}  {prod[4]:<9.2f} {prod[3]:<10} {prod[2]:<15}")
        print("-" * 65)  

def menu_registrar():
    print("Registrer nuevo producto")
    nombre = input("Nombre: ")
    desc = input("Descipcion: ").strip
    cantidad = input("Cantidad: ")
    precio = input("Precio: ")
    categ = input("Categoria: ")
    if db_manager.registrar_producto(nombre, desc, cantidad, precio, categ):
        print("Producto registrado con exito.")
    else:
        print("Error al registrar el producto.")

def menu_ver_productos():
    print("Lista de productos")
    productos = db_manager.listar_productos()
    mostrar_tabla(productos)

def menu_actualizar():
    print("Actualizar producto")
    menu_ver_productos()
    id_prod = validar_input_int("Ingrese el ID del producto a actualizar: ")
    producto_actual = db_manager.buscar_producto_por_id(id_prod)
    if not producto_actual:
        print("Producto no encontrado.")
        return
    print(f"En edicion: {producto_actual[1]}")
    nuevo_nombre = input(f"Nuevo nombre de {producto_actual[1]}: ").strip or producto_actual[1]
    nuevo_desc = input(f"Nueva descripcion de {producto_actual[2]}: ").strip or producto_actual[2]
    nuevo_cantidad = input(f"Nueva cantidad de {producto_actual[3]}: ").strip or producto_actual[3]
    nuevo_precio = input(f"Nuevo precio de {producto_actual[4]}: ").strip or producto_actual[4]
    nuevo_categ = input(f"Nueva categoria de {producto_actual[5]}: ").strip or producto_actual[5]
    if db_manager.actualizar_producto(id_prod, nuevo_nombre, nuevo_desc, nuevo_cantidad, nuevo_precio, nuevo_categ):
        print("Producto actualizado con exito.")
    else:
        print("Error al actualizar producto.")

def menu_eliminar():
    print("Eliminar un Producto")
    menu_ver_productos()
    id_prod = validar_input_int("Ingrese el ID del producto a eliminar: ")
    confirmar = input (f"¿Confirma que quiere borrar el producto ID {id_prod}? (s/n): ").lower()
    if confirmar == 's':
        if db_manager.eliminar_producto(id_prod):
                print("Producto eliminado con exito.")
    else:
        print("No hubo coincidencias con el ID.")

def menu_buscar():
    print("Buscar un producto")
    print("1.Buscar por ID")
    print("2.Buscar por NOMBRE o CATEGORIA")
    opcion = input("Seleccione una opcion: ")
    if opcion == '1':
        id_prod = validar_input_int("ID")
        res = db_manager.buscar_producto_por_id(id_prod)
        if res:
            mostrar_tabla([res])
    elif opcion == '2':
        termino = validar_input_string("Termino de busqueda")
        res = db_manager.buscar_producto_por_nombre(termino)
        mostrar_tabla(res)
    else:
        print("Opcion invalida.")

def menu_reporte():
    print("Reporte de stock")
    limite = validar_input_int("Ingrese la cantidad limite del producto: ")
    res = db_manager.reporte_bajo_stock(limite)
    if res:
        print(f"Se encontraron {len(res)} productos en stock con una cantidad menor a {limite}")
        mostrar_tabla(res)
    else:
        print("No hay productos con un stock menor al indicado.")

def main():
    db_manager.inicializar_db()
    while True:
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
        opcion = input("\nSeleccione una opcion: ").strip()
        if opcion == '1':
            menu_registrar()
        elif opcion == '2':
            menu_ver_productos()
        elif opcion == '3':
            menu_actualizar()
        elif opcion == '4':
            menu_eliminar()
        elif opcion == '5':
            menu_buscar
        elif opcion == '6':
            menu_reporte()
        elif opcion == '7':
            print("Preparando todo para salir...")
            sys.exit()
        else:
            print("Seleccione una opcion valida.")

if __name__ == "__main__":
    main()