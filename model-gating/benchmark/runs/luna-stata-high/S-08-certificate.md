# ReproCrowd computational reproduction check

**Outcome:** computational issues (partial check). **Robustness:** not checked. This report assesses computation only; it does not judge the scientific conclusion.

## Scope and method

The shipped package uses Stata, which is not installed in this environment. The ReproCrowd rule pack requires a direct R or Python translation. I translated and ran only the linked-record counts needed to check two sample-size statements and the Table 2 sample count. The counts come from the package's anonymized `Linked_GRO_and_Census_5yr.dta`; the original data and code were not copied into this bundle.

The translation uses `readstata13` 0.11.0 to read the shipped data, tabulates `period`, then applies the shipped exclusion of `GRO_master == "DUNMOW"` for the Table 2 analytic sample. These are direct equivalents of the data-read, tabulation, and exclusion operations. The exact executed code and console output are in `code/linked_sample_counts.R` and `logs/linked_sample_counts.log`.

## Checked results

| Claim | Printed result | Recomputed | Status |
|---|---:|---:|---|
| C1: linked sample, 1851–1855 | 150,792 | 150,792 | match |
| C1: linked sample, 1861–1865 | 126,509 | 126,509 | match |
| C2: Table 2 analytic sample | 277,057 | 277,057 | match |

All three values recur exactly, using translated code.

## Limits

This does **not** complete the requested paper-wide check. The full Stata preparation, regression, permutation, figure, and appendix pipeline was not translated or run. Consequently, all other data-derived numbers in the abstract, main text, and tables—including the Table 1 descriptive statistics and the estimates, standard errors, fit statistics, and permutation p-values in Tables 2–5—remain unchecked. They are not represented here as non-reproductions. The package does contain the anonymized linked dataset used for these sample counts; some upstream confidential inputs for link construction are not distributed, and the master Stata driver leaves that linking step commented out.

## Provenance and environment

- Paper: [doi:10.1257/app.20190131](https://doi.org/10.1257/app.20190131)
- Code and data: AEA Data and Code Repository package supplied by the user; local package used: `/tmp/scratch_bench_luna/packages/pkg-983292`
- Engine: Codex · GPT-6 · OpenAI
- ReproCrowd rules: crowd-repro v1.1.0
- Date: 2026-11-01
- Environment: macOS Tahoe 26.7, R 4.6.1, `readstata13` 0.11.0; full installed package inventory is recorded in `R-package-freeze.txt`, and `sessionInfo.txt` records the loaded environment.
- FORRT chain outcome: `outcome_computational = computational issues`; `outcome_robustness = not checked`.
