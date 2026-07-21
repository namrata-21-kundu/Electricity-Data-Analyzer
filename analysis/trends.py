import pandas as pd
import matplotlib.pyplot as plt
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


def calculate_summary(df):
    total_usage = df["usage_kwh"].sum()
    average_usage = df["usage_kwh"].mean()
    maximum_usage = df["usage_kwh"].max()
    minimum_usage = df["usage_kwh"].min()

    print(f"Total Usage   : {total_usage:.2f} kWh")
    print(f"Average Usage : {average_usage:.2f} kWh")
    print(f"Maximum Usage : {maximum_usage:.2f} kWh")
    print(f"Minimum Usage : {minimum_usage:.2f} kWh")

    return {
    "total_usage": total_usage,
    "average_usage": average_usage,
    "maximum_usage": maximum_usage,
    "minimum_usage": minimum_usage
    }

def plot_trend(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    plt.figure(figsize=(10, 5))

    plt.plot(df["timestamp"], df["usage_kwh"], marker="o")

    plt.title("Electricity Usage Trend")
    plt.xlabel("Timestamp")
    plt.ylabel("Usage (kWh)")
    plt.xticks(rotation=45)

    plt.grid(True)

    plt.tight_layout()

    plt.savefig("charts/trend.png")

    plt.close()

    print("Chart saved to charts/trend.png")
