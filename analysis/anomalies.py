import matplotlib.pyplot as plt
import pandas as pd
from analysis.trends import get_data

def detect_anomalies():
    df = get_data()

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    #threshold = mean + 2 × standard deviation
    mean_usage = df["usage_kwh"].mean()
    std_usage = df["usage_kwh"].std()

    threshold = mean_usage + (2 * std_usage)

    anomalies = df[df["usage_kwh"] > threshold]

    print("\nElectricity Anomaly Detection")
    print("-" * 30)

    print(f"Threshold : {threshold:.2f} kWh\n")

    if anomalies.empty:
        print("No anomalies detected.")
    else:
        print("Anomalies Found:\n")
        print(anomalies[["timestamp", "usage_kwh"]])

    #plot
    plt.figure(figsize=(10,5))

    plt.plot(
        df["timestamp"],
        df["usage_kwh"],
        label="Usage"
    )

    plt.scatter(
        anomalies["timestamp"],
        anomalies["usage_kwh"],
        color="red",
        label="Anomaly"
    )

    plt.title("Electricity Usage with Anomalies")

    plt.xlabel("Timestamp")
    plt.ylabel("Usage (kWh)")

    plt.legend()

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("charts/anomalies.png")

    plt.close()

    print("\nChart saved to charts/anomalies.png")