# CSV Analysis Report: `sample.csv`

This is the checked reference report for the complete synthetic fixture, not a
claim that a live model run succeeded. Empty cells are missing; the header is
excluded from completeness. Category and date summaries below are additional
full-file measurements, beyond the profiler's compact JSON output.

## Overview

| Property    | Value        |
|-------------|--------------|
| **File**    | sample.csv   |
| **Rows**    | 10           |
| **Columns** | 5            |
| **Delimiter** | Comma (`,`) |
| **Encoding** | UTF-8       |
| **Duplicate Rows** | 0    |

---

## Schema

| Column       | Type    | Non-Null | Nulls | Unique |
|--------------|---------|----------|-------|--------|
| name         | string  | 10       | 0     | 10     |
| age          | integer | 10       | 0     | 10     |
| salary       | integer | 9        | 1     | 9      |
| department   | string  | 10       | 0     | 3      |
| start_date   | date    | 9        | 1     | 9      |

---

## Numeric Column Statistics

| Statistic | age     | salary      |
|-----------|---------|-------------|
| Min       | 26      | 61,000      |
| Max       | 50      | 135,000     |
| Mean      | 35.70   | 93,111.11   |
| Median    | 34.00   | 92,000.00   |
| Sample Std Dev | 7.78 | 24,851.78 |

Statistics exclude missing values. Sample standard deviation uses `n - 1`:
10 observations for age and 9 for salary.

---

## Categorical Column Distributions

### department
| Value       | Count | Percentage |
|-------------|-------|------------|
| Engineering | 4     | 40%        |
| Marketing   | 3     | 30%        |
| Sales       | 3     | 30%        |

### name
All 10 values are unique (one per row).

---

## Date Column Summary

### start_date
| Property   | Value        |
|------------|--------------|
| Earliest   | 2017-08-30   |
| Latest     | 2023-02-28   |
| Span       | ~5.5 years   |

---

## Quality Issues

| Severity  | Column      | Issue                                           |
|-----------|-------------|-------------------------------------------------|
| ⚠ Warning | salary      | 1 missing value (row: Iris)                     |
| ⚠ Warning | start_date  | 1 missing value (row: Hank)                     |
| ℹ Info     | —           | No duplicate rows detected                      |
| ℹ Info     | —           | No outliers detected (all values within 3 SD)   |
| ℹ Info     | —           | Date format is consistent (`YYYY-MM-DD`)        |

---

## Key Findings

1. **Small dataset with two missing values** — 10 employee records have 48 populated cells out of 50 (96% completeness).

2. **Engineering is the largest department** — 4 of 10 employees (40%), with Marketing and Sales evenly split at 3 each.

3. **Salary values span 61,000–135,000** — Across 9 observations, the mean is 93,111.11 and sample standard deviation is 24,851.78. The fixture does not specify a currency.

4. **Median age is 34** — The 10 ages range from 26 to 50, with a mean of 35.70. No comparison population is supplied, so this does not establish a younger or older workforce.

5. **Start dates span about 5.5 years** — The 9 recorded dates range from 2017-08-30 to 2023-02-28. This is the span between start dates, not employee tenure; no as-of date is supplied.
