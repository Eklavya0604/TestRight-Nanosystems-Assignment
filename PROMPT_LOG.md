# PROMPT_LOG

## Initial Prompt

I asked the AI to create a Python script named `chart.py` that:

- loads `output/device_summary.json`
- extracts `device_id` and `average_temperature`
- generates a matplotlib bar chart
- labels both axes
- adds a chart title
- saves the chart to `output/average_temperature_chart.png`

I also asked it to keep the implementation simple and avoid modifying the
Section 2 processing logic.

## Issue Observed

The first chart was functionally correct, but the exact average temperature
values were not displayed above the bars. This meant the viewer had to
estimate the values from the y-axis.

## Follow-up Prompt

I asked the AI to improve only the visualization by:

- displaying the exact average temperature above each bar
- adding an `80.0` reference line for the Section 2 filtering threshold
- keeping the existing JSON loading and chart structure unchanged
- preserving the same output filename

## Final Verification

The updated chart was generated successfully. It displays the exact average
temperature values and the `80.0` threshold line while preserving the original
data-processing logic. The chart was saved to:

`output/average_temperature_chart.png`

## Multiple Test Files

The project also supports processing separate telemetry tests without
overwriting previous reports. Each CSV can be given its own JSON and chart
output path using the CLI arguments documented in `README.md`, for example:

```text
Telemetry_test_1.csv
Telemetry_test_1_summary.json
Telemetry_test_1_average_temperature_chart.png
```

This is a project usage convention, not a change to the Section 2 data
processing logic.

## Architecture Decisions

The implementation was kept deliberately small for the assessment:

- Section 1 remains a standalone standard-library function with three direct
  assertion tests.
- Section 2 is split into focused functions for reading, aggregation,
  filtering, JSON export, and terminal output.
- `main.py` owns the CLI workflow and supports an optional `--chart` flag.
- `chart.py` keeps JSON validation and visualization separate from CSV
  processing and uses Matplotlib's headless `Agg` backend.
- Custom input filenames automatically produce matching summary and chart
  filenames when no explicit output path is supplied.
- No classes, frameworks, databases, or unnecessary dependencies were added.

This keeps the assessment requirements visible while allowing one command to
produce a complete named report for each telemetry test file.
