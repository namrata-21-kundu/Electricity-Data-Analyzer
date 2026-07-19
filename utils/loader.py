import pandas as pd
from db.connection import connect_db

def load_csv(file_path):
    df = pd.read_csv(file_path)

    connection = connect_db()
    cursor = connection.cursor()

    query = """
    INSERT INTO readings(timestamp, usage_kwh)
    VALUES (%s, %s)
    """

    first_row = df.iloc[0]

    cursor.execute(
    query,
    (first_row["timestamp"], first_row["usage_kwh"])
    )
    
    connection.commit()

    cursor.close()
    connection.close()

    print("First row inserted successfully!")