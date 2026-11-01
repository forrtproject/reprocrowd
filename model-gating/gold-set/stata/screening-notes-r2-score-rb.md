# Stata screening, round 2: SCORE and REPRO-Bench

Screened 1 November 2026. **97 candidate records: 70 SCORE and 27 REPRO-Bench. Twenty-two are provisionally eligible: 14 computational issues, eight computationally reproducible, and no clean technical failures.** The issue target of at least five additional papers is exceeded. The technical-failure target of at least three is not met. These are screening judgements, not claim labels, a random draw, or completed reproductions.

## Counts and implications

| Discovery source | Recorded | Eligible | Excluded | Reproducible, eligible | Issues, eligible | Technical failure, eligible |
|---|---:|---:|---:|---:|---:|---:|
| SCORE | 70 | 5 | 65 | 0 | 5 | 0 |
| REPRO-Bench | 27 | 17 | 10 | 8 | 9 | 0 |
| Total | 97 | 22 | 75 | 8 | 14 | 0 |

“Recorded” includes **39 SCORE archive/availability prefilters**, retained so that exclusions are visible, and **31 case-level SCORE report/package assessments**. REPRO-Bench has 27 fresh package-inventory screens, four of which stop at the size bound. Do not describe all 97 as papers with fully inspected original code and human reports. The CSV states the stopping reason for every exclusion.

The 14 issue additions are SC-LyWB, SC-0P4r, SC-a2Yx, SC-L22B, SC-9wya, RB-037, RB-060, RB-064, RB-075, RB-077, RB-082, RB-104, RB-106 and RB-109. The eight additional reproducible candidates were encountered during this targeted search and are retained because eligibility was assessed independently of the desired stratum.

Five eligible papers have SCORE human evidence; 17 have I4R human evidence discovered through REPRO-Bench. The latter are not independent REPRO-Bench human replications. No I4R-catalogue-only lead was screened. The parallel I4R search can therefore be integrated by paper identity without claiming that a second discovery route supplies independent human evidence.

Adding this pool to round 1 gives 39 provisionally eligible papers before cross-source deduplication: 22 reproducible, 16 issues, and the existing one conditional technical-failure reserve, RB-031. **This pass does not establish two clean failures for a 4/4/2 draw.** Also re-adjudicate RB-031 against the current SPEC 4.6 rule rather than assuming its earlier conditional stratum is settled.

## Method and source coverage

1. Read the round-1 Stata CSV/notes, earlier R/Python screening and retained audit JSON, and current benchmark SPEC sections 4.2 and 4.6. Kept the exact 27-column schema and column order of candidates-stata.csv. Every new row has round=stata-2-score-rb and reuses SC-xxxx or RB-nnn identifiers.

