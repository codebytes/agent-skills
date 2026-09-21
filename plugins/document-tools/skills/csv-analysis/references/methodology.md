# CSV profiling methodology

Read this reference when interpreting the profiler's JSON or explaining
calculation and sampling caveats. It is not required merely to launch the script.

## Parsing and scope

- The delimiter is explicit; comma is the CLI default. Tab, semicolon, and pipe
  are supported with `--delimiter`. The script does not guess a dialect.
- UTF-8 with an optional BOM is the default. `--encoding` must come from the user
  if UTF-8 fails; there is no permissive fallback.
- A nonempty, unique header is required. Blank records, inconsistent row widths,
  and malformed quoting are errors, not records to silently skip.
- Files up to 100 MiB are read in full. Larger files use the first 10,000 data
  records, with a one-record lookahead to determine whether data remains.
  Sampling is a prefix, not a random or representative sample.
- `rows_analyzed` is always measured. `total_rows` is null when `sampled` is true.
  Duplicate and missing counts then describe only the analyzed prefix. No claim
  is made about the unread records, including their parseability.

## Missing values and duplicates

Missing values are empty/whitespace-only cells or the exact case-sensitive
markers `NA`, `N/A`, and `null` after trimming surrounding whitespace. Other
spellings are not automatically missing. No input cells are rewritten.

Completeness is `100 * non_missing_cells / data_cells`, excluding the header.
For a header-only file, completeness is null, not 100%.
Duplicate rows compare the original cell strings; unique counts exclude missing
values but otherwise preserve spelling and whitespace.

## Types and statistics

Types are inferred, not a schema guarantee. All non-missing values must agree:
booleans (`true`/`false`), finite numeric values, ISO `YYYY-MM-DD` dates, or strings.
All-missing columns have type `unknown`. Mixed numeric/text columns are strings;
the script never drops their text values to manufacture numeric statistics.

Numeric summaries include count, min, max, mean, median, sample standard
deviation (`statistics.stdev`, denominator `n - 1`), and the count more than
three sample standard deviations from the mean. Standard deviation and the
outlier count are null for fewer than two numeric values. Non-finite numbers
or unrepresentable calculations are errors, not valid JSON results.

Numeric-looking identifiers can be misclassified. Review the column's meaning
before interpreting arithmetic. A three-standard-deviation screen is not proof
that a value is wrong, nor that the dataset is clean.

## Reporting boundaries

The compact output includes aggregate counts and statistics, not row contents.
If the user needs category distributions, affected records, or formatting
examples, inspect only the relevant columns/records with local tools and label
any extra measurements. Do not claim the profiler measured something it omits.

Separate facts from interpretation. Do not infer currency, a younger/older
population, or employee tenure without metadata or an explicit as-of date.
Report errors and sampling before giving conclusions.
