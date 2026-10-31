# ReproCrowd rule pack — crowd-repro

**Version:** `1.1.0`
**URI:** `https://forrtproject.github.io/reprocrowd/crowd-repro/RULEPACK-v1.1.0.md`
**Status:** stable
**Maintainer:** ReproCrowd
**License:** CC BY 4.0
**Reference:** `reprocrowd/PROMPT.md`, `reprocrowd/WORKFLOW.md`

A ReproCrowd certificate reports on **computational reproducibility**: whether a paper's
shipped code and data can be re-executed and whether the reported outputs recur. It is a
**Reproduction Study** (same methodology, same tools). It does **not** rule on whether the
science is correct; that is a separate robustness/replication question.

## Change log

- **1.1.0** (this version): checks rather than certifies; every result states its `basis`
  (shipped code, justified fix, direct translation, not computed); agent-written or respecified
  analyses never count as a reproduction; Stata code is translated directly into R or Python;
  claim statuses are defined (§12); certificate schema 1.1.
- **1.0.0**: initial release. Six-phase workflow, six-step FORRT chain,
  computational-only outcome vocabulary, single sign-off file, FLoRA import mapping.

---

## 1. Purpose and scope
- Check whether the computation is reproducible and executable, and report what does and
  does not recur. Finding that something does not reproduce is as useful as finding that it
  does.
- Record, do not judge. Do **not** write "the paper is right/wrong"; write "the computation
  reproduced / did not reproduce the reported value X."
- Computational work only. No robustness or sensitivity analysis; that is out of scope.

## 2. The split
- Tools decide facts: real DOI, verbatim quote, did the run exit 0, does the value recur, is
  the term valid. A tool answer is final.
- The model proposes judgement: which sentence is the claim, the scope, how to phrase the outcome.

## 3. Copy, never touch
- Work on a copy (`working/`). Keep the shipped originals untouched (`extracted/`).
- Only **justified, documented** fixes to make it run: changes that leave the analysis
  unchanged (comment a hard-coded `setwd`, fix a path, install or pin a package, replace a
  deprecated call by an exact equivalent, run scripts in the right order). State exactly what
  changed in the result's `fix` field.
- Never write missing analysis code yourself, and never change the model specification, sample,
  exclusions or data to make a number recur. A value obtained that way is not a reproduction:
  report the claim as `not_checkable` (or `discrepant` if the shipped code gives a different
  value) and describe the attempt in `note`.
- Shipped Stata code (or code in another language you cannot run): translate it directly,
  command by command, into R (preferred) or Python, keep the translation in the bundle, and mark
  the results `basis: translated`. A translation follows the original; it does not improve it.
  If a command has no exact equivalent, say so and treat dependent claims as `not_checkable`.

## 4. Report both sides
- Report what reproduces and what does not, with exact numbers and the method used.
- A "cannot verify" needs the algorithm used, the numeric gap, and your judgement
  (algorithm difference vs data/analysis issue vs version drift).

## 5. Pin everything
- Header records: **repro standard version** (this rule pack version, e.g. `1.1.0`), **engine**
  (engine + model + provider), audit date, host OS, and the **procedure version** you ran.
- Record the **full program inventory**: every interpreter (R / Python / Stata / …) with its
  exact version, every package with its exact version, and the lockfile
  (`sessionInfo()`, `renv.lock`, `requirements.txt`, `pixi.lock`); flag version drift.
- Same header convention as a ReproAI report (`Engine: <engine> · rules: <version>`) plus the
  full environment block.

## 6. Enumerate claims first
- List every numeric claim (C1, C2, …) and the exhibits they map to; get the list approved
  before checking.

## 7. Verify, don't recall
- Quotes verbatim from the PDF (`verify_quote`); DOIs must resolve (`resolve_doi`); Wikidata
  terms must exist (`wikidata_lookup`); vocabulary terms from the template's enumeration.
- If a tool cannot confirm a value, it is not a value.

## 8. Audit the audit
- Re-read for internal contradictions. Every finding gets a cause and a suggested fix; every
  non-checkable item gets a reason.

## 9. Severity (by impact on the run)
- **P0** blocks the run / primary input missing.
- **P1** a primary statistic or DV not reproducible.
- **P2** a secondary result not exactly reproducible / documentation gap.
- **P3** hygiene (paths, README drift, naming).

## 10. Open by default
- Report, pipeline, and environment are public. Credit the codechecker (human or agent) and
  the model. This is what makes reports comparable and re-runnable.

## 11. Outcome vocabulary (computational, not robustness)
Map the result to exactly one of the FLoRA `outcome_computational` terms:
- `computationally reproducible` — the run re-executed and the reported outputs recurred
  (state in `certificate.md` whether this needed justified fixes or a translation).
- `computational issues` — it ran but some outputs did not recur / were flawed.
- `technical failure` — it could not be executed as shipped (missing code/data, fatal error).
- `computation not checked` — no computational verification was attempted (e.g. no code or
  data was shipped). Rare: a ReproCrowd certificate normally performs a run.

Always set `outcome_robustness = not checked`. A ReproCrowd certificate does not test
robustness (`robust` / `robustness challenges` are FLoRA terms for reproductions that did, and
are out of scope here); do not fill the robustness fields.

## 12. Claim status and basis
Each result in `certificate.json` has a `status` and a `basis`.
- `match`: the recomputed value equals the printed value at its printed precision.
- `close`: the difference is a minor reporting slip you can name (rounding or truncation, a
  transposed digit, a typo), or, for an unseeded stochastic analysis, within simulation
  variation. In a deterministic analysis, `close` asserts a reporting error, so do not use it
  loosely.
- `discrepant`: any larger difference.
- `not_checkable`: the shipped code, with only justified fixes or a direct translation, cannot
  produce the value (missing data or code, fatal error).

`basis` is `shipped_code`, `justified_fix`, `translated` or `not_computed`. Only the first three
can support `match` or `close`.

Each claim has one of three outcomes: it **reproduces** (shipped code), it **reproduces with
justified fixes** (`justified_fix` or `translated`), or it **does not reproduce** (`discrepant` or
`not_checkable`).

## 13. Output
- `certificate.json` (machine-readable), `certificate.md` (the human-readable report), and
  `flora-entry.json` (the FLoRA import record with the AI-generated tag and the GitHub URL).
- **`SIGN-OFF.md`** (see the template) is the **single** file the prompter reviews and signs; it
  records the repro standard version, engine, full program inventory, certification outcome,
  evidence, findings counts, and the FLoRA delivery.