2. Downloaded the public [SCORE analyst archive](https://osf.io/download/cs8up/) from the [SCORE reproducibility materials node](https://osf.io/ed8pj/), and read its saved metadata/outcome tables. Loading the RData only exported existing tables; no original statistical analysis or SCORE analytical script was run. The fresh archive has 586 version-of-record rows, including 104 not and five not attemptable rows across 53 papers. Reused the retained score_summary.json to locate reports, checked its outcome totals against the fresh archive, and retained all 53 negative-paper availability assessments. Added public-code papers with partial/approximate outcomes and targeted none outcomes, including 0P4r. The original eleven requested leads all have rows, including those whose original workflows are not Stata.

3. Traversed public SCORE project and original-material inventories, read transparency trails and reports, and inspected original do-files, saved output and small archives. OSF API requests became HTTP 429 rate-limited. I then used OSF’s public file-service inventory/download URLs, returned by the service itself, to recover reports and archives. These HTTP failures are not study blockers. In particular, h5kat is publicly downloadable even though its component title says Data (private). SC-9wya’s 46.045 MB expanded ZIP was opened and inspected.

4. Re-filtered the REPRO-Bench inventory for unscreened original .do/.DO workflows. Prioritised benchmark scores 1/2 and included score-3 leads. Fresh recursive per-task inventories and original small code/readme/article files were fetched at immutable HF commit `74958fba32daeacff51f2e1fd37be3916595648f`. Tasks screened: 2, 14, 17, 33, 35, 37, 39, 45, 51, 55, 57, 60, 64, 70, 75, 77, 82, 84, 85, 89, 96, 104, 105, 106, 107, 109 and 110. No round-1 Stata RB task was duplicated. This is a bounded search of these lower-score leads, not a claim to have re-read every high-score task.

5. Read the actual public human reports, not benchmark scores as verdicts. RePEc links were used only to recover the I4R report for a preidentified REPRO-Bench paper. DP287 supplied report links for specific benchmark papers, including Digital Addiction and Esposito (2022). Original paper PDFs, report sections, and numerical tables were inspected. DP82 Table 1, DP66 Table 3 and DP140 Table A1 were rendered and visually checked, including their notes and column identities.

6. Checked a public input-file byte range for all 17 eligible HF packages. All returned HTTP 206. This demonstrates unauthenticated access to a sampled input, not completeness or integrity of every large input. SCORE eligible original inputs were downloaded in full where small, including the 28.455 MB a2Yx analysis dataset. Original version 1 of a2Yx Tables 3-7 was recovered instead of relying on the analyst-modified current version 2.

7. Verified article DOIs against Crossref where possible and against the printed original article otherwise. Some Crossref calls returned HTTP 429. RB-057 uses the article DOI printed in the PDF, not the earlier Dataverse DOI in that PDF. Unverified SCORE article DOIs are omitted, including SC-0P4r and SC-9wya; report/data URLs remain available. Bibliographic year follows the cited journal issue where available, which can differ from first-online Crossref dates. No contact email was sent to any service.

## Eligibility and interpretation

Eligibility follows round 1: public original code and analysis inputs without NDA/restricted access for the assessed computations, social/behavioural subject matter, original Stata estimation workflow, package below 5 GB, credible runtime below about two hours, and human numerical evidence supporting a possible 5-8-result mapping. Public processed inputs are acceptable, as in round 1. A confidential upstream census or raw phone log is not required when the original package/report genuinely uses supplied anonymised analysis inputs. Its absence is recorded, not called a technical failure. Original .do source distributed as .do.txt is treated as a plain-text do-file; Word fragments newly saved as .do by a reproducer are not an original .do deposit.

Package sizes are decimal MB summed over replication_package files for HF, excluding task-level paper.pdf and instructions. For SCORE, they refer to the inspected original data/code copies or expanded original ZIP, excluding human reports and reproducer logs. Duplicated deposited ZIPs are included in HF totals: RB-075 has both datasets.zip and its expanded counterpart. RB-014’s 4.428 GB inventory has no embedded ZIP; it is still close to the size bound. Expanded archive contents were inspected where small.

Runtime is a screening estimate, not a timing result. Exact README timings are distinguished from static estimates and REPRO-Bench’s secondary inclusion bound. RB-014, RB-033, RB-075, RB-085 and RB-104 warrant particular runtime checks before a draw; uncertain runtime is not permission to truncate the original computation. By contrast RB-110 explicitly says one day, and RB-107’s mismatched package says 11 hours, so these are excluded. SCORE Pxp7, J999 and vaWE also fail the full-runtime criterion despite smaller individual code blocks being feasible.

User-written commands are a static inventory of observed calls, installer lists, bundled helpers and immediate dependencies. No Stata/SSC installation was performed. The lists are not solved, version-pinned transitive environments. README/code disagreements and reproducer-only versions are recorded explicitly. Original execution logs are distinguished from commands that would create a log, human reproduction logs, and TeX compilation logs. Among eligible packages, original Stata logs were found for RB-070, RB-085 and RB-104; none was found in the inspected original inventories for the other eligible papers.

Current SPEC 4.2 requires package evidence for a reporting slip: a located author correction, a donor value in executed output, or a single-character substitution with matching companion statistics. A human report’s typo/rounding explanation alone is insufficient. Exact counts and false bounds have additional vetoes. The per-candidate notes therefore identify the kind of non-recurrence, without assigning any claim outcome. RB-064 is provisionally an issue candidate because its descriptive gap is verified by the human source but a package-supported slip has not been established.

Current SPEC 4.6 reserves technical failure for demonstrated blockers preventing every primary computation in the frozen scope. SC-0P4r and RB-075/104/106 have missing computational components, but primary models elsewhere complete. They are issue candidates, not clean technical failures. An order/package/path fix, an unfinished search for output, a restricted source by design, or an unavailable website does not establish a failure. No claim list, primary subset or verdict was frozen here.

## Eligible candidates

### SC-LyWB: Administrative Unit Proliferation

**Provisional stratum:** computational issues. **Translation:** needs care. **Size:** 0.437 MB. **Runtime:** estimated 5-30 min from small input and code; not timed.

[Human source](https://osf.io/download/wep6a/); [original package or source-pinned mirror](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/26937). The unchanged Table 8 output differs from printed splinter coefficients and inference: panel A reports 0.027 but the source obtains 0.0111326 (p=0.397); panel D gives p=0.055 despite a printed p<0.05. The report also identifies mother/splinter row confusion.

**Stata:** 12.1 (version statement in original Data analysis.do). **User-written commands:** estout (eststo, esttab). **Original logs:** no.

Table 8 xtreg random effects requires matching GLS variance-component estimates and lag exclusions; Tables 4-6 use random-intercept logit and need matching quadrature if selected. Match Stata finite-sample inference.

Public SCORE mirror: data node kpb97, original code node 9vh3f. Original code has version 12.1. The analyst copied individual table blocks without altering estimators. Reproduction SMCL is separate from the original package. Non-recurrence type: Coefficient/row assignment and false significance bounds. A possible donor row does not explain the false bounds. Do not use a displayed p=0.010 alone as evidence of a threshold crossing, because it is rounded. Mapping: Tables 4-6 and 8; the report compares 37 numerical results, permitting 5-8 results that include the Table 8 differences.  Source SHA256: 5a5d26127f7a788488aa927f9d4c848a745f3315e725db0ba1ead401ff789bc7.

### SC-0P4r: Does Warfare Matter? Severity, Duration, And Outcomes Of Civil Wars

**Provisional stratum:** computational issues. **Translation:** needs care. **Size:** 0.609 MB. **Runtime:** estimated 5-30 min from sub-MB inputs and conventional models; not timed.

[Human source](https://files.osf.io/v1/resources/jcbfw/providers/osfstorage/624f12c8e6adfb017f5dec7a); [original package or source-pinned mirror](https://osf.io/jcbfw/). The final transparency trail finds no original estimation code for Table 1 PRIO100 duration models 5-8. The four printed irregular-war coefficients are 0.85, 0.82, 0.80 and 0.75, with no reproduction output. Other primary duration/outcome computations complete.

**Stata:** not stated in inspected original-material copies. **User-written commands:** estout (esttab); other dependencies not fully version-pinned. **Original logs:** no.

Weibull accelerated-failure-time models must reproduce stset calendar intervals and robust covariance, and distinguish raw coefficients from displayed time ratios. Logit/ordered-logit and severity models are otherwise conventional. The absent PRIO100 duration specifications cannot be replaced by guessed R models.

The human archive includes the original-material .do copies, three analysis datasets, and later Analysisattempt scripts. The original-material copies already show documented working-directory/data-load normalisations. Do not use the analyst-added mean calculation as evidence that the shipped code contained it. Original source route is the author-linked material described in the report. Non-recurrence type: Partial computational omission, with missing estimation code for four named models. This is computational issues under SPEC 4.6 because primary computations elsewhere complete; it is not a clean paper-wide technical failure. Mapping: The report assesses 14 results: ten computed after I/O normalisations and four PRIO100 Table 1 models with missing estimation code. A mixed 5-8-result mapping is feasible.  Source SHA256: 1a3e967833e0aaa6a767ef13725317ed77a73a5decb68f1c9d53800e65c94d5e.

### SC-a2Yx: Organizing The Global Value Chain

**Provisional stratum:** computational issues. **Translation:** straightforward. **Size:** 28.947 MB. **Runtime:** estimated 5-60 min from 29 MB data and linear models; not timed.

[Human source](https://osf.io/download/q4cgv/); [original package or source-pinned mirror](https://osf.io/qk9v3/). The report finds Table III column 7 N=207,991 rather than the printed 270,991 while the focal coefficient remains -0.115. The other assessed coefficients generally recur.

**Stata:** original target not stated in inspected scripts; human reproduction used 14. **User-written commands:** outreg2. **Original logs:** no.

Tables III-VII use OLS/absorbed fixed effects and linear Wald tests. Preserve industry clusters, absorb groups, weights and sample exclusions. Path/delimiter normalisations are separate from numerical changes.

Recovered original version 1 for Table3.do through Table7.do; the currently served version 2 contains the analyst delimiter/path normalisations. Public data node my6bg and code node zxdca. Use the source-described original snapshot, not an unidentified later author website package. Non-recurrence type: Exact sample-count non-recurrence, described by the human source as a transposition. Counts require exact agreement under SPEC 4.2, so the human typo explanation does not remove the issue. Mapping: Tables III-VII have 36 evaluated results; use the Table III sample discrepancy together with unchanged estimates to form a 5-8-result assessment.  Source SHA256: 97c20fcc792eef666c878f8da814772d1c5bd48e08a9d42177bef93b06edc1d7.

### SC-L22B: Measuring The Cost Of Privacy: A Look At The Distributional Effects Of Private Bargaining

**Provisional stratum:** computational issues. **Translation:** needs care. **Size:** 16.171 MB. **Runtime:** estimated 5-30 min from 16 MB input and short script; not timed.

[Human source](https://osf.io/download/83fd2/); [original package or source-pinned mirror](https://osf.io/gk6mh/). Unchanged public code gives Table 1 Model 3 coefficient 0.0516309 rather than 0.062 and N=12,391 rather than 12,066. Table 3 Model 6 gives p=0.009 where the paper states p<0.001.

**Stata:** original target not stated; human reproduction used 14. **User-written commands:** none observed; xtreg, margins, heckman and lrtest are built in. **Original logs:** no.

Table 1 fixed-effects GLS and clustered covariance are straightforward with matched degrees of freedom. Tables 3-4 use full-information Heckman selection and margins; match likelihood, starting values, optimisation, selection equation and clustered covariance.

Original publisher script S0007123414000520sup001.do.txt is plain Stata source, not prose-embedded code. Saving that text as .do changes no analysis. Data/code mirror nodes cz2rd/knxdw. The public reproduction output PDF is not an original execution log. Non-recurrence type: Coefficient and exact sample-count non-recurrence; false printed p-value bound. A human suggestion that the bound is a typo supplies no package erratum and does not erase the false bound. Mapping: The report compares seven results across Tables 1, 3 and 4, including the Model 3 coefficient/sample and Model 6 inference.  Source SHA256: 4890ee06357b64b5e22f4c4b5f7f72111ef8e6234133fe795c954779426d8503.

### SC-9wya: When The Money Stops: Fluctuations In Financial Remittances And Incumbent Approval In Central Eastern Europe, The Caucasus And Central Asia

**Provisional stratum:** computational issues. **Translation:** needs care. **Size:** 46.045 MB. **Runtime:** estimated 5-30 min for supplied processed-data analysis; not timed.

[Human source](https://osf.io/download/f5gvx/); [original package or source-pinned mirror](https://files.osf.io/v1/resources/h5kat/providers/osfstorage/632051bed88c07093b9d0816). The later unchanged-code reproduction gives Table 2 Model 3 coefficient 0.0462908 and p=0.166 rather than 0.064 and p<=0.01. Model 2 gives 0.0940312 rather than 0.070; Model 1 N is 1,245 rather than 1,287.

**Stata:** not stated in inspected original scripts; do not infer a version from dates. **User-written commands:** none observed in the LiK estimation .do; original figures also use R. **Original logs:** no.

The LiK xtreg calls omit fe/re and therefore use Stata random-effects GLS by default, with household and year indicators and individual panel IDs. Do not silently translate them as within fixed-effects regressions. Match variance-component and sample handling.

Opened public dataverse_files.zip despite its parent component being named Data (private). It contains the report-described V2 LiK_final_rec.dta and ReplicationCode_APSR_LiK_Revised.do. The earlier Talbert report reproduces a different Final-named snapshot; it does not override the later V2-specific evidence. Pin the ZIP. Harvard API returned HTTP 403, not evidence of a study blocker. Non-recurrence type: Coefficient, sample-count and significance non-recurrence in the source-pinned original-data/code snapshot. This is not a new clustering or robustness specification. Mapping: Five explicit Table 2/3 comparisons, each with coefficients, sample sizes and inference, support a 5-8-result mapping.  Source SHA256: af43866220a29b6409fa592d486ae28d1925b74ccaf2a2828f654670ca6526ed.

### RB-014: Cooperative Property Rights and Development: Evidence from Land Reform in El Salvador

**Provisional stratum:** computationally reproducible. **Translation:** specialised. **Size:** 4427.557 MB. **Runtime:** estimated 30-120 min; no package timing found; benchmark inclusion is secondary support.

[Human source](https://www.econstor.eu/bitstream/10419/268943/1/I4R-DP020.pdf); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/14/replication_package). DP20 reproduces original income/equity estimates before correcting duplicated observations and income construction. Those corrections do not create an unchanged-code issue.

**Stata:** 16 (README). **User-written commands:** rdrobust; rdbwselect; rdlocrand (rdrandinf); rdpower; winsor2; outreg2; outreg; estout; cmogram; dm88_1; grqreg; gr0002_3; pdslasso; lassopack; univar; ietoolkit; parmest. **Original logs:** no.

Large 4.428 GB deposited package, near the cap; public processed-data analysis is the feasible entry. R mapping/quantile components and RD bandwidth, kernel and inference defaults require care. Full raw-to-map runtime was not measured.

Mapping: Original income/equity Table 5 and distributional results compared in DP20 Tables 1/3 and Figure 1 support 5-8 results. 

### RB-033: Historical Lynchings and the Contemporary Voting Behavior of Blacks

**Provisional stratum:** computationally reproducible. **Translation:** needs care. **Size:** 865.331 MB. **Runtime:** estimated 15-120 min for supplied-data analysis; not timed; source benchmark bound is secondary support.

[Human source](https://www.econstor.eu/bitstream/10419/272843/1/I4R-DP032rev.pdf); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/33/replication_package). DP32 reproduces the original baseline before removing outliers or correcting registration rates; those subsequent changes are robustness/coding corrections.

**Stata:** not stated in inspected code/readme. **User-written commands:** psacalc; binscatter; estout; coefplot. **Original logs:** no.

The reproduced baseline is narrower than the whole original paper. ArcGIS maps are descriptive and excluded from feasible Stata result scope. Williams_Voting.log is a TeX compilation log, not a Stata execution log.

Mapping: Original Table 2 and Appendix B4 baseline columns are compared in DP32 Tables 1/3, with coefficient, SE, N and fit statistics. 

### RB-037: Immigration and Redistribution

**Provisional stratum:** computational issues. **Translation:** needs care. **Size:** 9.619 MB. **Runtime:** estimated 5-60 min from 9.6 MB package and scripts; not timed.

[Human source](https://www.econstor.eu/bitstream/10419/272841/1/I4R-DP040.pdf); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/37/replication_package). Unchanged main point estimates reproduce, but the paper describes 4,500 US respondents and 22,506 in total whereas the deposited dataset has 4,000 US respondents and 22,006 in total.

**Stata:** 17 (README; older versions said to work). **User-written commands:** winsor2; appendfile; estout; frmttable. **Original logs:** no.

Non-recurrence type: exact descriptive sample counts. Counts cannot be excused as close reporting slips. Appendix estimation code is absent, but working main computations rule out a clean technical-failure stratum. R is used for several figures; preserve the Stata sample/winsorisation and treatment contrasts.

Mapping: DP40 original-column comparisons for Figure 2 and Tables 4-6 plus the stated sample counts permit 5-8 results. 

### RB-045: Measuring the Welfare Effects of Shame and Pride

**Provisional stratum:** computationally reproducible. **Translation:** specialised. **Size:** 31.157 MB. **Runtime:** README 0.5-2 h.

[Human source](https://www.econstor.eu/bitstream/10419/276252/1/I4R-DP064.pdf); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/45/replication_package). DP64 explicitly reproduces all original results before correcting order dummies and the Table 6 coding error. The corrected estimates are not issue evidence.

**Stata:** 15 stated in README; report notes parts need a newer version. **User-written commands:** cdfplot; binscatter; estout. **Original logs:** no.

Nonlinear welfare/structural estimation and mixed models require a literal port if chosen. Restrict mapping to clearly verified original columns; keep order-dummy and preference-parameter corrections separate.

Mapping: Tables 2-6 and DP64 original-result comparisons offer 5-8 unchanged numerical results. 

### RB-057: Public Infrastructure and Economic Development: Evidence from Postal Systems

**Provisional stratum:** computationally reproducible. **Translation:** needs care. **Size:** 87.868 MB. **Runtime:** estimated 5-60 min from scripts and 88 MB package; not timed.

[Human source](https://www.econstor.eu/bitstream/10419/280689/1/I4R-DP092.pdf); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/57/replication_package). DP92 reports successful reproduction from supplied analysis data. Some upstream historical sources are proprietary, but they are not required to rerun the deposited processed-data regressions.

**Stata:** not stated in inspected README/.do. **User-written commands:** xtivreg2; ivreg2/ranktest dependencies; figures also use R. **Original logs:** no.

Do not treat unavailable proprietary upstream sources as a package failure. Match panel GLS/FE, IV, clustering and degrees of freedom. This eligible scope starts at public processed inputs, as in round 1.

Mapping: DP92 explicitly reproduces all paper results; original Tables 1-3 have many coefficient/SE comparisons. 

### RB-060: Recessions, Mortality, and Migration Bias: Evidence from the Lancashire Cotton Famine

**Provisional stratum:** computational issues. **Translation:** needs care. **Size:** 126.892 MB. **Runtime:** README about 30 min-1 h.

[Human source](https://www.econstor.eu/bitstream/10419/270605/1/I4R-DP025.pdf); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/60/replication_package). DP25 section 2 gives the 1851 minimum mortality rate as 0.569, rather than the printed 0.513, while otherwise reproducing original tables and figures.

**Stata:** not stated in inspected original code/readme. **User-written commands:** estout; geodist; gtools; grc1leg; shp2dta; spmap; ftools; reghdfe; outreg2; sutex. **Original logs:** no.

Non-recurrence type: multi-character descriptive reporting difference, identified only by the human report; no package erratum/donor evidence established. Census names are confidential upstream, but public anonymised analysis inputs are supplied. Use those inputs, not restricted reconstruction. Match weighted FE and clustered covariance.

Mapping: DP25 reproduces Figures 1-4 and Tables 1-5; include the Table 1 descriptive discrepancy alongside main estimates. 

### RB-064: Social Class and (Un)Ethical Behaviour: Causal and Correlational Evidence

**Provisional stratum:** computational issues. **Translation:** straightforward. **Size:** 45.131 MB. **Runtime:** README main Stata files 20 s, 20 s and 5 s.

[Human source](https://www.econstor.eu/bitstream/10419/270890/1/I4R-DP029.pdf); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/64/replication_package). DP29 reports an unchanged descriptive difference: Table 2 Survey 2 primed-rich religiousness is 3.8 (unrounded 3.848456), rather than printed 3.9. Original regression estimates recur without the proposed coding/imputation changes.

**Stata:** 16.1 main analysis (README; dependency section also says 16). **User-written commands:** none observed in original Stata estimation scripts; figures also use R. **Original logs:** no.

Non-recurrence type: descriptive reporting/rounding difference. The human double-rounding explanation alone is insufficient under SPEC 4.2; package evidence or matching companion statistics must still be established. Reproducible is an acceptable alternative if that evidence is recovered or scope contains only unchanged regression results. Do not count changed indicator coding or imputation as issues; figure-label swaps concern the mixed R component.

Mapping: DP29 comparison tables and the original unmodified models provide 5-8 numerical results. 

### RB-070: Targeting High Ability Entrepreneurs Using Community Information: Mechanism Design in the Field

**Provisional stratum:** computationally reproducible. **Translation:** needs care. **Size:** 18.567 MB. **Runtime:** README about 10 min.

[Human source](https://www.econstor.eu/bitstream/10419/274139/1/I4R-DP049.pdf); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/70/replication_package). DP49 reproduces original tables. Correcting the ordering/tercile-construction coding error changes Table 4 scientifically and is not unchanged-code non-recurrence.

**Stata:** 17 (README); custom program declares 15.1, user. **User-written commands:** distinct; isvar; blindschemes; lassopack; ftools; estout; pdslasso; dm88_1; bundled table/helper programs. **Original logs:** yes.

Matching post-double-selection and variable ordering needs care if those results are selected. A variable-order fix is not a clean fatal package blocker. A genuine original MASTERLOG.log ships.

Mapping: DP49 reproduces all original tables; original Tables 1-4 provide 5-8 results. 

### RB-075: The Dynamics and Spillovers of Management Interventions: Evidence from the Training within Industry Program

**Provisional stratum:** computational issues. **Translation:** needs care. **Size:** 1380.003 MB. **Runtime:** estimated 15-120 min; no original timing found; benchmark bound is secondary support.

[Human source](https://www.econstor.eu/bitstream/10419/276960/1/I4R-DP066.pdf); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/75/replication_package). DP66 section 2.1.4 and Table 3 show unexplained unchanged-code differences in Appendix Table A9 panel C; e.g., J-I x Post for log inventory is -0.037 (0.024) in print and -0.036 (0.012) in reproduction.

**Stata:** not stated in original read-me; report restores Stata 13 RNG and reghdfe 3 for particular results. **User-written commands:** reghdfe (version 3 for reference); ftools; outreg2; estout; wyoung; spmap. **Original logs:** no.

Non-recurrence type: unexplained coefficient/SE differences plus appendix reporting errors; some appendix computations also lack balanced/county variables or code. Those partial omissions do not block all primary models. Do not count differences removed by Stata 13 RNG/reghdfe 3, or R-only re-estimation differences. Full-runtime estimate is relatively uncertain for the 1.38 GB bundle.

Mapping: DP66 Tables 1-3 compare original Appendix A8/A15/A9C, and main results reproduce. A9C supplies multiple coefficient/SE pairs for 5-8 results. 

### RB-077: The Effects of Banking Competition on Growth and Financial Stability: Evidence from the National Banking Era

**Provisional stratum:** computational issues. **Translation:** specialised. **Size:** 135.068 MB. **Runtime:** README about 30 min.

[Human source](https://www.econstor.eu/bitstream/10419/286135/1/I4R-DP081update.pdf); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/77/replication_package). DP81 finds Table 9 magnitude differences and identifies FixBW.ado modifying the Fredericksburg sample after its first estimator call. Later calls therefore use a changed effective sample, also affecting Table 8 and F4.

**Stata:** 16.1 tested; minimum 15 (README/requirements). **User-written commands:** require; mdesc; winsor2; erepost; coefplot; estout; listtab; ftools; gtools; reghdfe; ppmlhdfe; scheme-sergio; rdrobust; rddensity; lpdensity; bundled FixBW, rdplot_recolored and RD helpers. **Original logs:** no.

Non-recurrence type: state/order-sensitive numeric outputs, not a fatal missing input. Pin master.do order and original helper version; classify alternative ambiguous if no determinate original-entry-point comparison can be fixed. New winsorisation/bandwidth choices are robustness changes. Exact RD kernel, bandwidth, bias correction, covariance and helper side effects make translation specialised.

Mapping: DP81 Tables 3.13.2-3.13.5 compare Table 9; unchanged main estimates and these deviations support 5-8 results. 

### RB-082: The Origin of the State: Land Productivity or Appropriability?

**Provisional stratum:** computational issues. **Translation:** needs care. **Size:** 10.978 MB. **Runtime:** estimated 5-60 min from 11 MB inputs and scripts; not timed.

[Human source](https://www.econstor.eu/bitstream/10419/280434/1/I4R-DP082rev.pdf); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/82/replication_package). DP82 Table 1 notes first-stage column 5 SE=0.029 rather than printed 0.068, alongside a missing decimal in its coefficient. Column 6 F=16.10 rather than 16.11; the land-productivity term is computed but omitted in print.

**Stata:** 15 SE (README). **User-written commands:** esta; pdslasso; lassopack (ivlasso); ivreg2; ranktest; outreg2; bundled xgmlt, x_ols, x_gmm. **Original logs:** no.

Non-recurrence type: paired coefficient/SE reporting differences and a small F-statistic difference. The SE companion does not match, so a claimed missing decimal alone does not establish a package-supported slip. Do not use new robustness specifications. Post-double-selection in column 6 and spatial helpers elsewhere require extra care.

Mapping: DP82 Table 1 explicitly reproduces original Table 1 with same data/code across six models. 

### RB-085: The Side Effects of Immunity: Malaria and African Slavery in the United States

**Provisional stratum:** computationally reproducible. **Translation:** specialised. **Size:** 269.796 MB. **Runtime:** estimated 15-120 min; no original timing found; benchmark bound is secondary support.

[Human source](https://files.osf.io/v1/resources/728ud/providers/osfstorage/65e7965285203703a388125d); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/85/replication_package). The report reproduces original tables. The small Table E2 differences follow correcting manually entered crop percentiles and are not unchanged-code failures.

**Stata:** not stated in inspected original README/.do. **User-written commands:** reghdfe; ftools; ranktest; ivreg2; ivreghdfe; outreg2; sutex; binscatter; parmest; reclink; estout; mm_regress; acreg; boottest; hdfe. **Original logs:** yes.

A missing upstream raw dataset did not affect the supplied analysis. Spatial covariance, IV/absorbed effects and wild bootstrap require literal defaults if selected. Original Table_B14_100.log and Table_D9.log ship; these are not merely TeX logs.

Mapping: The human report compares main Tables E1-E3 and later exhibits, with original columns explicitly distinguished. 

### RB-089: Wage Cyclicality and Labor Market Sorting

**Provisional stratum:** computationally reproducible. **Translation:** needs care. **Size:** 395.444 MB. **Runtime:** README approximately 2 h.

[Human source](https://www.econstor.eu/bitstream/10419/278116/1/I4R-DP078.pdf); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/89/replication_package). DP78 reproduces all main numbers using original data and code. LaTeX fragment wrapper failures do not stop the statistical computations.

**Stata:** 16 (README). **User-written commands:** reghdfe; ftools; estout; outreg; winsor; frmttable; README names egen without identifying a separate provider. **Original logs:** no.

Do not call missing begin-document wrappers technical failures. Preserve the skill-mismatch construction, high-dimensional FE, weights, covariance and percentile-dependent figure calculations.

Mapping: DP78 reproduces Tables 1/2 and Figures 2/3; its baseline columns give more than five numerical results. 

### RB-104: Web of Power: How Elite Networks Shaped War and Politics in China

**Provisional stratum:** computational issues. **Translation:** needs care. **Size:** 100.406 MB. **Runtime:** estimated 5-120 min; no original timing found; benchmark bound is secondary support.

[Human source](https://www.econstor.eu/bitstream/10419/290341/1/I4R-DP115.pdf); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/104/replication_package). DP115 finds Table I panel B code uses N=182,706 instead of the stated 1820-1910 sample N=149,786, and Table III code gives 1,110 rather than 1,125 after dropping singletons.

**Stata:** MP 16.0 (README). **User-written commands:** reghdfe; ftools; ivreghdfe; ivreg2; ranktest; outreg2; parmest. **Original logs:** yes.

Non-recurrence type: sample/reporting mismatch and dependency-sensitive singleton count. Do not count corrected fixed effects or Poisson models. The Figure III map data/shapefile was later supplied privately, while other main models complete; do not include that supplied addendum as shipped evidence. Original Results/All_in_One.log ships.

Mapping: DP115 section 2 identifies exact sample mismatches in Tables I/III/B2; matching main estimates and affected counts permit 5-8 results. 

### RB-105: Safe Assets

**Provisional stratum:** computationally reproducible. **Translation:** needs care. **Size:** 23.363 MB. **Runtime:** README empirical code seconds; simulations about 8 min.

[Human source](https://www.econstor.eu/bitstream/10419/295251/1/I4R-DP122.pdf); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/105/replication_package). DP122 runs original Stata code successfully. Table 3 original coefficients/SEs round as reported; large non-US/OECD gaps belong to the R translation or new HAC/year-effects specifications.

**Stata:** 15.1 (README); MATLAB R2019b for simulations. **User-written commands:** none observed in original Stata empirical code. **Original logs:** no.

The report does not reproduce the final real-return columns of original Table 2 and gives no precise unchanged-code comparison there. Exclude those from a verified reproducible scope. SCF input ZIPs ship; a downloaded web update must not silently replace them. Original workflow is mixed Stata/MATLAB, but the empirical Stata component stands alone.

Mapping: DP122 Tables 1, 3 and 4 provide multiple empirical comparisons; a 5-8-result Stata scope is feasible without MATLAB simulation targets. 

### RB-106: Kin Networks and Institutional Development

**Provisional stratum:** computational issues. **Translation:** needs care. **Size:** 151.964 MB. **Runtime:** README about 1 h.

[Human source](https://www.econstor.eu/bitstream/10419/296191/1/I4R-DP126.pdf); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/106/replication_package). DP126 gives Table 5 N=20,309 rather than printed 20,343, while the point estimates and SEs recur. Figures 1/2 have missing code, but main table computations complete.

**Stata:** 15.1 required (README). **User-written commands:** estout; acreg; bundled x_ols2 (modified Dube/Conley routine); other immediate helper calls as shipped. **Original logs:** no.

Non-recurrence type: exact sample-count discrepancy and partial missing figure code. Do not use replacing city-clustered SEs by Conley SEs as unchanged-code failure. Match the original acreg/x_ols2 spatial definitions when relevant, rather than inserting a convenient covariance estimator.

Mapping: DP126 reproduces Tables 1-6; Table 5 sample count plus unchanged model results permit 5-8 results. 

### RB-109: The Evolution of Access to Public Accommodations in the United States

**Provisional stratum:** computational issues. **Translation:** straightforward. **Size:** 29.446 MB. **Runtime:** estimated 5-60 min from 29 MB processed-data package; not timed.

[Human source](https://www.econstor.eu/bitstream/10419/301429/1/I4R-DP140.pdf); [original package or source-pinned mirror](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/109/replication_package). DP140 unchanged-code Table 3 panel A column 3 gives 0.0263 rather than printed 0.0191. Other main results reproduce.

**Stata:** not stated in inspected README/.do. **User-written commands:** ivreg2; ranktest; estout; parmest. **Original logs:** no.

Non-recurrence type: multi-digit coefficient difference with no demonstrated package erratum/donor. The following report sentence mentions 0.023 for a modified fixed-effects experiment; use the explicit unchanged result 0.0263 corroborated by Table A1. New White/clustered IV SEs are separate robustness checks.

Mapping: DP140 Table A1 compares six original Table 3 panel A models, supporting 5-8 results. 

## Borderline and excluded leads that matter for balance

**SC-WLkV, SC-QYNq and SC-R0ak are three source-described technical-failure leads, all excluded from the eligible count.** Their provisional descriptors in the CSV preserve what the source found; they are not ready for the draw.

- **SC-WLkV:** the supplied original Stata file creates/labels variables but contains no Mann-Whitney focal test. The source documents one comparison. A publisher listing identifies 9183data.zip, but I could not verify the public original dataset by download. Original estimation code and adequate assessed-result breadth remain unverified. The HTTP 403 itself is not the scientific blocker.
- **SC-QYNq:** the human report finds a genuine data/code mismatch. Fresh author ZIPs contain dataset.csv plus a codebook and PHP experimental stimuli, with no original .do. The saved SCORE do-file requires part, late_complete, a, b and treatment indicators absent from the CSV. It also loads a Stata-format dataset while the author file is CSV, but lossless import would not supply the missing prepared variables. Only one focal coefficient/SE/bound is documented, and original estimation-code provenance is unresolved.
- **SC-R0ak:** the report identifies missing numberofrebels in the Excel input, but original code is in a Word document. SCORE’s .do was created by the reproducer, and the human comparison concerns one focal coefficient/SE/bound. Do not admit it as an original .do package or infer a wider human numeric trail.
- **SC-0P4r:** final attempt 2 leaves original Table 1 PRIO100 models 5-8 uncomputed because the estimation code is absent. This is a genuine partial omission, with four named printed coefficients; primary duration/outcome models elsewhere compute. Its eligible stratum is issues under SPEC 4.6. Relabelling it technical failure would require a deliberately different frozen primary scope, not a change in the evidence.
- **SC-PVQK and SC-k7wj:** both have plausible unchanged-code numerical differences. Each inspected report is limited to one focal effect/model, and a broader 5-8-result human assessment was not verified. They remain excluded/borderline rather than being expanded with numbers the human source did not assess.
- **SC-9wya:** the later V2 archive is publicly accessible and supports five comparisons. The earlier successful Talbert reproduction refers to a different Final-named dataset/script. Pinning the opened V2 ZIP is essential; do not combine an early success with a later data/code snapshot.
- **RB-002 and RB-051:** the public human assessments use new R estimations of original Stata models. They can motivate further checking, but the reported differences do not establish unchanged original Stata-code failures.
- **RB-017:** Figure 4 is reconstructed as the reproducer’s best guess; other main figures reproduce. Re-adding app-level usage is a different data construction, and the author response explains the discrepancy. No precise unchanged-code 5-8-result issue/failure mapping was recovered.
- **RB-096:** the author acknowledges missing preparation chunks and a merge error, but primary estimation is in R. Changes after correcting the merge or spatial lag are not unchanged Stata non-recurrence. The old HF snapshot must not be silently replaced by the corrected 2025 package.
- **RB-107:** its article is Moretti’s High-Tech Clusters paper, but the deposited README and code identify Carrera et al.’s Who Chooses Commitment. This is a benchmark packaging mismatch, not evidence that the Moretti study shipped the wrong input.
- **RB-110:** DP144 documents a sample-count discrepancy, but the original README says about one day with Conley SEs. Its 2.77 GB size passes; its full runtime does not.

## Complete exclusion register

Every exclusion is also a CSV row. Archive-only prefilters indicate missing verified eligibility evidence in this pass; they do not claim that no current deposit exists anywhere.

| Candidate | Source | Reason |
|---|---|---|
| SC-q8xv | SCORE | No 5-8-result unchanged-original-code comparison trail established. |
| SC-RYKv | SCORE | No verified original Stata-code non-recurrence. |
| SC-EAa | SCORE | No public original code with a verified Stata workflow was established. |
| SC-JRpA | SCORE | Original workflow is R, not Stata. |
| SC-8R9d | SCORE | Original workflow is R, not Stata. |
| SC-J999 | SCORE | Full original runtime under about two hours not supported. |
| SC-Pxp7 | SCORE | Full original run exceeds about two hours in the human reproduction. |
| SC-9DZl | SCORE | Original workflow is SPSS, not Stata. |
| SC-rWbG | SCORE | No public original code with a verified Stata workflow was established. |
| SC-G4mp | SCORE | Human evidence is confined to one focal contrast, without a verified 5-8-result mapping. |
| SC-YpZZ | SCORE | No public original code with a verified Stata workflow was established. |
| SC-5Awm | SCORE | No public original code with a verified Stata workflow was established. |
| SC-AqDO | SCORE | No public original code with a verified Stata workflow was established. |
| SC-k7wj | SCORE | Human evidence is confined to one focal model; 5-8 assessed results not verified. |
| SC-PVQK | SCORE | Human comparison covers one focal effect; broader 5-8-result evidence not verified. |
| SC-zb3Y | SCORE | No public original code with a verified Stata workflow was established. |
| SC-AXBY | SCORE | No public original code with a verified Stata workflow was established. |
| SC-xYbO | SCORE | Original workflow is SPSS, not Stata. |
| SC-q4X2 | SCORE | No public original code with a verified Stata workflow was established. |
| SC-OY3B | SCORE | No public original code with a verified Stata workflow was established. |
| SC-Njqj | SCORE | No public original code with a verified Stata workflow was established. |
| SC-zK2 | SCORE | Original workflow is SPSS, not Stata. |
| SC-vaWE | SCORE | Full permutation runtime is far above the bound; open-data status also not established. |
| SC-pqzK | SCORE | No public original code with a verified Stata workflow was established. |
| SC-rjb | SCORE | Original workflow is R, not Stata. |
| SC-wRvv | SCORE | No public original code with a verified Stata workflow was established. |
| SC-qgWj | SCORE | No public original code with a verified Stata workflow was established. |
| SC-PkXJ | SCORE | No public original code with a verified Stata workflow was established. |
| SC-jDWN | SCORE | No public original code with a verified Stata workflow was established. |
| SC-GQvr | SCORE | No public original code with a verified Stata workflow was established. |
| SC-9OK1 | SCORE | Restricted data by design; negative outcomes include source-data reconstruction. |
| SC-2GKO | SCORE | No public original code with a verified Stata workflow was established. |
| SC-88xa | SCORE | No public original code with a verified Stata workflow was established. |
| SC-Z0ma | SCORE | Only one focal result and insufficient full-runtime/variation evidence. |
| SC-D2LY | SCORE | No public original code with a verified Stata workflow was established. |
| SC-9XrX | SCORE | No original Stata workflow; later report overturns initial not-attemptable lead. |
| SC-z0v1 | SCORE | No public original code with a verified Stata workflow was established. |
| SC-ky28 | SCORE | No public original code with a verified Stata workflow was established. |
| SC-exBp | SCORE | No verified unchanged original Stata-code comparison trail. |
| SC-4q0L | SCORE | No public original code with a verified Stata workflow was established. |
| SC-E5qr | SCORE | No public original code with a verified Stata workflow was established. |
| SC-3aPw | SCORE | No public original code with a verified Stata workflow was established. |
| SC-kXp8 | SCORE | No public original code with a verified Stata workflow was established. |
| SC-z4dO | SCORE | No public original code with a verified Stata workflow was established. |
| SC-qXX2 | SCORE | No public original code with a verified Stata workflow was established. |
| SC-BebG | SCORE | No public original code with a verified Stata workflow was established. |
| SC-j51N | SCORE | No public original code with a verified Stata workflow was established. |
| SC-0DO8 | SCORE | No public original code with a verified Stata workflow was established. |
| SC-R3pV | SCORE | No public original code with a verified Stata workflow was established. |
| SC-wxQZ | SCORE | No public original code with a verified Stata workflow was established. |
| SC-Z3mK | SCORE | Original workflow is R, not Stata. |
| SC-0qar | SCORE | No public original code with a verified Stata workflow was established. |
| SC-LbEB | SCORE | Original workflow is R/Stan, not Stata. |
| SC-Nv99 | SCORE | Full original runtime below about two hours not established. |
| SC-YRvg | SCORE | No public original code with a verified Stata workflow was established. |
| SC-l22v | SCORE | No public original code with a verified Stata workflow was established. |
| SC-Kj9d | SCORE | No public original code with a verified Stata workflow was established. |
| SC-G0Kb | SCORE | Original workflow is R, not Stata. |
| SC-V3pK | SCORE | No original Stata workflow verified. |
| SC-E32j | SCORE | No original Stata workflow or 5-8-result Stata human trail verified. |
| SC-WLkV | SCORE | Original estimation .do workflow, public data retrieval and 5-8-result human trail not established. |
| SC-QYNq | SCORE | Original estimation .do provenance and 5-8-result human coverage not established. |
| SC-GJe4 | SCORE | Original workflow is R, not Stata. |
| SC-R3eV | SCORE | No original Stata workflow or 5-8-result Stata human trail verified. |
| SC-R0ak | SCORE | No deposited original .do workflow; insufficient numeric human coverage. |
| RB-002 | REPRO-Bench | Human report uses R re-estimation instead of an unchanged Stata run; no qualified issue/blocker established. |
| RB-017 | REPRO-Bench | No precise 5-8-result unchanged-code numerical trail for the apparent Figure 4 problem. |
| RB-035 | REPRO-Bench | Deposited replication_package exceeds 5 GB. |
| RB-039 | REPRO-Bench | Deposited replication_package exceeds 5 GB. |
| RB-051 | REPRO-Bench | Reported non-recurrence comes from new R estimation; unchanged original Stata non-recurrence not established. |
| RB-055 | REPRO-Bench | Deposited replication_package exceeds 5 GB. |
| RB-084 | REPRO-Bench | Deposited replication_package exceeds 5 GB. |
| RB-096 | REPRO-Bench | No qualified unchanged Stata issue or 5-8-result Stata reference established. |
| RB-107 | REPRO-Bench | Benchmark package does not correspond to the article, and its README states 11 h. |
| RB-110 | REPRO-Bench | Original README states about one day, exceeding runtime criterion. |

## Audit trail and remaining validation

All downloads, inventories, exported source tables, extraction scripts, source PDFs/DOCX files, code copies, small archives and byte-range checks are under `/tmp/scratch_stata/r2-score-rb/`. Key files are `analyst.zip`, `analyst/*.csv`, `score/*/*/inventory.json`, `score/*/*/water_inventory.json`, `hf/*/tree.json`, `reports/`, `metadata.json`, `hf_access.json`, `curated_rows.json`, `details.json`, `build.py` and `notes.py`. The CSV records human-source SHA-256 values for eligible cases.

The following source snapshots are particularly important:

- SCORE analyst archive: SHA-256 `be3fcd7da8ac4d32bee0dfb330f0a50ce744996c378af41c0a45b81622ac29fd`.
- SC-9wya original V2 ZIP: SHA-256 `752d95939b0bd9f00792476cb34e443cee3b7ad8ef74f9799ac0f25400f50f57`.
- SC-a2Yx Table III original version 1: SHA-256 `c309df0bd00581d2e2e9ae9613f95f63c795b6f2129753d6817d75ceb158ffb1`.
- SC-0P4r final attempt-2 report: SHA-256 `1a3e967833e0aaa6a767ef13725317ed77a73a5decb68f1c9d53800e65c94d5e`.

Before a draw, resolve scope-sensitive strata (especially RB-064 and RB-077), verify full runtimes where estimated, pin original inputs and dependency versions, and check any proposed package-supported slip against actual companion statistics/output. None of that has been replaced with an analysis run here. Only the two requested repository outputs were written, no Stata was installed or run, and no commit was made.
