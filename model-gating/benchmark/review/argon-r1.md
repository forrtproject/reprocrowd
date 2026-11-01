# Spec review, round 1: Gemini 4 Argon (High), 1 November 2026

Argon returned its review as a chat reply instead of writing this file. This record lists its
points and my (Claude's) check of each against the repository. Several citations in the reply point
to paths that do not exist (`/Users/lukaswallrich/crowd-repro/…`), and its section 3 answers the
open questions of the earlier status report rather than SPEC.md section 5, so it appears to have
read partly stale context. No verdict line was given.

| # | Argon's point | Check | Action |
|---|---|---|---|
| 1 | The Codex `workspace-write` sandbox restricts writes, not reads; a run can read the repository, including `gold-set/`. | Correct. | Spec: run each job in a container or as a user without access to the repository; until then, audit logs for repository paths. |
| 2 | Network is open; a web search can reach the public source reports or the public `forrtproject/reprocrowd` repository, which holds the gold labels. | Correct; the repository is public (`gh repo view`). | Spec: forbidden-URL audit (repository, FORRT site, every evidence URL in gold) as a hard gate; consider keeping future gold private. |
| 3 | Twins get a local path and gold papers a URL, so the prompt reveals which targets are twins; the path itself contains `T-02`. | Correct (`run_codex.py` lines 48–54; batch 2 T-02 certificate quotes the path). | Spec: every target gets a pre-staged local package under a neutral name. |
| 4 | Parallel runs share one writable R library; concurrent installs and version pins can collide. | Correct (`run_codex.py` line 73). | Spec: read-only base library plus a per-run writable library (or a container per run). |
| 5 | The slim bundle (code, logs, lockfile) is not checked or archived. | Correct (`run_codex.py` lines 92–98 copy only the certificate). | Spec: archive the whole output bundle and the event log; a missing code or log file is flagged. |
| 6 | `score_one` keeps only the last result per `claim_id`. | Not as stated: results are mapped by printed value (`map_claims`). The real gap is that a gold claim with a printed p value scores only one of its two results. | Spec: score every printed number of a gold claim, including `reported_p`. |
| 7 | Recomputed values are never checked against the gold reference; copying the printed value and saying `match` would score. | Correct. | Spec: where gold has a reference value, the model's recomputed value must agree with it, otherwise the claim counts as wrong. |
| 8 | Hard gate on blocked claims can be bypassed by labelling the basis `justified_fix`. | Incorrect: the gate is basis-independent (`score_certificate.py` lines 141–143). | None. |
| 9 | Twins are pooled with their base papers, double-counting unchanged claims and inflating the bootstrap. | Correct. | Spec: report twins separately (planted claims as their own metric); bootstrap clusters a twin with its base paper. |
| 10 | Own-claim matching on a short shared number can false-match. | Plausible. | Spec 3.3 already requires exhibit agreement and a review file. |
| 11 | G-21 C3–C5: accept both `match` and `discrepant`. | Reopens a settled decision. | None. |
| 12 | G-16 C1, C2, C4, C5: the shipped `.tex` tables match the printed values, so `match` should be accepted. | Reading shipped outputs is not recomputation. The point that an exact rerun may be possible if the `grf` version can be matched is valid under SPEC 4.3. | Ask Sol to decide whether the G-16 rerun can be pinned. |
| 13 | Rule pack and prompt must be updated with the status rules before the run, and the benchmark prompt regenerated. | Correct; already in SPEC section 8. | Make explicit. |
| 14 | G-08 C6 rationale and notes still argue for the one-week reading and `discrepant`. | Correct (`gold/G-08.json`, C6 `rationale`, `notes.sol`). | Fix in gold v1.4. |
| 15 | Claim selection can be tested cheaply and separately (paper only, emit a claim list). | Consistent with the spec's decomposed mode. | Add as stage S1 alone. |
