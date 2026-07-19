from db.connection import connect_db

from utils.loader import load_csv

connection = connect_db()

if connection:
    print("Database connection successful!")
    connection.close()
    print("Connection closed.")
else:
    print("Connection failed.")

load_csv("data/sample_usage.csv")