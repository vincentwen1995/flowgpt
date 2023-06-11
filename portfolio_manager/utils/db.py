import psycopg2
from contextlib import contextmanager


@contextmanager
def create_db_connection(host: str, port: int, database: str, user: str, password: str):
    """
    Context manager to create and close a connection to a PostgreSQL database.
    """
    connection = None
    try:
        connection = psycopg2.connect(
            host=host, port=port, database=database, user=user, password=password
        )
        print("Connection to PostgreSQL database successful")
        yield connection
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
    finally:
        if connection:
            connection.close()
            print("PostgreSQL database connection closed")
