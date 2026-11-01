# ReproCrowd reproduction certificate

**Outcome:** computational issues · **Rule pack:** crowd-repro v1.1.0 · **Engine:** Codex · GPT-6 · OpenAI  
**Audit date:** 2026-11-01 · **Certification ID:** RC-0000-000

## Scope and procedure

This is a Reproduction Study of the computation only. Stata 15 was not installed, so the complete shipped do-file was translated command by command into R and run against the supplied datasets. The translation includes data recoding, the inflation adjustment, logit models with district indicators and robust covariance, the `both == 1` subset models, both alternative contribution windows, and the 50-point margins used for Figures 1–3. The `marhis` figures were translated as average predicted probabilities at 50 equally spaced focal-variable values; the generated values are in `logs/figure-*-margins.csv`.

The translation implements Stata's perfect-prediction omission by retaining only IDs with outcome variation in each model. It yields 187 district-model observations, while Table 1 and Table 3 report 186. Incumbent models yield 106, as reported. Robust p-values differ from several Table 1 printed p-values. These are reported as discrepancies; no specification, data, or reported values were adjusted to force agreement.

The shipped script does not calculate Table 2's contribution-change counts/percentages or the approximate probabilities in the Results prose. Those results are marked `not_checkable`; no additional analysis was written to reconstruct them. No existing reproduction or replication report was consulted.

## Findings

- The translation completes all model stages. Table 1 district sample size does not recur (187 vs 186); Table 1 includes other coefficient, p-value, and pseudo-R² comparisons individually in `certificate.json`.
- Both incumbent model sample sizes recur (106). Table 3 sugar-contribution coefficients round to the printed values; its p-values and observation counts are listed separately in the JSON.
- Table 2 descriptive values and approximate prose probabilities are not produced by the shipped code and cannot be checked from this reproduction pipeline.
- **Computational outcome:** computational issues. **Robustness outcome:** not checked. This certificate makes no judgment on the scientific conclusion.

## Reproduction materials

- Article: [doi:10.1017/S0003055422000466](https://doi.org/10.1017/S0003055422000466)
- Supplied code and data package: `/tmp/scratch_bench_luna/packages/pkg-4e0ab3` (linked to the original package location; not copied into this bundle)
- Translated execution: [`code/translated_pipeline.R`](code/translated_pipeline.R)
- Environment record: [`sessionInfo.txt`](sessionInfo.txt)
- Console logs: [`logs/run-4.txt`](logs/run-4.txt) is the final completed run; earlier attempts are retained as `run-1.txt` through `run-3.txt`.

## FORRT chain vocabulary

`entry_type`: reproduction · `outcome_computational`: computational issues · `outcome_robustness`: not checked · `ai_generated`: true.
