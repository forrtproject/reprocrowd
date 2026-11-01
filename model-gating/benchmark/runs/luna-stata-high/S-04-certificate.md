# Reproduction certificate

**Paper:** Kristian Vrede Skaaning Frederiksen, “Does Competence Make Citizens Tolerate Undemocratic Behavior?” *American Political Science Review* 116(3), 1147–1153 (2022). [Article DOI](https://doi.org/10.1017/S0003055422000119) · [Original replication data and code record](https://doi.org/10.7910/DVN/NGFLRO)

**Certification:** RC-0000-000 · **Procedure:** ReproCrowd benchmark prompt 0.1.2 · **Rules:** crowd-repro v1.1.0 · **Date:** 2026-11-01

**Outcome:** **computationally reproducible** for the article’s reported primary numerical results, using a direct R translation of the primary Stata analysis block. The translated estimates match the printed values at their reported precision. **Outcome robustness:** not checked. This report assesses computation only and makes no judgment about the scientific conclusion.

**Engine:** OpenAI Codex · **Model/provider:** GPT-6 / OpenAI. The model generated the translation and report. The actual run used R 4.6.1 on macOS Tahoe 26.7 (Apple Silicon); packages and versions are recorded in [sessionInfo.txt](sessionInfo.txt). The console output is in [analysis-primary.txt](logs/analysis-primary.txt), and the executed translation is [analysis.R](code/analysis.R).

## Results checked

The provided final dataset reproduces the article’s pooled sample counts exactly: **14,058 respondents** and **267,795 candidate observations**. Country counts also match the figure note: 2,481–3,159 respondents and 47,221–60,106 candidate observations.

The translated average-effects models reproduce the reported undemocratic-behavior effect range: **−0.0555 in South Korea** (reported −0.06) to **−0.2043 in the United States** (reported −0.20). The ordinal competence slope ranges from **0.1381 to 0.1492**, matching the reported approximate range of 0.14–0.15. Both effects meet the article’s stated p < .001 threshold in each of the five countries.

The interaction analysis reproduces the nonsignificant very-competent versus average-competence contrasts in all five countries. For the Czech very-incompetent versus average-competence contrast, the translated estimate is **0.1285**, 95% CI **[0.0508, 0.2062]**, p = **0.001205**; these round to the article’s 0.13, [0.05, 0.21], and p = .001. The equivalent low-competence contrasts are not significant in the other four countries.

Every checked numerical claim and individual result is listed in [certificate.json](certificate.json), retaining its C-id. Results use `basis: translated` as required for Stata code run in R.

## Scope and limits

The package includes `dataset.dta`, the final analysis dataset, and the translated primary analysis executes on it. `Data_prep.do` imports five country TSV files (`ukmain.tsv`, `usmain.tsv`, `mxmain.tsv`, `skmain.tsv`, and `czmain.tsv`) from a Windows U: drive; those raw exports are not present in the supplied package. Therefore the raw-to-final preparation stage could not be re-executed, and the complete 2,755-line preparation script and auxiliary commands in `Analysis.do` were not translated in full. The reported article results were checked against the supplied final dataset and the primary-analysis commands. This limitation is recorded as finding DATA-001 in the JSON certificate.

Original code and data were not copied or uploaded. The article identifies the authors’ replication record at the linked Harvard Dataverse DOI. The local package used for this check was `/tmp/scratch_bench_luna/packages/pkg-984353`.
