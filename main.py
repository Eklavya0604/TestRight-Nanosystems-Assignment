"""CLI entry point for the device log summarizer."""

import argparse
from pathlib import Path

from src.summarizer import (
    aggregate_devices,
    export_to_json,
    filter_devices,
    print_summary,
    read_telemetry,
)


def main() -> int:
    """Read telemetry, summarize it, and export the results."""
    parser = argparse.ArgumentParser(description="Summarize device telemetry.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/device_telemetry.csv"),
        help="Path to the telemetry CSV file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Path for the summary JSON file.",
    )
    parser.add_argument(
        "--chart",
        action="store_true",
        help="Generate the matching average-temperature chart too.",
    )
    args = parser.parse_args()

    if args.output is None:
        if args.input.name == "device_telemetry.csv":
            output_path = Path("output/device_summary.json")
        else:
            output_path = Path("output", f"{args.input.stem}_summary.json")
    else:
        output_path = args.output

    try:
        records = read_telemetry(args.input)
    except FileNotFoundError:
        print(f"Error: input file not found: {args.input}")
        return 1
    except ValueError as error:
        print(f"Error: {error}")
        return 1

    if not records:
        print("No valid telemetry records found.")

    summaries = filter_devices(aggregate_devices(records))
    export_to_json(summaries, output_path)
    print_summary(summaries)
    print(f"JSON output written to {output_path}")

    if args.chart:
        from chart import create_chart, load_device_summary

        if args.input.name == "device_telemetry.csv":
            chart_output = Path("output/average_temperature_chart.png")
        else:
            chart_output = Path(
                "output",
                f"{args.input.stem}_average_temperature_chart.png",
            )

        try:
            chart_records = load_device_summary(output_path)
            create_chart(chart_records, chart_output)
        except ValueError as error:
            print(f"Error: {error}")
            return 1

        if chart_records:
            print(f"Chart generated: {chart_output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
