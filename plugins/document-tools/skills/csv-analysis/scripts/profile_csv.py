#!/usr/bin/env python3
"""Read a local delimited file and emit a bounded aggregate JSON report."""

import argparse
import csv
import json
import math
import re
import statistics
import sys
from datetime import date
from pathlib import Path


MISSING = frozenset(("", "NA", "N/A", "null"))
LARGE_FILE_BYTES = 100 * 1024 * 1024
SAMPLE_ROWS = 10_000


def summarize_column(name, cells):
    present = [cell for cell in cells if cell.strip() not in MISSING]
    result = {
        "name": name,
        "type": "unknown",
        "non_null": len(present),
        "missing": len(cells) - len(present),
        "unique": len(set(present)),
    }
    if not present:
        return result
    if all(cell.strip().lower() in ("true", "false") for cell in present):
        result["type"] = "boolean"
        return result
    try:
        numbers = [float(cell) for cell in present]
    except ValueError:
        result["type"] = "string"
        if all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", cell) for cell in present):
            try:
                for cell in present:
                    date.fromisoformat(cell)
            except ValueError:
                return result
            result["type"] = "date"
        return result
    if not all(math.isfinite(value) for value in numbers):
        raise ValueError(f"column {name!r} contains a non-finite numeric value")
    result["type"] = (
        "integer" if all(re.fullmatch(r"[+-]?\d+", cell.strip()) for cell in present)
        else "number"
    )
    mean = statistics.mean(numbers)
    deviation = statistics.stdev(numbers) if len(numbers) > 1 else None
    result["statistics"] = {
        "count": len(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": mean,
        "median": statistics.median(numbers),
        "sample_stddev": deviation,
        "outliers_3sd": (
            sum(abs(value - mean) > 3 * deviation for value in numbers)
            if deviation is not None else None
        ),
    }
    return result


def profile(path, delimiter=",", encoding="utf-8-sig", max_rows=None):
    path = Path(path)
    if delimiter not in (",", "\t", ";", "|"):
        raise ValueError("delimiter must be comma, tab, semicolon, or pipe")
    if max_rows is not None and max_rows < 1:
        raise ValueError("max_rows must be positive")
    if max_rows is None and path.stat().st_size > LARGE_FILE_BYTES:
        max_rows = SAMPLE_ROWS
    rows = []
    sampled = False
    with path.open(encoding=encoding, newline="") as source:
        reader = csv.reader(source, delimiter=delimiter, strict=True)
        header = next(reader, None)
        if not header or any(not name.strip() for name in header):
            raise ValueError("a nonempty header with named columns is required")
        if len(set(header)) != len(header):
            raise ValueError("header column names must be unique")
        for record, row in enumerate(reader, 1):
            if max_rows is not None and len(rows) == max_rows:
                sampled = True
                break
            if len(row) != len(header):
                raise ValueError(
                    f"data record {record} (ending at line {reader.line_num}) "
                    f"has {len(row)} cells; expected {len(header)}"
                )
            rows.append(row)
    columns = [
        summarize_column(name, [row[index] for row in rows])
        for index, name in enumerate(header)
    ]
    missing = sum(column["missing"] for column in columns)
    cells = len(rows) * len(header)
    return {
        "file": path.name,
        "delimiter": delimiter,
        "encoding": encoding,
        "sampled": sampled,
        "rows_analyzed": len(rows),
        "total_rows": None if sampled else len(rows),
        "column_count": len(header),
        "missing_cells": missing,
        "completeness_percent": 100 * (cells - missing) / cells if cells else None,
        "duplicate_rows": len(rows) - len({tuple(row) for row in rows}),
        "columns": columns,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--delimiter", choices=(",", "\t", ";", "|"), default=",")
    parser.add_argument("--encoding", default="utf-8-sig")
    args = parser.parse_args(argv)
    try:
        report = profile(args.input, args.delimiter, args.encoding)
        output = json.dumps(report, indent=2, allow_nan=False)
    except (OSError, UnicodeError, LookupError, csv.Error, ValueError, OverflowError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
