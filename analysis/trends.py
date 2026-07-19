import pandas as pd
from db.connection import connect_db

def get_data():
    connection = connect_db()

    query = """
            SELECT *
            FROM readings
            """
    
    df = pd.read_sql(query, connection)
    
    connection.close()
    return df