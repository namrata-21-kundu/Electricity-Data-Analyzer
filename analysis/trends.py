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
   
    total_usage = df["usage_kwh"].sum()
    average_usage = df["usage_kwh"].mean()
    maximum_usage = df["usage_kwh"].max()
    minimum_usage = df["usage_kwh"].min()

    print(f"Total Usage: {total_usage:.2f} kWh")
    print(f"Average Usage: {average_usage:.2f} kWh")
    print(f"Maximum Usage: {maximum_usage:.2f} kWh")
    print(f"Minimum Usage: {minimum_usage:.2f} kWh")