# ReproCrowd benchmark: specification

Draft 0.4, 1 November 2026. Agreed by Claude, GPT-6.1 Sol (high effort) and Gemini 4 Argon (high)
after three review rounds (`review/`): both reviewers' final verdict is "AGREE as drafted".
Items marked **[settled]** are Lukas's decisions and
are not reopened in review. Items marked **[proposed]** are choices made in this draft that Lukas
has not yet seen.

## 1. What the benchmark measures

A ReproCrowd check asks a model to do three things for a published paper:

1. **Identify** the claims that need checking.
2. **Reproduce** each claim: obtain its value from the authors' materials.
3. **Judge** each claim (claim status) and the paper (paper outcome).

There are two tracks **[settled]**:

- **Track A, computational reproduction.** The model gets the article and the authors' code and
  data, and runs the shipped code with justified fixes only.
- **Track B, blinded recreation.** The model gets the article and the data, without the authors'
  code, logs or rendered outputs, and writes the analysis from the paper's description.

Each track has one headline score for the complete check **[settled]**. A must-check result earns
credit only when it is identified, its computation (or the reason it cannot be computed) is backed by
evidence, its basis and fixes are admissible, and its status is correct. The paper outcome is part of
the headline (section 6). Decomposed runs, which give the model the must-check list or a frozen
earlier stage, use the same criteria; they help develop pipelines and are not used for ranking.

The gold set is a public development set: its source reports are public, and models may have seen
them or the authors' code in training. Scores describe performance on this set. A ranking that needs
stronger blinding requires a separate held-out set.

## 2. Targets and packages

| Set | Track A | Track B | Purpose |
|---|---|---|---|
| Gold papers G-01 to G-30 (gold v1.4) | yes | eligible claims only (2.3) | Real packages with claim-level labels |
| Seeded twins T-01 to T-08 | yes | no | Planted discrepancies of known size and location |
| Stata papers (about 10, to be built) | yes | eligible claims only | Shipped Stata translated into R **[settled]** |

### 2.1 One packaging interface for every target

Every target, original or twin, reaches the model the same way: a local, pre-staged package under an
opaque name (for example `pkg-7f3a`), built by script from hash-pinned inputs, plus a pre-downloaded
article and supplement. No target receives a remote package URL, so the prompt and path never reveal
whether a target is a twin, and the run does not depend on downloading from OSF or GitHub. The
mapping from opaque name to target, the twin relation and the stripping record are evaluator-only
metadata. The model must not replace the supplied package with an upstream copy.

**Rendered outputs are stripped from every target [proposed; Sol and Argon agree].** The twin rule (2.2) applies to
originals too: knitted documents, figures, logs and saved result tables that the package's own code
produces are removed, and code that exists only inside a rendered document is extracted to a script.
Otherwise a package without outputs would itself mark a twin, and a model could copy values from
shipped outputs instead of computing them. Data the analysis reads stay. The authors' shipped outputs
remain available to the evaluator as references.

### 2.2 Twins

A twin is a gold package with one planted change to the analysis code (for example, standard errors
multiplied by 1.001). Rendered outputs that the package's own code produces are removed, because they
show the unpatched results **[settled]** (`../gold-set/twins/strip_outputs.json`). Retained files are
data that the analysis reads, documentation and task materials; the patched scripts were checked and
load no cached results downstream of the planted change. After stripping, each twin still produces
its recorded planted values (checked 1 November 2026 for T-02, T-03 and T-06, the three twins with
removed files).

Code-level twins test Track A only. A data-level twin (a planted change in the deposited data) would
test both tracks; this is an open extension.

### 2.3 Track B packages and eligibility

Eligibility is decided per claim, and the paper and claim counts are published before any run. A
claim is eligible when its inputs ship as data and the article states a starting point for the
analysis. Each Track B record states whether the starting data are raw observations or deposited
processed data (G-16 starts from supplied contextual probabilities and G-29 partly from processed
inputs), and which upstream steps are unavailable. A result from processed data is not described as a
recreation from raw data.

