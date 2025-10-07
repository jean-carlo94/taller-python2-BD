import os
import pymysql
from dotenv import load_dotenv
from pymysql.cursors import DictCursor

load_dotenv()

class DataBaseExecute:
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT")),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database=os.getenv("DB_DATA"),
                cursorclass=DictCursor
            )
            self.cursor = self.connection.cursor()
        except pymysql.MySQLError as e:
            print(f"❌ Error al conectar con la base de datos: {e}")
            self.connection = None
            self.cursor = None
        
    def __del__(self):
        try:
            if hasattr(self, "cursor") and self.cursor:
                self.cursor.close()
            if hasattr(self, "connection") and self.connection:
                self.connection.close()
        except Exception as e:
            print(f"⚠️ Error cerrando la conexión: {e}")
            
    # ────────────────────────────────────────────────
    # MÉTODOS CRUD BÁSICOS
    # ────────────────────────────────────────────────
        
    def find(self, table: str, id: int):
        query = f"SELECT * FROM {table} WHERE id = %s"
        return self._execute_fetchone(query, (id,))

    def find_by(self, table: str, column: str, value: str):
        query = f"SELECT * FROM {table} WHERE {column} = %s"
        return self._execute_fetchall(query, (value,))

    def find_all(self, table: str):
        query = f"SELECT * FROM {table}"
        return self._execute_fetchall(query)

    def insert(self, table: str, data: dict):
        keys = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
        return self._execute_commit(query, tuple(data.values()))

    def update(self, table: str, id: int, data: dict):
        set_clause = ", ".join([f"{k}=%s" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE id = %s"
        params = tuple(data.values()) + (id,)
        return self._execute_commit(query, params)

    def delete(self, table: str, id: int):
        query = f"DELETE FROM {table} WHERE id = %s"
        return self._execute_commit(query, (id,))

    
    def execute_query(self, query: str, params: tuple = None):
        return self._execute_fetchall(query, params)

    def execute_procedure(self, procedure_name: str, params: tuple = None):
        try:
            self.cursor.callproc(procedure_name, params or ())
            result = self.cursor.fetchall()
            self.connection.commit()
            return result
        except pymysql.MySQLError as e:
            print(f"❌ Error ejecutando procedimiento {procedure_name}: {e}")
            return None
        
    # ────────────────────────────────────────────────
    # EJECUCIÓN DE QUERYS Y PROCEDIMIENTOS
    # ────────────────────────────────────────────────
        
    def _execute_fetchall(self, query: str, params: tuple = None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"❌ Error ejecutando SELECT: {e}")
            return []

    def _execute_fetchone(self, query: str, params: tuple = None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"❌ Error ejecutando SELECT: {e}")
            return None

    def _execute_commit(self, query: str, params: tuple = None):
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor.lastrowid or self.cursor.rowcount
        except pymysql.MySQLError as e:
            print(f"❌ Error ejecutando operación de escritura: {e}")
            self.connection.rollback()
            return None
