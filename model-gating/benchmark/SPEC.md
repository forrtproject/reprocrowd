# ReproCrowd benchmark: specification

Draft 0.1, 1 November 2026. Status: under review by GPT-6.1 Sol and Gemini 4 Argon. Items marked
**[settled]** are Lukas's decisions and are not reopened in review.

## 1. What the benchmark measures

A ReproCrowd check asks a model to do three things for a published paper:

1. **Identify** the claims that need checking (the numeric results the paper's findings rest on).
2. **Reproduce** each claim: obtain the value from the authors' materials.
3. **Judge** each claim (claim status) and the paper (paper outcome).

The benchmark measures this in two tracks **[settled]**:

- **Track A, computational reproduction.** The model gets the article and the authors' code and
  data. It runs the shipped code, with justified fixes only.
- **Track B, blinded recreation.** The model gets the article and the data, without the authors'
  code, logs or rendered outputs. It writes the analysis from the paper's description.

Each track yields one **end-to-end score** (section 6), because what matters in use is the whole
check **[settled]**. Each track can also be run in a decomposed mode, which gives the gold claim
list to the model, so that reproduction and judgement can be scored without claim selection. The
decomposed scores serve pipeline development, not ranking.

## 2. Targets

| Set | Track A | Track B | Purpose |
|---|---|---|---|
| Gold papers G-01 to G-30 (gold v1.4) | yes | eligible subset (section 2.2) | Real packages with claim-level labels |
| Seeded twins T-01 to T-08 | yes | no | Planted discrepancies of known size and location |
| Stata papers S-01 to S-10 (to be built) | yes | eligible subset | Translation of shipped Stata into R **[settled]** |

### 2.1 Twins

A twin is a gold package with one planted change to the analysis code (for example, standard errors
multiplied by 1.001). The package is rebuilt from hash-pinned inputs and patched
(`build_twin_package.py`). Rendered outputs that the package's own code produces (knitted HTML,
figures, logs) are removed, because they show the unpatched results **[settled]**; the list and rule
are in `../gold-set/twins/strip_outputs.json`. Nothing in the package or prompt names it a twin.

Code-level twins only test Track A: removing the code removes the planted change. A data-level twin
(a planted change in the deposited data) would test both tracks; this is an open extension.

### 2.2 Track B packages

Track B needs a local package per paper with the authors' code, logs, rendered outputs and cached
results removed, keeping the data, codebook and README. A paper is eligible when (a) its data ship
as files separate from the code, (b) the claims rest on that data rather than on code-generated
intermediates that cannot be rebuilt without the code, and (c) the article describes the analysis.
Each Track B package is built by a script from hash-pinned inputs, like the twins.

The model must not fetch the authors' code. The prompt says so, the package link points at the
local copy, and the run log is checked afterwards for requests to the package's repository or DOI.
A fetch is a hard-gate violation.

## 3. Claims

### 3.1 Which claims count

The gold claim lists (`../gold-set/claims/`) hold 5 to 8 claims per paper, chosen from the results
the human source assessed. They are a **must-check set**, not an exhaustive list of every number in
the paper. A complete check must cover them; it may cover more.

Claim identification is therefore scored as **recall of the must-check set**. Extra claims a model
adds are not scored for correctness (there is no gold for them). They are reported as a count, and a
random sample is audited for fabrication (a claim the paper does not print is a hard gate).

### 3.2 One result per printed number

Each printed number gets its own result: a coefficient and its p value are two results under the
same claim id. Intervals are one result with both endpoints.

### 3.3 Mapping model claims to gold claims

In end-to-end mode the model numbers its own claims. A gold claim is matched to a model result when
(1) the result's printed value equals the gold printed value after normalisation (minus signs,
percent, brackets, thousands separators), and (2) the exhibit (table, figure, page or paragraph)
agrees. Ties go to the closest exhibit match. Unresolved ties and near-misses are written to a
mapping review file and resolved by hand before scores are published; the resolved mapping is stored
with the run. The mapping code has unit tests for repeated values and formatting variants.

## 4. Claim status

Each result has a status, a basis and, where relevant, a fix and a nondeterminism record.

| Status | Meaning |
|---|---|
| `match` | The recomputed value equals the printed value at the printed precision. |
| `close` | Deterministic analysis; the printed value differs because of one named reporting slip. |
| `within_variation` | The analysis is not exactly reproducible (section 4.3), and the value lies within its variation. |
| `discrepant` | Any other difference. |
| `not_checkable` | The shipped code (Track A) or the described method (Track B) cannot produce the value. |

### 4.1 `match` **[settled in principle]**

