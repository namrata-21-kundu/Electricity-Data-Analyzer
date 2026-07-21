import pandas as pd
import matplotlib.pyplot as plt
from analysis.trends import get_data

def get_peak_hours():
    df = get_data()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    hourly_usage = df.groupby("hour")["usage_kwh"].mean()
    
    peak_hour = hourly_usage.idxmax()
    peak_usage = hourly_usage.max()

    print("\nPeak Usage Analysis")
    print(f"Peak Hour     : {peak_hour}:00")
    print(f"Average Usage : {peak_usage:.2f} kWh")

    plt.figure(figsize=(10,5))

    plt.bar(hourly_usage.index, hourly_usage.values)

    plt.title("Average Electricity Usage by Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Usage (kWh)")
    plt.xticks(range(24))

    plt.tight_layout()

    plt.savefig("charts/peak_hours.png")

    plt.close()

    print("Chart saved to charts/peak_hours.png")

    return {
    "peak_hour": peak_hour,
    "average_usage": peak_usage
    }
