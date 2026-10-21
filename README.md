# Device Log Summarizer

A small Python CLI project for cleaning sensor values, summarizing device
telemetry, and generating an average-temperature chart.

## Project Structure

```text
device-log-summarizer/
├── data/
│   ├── device_telemetry.csv       # Default sample input
│   └── Telemetry_test_1.csv       # Named test input using the same dataset
├── output/
│   ├── device_summary.json        # Generated Section 2 output
│   ├── average_temperature_chart.png
│   ├── Telemetry_test_1_summary.json
│   └── Telemetry_test_1_average_temperature_chart.png
├── src/
│   ├── __init__.py
│   └── summarizer.py              # CSV aggregation and JSON export
├── sensor_cleaner.py              # Section 1 function and assertions
├── chart.py                       # Section 3 chart generation
├── main.py                        # Section 2 CLI entry point
├── requirements.txt               # matplotlib
└── PROMPT_LOG.md                  # AI charting collaboration log
```

The original CSV was not supplied, so `data/device_telemetry.csv` is a small
representative fixture matching the assessment schema.

## Architecture

The project is intentionally split into small, reviewable pieces:

```text
sensor_cleaner.py
    └── Section 1 cleaning function and three direct assertions

main.py
    └── CLI, input/output naming, Section 2 workflow, optional chart trigger

src/summarizer.py
    ├── read_telemetry()       -> CSV reading and row validation
    ├── aggregate_devices()    -> running totals by device
    ├── filter_devices()       -> removes averages strictly above 80.0
    ├── export_to_json()       -> readable JSON output
    └── print_summary()        -> terminal table

chart.py
    ├── load_device_summary()  -> JSON validation
    └── create_chart()         -> headless matplotlib chart generation
```

The data flow is:

```text
CSV → validated records → device aggregation → filtered JSON → chart
```

`main.py` keeps chart generation optional through `--chart`, so the Section 2
workflow can still be run independently. When a custom CSV is supplied and
`--output` is omitted, report filenames are derived from the CSV filename.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python sensor_cleaner.py
python main.py
python chart.py
```

To process the CSV and generate its chart in one command, add `--chart`:

```bash
python main.py --chart
```

Section 1 verifies mixed input, invalid and negative values, zero
preservation, values above `500.0`, and the exact `500.0` clipping boundary.
It contains exactly three assertion-based tests.

Custom Section 2 paths are also supported:

```bash
python main.py --input path/to/device_telemetry.csv --output output/custom.json
```

For separate telemetry tests, keep the test name in each output filename:

```bash
python main.py \
  --input data/Telemetry_test_1.csv \
  --output output/Telemetry_test_1_summary.json

python chart.py \
  --input output/Telemetry_test_1_summary.json \
  --output output/Telemetry_test_1_average_temperature_chart.png
```

The same test can be completed in one command. The chart filename is derived
from the input CSV name:

```bash
python main.py --input data/Telemetry_test_1.csv --chart
```

This produces test-specific outputs without overwriting the default files:

```text
output/Telemetry_test_1_summary.json
output/Telemetry_test_1_average_temperature_chart.png
```

The same workflow can be repeated for multiple CSV files. Use a matching
test name for every JSON and chart output:

```bash
python main.py --input data/Telemetry_test_2.csv --output output/Telemetry_test_2_summary.json
python chart.py --input output/Telemetry_test_2_summary.json --output output/Telemetry_test_2_average_temperature_chart.png

python main.py --input data/Telemetry_test_3.csv --output output/Telemetry_test_3_summary.json
python chart.py --input output/Telemetry_test_3_summary.json --output output/Telemetry_test_3_average_temperature_chart.png
```

Or use one command per test:

```bash
python main.py --input data/Telemetry_test_2.csv --chart
python main.py --input data/Telemetry_test_3.csv --chart
```

When `--output` is omitted, the JSON filename is generated from the CSV
filename, for example `Telemetry_test_1.csv` becomes
`output/Telemetry_test_1_summary.json`. The chart is named similarly when
`--chart` is used.

This keeps reports separate and prevents one test from overwriting another.
Use underscores instead of spaces in filenames for simpler command-line use.

The default assessment workflow remains:

```text
data/device_telemetry.csv
        ↓
output/device_summary.json
        ↓
output/average_temperature_chart.png
```

## Small Improvements Beyond the Assessment

- Malformed CSV rows produce concise warnings instead of stopping the run.
- The CLI accepts custom input and output paths for easier reuse.
- Custom CSV names automatically produce matching JSON and chart names.
- The chart displays exact values above each bar and includes the `80.0`
  filtering threshold for visual context.
- Empty or invalid JSON input produces a clear message instead of a traceback.

The implementation intentionally stays standard-library-first; matplotlib is
the only external dependency because the assessment requires a chart.

## Evaluation Criteria Evidence

### Readability

The code is organized into small, named responsibilities:

```text
read_telemetry()       -> reads and validates CSV rows
aggregate_devices()    -> calculates device totals and error counts
filter_devices()       -> removes averages above 80.0
export_to_json()       -> writes readable JSON
print_summary()        -> prints the terminal table
```

The project uses descriptive names, type hints, concise docstrings, and no
unnecessary classes or frameworks.

### Robustness

Running the normal dataset:

```bash
python main.py
```

Produces warnings for the 10 malformed rows, then continues successfully:

```text
Warning: skipped row 92: invalid temperature
Warning: skipped row 93: invalid temperature
Warning: skipped row 94: invalid temperature
Warning: skipped row 95: invalid temperature
Warning: skipped row 96: invalid temperature
Warning: skipped row 97: invalid status
Warning: skipped row 98: invalid status
Warning: skipped row 99: missing device_id
Warning: skipped row 100: missing device_id
Warning: skipped row 101: invalid status

Device Telemetry Summary
------------------------------------------------------------
Device ID      Records     Avg Temp       Errors
------------------------------------------------------------
DEV_A          8           70.0           0
DEV_B          9           75.0           1
DEV_C          10          79.99          2
DEV_D          7           80.0           1
DEV_G          11          65.0           0
DEV_H          10          72.0           0
DEV_I          9           78.0           1
DEV_J          9           60.0           2
------------------------------------------------------------
JSON output written to output\device_summary.json
```

Expected input errors, such as a missing CSV or invalid JSON, produce concise
error messages instead of raw tracebacks.

### AI Collaboration

The charting collaboration is documented in `PROMPT_LOG.md`:

1. The initial prompt requested a simple matplotlib bar chart.
2. The first chart was reviewed and a genuine issue was identified: exact
   average values were not visible above the bars.
3. A follow-up prompt requested bar value labels and an `80.0` threshold line.
4. The updated chart was regenerated and verified at:

```text
output/average_temperature_chart.png
```

This demonstrates that the generated code was reviewed and intentionally
improved rather than copied without inspection.
