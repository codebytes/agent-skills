---
name: csv-analysis
description: Analyze CSV files and generate comprehensive statistical reports with data profiling and quality checks
tools:
  - powershell
  - view
  - create
---

## Instructions

When asked to analyze a CSV file, follow this workflow:

### Step 1: Read and Profile
- Use the `view` tool to read the first 50 lines of the CSV
- Identify the delimiter (comma, tab, semicolon, pipe)
- Count total rows and columns
- Infer column data types (string, integer, float, date, boolean)

### Step 2: Compute Statistics
Run a Python script to compute per-column statistics:

```python
import csv
import statistics
from collections import Counter

# Read and analyze the CSV
# Compute: count, nulls, unique values, min, max, mean, median, std dev
```

### Step 3: Quality Assessment
Check for:
- Missing or null values (empty strings, "NA", "null", "N/A")
- Duplicate rows
- Inconsistent formatting (mixed date formats, case inconsistency)
- Potential outliers (values beyond 3 standard deviations)

### Step 4: Generate Report
Create a markdown report with:
- **Overview**: File name, row count, column count
- **Schema table**: Column name, type, non-null count, unique count
- **Statistics table**: Min, max, mean, median, std dev for numeric columns
- **Quality issues**: List of findings with severity (info/warning/error)
- **Key findings**: Top 3-5 insights from the data

## Output Format

The report should be a well-formatted markdown document suitable for inclusion in project documentation. Use tables for structured data and bullet points for findings.

## Error Handling

- If the file is not valid CSV, report the issue and suggest the correct format
- If the file is too large (>100MB), sample the first 10,000 rows and note the sampling
- If encoding errors occur, try UTF-8, Latin-1, and CP1252 in order
