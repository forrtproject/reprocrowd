# Second-round Stata screening: I4R catalogue

Screened 1 November 2026. **80 new paper candidates recorded: six provisionally eligible, comprising five computational-issues candidates and one computationally reproducible reserve. No technical-failure candidate passed all eligibility checks.** Of the other 74 records, 42 are reproducible report-stage reserves awaiting original-package verification. The remainder have an exclusion or a specific unresolved eligibility/stratum problem. `eligible=false` means not cleared for the draw, including pending verification; it does not mean that every such paper is intrinsically ineligible.

The target of at least five additional issue candidates is met provisionally. The target of three eligible technical failures is not met. This round therefore improves the issue pool but does not itself support the intended two-paper technical-failure draw. No random draw, claim selection, claim labels, severity assignments, Stata installation, or numerical analysis execution was performed.

## Decisions to review

- Runtime is a static screening estimate, as in round 1, rather than a timing measurement. All six eligible packages have plausible workflows below about two hours, but the wider confidence limits for I4R-85, I4R-175 and I4R-243 need confirmation before drawing. The Bayesian tail of I4R-175 is explicitly included in its estimate.
- I4R-243 must use the pinned pre-correction author code and author-deposited processed data. Replacing it with the June 2025 corrected code changes the scientific computation. Upstream ATUS reconstruction is outside this processed-data starting point. This is the same type of starting-point restriction used for several round 1 packages.
- I4R-277 and I4R-231 are useful technical-failure leads, not cleared candidates. Their full original runtimes remain unresolved. Restricting either paper to a convenient subset in order to meet the quota would require a separate scope decision.

## Coverage and method

I read the shared instructions, round 1 CSV/notes, the original gold candidate list, the local catalogue/helpers and benchmark SPEC section 4.2. The output retains all 27 round 1 columns in order, with `round=stata-2-i4r`. Downloads, extracted text, immutable HF article checks, static inventories, original source files and scratch scripts are in `/tmp/scratch_stata/r2-i4r/`. Only the requested CSV and this Markdown file were written in the repository.

