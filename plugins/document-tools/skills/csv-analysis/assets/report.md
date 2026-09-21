# CSV analysis report: {input filename}

## Scope

State delimiter, encoding, rows analyzed, column count, and whether the scan was
complete or sampled. If sampled, do not turn rows analyzed into a total row count.

## Schema and statistics

Show inferred type, non-missing count, missing count, and non-missing unique count
per column. For numeric columns include count, min, max, mean, median, and
**sample** standard deviation. Display null statistics as "not applicable".

## Data quality

Report missing cells, completeness, duplicate rows, and the numeric outlier
screen with their scope. Distinguish measured issues from follow-up checks.

## Key findings

Give three to five concise, evidence-backed findings when the data supports them.
Separate interpretation from measured facts; do not invent insights to fill
the list. Include missing-value, sampling, and calculation caveats.
