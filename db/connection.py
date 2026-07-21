import mysql.connector
from mysql.connector import Error
#import os   #reads values from .env
#from dotenv import load_dotenv  #loads environment variables into py
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

#load_dotenv()

def connect_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            #print("Connected to MySQL database.")
            return connection

    except Error as e:
        print(f"Database connection failed: {e}")
        return None