The live [I4R discussion-paper page](https://www.i4replication.org/papers) listed 336 papers, compared with 331 in the local snapshot. The live [reports page](https://www.i4replication.org/reports) listed 416 reports, matching the snapshot. I recovered the EconStor PDF for **every DP number 1-336**, extracted its text, and searched for both Stata and `.do` mentions. **167 DPs** contained either marker. This is catalogue triage, not 336 individual package screens: the series also contains responses, protocols, methodological papers, duplicate reports and studies whose reproducers alone used Stata. A marker does not establish an original Stata workflow.

I also downloaded the **149 OSF report PDFs with usable evidence URLs in the retained report indexes**. Of those, 26 contained Stata or `.do` mentions. The 416-entry catalogue was inspected as an index, not fully re-downloaded recursively. Some of its other records had no usable report-PDF pointer in those indexes. Therefore, this is complete DP-number text triage plus a bounded OSF supplement, not a claim to have read every OSF report. The paper-level CSV contains 80 distinct new candidate assessments, after consolidating alternate reports and removing overlaps. The other retrieved documents were used for discovery/deduplication or excluded at catalogue triage.

For the new candidates I examined the computational-reproducibility sections or corresponding report passages before prioritising packages. I looked for comparisons from the authors' unchanged code after path/package/order setup only. I excluded result changes produced by revised clustering, recoded variables, corrected samples, new estimators or robustness specifications. Original R, SPSS or MPLUS studies do not become Stata candidates because a reproducer used Stata.

I inspected original public inventories and code for nine papers: the six eligible papers plus I4R-277, I4R-231 and I4R-288. For I4R-191 I inspected a partial human archive and original documentation, but could not verify the original inputs or equivalence of the revised release. For I4R-323 I could read the report but could not inspect the original package. These are eleven prioritised package investigations, with distinct completion states. The 42 report-stage reproducible reserves have not had their full size/runtime/dependency checks and are not counted as eligible.

### Exclusion of earlier candidates and REPRO-Bench

I used both existing CSVs as exclusion lists, checking titles and candidate/source IDs. I fetched all 112 article PDFs from the [HF REPRO-Bench dataset](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f), pinned to `74958fba32daeacff51f2e1fd37be3916595648f`, and extracted their first two pages to verify overlap. No HF task packages or SCORE packages were screened as new additions here. The task articles were used only as an exclusion inventory.

Promising DP leads removed on that basis include DP66 (management interventions, task 75), DP115 (Web of Power, task 104), DP140 (Green Book/public accommodations, task 109), DP144 (pollution monitoring, task 110), and DP19 (political cleavages, task 5). Other familiar overlaps include DP12 (task 35), DP16 (task 46), DP24 (task 61), DP39 (task 55), DP43 (task 40), DP48 (task 52), DP54 (task 51), DP62 (task 87), DP64 (task 45), DP65 (task 48), DP67 (task 67), DP74 (task 73), DP88 (task 63), DP93 (task 16), DP95 (task 28), DP110 (task 26), DP132 (task 8), DP152 (task 112), and DP155 (task 54). They are not new candidate rows. The alternate wording of OSF z5pjq was also matched by candidate ID to the earlier CSV and removed.

DP175 and OSF w9tyb, DP243 and OSF crkgs, DP288 and OSF gexqa, DP221 and OSF rt48s, DP252 and OSF 2fghj, DP193 and OSF gj7v3 are consolidated as single paper records. DP162/180, DP245/279 (also OSF ubmt2) and DP256/257 are additional duplicate-report routes. Merely appearing in another paper's references was not treated as an exclusion match for the underlying candidate.

### Eligibility and byte accounting

Eligibility requires public original analysis inputs without an NDA or restricted-data requirement, social/behavioural subject matter, an original `.do` estimation workflow, a plausible runtime below about two hours, a package below 5 GB and human numerical evidence supporting a mixed 5-8-result mapping. Eligible processed-data starts are described explicitly. Absence of optional upstream raw data does not itself become a technical failure.

Dataverse marks all files in the five eligible Dataverse deposits unrestricted. Original-format DTA files were fetched using `format=original`, preserving the possibility of labels and types lost in TAB exports. Sizes use original-format bytes when the metadata provide them and include other deposited files, such as rendered outputs. They are not compressed-download sizes or minimal-input sizes. I4R-243 uses the two files in the authors' cleaned-data archive plus pinned code/documentation; its optional raw reconstruction is not included. All eligible sizes are comfortably below 5 GB. Neither generated `log using` commands nor a reproducer's log are counted as shipped original logs.

Version and command records come from inspected code/documentation. A DTA file format is not an original target Stata version. User-command inventories are static and are not a resolved, pinned transitive environment. No Stata, SSC, R or other analysis was installed or executed. Reading CSV headers, counting file lines, opening archives and extracting report tables were static inspections.

No personal contact email was sent to any service. Metadata queries omitted contact emails even where allowed. No data access agreements, account registrations, author contacts or credential submissions were made. A generic public-download login and an unavailable endpoint were not used as evidence of a technical failure.

## Counts

The provisional-stratum column describes the report lead, including excluded or unresolved leads. Only the eligible column contributes to the new sampling pool.

| Provisional stratum | All recorded | Eligible | Not cleared |
|---|---:|---:|---:|
| computationally reproducible | 52 | 1 | 51 |
| computational issues | 8 | 5 | 3 |
| technical failure | 10 | 0 | 10 |
| ambiguous | 10 | 0 | 10 |
| Total | 80 | 6 | 74 |

All six eligible packages have `ships_logs=no`. A log in the original misinformation reproducer archive is not an original-package log. I4R-231's small file called `log` is an ArcGIS record.

## Applying SPEC section 4.2 without labelling claims

Issue strata describe non-recurrence, not final claim status. A report saying “typo”, “rounding” or “minor” does not establish `close`. I recorded the mechanism and the available bundle evidence separately:

| Candidate | Non-recurrence established by human source | Evidence relevant to a reporting-slip explanation |
|---|---|---|
| I4R-db26h | Different z statistics, p-values and some CI endpoints; duplicate reported models | No in-package erratum located. Proposed duplicate donors require executed output; no report-only exemption. |
| I4R-85 | Different coefficient/SE pairs, including significance-threshold changes | Deposited TeX output corroborates the reproduced values. No located reporting slip explains the gaps; crossed thresholds invoke the veto. |
| I4R-175 | Incorrect published in-text CIs for treatment effects | The report locates the paragraph but no in-package author erratum or executed donor was found. The exact slip still needs bundle-level investigation. |
| I4R-243 | Incorrect original-code sample subset, so output differs from print | This is a deterministic code/print mismatch. It is not inferred from later corrected low-income coding or reweighted models. |
| I4R-289 | Table 3 column 1b SE .57 versus .55 | Potential single-character slip, contingent on matching companion statistics inside the staged bundle/output. The report's description alone is insufficient. |

No results were labelled `match`, `close`, `discrepant`, `within_variation` or `not_checkable`. Numeric tokens in these notes are evidence examples, not a frozen must-check list.

## Eligible candidates

### I4R-db26h: Market exposure and human morality

**Stratum:** computational issues. **Package:** 0.696 MB. **Runtime:** estimated 5-30 min from small analysis datasets and finite OLS/IV scripts; not timed.

[Human report](https://osf.io/download/xm3nj/); [original package](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/EEGV7A). Report section 2 and Table 1 compare original analysis-data results with Figure 3: e.g. prosociality IV z=2.76 and p=.006 versus 2.78 and .005; trust IV z=5.81 versus 5.94. Supplement Table 3 also duplicates model columns. New language-family fixed effects in report Table 2 are separate.

**Stata version:** not stated in inspected scripts or READ_ME; original data format is Stata 14, which is not a target-version statement. **User commands:** ivreg2; ranktest (ivreg2 dependency); estout (eststo, esttab, estadd); binscatter. **Translation:** needs care. OLS, areg and 2SLS are standard, but preserve cluster covariance, ivreg2 small-sample/default z-versus-t inference, country/continent indicators and manual figure-statistic calculations. Affects Figure 3 and Supplement Table 3; binscatter affects Figure 2.

Complete public Dataverse inventory: 10 unrestricted files, original-format DTA files downloaded. Main input is deposited processed data; upstream folklore cleaning is not supplied. READ_ME instructs separate Coef_plot.do and other do-files; !Master.do alone is not the whole documented workflow. Non-recurrence: numerical inference differences and duplicate reported model columns. No in-package erratum was found; report-only typo explanations and putative duplicate donors are unconfirmed under SPEC 4.2 until executed output establishes them. No claim labels assigned.

### I4R-85: Reshaping Global Trade: The Immediate and Long-Run Effects of Bank Failures

**Stratum:** computational issues. **Package:** 507.618 MB. **Runtime:** estimated 20-120 min; finite FE regressions and data construction, no bootstrap/MCMC loop seen; not timed.

[Human report](https://www.econstor.eu/bitstream/10419/279958/1/I4R-DP085.pdf); [original package](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/EIEQIS). DP85 section 2 and Tables 2-5 compare published Tables IV/V with unchanged deposited code: -0.656 (.210) versus -0.631 (.213), and -0.554 (.204) versus -0.505 (.207). Two Table IV estimates change from 1% to 5% significance. The report states deposited output tables show the same differences; no software-version explanation is needed.

**Stata version:** 16 (_Readme.docx; xu_tables.do also has version 16). **User commands:** reghdfe and bundled ado/Mata support; ftools; estout (eststo, esttab, estpost, estadd); estfe; coefplot; distinct; erepost; keeporder; kountry and bundled country-conversion helpers; psacalc/psacalci; ssaggregate. **Translation:** needs care. Preserve high-dimensional FE absorption, sample restrictions, analytic weights, singleton removal and variance/degrees-of-freedom rules. Tables IV/V supply issue targets. Separate long-run event-window recoding and spatial-HAC robustness are not unchanged-code issue evidence.

Full Dataverse metadata: 262 unrestricted files, no Stata log inventory entries. Original-format byte sum is 507.618 MB; inventory TAB representations sum to 491.594 MB. Original do-files and README inspected; original data downloads and deposited TeX tables retained in scratch. Non-recurrence: substantive coefficient/SE differences, including threshold changes. No in-package erratum identifying these differences found. Deposited tables contain the reproduced values but do not alone explain the historical cause. DP85 Table G12 discussion also changes event windows, so it is not used to establish the issue stratum. DOI matched to Crossref and the deposit publication metadata. No claim labels assigned.

### I4R-175: Political endorsement by Nature and trust in scientific expertise during COVID-19

**Stratum:** computational issues. **Package:** 0.465 MB. **Runtime:** estimated 5-90 min; small CSV, OLS plus eight low-dimensional bayesmh fits; not timed.

[Human report](https://www.econstor.eu/bitstream/10419/305223/1/I4R-DP175.pdf); [original package](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/KBIRPN). DP175 section 3 identifies incorrect confidence intervals in the last paragraph of Trust in Nature (published p.698), after reproducing the supplied clean-data Stata code. Report Table 1 gives numerical treatment estimates, SEs and p-values for four outcomes and both political groups. Original Figure 4 was independently recreated because its code was absent.

**Stata version:** not stated in original do-file or deposit documentation. **User commands:** estout (eststo, esttab); bayesmh and bayesstats are built in. **Translation:** needs care. Main treatment OLS, robust SEs, outcome standardisation and confidence intervals are straightforward with explicit Stata finite-sample inference. The full script also has seeded univariate/multivariate Bayesian fits and Bayes factors; those need specialised treatment and cannot share a Stata random stream merely by using the same seed in R.

Two unrestricted deposited files, zhang2023.csv and zhang2023_main_analysis.do, downloaded. Main OLS workflow uses the public clean data. Author-supplied non-public raw variables used for report extensions are outside the proposed targets. Non-recurrence: printed in-text confidence intervals, not a corrected model. The report calls them typos but does not locate an in-package erratum or executed donor; record the difference without assigning close/discrepant labels. Figure 4 missing code and absent supplementary variables are not used to claim a technical failure. Full runtime is a static screening estimate, including the small seeded Bayesian component, not a timing claim.

### I4R-243: Examining inequality in the time cost of waiting

**Stratum:** computational issues. **Package:** 967.914 MB. **Runtime:** estimated 15-120 min from deterministic regressions and data merges; not timed; processed-data start.

[Human report](https://www.econstor.eu/bitstream/10419/321370/1/I4R-DP243.pdf); [original package](https://github.com/stevebholt/waiting-time/tree/95e2eaec985dfbd7f2dfd5e05ebe768195e4e613). DP243 section 2 documents that the original 03_tables.do incorrectly subsets Table 1 Panel A column 6, so its unchanged output does not reproduce print. Figures 1-5 otherwise recur. Report Tables 2/3 document baseline and corrected results; only baseline comparisons are admissible. Later fixes to low-income coding, weights, activities and controls are separate analyses.

**Stata version:** not stated in original do-files or README. **User commands:** estout (esttab, estpost); coefplot; lean2 graph scheme; cpoisson command provider/version needs resolution because a historical user command and modern built-in share the name. **Translation:** needs care. Main weighted regressions/xtreg FE need matching sample restrictions, survey-weight scaling and state-clustered finite-sample covariance. Appendix censored Poisson/Tobit and margins need estimator/default care. The Panel A column 6 subset is retained exactly for Track A.

Original pre-correction code pinned to Git commit 95e2eaec985dfbd7f2dfd5e05ebe768195e4e613; confirm exact hash against commits.json. Later June 2025 author commits explicitly correct code and are not silently substituted. README links author-deposited cleaned data on Dropbox; archive downloaded and opened: atusall0319.dta 427620870 bytes and CPS_ASEC_selectvars_timeinequality.dta 540229519 bytes. Package size is these analysis inputs plus pinned scripts/documentation, not the optional BLS raw reconstruction files. Starting from author-deposited processed data is required for this estimate. Non-recurrence: deterministic sample-subset mismatch in unchanged original code. The output filename overwriting panel C is a separate output issue, not the numerical reason. No in-package reporting-slip explanation is needed or claimed. No claim labels assigned.

### I4R-289: Crisis and the Trajectory of Science: Evidence from the 2014 Ebola Outbreak

**Stratum:** computational issues. **Package:** 2.565 MB. **Runtime:** estimated 5-60 min; 589-scientist panel and finite ppmlhdfe/reghdfe fits; not timed.

[Human report](https://www.econstor.eu/bitstream/10419/339570/1/I4R-DP289.pdf); [original package](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/ZFEBRV). DP289 section 2, footnote 1, identifies an unchanged-code Table 3 column 1b standard error: .57 in print versus .55 in reproduction, for AFTER EPIDEMIC x ENDEMIC COUNTRY x NTD EXPERIENCE. Other main and appendix tables/figures reproduce. Report Tables 2/3 provide original baseline models alongside robustness variants.

**Stata version:** 16 (README.pdf). **User commands:** ppmlhdfe; reghdfe; ftools (dependency). **Translation:** needs care. Translate PPML with absorbed effects and matching cluster covariance, separation/singleton rules, convergence and sample definitions. This includes the Table 3 column 1b issue. Original processed scientist-year panel is the starting data; redoing CEM from proprietary Scopus records is not required.

Five unrestricted Dataverse files. Original-format ebola.dataset.dta and three original do-files inspected, with README. Original-byte size 2.565 MB; TAB-view inventory 2.449 MB. Non-recurrence: single-character reported SE difference, with unchanged coefficient/significance reported by the human source. This is a potential SPEC 4.2 single-character slip only if matching companion statistics are demonstrable inside the staged article/package and executed output; no labels assigned and no report-only slip exemption assumed. Raw Scopus records are proprietary, but all required original analysis inputs are openly deposited, so their absence is upstream, not an analysis-package blocker. DOI verified through Crossref.

### I4R-138: UN Peacekeeping and Democratization in Conflict-Affected Countries

**Stratum:** computationally reproducible. **Package:** 4.895 MB. **Runtime:** estimated 5-60 min; small country-year data and finite FE/RE/IV fits; not timed.

[Human report](https://www.econstor.eu/bitstream/10419/301427/1/I4R-DP138.pdf); [original package](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/UOYDHN). DP138 section 2 explicitly reruns the original Stata do-files and finds exact recurrence with no coding errors. Its subsequent tables provide numerical FE-model comparisons across multiple peacekeeping and democracy outcomes, enough for a 5-8-result mapping.

**Stata version:** SE 17.0 (readme.rtf). **User commands:** estout (eststo, esttab); bundled indvar_* and iv_ctrls* ado wrappers around xtreg/xtivreg; preserve each primary/secondary appendix programs directory. **Translation:** needs care. Main country FE models are ordinary panel regressions. Preserve lagged covariates, sample restrictions, within transformation and Stata variance/DF conventions. RE and panel IV routines occur elsewhere and need separate checks if selected.

Public inventory has 29 unrestricted files. Original-format sum 4.895 MB, versus 4.625 MB in TAB views. Metadata directory labels are essential: two appendix trees reuse basenames and helper names; both directory structures downloaded without treating the repeated names as missing material. Original Stata data and code inspected. Published processed panel is the admissible starting point. Eligible reproducible reserve, not an additional issue case. DOI verified in depositor publication metadata.

### Mapping feasibility and limits

- **I4R-db26h:** Figure 3 and source Tables 1/2 cover OLS/IV results across prosociality, trust, universalism and moral emotions. Use the original specifications, not the additional language-family FE exercise.
- **I4R-85:** The report explicitly pairs published Tables IV/V with its unchanged-code Tables 4/5, covering more than eight effect/SE comparisons. The later G12 recoding and spatial-HAC exercise must not supply the issue evidence.
- **I4R-175:** Report Table 1 covers treatment effects for Trump/Biden supporters across four outcomes; section 3 locates the incorrect CIs. The public clean dataset supports the main models. Missing raw extension variables are unnecessary for this mapping.
- **I4R-243:** Report Tables 2/3 contain baseline models and then corrected variants; only the baseline specifications and assessed Figures 1-5 are candidates for the human trail. Section 2 separately locates the incorrect subset in the original column 6 code. Table 1 of the report is a package-availability checklist, not a numerical comparison table. The eventual issue-value comparison still needs precise article-to-output alignment.
- **I4R-289:** The original baseline columns in report Tables 2/3, with section 2 footnote 1, support a mixture of matching estimates and the affected SE. Results using author-on-request pre-matching data are unnecessary.
- **I4R-138:** Section 2 explicitly attests to exact native-Stata recurrence; subsequent FE comparison tables give numerical results across personnel/outcome models. Restrict a draw to the original models and retain their finite-sample inference.

These are feasibility assessments. None is a claim selection or label list. Where the human source's point estimates and its prose disagree, package preparation must resolve the exact location before freezing gold claims.

## Borderline cases and why the failure quota remains open

### I4R-191: Local Elites as State Capacity: How City Chiefs Use Local Information to Increase Tax Compliance in the D.R. Congo

**Report lead:** computational issues. [Report](https://www.econstor.eu/bitstream/10419/307931/1/I4R-DP191.pdf). DP191 section 2 documents the opposite sign on Local for Incorrect exemption in Table 5; magnitude and SE agree. DP192, the authors response, confirms the sign error in Tables 5/A9 and a submitted corrigendum. Package/order fixes are separate.

**Not cleared:** Not cleared: original V1 is now marked unpublished by ICPSR, the human GitHub archive omits the data, and V3 has 2025 changes that were not downloaded/compared. Full original-package size/access and version equivalence remain unverified.

Read original README and preserved do-files in https://github.com/SossouAdjisse/LocalTaxReplicationProject, plus ICPSR V1/V3 inventories. GitHub master has been changed to run robustness exercises and supplies no input DTA files. Do not treat its 26.354 MB as the original package size. Non-recurrence is a sign reversal, which has a SPEC 4.2 veto even if an author corrigendum is later staged. Public account login was encountered for V3 downloads; no credentials or contact email were submitted. This access problem is not a technical-failure stratum.

### I4R-277: Understanding and reducing online misinformation across 16 countries on six continents

**Report lead:** technical failure. [Report](https://www.econstor.eu/bitstream/10419/334158/1/I4R-DP277.pdf). DP277 sections 3.1/3.2 report failed original-code references to false and rating_4 in Figures S11a-b/S11d. Static original-code inspection confirms false is never generated and reshape wide rating creates rating1/rating4 rather than rating_1/rating_4. These are shipped-code errors, independent of cluster2 compatibility.

**Not cleared:** Borderline technical-failure reserve only: full original runtime under two hours is not established. The package also includes an R Figure 6 routine with 1000 iterations across up to 50 bootstrap sizes per country; a Stata-only scope has not been authorised as a substitute.

Full recursive original g65qu inventory inspected and code/data downloaded. Original package has analysis/230412 CR.do, data/CR.csv, CovidCountryAUC.Rmd and bootstrap_fns.R plus materials. CR.csv has rating_4 before reshaping; the failure is the later generated-variable name, not an absent raw rating column. Original code also references rating_3 after reshaping. The report repository p5e6k ships Stata_output.smcl, but that is a reproducer log and is not counted as an original-package log. Report footnote w84na resolves to a PDF file in that reproducer repository, not the original package. No scientific fix or analysis executed here.

### I4R-231: The political consequences of resource scarcity: Targeted spending in a water-stressed democracy

**Report lead:** technical failure. [Report](https://www.econstor.eu/bitstream/10419/318265/1/I4R-DP231.pdf). DP231 section 2 states that bootstrap appendix code at lines 2464-2610 failed. Static original gw_replicate.do declares local aggvar, but the nrega branch uses undefined agvar in mi(), producing a malformed argument; this is separate from path and rdrobust installation fixes.

**Not cleared:** Borderline technical-failure reserve only: full original runtime under two hours is not established for two 1000-replication RD bootstraps and numerous preceding fits. The report does not identify the exact runtime failure, so the static macro defect must still be checked against an archived Stata environment before a draw.

Original public Dataverse inventory and .do downloaded. Data files include nregs_gp (7876 rows in public TAB view) and crosscut_station (16583 rows); these are substantial inputs for the repeated bootstrap fits. The file named log is an ArcGIS processing record, not a Stata execution log. Original-format byte sum not separately calculated, so 240.107 MB is the deposited inventory representation. No claim labels assigned.

### I4R-288: Discrimination reduces work effort of those who are disadvantaged and those who are advantaged by it

**Report lead:** ambiguous. [Report](https://www.econstor.eu/bitstream/10419/339569/1/I4R-DP288.pdf). DP288 Tables 2-7 document seven reporting differences, including Study 2 bonus-expectation control mean 2.38 versus 2.961, with 2.96 in the supplement. However, the report computes its comparisons in R rather than documenting an unchanged original-Stata rerun.

**Not cleared:** Not cleared for the computational-issues stratum: the human source is an independent R recreation, including a different mediation implementation, and does not establish recurrence/non-recurrence from an unchanged Stata execution.

All three original OSF files downloaded: combined data, manager survey data, replication code.do. Potential reporting-slip evidence includes an article/supplement disagreement and a proposed donor mean, but the donor has not been demonstrated in executed original output. Do not import the report classification or new count-model meta-analysis as an unchanged-code issue. No labels assigned.

### I4R-323: Does the Effect of Pollution on Infant Mortality Differ Between Developing and Developed Countries? Evidence from Mexico City

**Report lead:** computational issues. [Report](https://www.econstor.eu/bitstream/10419/344062/1/I4R-DP323.pdf). DP323 section 2 reports unchanged-code descriptive differences: published Table 1 N=24691 versus 18546 in provided Table 1.do for mortality panels, plus different Figure 4 mortality lines. Headline IV estimates largely reproduce; Table 5 needs deprecated-command edits.

**Not cleared:** Not cleared: source report read, but the original Oxford/Wiley package could not be downloaded and no code/data inventory, package size, target version or full runtime was established. An unavailable endpoint is not a technical failure.

Strong issue lead for follow-up; unchanged-code count differences are exact-count differences under SPEC 4.2, not rounding. Do not use the report minor-typo language to exempt them. Main effects could supply additional mappable results if package access is recovered; no benchmark claims selected.

### I4R-80: The Labor Market Impacts of Universal and Permanent Cash Transfers: Evidence from the Alaska Permanent Fund

**Report lead:** technical failure. [Report](https://www.econstor.eu/bitstream/10419/278842/1/I4R-DP080.pdf). DP80 section 2 says two necessary input datasets were absent and authors supplied them on request; after fixes native Stata results matched. Different synthetic-control weights in the report R recreation are separate.

**Not cleared:** Missing input names and their status in current V2 not independently verified; full original raw-package size and synthetic-control/placebo runtime not established. Not an eligible failure on report language alone.

Report source read; original ICPSR dataset/version route verified in public metadata. Do not count inability to download an endpoint as a code failure.

### I4R-30: The Arrival of Fast Internet and Employment in Africa

**Report lead:** technical failure. [Report](https://www.econstor.eu/bitstream/10419/270965/1/I4R-DP030.pdf). DP30 identifies missing morework and other variables, plus Table 5 Panel B unchanged-code discrepancies. Several other main tables require restricted-access inputs.

**Not cleared:** Restricted data required for parts of the original workflow; no complete open, under-5-GB and under-2-hour original package established. Public-subset scope would require a separate decision.

A missing constructed variable is a real package lead, but restricted-data unavailability is not the technical-failure reason. No corrected-variable reconstruction substituted.

### I4R-221: Income and Inequality in the Aztec Empire on the Eve of the Spanish Conquest

**Report lead:** ambiguous. [Report](https://www.econstor.eu/bitstream/10419/315048/1/I4R-DP221.pdf). DP221 reproduces the main Stata/Excel analysis-data results. Kolmogorov-Smirnov code was never supplied; the report writes ksmirnov code and obtains larger p-values. Changing the IV sample/SE calculation also changes the model.

**Not cleared:** Missing test implementation and new ksmirnov results do not demonstrate an unchanged shipped-Stata failure. No 5-8-result mapping containing an admissible blocker established; full mixed Stata/Excel package not inspected.

Duplicate OSF rt48s evidence consolidated here. Do not promote independently written tests to the computational-issues stratum.

### I4R-n4yt9: Arrests and convictions but not sentence length deter terrorism in 28 European Union member states

**Report lead:** technical failure. [Report](https://osf.io/download/qk9jv/). Report supplement section 3.1 says the V1 analysis data omit HDI/law-enforcement controls and original code covers only some figures; Tables 1/2 are independently reconstructed.

**Not cleared:** No 5-8-result unchanged original-code mapping established for the missing-table-code scope; original package not inspected. Incomplete reporting/implementation alone is not the requested demonstrated shipped-code blocker.

Human report SHA256 a076a0feb19a021b0b22311a03699e4c3dad34d0a2f064f8ff0d427f9aff503f.

### I4R-wdk2s: State Violence, Party Formation, and Electoral Accountability: The Political Legacy of the Marikana Massacre

**Report lead:** technical failure. [Report](https://osf.io/download/6a9041436462cf4a736b1273/). Report section 2 reproduces aggregate-data results, but cannot reproduce individual saturated models with municipality clustering and spatial controls because geolocations are absent.

**Not cleared:** Missing individual geolocations are covered by data-availability limitations and may be restricted by design; no qualifying accidental public-package blocker established. Full size/runtime also not inspected.

Manually locating the reg2hdfespatial ado and downgrading R for maps are package/environment fixes, not technical-failure reasons.

### Other clear restrictions and language exclusions

The CSV records further examined candidates individually. DP233 requires restricted NHTS inputs; DP252 requires a BIT agreement/proprietary TargetSmart data; DP259 does not redistribute the HSNP/DHS data; DP301 relies on CBS microdata. Their data restrictions are not eligible shipped-package failures. DP137 is an original MPLUS analysis; DP178, DP186, DP202 and OSF nk6ev/mg95t have original R workflows. Stata use by a reproducer does not satisfy the original-language criterion. DP163 and OSF zn98a involve recreation rather than demonstrated unchanged-Stata execution. These distinctions explain why apparently adverse human reports did not automatically become issue/failure additions.

The 42 report-stage reproducible reserves are retained in the CSV with the explicit common pending-verification reason. They are a follow-up queue, not 42 additional eligible papers. The CSV names each report, records the assessment basis and keeps uninspected size/runtime/log fields empty or unknown. No source status label was imported as a gold outcome.

## Audit trail

Each CSV row retains the downloaded human-report SHA256. The table below additionally pins representative original do-files for eligible candidates. These hashes identify inspected files; downloads are temporary and must be staged durably before a benchmark draw.

| Candidate | Representative original code | SHA256 |
|---|---|---|

| I4R-db26h | `packages/db26h/Coef_plot.do` | `f378154e4ce0a310ec56a7adaaa3d3ab17e93c0ad6490dd3533e0a815403bcca` |
| I4R-85 | `packages/85/xu_tables.do` | `bcd75e73b717099d814c82029b80a758f1db6aee03d14f66ae8b7b5b97bb7fc0` |
| I4R-175 | `packages/175/zhang2023_main_analysis.do` | `3fa7c0d208d478809804d4e2117c9f82d9fba1b0b8eda5745de5d0efc273fa2c` |
| I4R-243 | `packages/243/original/03_tables.do` | `e5d9cf912d3f06a6d77029d45e232131f0f6c557f1ff248d27194c1c66ad2648` |
| I4R-289 | `packages/289/replication_tables.do` | `f7d6b79d40497143fc0658e0c6c28e3b5523e9b51ea7816be8db2485b3891381` |
| I4R-138 | `packages/138/replication.do` | `e50f8ddce654872bc7d7ba0f024dab0ffd451174e9a172edb5875f404838078f` |

Scratch provenance includes `dp_index.json` (all 336 report URLs), `osf_index.json`, `dp_skips.json` (discovery matches, not authoritative whole-paper exclusions), all 112 HF article first-page checks, package metadata/recursive inventories, the waiting-time commit list, original byte inventories, original files and Crossref responses. A full-text reference match can be incidental; final additions were checked by their own scientific title/source identity. The exact waiting-time commit is stored in `packages/243/original/commit.txt` and in its candidate URL.

No further search result, unavailable endpoint, or coarse reproducibility rating has been converted into an eligible technical failure. The remaining useful work is to establish full runtime and precise blocker-to-result scope for the two best technical leads, or obtain additional eligible failures from a different source stream.
