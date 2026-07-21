import argparse

from utils.loader import load_csv
from analysis.trends import get_data, calculate_summary, plot_trend
from analysis.peak_hours import get_peak_hours

def main():
    parser = argparse.ArgumentParser(
        description="Electricity Analytics Platform"
    )

    parser.add_argument(
        "command",
        choices=["load", "summary", "trend", "peak"],
        help="Command to execute"
    )

    parser.add_argument(
        "file",
        nargs="?",
        help="Path to CSV file (required for load command)"
    )

    args = parser.parse_args()

    if args.command == "load":
        if not args.file:
            print("Please provide a CSV file.")
            return

        load_csv(args.file)

    elif args.command == "summary":
        df = get_data()
        calculate_summary(df)
    
    elif args.command == "trend":
        df = get_data()
        plot_trend(df)

    elif args.command == "peak":
        get_peak_hours()

if __name__ == "__main__":
    main()