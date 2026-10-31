# ReproCrowd pilot certificate RC-2026-908

**Engine: T3 Code / Codex harness · gpt-6.1-sol (OpenAI, high reasoning) · rules: crowd-repro v1.0.0**

Audit date: 2026-10-30 · Procedure: 0.1.0-pilot-G08.1 · Study type: **Reproduction Study** (same methodology, same tools).

## Computational outcome

**validation_status: technical failure.** The unchanged main-text R script failed in a 24-row figure-label data frame. The unchanged appendix ran successfully. One lossless loop-bound correction allowed the full main-text script to complete. Of 698 comparisons across 225 claims/exhibit checks, 650 match within stated tolerances, 14 are close, 24 are discrepant, and 10 are not checkable. Public publication, FORRT chain URIs and human sign-off remain pending. Scientific correctness and robustness were not assessed.

This outcome applies to executability of the shipped package. It does not establish whether the paper’s scientific conclusions are correct. `outcome_robustness = not checked`. The normalized-run outcome is **computational issues**; normalization did not turn the unchanged source into a successful run.

## Sources and scope

- Article: [Do Transitional Justice Museums Persuade Visitors? Evidence from a Field Experiment](https://doi.org/10.1086/714765). DOI/title/authors/year were checked using Crossref, not recalled.
- Comparison document: September 1, 2020 accepted manuscript, [public PDF](https://www.almendron.com/tribuna/wp-content/uploads/2020/10/do-transitional-justice-museums-persuade.pdf); 28 pages. Final publisher PDF was not accessible.
- Code and data: [pinned shipped package](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/19/replication_package). Exactly five files were downloaded. No prior reproduction report was opened or used.
- `sources/source-manifest.json` records immutable SHA-256 hashes, byte sizes and public download URLs. No original code or data was uploaded.
- `claims.json` and `claims-approval.json` enumerate the claims before computational checks; user pilot instruction 4 supplies approval. C225 (missingness) was added transparently in the completeness audit after the first run; the initial list is retained in `sources/claims-initial.json`. Supplementary numerical cells are not exhaustively enumerated because their source document was unavailable.

## Execution and normalization

| Run | Exit code | Evidence |
|---|---:|---|
| maintext-original | 1 | `logs/maintext-original.log` |
| appendix-original | 0 | `logs/appendix-original.log` |
| maintext-normalized | 0 | `logs/maintext-normalized.log` |

Exact equality of all 51 estimator objects common to the original and normalized runs was verified (`outputs/normalization-invariance.json`). The sole edit is `for (i in 22:34)` → `for (i in 22:24)` in the Figure 2 label assignment. It only removes iterations beyond the 24 existing results rows; it changes no numeric cell or estimator. Originals remain under `extracted/`; `outputs/normalization.patch` records the exact diff. Data were copied without cleaning or recoding beyond what the authors’ scripts themselves do.

## Comparisons

| Status | Results |
|---|---:|
| match | 650 |
| close | 14 |
| discrepant | 24 |
| not_checkable | 10 |

Total: **225 claims/exhibit checks; 698 results**. One claim may contain multiple quantities (estimate, SE, two CI endpoints). There are 154 plotted estimate/uncertainty records: 117 in Figures 1–3 and 37 in Figure 4.

Text and figure-label values use half the last printed unit as tolerance; integers require equality. Graphical values are extracted independently from PDF vectors, using printed axis ticks for calibration: interval midpoints yield estimates, half of short intervals yields SEs, and long intervals yield 95% CIs. Graphical absolute tolerance is 0.005 outcome units; “close” allows up to 0.01. All calibration coordinates, paths and extracted values are retained in `outputs/digitized-figures.json`. Graphical values are approximate reconstructions of the printed exhibit, not claimed original floats.

Examples: government-satisfaction coefficient 0.15 → 0.152164891977; democracy 0.14 → 0.136477997261; church trust 0.18 → 0.180891398614; pardoning 0.22 → 0.216794594636. The government p-value 0.04 → 0.034968351847 is close but falls just outside strict two-decimal rounding tolerance.

The full comparison ledger is [results.md](results.md); exact numeric fields and differences are in [certificate.json](certificate.json). This ledger includes negative results and non-checkable items, not only matches.

## Findings

### RUN-001 · P0 · defect

The unchanged main-text script fails in the Figure 2 labelling loop: indices 22:34 extend a 24-row results data frame.

**Evidence:** logs/maintext-original.log: replacement has 25 rows, data has 24; outputs/execution.json exit code 1.

**Suggested fix:** Change only the loop upper bound from 34 to 24; distribute a tested master runner.

### NORM-001 · P3 · normalization

The working copy changes one loop bound, 22:34 to 22:24. No data, model specification, compliance factor, estimate, standard error or p-value is changed.

**Evidence:** outputs/normalization.patch; maintext-normalized exits 0. Extracted originals retain source-manifest SHA-256 hashes.

**Suggested fix:** Retain this documented patch until upstream code is corrected.

### PV-001 · P1 · defect

The shipped estimators divide all four coeftest fields by the compliance scalar, including the t statistic and p-value. The certificate faithfully reports the shipped values.

**Evidence:** BPV_museums_maintext.R lines 34, 44, 507, 517; itt.d=0.965034965034968. No correction was made.

**Suggested fix:** Authors should clarify the intended inference and scale only fields for which that scaling is intended, then regenerate p-values and figures consistently. This certificate does not test scientific robustness.

### MEAN-001 · P2 · defect

3 hard-coded figure control means do not equal the means of the shipped control observations.

**Evidence:** policies_compensate.control_mean: printed 1.51, observed 1.152, gap -0.358; decided.control_mean: printed 2.14, observed 2.21428571429, gap 0.0742857142857; negative.control_mean: printed 3.44, observed 5.50793650794, gap 2.06793650794

**Suggested fix:** Generate annotations from the same analysis data and document the denominator and outcome definition.

### GRAPH-001 · P2 · defect

15 plotted numerical quantities exceed 0.01 outcome units of difference; additional close values are listed separately. Differences concentrate in right-subgroup emotions.

**Evidence:** C123 positive.right.coefficient: gap 0.0766160514314; C123 positive.right.ci95.low: gap 0.0712581237607; C123 positive.right.ci95.high: gap 0.08143904562; C126 alert.right.coefficient: gap 0.0132261356501; C126 alert.right.ci95.low: gap 0.0176157287986; C132 decided.right.coefficient: gap 0.0258705939981; C132 decided.right.ci95.low: gap 0.0221860481862; C132 decided.right.ci95.high: gap 0.0294016371585; C135 energetic.right.coefficient: gap 0.0134197483561; C135 energetic.right.ci95.low: gap 0.0122623104105; C135 energetic.right.ci95.high: gap 0.0141259815384; C156 negative.right.ci95.low: gap 0.0178597477962; C174 irritable.right.coefficient: gap 0.0122536005575; C174 irritable.right.ci95.low: gap 0.0135711997615; C174 irritable.right.ci95.high: gap 0.0104218732625

**Suggested fix:** Reconcile the accepted-manuscript figure inputs with the shipped subgroup data and preprocessing. Exact cause is unestablished: possible undocumented data/imputation or paper/code version differences, not demonstrated interpreter drift.

### TIME-001 · P2 · defect

The follow-up pardon numbers 0.20 and 0.16 match f3 (24 weeks), while nearby text describes diminishing significance after one week. At f1 the shipped result is 0.3080994760 with p=0.0040619090.

**Evidence:** C21; pardoned_f3 coefficient 0.2047054162, p 0.1640234164. Both temporal interpretations are retained in results.

**Suggested fix:** State the wave explicitly in the sentence; do not substitute the f3 result for f1 without explaining the time point.

### DESC-001 · P2 · defect

Some descriptive proportions and ideology gaps cannot be recovered under the stated arithmetic or either of two documented natural subgroup algorithms.

**Evidence:** Control arrivals: 126/251=50.1992031873%, printed 50.6%. New-information share: 18/135=13.3333333333%, printed 13.14%. Gap comparisons and alternate definitions are recorded per result.

**Suggested fix:** Publish the exact denominators, subgroup summaries and construction code for descriptive claims; distinguish retained data from assignment and arrival populations.

### SCOPE-001 · P2 · defect

Full final-version and supplementary numerical certification remains incomplete. The publisher PDF request returned an access/challenge page; comparisons use a September 1, 2020 accepted manuscript. The package contains no supplementary paper.

**Evidence:** sources/article-accepted.pdf (28 pages), source manifest; appendix execution succeeded but no independently reported table values were available.

**Suggested fix:** Supply the final article and supplement with an exhibit-to-code map, plus original environment/version information and recruitment/attrition provenance.

### DOC-001 · P3 · defect

The codebook refers to replicationdata.csv and baselineuc.csv, whereas the shipped files are all.Rdata and baseline.Rdata; the scripts use an earlier paper title.

**Evidence:** Codebook p.1; extracted file manifest. The RData object names are all and baseline; dimensions 264 x 151 and 1172 x 8.

**Suggested fix:** Update the codebook filenames/title and provide a master README. Use data-inventory.json as the authoritative actual column count.

### URL-001 · P3 · defect

The prompt’s original rule-pack and schema URLs return 404. The user supplied working forrtproject.github.io URLs during this run.

**Evidence:** logs/schema-headers.txt and logs/rulepack-headers.txt; corrected public copies are vendored and hashed in source-manifest.json.

**Suggested fix:** Update the prompt URLs. This run uses the identical version-labelled live rule pack and live certificate/flora schemas supplied by the user.

### PUB-001 · P2 · defect

No GitHub report, archive DOI, FORRT nanopublication chain, or FLoRA delivery was published. Human sign-off is pending.

**Evidence:** nanopubs/PUBLISHED.md explicitly lists no published URIs. github_url/url_r contain an unpublished URN, not an invented repository URL. SIGN-OFF.md is unsigned.

**Suggested fix:** After human review, publish a source-free report bundle through the contributor’s chosen destination, replace the unpublished URN with the real report URL, and complete the six linked nanopublications without including private identifiers or source data/code.

## Environment and rerun

Host: macOS 26.7, arm64 (25.6.0). R 4.6.1; Python 3.12.12; pixi 0.83.0. The full inventory is in [environment.json](environment.json). `pixi.lock` pins the Python and workflow dependency graph; `r-packages.lock.json` pins 48 R/base packages, including SHA-256 hashes for 37 downloadable binaries. Installed system R 4.6.1 and its recommended lattice 0.22-9 are required. No original author environment lockfile was supplied.

From this directory, with the locally installed pixi executable or another pixi 0.83.0:

```sh
../tools/pixi install --locked
../tools/pixi run --locked snakemake --cores 1
```

Inside the activated pixi environment, `snakemake --cores 1` runs the same workflow. `scripts/bootstrap_r.py` checks or installs the pinned R binaries into the library inside the pilot directory. To force a full local rerun, use `snakemake --cores 1 --forceall`. Download/analysis failures are recorded truthfully; the pipeline treats the known original-main failure as an observed result, not as a successful original run.

## Rule-pack URL correction

The prompt’s original `https://lukasroeseler.github.io/reprocrowd/...` rule-pack and schema links returned HTTP 404. The user corrected them to `https://forrtproject.github.io/reprocrowd/...`. The corrected public version 1.0.0 rule pack and both schemas are vendored and hash-recorded. Original 404 headers are retained. This report follows the live pack rather than relying only on fallback requirements.

## Publication, FORRT vocabulary and sign-off

FORRT chain vocabulary: **Quote-with-comment → AIDA → FORRT Claim → FORRT Replication Study (type: Reproduction Study) → Replication Outcome → CiTO Citation**. The study type is **Reproduction Study**; computational status is **technical failure**; robustness is **not checked**. The draft evidence qualification is **PartiallySupported** with **HighConfidence**, distinct from the certificate’s computational status, and any later CiTO link would **qualify** computational evidence rather than judge scientific truth.

`nanopubs/PUBLISHED.md` contains no published URI. `nanopubs/chain-plan.json` is a local plan with missing links explicitly absent. No external identity/signature was created or submitted. `SIGN-OFF.md` is prepared for human review and remains unsigned. `flora-entry.json` is schema-valid staging metadata, not evidence of FLoRA ingestion. `github_url` and `url_r` deliberately use `urn:reprocrowd:unpublished:RC-2026-908`; it is a valid URI and an explicit unpublished marker, not a claimed GitHub destination. No repository/DOI was fabricated.

## Limitations

- As-shipped execution and normalized execution are separate outcomes. Overall status follows rule pack §11: a fatal as-shipped script error is technical failure. After the single documented normalization, the run completes with remaining computational issues.
- Accepted manuscript, not publisher final version: September 1, 2020, 28 pages. Crossref verifies DOI/title/authors/year. Numeric differences might reflect manuscript/package drift; no existing reproduction report was consulted.
- Claim enumeration covers empirical numeric prose and main-figure point estimates/uncertainty/control means. Supplementary numeric cells are grouped as unavailable, not individually transcribed; historical dates, scale endpoints and cited-study statistics are outside computational scope.
- Recruitment, arrival and noncomplier records are not in the shipped data. The smaller baseline file cannot independently establish the full baseline-response count.
- Graphical matches use vector extraction with absolute tolerance 0.005 outcome units; close means a difference up to 0.01. They are not assertions of exact floating-point or image-byte identity. Text/label comparisons use half the last printed unit.
- No robustness or alternative-method analyses were designed. The original appendix includes author-supplied complete-case and ideology recoding analyses; these were executed solely as shipped code.
- The authors did not pin R/package versions. The local workflow uses R 4.6.1 and hash-pinned observed R packages, plus a genuine pixi.lock for Python/tool dependencies. Base R/lattice are supplied by the installed system distribution and not vendored.
- Public publication and the six nanopublication URIs remain incomplete; no human signature has been fabricated. An unpublished URN satisfies URI syntax but is not a delivered GitHub report or FLoRA submission.
- An initial DOI-only search returned unsolicited snippets for earlier reproduction reports. None was opened, downloaded or used in the analysis. Subsequent evidence came only from the manuscript, shipped package, bibliographic metadata and generic standards documentation.
