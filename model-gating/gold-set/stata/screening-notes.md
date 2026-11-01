# Stata candidate screening

Screened 1 November 2026. **34 papers screened, 17 provisionally eligible, 17 excluded.** This is a screening pool for a possible stratified draw of about 10 papers. No random draw, claim list, claim labels, severity assignments, or final paper verdicts were made. All downloads and working scripts are in `/tmp/scratch_stata/`, outside the repository. No Stata installation or analysis execution was attempted.

## Counts and interpretation

| Discovery source | Individually screened | Eligible | Excluded | Reproducible | Computational issues | Partial technical-failure reserve |
|---|---:|---:|---:|---:|---:|---:|
| REPRO-Bench packages | 31 | 16 | 15 | 13 | 2 | 1 |
| I4R catalogue / earlier audit | 3 | 1 | 2 | 1 | 0 | 0 |
| Total | 34 | 17 | 17 | 14 | 2 | 1 |

The last three columns count eligible papers only. There are no eligible ambiguous-stratum candidates. The technical-failure entry is conditional: **RB-031 has a documented missing appendix computation, while its main regressions reproduce from the deposited processed data.** If the eventual targets omit the unavailable appendix, it belongs in the reproducible stratum. Thus this pool supports reproducible and issue cases with reserves, but does not establish a full quota of clean technical failures. Even setting RB-031 aside leaves 16 candidates, above the requested minimum of 15.

Discovery source is not independent human verification. **All 17 eligible papers use I4R human evidence**, including the 16 found through REPRO-Bench. No independent SCORE or CODECHECK additions were established. Do not describe these as 17 independent replication programmes or use the REPRO-Bench scores as gold outcomes.

Translation judgement among eligible candidates:

- straightforward: 5.
- needs care: 9.
- specialised: 3.

These judgements describe the observed code, not verified numerical equivalence. Straightforward candidates use ordinary linear/survey models and familiar inferential calculations. Candidates marked needs care have important defaults, contrasts, auxiliary algorithms, or specialised appendix analyses. Specialised candidates need estimator-level work and are higher-effort reserves. None has been translated or executed here.

Six eligible packages do not disclose an original target Stata version in the inspected code/documentation: RB-020, RB-022, RB-031, RB-050, RB-067, and I4R-rcngs. RB-067's report ran Stata 17, which is recorded as a reproducer environment, not an inferred original target. This is an explicit screening limitation rather than an invented version requirement. Eleven eligible packages have a target/last-run version statement.

Two eligible packages ship Stata execution logs: RB-040 and RB-071. Their files are named below. No log was found in the inspected inventories for the other eligible packages. Generated log commands do not demonstrate that a log was deposited. HTML, DOCX, PDF, TeX tables, and TeX compilation logs were not counted as Stata logs.

## Method and sources

I reused the criteria, CSV fields, and provisional-outcome distinctions in the original `../README.md`, `../candidates.csv`, `../screening-notes.md`, and retained `../audit/screening/` records. I read benchmark `../../benchmark/SPEC.md`, especially the Stata targets and justified-fix requirements. The original 22 columns, including `round`, are retained in order; `stata_version`, `user_commands`, `translatability`, `translatability_notes`, and `ships_logs` are appended. All rows have `round=stata-1` and keep existing candidate IDs where applicable.

I used the earlier I4R report and papers catalogues, the HF package inventory, and earlier Stata exclusions as discovery aids. I then reopened the actual public reports, downloaded article PDFs, and inspected original do-files, readmes, ado source where deposited, logs, and archive inventories. Existing eligibility judgements were not carried over automatically. Notably, the original-language exclusion now disappears for I4R-rcngs, but the larger mixed-software and runtime problems in I4R-hxadk remain.

Sources searched or opened:

