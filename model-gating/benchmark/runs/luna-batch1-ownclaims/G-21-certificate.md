# ReproCrowd computational reproduction certificate

**Paper:** Oktar, Kerem; Lombrozo, Tania; and Griffiths, Thomas L. (2024), “Learning From Aggregated Opinion,” *Psychological Science*, 35(9), 1010–1024. [Article DOI](https://doi.org/10.1177/09567976241251741) · [OSF project and materials](https://osf.io/dexuy/)

**Outcome:** `computational issues` · **Outcome robustness:** `not checked`

**Repro standard:** crowd-repro v1.1.0 · **Prompt/procedure:** ReproCrowd benchmark prompt 0.1.2 · **Engine:** Codex · **Model/provider:** GPT-6 / OpenAI · **Date:** 2026-10-31 · **Certification ID:** RC-0000-000

## Summary

The supplied analyses are **partly executable**, but the complete computation is not reproducible. The Experiment 2 and Experiment 3 scripts completed with the OSF data and justified path/package adjustments. Experiment 1 stopped before its reported model correlations and tests. The Experiment 2 script does not compute the Pearson correlations printed in Figure 4. Experiment 3 reproduced the model ordering and participant-level percentages, while several printed AIC values differed substantially. Two pilot scripts also stopped with errors; the second pilot script completed.

This is a computational check only. It makes no claim about whether the scientific conclusions are correct and does not assess robustness.

## Claims and results

| Claim | Reported result | Recomputed from shipped code | Status |
|---|---|---|---|
| C1 · Experiment 1 correlations and tests (pp. 1014–1015) | Bayes r=.92; UPCO r=-.08; Competence r=.79; t=4.51 and t=1.35 | Not computed. After justified repairs, the script stopped because the vectors passed to `cor.test` had different lengths. | `not_checkable` |
| C2 · Experiment 2 correlations (Fig. 4) | Bayes r=.99; UPCO r=.97; Competence r=.96 | The shipped script does not calculate these Pearson correlations. I did not add the missing analysis. | `not_checkable` |
| C3 · Experiment 2 model comparisons (Fig. 6) | Ensembles outperform individual models; adding Competence gives a larger improvement than adding UPCO. | AICs for Bayes, Competence, UPCO, C+U, B+U, B+C, and B+U+C: -890.393, -569.659, -633.520, -659.979, -1039.405, -1139.647, -1149.107. The all-model ensemble ranks first; the qualitative comparison recurs. | `match` |
| C4 · Experiment 3 model AICs (Fig. 8) | Bayes≈410; UPCO≈497; Competence≈507; Bayes best individual model; an ensemble is best overall. | Bayes=463.148; UPCO=569.755; Competence=785.130; Bayes+C=322.711 is best overall. Individual AIC gaps are +53.148, +72.755, and +278.130. The ordering recurs, but the printed values do not. | `discrepant` |
| C5 · Experiment 3 heuristic AICs (p. 1021) | Proportion≈1722; prior≈922. | Proportion=1766.298; prior=922.169. Prior rounds to the reported value; proportion differs by +44.298. | `discrepant` |
| C6 · Experiment 3 participant-level model rates (p. 1021; Fig. 8b) | Bayes captures 43% by correlation and 48% by deviation. | 42.553% by correlation and 48.085% by deviation; both round to the reported whole percentages. | `match` |

A `match` here refers only to the reported computational quantity and precision. It does not validate any scientific conclusion.

## Execution and justified changes

All six OSF analysis scripts were attempted. The two experiment scripts that completed were E2_analysis.R and E3_analysis.R. Pilot 2 also completed. E1_analysis.R stopped after its first repair at `cor.test.default(ofq, bfq)` because the vectors differed in length. Pilot 1 stopped in `boot.ci()` with “missing value where TRUE/FALSE needed.” E3pilot_analysis.R stopped with “No random effects terms specified in formula.” Full console output for each run, including the initial and subsequent attempts, is in `logs/`.

Justified changes were limited to replacing the scripts’ placeholder or machine-specific `setwd()` paths with the local OSF data directory, installing packages required by the shipped `library()` calls, installing Hmisc to render existing `stat_summary()` layers, and adding a one-line `belief`→`value` alias in the E1 and Pilot 1 working copies. That alias preserves the measured response column before the shipped code reuses `belief` for item labels. No model, exclusion, sample, or data changes were made. The resulting working copies are in `code/`.

The six original analysis-script SHA-256 values matched the identifiers supplied with the request. Original source code and data remain linked through [OSF](https://osf.io/dexuy/) and were not included as raw data in this bundle. CSVs used for execution were kept outside this certification directory.

## Original OSF files

The following links point to the source files. Original script hashes were verified against the identifiers provided for this check; the CSV data remain outside this bundle. Their hashes are recorded in `certificate.json` under `provenance.analysis_script`.

| Analysis script | OSF | Data used | OSF |
|---|---|---|---|
| `E1_analysis.R` | [OSF file](https://osf.io/download/dcrfb/) | `e1_data.csv` | [OSF file](https://osf.io/download/tcf9w/) |
| `E2_analysis.R` | [OSF file](https://osf.io/download/uaje8/) | `e2_data.csv` | [OSF file](https://osf.io/download/hfnqz/) |
| `E3_analysis.R` | [OSF file](https://osf.io/download/gx82e/) | `e3_data.csv` | [OSF file](https://osf.io/download/p63cj/) |
| `E3pilot_analysis.R` | [OSF file](https://osf.io/download/w4tfx/) | `pilot3_data.csv` | [OSF file](https://osf.io/download/kjdqu/) |
| `pilot1_analysis.R` | [OSF file](https://osf.io/download/pz34y/) | `pilot1_data.csv` | [OSF file](https://osf.io/download/nm3xp/) |
| `pilot2_analysis.R` | [OSF file](https://osf.io/download/sev9t/) | `pilot2_data.csv` | [OSF file](https://osf.io/download/k62fw/) |

## Findings

- **P1 · EXEC-001:** Experiment 1 does not reach the reported correlations or tests. The script needs to align its vectors over the same 18 stimuli before rerunning.
- **P1 · AIC-001:** Experiment 3’s printed individual-model AICs and proportion-heuristic AIC do not recur. The model ordering does recur. The manuscript and script analysis/filtering should be reconciled.
- **P2 · EMIT-001:** The Experiment 2 script does not compute the correlations printed in Figure 4.
- **P2 · PILOT-001 / PILOT-002:** Pilot 1 and the Experiment 3 pilot script terminate with errors.
- **P3 · PATH-001:** The original scripts rely on placeholder or machine-specific working directories.

## Environment

- **Host:** macOS Tahoe 26.7, arm64 (Darwin 23)
- **R:** 4.6.1; the session record and package inventory are [sessionInfo.txt](sessionInfo.txt) and [packages.csv](packages.csv).
- **Python:** 3.14.6; package inventory in [python-packages.txt](python-packages.txt). Python was used for OSF retrieval, checksums, and schema validation.
- **Main R packages:** qualtRics 3.3.0, data.table 1.18.4, ggplot2 4.0.3, lme4 2.1-0, MuMIn 1.48.19, sjPlot 2.9.0, metR 0.19.0, Hmisc 5.3-0, and the remaining package versions listed in the session record.

## FORRT chain vocabulary

`outcome_computational`: **computational issues** · `outcome_robustness`: **not checked**. This certificate reports computational reproduction only.
