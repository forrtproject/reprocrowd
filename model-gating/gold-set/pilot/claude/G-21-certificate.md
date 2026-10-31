# ReproCrowd certificate RC-2026-921

Engine: Claude Code (Claude Agent SDK subagent), Claude Opus 5.5 (`claude-opus-5-5`) via Anthropic · rules: crowd-repro v1.0.0 · procedure: ReproCrowd prompt 0.1.0 · audit date: 2026-10-30 · host: macOS 26.7 (arm64)

**Paper:** Oktar, K., Lombrozo, T., & Griffiths, T. L. (2024). Learning from aggregated opinion. *Psychological Science, 35*(9), 1010–1024. [doi:10.1177/09567976241251741](https://doi.org/10.1177/09567976241251741)
**Code and data:** [osf.io/dexuy](https://osf.io/dexuy/). They are linked, not redistributed. `notebooks/01_data_download.py` fetches them and checks each file's MD5.

## Summary

**Outcome (FLoRA `outcome_computational`): computational issues.** `outcome_robustness`: not checked.

All three main analysis scripts (E1, E2, E3) ran to completion. E1 needed two fixes for `data.table` version drift before it would run; neither changes a number. Of 40 checked quantities across 20 claims, **31 matched**, **8 were discrepant** and **1 was not checkable**. This certificate covers only whether the computation reproduces. It makes no judgement on whether the paper's conclusions are correct.

What reproduced exactly:
- **Experiment 1:** all correlations and tests: r = .92, −.08 and .79; differences 4.51 and 1.35; paired t(132) = 13.68 and 4.19.
- **Experiment 2:** the r = .99, .97 and .96 correlations, and the AIC ranking (Bayes is the best single model; ensembles beat it; B+C beats B+U).
- **Experiment 3:** the sample of 235, the Figure 8a AIC ordering, the prior-heuristic AIC of 922, the mixed-model AICs of 410, 497 and 507, and the 43% and 48% Bayes shares.

What did not reproduce:
- **E1 sample size:** the paper says 133 recruited and 17 excluded. The data have 150 rows; the script excludes 17 and analyses 133, which agrees with the reported df of 132. The abstract's N = 886 equals 133 + 458 + 295: analysed counts for E1 and E2 but the recruited count for E3.
- **E2 sample size:** the paper says 458 recruited and 108 excluded, although its own 33 + 72 = 105. The data have 563 rows; the script excludes 105 and analyses 458.
- **E2 "one quarter":** the paper says UPCO and Competence best fit one quarter of participants. The shipped code gives 30.8% by correlation and 38.2% by deviation.
- **E3 proportion-heuristic AIC:** the shipped `lmer` gives 1766.3 against a reported ≈1722 (a gap of +44). The formula `post_j ~ (t / (t + f))` is parsed by R as nesting, not as a proportion. Refitting with `I(t / (t + f))` gives 1721.98, which matches. The cause is therefore a difference in the analysis code, not version drift: the shipped formula did not produce the reported value.

Not checkable: the E1 shares of participants best fit by Bayes (≈75% by correlation, ≈80% by deviation). E1_analysis.R contains no code that computes them.

## Method

1. Downloaded the shipped data and scripts from OSF into `extracted/` (MD5-verified, left untouched).
2. Made working copies in `working/` with these lossless edits only (`working/edits.json`):
   - commented out three `setwd()` calls and one `install.packages()` call;
   - in E1, a post-`melt` block that restores the output of `data.table` versions before 1.15.
   
   `notebooks/driver.R` adds a `melt.data.frame` shim that calls `reshape2`, which reproduces the redirect older `data.table` versions performed. No line that computes a number was changed.
3. Ran each script with `source(echo = TRUE)` through `notebooks/driver.R`. The driver then saved the reported quantities to JSON. Some quantities are assigned but never printed by the shipped code (E1 `c1`–`c3`; E2 correlations, `AICs`, `devps` and `corps`; E3 AIC tables); the driver reads them from the same R session.
4. Two quantities needed computation beyond the shipped code, both with the script's own objects:
   - the E2 Figure 4a correlations: `cor.test` on `m_sk`;
   - the E3 mixed-model AICs: `lmer` with random intercepts for Subject and item, as the script's comment instructs.
5. A diagnostic refit of the E3 proportion heuristic using `I(t / (t + f))` was run to judge the cause of the gap in DEF-004. It is not a robustness analysis.
6. `notebooks/04_figures.py` checks that the figure PDFs exist and builds `outputs/claims_comparison.{json,csv}`.

Reported values were transcribed from the published PDF hosted by the authors' lab. Its DOI 10.1177/09567976241251741 resolves via Crossref.

## Environment

- **Certified run:** host R 4.6.1 (2026-06-24) with a task-local CRAN library. Key versions: data.table 1.18.6.1, lme4 2.1-0, MuMIn 1.48.19, psych 2.6.9, qualtRics 3.3.0, gmp 0.7-5.1, reshape2 1.4.5. The full inventory is in `environment.json` and `outputs/E*/E*_sessionInfo.txt` / `E*_packages.csv`.
- **Pinned environment:** `pixi.toml` and `pixi.lock` (pixi 0.83.0; conda-forge r-base 4.5.3, bioconda snakemake-minimal 9.x). It was solved and installed on osx-arm64, and `snakemake -n` validates the DAG.
- **Not done:** the full pipeline was not re-executed under pixi in this pilot. qualtRics is not on conda-forge, so step 1 installs it from the CRAN tarball when `REPRO_INSTALL_QUALTRICS=1` is set.
- **Version drift:** R 4.6.1 (run) vs 4.5.3 (lock). The authors' versions are undocumented. `data.table` has changed `melt` semantics since the code was written.

Re-run: `REPRO_INSTALL_QUALTRICS=1 pixi run snakemake --cores 1`

## Findings

| ID | Sev. | Type | Finding |
|---|---|---|---|
| NORM-001 | P3 | normalization | `setwd()` to author paths commented out |
| NORM-002 | P3 | normalization | mid-script `install.packages("PairedData")` commented out |
| NORM-003 | P0 (resolved) | normalization | E1 halts as shipped under data.table ≥ 1.15 (`melt` naming); restored the old output |
| NORM-004 | P2 | normalization | E1 `melt()` on a data.frame needs the reshape2 redirect; shim added |
| DEF-001 | P2 | defect | E1 recruited/analysed N misreported (150/133 vs "133 recruited") |
| DEF-002 | P2 | defect | E2 N misreported (563/458 vs "458 recruited, 108 excluded"; 33 + 72 = 105) |
| DEF-003 | P2 | defect | E2 "one quarter" not reproduced (30.8% / 38.2%) |
| DEF-004 | P2 | defect | E3 proportion-heuristic AIC 1766 vs 1722; `I(t/(t+f))` gives 1721.98 |
| DEF-005 | P2 | defect | E3 reported mixed-model AICs come from code described only in a comment |
| DEF-006 | P2 | defect | No code for the E1 participant-level shares |
| DEF-007 | P3 | defect | E2 Fig. 6b labels for UPCO and Competence swapped in the plotting data |
| DEF-008 | P3 | defect | paired.r gives z, reported as t |
| DEF-009 | P3 | defect | Manual exclusions by hard-coded row index |
| DEF-010 | P3 | defect | No versions or lockfile shipped; unseeded plot jitter |

Each finding's evidence and suggested fix are in `certificate.json`.

## Limitations

- **Pilot status:** this is a pilot. The bundle is unpublished, no nanopublications were minted and there is no Zenodo DOI. `github_url` points to the ReproCrowd project repository.
- **Broken URLs:** the rule-pack and schema URLs given in the prompt (`https://lukasroeseler.github.io/reprocrowd/...`) returned **404**. The live copies at `https://forrtproject.github.io/reprocrowd/...` were used instead. The schema `$id`s still point to the broken host.
- **Out of scope:** the pilot studies, the E3 pilot script and the Supplemental Material values were not checked.
- **Quote checking:** quotes were checked against `pdftotext` output; no `verify_quote` tool was available.
- **Console logs not published:** `outputs/E*/E*_console.log` stay local as evidence and are excluded from publication via `.gitignore`. They echo the shipped source code and participants' free-text responses, which this bundle must not redistribute. All derived outputs (results JSON, plots, package lists, sessionInfo) are included.
