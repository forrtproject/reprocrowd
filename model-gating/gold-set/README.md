# Gold set v1.1 (30 papers)

The pilot gold benchmark proposed in [`../gold-benchmark-30.md`](../gold-benchmark-30.md). Each
record states what a paper's shipped original code and data produce relative to the printed
numbers, at the level of individual claims, using the outcome vocabulary of
[`certificate.schema.json`](../../schemas/certificate.schema.json). It is a development set, not a
qualification set.

## Contents

| File | What it is |
|---|---|
| `gold/G-01.json` to `gold/G-30.json` | The gold records (claims, expected statuses, severities, scoring references, diagnostics, provenance) |
| `gold-summary.csv` | One row per paper: expected status, alternatives, claim counts, confidence |
| `candidates.csv`, `screening-notes.md` | The screened pool (111 rows, 49 eligible) and how it was built |
| `draw.json` | The stratified random draw (seed 20261030) and reserves |
| `claims/` | The shared, verdict-free claim lists both labellers worked from |
| `labels/sol/`, `labels/claude/` | The two independent label sets, as reconciled |
| `reconciliation.md` | Every disagreement, the rules adopted to settle it, and both sides' sign-off |
| `audit/` | Sol's targeted check scripts and logs for G-19 and G-30, and in `audit/screening/` the screening scripts and intermediate JSON. They read files downloaded to a temporary folder that no longer exists; inputs are pinned by hash in the claims files. The G-14 references to a temporary `Data_Extraction.csv` are hash-pinned the same way. Two large re-derivable inputs were not kept: the per-task REPRO-Bench Hugging Face inventories and `packages_summary.json` |
| `reruns/` | Agent executions of the shipped code for G-04 and G-26 (results, trimmed logs, commands) |
| `twins/` | Eight seeded twins (T-01 to T-08): one planted change each, with patch, expected labels and run logs |
| `pilot/` | Six certificates from running the real prompt on G-08, G-21 and G-23 with two models, and their scores |

Scripts are in [`../scripts/`](../scripts/):
- `draw_gold.py`: the stratified draw.
- `compare_labels.py`: compares the two label sets.
- `build_gold.py`: rebuilds `gold/` and `gold-summary.csv` from the claims and labels.
- `score_certificate.py`: scores any set of certificates against gold papers or twins, with cluster-bootstrap intervals and hard-gate checks.
- `test_score_certificate.py`: sanity tests for the scorer.

## How it was built

1. **Screening (GPT-6.1 Sol, two rounds).** Sol screened 111 candidates from I4R reports,
   REPRO-Bench, SCORE and CODECHECK against the eligibility rules: open code and data, R or
   Python, under about two hours and 5 GB, social or behavioural science, and mappable to 5 to 8
   numerical claims. 49 were eligible. Journal data-editor checks gave no usable public claim-level
   verdicts.
2. **Draw (Claude).** Stratified random draw with a fixed seed. Planned strata were 10/10/5/5;
   the pool held only three eligible technical failures, so the draw used 12 reproducible,
   10 issues, 3 technical failure and 5 ambiguous. One drawn paper (I4R-qe3fx) was replaced from the
   reserve list.
3. **Claim lists (Sol).** 5 to 8 claims per paper, taken from results the human source assessed,
   with printed values copied from the paper and no verdict information.
4. **Independent labelling.** Sol and six blind Claude labellers labelled every claim from the
   source reports, the papers and static checks of the shipped files. Nobody reran a full
   analysis. Before reconciliation, paper-level status agreed on 25 of 30 papers and claim status on
   161 of 167 claims (after G-14, whose claim list changed mid-labelling, was relabelled blind).
5. **Reconciliation.** Three rounds settled the differences through nine written rules (R1 to R9 in
   `reconciliation.md`), covering paper status for abstention claims, severity, lossless edits,
   reference provenance and paper-level alternatives. Both labellers agree on every paper status,
   claim status and severity, and Sol's last entry reads "FINAL: AGREE to freeze gold v1.0".
6. **Execution and v1.1 (round 4).** Agent reruns of the shipped code confirmed every claim of
   G-04 and G-26, the two papers flagged for a rerun in v1.0. The pilot runs exposed three gold
   errors. On G-08, both pilot models found two wrong printed numbers the human report missed; these
   were added as claims C6 and C7, and the paper became `computational issues`. On G-23, claims C3
   and C4 turned out to be computable from shipped code (C3 match, C4 discrepant). Sol checked and
   agreed to every change ("FINAL: AGREE to gold v1.1"). Each changed record lists its
   `corrections`.

## What the set contains

The final statuses differ from the drawn strata because labels follow the evidence. For example,
G-07 has a wrong printed SD, and G-19's blocker turned out to be a lossless filename fix.

- Papers: 13 computationally reproducible, 13 computational issues, 4 technical failure.
- Claims: 169 in total. 103 match, 8 close, 29 discrepant (3 P1, 26 P2) and 29 not_checkable.
  Of the not_checkable claims, 24 are P0 blockers; the other 5 depend on unstated choices such as
  unseeded bootstraps or undefined procedures.
- Execution evidence: agents have run the shipped code for the selected claims of 11 papers: the
  eight twin bases, the G-04 and G-26 reruns, and pilot runs of G-08, G-21 and G-23. The
  remaining labels rest on human reports and static checks.
- Twins: 8 seeded twins with 20 planted discrepant claims (13 P1, 7 P2). Score them separately.

## Limitations

- **One source dominates.** 28 of the 30 papers rest on Institute for Replication reports (REPRO-Bench's human reports are I4R reports; the exceptions are one CODECHECK and one SCORE case), and the
  set leans heavily towards psychology and R. This reflects which public reports have claim-level
  detail and open R or Python code; it is not a sample of the literature.
- **Few P1 discrepancies.** Only 3 of the 29 discrepant claims in the 30 papers are P1 (the twins add 13). Most documented
  discrepancies are wrong secondary numbers (P2), so sensitivity has to be estimated on P1 and P2
  together.
- **Partial execution.** 19 papers still rest on human reports and static checks. One paper (G-16)
  has low label confidence. No human has rerun any analysis; all executions were by agents.
- **Public sources.** All reports are public, so models may have seen them. The twins counter
  this, because their correct answers exist nowhere else.
- **Human reports miss things.** G-08 shows that a favourable human report does not guarantee
  every printed number recurs. Gold labels for unexecuted papers may contain similar errors.