The only tolerance is the rounding convention. A value matches when rounding the unrounded
recomputed value to the printed number of decimals, by round-half-up or by round-half-even, gives the
printed value. Values within 1e-9 (relative) of a half boundary count as on the boundary, so that
binary floating-point storage (0.125 stored as 0.12499999…) does not decide the outcome. A printed
inequality (`p < .001`) matches when the recomputed value satisfies it. Nothing else is a match: a
gap of one unit in the last digit that rounding does not explain is not a match.

### 4.2 `close`

`close` asserts a reporting error, so it needs evidence. The printed value must be obtained from the
recomputed value by **one named slip**, and undoing that slip must give an exact `match`:

- truncation instead of rounding (.07849 printed as .07);
- transposed digits (0.32 for 0.23);
- transposed cells or rows (two values printed in each other's place);
- a typo identified by the authors (erratum, corrigendum) or by a documented source.

The vetoes apply before `close`: a flipped sign, an interval that now includes or excludes the null,
a false printed inequality, or a crossed threshold the paper relies on is `discrepant`. Counts
(sample sizes, numbers of studies) must match exactly; a wrong count is `discrepant`. Without a
named slip, any gap is `discrepant`.

### 4.3 `within_variation` and the nondeterminism record

Some analyses do not give the same number on every run. The benchmark tests whether models notice
this, so these results get their own status instead of being folded into `close` **[settled]**.

A result is nondeterministic when its value depends on something the package does not fix:

- `unseeded`: random draws without a seed (bootstrap, MCMC, simulation, random splits);
- `rng_version`: a seed is set, but the random-number stream changed between software versions
  (for example R's `sample()` in 3.6.0) and the original version cannot be installed;
- `package_version`: a deterministic algorithm whose output changed between package versions, when
  the version used cannot be installed;
- `parallel`: parallel or GPU computation whose order is not fixed;
- `optimiser`: an iterative fit whose result depends on platform or starting values.

The model records the source and its evidence (the line without a seed, the changed function, the
version it could not install). When the original seed and versions can be matched, the analysis is
deterministic and must `match`. A nondeterministic result is `within_variation` when the gap lies
within the variation shown by repeated runs (at least five, different seeds) or by a published
Monte Carlo error; a gap outside that range is `discrepant`. The vetoes in 4.2 still apply.

### 4.4 Basis and fixes

`basis` is `shipped_code`, `justified_fix`, `translated` (Track A) or `recreated` (Track B), or
`not_computed`. Each fix states **what changed and why it leaves the analysis unchanged**
**[settled]**, as a structured record:

```json
"fix": {"category": "path", "change": "commented out setwd('C:/Users/…')",
        "reason": "working directory only; no input or statistic depends on it"}
```

Allowed categories: `path`, `package` (install or pin a version), `equivalent_call` (a deprecated
function replaced by an exact equivalent), `order` (run scripts in the documented order),
`skip_failing_statement` (a statement that fails is skipped, and the claim does not depend on its
output **[settled]**), `translation` (Stata or another language translated command by command into R
or Python **[settled]**).

Not allowed, whatever the outcome: writing missing analysis code; changing the model, sample,
exclusions or data; switching on an option the authors describe but do not run **[settled]** (G-21:
the script comments describe a mixed-effects variant; the printed AICs come from it; running it is
not a reproduction of the shipped code). A value obtained that way does not reproduce the claim.

A fix without a reason, or with a reason that does not match the change, is flagged by the scorer
and counted as an unsupported fix.

### 4.5 Claim outcome

Each claim has one of three outcomes **[settled]**: it **reproduces** (`match` on `shipped_code`),
**reproduces with justified fixes** (`match`, `close` or `within_variation` on `justified_fix` or
`translated`), or **does not reproduce** (`discrepant` or `not_checkable`). `close` and
`within_variation` on `shipped_code` count as reproducing for the outcome, but the status is scored
separately.

### 4.6 Paper outcome

Track A uses the FLoRA vocabulary: `computationally reproducible`, `computational issues`,
`technical failure` (rule pack section 11). Track B uses the same three terms for the recreation
(the paper's description reproduces its results, partly, or the data cannot support it).

## 5. Gold labels

Track A gold is the existing gold set, moved to v1.4 under section 4. Projected changes from v1.3:

| Claim | v1.3 | v1.4 | Reason |
|---|---|---|---|
| G-21 C3, C4, C5 | match | discrepant (severity to agree) | Documented-but-unrun option is not a fix (4.4) |
| G-16 C1, C2, C4 | close | within_variation (`package_version`) | Seed set; grf output differs across versions |
| G-16 C5 | close or not_checkable | within_variation or not_checkable | As above; no exact scalar in the source |
| G-28 C6 | close | within_variation (`unseeded`) | Report: no `set.seed()` |
| G-29 C1 to C3 | not_checkable (close accepted) | not_checkable (within_variation accepted) | `set.seed(999)` but state-dependent bootstrap intervals |
| G-08 C4 | close | close | Truncation (0.198 printed as 0.19) |
| G-18 C1 | close | close | Transposed effect sizes (.012 and .004) |
| G-22 C1 | close | close | Truncation (.07849 printed as .07) |
| G-22 C2 | close | close | Source-identified typo (5.28 printed as 5.25) |
| G-22 C3 | close | discrepant | Both endpoints differ ([5.11, 5.44] vs [5.08, 5.43]); no single slip |

Every gold claim also gets a `nondeterminism` field (null for deterministic analyses), so that
recognition of nondeterminism can be scored. Paper outcomes are unchanged by these edits (G-16, G-21,
G-22 and G-28 are already `computational issues`).

Track B gold is new. For each eligible claim it records whether the article's description determines
the analysis. Claims whose description leaves a choice open that changes the value are labelled
`underspecified` and score as correct when the model reports `not_checkable` with that reason. The
reference value is the Track A value. Two labellers (Claude and Sol, as for Track A) label
independently and reconcile.

## 6. Scores

All scores are per track and are computed over gold claims, so a missed claim counts against the
model.

**End-to-end score (headline, one per track).** The mean over papers of the paper score. The paper
score is the share of must-check claims that the model both identified and labelled with the correct
status. A paper with a hard-gate violation scores 0. Twins enter Track A with the same weight as a
paper.

Reported beside it, never folded in:

- claim recall (identification);
- claim outcome accuracy (reproduces vs does not);
- sensitivity to discrepancies (P1 and P1+P2) and specificity (reproducing claims not flagged);
- paper outcome accuracy;
- nondeterminism recognition (gold nondeterministic claims the model flagged, and false flags);
- unsupported fixes and fixes that change the analysis;
- blocked claims reported as not reproducing;
- hard-gate violations;
- cost: wall-clock minutes, tokens and US$ per paper.

**Hard gates.** Invalid certificate; a claim or value the paper does not print; a recomputed value
with no code and log behind it; a fetch of the authors' code in Track B; editing the gold or
reading earlier reproduction reports.

With 30 to 48 targets per track, differences of a few points are noise. Scores are reported with a
paper-level bootstrap interval.

## 7. Modular pipeline

The benchmark separates **inputs**, **pipelines** and **scoring**, so that any model, prompt or
sequence of steps can be run on the same inputs and scored the same way.

### 7.1 Inputs (per target, built once)

```
inputs/<track>/<target>/
  target.json      # doi, article URL, track, package (URL + version pin, or local path)
  claims.json      # gold claim list, verdict-free (used only in decomposed mode)
  package/         # local package for twins and Track B (built by script, not committed)
```

### 7.2 Stage contracts

A pipeline produces some or all of these files, each with a JSON schema:

| Stage | Input | Output |
|---|---|---|
| S1 identify | article, package | `claims.json`: id, claim, exhibit, page, quantity, printed value |
| S2 reproduce | package, `claims.json` | `results.json`: per printed number, recomputed value, basis, fix, nondeterminism, code and log references |
| S3 judge | `results.json`, printed values | `certificate.json` (schema 1.2): statuses, paper outcome |

A single-agent pipeline does S1 to S3 in one run and writes all three files. A multi-step pipeline
can use a different model or prompt per stage. In decomposed mode, the runner supplies the gold
`claims.json` in place of S1.

### 7.3 Pipeline manifest

```json
{"name": "luna-codex-medium", "track": "A", "mode": "end_to_end",
 "executor": "codex_cli", "model": "gpt-6-luna", "options": {"reasoning_effort": "medium"},
 "stages": [{"id": "S1-S3", "prompt": "prompts/check-A-v0.2.txt"}],
 "timeout_minutes": 75}
```

Executors are small adapters (Codex CLI, Claude Code, OpenCode, an API loop, a human), each taking
a filled prompt and a working directory and returning the stage files and a run record (exit status,
minutes, tokens, cost). The runner fills prompts from `target.json`, creates a fresh directory per
run outside the repository, and copies the outputs to `runs/<pipeline>/<target>/`. Scoring reads only
those outputs.

### 7.4 Isolation

Runs execute outside the repository, so gold files and twin metadata are out of reach. Network access
stays open because packages must install; the run log is checked for fetches of earlier reproduction
reports and, in Track B, of the authors' code.

## 8. What exists and what is left

Exists: gold v1.3 (30 papers), eight verified twins with rendered outputs stripped, the certificate
schema 1.1, the scorer (match and close distinct), the Codex runner, and two validation batches on
GPT-6 Luna (five targets each). The batch 2 twin certificates predate the stripping and are kept only
as a record.

Left, in order: gold v1.4 and schema 1.2 (sections 4 and 5); the stage schemas, manifest runner and
executor adapters (section 7); mapping tests (3.3); the Stata papers; Track B eligibility, packages
and gold; then the full Luna run on both tracks.
