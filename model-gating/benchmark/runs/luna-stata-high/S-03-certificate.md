# ReproCrowd certificate: Measuring the Welfare Effects of Shame and Pride

**Outcome:** computational issues. The complete shipped pipeline was executable after direct R translation and documented run-enabling fixes. Most reduced-form table values recur, while some structural estimates, tests, and welfare outputs differ at the printed precision. This report does not judge the scientific conclusion.

**Engine:** Codex · **Model/provider:** GPT-6 (exact serving variant not exposed) · OpenAI · **Rules:** crowd-repro v1.1.0 · **Procedure:** ReproCrowd prompt 0.1.2 · **Audit date:** 2026-11-01.

**Article:** [AER article](https://doi.org/10.1257/aer.20190433) · **Supplied package:** [/tmp/scratch_bench_luna/packages/pkg-6db66d](/tmp/scratch_bench_luna/packages/pkg-6db66d).

## Computation and result

The complete shipped Stata pipeline, including data preparation, was translated to R because Stata was unavailable. Tables 1-6 and 8 were computed from the translated datasets. Structural formulas and welfare calculations were also translated. The participant-cluster bootstrap used 1,000 resamples and seed 12345; valid replications were 999 for YMCA, 1,000 for Prolific and Berkeley, and 994 for BU because some draws had invalid structural roots. The R and Stata random-number generators differ, so bootstrap intervals can differ.

YMCA Tables 1-4 reproduce the printed means, balance p values, coefficients, standard errors, sample counts, and nearly all curvature values at printed precision. Table 5 coefficients, standard errors, sample counts, and Table 6 estimates recur. Table 8's six point estimates recur. Table 5 order-effect p values, some Table 7 estimates and intervals, and several Table 9 welfare outputs differ. The charity non-monotonic share in Prolific also differs at printed precision. Each checked number has its own result record in certificate.json.

## Execution-preserving changes

- Set the working package path to the supplied local package and matched `Raw Data` case; created `Prepped data`, `temp`, and `Analysis/Output` folders expected by the do-files.
- Removed the standalone `break` in Prolific_Build.do, which otherwise halts the pipeline after import.
- Corrected the apparent `switch`/`switch_preference` typo by incrementing the initialized variable.
- Aliased the raw CSV `survey_id` fields to the Stata merge key `survey` while retaining the original field.
- Preserved sample filters, outcomes, model specifications, clustering, and source script order. Charity sample labels and the overwritten BU QM221 relabel were kept as the source pipeline implements them.

## Re-running

Run from the workspace root with Rscript:

```sh
Rscript aer20190433-certification/code/translated_pipeline.R
Rscript aer20190433-certification/code/translated_ymca_analysis.R
Rscript aer20190433-certification/code/translated_charity_analysis.R
Rscript aer20190433-certification/code/translated_welfare_analysis.R
Rscript aer20190433-certification/code/translated_structural_bootstrap.R
Rscript aer20190433-certification/code/build_certificate.R
```

The original package and article remain at the supplied local paths. They are linked, not copied into this bundle. Full R session and package versions are in environment.txt; console logs are in logs/.

**FORRT chain outcome:** `outcome_computational = computational issues`; `outcome_robustness = not checked`. The certification id and GitHub URL use the benchmark placeholders specified in the prompt.

## Findings

- **P3 normalization:** supplied root path/folder-case mismatch and debugger break required documented run-enabling fixes.
- **P2 normalization:** the switch counter typo was corrected to the initialized/consumed variable.
- **P1 defect:** some structural estimates and scaling-up welfare outputs differ at printed precision under the R translation.

Detailed claim IDs and one result for each checked printed value are in certificate.json.
