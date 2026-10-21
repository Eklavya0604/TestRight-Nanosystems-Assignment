"""Clean and normalize mixed sensor readings."""

from typing import List, Sequence


def clean_sensor_readings(readings: Sequence[object]) -> List[float]:
    """Return valid, non-negative sensor readings capped at 500.0."""
    cleaned_readings: List[float] = []

    for reading in readings:
        try:
            numeric_reading = float(reading)
        except (TypeError, ValueError, OverflowError):
            continue

        if numeric_reading < 0:
            continue

        cleaned_readings.append(min(numeric_reading, 500.0))

    return cleaned_readings


if __name__ == "__main__":
    # Test 1: mixed valid, invalid, negative, zero, and oversized values.
    mixed_readings = [
        10,
        25.5,
        "45.5",
        None,
        "invalid",
        -3,
        0,
        500.0,
        750,
    ]
    assert clean_sensor_readings(mixed_readings) == [
        10.0,
        25.5,
        45.5,
        0.0,
        500.0,
        500.0,
    ]

    # Test 2: empty input.
    assert clean_sensor_readings([]) == []

    # Test 3: no valid readings.
    invalid_readings = [None, "not-a-number", -1, -20.5]
    assert clean_sensor_readings(invalid_readings) == []

    print("All sensor cleaner tests passed.")
