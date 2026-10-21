"""Create a bar chart from the device summary JSON file."""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INPUT_PATH = Path("output/device_summary.json")
OUTPUT_PATH = Path("output/average_temperature_chart.png")


def load_device_summary(input_path: Path) -> List[Dict[str, Any]]:
    """Load and lightly validate device summary records from JSON."""
    try:
        with input_path.open(encoding="utf-8") as json_file:
            records = json.load(json_file)
    except FileNotFoundError:
        raise ValueError(f"Input JSON file not found: {input_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Input JSON file is not valid JSON: {input_path}")

    if not isinstance(records, list):
        raise ValueError("Input JSON must contain a list of device records.")

    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each device record must be a JSON object.")
        if "device_id" not in record or "average_temperature" not in record:
            raise ValueError(
                "Each device record must contain device_id and "
                "average_temperature."
            )

    return records


def create_chart(records: List[Dict[str, Any]], output_path: Path) -> None:
    """Create and save an average-temperature bar chart."""
    if not records:
        print("No device records found. Chart was not generated.")
        return

    device_ids = [record["device_id"] for record in records]
    average_temperatures = [
        record["average_temperature"] for record in records
    ]

    bars = plt.bar(device_ids, average_temperatures)
    for bar, temperature in zip(bars, average_temperatures):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{temperature:.2f}",
            ha="center",
            va="bottom",
        )
    plt.xlabel("Device ID")
    plt.ylabel("Average Temperature")
    plt.title("Average Temperature by Device")
    plt.axhline(
        y=80.0,
        color="red",
        linestyle="--",
        label="80.0 threshold",
    )
    plt.legend()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()


def main() -> int:
    """Load device summaries and generate the chart."""
    parser = argparse.ArgumentParser(
        description="Generate an average-temperature chart."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=INPUT_PATH,
        help="Path to the device summary JSON file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_PATH,
        help="Path for the generated chart PNG.",
    )
    args = parser.parse_args()

    try:
        records = load_device_summary(args.input)
        create_chart(records, args.output)
    except ValueError as error:
        print(f"Error: {error}")
        return 1

    if records:
        print(f"Chart generated: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
