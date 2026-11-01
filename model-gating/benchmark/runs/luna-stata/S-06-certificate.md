# ReproCrowd reproduction check

**Outcome: technical failure.** The supplied master pipeline cannot start its cleaning stage because all five raw ATUS input files it requires are absent. No result was recomputed, so this check makes no judgment about the paper’s scientific conclusions.

## Identification and environment

- Paper: *Examining inequality in the time cost of waiting* (2023), [doi:10.1038/s41562-023-01524-w](https://doi.org/10.1038/s41562-023-01524-w)
- Procedure: ReproCrowd benchmark prompt 0.1.2; rule pack `crowd-repro v1.1.0`
- Engine: Codex · model: GPT-6.1 Luna · provider: OpenAI
- Date: 2026-11-01; host: macOS
- R 4.6.1; haven 2.5.5; Stata not installed. See [sessionInfo.txt](sessionInfo.txt).

## Execution and findings

The R entry point records the shipped master order and checks the files consumed by `02_cleaning.do`. The run stopped at its first stage with `atusrost0319.dta`, `atuscps0319.dta`, `atusresp0319.dta`, `atussum0319.dta`, and `atusact0319.dta` all missing. The shipped `atusall0319.dta` is a preassembled analytic dataset, but it is not a substitute for reproducing the omitted cleaning stage. `05_imputation.do` additionally references `draft\nature\check\federal_poverty_threshold.dta`, also absent.

The result records identify selected reported values from Supplementary Table 1 and the accompanying text as `not_checkable`; each has `basis: not_computed`. No computed value is presented as a reproduction. The full article includes further numerical results not inventoried here. Stata’s five scripts were **not** translated command by command into R; the included R file is only an execution entry point and missing-input check. Thus this deliverable does not satisfy the requested full-pipeline translation or exhaustive claim enumeration.

The package README points to the ATUS source files at [BLS ATUS 2003–2019 data files](https://www.bls.gov/tus/datafiles-0319.htm) and states that the scripts need them. The original package is at `/tmp/scratch_bench_luna/packages/pkg-3189d3`; it was not modified or uploaded.

The FORRT chain mapping is `outcome_computational: technical failure` and `outcome_robustness: not checked`. Certification identifier and GitHub fields use the benchmark placeholders.

## Artifacts

- [R execution entry point](code/pipeline_translation.R)
- [Run log](logs/pipeline.log)
- [Environment record](sessionInfo.txt)
- [Machine-readable certificate](certificate.json)
