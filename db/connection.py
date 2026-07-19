import mysql.connector
from mysql.connector import Error
import os   #reads values from .env
from dotenv import load_dotenv  #loads environment variables into py

load_dotenv()

def connect_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            #print("Connected to MySQL database.")
            return connection

    except Error as e:
        print(f"Database connection failed: {e}")
        return None