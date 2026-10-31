# ReproCrowd reproduction certificate

**Paper:** Eunji Kim, “Entertaining Beliefs in Economic Mobility,” *American Journal of Political Science* 67(1), 39–54 (2023). [Article DOI](https://doi.org/10.1111/ajps.12702) · [Replication data archive](https://doi.org/10.7910/DVN/P4AH5C)

**ReproCrowd:** crowd-repro v1.1.0 · procedure 0.1.2 · audit date 2026-10-31  
**Engine:** Codex · **model/provider:** GPT-6 / OpenAI  
**FORRT chain outcome:** `outcome_computational = computational issues`; `outcome_robustness = not checked`.

## Outcome

The README-designated manuscript and appendix R scripts both execute to completion after installing their declared R dependencies. Seven of the eight selected numeric claims recur at the printed precision. One Table 1 treatment coefficient does not: the manuscript script returns **0.057** for the all-participant MTurk model, while the packaged rendered RMarkdown output gives **0.055**. The difference is 0.002. The `.R` script's `m1` model omits `optimism_index`, which the corresponding RMarkdown model includes. This is a shipped-code specification inconsistency, not a modified reproduction analysis.

The computation is **executable** with the documented package installation. It is **not fully computationally reproducible** under the shipped `.R` script because of the Table 1 discrepancy. No judgment is made about the scientific conclusion.

## Claims checked

| ID | Exhibit and quantity | Reported | Recomputed | Status |
|---|---|---:|---:|---|
| C1 | Table 1, MTurk treatment coefficient, all participants | 0.055 | 0.057 | discrepant |
| C2 | Table 1, lab-in-the-field treatment coefficient, all participants | 0.068 | 0.068 | match |
| C3 | Table 2, controlled heavy-viewer coefficient | 0.040 | 0.040 | match |
| C4 | Appendix Table A1, ordinary-category Cohen kappa | 0.936 | 0.936 | match |
| C5 | Appendix Table A1, economic-benefit-category Cohen kappa | 0.91 | 0.91 | match |
| C6 | Appendix Table A1, hard-work-category Cohen kappa | 0.835 | 0.835 | match |
| C7 | Appendix Table E1, America’s Got Talent viewing share (%) | 39.6 | 39.6 | match |
| C8 | Appendix Table K1, treatment × high system-justification interaction | 0.181 | 0.181 | match |

Each run used the supplied model and data. The only code-execution change was installing declared R packages; the shipped R scripts themselves are unmodified. The package README specifies R 4.1.0 on macOS Catalina; this run used R 4.6.1 on macOS Tahoe 26.7. See [sessionInfo.txt](sessionInfo.txt) and the full dependency inventory in `certificate.json`.

## Findings

- **P1 — Table 1 estimate differs.** The `.R` script returns 0.057 versus the packaged rendered RMarkdown output's 0.055. The `.R` model does not include `optimism_index`; the RMarkdown model does. Align the shipped model with the published specification and rerun.
- **P2 — environment version drift.** The environment differs from the package README's R and macOS versions. Missing packages were installed into the task-local R library. Package versions are recorded in `certificate.json`.

## Run records and code

- [Manuscript console log](logs/manuscript.log)
- [Appendix console log](logs/appendix.log)
- [Initial missing-package attempt](logs/initial-attempt.log)
- [Manuscript script](code/AJPS_2021_Kim_Manuscript.R)
- [Appendix script](code/AJPS_2021_Kim_Appendix.R)

The original code and data are not included here. Code/data link: [Harvard Dataverse replication archive](https://doi.org/10.7910/DVN/P4AH5C). Robustness was not checked.
