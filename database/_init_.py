import psycopg2
from psycopg2 import sql, DatabaseError
from config import db_config

dbname = db_config['dbname']

def create_database(dbname):
    try:
        conn = psycopg2.connect(
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port']
        )
        
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(
            sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s;"),
            [dbname]
        )

        exists = cursor.fetchone()

        if exists:
            print(f"База данных '{dbname}' уже существует.")
        else:
            cursor.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(dbname)))
            print(f"База данных '{dbname}' успешно создана.")

    except DatabaseError as e:
        print(f"Ошибка базы данных: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

create_database(dbname)
