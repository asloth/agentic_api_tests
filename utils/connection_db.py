import sqlite3
import os
from typing import List, Tuple, Optional, Any

class DatabaseConnection:
    """Usa esta Tool para conectarte a la base de datos SQLite y ejecutar consultas SQL.
    Clase para manejar la conexión y consultas a la base de datos library_database.db"""
    
    def __init__(self):
        """Inicializa la conexión a la base de datos"""
        self.db_path = self._get_database_path()
        self.connection = None
    
    def _get_database_path(self) -> str:
        """Obtiene la ruta de la base de datos en la carpeta utils"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "library_database.db")
    
    def connect(self) -> bool:
        """Establece conexión con la base de datos"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Para acceder a columnas por nombre
            return True
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return False
    
    def disconnect(self) -> None:
        """Cierra la conexión con la base de datos"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def get_tables(self) -> List[str]:
        """
        Obtiene la lista de todas las tablas en la base de datos.
        """
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT name 
                FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """)
            tables = [row[0] for row in cursor.fetchall()]
            return tables
        except sqlite3.Error as e:
            print(f"Error al obtener las tablas: {e}")
            return []
    
    def get_table_schema(self, table_name: str) -> List[Tuple]:
        """Obtiene el esquema de una tabla específica
        Args:
            table_name (str): Nombre de la tabla e.g. "books"
        Returns:
            List[Tuple]: Lista de tuplas con la información de las columnas de la tabla
        """
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener el esquema de la tabla {table_name}: {e}")
            return []
    
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[sqlite3.Row]:
        """Ejecuta una consulta SELECT y retorna los resultados
        
        Args:
            query (str): Consulta SQL a ejecutar. e.g "SELECT * FROM books WHERE author = ?"
            params (Optional[Tuple]): Parámetros para la consulta SQL. e.g. ('J.K. Rowling',)
        Returns:
            List[sqlite3.Row]: Resultados de la consulta
        """
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []
    
    def execute_command(self, command: str, params: Optional[Tuple] = None) -> bool:
        """Ejecuta un comando INSERT, UPDATE o DELETE
        Args:
            command (str): Comando SQL a ejecutar. e.g "INSERT INTO books (title, author) VALUES (?, ?)"
            params (Optional[Tuple]): Parámetros para el comando SQL. e.g. ('New Book', 'Some Author')
        Returns:
            bool: True si el comando se ejecutó exitosamente, False en caso contrario
        """
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(command, params)
            else:
                cursor.execute(command)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al ejecutar el comando: {e}")
            self.connection.rollback()
            return False
    
    def get_foreign_keys(self) -> List[dict]:
        """
        Obtiene información de las foreign keys (claves foráneas) de todas las tablas.
        
        Returns:
            List[dict]: Lista de diccionarios con información de foreign keys. e.g. {'constraint_name': 'FK_sales_user_id_users', 'table_name': 'sales', 'column_name': 'user_id', 'referenced_table_name': 'users', 'referenced_column_name': 'user_id'}
        """
        if not self.connection:
            if not self.connect():
                return []
        
        foreign_keys = []
        tables = self.get_tables()
        
        for table in tables:
            try:
                cursor = self.connection.cursor()
                cursor.execute(f"PRAGMA foreign_key_list({table})")
                fk_info = cursor.fetchall()
                
                for fk in fk_info:
                    foreign_key = {
                        "constraint_name": f"FK_{table}_{fk[3]}_{fk[2]}",  # Nombre generado
                        "table_name": table,
                        "column_name": fk[3],  # from column
                        "referenced_table_name": fk[2],  # table
                        "referenced_column_name": fk[4]  # to column
                    }
                    foreign_keys.append(foreign_key)
                    
            except sqlite3.Error as e:
                print(f"Error al obtener foreign keys de la tabla {table}: {e}")
        
        return foreign_keys

    def get_database_info(self) -> dict:
        """Obtiene información completa de la base de datos"""
        info = {
            "database_path": self.db_path,
            "tables": [],
            "exists": os.path.exists(self.db_path)
        }
        
        if not info["exists"]:
            return info
        
        tables = self.get_tables()
        info["tables"] = []
        
        for table in tables:
            schema = self.get_table_schema(table)
            table_info = {
                "name": table,
                "columns": [
                    {
                        "name": col[1],
                        "type": col[2],
                        "not_null": bool(col[3]),
                        "default_value": col[4],
                        "primary_key": bool(col[5])
                    }
                    for col in schema
                ]
            }
            info["tables"].append(table_info)        
        
        return info

# Función de conveniencia para usar directamente
def get_db_connection() -> DatabaseConnection:
    """Retorna una instancia de DatabaseConnection"""
    return DatabaseConnection()

# Ejemplo de uso
if __name__ == "__main__":
    # Crear conexión
    db = DatabaseConnection()
    
    # Conectar
    if db.connect():
        print("Conexión establecida exitosamente")
        
        # Obtener lista de tablas (equivalente a tu consulta de information_schema)
        tables = db.get_tables()
        print(f"Tablas encontradas: {tables}")
        
        # Obtener foreign keys (equivalente a information_schema.key_column_usage)
        #foreign_keys = db.get_foreign_keys()
        #print(f"Foreign Keys encontradas:")
        #for fk in foreign_keys:
        #    print(f"  {fk}")
        
        # Obtener información completa de la base de datos
        #db_info = db.get_database_info()
        #print(f"Información de la base de datos: {db_info}")
        #
        ## Ejemplo de consulta
        if tables:
            books = db.execute_query("SELECT * FROM books LIMIT 3")
            print(f"Primeros 3 libros: {[dict(book) for book in books]}")
        
        # Cerrar conexión
        db.disconnect()
    else:
        print("No se pudo establecer la conexión")
