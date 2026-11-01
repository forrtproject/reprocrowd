# ReproCrowd reproduction check

**Paper:** Kevin Grier, Robin Grier, and Gor Mkrtchian (2023), [“Campaign Contributions and Roll-Call Voting in the U.S. House of Representatives: The Case of the Sugar Industry”](https://doi.org/10.1017/S0003055422000466).  
**Code and data:** [Harvard Dataverse dataset](https://doi.org/10.7910/DVN/2IFZR9); the local package supplied for this check was `/tmp/scratch_bench_luna/packages/pkg-4e0ab3`. The original files were not copied or uploaded.  
**Reproduction procedure:** ReproCrowd benchmark prompt 0.1.2.  
**Standard:** crowd-repro v1.1.0.  
**Engine:** Codex · rules: crowd-repro v1.1.0.  
**Model and provider:** GPT-6 · OpenAI.  
**Date and environment:** 2026-11-01; macOS Tahoe 26.7 (aarch64-apple-darwin23); R 4.6.1. See `logs/sessionInfo.txt` and the environment inventory in `certificate.json`.

## Outcome

**FLoRA outcome_computational: computational issues.** The translated pipeline executed in R. The shipped Stata code was not executed as shipped because Stata 15 is unavailable; all checked model and graph results therefore have basis `translated`. `outcome_robustness` is **not checked**. This report describes computational recurrence only and does not assess the scientific conclusion.

The six translated logit models reproduced the reported observation counts (186 and 106) and Table 1 pseudo-R² values (0.745 and 0.721) at printed precision. Some coefficients recur at printed precision. Other coefficients differ, most notably the agriculture-committee coefficient, and the recomputed p-values frequently do not match the values printed in Tables 1 and 3 under the rule pack’s 1% p-value tolerance. See the separate result entries in `certificate.json`.

Across 88 numeric results, 14 match, 37 are discrepant, and 37 are not checkable. There are no `close` results. Not-checkable values are descriptive or narrative statistics for which the supplied do-file contains no computation; no new analysis was written to generate them.

## Translation and run notes

The source do-file imports the three `.dta` files, creates `yesvote`, `repub`, and inflation-adjusted `rsugcont`, fits six logit models with `i.id` and robust standard errors, filters `both == 1` for the incumbent models, and draws three `marhis` figures. The R translation is `code/translated_pipeline.R`; its final console output is `logs/run_03.txt`.

The R translation uses `haven` to read Stata data, `glm(..., family = binomial("logit"))` with `factor(id)` for the fixed effects, and `sandwich::vcovHC(type = "HC1")` for robust covariance estimates. Stata’s logit drops fixed-effect groups that perfectly predict the outcome. To match its estimation sample, the translation first applies model complete-case omission and then retains only ids with within-id outcome variation. This yields 186 and 106 observations, respectively, without changing the estimable sample. `xtset` is metadata only, and `repub` is generated but unused in the shipped models.

The [Stata `marhis` package documentation](https://econpapers.repec.org/software/bocbocode/s458145.htm) specifies average adjusted predictions by default. The translation makes the three figures on a 51-point grid including both endpoints for `points(50)`, holds other covariates at their observed values, uses robust delta-method confidence intervals, and writes temporary figure files outside the certification bundle. The paper describes this grid as 50 equally spaced values. Because Stata itself was unavailable, the plotted values and confidence intervals were not independently verified against Stata’s margins engine. Approximate probability readings discussed in the paper are not treated as exact numerical outputs.

No specification, data, or estimand was changed to make a value recur. The initial execution attempts are retained as logs; `run_03.txt` is the final corrected run. The original package was read in place and not copied into this bundle.

## Findings

- **P1:** Some reported Table 1 and Table 3 model results did not recur under the direct R translation. The R run emitted warnings about fitted probabilities of 0/1 and near-singular HC1 covariance matrices. Without Stata, the source of the remaining differences cannot be isolated. Running the original do-file in Stata 15 would distinguish Stata behavior from translation or version effects.
- **P2:** The do-file does not calculate Table 2 or several descriptive and approximate predictive quantities in the text. Those entries are `not_checkable`; the missing calculations were not reconstructed.

## Files

- `certificate.json` contains the claims, one entry per printed numeric result, result status and basis, environment, and FLoRA outcome.
- `code/translated_pipeline.R` is the complete translated pipeline.
- `logs/` contains the execution logs and the R session record.
