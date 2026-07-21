import matplotlib.pyplot as plt
from analysis.trends import get_data

RATE_PER_UNIT = 8

def get_cost_summary():
    df = get_data()
    total_units = df["usage_kwh"].sum()
    average_units = df["usage_kwh"].mean()

    estimated_cost = total_units * RATE_PER_UNIT

    print("\nElectricity Cost Analysis")
    print("-" * 30)
    print(f"Total Consumption : {total_units:.2f} kWh")
    print(f"Average Usage     : {average_units:.2f} kWh")
    print(f"Rate per Unit     : ₹{RATE_PER_UNIT}")
    print(f"Estimated Bill    : ₹{estimated_cost:.2f}")


    plt.figure(figsize=(6,5))

    plt.bar(
        ["Consumption (kWh)", "Estimated Cost (₹)"],
        [total_units, estimated_cost]
    )

    plt.title("Electricity Consumption and Estimated Cost")

    plt.tight_layout()

    plt.savefig("charts/cost_breakdown.png")

    plt.close()

    print("\nChart saved to charts/cost_breakdown.png")

    return {
    "total_units": total_units,
    "average_usage": average_units,
    "rate_per_unit": RATE_PER_UNIT,
    "estimated_cost": estimated_cost
    }