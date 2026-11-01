# Reproduction Study: Reshaping Global Trade

**Outcome: computational issues.** This is an incomplete benchmark check, not a certification that the paper reproduces. The translated Table I calculations recover the reported port summaries and most country summaries. Four country bank summary values differ. The full data preparation, table, and figure pipeline was not translated or run, and the remaining data-derived values in the article were not checked. The computation is therefore not established as reproducible or executable end to end.

## Record

- DOI: [10.1093/qje/qjac016](https://doi.org/10.1093/qje/qjac016)
- Source package: `/tmp/scratch_bench_luna/packages/pkg-6165a5/qje_replication2 edited` (local source; not uploaded)
- Reproduction standard: ReproCrowd `crowd-repro v1.1.0`
- Procedure: ReproCrowd benchmark prompt `0.1.2`
- Engine: Codex; model/provider: GPT-6 (OpenAI)
- Date: 2026-11-01
- Environment: macOS, R 4.6.1, haven 2.5.5. See [sessionInfo.txt](sessionInfo.txt).
- FLoRA outcome vocabulary: `outcome_computational = computational issues`; `outcome_robustness = not checked`.

## Scope and method

The Stata master file calls `xu_make_data.do`, `xu_tables.do`, and `xu_figures.do`. These files total 4,118 lines. Stata was not available. I translated the Table I selection, renaming, distance scaling, summary statistics, and sample count into [table1_translation.R](code/table1_translation.R), and ran it against the package-distributed `sr_ports_final.dta` and `lr_trade_final.dta`. The run log is [table1_translation.log](logs/table1_translation.log).

This is only a partial translation. It reads final datasets and does not execute the upstream data preparation, which itself creates those datasets and additional intermediate data. It does not run the article's regressions or figures. The certificate JSON therefore records Table I results only; it does not enumerate all data-derived numerical results in the article. Values not checked here must not be read as matches.

## Results checked

Table I port statistics match at the printed two-decimal precision. Country summaries match except for the British-bank and non-British-bank rows:

| Quantity | Printed country mean (SD) | Recomputed country mean (SD) | Result |
|---|---:|---:|---|
| British banks | 13.45 (13.82) | 13.27 (13.65) | Discrepant |
| Non-British banks | 1.26 (3.25) | 1.28 (3.28) | Discrepant |

The country sample size of 55 and port sample size of 289 recur. Full claim-level and printed-number results are in `certificate.json`.

## Findings and cause

- **P1:** Full-pipeline execution and comprehensive claim checking remain unverified because only Table I was translated and run. The partial translation uses package-distributed final datasets, so it bypasses all preparation commands and cannot establish that the shipped pipeline executes.
- **P2:** Four country bank summary statistics differ. Because the preparation pipeline was not run, the cause cannot be isolated; this is not attributed to rounding or a reporting slip.

The appropriate next step is a full command-by-command R translation and run of all three shipped scripts, followed by checks of every printed data-derived number. No missing analysis was authored to force a match. No source code or data were uploaded.

## ReproCrowd / FORRT chain

This report uses the computational outcome vocabulary `computational issues`; robustness is `not checked`. The chain is: source article and package identified → partial direct translation executed → printed Table I results compared → differences recorded → incomplete coverage disclosed. No FLoRA entry was submitted.
