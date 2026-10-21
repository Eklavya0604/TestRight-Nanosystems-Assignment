"""Read, summarize, filter, and export device telemetry."""

import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple


VALID_STATUSES = {"ACTIVE", "WARNING", "ERROR"}
REQUIRED_COLUMNS = {"device_id", "status", "temperature"}
TelemetryRecord = Tuple[str, str, float]


def read_telemetry(input_path: Path) -> List[TelemetryRecord]:
    """Read and validate usable telemetry records from a CSV file."""
    records: List[TelemetryRecord] = []

    with input_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        columns = set(reader.fieldnames or [])
        missing_columns = REQUIRED_COLUMNS - columns
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Missing required column(s): {missing}")

        for row_number, row in enumerate(reader, start=2):
            device_id = (row.get("device_id") or "").strip()
            status = (row.get("status") or "").strip()
            temperature_text = (row.get("temperature") or "").strip()

            if not device_id:
                print(f"Warning: skipped row {row_number}: missing device_id")
                continue
            if status not in VALID_STATUSES:
                print(f"Warning: skipped row {row_number}: invalid status")
                continue

            try:
                temperature = float(temperature_text)
            except (TypeError, ValueError, OverflowError):
                print(
                    f"Warning: skipped row {row_number}: invalid temperature"
                )
                continue

            records.append((device_id, status, temperature))

    return records


def aggregate_devices(
    records: List[TelemetryRecord],
) -> Dict[str, Dict[str, float]]:
    """Calculate record counts, temperature sums, and error counts by device."""
    aggregated: Dict[str, Dict[str, float]] = {}

    for device_id, status, temperature in records:
        device = aggregated.setdefault(
            device_id,
            {"total_records": 0, "temperature_sum": 0.0, "error_count": 0},
        )
        device["total_records"] += 1
        device["temperature_sum"] += temperature
        if status == "ERROR":
            device["error_count"] += 1

    return aggregated


def filter_devices(
    aggregated: Dict[str, Dict[str, float]],
) -> List[Dict[str, object]]:
    """Keep devices whose actual average temperature is at most 80.0."""
    summaries: List[Dict[str, object]] = []

    for device_id, values in aggregated.items():
        average = values["temperature_sum"] / values["total_records"]
        if average > 80.0:
            continue

        summaries.append(
            {
                "device_id": device_id,
                "total_records": int(values["total_records"]),
                "average_temperature": round(average, 2),
                "error_count": int(values["error_count"]),
            }
        )

    return summaries


def export_to_json(summaries: List[Dict[str, object]], output_path: Path) -> None:
    """Write device summaries as readable JSON, creating its directory."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(summaries, json_file, indent=4)
        json_file.write("\n")


def print_summary(summaries: List[Dict[str, object]]) -> None:
    """Print a readable summary table to the terminal."""
    print("\nDevice Telemetry Summary")
    print("-" * 60)
    print(f"{'Device ID':<15}{'Records':<12}{'Avg Temp':<15}{'Errors':<10}")
    print("-" * 60)

    if not summaries:
        print("No devices to display.")
    else:
        for summary in summaries:
            print(
                f"{summary['device_id']:<15}"
                f"{summary['total_records']:<12}"
                f"{summary['average_temperature']:<15}"
                f"{summary['error_count']:<10}"
            )

    print("-" * 60)