Every retained file is audited by content, not by extension: README text, codebooks, spreadsheets
(including formula cells), R and Python objects, notebook metadata, archives and hidden files.
Documentation needed to read the data stays. Author analysis code, recipes that amount to that code,
and stored analytical outputs are removed. Each removal, and any methodological information lost
with it, is recorded.

## 3. Claims and results

### 3.1 Must-check claims

The gold claim lists hold 5 to 8 claims per paper, chosen from results the human source assessed.
They are a **frozen must-check subset**, not every important claim in the paper. Claim identification
is scored as recall of this subset, and the benchmark makes no stronger claim about claim selection.
A broader claim-selection benchmark would need independent coverage annotations.

Each must-check claim records why it belongs in the subset and its scientific referent (study,
sample or group, outcome, predictor or contrast, model, wave, statistic), and whether it is
**primary** (a main-text focal hypothesis test or headline estimate; not sample descriptives,
manipulation checks or robustness tables). Extra claims a model adds are not counted as errors;
section 6.4 describes how they are audited.

**Submission cap [proposed; Sol and Argon agree].** An end-to-end certificate may hold at most 15 claims (the cap is in
`input-bundle.json`; gold has 5 to 8). Without a cap, a model could list every number in the paper
and reach full recall without selecting anything. A certificate over the cap is invalid.

### 3.2 Results and printed values

A claim has one or more **results**, one per printed number **[settled]**, each with a stable
`result_id` (for example `C6.b`, `C6.p`). An interval is one result with two ordered endpoints. Gold
v1.4 splits combined records into results (for example the coefficient and p value of G-08 C6, and
the six columns in each of G-27 C1 to C5) and fixes which results each claim requires.

Each printed value is stored as typed data:

```json
{"token": "−0.023", "kind": "scalar", "operator": "=", "value": "-0.023",
 "quantum": "0.001", "unit": "proportion", "scale": 1}
```

`kind` is `scalar`, `interval`, `count` or `bound`. `operator` is `=`, `<`, `<=`, `>` or `>=`.
`quantum` is the rounding step implied by the printed token, including trailing zeros and scientific
notation (`1.2e-05` has quantum `1e-06`). Counts written as words ("five") are stored as integers.
Percentages and proportions are related only by an explicit scale conversion; a percentage-point
effect and a relative change are different quantities.

### 3.3 Mapping model results to gold results

In end-to-end runs the model numbers its own claims. Mapping uses scientific identity and article
location first, and the printed value only as a consistency check. It is one-to-one, and it never
uses the model's status or recomputed value. Normalisation keeps signs, inequality operators,
endpoint order, units and printed precision; it standardises typography only (minus signs, dashes,
thousands separators, a leading zero). Unmatched gold results, near-misses and ambiguous identities
go to a mapping review file, which is adjudicated without seeing the model's status or value, and
the adjudication is stored with the run. The mapping code has tests for repeated values, intervals
written with dashes, values without a leading zero (`.17`), bounds versus equalities, and intervals
inside longer strings.

## 4. Claim status

| Status | Meaning |
|---|---|
| `match` | Deterministic analysis; the recomputed value equals the printed value under the rounding rule. |
| `close` | Deterministic analysis; the printed value differs because of a named reporting slip. |
| `within_variation` | The analysis is not exactly reproducible (4.3), and the printed value is compatible with its variation. |
| `discrepant` | Any other difference. |
| `not_checkable` | The value cannot be produced: a shipped-code blocker (Track A) or an unavailable or underspecified input or method (Track B). |

### 4.1 `match`: the rounding rule only **[settled]**

The only tolerance is the rounding convention. Let `q` be the printed quantum. A scalar matches when
rounding the unrounded recomputed value (first converted to the printed unit) to `q`, by round half
away from zero or by round half to even, gives the printed value. Only a recomputed value within
`1e-9 × q` of a half boundary counts as on the boundary: rounding to quantum 0.01, a computed
0.0449999999997 is treated as the boundary 0.045. The allowance is not scaled by the statistic, and it
does not apply to bounds or counts. Comparisons use decimal arithmetic.

