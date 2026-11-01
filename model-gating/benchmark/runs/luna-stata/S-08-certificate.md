# ReproCrowd computational reproduction check

**Paper:** Vellore Arthi, Brian Beach, and W. Walker Hanlon, “Recessions, Mortality, and Migration Bias: Evidence from the Lancashire Cotton Famine” (2022), [doi:10.1257/app.20190131](https://doi.org/10.1257/app.20190131).  
**Outcome:** technical failure — the complete computation was not checked.  
**Standard:** crowd-repro v1.1.0. **Procedure:** [rule pack](https://forrtproject.github.io/reprocrowd/crowd-repro/RULEPACK-v1.1.0.md).  
**Engine:** Codex (GPT-6), OpenAI API. **Audit date:** 2026-11-01.

## What ran

Stata was unavailable. I translated and ran only the initial age-weight construction stage from `Gen_age_weights.do` in R. The script read the supplied Registrar mortality and linked GRO/census data, collapsed the Registrar deaths by the two analysis periods, computed age shares, classified linked deaths into the shipped age categories, and constructed the same period/category weights. It completed and wrote 28 weights (`logs/run-01.log`). This intermediate has no printed counterpart in the paper, so it verifies no article result.

Environment: Linux x86_64; R 4.6.1; haven 2.5.5, dplyr 1.1.4, tidyr 1.3.1. The full `sessionInfo()` is in `logs/sessionInfo.txt`.

## What did not run

The supplied master Stata script uses a `USERPATH` placeholder and sequences multiple intermediate datasets under `Data/_Temp`. Its linked records and source data are present, but producing the claimed outputs requires translating and executing the remaining preparation, regression, permutation, figure, and appendix scripts. That work was not completed here. Consequently, no reported value has a recomputed counterpart. All listed exhibits are `not_checkable`, not discrepancies; this is not evidence that their values fail to recur.

The article’s headline printed values include 24,418 excess deaths; 9.5% of cotton-district deaths; 10,191 excess deaths among those aged 55+; and an 18.8% increase for that age group (main text, pp. 247–248). Tables 1–5 contain numerous further numerical results. Since the complete claim-by-claim extraction and execution were not performed, this certificate does not meet the requested benchmark deliverable. The grouped claim inventory in `certificate.json` is a transparent record of that limitation, not a complete result-level claim list.

## Findings and next step

The only executed stage succeeded. The overall analysis remains unverified because the translation stopped before the output-producing scripts. A complete check requires translating the whole shipped pipeline command by command, running it, and recording a separate result for every reported number. This certificate makes no judgement about the scientific conclusion. Robustness was not checked.

Original code and data are referenced at `/tmp/scratch_bench_luna/packages/pkg-983292`; they have not been uploaded or copied into this bundle.
