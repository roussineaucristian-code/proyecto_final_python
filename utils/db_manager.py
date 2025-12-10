import sqlite3
# Importa las constantes DB_NAME (nombre del archivo de base de datos) 
# y TABLE_NAME (nombre de la tabla) desde un archivo de configuración.
from config import DB_NAME, TABLE_NAME
    
def conectar_db():
    """
    Establece una conexión a la base de datos SQLite.

    Returns:
        sqlite3.Connection: Objeto de conexión a la base de datos.
    """
    return sqlite3.connect(DB_NAME)

def inicializar_db():
    """
    Crea la tabla de productos si no existe.
    """
    try:
        # Usa 'with' para asegurar que la conexión se cierre automáticamente.
        with conectar_db() as conn:
            cursor = conn.cursor()
            # Define la estructura SQL para crear la tabla usando f-string para el nombre de la tabla.
            sql = f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT)
            '''
            cursor.execute(sql)
            conn.commit() # Confirma los cambios.
    except sqlite3.Error as e:
        # Captura y muestra errores específicos de SQLite.
        print(f"Errror al imprimir la base de datos: {e}")

def registrar_producto(nombre, descripcion, cantidad, precio, categoria):
    """
    Inserta un nuevo producto en la base de datos.

    Returns:
        bool: True si el registro fue exitoso, False en caso contrario.
    """
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {TABLE_NAME} (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)", (nombre, descripcion, cantidad, precio, categoria))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print (f"Error al registrar el producto: {e}")
        return False

def actualizar_producto(id_prod, nombre, descripcion, cantidad, precio, categoria):
    """
    Actualiza los detalles de un producto existente basado en su ID.

    Returns:
        bool: True si se actualizó al menos una fila, False en caso contrario.
    """
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            # Usa '?' como placeholders y pasa los datos como una tupla para prevenir inyecciones SQL.
            sql = f"UPDATE {TABLE_NAME} SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ? WHERE id = ?"
            # Se pasa id_prod al final de la tupla de valores.
            cursor.execute(sql, (nombre, descripcion, cantidad, precio, categoria, id_prod))
            if cursor.rowcount > 0 :
                conn.commit()
                return True
            # Devuelve False si el ID no existe (0 filas afectadas).
            return False
    except sqlite3.Error as e:
        print (f"Error al actualizar el producto: {e}")
        return False

def listar_productos():
    """
    Recupera todos los productos de la base de datos.

    Returns:
        list: Una lista de tuplas, donde cada tupla es una fila de la tabla.
    """
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME}")
            return cursor.fetchall() # Devuelve todas las filas.
    except sqlite3.Error as e:
        print (f"Error al listar productos: {e}")
        return []

def buscar_producto_por_id(id_prod):
    """
    Busca un producto específico usando su ID.

    Returns:
        tuple or None: La tupla del producto encontrado o None si no existe o hubo un error.
    """
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = ?", (id_prod,))
            return cursor.fetchone() # Devuelve la primera fila encontrada o None.
    except sqlite3.Error as e:
        print (f"Error al buscar producto por id: {e}")
        return None

def buscar_producto_por_nombre(termino):
    """
    Busca productos por nombre o categoría usando el operador LIKE para coincidencias parciales.

    Returns:
        list: Lista de productos coincidentes.
    """
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            querry = f"SELECT * FROM {TABLE_NAME} WHERE nombre LIKE ? OR categoria LIKE ?"
            # Se usan comodines (%) en la tupla de parámetros.
            cursor.execute(querry, (f"%{termino}%", f"%{termino}%"))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print (f"Error al buscar producto por nombre: {e}")
        return []

def eliminar_producto(id_prod):
    """
    Elimina un producto de la base de datos por su ID.

    Returns:
        bool: True si se eliminó al menos una fila, False en caso contrario.
    """
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = ?", (id_prod,))
            if cursor.rowcount > 0 :
                conn.commit()
                return True
            return False
    except sqlite3.Error as e:
        print (f"Error al eliminar producto: {e}")
        return False

def reporte_bajo_stock(limite):
    """
    Genera un listado de productos cuyo stock (cantidad) es menor o igual a un límite dado.

    Returns:
        list: Lista de productos (tuplas) con bajo stock.
    """
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE cantidad <= ?", (limite,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print (f"Error al generar reporte: {e}")
        return []