# ReproCrowd reproduction check

**Outcome:** computationally reproducible, with justified fixes. This checks computation only; scientific robustness was not checked.

**Paper:** Laia Balcells, Valeria Palanza, and Elsa Voytas, “Do Transitional Justice Museums Persuade Visitors? Evidence from a Field Experiment” (2022), [doi:10.1086/714765](https://doi.org/10.1086/714765).

**Engine:** Codex · **Model:** GPT-6 · **Provider:** OpenAI · **Rules:** crowd-repro v1.1.0 · **Date:** 2026-10-31.

## Run

The shipped main-text R script and its supplied `all.Rdata` were run. The first attempt stopped because the declared dependency `sandwich` was absent. After installing version 3.1-3, the unchanged script stopped in Figure 2 plotting-label code: it assigned a label to rows 22:34 in a 24-row results table. The copy in `code/` corrects the range to 22:24. This changes plot labels only, and the full script then exited successfully. No analysis code, outcomes, model, data, or sample were changed.

`code/report_claim_values.R` sources the analysis and prints already-computed estimate objects; it performs no additional analysis. Logs include the initial failed attempt, dependency installation, failed unmodified run, successful run, and values. The original data are not bundled. The [code and data package at the specified Hugging Face snapshot](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/19/replication_package) is linked here.

## Claim results

| Claim | Reported | Recomputed | Status |
|---|---:|---:|---|
| C1 Government satisfaction coefficient | 0.15 | 0.1521649 | match |
| C2 Democracy satisfaction coefficient | 0.14 | 0.1364780 | match |
| C3 Past prevents progress coefficient | −0.32 | −0.3190497 | match |
| C4 Victim compensation coefficient | 0.19 | 0.1980145 | close: truncation to 2 decimals |
| C5 Public military apology coefficient | 0.18 | 0.1817317 | match |
| C6 Pardoning follow-up coefficient | 0.20 | 0.2047054 | match |
| C6 Pardoning follow-up p value | 0.16 | 0.1640234 | match |

C4 truncates to 0.19 at two decimals; conventional rounding gives 0.20. It is therefore `close` under the rule pack’s named-truncation allowance. The C6 values are from the 24-month follow-up.

## Environment

R 4.6.1 on macOS Tahoe 26.7 (arm64). Packages used: sandwich 3.1-3, plyr 1.8.9, lmtest 0.9-40, zoo 1.9-1, dplyr 1.2.1, gridExtra 2.3.1, RColorBrewer 1.1-3, ggplot2 4.0.3. Full `sessionInfo()` is in [environment.txt](environment.txt).

FLoRA chain vocabulary: **outcome_computational = computationally reproducible**; **outcome_robustness = not checked**. No robustness or scientific-validity judgement is made.
