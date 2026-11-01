# ReproCrowd certificate

**Outcome: technical failure.** This is not a completed reproduction study: no numerical result from the paper was recomputed or checked. The result inventory is therefore empty. The report does not assess whether the scientific conclusions are correct.

**Paper:** Luigi Butera, Robert Metcalfe, William Morrison, and Dmitry Taubinsky, “Measuring the Welfare Effects of Shame and Pride,” *American Economic Review* 112(1), 2022. DOI: [10.1257/aer.20190433](https://doi.org/10.1257/aer.20190433).

**Engine:** Codex · **Model:** GPT-6 · **Provider:** OpenAI · **Rules:** crowd-repro v1.1.0 · **Procedure:** ReproCrowd prompt 0.1.2 · **Audit date:** 2026-11-01.

## Execution and limitation

The package README describes a Stata 15 master script that runs three build scripts followed by eight analysis scripts. The raw data and the full Stata sources were present at the supplied local package path. Stata was not installed (`stata` and `stata-se` were not found). R 4.6.1 and common analysis packages were available, but the complete command-by-command translation of all data preparation and analysis scripts was not completed. Consequently, this report does not claim that the computation was reproduced or that any reported result failed to recur. This is an incomplete benchmark attempt, not a result-level audit.

Only an environment check ran. Its console output is in [logs/environment_check.log](logs/environment_check.log); the R session record is [sessionInfo.txt](sessionInfo.txt). The executed code is [environment_check.R](code/environment_check.R). No original code or data was copied into this bundle or uploaded.

## FORRT chain outcome

- `outcome_computational`: `technical failure`
- `outcome_robustness`: `not checked`

The required next step is a full direct R translation of the shipped Stata pipeline, followed by checking every data-derived number in the article’s abstract, main text, and tables. No scientific-validity judgment is made here.
