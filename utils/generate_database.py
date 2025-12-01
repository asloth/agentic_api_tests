import sqlite3
import os

def create_database_structure():
    """Creates a SQLite database for storing book information."""
    # Crear la BD en la misma carpeta que este script (utils)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_name = os.path.join(script_dir, "library_database.db")


    conexion = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    
    # Create table books
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            published_year INTEGER,
            genre TEXT
        )
    ''')

    #Create table users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Create table sales
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            sale_date TEXT,
            total_amount DECIMAL(10, 2),
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')

    # Create a sales_details table
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS sales_details (
            sale_id INTEGER,
            book_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY(sale_id) REFERENCES sales(sale_id),
            FOREIGN KEY(book_id) REFERENCES books(book_id),
            PRIMARY KEY (sale_id, book_id)
        )
    ''')


    conexion.commit()
    conexion.close()
    print(f"Database '{db_name}' created with 'books', 'users', 'sales', and 'sales_details' tables.")

def ingest_data_into_database():
    """Ingests initial data into the database tables."""
    # Crear la BD en la misma carpeta que este script (utils)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_name = os.path.join(script_dir, "library_database.db")
    conexion = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    
    # Insert sample data into books table
    books_data = [
        ("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Fiction"),
        ("To Kill a Mockingbird", "Harper Lee", 1960, "Fiction"),
        ("1984", "George Orwell", 1949, "Dystopian"),
        ("Pride and Prejudice", "Jane Austen", 1813, "Romance"),
        ("The Picture of Dorian Gray", "Oscar Wilde", 1890, "Philosophical Fiction"),
        ("I'm robot", "Isaac Asimov", 1950, "Science Fiction")
    ]
    cursor.executemany('''
        INSERT INTO books (title, author, published_year, genre)
        VALUES (?, ?, ?, ?)
    ''', books_data)


    # Insert sample data into users table
    users_data = [
        ("Alice Johnson", "alice.johnson@example.com"),
        ("Bob Smith", "bob.smith@example.com"),
        ("Charlie Brown", "charlie.brown@example.com"),
        ("Diana Prince", "diana.prince@example.com"),
        ("Sara Benelli", "sara.benelli@example.com"),
        ("Geraldine Curupaco", "geraldine.curupaco@example.com")
        ]
    cursor.executemany('''
        INSERT INTO users (name, email)
        VALUES (?, ?)
    ''', users_data)


    # Insert sample data into sales table
    sales_data = [
        (1, "2025-11-01", 29.99),
        (2, "2025-11-02", 15.50),
        (3, "2025-11-03", 45.00),
        (1, "2025-11-04", 22.75),
        (4, "2025-11-05", 18.20)
    ]
    cursor.executemany('''
        INSERT INTO sales (user_id, sale_date, total_amount)
        VALUES (?, ?, ?)
    ''', sales_data)


    # Insert sample data into sales_details table
    sales_details_data = [
        (1, 1, 1),
        (1, 3, 2),
        (2, 2, 1),
        (3, 4, 1),
        (3, 5, 1),
        (4, 1, 1)
    ]
    cursor.executemany('''
        INSERT INTO sales_details (sale_id, book_id, quantity)
        VALUES (?, ?, ?)
    ''', sales_details_data)

    conexion.commit()
    conexion.close()
    print(f"Data ingested into database '{db_name}' successfully.")


if __name__ == "__main__":
    create_database_structure()
    ingest_data_into_database()