- An interval matches when both endpoints match, each at its own printed quantum.
- A count matches only when the integers are equal.
- A bound (`p < .001`) matches when the unrounded recomputed value satisfies it.
- A printed p value of 0.000 is a rounded scalar, not a bound.

An inference the paper states in words (for example "significant at the 5% level") is a separate
result of kind `bound` when it is a must-check result. It is judged separately, so a rounded value
can match while the stated inequality is false.

### 4.2 `close`: a named reporting slip

`close` asserts a reporting error, so it needs evidence of a specific slip, and undoing it must
give a `match`:

- **truncation** instead of rounding (.07849 printed as .07);
- **transposed digits** (0.32 for 0.23);
- **transposed or copied cells or rows**, where the source of the copied value is identified (two
  effect sizes printed in each other's place; a coefficient and SE pair copied from the adjacent row);
- a **located typo**: an erratum, corrigendum or other author document in the input bundle
  identifies the entry and gives the corrected value; or the printed value differs from the
  recomputed value by a single-character substitution while the companion statistics of the same test,
  table row or in-text summary (for example the mean beside an SD) match.

**The evidence must be inside the bundle [proposed; Sol and Argon agree].** A model is not allowed to read reproduction
reports, so a slip that only a human report identifies cannot support `close`, either for the model
or in gold. A copied cell or row needs its donor value in the executed output. A general remark that
a paper contains typos does not cover any particular entry.

The vetoes apply to every affected result: a flipped sign, an interval that now includes or excludes
the null, a false printed bound, or a crossed threshold the paper relies on is `discrepant`. Counts
must be exact: a wrong count is `discrepant`. There is no numerical ceiling on `close`; the evidence
requirement does the work. Without a named slip, any gap in a deterministic analysis is `discrepant`.

### 4.3 `within_variation`: analyses that are not exactly reproducible **[settled in principle]**

The benchmark tests whether models notice analyses that do not give the same number on every run.
A result is nondeterministic when its value depends on something the package does not fix:

| Source | Example | Evidence required |
|---|---|---|
| `unseeded` | bootstrap, MCMC or Bayes-factor sampling without a seed | the unseeded call; at least five runs with independent seeds |
| `rng_version` | seed set, but the random stream changed between versions (R's `sample()` in 3.6.0) | the changed behaviour; an attempt to install the original version |
| `package_version` | deterministic algorithm whose output changed between versions | the changed behaviour; runs under two named versions |
| `parallel` | parallel or GPU computation in unfixed order | runs with different scheduling |
| `optimiser` | iterative fit sensitive to platform or start values | runs with the start values or platforms varied |

A possible source is not enough: the record must show that the target result actually varies.

**Acceptance protocol.** Before candidate runs, each nondeterministic gold result gets a frozen
variation protocol: the source varied, the run count, the seed or environment selection, and how the
acceptance region is built. Stochastic sources need at least five independent runs; version, platform
or scheduling effects need controlled comparisons. Each run keeps the same data, estimand and
analysis. Every attempt and setting is kept; runs are not selected, nor the region widened, after
seeing candidate results. The region is an operational rule, not a calibrated coverage guarantee. A
published Monte Carlo error can be used only if it applies to the same quantity and comparison; a
confidence interval for the estimate is not a Monte Carlo error.

The printed value is compatible when its rounding region intersects the frozen acceptance region.
For an interval, the region is joint for the endpoint pair; endpoints that are compatible only in
different runs are not enough. The vetoes in 4.2 apply.

**Precedence [proposed; Sol and Argon agree].** A compatible result with established variation is
`within_variation`, even when a run prints the reported value; the record notes
`printed_match: true`. When all relevant sources are fixed (original seed and package or RNG versions
recovered and verified in the bundle), the deterministic rules apply and may give `match`, `close` or
`discrepant`. For `rng_version` and `package_version` gold results, both `within_variation` (from
multi-version runs) and the deterministic status from a verified original-version recovery earn
credit. A demonstrated structural
blocker takes precedence over variation. A result outside the region is `discrepant`. Insufficient
gold evidence means the gold result is held (5.1). A model that asserts variation without the
evidence gets no credit for `within_variation`.

### 4.4 Basis and fixes

`basis` is `shipped_code`, `justified_fix`, `translated` (Track A), `recreated` (Track B) or
`not_computed`. A result can carry several fixes, in order. Each fix states **what changed and why it
leaves the analysis unchanged** **[settled]**:

```json
"fixes": [{"category": "path", "file": "code/main.R", "sha256": "…", "lines": "3",
           "change": "commented out setwd('C:/Users/…')",
           "reason": "sets the working directory only; no input or statistic depends on it"}]
```

**Track A** allows these categories only:

- `path`;
- `package`: install or pin a version;
- `equivalent_call`: a deprecated function replaced by an exact equivalent;
- `order`: run scripts in the documented order;
- `inspect`: add statements that only print or save values (for example the unrounded estimate behind
  a rounded table), without changing any object the analysis uses;
- `skip_failing_statement` **[settled]**: names the statement by file hash and line, gives its error,
  and shows that the claim does not use its output;
- `translation` **[settled]**: shipped Stata translated command by command into R, kept in the bundle,
  with dependent claims `not_checkable` where a command has no exact equivalent.

Not allowed, whatever the outcome:

- writing missing analysis code;
- changing the model, sample, exclusions or data;
- switching on an option the authors describe but do not run **[settled]**. In G-21, the script
  comments describe a mixed-effects variant and the printed AICs come from it; running that variant
  does not reproduce the shipped code.

**Track B** permits new analysis code that implements the method as the documentary corpus describes
it (`basis: recreated`), with every analytical choice linked to the article text that determines it.
It does not permit changing the method to make the printed value recur.

The scorer checks that each fix has the required fields and an allowed category. Whether a fix really
leaves the analysis unchanged is checked by the evaluator from the diff (section 6.3).

### 4.5 Claim outcome

| Status | `shipped_code` | `justified_fix` or `translated` | `recreated` |
|---|---|---|---|
| `match`, `close`, `within_variation` | reproduces | reproduces with justified fixes | reproduces |
| `discrepant`, `not_checkable` | does not reproduce | does not reproduce | does not reproduce |

`not_checkable` with `basis: not_computed` maps to "does not reproduce" and needs the blocker
evidence in 6.3; no other status can use `not_computed`. A failed or timed-out attempt is an execution
state, not evidence of a study blocker.

These are the three settled outcomes **[settled]**. A claim with several results takes the worst
outcome among its required results: "does not reproduce" beats "reproduces with justified fixes",
which beats "reproduces".

### 4.6 Paper outcome **[proposed; Sol and Argon agree]**

Before targets are scheduled, each paper's scored assessment scope is frozen, after removing held and
(Track B) ineligible results, together with a non-empty primary subset. A target with no scored
claims or no assessable primary result is not scheduled. Outcomes describe only this scope.

- **Computationally reproducible:** every assessed result is `match`, `close` or `within_variation`.
  Reporting slips are listed separately in the certificate; they do not make the computation fail.
- **Technical failure:** demonstrated study blockers prevent every primary computation.
- **Computational issues:** at least one primary computation completes, and an assessed result is
  `discrepant` or `not_checkable`.

In end-to-end runs, if a model's paper outcome differs from gold only because of an extra claim
outside the must-check subset, the outcome counts as correct when that extra claim passes the
evidence checks in 6.3.

Track B uses the same three terms for the recreation. Its `not_checkable` results carry a structured
reason: `underspecified`, `contradictory_specification`, `data_unavailable` or `numerical_failure`.
An executor timeout is not a paper outcome; it is a failed run (6.1).

## 5. Gold

### 5.1 Track A: gold v1.4

Gold v1.4 applies section 4 to every record. A label is frozen only when the evidence meets section 4.
A result whose evidence is not yet sufficient is **held**: it is excluded from scoring until
adjudicated, which is different from `not_checkable` (a property of the study, not of the evidence).
The changes agreed or still open after round 1:

| Claim | v1.3 | v1.4 | Basis |
|---|---|---|---|
| G-21 C3, C4, C5 | match | discrepant, P2; scoring reference replaced by the executable fixed-effects output, mixed-effects values kept as diagnostics | Documented-but-unrun option (4.4); Sol r1 checked the pinned script |
| G-08 C4 | close | close | Truncation; independent rerun 0.1980 |
| G-08 C6 | match | match, expected basis `justified_fix` (`skip_failing_statement`) | An earlier statement errors before the follow-up models |
| G-18 C1 | close | close (C2 stays discrepant, P2) | Paired transposition; .012 violates C2's printed bound |
| G-22 C1 | close | close | Truncation (.07849 printed as .07), demonstrable from the recomputed value |
| G-22 C2, C3 | close | discrepant, P2 **[proposed; Sol and Argon agree]** | The intercept (5.28 printed as 5.25) and its interval ([5.11, 5.44] printed as [5.08, 5.43]) differ together, so no single-character substitution with matching companion statistics explains either; only the human report calls this a typo, and that report is outside the bundle |
| G-07 C1 | discrepant, P2 | held until the companion statistics (the accompanying descriptives) are checked; then close, severity null, otherwise discrepant, P2 | Single-character substitution (0.14 for 1.14) in an in-text SD |
| G-15 C1, C2 | discrepant, P2 | held until the donor row (-0.05, 0.06) is found in the package's output; then close, otherwise discrepant, P2 | Coefficient and SE pair apparently copied from the adjacent row |
| G-16 C1, C2, C4 | close | held pending same-input provenance; if confirmed, discrepant, P2, unless claim-specific evidence establishes within_variation | Seed set; no claim-specific evidence that versions explain the gaps; input chosen by file time |
| G-16 C5 | close or not_checkable | held pending a scalar recomputation and variation adjudication | No scalar reference in the source |
| G-28 C3, C4, C6 | match, match, close | held; `unseeded` recorded | Bayes factors computed without a seed; needs the repeated-run range |
| G-29 C1 to C3 | not_checkable | held | Seed set; computable; needs a complete same-environment run |
| G-24 | as v1.3 | to audit | Table 1 code precedes the parse fault, so `skip_failing_statement` may now reach it |

Held results are resolved by evaluator reruns (five or more runs for each stochastic source, or the
original package versions). A target with no assessable primary result is not scheduled (G-28's
only primary claim, C3, is held). Other held results stay excluded and are reported as such.

Gold v1.4 has one label per result and one outcome per paper; the earlier `acceptable_statuses` and
`acceptable_alternatives` lists are removed, and a case the labellers cannot settle is held. The only
exception is the version-recovery rule in 4.3. Every gold result gets a `primary` flag and a
`nondeterminism` record (null when deterministic). Paper outcomes are recomputed under 4.6 after the
claim labels settle; G-07 and G-15 are the likely changes. Stale explanatory text is repaired (G-08 C4
and C6, G-11 C2 and C5, and the copied evidence strings in G-29 C4 to C6).

**Reference values.** Gold distinguishes the label's evidence from the numerical reference used to
check a model's recomputed value. Where an earlier reference was coarse (G-03 has no reference at the
printed scientific-notation precision) or conflicts with another run (G-11 C2, C5), a well-documented
new run that disagrees with it goes to adjudication; it is not marked wrong automatically.

### 5.2 Track B gold

Track B gold is built from independent recreations, not from Track A answers, because the published
method and the executable code can differ (G-21) and a recreation should recover the analysis, not a
misprinted number (G-22). Two labellers (Claude and Sol, in fresh contexts restricted to the frozen corpus) work from the
same documentary corpus and sanitised data the models receive, before seeing Track A code, outputs or reports. For each claim they
record the estimand, sample, exclusions, transformations, missing-data handling, model, inference and
numerical conventions the corpus determines, run their implementations, and reconcile. Track A results
can corroborate a later adjudication.

When the description leaves open a choice that changes the printed value, the gold records the missing
choice, its location and at least two admissible implementations that give different values, and labels
the claim `not_checkable` (`underspecified`). A model gets credit only when it identifies the same
missing choice. When the admissible implementations give the same printed value, the claim stays
checkable. Unresolved labeller disputes are held.

## 6. Scores

### 6.1 Headline score (one per track)

Before runs, the target list, scored results, evidence rules and weights are frozen.

1. **Result credit.** A must-check result earns 1 when all of these hold:
   - it is identified and mapped (3.3);
   - its evidence passes (6.3);
   - its basis and fixes are admissible (4.4);
   - its status is correct.

   Otherwise it earns 0. Credit is averaged over the frozen gold results of each must-check claim
   (an unmapped gold result scores 0), so splitting a claim into more rows does not change its weight.
   Claims are averaged within a paper.
2. **Paper score [proposed; Sol and Argon agree].** Weighted partial credit for the complete check: the claim
   average, multiplied by 1 if the paper outcome is correct and by 0.5 if not. A paper with a verified hard-gate violation scores 0. A timeout, a crash or a missing
   or invalid certificate scores 0 and stays in the denominator; an infrastructure failure outside the
   pipeline is rerun under a predeclared rule.
3. **Headline.** The unweighted mean of paper scores over all scheduled targets. Each twin counts as a
   target with the same weight as a paper **[settled in principle]**.

### 6.2 Diagnostics (reported beside the headline, never folded in)

- claim recall;
- three-way claim outcome accuracy (4.5) and the binary version (reproduces vs does not);
- status confusion matrix with all denominators;
- sensitivity to discrepancies (P1, P1+P2) and specificity, counting only identified, evidenced
  reproducing results (a missed or `not_checkable` result on reproducible gold is a failure, not a
  true negative);
- paper outcome accuracy;
- nondeterminism recognition: gold nondeterministic results the model flagged, and false flags;
- fixes: count, inadmissible fixes, fixes without reasons;
- gold papers and twins separately, with planted twin results as their own sensitivity measure;
- baselines under the same rules: all `match`, all `not_checkable`, all `discrepant`;
- cost: wall-clock minutes, tokens and US$ per target, including failed attempts.

### 6.3 Evidence checks

The checks depend on the status:

- **`match`, `close`, `discrepant`.** The evaluator inspects the executed source and its diff against
  the package (hash-checked against `input-bundle.json` and `run.json`) to confirm that the result was
  computed from the permitted inputs by the admissible analysis, not printed as a constant or read from
  a shipped output. It then takes the recomputed value from the execution output: unrounded where the
  code prints it (an `inspect` fix may be used), otherwise at the precision the unmodified code
  emits. Agreement with the printed value or a log entry alone is never enough. Where gold has a
  deterministic reference value, the model's value and the reference must round to the same value at
  the printed quantum, under the same rounding mode (subject to the reference policy in 5.1). Twins
  have exact planted references.
- **`close`.** The named slip must be demonstrated from the bundle and the execution output (4.2):
  truncation or digit transposition applied to the recomputed value, the donor value in the executed
  output, an erratum in the bundle, or a single-character substitution with matching companion
  statistics.
- **`within_variation`.** The repeated runs and their settings must be in the bundle, pass the same
  analysis and provenance check, show actual variation, and meet 4.3.
- **`not_checkable`.** A specific study blocker must be named (the missing file, the failing statement
  and its error, or the Track B ambiguity) and match the gold blocker. An error that an allowed fix
  (4.4) would remove is not a study blocker. An unsupported abstention earns nothing.

Mechanical checks cover structure, hashes, numerical predicates and the presence of values in logs. A
fix's admissibility and a Track B ambiguity need evaluator adjudication, which is recorded.

### 6.4 Extra claims and hard gates

Extra claims are counted and audited. For each target, a uniform sample without replacement of five
distinct extra result identities (or all, if fewer) is drawn with a recorded seed from a canonical
ordering. The audit counts invented or materially misattributed **reported targets** (values the
model says the article prints), after permitted normalisation; recomputed values, diagnostics and
intermediates are not reported targets. Two distinct verified fabrications anywhere in a certificate
trigger the fabrication gate **[proposed; Sol and Argon agree]**; a single instance is recorded without the
gate. Every result used for score credit is audited in full. The certificate has one final result per
scientific identity; any duplicate result (same result id or same scientific identity) makes it
invalid, as does exceeding the claim cap (3.1).

Hard gates (verified by the evaluator, with evidence recorded):

- the certificate is invalid;
- two or more verified fabricated reported targets, as defined above;
- a recomputed value with no code and log behind it;
- `match` or `close` on a gold P0 blocked result;
- access to the authors' code in Track B;
- access to gold, earlier reproduction reports or previous runs;
- editing files outside the run directory.

A numerical mismatch alone is never treated as fabrication.

### 6.5 Uncertainty

Intervals come from a bootstrap over paper families (an original and its twin resampled together).
Pipelines run on the same targets are compared with a paired family bootstrap. The intervals describe
this development set, not published research in general.

## 7. Modular pipeline

### 7.1 Principle

The benchmark separates **inputs**, **stages** and **evaluation**. Any model, prompt or executor can
implement one stage, several stages, or the whole check, provided the files at each stage boundary
validate against the same schemas and carry enough evidence for another pipeline to continue. Model
stages never see gold, twin metadata or the mapping.

### 7.2 Stage contracts

Every stage runs in a fresh working directory. Artefacts from earlier stages are mounted read-only at
fixed relative paths, so a later stage cannot change an earlier one:

```
./input-bundle.json   ./article/   ./package/          (from S0)
./claims.json                                          (from S1)
./results.json        ./s2-workspace/                  (from S2: edited copies, logs, lockfile)
```

Each stage writes its outputs to `./`. Every artefact is JSON with `"schema_version": "1.2"`. Results
are keyed by `claim_id` (`C1`, `C2`, …) and `result_id` (`C1.b`, `C1.p`, …). For an interval, the
typed `value` and `quantum` (3.2) are two-element arrays `[low, high]`. A validator checks schemas, ID
uniqueness, references between files, allowed track and basis combinations, required evidence and
file hashes.

| Stage | Reads | Writes |
|---|---|---|
| S0 package (evaluator) | pinned sources | `input-bundle.json` (target id, track, mode, data scope raw or processed, file list with hashes, claim cap), `article/`, `package/` |
| S1 identify | input bundle, article, package | `claims.json`: per claim `claim_id`, wording, `primary`, exhibit, printed and PDF page, quote or table cell, referent (study, sample, outcome, predictor, model, wave, statistic), selection reason, and its results (`result_id`, quantity, typed printed value) |
| S2 reproduce | input bundle, article, package, `claims.json` | `results.json` and `s2-workspace/`: per result, state (completed, blocked, ambiguous, failed, timed out), recomputed value (unrounded and as emitted), execution (script path and hash, lines, command, exit status, log paths, lockfile), ordered fixes with diff paths, method choices with article quotes (Track B), variation runs (setting, value, log path) |
| S3 judge | everything above | `certificate.json` (schema 1.2): per result `status`, `basis`, claim outcome, comparison, slip or blocker evidence, severity, `printed_match`; paper outcome and findings |
| run record (runner) | all stage directories, proxy and process logs | `run.json`: manifest and input-bundle hashes, and per stage attempt: start and end, exit status, executor and version, provider, requested and resolved model, options, prompt path and hash, tokens, cost, event log, artefact hashes, network log |

In decomposed mode the runner mounts the gold `claims.json` (same schema, no labels) in place of S1's
output, or a frozen S1 and S2 bundle in place of both. A judgement-only run is a diagnostic. The
end-to-end input bundle never contains the gold claim list.

### 7.3 Pipeline manifest and executors

```json
{"name": "split-luna-s1-claude-s2s3", "track": "A", "mode": "end_to_end",
 "defaults": {"executor": "claude_code", "model": "claude-opus-5-5",
              "options": {"effort": "high", "web_search": false},
              "timeout_minutes": 75, "max_cost_usd": 25, "retries_on_infra_error": 1},
 "stages": [
   {"id": "S1", "executor": "codex_cli", "model": "gpt-6-luna",
    "options": {"reasoning_effort": "medium", "web_search": false},
    "prompt": "prompts/s1-identify-v1.txt"},
   {"id": "S2-S3", "prompt": "prompts/s2s3-reproduce-judge-A-v1.txt"}]}
```

Valid stage ids are `S1`, `S2`, `S3`, `S1-S2`, `S2-S3` and `S1-S3`; what each stage reads and writes
follows from 7.2. Stage fields override `defaults`. Prompts need no filling in: they tell the agent to
read the mounted paths in `./` and write the stage outputs there. A combined stage still writes every
intermediate artefact.

An executor adapter is a function `run_stage(stage, work_dir, env) -> attempt_record`. It runs the
model on the prompt in `work_dir` and returns its part of the run record (7.2), with the raw provider
event stream saved as `events.jsonl`. From that stream the runner checks the resolved model, the
options (including that provider-side web search and URL fetching are off) and token counts against
the manifest. Adapters exist or are planned for the Codex CLI, Claude Code, OpenCode, an API loop and
a human. The runner keys reuse on input and manifest hashes (not on the presence of a certificate)
and keeps every attempt.

### 7.4 Isolation

A separate working directory is not an access boundary: the current Codex sandbox restricts writes,
not reads, and the gold set is in a public repository. Each stage attempt therefore gets:

- an isolated environment (a container, or an equivalent sandbox), with only the artefacts it reads
  mounted read-only and a fresh writable `./`;
- no access to the host repository, home directory, raw credentials, previous runs or other targets;
- network access only through an evaluator-controlled proxy that allows package repositories (CRAN,
  Posit Package Manager, Bioconductor, PyPI, conda, and evaluator mirrors of GitHub-only
  dependencies) and, when the agent runs inside the container, the model provider's inference
  endpoint. The proxy adds the API credentials, so the container never holds them. Provider-side web
  search and URL fetching are disabled, because the proxy cannot see what the provider fetches on the
  model's behalf. Every request is logged outside the model's control;
- a read-only shared base library of R and Python packages plus a per-stage writable library.

An executor that cannot enforce this policy produces diagnostic results only, not ranking results.

## 8. What exists and what is left

Exists:

- gold v1.3 (30 papers);
- eight verified twins with rendered outputs stripped;
- certificate schema 1.1;
- the pilot scorer (status only);
- the pilot Codex runner (shared R library, remote packages for gold papers, certificate-only copy);
- two diagnostic Luna batches on five targets each, tied to their prompt, gold and package versions.

Left, in order:

1. Freeze this specification.
2. Gold v1.4: atomic results, typed printed values, nondeterminism records, the section 5.1 changes,
   evaluator reruns for held results, paper outcomes recomputed.
3. Rule pack 1.2, public prompt and certificate schema 1.2, aligned with section 4.
4. Stage schemas and validator; packaging for all targets with opaque names, checked so that
   every frozen checkable result is still reachable after stripping; isolated runner with
   proxy and run records; executor adapters; scorer with evidence checks, mapping review and
   baselines.
5. Adversarial tests of the scorer: copied printed values, all-`not_checkable`, duplicate rows,
   flooding with extra claims.
6. Stata papers.
7. Track B eligibility, packages, content audits and gold.
