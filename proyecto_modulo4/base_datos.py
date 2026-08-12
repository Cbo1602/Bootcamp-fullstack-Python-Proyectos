# base_datos.py
import sqlite3
from exepciones import ClienteError


class BaseDatos:

    def __init__(self, db_name="clientes.db"):
        self.db_name = db_name
        self.inicializar_bd()

    def obtener_conexion(self):
        """Retorna una conexión activa a la base de datos SQLite."""
        return sqlite3.connect(self.db_name)

    def inicializar_bd(self):
        """Crea la tabla 'clientes' si aún no existe."""
        try:
            with self.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS clientes (
                        identificador INTEGER PRIMARY KEY,
                        tipo TEXT NOT NULL,
                        nombre TEXT NOT NULL,
                        email TEXT NOT NULL,
                        telefono TEXT NOT NULL,
                        direccion TEXT NOT NULL,
                        dato1 TEXT,
                        dato2 TEXT
                    )
                """
                )
                conexion.commit()
        except sqlite3.Error as e:
            raise ClienteError(f"Error al inicializar la base de datos: {e}")

    def guardar_cliente(
        self,
        identificador,
        tipo,
        nombre,
        email,
        telefono,
        direccion,
        dato1,
        dato2="",
    ):
        """Inserta o actualiza un cliente en la base de datos."""
        try:
            with self.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO clientes 
                    (identificador, tipo, nombre, email, telefono, direccion, dato1, dato2)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        identificador,
                        tipo,
                        nombre,
                        email,
                        telefono,
                        direccion,
                        str(dato1),
                        str(dato2),
                    ),
                )
                conexion.commit()
        except sqlite3.Error as e:
            raise ClienteError(f"Error al guardar cliente en la BD: {e}")

    def eliminar_cliente(self, identificador):
        """Elimina un cliente de la base de datos usando su ID."""
        try:
            with self.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    "DELETE FROM clientes WHERE identificador = ?",
                    (identificador,),
                )
                conexion.commit()
        except sqlite3.Error as e:
            raise ClienteError(f"Error al eliminar cliente de la BD: {e}")

    def cargar_todos(self):
        """Obtiene todos los registros almacenados en la base de datos."""
        try:
            with self.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM clientes")
                return cursor.fetchall()
        except sqlite3.Error as e:
            raise ClienteError(f"Error al consultar la BD: {e}")