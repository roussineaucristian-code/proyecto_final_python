import sqlite3
from config import DB_NAME, TABLE_NAME

def conectar_db():
    return sqlite3.connect(DB_NAME)

def inicializar_db():
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
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
            conn.commit()
    except sqlite3.Error as e:
        print(f"Errror al imprimir la base de datos: {e}")

def registrar_producto(nombre, descripcion, cantidad, precio, categoria):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {TABLE_NAME} (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)", (nombre, descripcion, cantidad, precio, categoria))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print (f"Error al registrar el producto: {e}")
        return False

def actualizar_producto(nombre, descripcion, cantidad, precio, categoria, id_prod):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            sql = f"UPDATE {TABLE_NAME} SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ? WHERE id = ?"
            cursor.execute(sql, (nombre, descripcion, cantidad, precio, categoria, id_prod))
            if cursor.rowcount > 0 :
                conn.commit()
                return True
            return False
    except sqlite3.Error as e:
        print (f"Error al actualizar el producto: {e}")
        return False

def listar_productos():
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME}")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print (f"Error al listar productos: {e}")
        return []

def buscar_producto_por_id(id_prod):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = ?", (id_prod))
            return cursor.fetchone()
    except sqlite3.Error as e:
        print (f"Error al buscar producto por id: {e}")
        return None

def buscar_producto_por_nombre(termino):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            querry = f"SELECT * FROM {TABLE_NAME} WHERE nombre LIKE ? OR categoria LIKE ?"
            cursor.execute(querry, (f"%{termino}%", f"%{termino}%"))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print (f"Error al buscar producto por nombre: {e}")
        return []

def eliminar_producto(id_prod):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = ?", (id_prod))
            if cursor.rowcount > 0 :
                conn.commit()
                return True
            return False
    except sqlite3.Error as e:
        print (f"Error al eliminar producto: {e}")
        return False

def reporte_bajo_stock(limite):
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE cantidad <= ?", (limite))
            conn.commit()
            return cursor.fetchall()
    except sqlite3.Error as e:
        print (f"Error al generar reporte: {e}")
        return []