import pyodbc
from config import database_config

#creates a database connection to Azure SQL that can be easily reused
def db_connection():
    conn = pyodbc.connect(
        f"DRIVER={database_config['driver']};"
        f"SERVER={database_config['server']};"
        f"DATABASE={database_config['database']};"
        f"UID={database_config['username']};"
        f"PWD={database_config['password']}"
    )
    return conn