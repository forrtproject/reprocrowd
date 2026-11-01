# ReproCrowd computational reproduction check

**Outcome: technical failure.** The provided code does not reach the approved analyses, and none of the five reported statistics could be checked. This report concerns computation only; it does not assess the scientific conclusions.

**Engine:** Codex · **model/provider:** GPT-6 · OpenAI · **rules:** crowd-repro v1.1.0 · **prompt:** 0.1.2 · **date:** 2026-10-31.

## Source materials and execution

The paper is [Tomai et al. (2023)](https://doi.org/10.5194/agile-giss-4-13-2023). The original [Figshare article, version 1](https://figshare.com/articles/dataset/Does_spatial_thinking_ability_relate_to_performance_when_using_web-mapping_services_A_survey_with_digital_natives/22132940/1) supplied `survey_2021.R` (SHA-256 `ce9f3a018da08164caa62e0b601399ee740bed9b2f2cd4311bfb47bbf3c4fa5e`) and `dataset.7z` (SHA-256 `86898d52d894af27904f3e80428c71a32af4f8a42f3bc575ad30138caf8ee89e`). Both fingerprints matched before execution. The original data and unmodified code are not included here.

The shipped R script was run with R 4.6.1 and its required packages installed in the available environment. The full installed R package inventory and `sessionInfo()` are recorded in [environment_sessionInfo.txt](logs/environment_sessionInfo.txt). The console output is [full_run.log](logs/full_run.log).

Two execution-only changes are in [survey_2021.R](code/survey_2021.R): the two `View()` calls are guarded by `interactive()` because this run has no graphical R session; and the script’s Group 2 section now reads the explicitly named `GM_HWG.csv` using the same `read_delim()` settings as the other service CSVs. The latter exposed the next problem: the script uses `GMHWG$Sum_GM_Group2` but never constructs that score column. Building it would require writing omitted preprocessing, so execution stopped without doing so. The added [run_reproduction.R](code/run_reproduction.R) only sources the working script and would print existing test objects if the source reached them.

## Approved claims

| ID | Reported statistic | Recomputed | Result |
|---|---:|---:|---|
| C1 | Wilcoxon signed-rank V = 281 | Not computed | Not checkable: the shipped script omits the Google Maps versus HERE WeGo total-task test. |
| C2 | Wilcoxon rank-sum W = 1036 | Not computed | Not checkable: execution stops because `Sum_GM_Group2` is absent. |
| C3 | Paired t = 9.45 | Not computed | Not checkable: execution stops before the SUS analyses. |
| C4 | Wilcoxon rank-sum W = 1037.5 | Not computed | Not checkable: execution stops before the between-group SUS test. |
| C5 | Kendall tau = 0.29 | Not computed | Not checkable: execution stops before the STAT–Google Maps correlation. |

## Findings

- **DEF-001 (P0, defect):** the source stops at its first use of the uncreated Group 2 score column (`GMHWG$Sum_GM_Group2`). The Group 2 preprocessing needed to create it is omitted from the shipped script. The run exits with code 1.
- **DEF-002 (P1, defect):** the approved Google Maps versus HERE WeGo total-task comparison is not implemented in the shipped script; the Group 2 test code is described as omitted.

The FORRT outcome is **technical failure** (`outcome_robustness: not checked`). No numeric result reproduced because none was computed; no value was independently reconstructed. The most direct way to make these claims checkable is for the authors to supply the omitted Group 2 preprocessing and the Google Maps versus HERE WeGo total-task test code.
