import pandas as pd
import mysql.connector
from mysql.connector import Error
import configparser
import os

def leer_config(filename='config.ini', section='mysql'):
    """
    Lee el archivo de configuración desde el directorio raíz del proyecto.
    Esta función es robusta y puede ser llamada desde cualquier archivo del proyecto.
    """
    # __file__ es la ruta del archivo actual (db_logic.py)
    script_dir = os.path.dirname(__file__)
    config_path = os.path.join(script_dir, filename)
    
    parser = configparser.ConfigParser()
    parser.read(config_path)
    
    if parser.has_section(section):
        return dict(parser.items(section))
    else:
        raise Exception(f"No se pudo encontrar la sección '{section}' en {config_path}. Asegúrate de que tu archivo 'config.ini' está en el directorio principal.")

def ejecutar_comando(comando_sql, valores=None):
    """
    Ejecuta comandos que MODIFICAN la base de datos (INSERT, UPDATE, DELETE).
    """
    db_params = leer_config()
    connection = None
    try:
        connection = mysql.connector.connect(**db_params)
        cursor = connection.cursor()
        cursor.execute(comando_sql, valores)
        connection.commit()
        return True
    except Error as e:
        print(f"Error en la operación de base de datos: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            connection.close()

def ejecutar_consulta(query):
    """
    Ejecuta comandos que LEEN datos de la base de datos (SELECT).
    """
    db_params = leer_config()
    connection = None
    try:
        connection = mysql.connector.connect(**db_params)
        return pd.read_sql(query, connection)
    except Error as e:
        print(f"Error al consultar la base de datos: {e}")
        return pd.DataFrame()
    finally:
        if connection and connection.is_connected():
            connection.close()