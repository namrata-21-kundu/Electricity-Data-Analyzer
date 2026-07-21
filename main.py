import argparse

from utils.loader import load_csv
from analysis.trends import get_data, calculate_summary, plot_trend
from analysis.peak_hours import get_peak_hours
from analysis.cost import get_cost_summary
from analysis.anomalies import detect_anomalies
from assistant.router import route_query
from assistant.explain import explain

def main():
    parser = argparse.ArgumentParser(
        description="Electricity Analytics Platform"
    )

    parser.add_argument(
        "command",
        choices=[
            "load",
            "summary",
            "trend",
            "peak",
            "cost",
            "anomalies",
            "ask"
        ],
        help="Command to execute"
    )

    parser.add_argument(
    "input",
    nargs="?",
    help="CSV path (for load) or question (for ask)"
    )

    args = parser.parse_args()

    if args.command == "load":
        if not args.file:
            print("Please provide a CSV file.")
            return

        load_csv(args.input)

    elif args.command == "summary":
        df = get_data()
        calculate_summary(df)
    
    elif args.command == "trend":
        df = get_data()
        plot_trend(df)

    elif args.command == "peak":
        get_peak_hours()

    elif args.command == "cost":
        get_cost_summary()

    elif args.command == "anomalies":
        detect_anomalies()

    elif args.command == "ask":
        if not args.input:
            print("Please enter a question.")
            return

        question = args.input
        analysis = route_query(question)
        answer = explain(question, analysis)

        print("\n🤖 AI Explanation")
        print("-" * 40)
        print(answer)

if __name__ == "__main__":
    main()