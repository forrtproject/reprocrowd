# ReproCrowd computational reproducibility certificate

**RC-2026-923 · 2026-10-30 · Reproduction Study · PartiallySupported**

[Does spatial thinking ability relate to performance when using web-mapping services? A survey with digital natives](https://doi.org/10.5194/agile-giss-4-13-2023)

51 claim groups were assessed: **48 match fully and 3 match partly in primary R 4.6.1** after explicitly documented code repairs. A supplementary same-call check under R 4.2.2 recovers two discrepant confidence intervals, leaving one unresolved reported statistic across the recorded runtimes. The unmodified deposited script fails; this is not an unqualified certificate of executable shipped code. Scientific correctness was not assessed.

## Required validation and publication gaps

The exact public rule pack and certificate schema both returned **HTTP 404**. The prompt artifact list was used as the fallback. **Official schema validation is unavailable**, although certificate.json parses as JSON and has one result for every claim. See [validation evidence](results/schema-validation.json). No substitute schema was invented.

No signed FORRT chain was published and no public report URL was created. [nanopubs/PUBLISHED.md](nanopubs/PUBLISHED.md) records the missing URIs. A local draft uses the documented FORRT chain vocabulary; it is not a published nanopublication. Human sign-off is pending.

## Source and execution evidence

[Figshare version 1](https://figshare.com/articles/dataset/22132940/1) contains the 47,107-byte R script, dataset.7z, and questionnaire. All three files match the repository MD5 values; SHA256 checksums are in [source-manifest.json](results/source-manifest.json). They were downloaded only; nothing was uploaded. The seven CSVs remain unchanged.

The strict run stops at `View(Demographics_DNAS)` because X11 is unavailable. Omitting only View reaches `object 'GMHWG' not found` at original line 769. The source explicitly omits the Group 2 block. Its Fisher comparisons use hard-coded HWG success counts; these were cross-checked against the shipped data. SUS objects are also consumed before their definitions. Continue-on-error diagnosis records 419 expressions, two omitted View calls and 87 propagated errors. [Strict log](logs/original-strict.log), [headless log](logs/original-headless.log), [diagnostic ledger](results/diagnostic/execution.json).

## Transparent repairs

- **D1 (execution_adaptation):** Omit the two interactive View() calls for headless execution; retain all original files unchanged.
- **D2 (missing_code_reconstruction):** Copy source lines 272–758 (Group 1 analysis), substituting BM→HWG, Group1→Group2 and group1→group2, to supply the explicitly omitted Group 2 block.
- **D3 (explicit_missing_data_assumption):** Treat the five blank Group 2 binary task responses as unsuccessful (0): Task5_GM 1, Task4_HWG 1, Task5_HWG 3. This is consistent with the paper scoring description and the shipped STAT NA→0 step, but is not executable shipped Group 2 code. Preserve minimal-repair outputs without this assumption for comparison.
- **D4 (dependency_order_repair):** Evaluate the original SUS input/scoring definitions (source lines 1045–1084) before the cross-group analysis that consumes those objects at lines 774 onward. Original later definitions remain unchanged.
- **D5 (missing_result_reconstruction):** Compute the omitted four HWG Kendall correlations using the paper-described test and the same R cor.test(method="kendall",exact=FALSE) pattern. Match rows by participant ID; audit confirms existing file order is aligned.
- **D6 (result_export_only):** Capture the original Google Maps SUS–task correlation before the final source lines overwrite SUS_GMCorrelation with a STAT correlation; export full-precision test fields separately from rounded display matrices.

The minimal Group 2 reconstruction leaves five task responses missing and therefore produces missing total scores and different complete-case tests. [Preserved minimal-repair outputs](results/minimal-repair) show this intermediate result. Converting these missing binary responses to zero restores the reported group means, comparisons and correlations. This assumption is reported as a repair, rather than attributed to absent shipped code.

## Numerical discrepancies

| Claim | Paper | Recomputed in R 4.6.1 | Agreement |
|---|---|---|---|
| C22, Table 4 GM–BM score | V = 78, p = .012, CI [−1.5, 0.0] | V = 78, p = .0117351, CI [−1.00004, −0.0000771] | Statistic and p match; CI differs |
| C35, Table 8 GM–BM SUS | V = 382.5, p < .001, CI [5, 13.75] | V = 382.5, p = .0000438317, CI [3.74998, 9.99999] | Statistic and p match; CI differs |
| C37, Table 8 BM–HWG SUS | W = 1037.5, p < .001, CI [12.5, 30.0] | W = 1137.5, p = .000000968047, CI [12.50005, 29.99996] | p and CI match; statistic differs |

These mismatches also occur in the shipped expressions during headless diagnostic execution, so the Group 2 score repair does not explain them. A controlled supplementary check used the same shipped columns and the same three base-R test calls under a separately pinned R 4.2.2 runtime. It recovers both published confidence intervals: C22 [−1.5000228, −0.0000444] and C35 [5.0000035, 13.7499632]. Repeating the identical check under R 4.6.1 agrees with the primary run, establishing version sensitivity of those two intervals. C37 remains W = 1137.5 under both versions. The authors’ exact original runtime is not established. See [R 4.2.2 output](results/version-check-R-4.2.2.csv), [R 4.6.1 control](results/version-check-R-4.6.1.csv), and [runtime lock](historical-R-check/pixi.lock). Primary statuses in the following table remain tied to R 4.6.1; supplementary results are nested within the existing claim results, rather than counted as additional claims.

## Claim-by-claim results

“Reproduced” below means every assessed numerical field in that claim group matches at the reported precision; it does not mean the original unmodified script ran successfully. `shipped_code_headless_diagnostic` records expressions executed after omitting View and continuing past earlier errors. `reconstructed_code` requires the documented additions.

| Claim | Paper location | Result | Execution basis | Mismatched fields |
|---|---|---|---|---|
| C01 Sample composition and group sizes | §3.2, §3.5.1 | reproduced | source_data_audit | — |
| C02 Reasons for computer and smart-device use: education, entertainment and social media predominate | Figure 1; §4.2 | reproduced | shipped_code_headless_diagnostic | — |
| C03 Familiarity: GM highest, HWG lowest; about 7% moderately familiar with Boston | Figure 2; §4.2 | reproduced | mixed_shipped_and_reconstructed | — |
| C04 DNAS descriptive statistics and internal consistency | §4.2; Figure 3 | reproduced | shipped_code_headless_diagnostic | — |
| C05 STAT descriptive statistics, internal consistency, and no boxplot outliers | §4.3; Figures 4–5 | reproduced | shipped_code_headless_diagnostic | — |
| C06 Task score means by group and service | Figures 6–7 | reproduced | mixed_shipped_and_reconstructed | — |
| C07 Group 1 Task 1: success rates and McNemar test | Table 1 | reproduced | shipped_code_headless_diagnostic | — |
| C08 Group 1 Task 2: success rates and McNemar test | Table 1 | reproduced | shipped_code_headless_diagnostic | — |
| C09 Group 1 Task 3: success rates and McNemar test | Table 1 | reproduced | shipped_code_headless_diagnostic | — |
| C10 Group 1 Task 4: success rates and McNemar test | Table 1 | reproduced | shipped_code_headless_diagnostic | — |
| C11 Group 1 Task 5: success rates and McNemar test | Table 1 | reproduced | shipped_code_headless_diagnostic | — |
| C12 Group 2 Task 1: success rates and McNemar test | Table 2 | reproduced | reconstructed_code | — |
| C13 Group 2 Task 2: success rates and McNemar test | Table 2 | reproduced | reconstructed_code | — |
| C14 Group 2 Task 3: success rates and McNemar test | Table 2 | reproduced | reconstructed_code | — |
| C15 Group 2 Task 4: success rates and McNemar test | Table 2 | reproduced | reconstructed_code | — |
| C16 Group 2 Task 5: success rates and McNemar test | Table 2 | reproduced | reconstructed_code | — |
| C17 BM versus HWG Task 1: success rates and Fisher test | Table 3 | reproduced | shipped_code_headless_diagnostic | — |
| C18 BM versus HWG Task 2: success rates and Fisher test | Table 3 | reproduced | shipped_code_headless_diagnostic | — |
| C19 BM versus HWG Task 3: success rates and Fisher test | Table 3 | reproduced | shipped_code_headless_diagnostic | — |
| C20 BM versus HWG Task 4: success rates and Fisher test | Table 3 | reproduced | shipped_code_headless_diagnostic | — |
| C21 BM versus HWG Task 5: success rates and Fisher test | Table 3 | reproduced | shipped_code_headless_diagnostic | — |
| C22 All-task score comparison: GM1-BM | Table 4 | partially_reproduced | shipped_code_headless_diagnostic | ci |
| C23 All-task score comparison: GM2-HWG | Table 4 | reproduced | reconstructed_code | — |
| C24 All-task score comparison: BM-HWG | Table 4 | reproduced | reconstructed_code | — |
| C25 Successful Task 4 completion time: BM versus HWG | Table 5 | reproduced | reconstructed_code | — |
| C26 Successful Task 5 completion time: BM versus HWG | Table 5 | reproduced | reconstructed_code | — |
| C27 SUS descriptive statistics: GM1 | Table 6 | reproduced | shipped_code_headless_diagnostic | — |
| C28 SUS descriptive statistics: BM | Table 6 | reproduced | shipped_code_headless_diagnostic | — |
| C29 SUS descriptive statistics: GM2 | Table 6 | reproduced | shipped_code_headless_diagnostic | — |
| C30 SUS descriptive statistics: HWG | Table 6 | reproduced | shipped_code_headless_diagnostic | — |
| C31 SUS internal consistency: GM1 | Table 7 | reproduced | shipped_code_headless_diagnostic | — |
| C32 SUS internal consistency: BM | Table 7 | reproduced | shipped_code_headless_diagnostic | — |
| C33 SUS internal consistency: GM2 | Table 7 | reproduced | shipped_code_headless_diagnostic | — |
| C34 SUS internal consistency: HWG | Table 7 | reproduced | shipped_code_headless_diagnostic | — |
| C35 SUS score comparison: GM1-BM | Table 8 | partially_reproduced | shipped_code_headless_diagnostic | ci |
| C36 SUS score comparison: GM2-HWG | Table 8 | reproduced | shipped_code_headless_diagnostic | — |
| C37 SUS score comparison: BM-HWG | Table 8 | partially_reproduced | shipped_code_headless_diagnostic | statistic |
| C38 Kendall correlation: STAT with task score on GM | Table 9 | reproduced | reconstructed_code | — |
| C39 Kendall correlation: STAT with task score on BM | Table 9 | reproduced | shipped_code_headless_diagnostic | — |
| C40 Kendall correlation: STAT with task score on HWG | Table 9 | reproduced | reconstructed_code | — |
| C41 Kendall correlation: FAM with task score on GM | Table 9 | reproduced | reconstructed_code | — |
| C42 Kendall correlation: FAM with task score on BM | Table 9 | reproduced | shipped_code_headless_diagnostic | — |
| C43 Kendall correlation: FAM with task score on HWG | Table 9 | reproduced | reconstructed_code | — |
| C44 Kendall correlation: DNAS with task score on GM | Table 9 | reproduced | reconstructed_code | — |
| C45 Kendall correlation: DNAS with task score on BM | Table 9 | reproduced | shipped_code_headless_diagnostic | — |
| C46 Kendall correlation: DNAS with task score on HWG | Table 9 | reproduced | reconstructed_code | — |
| C47 Kendall correlation: SUS with task score on GM | Table 9 | reproduced | reconstructed_code | — |
| C48 Kendall correlation: SUS with task score on BM | Table 9 | reproduced | shipped_code_headless_diagnostic | — |
| C49 Kendall correlation: SUS with task score on HWG | Table 9 | reproduced | reconstructed_code | — |
| C50 Google Maps task-score homogeneity between groups | §4.5 | reproduced | reconstructed_code | — |
| C51 Google Maps SUS scores similar between groups | §4.5 | reproduced | reconstructed_code | — |

All expected and observed values, with full-precision results and field checks, are in [certificate.json](certificate.json) and [claim-results.json](results/claim-results.json). All 28 available shipped hypothesis-test objects are identical between headless diagnostic and repaired execution; see [the comparison](results/shipped-htest-comparison.json). The [input audit](results/data-audit.json) checks counts, ID uniqueness/order, and missingness without exposing participant records.

## Figures

Seven figures were regenerated in R. Original code comments number several figures differently from the final article; the output manifest follows the article captions. Figures 1–6 use shipped plotting calls; Figure 7 uses their Group 2 counterpart. PNG hashes and dimensions are in [the manifest](results/figures/manifest.json). The published page render and generated plots were inspected for selected figures; exact pixels, fonts, and margins were not certified.

## Environment and rerun

Engine: **Codex harness through T3 Code**. Model/provider: **gpt-6.1-sol / OpenAI**, reasoning effort high. Requested rule version: **v1.0.0 unavailable**; supplied prompt **0.1.0** used as fallback.

[environment.json](environment.json) records OS, interpreter versions, executable inventory, package versions, and lock hashes. The supplied macOS R 4.6.1 executes the statistical script. Pixi 0.83.0 is installed locally; pixi.lock pins Python, a same-version R distribution, native build dependencies, and Python packages. historical-R-check/pixi.lock separately pins the supplemental R 4.2.2 base runtime. **148 R packages** are independently pinned by exact version, archive URL, and SHA256 in r-packages.lock.json and restored into r-library. Mac R framework binaries require the compatible host R; the pixi R binary is not assumed to replace it.

On this macOS arm64 host, run:

```sh
./bootstrap.sh
# After activation and package restoration:
CERT_RSCRIPT=/usr/local/bin/Rscript tools/pixi run snakemake --cores 1
```

The workflow preserves expected original-code failures and continues to the repaired numerical analysis. A successful workflow exit means the report was built; schema unavailability and unpublished nanopublications remain explicit certification gaps. A clean restoration of all 148 R packages and a full forced workflow rerun were checked locally. A second machine and other operating systems have not been certified.

## Limits and sign-off

- The required public rule pack and certificate schema returned HTTP 404. The prompt artifact list is the fallback specification. Official JSON-schema conformance cannot be established; syntactically valid JSON and local integrity checks are not schema validation.
- The unmodified shipped script is not executable end to end in the headless environment; it stops at View(), and a headless-only adaptation stops at the omitted GMHWG object. Numerical reproduction after transparent repairs must not be read as execution success of the unmodified archive.
- Three numerical claim groups only partly match under primary R 4.6.1. A targeted same-data, same-call check under R 4.2.2 recovers both discrepant confidence intervals; the W=1037.5 versus 1137.5 discrepancy persists. The original exact runtime was not shipped, so R 4.2.2 is not asserted to be the authors’ actual version.
- No signed nanopublications or public report repository were published. nanopubs/PUBLISHED.md explicitly records that no result URIs exist; a field-by-field draft chain is supplied. Human identity, ORCID, signing credentials, and public repository URL were not supplied or transmitted.
- This certifies numerical computational agreement only. Scientific validity, the suitability of statistical tests, robustness under alternative methods, and independent replication with new data were not assessed.
- The locked Pixi environment was created locally and all 148 R packages were restored into an empty library, followed by a full workflow rerun. A rebuild on a second host has not been tested; macOS framework R 4.6.1 and Apple build tools remain host prerequisites.

No prior reproduction, replication or verification report about this paper was consulted. The review link printed in the original article was not followed. No emails, ORCIDs, contributor names, signing identities, original data or original code were transmitted to a publishing service. See [SIGN-OFF.md](SIGN-OFF.md).
