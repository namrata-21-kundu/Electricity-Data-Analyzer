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

    for index, row in df.iterrows():    #access one row at a time
        cursor.execute(
            query,
            (row["timestamp"], row["usage_kwh"])
        )

    connection.commit()

    cursor.close()
    connection.close()

    print(f"{len(df)} rows inserted successfully.")