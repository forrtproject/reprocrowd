# ReproCrowd computational check

**Status: computation not checked.** No reported value was recomputed, so this is not a completed reproduction study and makes no claim that any result recurs or fails to recur. It does not assess the scientific conclusion.

## Paper and procedure

Bianchi and Giorcelli, “The Dynamics and Spillovers of Management Interventions: Evidence from the Training within Industry Program,” *Journal of Political Economy* (2022), [doi:10.1086/719277](https://doi.org/10.1086/719277).

ReproCrowd `crowd-repro` rule pack v1.1.0; procedure URI: https://forrtproject.github.io/reprocrowd/crowd-repro/RULEPACK-v1.1.0.md. Engine: Codex; model/provider: GPT-6.1 Luna / OpenAI. Environment: macOS, R 4.6.1; see `sessionInfo.txt`.

## Execution and limitations

The shipped master file calls 3 main-text figures, 5 main-text tables, 11 appendix figures and 21 appendix tables. Stata is not installed. Although the prompt requires translating and running the whole pipeline in R, that translation was not completed. The `.do` files in `code/` are copies for reference only and were not executed. No result has been marked match, discrepant, or not_checkable, and no reported values were recomputed.

The complete set of data-derived numerical claims in the abstract, main text and tables was also not enumerated. The empty claim/result lists in `certificate.json` mean “not assessed,” not “no claims.” This certificate therefore does not fulfill the requested exhaustive benchmark. The local shipped package is `/tmp/scratch_bench_luna/packages/pkg-775f66`; no original data were copied or uploaded.

## Required next step

A complete check requires a command-by-command R translation of every script invoked by the master pipeline, execution of that translation, and a claim-by-claim audit of every printed data-derived number in the article. Only then can the computation be classified as reproducible, computational issues, or technical failure under the rule pack.
