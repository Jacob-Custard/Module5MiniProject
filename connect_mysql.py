import mysql.connector
from mysql.connector import Error



def connect_database():
    db_name = "library_managment_db"
    user = "root"
    password = "FrostyBearSquash13#"
    host = "localhost"
    
    try:
        connection = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )

        print("Connected to MySql database successfully")
        return connection

    except Error as e:
        print(f"Error: {e}")
        return None