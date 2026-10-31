# Computational reproduction certificate

**Outcome: computational issues.** The principal correlations and individual-model rankings recur; specific numerical summaries and one pilot execution do not. This certificate makes no claim about scientific correctness.

Engine: T3 Code / Codex harness · model: gpt-6.1-sol · provider: OpenAI · rules: 1.0.0 · prompt/procedure: 0.1.0 · audit: 2026-10-30

Certificate: RC-2026-921 · DOI: [10.1177/09567976241251741](https://doi.org/10.1177/09567976241251741) · Original code/data: [OSF dexuy](https://osf.io/dexuy/).

## Outcome

The shipped main R analyses reproduce the principal correlations and individual-model rankings after documented lossless execution fixes. Experiment 2 participant shares and exclusion bookkeeping differ from the paper; Experiment 3 AIC values recur with the documented mixed-model specification, while its UPCO parameter and the third pilot execution differ. This local, AI-generated Reproduction Study assesses computation only; robustness is not checked.

35 grouped claims; 35 results: 12 close, 7 discrepant, 16 match.

The three main scripts complete after the documented execution normalizations. pilot1 and pilot2 complete; E3pilot stops before its model-comparison and power-analysis tail. Original source errors are recorded separately from successful normalized source runs; wrapper exit 0 alone is never treated as source completion.

## Main numerical evidence

| Quantity | Reported | Recomputed | Interpretation |
|---|---:|---:|---|
| E1 aggregate r: Bayes / UPCO / Competence | .92 / −.08 / .79 | .915954 / −.082131 / .789281 | Rounding matches |
| E1 paired participant tests | t(132)=13.68 / 4.19 | 13.681348 / 4.192008 | Matches |
| E2 aggregate r: Bayes / UPCO / Competence | .99 / .97 / .96 | .991057 / .971717 / .962253 | Rounding matches |
| E2 exclusions | 108 (33+72) | 105=33+72 | Difference −3 |
| E2 alternatives best by correlation / deviation | about 25% / 25% | 30.786026% / 38.209607% | Differences +5.786026 / +13.209607 percentage points |
| E3 Bayes best by correlation / deviation | 43% / 48% | 42.553191% / 48.085106% | Rounding matches |
| E3 UPCO mapping | .52 | .51 | Difference −.01 |
| Abstract total N | 886 | raw 1008; retained 826 | Mixed cohort bases in the reported total |

### Experiment 3 AIC specification

The main script uses `lm`. Its comments instruct the reader to substitute `lmer` and add random intercepts for participant and item to reproduce the supplementary mixed models. The five approximate paragraph values recur under that documented recipe with default REML:

| Predictor | Reported ≈ | Shipped default fixed effects | Documented mixed effects (REML) |
|---|---:|---:|---:|
| Proportion | 1722 | 3299.089276 | 1721.981455 |
| Prior | 922 | 1013.754109 | 922.169207 |
| Bayes | 410 | 463.147512 | 410.085803 |
| UPCO | 497 | 569.755113 | 497.266911 |
| Competence | 507 | 785.130034 | 506.927699 |

Individual-model rankings and the top Bayes-containing ensembles agree across specifications. The full ordering does not: C+U is worse than Bayes in the fixed-effects analysis (505.396935 versus 463.147512) but better in the documented mixed-effects analysis (399.297760 versus 410.085803). Thus the paper’s statement that the ordering does not change is only partially reproduced (C28). No alternate parameters were fitted to force agreement. This reruns the stated supplementary computation; it is not an added robustness analysis.

## Inputs, execution and environment

Host: macOS-26.7-arm64-arm-64bit. Authors’ analyses run in R 4.6.1. Workflow Python is 3.12.12; initial standard-library setup used Python 3.14.6. Pixi 0.83.0 and Snakemake 9.13.7 are installed inside the pilot directory. Full versions are in [environment.json](environment.json), [pixi.lock](pixi.lock), [R-environment.lock.json](R-environment.lock.json), and per-run sessionInfo files. All 150 contained R package binaries are pinned by version, source URL and SHA256. R itself and its bundled packages are host-provided.

The 18 shipped OSF files, original paper and public rules/schemas are hash-checked. Originals remain under `extracted/`; edits are made only to copies under `working/`. The lossless reshaping normalization preserves all 2,394 E1 values exactly after the original reverse coding. No exclusion, model equation, grid, optimization objective, test argument or data value was modified. Stochastic plotting is seeded. See `working/*/*/changes.diff` and [outputs/input-audit.json](outputs/input-audit.json).

The initial claim sheet incorrectly inferred analyzed sample sizes by subtracting exclusions from every reported N. It was corrected to the literal reported Ns and exclusion counts, preserving the initial sheet in `claims-initial.json` and explaining the correction in `claims-revision-note.md`. No comparison tolerance was widened.

## Findings

14 findings: 4 P0, 2 P1, 6 P2, 2 P3.

### NORM-001 · P3 · normalization

Hard-coded Windows or placeholder working directories prevent direct execution. Portable copies point to the untouched downloaded data directory.

Evidence: `extracted/analysis_scripts; logs/*-unmodified.log; working/*/*/changes.diff`

Suggested fix: Use project-relative data paths. No source data or statistical constants changed.

### NORM-002 · P0 · normalization

E1 and pilot1 create a named melt measure column but later request value and original trial names. Flattening the single measure family restores the expected schema losslessly.

Evidence: `logs/E1-portable.log; working/E1/normalized/changes.diff; outputs/input-audit.json proves exact equality for all 2,394 E1 observations.`

Suggested fix: Use a character measure.vars vector and the intended value column explicitly.

### NORM-003 · P0 · normalization

Current data.table rejects forwarding melt(data.frame(...)) to reshape2. E1/pilot1 compatibility copies explicitly namespace that same reshape2 method.

Evidence: `logs/E1-forwarding-check.log; working/E1/normalized/changes.diff`

Suggested fix: Use reshape2::melt for data.frame objects. No values or calculations changed.

### NORM-004 · P0 · normalization

pilot1 calls paired.r without importing psych. Its compatibility copy adds library(psych).

Evidence: `logs/pilot1-import-check.log; working/pilot1/normalized/changes.diff`

Suggested fix: Import psych explicitly. This restores the original called function, without changing its arguments.

### NORM-005 · P3 · normalization

Missing packages were installed locally. Hmisc was additionally required for the shipped bootstrap confidence-interval plotting functions. In-script package installation was moved into setup.

Evidence: `logs/R-restore.log; R-environment.lock.json; outputs/figures.complete.json`

Suggested fix: Ship an environment lock and explicit plotting dependencies. Pinned archives are retained locally; original environment versions were not supplied.

### DOC-001 · P2 · defect

E2 reports 108 exclusions, but the stated breakdown and shipped code both give 33+72=105.

Evidence: `C02; outputs/recomputed.json: E2.exclusion_audit`

Suggested fix: Correct the total to 105 and distinguish raw N=563 from retained N=458.

### NUM-001 · P1 · defect

E2 alternative models best capture 30.7860% by correlation and 38.2096% by deviation, versus about 25% reported.

Evidence: `C17-C18; outputs/recomputed.json: E2.best_*_counts`

Suggested fix: Regenerate the participant-share description from the named-model count table, or identify the input/version that produced the reported percentages.

### PLOT-001 · P2 · defect

E2 labels UPCO and Competence in the opposite order from the underlying melted model columns when constructing percplotd; its original chart remains unchanged in the reproduction.

Evidence: `extracted/analysis_scripts/E2_analysis.R:199 and 258-264; outputs/E2/portable/objects.RData`

Suggested fix: Use mods, whose order is Competence, UPCO, Bayes, as the plotting label order. Do not change the stored model predictions.

### DOC-002 · P2 · defect

Five E3 paragraph AICs recur under the documented mixed-effects REML recipe, while the default main analysis is fixed-effects lm and yields different AICs.

Evidence: `C21-C25; outputs/recomputed.json: E3.aic_fixed and E3.aic_mixed_REML`

Suggested fix: Identify the regression specification and REML setting beside every reported AIC, and export both documented analyses explicitly.

### NUM-003 · P2 · defect

E3 full model ordering changes under the documented mixed-model recipe: C+U moves from worse than Bayes to better than Bayes, although individual rankings and best Bayes-containing ensembles agree.

Evidence: `C28; outputs/recomputed.json: E3.aic_fixed and E3.aic_mixed_REML`

Suggested fix: Qualify the ordering-invariance statement and show both complete AIC tables. No statistical model was changed beyond the script-documented substitution.

### NUM-002 · P1 · defect

E3 shipped UPCO search selects .51, while Supplement A reports .52.

Evidence: `C30; extracted/analysis_scripts/E3_analysis.R:172-182; outputs/recomputed.json`

Suggested fix: State .51 for the shipped dataset/code, or provide the precise original data/software version that yields .52.

### RUN-001 · P0 · defect

The E3 pilot cannot execute its model-comparison/power tail because lmer is called without any random effects.

Evidence: `C32; logs/E3pilot-portable.log; outputs/E3pilot/portable/status.json`

Suggested fix: Authors should specify the intended model (lm or an explicit mixed formula). The reproduction does not guess a statistical correction.

### DOC-003 · P2 · defect

E1 aggregate comparison numbers recur as Fisher z statistics, although the text calls them t. Its UPCO p-value rounds to .75 as in the text but Fig.3 prints .74.

Evidence: `C05, C07-C08; outputs/recomputed.json: E1.aggregate_comparisons`

Suggested fix: Correct the statistic label and use consistent p-value rounding; retain the original test specification explicitly.

### DOC-004 · P2 · defect

The abstract N=886 combines retained E1/E2 cohorts with the raw E3 cohort. Shipped files contain 1,008 raw completed responses and 826 retained participants.

Evidence: `C31, C33-C35; outputs/input-audit.json`

Suggested fix: Use a consistent raw or analyzed sample basis and report per-study enrollment/exclusions/retained counts.

## Per-claim audit

“Match” means the stated rounding/ordering/test threshold recurs. “Close” flags an explicit approximate band, a label/coding convention, or a value recovered only under another documented specification. “Discrepant” means the declared comparison fails. Every computed value, numeric gap and algorithm is recorded in [certificate.json](certificate.json) and [outputs/recomputed.json](outputs/recomputed.json).

| Claim | Status | Claim / location |
|---|---|---|
| C01 | close | Experiment 1 reports N=133 and 17 exclusions — p.1012 |
| C02 | discrepant | Experiment 2 reports N=458 and 108 exclusions, broken down as 33 + 72 — p.1014 |
| C03 | match | Participant counts — p.1017 |
| C04 | match | Bayes correlation with the 18 mean judgments — p.1014; Fig.3 |
| C05 | close | UPCO correlation with the 18 mean judgments — p.1014; Fig.3 |
| C06 | match | Competence correlation with the 18 mean judgments — p.1014; Fig.3 |
| C07 | close | Bayes versus UPCO aggregate correlation comparison — p.1014 |
| C08 | close | Bayes versus Competence aggregate correlation comparison — p.1014 |
| C09 | match | Bayes has the largest mean participant-level correlation — p.1015; Fig.3b |
| C10 | close | Bayes best captures about 75% of participants by correlation — p.1014 |
| C11 | close | Bayes best captures about 80% of participants by absolute deviation — p.1014 |
| C12 | match | Bayes correlation with mean judgments across 225 stimuli — Fig.4a, p.1017 |
| C13 | match | UPCO correlation with mean judgments across 225 stimuli — Fig.4a, p.1017 |
| C14 | match | Competence correlation with mean judgments across 225 stimuli — Fig.4a, p.1017 |
| C15 | match | Bayes has the lowest AIC among individual models — Fig.6a, p.1019 |
| C16 | match | Ensembles outperform individual models; Competence adds more to Bayes than UPCO — pp.1016-1017; Fig.6a |
| C17 | discrepant | Alternative models best capture about one quarter of participants by correlation — p.1017; Fig.6b |
| C18 | discrepant | Alternative models best capture about one quarter of participants by deviation — p.1017; Fig.6b |
| C19 | match | Bayes has the lowest AIC among individual models — p.1020; Fig.8a |
| C20 | match | Ensembles improve on Bayes and Bayes+Competence has the best AIC — pp.1020-1021; Fig.8a |
| C21 | close | AIC for a proportion-only predictor is approximately 1722 — p.1021 |
| C22 | close | AIC for a prior-only predictor is approximately 922 — p.1021 |
| C23 | close | AIC for Bayes is approximately 410 — p.1021 |
| C24 | close | AIC for UPCO is approximately 497 — p.1021 |
| C25 | close | AIC for Competence is approximately 507 — p.1021 |
| C26 | match | Bayes best captures 43% of participants by correlation — p.1021 |
| C27 | match | Bayes best captures 48% of participants by absolute deviation — p.1021 |
| C28 | discrepant | Adding participant and item random intercepts preserves the main model ordering — p.1020; Figs.S12-S13 |
| C29 | close | The UPCO grid-search optimum is .51 — Supplement A p.4; pilot1_analysis.R |
| C30 | discrepant | The UPCO grid-search optimum is .52 — Supplement A p.4; E3_analysis.R |
| C31 | discrepant | Total sample size in the abstract — p.1010 |
| C32 | discrepant | The Experiment 3 pilot script executes its model comparison and power analysis — E3pilot_analysis.R lines 238-260 |
| C33 | match | E1 demographic counts and mean age — p.1012 |
| C34 | match | E2 demographic counts and mean age — p.1014 |
| C35 | match | E3 demographic counts and mean age — p.1017 |

## Fresh rebuild verification

A fresh copy began with no original inputs, R library, Pixi environment or download cache. It downloaded and SHA256-verified all inputs, restored the locked environments and completed all eight workflow rules. Both schemas passed. All 222 recomputed numeric scalars and the complete recomputed.json byte hash match the first run exactly. This check used the same host and a copied Pixi 0.83.0 bootstrap executable. See [outputs/fresh-rebuild-check.json](outputs/fresh-rebuild-check.json) and logs/fresh-rebuild.log.

## Rule URLs and provenance

The original prompt URLs at `https://lukasroeseler.github.io/reprocrowd/` returned HTTP 404. The user corrected them to `https://forrtproject.github.io/reprocrowd/crowd-repro/RULEPACK-v1.0.0.md` and the `schemas/` folder. The retrieved schemas retain the older `$id`; validation uses their live, hash-recorded bytes. Both schemas are applied with a Draft 2020-12 validator and URI/date format checking. Retrieval failures and replacement hashes are preserved under `rules/`.

Only the original paper, its shipped OSF data/code/materials, public ReproCrowd instructions/schemas and generic FORRT vocabulary documentation were consulted. No existing reproduction, replication or verification report of this paper was searched, opened or used. No credentials, email addresses or participant identifiers were submitted to an external service.

## Limits and delivery

- No robustness or sensitivity analysis was performed; scientific correctness was not assessed. outcome_robustness is not checked.
- The main reported statistics and selected pilot/execution checks are enumerated in 35 grouped claims. This is not an exhaustive numerical audit of all supplementary figures, simulation outputs or preregistrations. No approval wait was needed under the pilot instruction.
- The publisher supplement was initially visible through web retrieval, including Supplement A model-implementation details, but direct local PDF download returned HTTP 403 and later web retrievals failed. No local supplement PDF is bundled. Only its inspected .51/.52 implementation statements were used.
- No original R/package version or lockfile was shipped. All used versions are recorded; source-era version drift cannot be measured. No alternative cognitive-model parameters were substituted.
- R 4.6.1 and bundled/core R packages are host-provided. Pixi pins Python/workflow dependencies; R-environment.lock.json pins 150 locally installed CRAN binaries with SHA256. A same-host rebuild from empty input, package-library, Pixi-environment and download-cache directories was tested where documented in outputs/fresh-rebuild-check.json. Future CRAN/OSF availability and other hosts are not guaranteed.
- Original data/code and local RData snapshots remain private local inputs. No original data/code or participant identifiers were uploaded. Download scripts link to and hash-check the original sources.
- The pilot is local-only: no GitHub repository, release DOI, FLoRA submission or signed nanopublications were published. Required URI fields use an explicit urn:reprocrowd:unpublished identifier rather than a fictitious public URL. The FLoRA record is a schema-valid local draft, not ready for import until its publication URL exists.
- Human review/signature is pending in SIGN-OFF.md. Nanopublication drafts use verified FORRT vocabulary but have no signed/published chain URIs.
- The prompt originally supplied broken lukasroeseler.github.io URLs (HTTP 404). The user supplied live forrtproject.github.io replacements; those rule pack/schema bytes and hashes are preserved locally.
- Bootstrap/jitter plotting is seeded for reruns. No exact-pixel or exact-bootstrap-CI equivalence to the paper is claimed. The MyST configuration is supplied; a MyST site build was not performed.

The FORRT chain is prepared locally with `Reproduction Study`, `model performance`, `PartiallySupported`, `HighConfidence`, and `cito:qualifies`; the computational outcome is exactly `computational issues` and `outcome_robustness` is `not checked`. [nanopubs/PUBLISHED.md](nanopubs/PUBLISHED.md) explicitly records that no chain URI exists. [SIGN-OFF.md](SIGN-OFF.md) is the sole human sign-off file.

## Bundle validation

Both certificate.json and flora-entry.json pass the downloaded public JSON Schemas using Draft 2020-12 with URI/date format checking. All 15 required artifact types are present; claim/result cross-references, source checksums, R archive checksums and source-run completion states pass internal checks. Publication and human sign-off remain incomplete. See validation.json.
