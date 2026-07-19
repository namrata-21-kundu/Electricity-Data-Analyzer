from db.connection import connect_db

connection = connect_db()

if connection:
    print("Database connection successful!")
    connection.close()
    print("Connection closed.")
else:
    print("Connection failed.")