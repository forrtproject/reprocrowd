# ReproCrowd reproduction certificate

**Paper:** Yang Xiang, Kevin Dorst, and Samuel J. Gershman (2025), “On the Robustness and Provenance of the Gambler’s Fallacy,” [doi:10.1177/09567976251344570](https://doi.org/10.1177/09567976251344570).  
**Code and data:** [authors’ GitHub repository](https://github.com/yyyxiang/gamblers_fallacy); the provided local package copy was run from `/tmp/scratch_bench_luna/packages/T-06`. No original code or data is bundled.  
**Rules:** [ReproCrowd crowd-repro v1.1.0](https://forrtproject.github.io/reprocrowd/crowd-repro/RULEPACK-v1.1.0.md). **Engine:** Codex · **model:** GPT-6 · **provider:** OpenAI · **date:** 2026-10-31.  
**Environment:** R 4.6.1, macOS Tahoe 26.7, arm64. See `logs/sessionInfo.txt` and `logs/package-inventory.tsv` for package and session records.

## Outcome

**FLoRA outcome_computational: computational issues.** Both supplied analysis and plot scripts completed after justified setup fixes. Several checked values recurred at the paper’s printed precision; the Experiment 1a posterior effect did not. **FLoRA outcome_robustness: not checked.** This report concerns computational reproducibility only; it does not assess the scientific conclusion.

## Checked claims

| Claim | Reported | Recomputed | Status |
|---|---:|---:|---|
| Experiment 1a posterior median δ (95% interval) | −0.11 [−0.27, 0.05] | −0.2164 [−0.32790, −0.09971] | **discrepant** |
| Experiment 2a, 60% ground truth posterior median δ (95% interval) | −0.34 [−0.50, −0.18] | −0.3413 [−0.50103, −0.1764] | **match** |
| Experiment 3 posterior median δ (95% interval) | −0.33 [−0.50, −0.17] | −0.3302 [−0.4954, −0.1677] | **match** |
| Experiment 3 participants with P(repeat) < 40% | 7.33% | 7.33% | **match** |
| Experiment 1a Wilcoxon Z, p, r | −1.03, .304, .08 | Not printed by script | **not_checkable** |

The Experiment 1a posterior interval differs enough to change whether zero is included. The run does not establish why. The script assigns its Wilcoxon result and derived statistics but does not print them, so these numbers cannot be compared without adding output code. Full console evidence is in `logs/statistical-analysis.log`.

## Execution and fixes

The package supplied `Code/statistical_analysis.R`, `Code/plot_figures.R`, and `Code/helper.R`. Copies are under `code/`; only their relative CSV paths were changed to absolute paths into the supplied package data. The original package was left untouched. I installed the packages required by the scripts, including `nortest`, `brms`, `BayesFactor`, `patchwork`, and dependencies.

The first plotting run warned that `Hmisc` was missing, so bootstrap error bars were not computed. I installed `Hmisc` and reran the unchanged figure script. Both logs are retained. Generated PDFs were removed; the certificate bundle contains only benchmark-mode artifacts.

## FORRT chain fields

- `outcome_computational`: **computational issues**
- `outcome_robustness`: **not checked**
- `entry_type`: **reproduction**
- Certification placeholder: **RC-0000-000**
- Certificate schema: **1.1**