- [REPRO-Bench official code repository](https://github.com/uiuc-kang-lab/REPRO-Bench), [dataset](https://huggingface.co/datasets/chuxuan/REPRO-Bench), and [benchmark article](https://aclanthology.org/2025.findings-acl.1210.pdf). Package inspections use the previously recorded immutable HF snapshot `74958fba32daeacff51f2e1fd37be3916595648f`, with fresh recursive per-task API inventories. Only the 31 individually inspected tasks have candidate rows; scanning catalogue filenames to identify leads is not counted as full paper screening. The publication's runtime inclusion criterion is secondary support where an individual package has no timing; it is not a laptop measurement.
- I4R [reports](https://www.i4replication.org/reports) and [discussion papers](https://www.i4replication.org/papers), using the earlier local catalogue snapshots to find matches. EconStor PDFs were recovered from opened RePEc records; public OSF report URLs were reopened. Each row names its actual report, not merely a catalogue status. Newly downloaded report hashes are retained in the CSV or provenance index below.
- [SCORE process and source routes](https://www.cos.io/score-process) and [evidence page](https://www.cos.io/score-evidence), plus the earlier SCORE screening summary. The targeted search did not produce an additional original Stata package with a verified 5-8-result human trail in this pass. I did not redo the full SCORE analyst-archive screen or count its previous non-Stata papers as newly screened candidates.
- [CODECHECK register](https://codecheck.org.uk/register/) and a targeted Stata/certificate search. No additional suitable original Stata social-science package and numerical human-comparison trail was recovered. This is a bounded search, not evidence that no such certificate exists.
- Crossref records were requested for article identifiers read in the downloaded PDFs. Some endpoints did not return usable matches. A DOI in the CSV either appears in the opened original article, or, for retained original-audit rows, was already verified there. No DOI was constructed from a title. For example, RB-078's first DOI in the PDF is the data deposit, so the article DOI later in that PDF is used instead. Row notes distinguish successful Crossref matching from verification against the article itself.

Eligibility required publicly accessible original analysis inputs and an original `.do` estimation workflow, social/behavioural subject matter, deposited package size below 5 GB, a credible original runtime below about two hours, and a human report assessing enough numerical material for a likely 5-8-result mapping. Feasibility is recorded at exhibit level without selecting claims. Public processed inputs are acceptable starting data when the original package and human report use them; absence of their upstream raw source is documented. This does not permit replacing a required confidential dataset or recreating a scientifically different model.

For each eligible HF package I made a fresh unauthenticated data-file byte-range access check, in addition to its public inventory and documentation. These checks confirm access, not the entire dataset's integrity. I did not download every large data file, notably the 1.32 GB RB-020 dataset. Live OSF root/folder metadata and original files were fetched for I4R-rcngs and I4R-hxadk. All such requests omitted personal email addresses; no private-data requests or service registration were made.

`package_size_mb` is the sum of deposited files inside `replication_package`, in decimal MB, excluding the task-level article PDF and benchmark instruction file. This differs deliberately from the earlier HF summary, which sometimes totalled the entire task. It includes deposited rendered outputs and duplicate ZIP copies; it is not an expanded archive or minimal-input size. No eligible inventory reached the API's 1,000-entry limit. Small embedded ZIPs for RB-034, RB-068, and I4R-hxadk were opened to look for additional code/logs. The inspected archives are small enough that expansion does not approach the 5 GB cap.

`user_commands` records user-written commands directly invoked or installed, observed bundled helper programs, and identified immediate dependencies. I checked calls as well as installer lines: RB-041 calls coefplot without installing it; RB-062 uses esttab despite its short README dependency list; RB-067 calls sdecode without an installer. No Stata or SSC installation was performed, so these are **static dependency inventories, not a solved, version-pinned transitive dependency environment**. Some excluded packages were stopped before a full dependency audit. Unknown providers are named explicitly rather than silently omitted. A draw/package-preparation stage still needs to resolve and pin the listed dependencies.

Original-computation strata follow the human report's unchanged-code comparisons. Corrected coding, new clustering, added controls, alternative data, and robustness analyses do not themselves establish computational issues. A named missing input/code path can support a partial technical-failure lead; an unavailable web endpoint or a coarse benchmark rating cannot. Claims remain unlabelled, and the `close` versus `discrepant` distinction for reported slips is left for the approved labelling rules.

## Eligible candidates and candidate-specific cautions

The following entries describe evidence and mapping feasibility, not a claim list. Links point to the opened human reports and immutable package inventories.

### RB-054: Winter is Coming: Early-life Experiences and Politicians’ Decisions

**Provisional stratum:** computational issues. **Translation:** needs care. **Package:** 24.062 MB. **Runtime:** README: about 10 min.

[Human report](https://www.econstor.eu/bitstream/10419/302899/1/I4R-DP155.pdf); [original package or public mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/54/replication_package). DP 155, section 2, documents original-code numerical discrepancies in Tables B4, C1 and C7, while otherwise reproducing the analysis-data results. The reported B4 coefficient/SE pair differs, and C7 has an order-of-magnitude R-squared typo.

**Stata version:** 17.0 SE (README). **User-written dependencies:** logout; reghdfe; ftools (reghdfe dependency); outreg2; coefplot; bundled ols_spatial_HAC.

Main reghdfe maps to fixest with the same effects, clusters and degrees of freedom. A custom ols_spatial_HAC program appears in the appendix and must be ported literally if its SE claims are chosen; a generic Conley routine is not an exact replacement. Distinguish this from ordinary clustered main-table estimates.

The report labels several discrepancies typing/rounding errors. Their eventual close/discrepant treatment is deliberately unresolved here. Correcting the same-prefecture interaction is a different analysis and is not the reason for the issue stratum.

**Mapping feasibility:** The report covers the main Tables 2-4 and named appendix discrepancies, supporting a mixed 5-8-result mapping without using corrected prefecture coding.

### RB-067: State Action to Prevent Violence against Women: The Effect of Women’s Police Stations on Men’s Attitudes toward Gender-Based Violence

**Provisional stratum:** computational issues. **Translation:** specialised. **Package:** 0.244 MB. **Runtime:** estimated 15-120 min; small data but many mixed models; source inclusion <2 h.

[Human report](https://www.econstor.eu/bitstream/10419/276961/1/I4R-DP067.pdf); [original package or public mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/67/replication_package). DP 67, section 3 and Appendix Table A1, compares unchanged-code Table 1 output with print and identifies three sign reversals, plus further third-decimal differences. A graph filename typo only overwrites an output and is not the numerical issue.

**Stata version:** target not stated in .do; human report reran in 17. **User-written dependencies:** estout (eststo); parmest; eclplot; psmatch2 (pstest); sdecode.

Core meologit mixed ordered-logit and appendix melogit require matching likelihood, ordinal thresholds, quadrature nodes, optimiser, covariance and inference. ordinal::clmm/lme4 are possible implementation bases, not certified exact replacements. This affects the Table 1 issue evidence itself. margins expression(predict(mu fixedonly outcome(5))) and contrast(effects overjoint) affect Figures 2-4. psmatch2 matching/ties affect additional models.

Strongest sign-error evidence, but a high-effort translation reserve. The observed sdecode call is absent from the script installer. No target Stata version was inferred from the reproducer version.

**Mapping feasibility:** Original Table 1 and report Appendix A1 provide a complete coefficient/SE comparison across eight models.

### I4R-rcngs: Gender Differences in Climbing up the Ladder: Why Experience Closes the Ambition Gender Gap

**Provisional stratum:** computationally reproducible. **Translation:** needs care. **Package:** 21.136 MB. **Runtime:** estimated 5-60 min from scripts and data size; not timed.

[Human report](https://osf.io/download/wh7dx/); [original package or public mirror](https://osf.io/w8e35/). The report reproduces all Study 1 main results and all preregistered Study 2 results from raw and analysis data without sign, magnitude or significance discrepancies.

**Stata version:** not stated in original .do or inspected package documentation. **User-written dependencies:** none observed in original Stata component.

Original Stata cloglog with state indicators and respondent-clustered covariance maps to glm(binomial(link="cloglog")) plus clustered sandwich covariance. Preserve the polynomial interaction, finite-sample scaling and margins atmeans. The other study and original cleaning are in R; this is a mixed package with a genuine Stata estimation workflow.

Live OSF file inventory: 16 public files, 21.136 decimal MB. The original study1_marginsplot_stata_code.do contains a cloglog model and margins atmeans; it asks for a .dta while a matching cleaned CSV is deposited, so lossless format import must be recorded. The source Tables 5/6/7 compare multiple original Study 1 model coefficients and inference results, enough for 5-8 numerical claims without relying on the R-only Study 2. No claim list or final labels made. HTML and DOCX rendered outputs ship, but no Stata execution log was found.

### RB-007: Campaign Contributions and Roll-Call Voting in the U.S. House of Representatives: The Case of the Sugar Industry

**Provisional stratum:** computationally reproducible. **Translation:** needs care. **Package:** 0.430 MB. **Runtime:** estimated 5-30 min; static inspection; REPRO-Bench inclusion <2 h.

[Human report](https://www.econstor.eu/bitstream/10419/275682/1/I4R-DP057.pdf); [original package or public mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/7/replication_package). DP 57, section 2 and section 3.1/Table 1, reports successful reproduction of the original models and figures. Inconsistent accents in names do not affect the correctly coded incumbent indicator.

**Stata version:** 15 (first line of original .do). **User-written dependencies:** marhis.

Main logit has an R binomial-GLM equivalent with explicit district/incumbent indicators and sandwich robust covariance. Reproduce Stata perfect-prediction exclusions and finite-sample scaling; the report notes different automatic sample dropping in R. marhis affects marginal-effect figure calculations/formatting and needs an explicit delta-method translation.

APSR Replication Codes.do lines 1, 24, 32 onward. Do not call clustered-SE robustness models the unchanged-code reference.

**Mapping feasibility:** Table 1 district/incumbent logit models and the corresponding report comparison table provide more than five numerical results without using altered specifications.

### RB-013: Checking and Sharing Alt-Facts

**Provisional stratum:** computationally reproducible. **Translation:** needs care. **Package:** 5.343 MB. **Runtime:** README: less than 10 min.

[Human report](https://www.econstor.eu/bitstream/10419/271674/1/I4R-DP034.pdf); [original package or public mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/13/replication_package). DP 34 confirms the original O analysis reproduces exactly under Stata 16.1. Its Tables 1, 2A and 2B compare published estimates to original-code output; the Stata 17 variant changes the Table 2C sample.

**Stata version:** 16.1; report contrasts 17. **User-written dependencies:** estout (esttab, eststo, estadd, estpost); cibar; grc1leg (st0085_2); outreg2.

Main treatment OLS and xtreg fixed effects are expressible with lm/fixest and the original variance corrections. Adaptive lasso selection with rseed(1234) has no automatically exact glmnet replacement: affected Table A5/A7 and downstream predicted-versus-actual Table 2C/Table A6 calculations must be traced. Do not replace version-sensitive selection by a convenient R lasso.

Master_replication_HZG.do installs packages; README states version and runtime. Distinguish the original O columns from V/S/L/C robustness columns.

**Mapping feasibility:** Main Table 2 treatment estimates and report Tables 1/2A/2B support a 5-8-result mapping.

### RB-020: Does Competence Make Citizens Tolerate Undemocratic Behavior?

**Provisional stratum:** computationally reproducible. **Translation:** needs care. **Package:** 1324.441 MB. **Runtime:** estimated 15-120 min from code and source inclusion <2 h; not timed.

[Human report](https://www.econstor.eu/bitstream/10419/270858/1/I4R-DP028.pdf); [original package or public mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/20/replication_package). DP 28, section 2, says the analysis script and all tables/figures reproduce without coding issues. Figure 1 and Appendix A Tables A1/A2 reproduce exactly in Stata and R. The raw-data cleaning script cannot run because raw inputs are not deposited.

**Stata version:** not stated in shipped ReadMe.txt or analysis scripts. **User-written dependencies:** estout (eststo, esttab); coefplot; grc1leg.

The shipped Analysis.do uses OLS with respondent-clustered inference and margins contrast(effects). R lm/fixest and explicitly constructed marginal contrasts can implement this model. Preserve reference category 3, averaging, contrasts, cluster scaling and original sample. Power.R is ancillary power analysis, not the Stata estimates.

Starting point is deposited dataset.dta, about 1.32 GB. Missing raw data are an upstream limitation, not an automatic failure of the original analysis-data workflow. Full data were not downloaded; a public byte-range request succeeded.

**Mapping feasibility:** Figure 1 and Appendix A Tables A1/A2 contain multiple country-specific conjoint contrasts and coefficients assessed in the report.

### RB-022: Does Public Opinion Affect the Preferences of Foreign Policy Leaders? Experimental Evidence from the UK Parliament

**Provisional stratum:** computationally reproducible. **Translation:** straightforward. **Package:** 0.024 MB. **Runtime:** estimated 1-10 min; tiny survey; source inclusion <2 h.

[Human report](https://osf.io/download/8jx43/); [original package or public mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/22/replication_package). The public Chu and Recchia report, section 3.1, explicitly says all numerical results in Online Appendix Tables 1 and 2 reproduced exactly using the shipped data and original weights. Unweighted analyses are separate robustness checks.

**Stata version:** not stated in shipped .do; report gives R version only. **User-written dependencies:** none observed; survey commands are built in.

svyset and svy: regress map to the R survey package, as demonstrated by the human reproducer. Keep pweights, strata/PSU declaration, survey degrees of freedom and missing-value handling. No user-written estimator was found.

JOP_ChuRecchia_ReplicationStataCode.do is the original analysis. Weight construction is poorly documented, but the actual deposited weights define Track A computation.

**Mapping feasibility:** Appendix Tables 1/2 supply weighted group percentages, differences and survey regression results, with report comparison tables.

### RB-026: Evaluating Deliberative Competence: A Simple Method with an Application to Financial Choice

**Provisional stratum:** computationally reproducible. **Translation:** straightforward. **Package:** 27.820 MB. **Runtime:** README: under 10 min.

[Human report](https://www.econstor.eu/bitstream/10419/289580/1/I4R-DP110.pdf); [original package or public mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/26/replication_package). DP 110, section 2.1, states the provided code is functional and produces the original results. Its focus is original Tables 4 and 7 and Figure 4. Changes to the squared-distance metric, clustering and switcher exclusions are subsequent robustness exercises.

**Stata version:** 16 (README). **User-written dependencies:** outreg2; distplot.

Main regressions use reg, clustered inference, lincom and test, with lm/fixest and linear Wald contrasts as R equivalents. qreg appears in the wider script and needs the same quantile, covariance and sample conventions if used. distplot/outreg2 concern display/export.

Analysis.do and README agree that controlled randomness is not used. Do not treat replacing the squared-distance measure as unchanged-code non-recurrence.

**Mapping feasibility:** Original Tables 4/7 and report baseline comparisons have enough assessed treatment coefficients and inference results.

### RB-034: Hobo Economicus

**Provisional stratum:** computationally reproducible. **Translation:** straightforward. **Package:** 0.759 MB. **Runtime:** README: less than 5 min; reported computation 2 min.

[Human report](https://www.econstor.eu/bitstream/10419/274554/1/I4R-DP055.pdf); [original package or public mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/34/replication_package). DP 55, section 2.1, reports that the original Stata package easily reproduces every table and figure with the same contents as the paper. Section 2.2 separately checks the computations in R.

**Stata version:** 16 (README, last run November 2021). **User-written dependencies:** stripplot; outreg; labutil (labmask, varlabel).

OLS, oneway ANOVA, t/distribution calculations and variance tests have direct mathematical R implementations. Preserve Stata group definitions, ANOVA weighting and test degrees of freedom. The report discusses details of the R ANOVA implementation separately from original-code reproduction.

Nested replicate.zip was opened as well as the expanded tree. It contains another copy of the do/data files, not hidden execution logs. Size includes this deposited duplication.

**Mapping feasibility:** Main Tables 1/2 and Table 4 ANOVA include assessed means, OLS coefficients and test statistics suitable for a 5-8-result mapping.

### RB-040: Interventions and Cognitive Spillovers

**Provisional stratum:** computationally reproducible. **Translation:** straightforward. **Package:** 16.849 MB. **Runtime:** README: less than 10 min.

[Human report](https://www.econstor.eu/bitstream/10419/272845/1/I4R-DP043.pdf); [original package or public mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/40/replication_package). DP 43 says all main findings reproduce using the original Stata code and are verified in R. Section 5 provides numerical comparisons for the main experimental findings.

**Stata version:** 15 (README). **User-written dependencies:** estout (eststo, estadd, esttab, estpost); coefplot; cdfplot; bundled convert program.

Main reg models and clustered/robust tests map to lm/fixest and sandwich covariance. estout, coefplot and cdfplot are export/plot helpers. The shipped library also contains unused estimators; their presence does not mean the main models use them.

Six original analysis .log files are in EmpiricalAnalysis/out. Preserve these as evaluator references and strip from model bundles. README includes oTree experiment software, which is not needed to analyse already deposited observations.

**Mapping feasibility:** Main attention, decision quality, spillover and payoff tables, cross-referenced by report section 5, offer more than five assessed numerical results.

**Shipped Stata logs:** `40/replication_package/EmpiricalAnalysis/out/4_1_Allocation_Attention.log; 40/replication_package/EmpiricalAnalysis/out/4_1_Passive_Behavior.log; 40/replication_package/EmpiricalAnalysis/out/4_2_Cognitive_Spillover.log; 40/replication_package/EmpiricalAnalysis/out/4_2_Interventions_targeted_domain.log; 40/replication_package/EmpiricalAnalysis/out/4_3_Payoffs_And_Efficiency.log; 40/replication_package/EmpiricalAnalysis/out/Randomization_Check.log`.

### RB-041: Jumping the Gun: How Dictators Got Ahead of Their Subjects

**Provisional stratum:** computationally reproducible. **Translation:** needs care. **Package:** 110.872 MB. **Runtime:** README: data preparation 30-60 min; main results <5 min; appendix 5-10 min.

[Human report](https://www.econstor.eu/bitstream/10419/274140/1/I4R-DP050.pdf); [original package or public mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/41/replication_package). DP 50, section 2 and original-result exhibits in section 3, describes a complete annotated package with minor relative-path inconsistencies. It reprints the original main models before alternative weighting and leave-one-out analyses.

**Stata version:** 15 (README). **User-written dependencies:** ranktest; xtabond2; ivreg2; reghdfe; ivreghdfe; ftools (reghdfe dependency); outreg2; plausexog; coefplot.

Main reghdfe/ivreghdfe OLS and 2SLS map to fixest, with matched singleton dropping, absorption and small-sample corrections. Appendix xtabond2 and plausexog have no established drop-in exact R translation in this screen: flag any dynamic-panel/GMM or plausibly exogenous bounds claims. No randomisation-inference result from the reproducer is an original target.

1_jtg_install_packages.do is incomplete as an exhaustive dependency declaration: coefplot is called later but not installed there. DP 50 randomisation-inference timings concern the new robustness exercise, not original runtime.

**Mapping feasibility:** Main reduced-form/IV results and the source reprinted original Tables 2/3 provide enough assessed coefficients and inference statistics.

### RB-048: Motivated Beliefs and Anticipation of Uncertainty Resolution

**Provisional stratum:** computationally reproducible. **Translation:** straightforward. **Package:** 8.929 MB. **Runtime:** estimated 5-30 min; source inclusion <2 h; not timed.

[Human report](https://www.econstor.eu/bitstream/10419/276253/1/I4R-DP065.pdf); [original package or public mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/48/replication_package). DP 65, section 2, reports that the original cleaning and analysis scripts produce the paper tables and figures without coding errors. Its Table 1 is an analytical literature classification rather than a numerical model output.

**Stata version:** 15 (README). **User-written dependencies:** estout (eststo, esttab).

Main OLS/ttest and clustered reg specifications have direct lm/fixest/sandwich equivalents. Preserve subject/session clustering and treatment interactions. eststo/esttab export results and do not change the estimator.

Data_creation.do reads the public session spreadsheets. Robustness exclusions of probabilistically inconsistent subjects are not computational discrepancies.

**Mapping feasibility:** Experimental belief-updating regression tables and the corresponding human report cover more than five numerical results.

### RB-050: Not All Elections Are Created Equal: Election Quality and Civil Conflict

**Provisional stratum:** computationally reproducible. **Translation:** specialised. **Package:** 1.621 MB. **Runtime:** estimated 5-60 min; source inclusion <2 h; not timed.

[Human report](https://osf.io/download/8xrkt/); [original package or public mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/50/replication_package). The public Donno, Morrison and Savun report, section 2 and Appendix I, reproduces original Table 2 and Figures 1/2 and explicitly finds no differences or computational errors.

**Stata version:** not stated in the shipped replication.do. **User-written dependencies:** firthlogit; coefplot; sutex2; cem (imb).

Standard clustered logit maps to glm/fixest. Main firthlogit needs a faithful Firth penalised-likelihood implementation, for example logistf with inference settings checked, rather than ordinary logit. ivprobit in Table 2 model 6 is not 2SLS or ordinary probit. Figure 1/2 use margins expression(invlogit(predict(xb))) and require an exact derivation; do not assume a generic marginaleffects call matches. cem/imb affect appendix matching.

Higher-effort reserve because core claims involve penalised logit and nonlinear margins. The method has R implementations, but numerical equivalence has not been established by this static screen.

**Mapping feasibility:** Table 2 includes several original model specifications and the report Appendix I provides numerical evidence sufficient for 5-8 results.

### RB-062: Run-off Elections in the Laboratory

**Provisional stratum:** computationally reproducible. **Translation:** needs care. **Package:** 133.165 MB. **Runtime:** README: tables 89 seconds; figures 67 seconds.

[Human report](https://www.econstor.eu/bitstream/10419/281134/1/I4R-DP099.pdf); [original package or public mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/62/replication_package). DP 99 reports that re-executing the authors Stata scripts reproduces all tables and figures with no coding errors or discrepancies. The reproducer independently checks the cleaned data against the raw zTree output.

**Stata version:** 15.1 MP Windows; 14.1 MP macOS (README). **User-written dependencies:** coefplot; estout (esttab).

Many xtreg calls omit fe, so these are default random-effects models, not fixed effects. Translate the GLS variance-component estimator and clustered covariance explicitly, using an appropriate plm implementation only after matching Stata defaults. Ordinary reg results are direct. Do not mechanically replace these xtreg calls with fixest fixed effects.

README only names coefplot, but the scripts also use esttab. BGLM_Tables.do sets a seed; any simulation-derived theoretical figure needs a separate RNG audit. Deposited experimental observations permit the core regressions.

**Mapping feasibility:** Main voting-system regression tables and source baseline comparisons cover multiple treatment and coordination outcomes, sufficient for 5-8 results.

### RB-068: Student Performance, Peer Effects, and Friend Networks: Evidence from a Randomized Peer Intervention

**Provisional stratum:** computationally reproducible. **Translation:** specialised. **Package:** 22.825 MB. **Runtime:** README: nearly 2 h with Stata MP two cores; borderline upper limit.

[Human report](https://www.econstor.eu/bitstream/10419/289581/1/I4R-DP111.pdf); [original package or public mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/68/replication_package). DP 111, section 2, explicitly says the provided package is computationally reproducible in Stata 14, 17 and 18. Altering Big Five coding, controls and peer specifications belongs to the later robustness analyses.

**Stata version:** 16 (README); report tested 14, 17 and 18. **User-written dependencies:** outreg2; moulton (bundled brl helper); randcmd; rwolf; nwcommands (nwset, nwqap); pairdata.

Main OLS coefficients map to lm/fixest, but moulton adjusted covariance needs the actual bundled formula. randcmd/rwolf randomisation and multiplicity output and appendix nwqap permutation p-values have no guaranteed identical R random streams. The script explicitly notes nwqap cannot set a seed. Flag affected adjusted p-values/network appendix results; deterministic OLS coefficients are lower risk.

Moulton.zip and nwqaq.zip were downloaded and opened. They contain ado source, with no logs. nwset is from the bundled nwcommands collection. pairdata is called in the appendix and its provider was not verified. Gephi 0.92 only makes the network picture. Runtime is at the threshold and must be confirmed before a draw.

**Mapping feasibility:** Main achievement, personality and peer-effect Tables 2-5 and report baseline comparisons support a 5-8-result mapping.

### RB-071: Teaching Norms: Direct Evidence of Parental Transmission

**Provisional stratum:** computationally reproducible. **Translation:** needs care. **Package:** 6.301 MB. **Runtime:** README: less than 1 min.

[Human report](https://www.econstor.eu/bitstream/10419/286490/1/I4R-DP106.pdf); [original package or public mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/71/replication_package). DP 106 distinguishes original reproduction from modified controls/imputation. Section 3 says original results recur with the original controls and without the reproducer imputation; its own changed estimates are not original-code failures.

**Stata version:** 17.0; version 16 prefix for one legacy table (README and .do). **User-written dependencies:** estout (eststo, estadd, estpost, esttab).

Main OLS, logit and linear margins map to lm/glm/fixest with school-clustered inference; ranksum/signrank must use Stata tie and exact/asymptotic rules. Appendix Table A14 uses cmrologit incomplete(99) reverse with robust inference: not an ordinary multinomial logit, and a Plackett-Luce/rank-ordered implementation must match its likelihood before use.

The package contains Log/Log_output.log, even though README calls it Log_output.txt. Earlier missing variable-construction code was later supplied; processed observations and the analysis do-file are already deposited.

**Mapping feasibility:** Main Tables 1-4 and assessed original-baseline regressions and distributions provide multiple numerical results.

**Shipped Stata logs:** `71/replication_package/3 replication package/Log/Log_output.log`.

### RB-031: Good Reverberations? Teacher Influence in Music Composition since 1450

**Provisional stratum:** technical failure. **Translation:** needs care. **Package:** 353.457 MB. **Runtime:** estimated 15-120 min for deposited-data regressions; source inclusion <2 h; missing appendix stops before estimation.

[Human report](https://www.econstor.eu/bitstream/10419/270744/1/I4R-DP027.pdf); [original package or public mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/31/replication_package). DP 27, section 2, identifies absent code and class/wealth variables for Appendix E.6, as well as absent raw tempo/key inputs. The report also reproduces the main similarity regressions from deposited processed outcomes and gives original-specification numerical tables.

**Stata version:** not stated in shipped readme or main wrappers. **User-written dependencies:** estout (eststo, esttab, estadd); outreg2; confirmdir; unique; bundled programs olspost, ivpost, saveTabstat, saveCorr, saveTtest.

Main areg models map to fixest with teacher-clustered SEs and explicit absorption. Missing E.6 variables/code cannot be supplied by translating areg. Do not confuse the report independently reconstructed/standardised outcomes with the deposited original outcomes.

PARTIAL TECHNICAL FAILURE RESERVE. No whole-paper gold verdict is assigned. Missing raw tempo/key construction alone is not a blocker when starting from supplied processed indices. If only assessed main results are later selected, this becomes a reproducible candidate. Absence of E.6 is reported by the human source, not inferred from an HTTP error.

**Mapping feasibility:** The source assesses multiple main regression results and identifies a specific unavailable appendix computation. A mixed 5-8-result task appears feasible, but the technical-failure stratum depends on retaining an Appendix E.6 target.

## Exclusions and borderline decisions

Every individually screened excluded paper has a CSV row. This table gives the decisive restriction or verification gap. A blank provisional stratum in the CSV means that no qualifying original-computation stratum was established, rather than an unreported failure.

| Candidate | Paper | Exclusion |
|---|---|---|
| I4R-hxadk | Can One Donation a Day Keep Depression Away? Three Randomized Controlled Trials of an Online Micro-Charitable Giving Intervention | Full original runtime under 2 h not established; full package additionally uses SPSS PROCESS; missing actual FDR/permutation-output code prevents an approved command-preserving scope. |
| I4R-rvynd | Unpacking P-hacking and Publication Bias | Restricted/confidential regressors and analysis files; no complete public original Stata task. |
| RB-003 | Assortative Matching at the Top of the Distribution: Evidence from the World’s Most Exclusive Marriage Market | Full original runtime exceeds 2 h; full appendix alone is 6 h 45 min; peerage redistribution is restricted. |
| RB-009 | Can Technology Solve the Principal-Agent Problem? Evidence from China’s War on Air Pollution | Full original workflow needs ArcGIS and brain neural-network code; original-only package boundaries and a 5-8-result Stata translation scope were not established. |
| RB-018 | Do Thank-You Calls Increase Charitable Giving? Expert Forecasts and Field Experimental Evidence | Public human claim-level reproduction evidence not recovered; REPRO-Bench score alone is insufficient. |
| RB-021 | Does Patient Demand Contribute to the Overuse of Prescription Drugs? | Full runtime below 2 h not established; bootstrap can take several hours; qualifying human report not recovered. |
| RB-024 | Enabling or Limiting Cognitive Flexibility? Evidence of Demand for Moral Commitment | Public human claim-level reproduction evidence not recovered; do not import the benchmark score as a verdict. |
| RB-028 | Finance and Green Growth | Qualifying unchanged-code claim-level comparison not established; reported differences follow corrected standard errors/GMM specifications. |
| RB-043 | Major Reforms in Electricity Pricing: Evidence from a Quasi-Experiment | Public human claim-level reproduction report not recovered; benchmark score alone is insufficient. |
| RB-046 | Mental Health Costs of Lockdowns: Evidence from Age-Specific Curfews in Turkey | Full original package requires restricted Turkish HLFS data under a data use agreement. |
| RB-056 | Pre-Colonial Warfare and Long-Run Development in India | Full declared workflow includes ArcGIS; an original Stata-only 5-8-result path and exact spatial-HAC translation were not established. |
| RB-074 | Gendered Reactions to Terrorist Attacks Can Cause Slumps Not Bumps | Sufficient original-code claim-level comparison and complete runtime not established; the recovered report focuses on corrected/altered analyses. |
| RB-076 | The Economic Effects of Long-Term Climate Change: Evidence from the Little Ice Age | Public human claim-level evidence and full runtime not established. |
| RB-078 | The Geography of Repression and Opposition to Autocracy | Public human claim-level report and full runtime not established; specialised covariance path needs further work. |
| RB-079 | The Long-Run Effects of Sports Club Vouchers for Primary School Children | Full original package uses NDA/data-use-agreement and restricted auxiliary datasets; no approved public-survey-only scope. |
| RB-086 | The Wheels of Change: Technology Adoption, Millwrights and the Persistence in Britain’s Industrialisation | Public human claim-level reproduction report not recovered; full appendix already reaches the 2 h bound before main outputs. |
| RB-095 | Understanding Cultural Persistence and Change | Qualifying 5-8-result unchanged-code comparison and full open-input/runtime checks not established; corrected-analysis differences are outside the issue stratum. |

Several decisions matter for later work:

- **RB-031 is a conditional reserve, not a whole-paper failure label.** The missing Appendix E.6 class/wealth variables and code are documented independently of the report's rebuilt outcome standardisation. The raw tempo/key omissions alone do not block the deposited-data main regressions. Any later decision to count a technical failure must depend on the actual approved targets. I have not selected such targets to force a stratum.
- **RB-020 starts from processed data.** The report finds missing raw data for `Data_prep.do` and complete reproduction from `dataset.dta`. This is recorded as reproducible from the deposited starting dataset. The R power script is ancillary. It is not evidence that the core original estimates were R rather than Stata.
- **I4R-rcngs is a genuine mixed original package.** The original Stata file itself estimates the Study 1 complementary-log-log model and margins, while the package also contains R cleaning and study analyses. The assessed Stata model contains enough numerical material for screening. The `.dta` requested by the script is not present, but a correspondingly named cleaned CSV is; any lossless import/format change must be recorded under the justified-fix rule. It is not a reason to infer a fatal scientific blocker.
- **I4R-hxadk is excluded after closer inspection.** Its original DOCX names Stata 15.0, R for FDR and SPSS 26 PROCESS for mediation. Its ZIP has three do-files, cleaned inputs, and no execution logs. Missing actual FDR/permutation conversion code and extensive imputation/permutation loops mean that an unchanged, fully specified, under-two-hour task has not been established. The source's one FDR mismatch does not become evidence of an unchanged Stata-output error when the actual original FDR calculation code is absent.
- **RB-054 has numerical recurrence issues even though the report calls the reproduction successful.** The unchanged-output discrepancies in its appendix are eligible evidence; corrected prefecture coding and changed samples are not. No severity or final match/close/discrepant labels have been assigned.
- **RB-067 has strong issue evidence but difficult translation.** The source's sign reversals are explicit unchanged-code comparisons. They affect estimates from `meologit`, so choosing this paper does not avoid the ordinal mixed-likelihood problem. `margins` uses fixed-only category probabilities and joint contrasts. It is a specialised reserve, not a certified exact `clmm` replacement.
- **RB-062's `xtreg` is not `xtreg, fe`.** The omitted model option invokes random effects. A fixed-effects translation would change the original computation. Its README names only coefplot; esttab is also required by the script.
- **RB-068 is borderline on time and stochastic inference.** The README says nearly two hours. The appendix explicitly warns that `nwqap` cannot set a seed. Deterministic OLS coefficients, Moulton SEs, and randomisation/multiplicity p-values require different evaluator treatment. No stochastic claim labels were made. `pairdata` is an observed appendix call whose provenance remains unresolved.
- **RB-013 is version sensitive.** The report reproduces the original under 16.1 and treats 17 as a separate variant. Its OLS treatment table should not be conflated with lasso-derived predicted outcomes. A glmnet fit with the same integer seed is not evidence of a command-preserving translation.
- **RB-041's methods differ across main and appendix analyses.** `reghdfe`/`ivreghdfe` main results are promising. `xtabond2` and `plausexog` appendix outputs need separate method-level work. The source's expensive newly added randomisation-inference exercise is not the original runtime.
- **RB-050's nonlinear post-estimation is material.** Firth logit has R implementations, but ordinary binomial glm is not the same estimator. The printed `margins` expressions must be translated as written. `ivprobit` cannot be replaced with linear IV. Keep this paper as a higher-effort reserve until numerical equivalence is checked.
- **RB-071 includes an original log, and an unusual appendix model.** `Log_output.log` is present despite the README's `.txt` name. `cmrologit, incomplete(99) reverse` for Appendix A14 is rank ordered logit, not ordinary multinomial logit. Main OLS/logit and school-clustered models are easier starting points.
- **RB-046 and RB-079 remain excluded for access restrictions.** Public main datasets do not erase required restricted auxiliary datasets in the full original package. A future explicit task scope could revisit them, but no such exception was assumed here.
- **RB-003 is excluded for full runtime and reuse restrictions.** The README times the appendix at 6 h 45 min, separately from the 75-minute main analysis, and limits redistribution of the deposited peerage subset. Dropping computationally expensive bootstrap inference would change the target computation.
- **RB-028, RB-074 and RB-095 are not imported as computational-issue cases.** Their recovered reports mostly present corrected models, control/sampling changes or alternative inference. This screen did not establish the required 5-8-result unchanged-code numerical comparison. RB-028's anonymised Orbis-derived inputs also deserve careful rights review if revisited; no access restriction is inferred solely from the commercial origin of the data.
- **RB-009 and RB-056 are future scope leads.** Their main Stata findings have human support, but the full declared workflows include GIS and specialised reconstruction/covariance code. A validated Stata-estimates-only scope was not completed here. The RB-009 mirror also includes reproducer weather files, so original versus added files must be separated from source evidence before use.

## Translation and evaluator preparation

The general mapping is the one requested by the project lead: regress/areg/reghdfe and linear IV to suitable R linear/fixed-effect estimators, logit/probit to the corresponding likelihoods, survey estimation to `survey`, and explicit preservation of each original command's sample and inferential conventions. The [fixest standard-error documentation](https://lrberge.github.io/fixest/articles/standard_errors.html) explains why degrees-of-freedom and covariance defaults must be chosen deliberately when matching other software. A matching estimator family is not proof that package defaults reproduce a Stata number.

Before a draw/package freeze, verify a complete 5-8-result mapping, the original package/report version match, runtime on the intended hardware, the six unstated target versions, and a pinned dependency inventory. This is a continuation of the original screening standard, not work completed by static inspection. In particular, resolve the specialised translation issues before relying on those outputs as deterministic R references. Original logs and rendered outputs must remain evaluator-only and be stripped from benchmark bundles under the approved packaging rules.

No claims were selected in order to maximise the issue/failure count. No inferential tolerance, seeded-draw equivalence rule, missing-code remedy, or new labelling rule was settled by this screen.

## Compact provenance index

The CSV records a report SHA256 and representative do-file SHA256 for each eligible package where downloaded. These hashes identify the inspected evidence without committing downloads. The scratch directory contains full recursive inventories, source PDFs/text, static code, archive expansions, metadata responses, data-access checks, and the curation scripts. It is temporary and should not be treated as a durable benchmark input store.

| Candidate | Human evidence record | Report SHA256 |
|---|---|---|
| I4R-rcngs | [I4R rcngs](https://osf.io/download/wh7dx/) | `237f64c94e1c0f8815fdf1a9307f2eed21c4fc7634836706a14bd1bef4b354f4` |
| RB-007 | [7; I4R DP 57](https://www.econstor.eu/bitstream/10419/275682/1/I4R-DP057.pdf) | `d38d6e676457ab533c84d35431b4fa732d60bdf7998b5cbbbbe05b39979bb4b7` |
| RB-013 | [13; I4R DP 34](https://www.econstor.eu/bitstream/10419/271674/1/I4R-DP034.pdf) | `93551501136584e985f853b6b32e81e2e153374be52e39a9137ce1c3b7c8f3da` |
| RB-020 | [20; I4R DP 28](https://www.econstor.eu/bitstream/10419/270858/1/I4R-DP028.pdf) | `ab6030a1ad9967982417c427adeea5ebfb2505840370b8168868b56b16a20b18` |
| RB-022 | [22; I4R bqz6w](https://osf.io/download/8jx43/) | `844fd201a8ee3f597ca7f6822bfe573ab0716b0fdb0e9a2ea16e9c0bb46fd83c` |
| RB-026 | [26; I4R DP 110](https://www.econstor.eu/bitstream/10419/289580/1/I4R-DP110.pdf) | `fdeb8e85423dfc3080ad094ac3b50f0b1fe64ec981335e9b73f0ca5c61a3cf80` |
| RB-031 | [31; I4R DP 27](https://www.econstor.eu/bitstream/10419/270744/1/I4R-DP027.pdf) | `a656f0389026a34854c17bbc6b51fd3c72a3bd0335c790f2c96136d2557c0e28` |
| RB-034 | [34; I4R DP 55](https://www.econstor.eu/bitstream/10419/274554/1/I4R-DP055.pdf) | `7795aa1986062d7b9ac25b3a7a263ae79bca074382ce9e26ab006c8f3fde48a7` |
| RB-040 | [40; I4R DP 43](https://www.econstor.eu/bitstream/10419/272845/1/I4R-DP043.pdf) | `5e62c658c278649c4c4786df6e2e078f055a4470f4c6689da0826604760ee729` |
| RB-041 | [41; I4R DP 50](https://www.econstor.eu/bitstream/10419/274140/1/I4R-DP050.pdf) | `dc2712f3ab4f125573ddf9c3b2ce90bcbfbb71cada9c2ca24dd7f62bb8d6f31c` |
| RB-048 | [48; I4R DP 65](https://www.econstor.eu/bitstream/10419/276253/1/I4R-DP065.pdf) | `a70118ede0593b58612de3668cf0561f3114142cfc79c4abd5e799239de0393d` |
| RB-050 | [50; I4R unhkr](https://osf.io/download/8xrkt/) | `416acf5b0b70f6a25149448047e9640e4044d2eed24283775bd08120db9631b5` |
| RB-054 | [54; I4R DP 155](https://www.econstor.eu/bitstream/10419/302899/1/I4R-DP155.pdf) | `bc8595abcd2644e6bf4abadd1bbd48a668b65ecce95090de483471aa740452c9` |
| RB-062 | [62; I4R DP 99](https://www.econstor.eu/bitstream/10419/281134/1/I4R-DP099.pdf) | `530b360fd06a0709ee0e4e56b25f2e8919197b95cb85f7ce9e344ada1c48c93c` |
| RB-067 | [67; I4R DP 67](https://www.econstor.eu/bitstream/10419/276961/1/I4R-DP067.pdf) | `0673e37298b4f6f3e3b0d053b00b6943f7d1f5e258668d0da94d45c886c36f87` |
| RB-068 | [68; I4R DP 111](https://www.econstor.eu/bitstream/10419/289581/1/I4R-DP111.pdf) | `83d2150d3389657c1aa672f9c7dfe844786f11a59f1e26df55d87d3756dcf280` |
| RB-071 | [71; I4R DP 106](https://www.econstor.eu/bitstream/10419/286490/1/I4R-DP106.pdf) | `0a39bd81e27984885d3d51525231bd1fec8ce0f575f449141e221b2139fe4a2a` |

