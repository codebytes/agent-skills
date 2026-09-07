# CSV Analysis Report: `sample.csv`

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
| Std Dev   | 7.78    | 24,851.78   |

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

1. **Small, clean dataset** — 10 employee records with only 2 missing values across all columns (98% completeness).

2. **Engineering is the largest department** — 4 of 10 employees (40%), with Marketing and Sales evenly split at 3 each.

3. **Wide salary range** — Salaries span from $61,000 to $135,000 (a 2.2× difference), with a standard deviation of ~$24,852, indicating moderate dispersion.

4. **Age distribution skews younger** — The median age is 34 with a range of 26–50. Most employees are in their late 20s to mid-30s.

5. **Tenure varies significantly** — Start dates range from Aug 2017 to Feb 2023 (~5.5 years), suggesting a mix of long-tenured and recently hired staff.
