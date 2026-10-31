# Label reconciliation log

Two independent label sets: `labels/sol/` (GPT-6.1 Sol) and `labels/claude/` (Claude, six blind
labellers). Compared with `scripts/compare_labels.py`.

## Round 1 (Claude's proposals; Sol to respond item by item)

First comparison: paper-level status agreed on 25/30 papers, claim status on 157/166 claims.
G-14 is excluded from this count: its claim list was revised (5 to 6 claims) after Claude's
labeller had read it, so Claude is relabelling it blind against the current list.

### Proposed general rules

- **R1. Paper-level status for papers with abstention claims.** `computation not checked` means no
  computational verification was attempted (rule pack section 11). It is wrong for a paper where
  most claims were checked. Paper status follows the checked outputs; `not_checkable` claims caused
  by unstated choices do not change paper status by themselves. A shipped-code blocker on some
  outputs gives `computational issues`; a blocker on the primary claims gives `technical failure`.
  The sampling stratum "ambiguous" is about claim-level abstention, not a paper status.
- **R2. Severity.** P1 = point estimate or test statistic of a primary (pre-registered or headline)
  hypothesis test. P2 = any other wrong printed number: secondary or exploratory results,
  descriptives, counts, SEs or CI bounds where the point estimate and p-value are right. P3 =
  labelling or display problems with no wrong number. A truncation error that makes the printed
  value wrong at printed precision is P2, not P3.
- **R3. Claim-level alternatives.** Add `acceptable_statuses` per claim for genuinely borderline
  cases (e.g. `close` vs `not_checkable` for seed-dependent intervals). The scorer will accept any
  listed status; the headline status stays the expected one.
- **R4. Lossless edits (rule pack section 3).** Path fixes, adding missing `library()` calls,
  `git lfs pull`, replacing `file.choose()` with the deposited file path, and running the authors'
  own scripts in their intended order are lossless and do not make a claim P0. Renaming functions or
  objects, reordering logic, editing data, or substituting intermediate files are not lossless; if a
  claim needs them, it is `not_checkable` with P0.
- **R5. Reference values.** Where one labeller gives a sourced `reference_recomputed` and the other
  gives null, the gold record takes the sourced value. Values taken from the authors' own shipped
  rendered output (HTML/PDF/log) are recorded with provenance `shipped_output`, values from the
  human report with provenance `source_report`, values from direct static checks with
  `direct_check`.
- **R6. Claims must have a printed number.** A claim whose `reported` value is not a number (e.g.
  "bootstrapped 95% CIs") is replaced by another assessed numerical claim from the same paper.

### Item proposals

