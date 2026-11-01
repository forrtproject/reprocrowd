# ReproCrowd computational check

**Outcome:** computational issues (partial check only)  
**ReproCrowd rules:** crowd-repro v1.1.0  
**Procedure:** ReproCrowd benchmark prompt 0.1.2  
**Engine:** Codex · **model/provider:** GPT-6 / OpenAI  
**Date:** 2026-11-01  
**Paper:** Henry, Zhuravskaya & Guriev (2022), “Checking and Sharing Alt-Facts,” DOI [10.1257/pol.20210037](https://doi.org/10.1257/pol.20210037)

## Results obtained

Stata was not installed. The R script in `code/partial_translation.R` directly translates the shipped import/filter/count/mean segment for the three main-experiment survey CSVs. It reproduces the abstract’s treatment-group sharing-intention rates at the printed precision: 14.7%, 10.2%, and 10.8%. The retained sample is 2,533 (844, 845, and 844 by survey), four below the article’s reported 2,537. The run output is in `logs/partial_translation.log`; `sessionInfo.txt` records the environment.

## Scope limitation

This is **not the requested complete reproduction study**. The remaining shipped pipeline in `dofiles/1.infile_data.do`, `2.analysis_final_paper.do`, and `3.numbers_in_text.do` was not translated or executed. That includes the Google Analytics and Facebook merges, derived outcomes, adaptive LASSO, regressions, tables, and figures. The abstract and selected headline values that depend on those steps are listed as not checkable in `certificate.json`; the full article’s numeric result inventory (including Tables 1–3 and appendices) has not been enumerated. The code directory contains only the partial translation and certificate-generation script, not a full translation.

The package code and data were not copied or uploaded. The provided local package is `/tmp/scratch_bench_luna/packages/pkg-9c83b5`. No scientific conclusion is assessed. FORRT chain outcome: `outcome_computational = computational issues`; `outcome_robustness = not checked`.
