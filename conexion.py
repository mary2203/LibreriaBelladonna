import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


def conectar():
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        return conexion

    except mysql.connector.Error as error:
        print(f"Error al conectar con MySQL: {error}")
        return None