| Item | Sol | Claude | Proposal |
|---|---|---|---|
| G-07 C1 severity | P2 | P3 | P2 (R2: a wrong descriptive SD, 0.14 vs 1.14) |
| G-08 C4 | match | close | close (0.198 rounds to 0.20, printed 0.19); acceptable: match |
| G-16 C3 severity | P1 | P2 | P2 if the 6.5 pp result is exploratory/non-preregistered (Claude's reading); Sol to confirm whether the paper treats it as a primary test |
| G-16 C5 | close | not_checkable | close with acceptable not_checkable; the report covers Fig. 2 only qualitatively ("smaller differences in decimals") |
| G-22 C1 severity | P1 | P3 | P2 (R2: SE truncation, secondary model) |
| G-22 C4 severity | P1 | P2 | P2 (R2: CI sign error; point estimate and p correct) |
| G-26 paper | not checked | reproducible | computationally reproducible, alt computational issues (R1). C1 not_checkable, severity null (path fix is lossless under R4; the 11,016 vs 11,018 difference is gender-package version dependence) |
| G-27 paper | not checked | technical failure | technical failure, alt computational issues. SCORE push-button completed no claims; the shipped script needs renamed functions and an undefined object (`binary` vs `bin`) fixed, which R4 treats as non-lossless. C1-C5 not_checkable (unseeded bootstrap), C6 not_checkable P0 with acceptable discrepant |
| G-28 paper | not checked | computational issues | computational issues, alt computationally reproducible. C1/C2 not_checkable P0: Claude checked that `KSS_data.csv` lacks the `time` column the KSS script filters on, so the subset cannot be built (and no seed is set). Sol to check |
| G-28 C5 | close (0.52) | not_checkable P0 | Sol to check which contrast the report's 0.52 refers to. Claude reads it as yellow-bright vs blue-dim, not the overall condition effect printed as 0.62 |
| G-29 C1-C3 | not_checkable | close | not_checkable with acceptable close (R3): point estimates identical, CI endpoints move up to 0.2 between runs despite a seed |
| G-29 C4-C5 severity | null | P0 | null: no code exists for the critical-sentence medians, so this is an underspecified procedure, not a shipped-code blocker |
| G-29 paper | not checked | computational issues | computational issues, alt computationally reproducible (chi-squared 0.65 vs 2.43 and the Study 4 preprocessing failure are documented outputs that do not recur) |
| G-30 paper | not checked | reproducible | computationally reproducible (R1) |
| G-30 C1-C2 | not_checkable | not_checkable | replace both under R6 with one or two numerical claims the report assessed |
| G-14 | issues; C1-C3, C5 discrepant P2 | same after blind relabel | agreed: computational issues; Claude listed acceptable alt `computationally reproducible` (report's overall verdict); proposal: no paper alternative, since four printed counts are wrong |

### Claim-list corrections raised by Claude's labellers (Sol to verify and apply)

- G-19 C6: exhibit says "model 3", but 1.48 comes from the model adding social desirability bias
  (Model 2 in the code; Model 3 gives 1.45). Correct the exhibit to where 1.48 is printed.
- G-21 C1: exhibit says "Figure 6"; the value is in Fig. 8 (p. 1021).
- G-25 C3: the claim's 0.47 comes from the 2025 Author Correction (doi 10.1038/s41562-025-02299-y);
  the original article printed 0.36, and the pinned commit predates the correction. Proposal: use
  the original article's 0.36 and note the correction, since the gold refers to the pinned package.
- G-29 C6: exhibit says "Experiments 1-3 combined"; in the paper beta = 0.16 is the race-trial
  analysis across experiments 1-4.
- G-04: the report gives only blanket statements ("all the main results", "fully reproducible");
  the one number it presents (b = 1.64) matches no claim. Keep with label_confidence low and flag
  for a human rerun, unless Sol finds a better-evidenced substitute in the reserve.
- G-04, G-12, G-22: the version pins omit the data files the code needs. Add them.

## Round 1: Sol's responses

I checked the downloaded articles, human reports, and deposited files, and ran targeted checks
for G-19 and G-30. I changed only `claims/`, `labels/sol/`, and this appended section;
`labels/claude/` is untouched. This round does **not** establish full agreement. In particular,
new execution evidence overturns our shared G-19 blocker, and the repaired-input problem also
affects G-27 C7/C8. No full-paper rerun is claimed.

### General rules

- **R1 — AGREE.** Abstaining on some claims does not mean computation was not checked for
  the paper. Apply the proposed primary-versus-secondary blocker distinction, and keep the
  ambiguous sampling stratum separate from the paper verdict. Removed my old use of
  `computation not checked` for G-16's paper alternative and G-26–G-30's primary labels.
- **R2 — AGREE**, as the pilot's explicit severity convention. A wrong descriptive number,
  count, secondary SE, or CI sign is P2, even when the scientific conclusion is unchanged.
  P3 is reserved for problems without an incorrect numerical quantity. This resolves G-07
  C1 and G-22 C1/C4. Non-preregistration alone does not prove secondary status, but the
  G-16 restricted-policy analysis is identified as exploratory by the report and explicitly
  non-preregistered in the article.
- **R3 — AGREE.** Added `acceptable_statuses` containing the primary and defensible
  alternatives for G-08 C4, G-16 C3/C5, and G-29 C1–C3. G-26 C2–C5 also record the
  source-report versus strict shipped-R interpretation. An alternative is not permission to
  use altered inputs or treat any repaired output as an original-code discrepancy. The current
  comparison script does not inspect these lists.
- **R4 — DISAGREE with the blanket prohibition on renaming or ordering.** The rule pack
  requires an edit to be lossless and documented; spelling alone does not determine that.
  Counter-proposal: allow a path/identifier/API alias or dependency-preserving execution order
  only when its equivalence is demonstrated; prohibit changes to data, models, logic, or
  intermediate inputs without that proof. The named path/library/LFS/file-selector fixes and
  authors' intended script order are acceptable. G-27's combined intermediate substitution and
  changed function arguments are not demonstrated lossless. Conversely, the G-19 filename
  issue **is** lossless: the original activity data already exist, and the original expressions
  reproduce all three summaries after correcting only the input path (details below).
- **R5 — DISAGREE as an unconditional fill-null rule; AGREE with the provenance categories.**
  A number must identify the same claim, precision, inputs, and computational procedure.
  Counter-proposal: put a defensible same-workflow value in `reference_recomputed` with
  `reference_provenance`, `reference_evidence`, and `reference_scope`. Keep repaired-run,
  translated-analysis, or lower-precision corroboration in `diagnostic_results` with
  `is_scoring_reference: false`. A report's column quoting the original paper is not itself
  a rerun. Where an explicit original-workflow reproduction statement supports the printed
  original value, identify that indirect support rather than claiming a separately printed run
  log. This distinction is recorded for G-30. Applied the supported reference additions and
  retained the other numbers as diagnostics, as itemised below.
- **R6 — AGREE.** Require printed numerical quantities, allowing numeric strings with units,
  intervals, or bundled numerical cells. A printed confidence level without endpoint values
  does not supply a CI target. Retired G-30 C1/C2 and added **G-30 C7/C8**, without reusing
  IDs. Their claims file contains no verdicts; their labels are only in `labels/sol/`.

### Responses to every item proposal

- **G-07 C1 — AGREE: P2.** The SD is numerically wrong, not merely a display problem.
- **G-08 C4 — AGREE: close, acceptable match.** The report gives 19.8%, corresponding to
  0.198; conventional rounding gives 0.20, rather than the printed 0.19. Recorded the source
  value and the explicitly permitted report-based interpretation.
- **G-16 C3 — AGREE: P2.** The article's Results says estimation of the Restricted Targeted
  Policy was not preregistered; the human report calls it exploratory. The 6.5 pp passage is
  specifically about that policy. This is not the primary treatment test. Retained 4.9 as the
  source reference and added acceptable `not_checkable` for the unresolved RDS/input-version
  issue already documented in my previous rationale.
- **G-16 C5 — AGREE: close, acceptable not_checkable.** Figure 2 is discussed only
  qualitatively; the report gives no separate recomputed scalar for the printed −2.3 pp.
  Reference remains null, without inventing an estimate.
- **G-22 C1 — AGREE: P2.** The source gives 0.07849, which rounds to 0.08 rather than
  0.07. A secondary-model SE truncation is not P1 or P3 under R2.
- **G-22 C4 — AGREE: P2.** The rendered original output gives positive CI bounds 0.09–0.40;
  the printed negative signs are wrong while the point estimate and p-value recur.
- **G-26 paper/C1 — AGREE with the proposed paper headline, alternative, and null C1
  severity, but provisionally.** Set `computationally reproducible`, alternative
  `computational issues`, and `label_confidence: low`. The path correction is lossless; the
  11,018 versus 11,016 sample is environment dependent. A further evidence limitation matters:
  report section 2 explicitly translates the second-stage cleaning and regressions to Stata.
  The original-R analysis was not run by that report. Keep those numbers as diagnostic
  corroboration and require a pinned-R rerun before freezing a fully evidenced R-only gold
  result; C2–C5 accept `not_checkable` under that strict reading.
- **G-27 paper/C1–C6 — DISAGREE in part.** Agree with `technical failure`, alternative
  `computational issues`, and C1–C6 `not_checkable`. Counter-proposal: **P0 for every output
  downstream of the pre-output blocker, including C1–C5**; their additional unseeded-bootstrap
  uncertainty does not cancel that blocker. Do not accept C6 `discrepant` merely from repaired
  version 3: the report itself says its difference could result from the code changes. Retain
  2.9574 as a repaired-run diagnostic. The same input-provenance objection also affects C7/C8,
  as detailed under additional findings.
- **G-28 paper/C1/C2 — AGREE: computational issues**, alternative
  `computationally reproducible`; C1/C2 `not_checkable` P0. Direct inspection confirms
  `KSS_data.csv` has exactly `PB_No, appointment, condition, KSS_value, KSS_no, gender`,
  with no `time`. The pinned script filters `time == "Evening_1"`, and the pooled data do not
  provide a documented mapping to that evening. The report narrative's 0.11/0.05 remain
  diagnostics because the subset is unresolved; its Table 1 instead gives interaction BF
  0.01 and calls it matched. Unseeded sampling is an additional limitation.
- **G-28 C5 — AGREE: not_checkable P0, reference null.** Table 1 S2 labels 0.52 as the
  **yellow-bright versus blue-dim** condition difference. It is not an identified recomputation
  of the overall condition BF 0.62. Removed my incorrect substitution and the close label.
- **G-29 C1–C3 — AGREE: not_checkable, acceptable close.** The original script does set
  `set.seed(999)` once. The report observes CI shifts up to 0.2 percentage points; execution/RNG
  state, rather than simply an absent seed, remains the uncertainty. No exact new bounds exist.
- **G-29 C4–C5 severity — AGREE: null.** No operational definition or corresponding median
  calculation is supplied; this is underspecification rather than a demonstrated fatal step for
  these particular claims.
- **G-29 paper — AGREE: computational issues**, alternative `computationally reproducible`.
  The separate chi-squared difference (0.65 versus 2.4272) and Study 4 preprocessing failure
  support the headline; they do not turn the selected ambiguous claims into known discrepancies.
- **G-30 paper — AGREE: computationally reproducible.** The numerical analyses are assessed
  as reproduced by section 2 of the report. I also checked its apparent six-versus-seven
  exclusion criticism before accepting this verdict; it compares different denominators and
  does not establish a wrong printed count (details below).
- **G-30 C1–C2 — AGREE: replace under R6.** Retired the graphical targets and added C7/C8,
  two numerical Study 2A tests explicitly covered by the report's original regression/t-test
  reproduction statement and printed comparison table. Please label the new IDs blind before
  opening my G-30 labels.
- **G-14 — AGREE.** Keep `computational issues`, the four P2 count discrepancies, and no
  paper alternative. The report's favourable aggregate description does not erase the verified
  wrong printed counts. No further claim-list revision is needed here.

### Responses to every claim-list correction

- **G-19 C6 — AGREE.** Changed the exhibit to the social-desirability-controlled model,
  code **Model 2**. The article prints 1.48 in this paragraph; its later moderation model
  prints 1.45. My targeted evaluation of the authors' Model 2 expression gives
  **1.47641713313**. Model 1 also gives C4 **1.6412610274** and C5 **0.7729283248**.
  These are direct-check references, with local audit scripts, input hashes, and environment
  identified in the labels. The fitted models emit singular-fit warnings; they reproduce the
  printed coefficients.
- **G-21 C1 — AGREE, and extend to C2–C5.** All five claim exhibits incorrectly named
  Figure 6. The Experiment 3 Results and p.1021 caption identify **Figure 8** for the full
  model comparison. Changed all five exhibits.
- **G-25 C3 — AGREE.** Set reported to **0.36**, targeting the original 2023 article and
  the pre-correction commit. The original downloaded article prints 0.36 in the abstract and
  genetic-correlation results. The [Author Correction](https://www.nature.com/articles/s41562-025-02299-y),
  published 11 August 2025, documents the change to 0.47. Added the article-version note and
  correction provenance; the shipped-code P0 label is unchanged. The correction notice was
  readable in the downloaded HTML; a fresh browser fetch hit Nature's inaccessible login
  redirect, so that fresh request is not claimed as new verification.
- **G-29 C6 — AGREE.** The article says it combines individual data from **Experiments
  1–4**, then reports beta 0.16 for the **race trials**, associated with Figure 2b. Corrected
  both the exhibit and claim wording; the coefficient is unchanged.
- **G-04 — AGREE: retain, low confidence, human rerun required.** The blanket reproduction
  statement is evidence, but no claim-specific number is printed for these six coefficients.
  The unexplained b=1.64 is not a substitute. Set `requires_human_rerun: true`, left the
  references null, and did not introduce an unverified reserve replacement. This remains a
  pre-freeze evidence gap, not a completed human rerun.
- **G-04/G-12/G-22 data pins — AGREE.** Added exact OSF file IDs, versions, SHA-256 hashes,
  paths, and download URLs in `package.data_files` and extended `version_pin`. G-04 now
  includes all five raw/clean CSVs and the predictions spreadsheet; G-12 includes its three
  deposited analysis CSVs; G-22 includes the deposited spreadsheet inputs and data archives,
  retaining original-file versus later-directory paths. These are inventory/hash pins, not a
  claim that every file or dependency has been rerun. Added the specific G-19 inputs used in
  my checks and G-30 UK raw file for the additional diagnostic check.

### Reference-value differences and additional findings

**Reference-only decisions.** AGREE with adding the sourced references for G-01 C1–C5,
G-02 C1/C2, G-05 C1–C6, G-06 C1–C5, G-08 C3–C5, and G-17 C5/C6, each with provenance.
G-19 C4–C6 now have my own targeted-run values. Retain my **G-15 C3 = 0.75**: report
section 2.2 explicitly says the primary effect sizes reproduced and prints that value.
G-20 C3 `7` versus `seven`, and G-22 C4 `[0.09, 0.4]` versus `[0.09, 0.40]`, are semantic
agreement with representation differences; keep numeric/structured values in my labels.
G-30 C3–C6 get report-supported original values with the support's scope explicitly qualified.

**G-03 C1–C6 — DISAGREE with the proposed precise recomputed references.** The report's
Table 1 `Original` column quotes the paper's three-significant-figure values. The actual shipped
`Study 1a/tableS3.csv`, `X021D` rows, prints adjusted p-values of **2.1e-04, 6.8e-09,
4.3e-05, 3.1e-06, 3.3e-08, 4.5e-05** for the six claims. Those corroborate the article only
at two significant figures. Counter-proposal: keep the match judgement from the report's
explicit reproduction statement, leave precise recomputed references null until a full-precision
rerun, and retain the actual CSV values as `shipped_output` diagnostics. Do not add a third
digit by copying the paper.

**G-25 C1; G-26 C1–C5; G-27 C1–C8; G-28 C1/C2 — DISAGREE with treating all supplied
numbers as canonical same-workflow references.** G-25's 0.66 follows variable replacements
and reordering; G-26's analysis is translated to Stata (and its count is environment dependent);
G-27's outputs follow substituted intermediate inputs and altered functions/arguments; G-28's
KSS subset is unresolved. Counter-proposal: retain every supplied numerical value with source
and method in `diagnostic_results`; use null for an unestablished original-workflow reference.
This preserves evidence without asking the scorer to reward repairs as faithful execution.

**G-19 C1–C3 and paper — DISAGREE with both original label sets; new direct evidence.**
The shared P0 rested on a missing filename. OSF file **659c057d5e925a0bdc45b93e**,
`s2_data_actions.csv` version 1, was deposited **8 January 2024**, before pinned script revision
6 on **27 March 2024**. Its downloaded SHA-256 is
`89e1deb53407bd4b6aebc27c51e04c9b8627e8ec7203147410addd017103bd48`, matching the
archived OSF inventory. The report's Study 2 and Conclusion explicitly explain that the author
fixed the called filename. Pointing revision 6's original input read at this deposited file and
evaluating its original count/summary expressions yields:

- C1 PEB mean **2.110497237569**, printed 2.11;
- C2 PEB SD **0.976928449696**, printed 0.98;
- C3 Fun mean **2.301136363636**, printed 2.30.

Counter-proposal, applied to my labels: **C1–C3 match, severity null; paper computationally
reproducible** under R4's documented lossless path rule. No data content, formula, or script
revision is replaced. The inputs and historical code remain pinned. Audit:
`model-gating/gold-set/audit/check_g19_actions.R` and `check_g19_actions.log`.

**G-27 C7/C8 — DISAGREE with our shared match labels.** SCORE's own trail says no
push-button claims completed; its successful values are from the same run that deletes the
first 30 lines and loads `Cleaning File.Rdata`. Both C7's row-count correlation and C8's
unique-response test depend on the cleaning output `con`. A downstream statistic being
deterministic does not show that this substituted input equals revision 1's intended input.
Counter-proposal, applied: **not_checkable P0**, with 0.1697285 and 16.908 as repaired-run
diagnostics. To restore match, demonstrate equality to the intended processed input or rerun the
original cleaning with lossless repairs. For C1–C5, the same blocker gives P0 in addition to the
RNG uncertainty; no need to invent original bootstrap targets.

**G-30 exclusion criticism — DISAGREE with the P3 typo assertion in Claude's notes.**
The [original supplement](https://static-content.springer.com/esm/art%3A10.1038%2Fs41562-023-01769-5/MediaObjects/41562_2023_1769_MOESM1_ESM.pdf),
p.22, explicitly describes six duplicate exclusions **among the 1,073 participants who received
a payment code**. The original code deduplicates earlier. A targeted evaluation on deposited
`Study2A_RAW_UK_deidentified.xlsx` (download hash verified against the OSF inventory) drops
seven rows overall, of which **six have positive `num_total_answers` and one has zero**.
The final UK sample is **1,067**, as printed. The report's seven-row observation therefore
does not establish a wrong six-completer statement. Counter-proposal: remove the typo assertion;
do not assign either P2 or P3 without matching the conditioning set. This leaves the proposed
paper verdict intact. Audit: `model-gating/gold-set/audit/check_g30.R`,
`check_g30_counts.R`, and `check_g30_completed.log`.

**R1/R2 consistency in Claude's notes.** Remove the G-04 `computation not checked` paper
alternative if verification was attempted; low claim-level confidence and a required rerun
express the actual evidence gap. The G-29 notes' wrong signed z statistic, if retained as a
numerical error, is P2 under the proposed R2, rather than P3. Neither is a new scored claim.

### New IDs and remaining reconciliation

**New blind labels required: G-30 C7 and G-30 C8.** C1/C2 are retired. The 30 current claim
files still contain **167 claims**, six for G-30. Its replacement labels were written only to
`labels/sol/G-30.json`; no verdict is placed in the shared claims file.

The raw comparison after these edits gives **29/30 paper headlines** and **156/165 shared
claim headlines** agreeing. Four of the nine status differences are explicitly accepted under
R3 (G-16 C5 and G-29 C1–C3); five are substantive new objections (G-19 C1–C3, G-27 C7/C8).
The comparison also reports the intentionally retired/new G-30 IDs and unresolved reference
and severity representations; it does not score alternatives or diagnostic provenance. G-19's
paper is the remaining paper-headline disagreement. G-04 and strict shipped-R verification
for G-26 remain evidence gaps before gold-set freeze. No commit was made.

## Round 2 (Claude)

Claude accepts all of Sol's round-1 counter-proposals: R4 as amended (renames, aliases and
execution order are allowed only when equivalence is demonstrated), R5 as amended (repaired-run,
translated or lower-precision values go to `diagnostic_results` with
`is_scoring_reference: false`), P0 for all G-27 outputs including C7/C8, G-19 C1-C3 `match` with
the paper `computationally reproducible`, G-03 references left null, and removal of the G-30
exclusion-typo note and the G-04 `computation not checked` alternative. Claude's labels were
updated accordingly. Claude's G-30 labeller labelled the new C7/C8 blind; both `match`, agreeing
with Sol.

Comparison after these updates: paper status 30/30, claim status 167/167, severity 167/167.
The remaining reference differences are all cases where Sol, under amended R5, keeps the value as a
diagnostic rather than a scoring reference.

Proposed final rules:

- **R7. Paper-level alternatives.** Accept an alternative only at a genuine category boundary: a
  lossless-edit boundary, version or stochastic noise, or a partial blocker. A paper with a confirmed
  wrong printed number does not get `computationally reproducible` as an alternative, even when the
  source's overall verdict was favourable, because claim-level scoring would otherwise conflict with
  paper-level scoring. Hence: no alternative for G-07, G-14, G-18, G-21, G-22 (Sol's position);
  keep Sol's G-08 alternative; add `computational issues` as an alternative for G-11 (two claims
  `close` from environment-dependent matching) and G-19 (the shipped script names a missing input
  file, so a reproducer may reasonably flag it).
- **R8. Merge.** Gold records take Sol's curated references, diagnostics and provenance; claim-level
  `acceptable_statuses` are the union of both labellers' lists; `label_confidence` is the lower of
  the two; Claude's rationale is kept as `second_labeller_rationale`.
- **R9. Rerun flags.** `requires_human_rerun` is set for G-04 (blanket statements only) and G-26
  (Stata re-implementation; shipped R not run). Gold v1.0 is frozen with these two flags as
  documented evidence gaps.

Merged output: `gold/G-01.json` to `gold/G-30.json` and `gold-summary.csv`, built by
`scripts/build_gold.py`. Distribution: 14 computationally reproducible, 12 computational issues,
4 technical failure. Claims: 101 match, 8 close, 26 discrepant (3 P1, 23 P2), 32 not_checkable.

## Round 2: Sol's responses

I audited the existing 30 merged records and all 167 claims against the shared claim lists,
both label sets, amended R4/R5, and the round-1 decisions. I also inspected the retained
reports and targeted-check logs where the final explanations raised a question, and
rechecked the pinned G-14 CSV counts and G-21 script. This is a final record/provenance
audit, not a new end-to-end rerun of the 30 packages. The source records agree on all
30 paper headlines, all 167 claim statuses, and all 167 severities. That agreement does
not by itself resolve the stale explanations or the severity-rule inconsistency below.

### R7, R8 and R9

- **R7 — AGREE.** Alternatives must describe an identified category boundary, rather than
  compensate for a favourable source summary. Keep the stated exclusions for G-07,
  G-14, G-18, G-21 and G-22, and retain G-08's documented figure-code boundary.
  **G-11: AGREE** to `computational issues` as an alternative: C2/C5 are close,
  environment-dependent matched-sample results, not established deterministic errors.
  **G-19: AGREE** to `computational issues` as the narrow paper-level interpretation of
  the deposited script's incorrect input filename. This does not restore a missing-data
  P0, a technical-failure alternative, or abstention on C1-C3: the deposited input and
  lossless repair are established, and all six selected claims remain match. I added
  these two paper alternatives to my own label files as well; the built records already
  contain them through the script's R7 additions.
- **R8 — AGREE with the merge policy; the current narrative inputs need correction.**
  Sol's curated references/diagnostics, the union of accepted claim statuses, and the
  lower confidence are appropriate. Keep Claude's rationale, but it must explain the
  reconciled judgement. Copying a pre-reconciliation rationale into a field named
  `second_labeller_rationale` does not make it a final supporting rationale. In
  particular, rejected interpretations must not remain described as “live alternatives”.
  Counter-proposal for implementation: update the affected Claude rationales before
  rebuilding; retain original blind notes only with an explicit historical/superseded
  label and a current adjudication beside them.
- **R9 — AGREE for this versioned development benchmark.** G-04 and G-26 can remain
  explicitly provisional, low-confidence records in a frozen development snapshot,
  with the two unresolved rerun flags visible. This supersedes my earlier demand that
  those reruns precede any freeze. It does not establish claim-specific execution for
  G-04 or shipped-R execution for G-26. Keep their references null, keep G-26's Stata
  values diagnostic, and retain its C2-C5 `not_checkable` alternatives. I updated my
  G-04 notes/rationales to express this decision without implying precision-verified
  claim-specific results. The two reruns are outstanding evidence work, not additional
  blockers to the qualified development freeze proposed by R9.

### Mechanical audit of the existing merged files

All 30 records have exactly the current claim IDs, with no duplicates, omissions or
retired G-30 C1/C2 entries. The shared claim fields, including reported values and
exhibits, were copied without accidental label-field overrides. Every merged status,
severity, numerical reference, diagnostic and provenance field comes from the intended
input. Every `second_labeller_rationale` exactly matches its Claude input; the problems
below are stale input text, not an indexing error in the builder. The acceptable-status
unions include the primary status and no unexpected status. Paper alternatives and the
lower-confidence rule match the build policy. Both rerun flags and every summary-CSV
row agree with the JSON records.

The existing outputs contain 14 reproducible papers, 12 with computational issues and
4 technical failures; 101 match, 8 close, 26 discrepant and 32 not_checkable claims.
Discrepancies comprise 3 P1 and 23 P2 labels; 26 not_checkable claims have P0. There are
101 non-null scoring references (89 source_report, 10 direct_check, 2 shipped_output)
and 22 diagnostic entries, all explicitly `is_scoring_reference: false`. In particular,
G-03, G-25 C1, G-26, G-27 and G-28 C1/C2 diagnostics have not leaked into scoring
references. G-28 C5 correctly has no substituted 0.52 reference. G-30's qualified
report-supported references do not claim a separate original-run numerical log.

The remaining raw comparison differences are **not all diagnostic-versus-reference
cases**, as the preceding round-2 summary suggests. They also include sourced Sol
references versus Claude nulls (G-15 C3 and G-19 C1-C3), `7` versus `seven` (G-20 C3),
and interval formatting (G-22 C4). R8 handles these correctly; they do not constitute
new disagreements in the scored labels.

The table records the per-paper check. Counts are match/close/discrepant/not_checkable
in the existing gold files. “Metadata corrected” means I changed an authorised source
file; the gold output still needs rebuilding.

| Paper | Claims: M/C/D/N | Values, exhibits, references, diagnostics and final interpretation |
|---|---:|---|
| G-01 | 5/0/0/0 | Pooled estimate/CI and forest-plot Q, I-squared and N references retained; stale Sol null-reference note corrected. |
| G-02 | 5/0/0/0 | Original baseline columns and report-to-paper column mapping retained; no robustness coefficient substituted. |
| G-03 | 6/0/0/0 | Printed Supplementary Table 2 targets retained; references null, six coarse CSV diagnostics non-scoring; precision qualification corrected. |
| G-04 | 6/0/0/0 | Blanket-report matches remain provisional, six null references and low confidence; R9 note/rationales corrected; Claude historical note needs qualification. |
| G-05 | 6/0/0/0 | Original lfe coefficients retained; fixest/Stata alternatives excluded from the references. |
| G-06 | 5/0/0/0 | Original Table 1/A3 coefficients and SE retained; reconstructed measures/multiverse excluded. |
| G-07 | 5/0/1/0 | Final published SD 0.14 versus 1.14, P2, no reproducible paper alternative; Claude note still contradicts this. |
| G-08 | 4/1/0/0 | 0.198 versus 0.19 remains close with match accepted; percentage-to-coefficient mapping documented; figure-code paper alternative retained. |
| G-09 | 5/0/0/0 | Selected per-trait models and resource mean retained; reconstructed omnibus analysis remains outside scope. |
| G-10 | 5/0/0/0 | LR statistics/SE retained; Stata Wald tests excluded; C1/C4/C5 references remain null. |
| G-11 | 4/2/0/0 | Matched-column gaps 0.002/0.005 retained as close; R7 paper alternative accepted. |
| G-12 | 5/0/0/0 | Report-supported Wilcoxon matches, null scalar references and processed-data scope retained; Claude's missing-data-pin note is obsolete. |
| G-13 | 2/0/3/0 | NoChanges SEs 0.07 retained; the three agreed P1 labels need the explicit R2 clarification in B2 below. |
| G-14 | 2/0/4/0 | Rechecked pinned CSV: 370 rows, Binary 132, Categoric 180, Decide 336, Create 34; direct-check provenance strengthened; Claude paper alternative is obsolete. |
| G-15 | 4/0/2/0 | Secondary beta/SE discrepancy retained; d=0.75 remains a sourced reference; version-dependent Wald tests excluded. |
| G-16 | 0/4/1/0 | 4.9 versus 6.5 remains P2 with abstention accepted; no invented C5 scalar; false statement that the shipped table disagrees with text corrected. |
| G-17 | 2/0/4/0 | Four secondary predicted means and two matching primary statistics retained; source-report scope and medium confidence retained. |
| G-18 | 3/0/2/0 | Effect-size swap remains two P2 discrepancies; F/t references retained; Claude's reproducible/P3 suggestions are obsolete. |
| G-19 | 6/0/0/0 | All six direct-check values agree with retained logs; C6 Model 2 exhibit retained; Study 1 evidence pointer corrected; Claude C1-C3 explanations and notes still reject the accepted repair. |
| G-20 | 2/0/3/0 | Ages/exclusion count remain P2; seven is numeric 7 in the reference; face-model processed-input scope and null coefficient references retained. |
| G-21 | 4/0/1/0 | Printed values unchanged; numerical-paragraph exhibit and mixed-effects reference scope clarified as detailed below; no reproducible paper alternative. |
| G-22 | 1/0/5/0 | Truncated SE, intercept and CI errors remain P2; two shipped-HTML provenance links strengthened; Claude paper alternative/pin note is obsolete. |
| G-23 | 0/0/0/5 | Original-version missing-object blocker retained; correspondence-repaired output is not a reference. |
| G-24 | 0/0/0/5 | Pinned manuscript/update parse blockers retained with medium confidence; no repaired Table 1 values invented. |
| G-25 | 0/0/0/5 | Original 2023 C3=0.36 target retained; 0.66 repaired-run diagnostic only; Claude's old 0.47/reference/match note is obsolete. |
| G-26 | 4/0/0/1 | Version-sensitive count and translated Stata coefficients remain diagnostics; R9 flag and strict-R claim alternatives retained; C1's Claude “live” discrepant alternative is rejected. |
| G-27 | 0/0/0/8 | All eight P0 blockers retained; all repaired-run quantities diagnostic only; no C6 discrepant alternative; Claude rationales need final input-provenance explanation. |
| G-28 | 2/1/0/3 | Missing KSS time column supports C1/C2/C5 P0; 0.11/0.05 diagnostics only, no 0.52 substitution; primary BF references and stochastic close retained. |
| G-29 | 2/0/0/5 | Seed-state CI ambiguity and undefined critical-sentence timings retained; C6 race trials cover Experiments 1-4; Claude notes/rationales need updates. |
| G-30 | 6/0/0/0 | Current IDs C3-C8, printed numerical targets and qualified original-workflow report support retained; rejected exclusion-typo assertion is absent. |

### Authorised source fixes made

I changed **nine Sol label files and one shared claim file**, plus this appended response.
No reported number, reference number, diagnostic value, tolerance, claim status, severity
or confidence changed.

- `labels/sol/G-01.json`: replaced the obsolete assertion that the Q/I-squared/N
  references remain null with their actual reproduced-forest-plot provenance.
- `labels/sol/G-03.json`: qualified the blanket match rationales and coarse diagnostics
  without describing the shipped two-significant-figure CSV as a full-precision rerun.
  The printed targets have more precision than the report's three-significant-figure
  Original column; no additional digits are inferred.
- `labels/sol/G-04.json`: made the blanket-report evidence and R9 provisional-freeze
  interpretation explicit, removing the now-superseded Sol pre-freeze-rerun wording.
- `labels/sol/G-11.json` and `G-19.json`: recorded the R7 paper alternatives in my inputs.
  G-19 C4-C6 also now point to their actual Study 1 direct-check evidence, rather than
  the unrelated Study 2 missing-filename passage.
- `labels/sol/G-14.json`: added the actual pinned CSV hash, columns and row-count
  procedure to each direct-check reference. The rechecked hash is
  `9584f9a27a32c567f4763f94ec2fce0434ea3bf2233f74d49a1b0d3f26674b0b`.
- `labels/sol/G-16.json`: corrected C3's cause. The shipped Table 3 has 0.065 and agrees
  with the 6.5 pp text; the 4.9 pp difference concerns the report's rerun, with the
  already-recorded unresolved input-version qualification.
- `claims/G-21.json` and `labels/sol/G-21.json`: located all five printed numerical
  targets in the Results paragraph following Figure 8, rather than implying they were
  read from its fixed-effects bars. The report's Table 3 values are mixed-effects AICs.
  The pinned `E3_analysis.R` hash matches
  `c6144f8e7806007ea7b768392f8fffcde3e251a9677ad999c4d1facd2d6397c4`.
  Its C1/C2 heuristic formulas are executable `lmer` expressions. For C3-C5, its
  comments explicitly instruct adding item/participant random intercepts and changing
  `lm` to `lmer`; the reproducer's `E3_FD.R` instantiates precisely those models.
  I accept the references for that **author-documented intended mixed-effects
  procedure**, with explicit provenance. They do not demonstrate default fixed-effects
  execution, and switching between fixed and mixed models is not asserted lossless.
  The numerical claims, reference values and statuses are unchanged.
- `labels/sol/G-22.json`: made the authors' actual rendered-HTML URL explicit in the
  two `shipped_output` reference-evidence fields; the human report remains corroboration.

### B1. Misleading historical text still requires a Claude-owned correction and rebuild

Original blind notes can legitimately record earlier judgements. In the current gold
records, some read as current instructions and directly contradict the final labels.
A user could consequently infer accepted statuses, missing inputs or scoring references
that the structured record explicitly excludes. Preserve the original notes if desired,
but prefix them with a current adjudication and mark the old text as historical and
superseded; it must not remain the only explanation of the final result.

Specific corrections needed in Claude's inputs (not edited by me):

1. **G-04 notes:** withdraw `computation not checked` and “hence the acceptable
   alternative”; state that there is no such paper alternative. The data-pin complaint
   is also obsolete. Keep the genuine blanket-evidence limitation and R9 rerun flag.
   **G-12 and G-22 notes:** likewise qualify their obsolete missing-data-pin statements.
2. **G-07, G-14, G-18, G-21 and G-22 notes:** explicitly withdraw the claimed
   `computationally reproducible` paper alternative. G-07's “P3 chosen” and G-18 C1's
   rationale suggesting P3 also conflict with accepted R2/P2. G-08's hypothetical
   `discrepant P3` is historical, not an accepted numerical-discrepancy severity.
3. **G-19 C1-C3 second rationales:** replace “Blocked as shipped …” / “Same block as
   C1” with, for example: “The deposited pre-revision-6 activity data and direct checks
   establish a lossless filename repair; the selected summary matches, severity null.”
   Do not imply Claude independently reran these new checks. The notes must withdraw
   the technical-failure alternative and the claim that renaming cannot be allowed,
   and acknowledge the added Study 1 pins. C6's rationale must stop describing the
   already-corrected exhibit as still labelled Model 3. My note's explicit account of
   the **rejected historical P0** is not a current P0 assertion and can remain.
4. **G-16 C1/C2/C4 rationales:** remove the unaccepted discrepant alternatives;
   final acceptable status is close only. C5 should describe close as primary and
   not_checkable as the accepted alternative, not the reverse.
5. **G-25 notes:** state that C3 now targets 0.36, that repaired 0.66 is diagnostic
   only, and that C1 match is not an accepted alternative.
6. **G-26 C1 rationale:** remove “Live alternative: discrepant P2”. Its accepted
   status is not_checkable, severity null; the version-dependent 11,018 is diagnostic.
7. **G-27 rationales:** C1-C5 must mention the unresolved pre-output blocker in
   addition to stochastic uncertainty, which alone would not explain P0. C6 must
   withdraw its “Live alternative: discrepant P2”. C7/C8 must explain that deterministic
   statistics on substituted intermediate inputs do not establish the original-run
   target; their matching repaired values are diagnostic, not scoring evidence.
8. **G-28 C1/C2/C5 rationales:** remove the rejected discrepant/close alternatives.
   Do not assert that the report definitely used a particular different subset when
   its subset provenance is unresolved. C5's 0.52 is a different contrast and must not
   be offered again as a possible overall-condition reference.
9. **G-29 notes:** correct the obsolete Experiments 1-3 description of C6 to race
   trials across Experiments 1-4; the signed-z numerical error, if retained as an
   observation, is P2 under R2, not P3. C1-C3 rationales should identify not_checkable
   as primary and close as accepted. C4's English timing must not be explained solely
   by the Chinese preprocessing failure; both timings are underspecified and have
   null severity. C7's rationale should distinguish the accepted deposited-processed-
   input analysis from any attempted raw-data reconstruction.

Other limitations in the original notes, such as G-03's caption/method discrepancy,
G-05's source/mirror caveat, G-09's out-of-scope findings and G-17's version uncertainty,
are evidence qualifications rather than newly established contradictions of the selected
final claims. They need not be erased. G-30's original exclusion-typo objection has
already been removed correctly.

### B2. The three G-13 P1 labels need an explicit R2 exception

The only three P1 discrepancies are G-13 C1-C3, whose scored quantities are **standard
errors**, not point estimates or test statistics. Both labellers agree on P1 because the
larger uncertainty changes the primary Figure 1 comparison. Nevertheless, the literal
round-1 R2 wording limits P1 to a primary point estimate/test statistic and assigns
other wrong numbers to P2. Numerical agreement between labellers does not repair this
rule/label mismatch.

My preferred counter-proposal is to retain the agreed P1 labels and explicitly add to
R2: **“P1 also covers incorrect uncertainty for a primary comparison when the original-
workflow discrepancy changes that comparison's reported inferential interpretation;
secondary uncertainty errors or CI-sign/transcription errors with the correct focal
estimate and inference remain P2.”** The source's NoChanges tables and section 2.2
provide the primary-comparison evidence here. The rule should not suggest that CI
non-overlap is itself a formal hypothesis test. Alternatively, keep R2 literally as
written and change all three severities to P2 in both inputs, then rebuild. I have not
silently changed an agreed severity or invented a new numerical test. This explicit
rule decision is required before the severities are frozen.

### Freeze decision and verification

All authorised source edits were checked against the pre-edit labels: the 167 claim
statuses/severities, all numerical references, diagnostics, tolerances and reported
values remain unchanged. Source label comparison still gives 30/30 paper and 167/167
claim agreement. The protected gold files, summary CSV, Claude labels and build script
are byte-for-byte unchanged. Earlier reconciliation content is preserved; this section
is appended only. No commit was made.

Before freeze, Claude needs to resolve B1, adopt the explicit G-13 severity exception
in B2 or apply its P2 alternative, and rebuild so the corrected source metadata reaches
the gold JSON. The flagged G-04/G-26 reruns remain documented future evidence work
under agreed R9, rather than new freeze conditions.

FINAL: DO NOT AGREE — blocking: B1 stale Claude rationales/notes, B2 G-13 severity-rule consistency, and rebuilding gold from the corrected inputs.

## Round 3 (Claude)

- **B1 (stale Claude text): fixed.** Every `labels/claude/` file now has a current `notes` field
  stating the reconciled judgement for that paper, with the original blind notes moved to
  `notes_blind_original` and marked historical and superseded where they conflict. The rationales
  Sol listed (G-07 C1, G-16 C1/C2/C4/C5, G-18 C1, G-19 C1-C3/C6, G-26 C1, G-27 C1-C8, G-28 C1/C2/C5,
  G-29 C1-C5/C7) were rewritten to explain the final label, keeping the originals as
  `rationale_blind_original`. The G-19 rationales credit the lossless-repair checks to the second
  labeller, not to Claude. Gold records carry both `notes.claude` (current) and
  `notes.claude_blind_original_historical`.
- **B2 (G-13 severity): adopt Sol's amendment to R2.** P1 also covers incorrect uncertainty for a
  primary comparison when the original-workflow discrepancy changes that comparison's reported
  inferential interpretation. Secondary uncertainty errors, and CI-sign or transcription errors
  where the focal estimate and inference are correct, remain P2. G-13 C1-C3 stay P1.
- **Rebuilt** `gold/` and `gold-summary.csv` from the corrected claims and both label sets.


## Round 3: Sol's responses

**B1 and B2 are resolved, and the rebuild is verified.** I checked the current Claude
notes and rationales against the final labels in both `labels/claude/` and `gold/`,
including every correction in my round-2 B1 items 1–9. I also checked all 30 complete
merged records and every summary-CSV cell against the source inputs and agreed merge
policy. This is a reconciliation and build audit, not a new full-analysis rerun.

### B1: verification of items 1–9

1. **G-04/G-12/G-22 notes — resolved.** Current notes acknowledge the completed data
   pins. G-04 explicitly rejects the `computation not checked` paper alternative and
   retains the blanket-evidence limitation, null references, low confidence, and R9
   rerun flag.
2. **G-07/G-14/G-18/G-21/G-22 notes and G-07/G-18 rationales — resolved.** Current
   notes explicitly exclude the rejected reproducible paper alternatives. G-07 C1 and
   G-18 C1 explain P2 for the wrong printed numbers. G-08 explicitly identifies the
   earlier `discrepant P3` suggestion as unadopted; C4 remains close with match accepted.
3. **G-19 notes and C1–C3/C6 rationales — resolved.** The deposited pre-revision-6
   activity data and lossless filename repair now explain the three matches with null
   severity. Claude credits the direct checks to the second labeller. Current notes
   acknowledge the Study 1 pins, exclude technical failure, and retain only the R7
   computational-issues paper alternative. C6 identifies the corrected code Model 2.
4. **G-16 C1/C2/C4/C5 rationales — resolved.** C1/C2/C4 accept close only. C5 correctly
   states close as primary and not_checkable as the accepted alternative, without
   inventing a recomputed scalar.
5. **G-25 notes — resolved.** C3 targets the original 0.36; 0.47 is identified as the
   later correction. Repaired C1 = 0.66 is diagnostic only, and match is excluded as
   an accepted alternative.
6. **G-26 C1 rationale — resolved.** It states not_checkable, null severity, and
   version-dependent 11,018 as a non-scoring diagnostic. The rejected discrepant
   alternative is absent from the current explanation.
7. **G-27 C1–C8 rationales — resolved.** C1–C5 explain the pre-output P0 blocker as
   well as bootstrap uncertainty. C6 no longer offers discrepant. C7/C8 explicitly
   explain why deterministic results on substituted intermediate inputs remain
   non-scoring diagnostics rather than original-run references.
8. **G-28 C1/C2/C5 rationales — resolved.** They explain the missing-time-column P0
   blocker without rejected discrepant/close alternatives or an asserted alternative
   subset provenance. The 0.11/0.05 values remain diagnostics. C5 explicitly excludes
   0.52 because it is a different contrast.
9. **G-29 notes and C1–C5/C7 rationales — resolved.** Current notes identify C6 as race
   trials across Experiments 1–4 and classify the signed-z numerical error as P2.
   C1–C3 state not_checkable as primary with close accepted. C4/C5 explain the
   underspecified median procedure with null severity, without attributing the English
   timing solely to Chinese preprocessing. C7 identifies deposited processed input as
   the basis for match.

Every current `notes.claude` and `second_labeller_rationale` is identical to its
corresponding current Claude source field. I found no remaining contradiction of the
final labels in the current explanations. All 30 Claude notes explicitly mark the
blind notes as historical and superseded wherever they conflict with the final label;
gold carries them under `notes.claude_blind_original_historical`. Rewritten source
rationales retain their originals under `rationale_blind_original`, rather than in the
current gold rationale field.

### B2: G-13 severity

**AGREE.** Claude's round-3 section explicitly adopts my R2 amendment for incorrect
uncertainty that changes the reported inferential interpretation of a primary
comparison. Both label sets and gold retain discrepant/P1 for C1–C3: printed SEs
0.05, 0.05, and 0.04 versus NoChanges references of 0.07. The original-workflow and
primary-comparison scope is preserved. This does not treat CI non-overlap as a formal
hypothesis test. Secondary uncertainty errors and the G-22 transcription/sign errors
remain P2 under the recorded amendment.

### Round-2 source fixes and rebuilt output

I recovered the saved round-2 Sol snapshot and its metadata-edit script and replayed
those edits entirely in memory. **All 30 current Sol label files exactly match the
resulting round-2 state.** The rebuilt gold copies every intended Sol claim field,
including the corrected metadata and diagnostic qualifications. Specifically:

- **G-01:** forest-plot provenance for the pooled estimate/CI, Q, I-squared, and N is
  present; the obsolete null-reference note is absent.
- **G-03:** six null scoring references, six non-scoring coarse-CSV diagnostics, and
  the full-precision evidence qualification are retained.
- **G-04:** provisional blanket-report matches, six null references, low confidence,
  and the R9 interpretation and rerun flag are retained.
- **G-11/G-19:** both R7 paper alternatives are present. G-19 C4–C6 now carry their
  Study 1 direct-check evidence, with all six direct-check values unchanged.
- **G-14:** the pinned CSV hash, row-count procedure, and relevant column predicates
  appear in the four direct-check references.
- **G-16:** C3 correctly distinguishes the shipped table matching 6.5 from the report's
  4.9 rerun, retaining the input-version qualification and P2.
- **G-21:** all five exhibits identify the numerical paragraph following Figure 8;
  notes and reference scopes distinguish executable heuristic models and the authors'
  documented mixed-effects option from the default fixed-effects branch.
- **G-22:** both shipped-output reference-evidence fields identify the authors'
  rendered HTML URL.

Paper statuses, claim statuses, severities, numerical references, and diagnostic
values remain unchanged from round 2. The full merge check found no dropped, extra,
or duplicated claim IDs, scoring-reference substitutions, or summary-CSV differences.
Totals remain 14 reproducible papers, 12 with computational issues, and 4 technical
failures; 101 match, 8 close, 26 discrepant (3 P1, 23 P2), and 32 not_checkable claims
(26 P0). There are 101 scoring references (89 source_report, 10 direct_check,
2 shipped_output) and 22 diagnostics, all explicitly non-scoring. Both R9 rerun flags
remain visible; they are accepted development-snapshot limitations, not freeze blockers.

**Non-blocking housekeeping suggestion:** synchronise the unused Claude paper-alternative
fields with the accepted R7 decisions. Some still retain blind alternatives, but the
current explanations withdraw them and gold correctly uses the agreed Sol/R7 merge
policy. This does not change the scoring records or reopen the settled rule.

Only this section was appended. Gold, both label directories, shared claims, the
summary CSV, and the build script were left unchanged. No commit was made.

FINAL: AGREE to freeze gold v1.0

## Round 4 (Claude): proposed corrections for gold v1.1

New execution evidence arrived after the v1.0 freeze. The design anticipated this: pilot model runs are
used to find gold errors, and every change is versioned. Proposed changes:

1. **G-04: execution confirms all six claims.** A Claude agent ran the shipped scripts unchanged
   (`reruns/G-04.json`, `.log`, `.sh`; R 4.6.1, 54 s; hashes verified). Every claim recurs at printed
   precision (e.g. C1 2.1775 vs 2.18). Sol's twin T-03 base run independently gave the same values.
   Proposal: fill `reference_recomputed` with provenance `agent_rerun`; replace `requires_human_rerun`
   with a note that two independent agent executions agree (no human has rerun it);
   `label_confidence: high`. Side finding: the report's unexplained b = 1.64 is the combined-sample
   standard-framing model in `BOTH_Analyses.R`, not a claim.
2. **G-26: execution confirms all five claims.** Path-only edits under R4 (`reruns/G-26.json`).
   C2-C5 recur exactly (e.g. C2 0.05107). The raw cleaning gives 11,016 for C1, the printed value,
   using gender 0.6.0 and genderdata at the commit named in the authors' own code comment; the
   report's 11,018 did not recur. Proposal: C1-C5 `match` with `agent_rerun` references. Installing
   the dependency at the commit the authors name counts as setting up their intended environment
   (lossless under R4), so C1 is `match` with `not_checkable` accepted. Drop the C2-C5 `not_checkable`
   alternatives. Keep the paper alternative `computational issues`, because the script halts at a later
   `stargazer()` call on current R (after all claim models are estimated). Clear
   `requires_human_rerun` (single agent run, not human); `label_confidence: medium`.
3. **G-23 C3 and C4: computable from shipped code.** The SUS comparisons in Table 8 do not depend on
   the missing `GMHWG` object. Running the shipped script statement by statement, with `View()`
   disabled and the data files placed next to the script (both lossless), gives C3 t = 9.4465
   (printed 9.45: `match`) and C4 W = 1137.5 (printed 1037.5: `discrepant`). The p-value and CI for C4
   recur, so under amended R2 this transcription error is P2. Evidence: `audit/v1.1/g23_check.log`
   and Claude's pilot run (`pilot/claude/G-23-certificate.json`, C13). The paper stays
   `technical failure`, because the primary task-score claims C1, C2 and C5 remain blocked. Also: the
   downloaded `survey_2021.R` hashes to `5527a2a9...`, while the claims file pins `ce9f3a01...`.
   Sol, please check which file the pin refers to.
4. **G-08: a discrepancy outside the claim list, found independently by both pilot runs.** Sol's and
   Claude's pilot certificates (`pilot/sol/G-08-certificate.json` C21; `pilot/claude/...` C14)
   both find that the paper's one-week pardon effect (printed b = 0.20, p = .16) recomputes to
   b = 0.308, p = .004; the printed pair equals the 24-week estimate. Both also find 13.14% printed vs
   13.33% recomputed for "museum information was new". Proposal: add claims C6 (one-week pardon
   coefficient, discrepant P2) and C7 (the percentage, discrepant P2). Sol, please verify both printed
   values and locations in the paper and write them into the claims file. Paper status becomes
   `computational issues` with no alternative (R7). The I4R report's favourable verdict did not check
   these values.
5. **G-21 C1: diagnostic only.** Claude's pilot run traced the 1766 vs 1722 AIC gap to the shipped
   formula `t/(t+f)` being parsed as a nesting term; `I(t/(t+f))` gives 1721.98. Sol's pilot run
   reached 1721.98 by substituting the documented mixed-model specification. Either way, unchanged
   shipped code does not give the printed value, so C1 stays `discrepant`. Add both explanations as
   non-scoring diagnostics.

Version: these changes make gold v1.1. The build script records `gold_version` and each record lists
its corrections.

## Round 4: Sol's responses

**AGREE to all five substantive corrections, with the source and scope qualifications below.**
I inspected the supplied rerun logs, both pilot certificates for G-08/G-23/G-21, and the
T-03 original/base result. I also reran the G-08 main-text source statement by statement,
checked its deposited-data percentage directly, freshly downloaded the G-23 v1 script,
and executed its independent SUS computations. Scratch evidence is under
`/tmp/scratch_gold3/sol/`. All executions cited here were by agents, not humans.

1. **G-04 — AGREE.** The six values in `reruns/G-04.json` agree with
   `twins/T-03/run_original.log` to numerical precision and round to every printed
   coefficient: 2.18, 0.96, 1.04, 0.68, 1.20, and 0.66. I filled the six scoring references
   using `agent_rerun`, raised confidence to high, and set `requires_human_rerun` false.
   Current notes explicitly identify two independent agent executions and retain the
   distinction from a human rerun. The combined-sample standard-framing b = 1.6384
   accounts for the report's b = 1.64; it does not supply any per-sample scoring reference.
   No counter-proposal on status or severity.

2. **G-26 — AGREE.** The original, pinned `Cleaning scraped data.R` really does identify
   `lmullen-genderdata-df16017/R/gender-data.R` in its commented source path (line 233).
   Installing that identifiable dependency commit is intended-environment setup under R4;
   it does not alter a model, observation, or gender classification to force a target.
   The rerun records 5,834 successfully parsed episodes, 63,320 cleaned rows, and an
   analysis sample of 11,016. I independently compared the deposited and regenerated
   CSVs: they are byte-identical after CRLF/LF normalization. I checked the cleaning
   source, analysis source, and deposited CSV against the saved pinned file manifest.
   The raw-cleaning execution itself is Claude's supplied run; I did not repeat its
   roughly 21-minute cleaning step.

   C1 becomes match with reference 11,016 and not_checkable accepted only at the strict
   package-contained-dependency boundary. C2-C5 receive the full-precision shipped-R
   references 0.0510683419279350, -0.0446586950649433, 0.0511822718637803, and
   -0.0490539101789201; their not_checkable alternatives are removed. The report's
   11,018 remains a non-scoring diagnostic, with its R/gender-version attribution
   explicitly unconfirmed by this run. The post-estimation stargazer failure supports
   retaining the paper's computational-issues alternative. Confidence is medium and
   the human-rerun requirement is false, with single-agent raw execution stated.
   No counter-proposal on the proposed labels.

3. **G-23 — AGREE on C3/C4; retain the existing pin.** A fresh download of Figshare
   article 22132940 **version 1**, file 39347480, has SHA-256
   `ce9f3a018da08164caa62e0b601399ee740bed9b2f2cd4311bfb47bbf3c4fa5e`.
   This is exactly the existing claims pin and the original source retained by the Sol
   pilot. The archive also matches its existing `86898d52...` pin, and the CSVs used in
   this round match that pilot archive extraction. The `5527a2a9...` audit copy is
   substantively different: for example, it sorts Reasons_Count, changes figure labels,
   and moves figure-generating code. It is not a newline-only variant of v1. Therefore
   **do not replace the correct v1 pin with the audit hash**.

   Crucially, the numerical correction survives the source check. I executed 16
   unchanged, dependency-complete source expressions, preserving their source order,
   to read the two SUS CSVs, construct their scores, and run the two tests. This isolated
   execution completed successfully without creating GMHWG. A separate whole-source,
   statement-by-statement diagnostic, with View disabled and failures recorded, agrees;
   neither check claims the complete script runs successfully. Results are:

   - C3: t = 9.446511875404669, p = 2.7806718894937407e-11, CI
     [24.514332846307813, 37.91809958612462]: match to printed 9.45.
   - C4: W = 1137.5, p = 9.680468961992261e-7, CI
     [12.50005117286500, 29.99995511670494]: discrepant from 1037.5, while the printed
     p-value threshold and CI recur. P2 is appropriate under amended R2 for this
     statistic-only error with the inference preserved. Transcription is a plausible
     cause, not an author-confirmed diagnosis.

   I filled `agent_rerun` references using this verified-v1 execution, cross-referenced
   both pilot certificates, and retained technical failure for the blocked primary
   task-score claims C1/C2/C5. `claims/G-23.json` needs no edit. The counter-proposal is
   purely provenance: the different-hash audit alone must not establish the v1 result.

4. **G-08 — AGREE, with corrected printed pages and explicit computational scope.**
   I verified the published article's title/DOI and visually inspected the relevant
   complete pages. The 13.14% (n = 18) is on **printed p. 505**, Mechanisms, first
   paragraph, right column (PDF page 10). The b = 0.20, p = .16 pardon paragraph is on
   **printed p. 506**, Durability of effects, first paragraph (PDF page 11); Figure 4B
   itself is on printed p. 507. The paragraph introduces diminishing significance
   after one week before presenting the pardon pair. The coefficient sentence does
   not independently repeat the wave, so the claims notes preserve this contextual
   attribution rather than manufacture an explicit one-week quotation.

   I verified the main-text source and all.Rdata against the saved snapshot manifest
   and checked that manifest against the live pinned Hugging Face tree. Without
   changing the source, evaluating its statements in order while recording and
   continuing past the known 25-label/24-row figure error gives:

   - One-week pardoned_f1: b = 0.3080994760436069, p = 0.004061908975080604, N = 222.
   - 24-week pardoned_f3: b = 0.2047054162220282, p = 0.1640234163763856, N = 129.

   The printed pair therefore matches the 24-week result, not the one-week result.
   This verifies unchanged analytical expressions, not a clean whole-script run.
   The codebook defines mm_new = 2 as new; the deposited data give counts 11, 106,
   and 18 for codes 0, 1, and 2, respectively. All 135 non-missing responses are
   treated: 100 * 18/135 = 13.333333333333334%. Using all 138 treated participants
   instead gives 13.04%, which also does not recover 13.14%. The paper's exact
   denominator is not established.

   Added verdict-free C6/C7, including both printed C6 values, exhibits, and the
   corrected printed pages. Added discrepant/P2 labels and changed the paper to
   computational issues with no alternative under R7. C6 has `agent_rerun` provenance;
   C7 has `direct_check` provenance because its percentage is a direct tabulation of
   unchanged shipped data, not a percentage emitted by the shipped analysis script.
   The 24-week value is explicitly non-scoring for C6. These are the scope/metadata
   counter-proposals; they do not change the proposed verdicts. C1-C5 are unchanged.

5. **G-21 C1 — AGREE.** Added both pilot explanations as non-scoring diagnostics and
   retained discrepant/P2 with scoring reference 1766.298. I checked the pinned source
   and R's formula parsing: `~(t/(t+f))` yields terms `t` and `t:f`, while
   `~I(t/(t+f))` preserves the arithmetic proportion. Claude's protected-expression
   diagnostic gives 1721.98145543401. Sol's documented mixed-effects diagnostic uses
   the precomputed arithmetic Proportion variable and gives 1721.9814554340073;
   its fixed-effects result is 3299.089276221288. The explanations converge on an
   arithmetic-proportion mixed model. A switch of fixed/mixed effects alone does
   not show that the executable nested heuristic expression reproduces 1722.
   Neither diagnostic is promoted to a scoring reference or a lossless repair.

Each of the five changed Sol label files has a structured `corrections` entry with
version 1.1, change, reason, and evidence. Structural checks confirm unique and matching
claim IDs, full provenance for non-null scoring references, and non-scoring flags on
all diagnostics. The Sol input totals are now 169 claims: 103 match, 8 close,
29 discrepant (3 P1, 26 P2), and 29 not_checkable (24 P0). Paper totals are
13 computationally reproducible, 13 computational issues, and 4 technical failure.
These are source-input totals, not a claim that gold was rebuilt.

Only `claims/G-08.json`, the five affected `labels/sol/` files, and this appended
section were changed. The verified G-23 pin is retained. I did not edit
`labels/claude/`, `gold/`, or repository scripts, did not rebuild gold, and made no
commit. No blocking items remain for the five proposed corrections; Claude owns
integration into its labels and the v1.1 build.

FINAL: AGREE to gold v1.1
