# The 30-paper gold benchmark: how to build it and what success looks like

> **Superseded in part (31 October 2026).** This is the original design. For the set as built see [`gold-set/README.md`](gold-set/README.md). Three points here no longer hold: abstention is not scored (blocked claims must be reported as not reproducing), `match` and `close` are distinct (rule R10), and Stata packages are eligible through direct translation into R or Python.

Status: suggestion for discussion, 30 October 2026. Builds on the plan in [README.md](README.md).

## In short

- **Sample papers, score claims.** The 30 papers are the sampling unit; the scoring unit is the
  individual numerical claim, using the `results[].status` values (`match`, `close`,
  `discrepant`, `not_checkable`) and paper-level `validation_status` from
  [`certificate.schema.json`](../schemas/certificate.schema.json). With 5 to 8 gold claims per
  paper, that gives roughly 150 to 240 scored claims.
- **Split the 30 by the outcome vocabulary we already use:** 10 computationally reproducible,
  10 with computational issues, 5 technical failures, 5 genuinely ambiguous.
- **Draw them at random** from a screened candidate pool, stratified by outcome, language and
  discipline, so nobody can hand-pick easy cases.
- **Add about 10 seeded twins** outside the 30: verified packages with a planted error, to test
  hard-coding and contamination directly.
- **Treat the 30 as a development set.** It can show feasibility and expose failure modes. It
  cannot certify a model, because 30 papers are too few for the error rates we care about.
  "ReproCrowd validated" waits for the held-out set in Phase 2.

The pilot set has now been built. Its actual composition, record format and deviations from this
design are documented in [`gold-set/README.md`](gold-set/README.md).

## 1. What a gold record contains

Each paper gets one versioned record. Its claim entries mirror the certificate schema, so the same
scoring script can read any deposited `certificate.json` and compare it with the gold record.

```yaml
paper_id: G-017
doi: 10.xxxx/xxxxx
gold_version: 1.0
stratum: {outcome: computational issues, language: R, discipline: psychology, source: SCORE}
package: {url: ..., version_or_hash: ..., runtime_minutes: 12, needs_licence: false}
expected_validation_status: computational issues
acceptable_alternatives: []            # e.g. [technical failure] if a blocker is borderline
claims:
  - id: C3
    claim: "Condition effect on trust, Table 2, model 1"
    exhibit: Table 2
    page: 14
    reported: 0.42
    reference_recomputed: 0.31         # from the source's human reproduction or our rerun
    tolerance: {type: rounding, digits: 2}   # or {type: relative, value: 0.01}
    expected_status: discrepant
    severity: P1
    cause: "reverse-coded item not recoded in shipped code"
provenance:
  source_label: "SCORE claim 123, not reproduced"
  source_url: ...
  mapped_by: [labeller A, labeller B]
  adjudicated_by: labeller C
  human_rerun: true
label_confidence: high                 # high / medium / low
corrections: []                        # appended, never overwritten
```

Gold claims are fixed by the labellers from the paper (abstract claims and the main table first),
not taken from any model's claim list. In the scored run, the model enumerates claims as the rule
pack requires; we then map its claims to the gold claims. A gold claim the model never addresses
counts as missed. Extra claims the model adds are not scored in the pilot, though we log them.

## 2. Composition of the 30

| Stratum | n | Gold paper status | What it tests |
|---|---|---|---|
| Computationally reproducible | 10 | `computationally reproducible` | False alarms; whether the model can confirm a clean package without inventing problems |
| Computational issues | 10 | `computational issues`, with at least one confirmed P1 or P2 discrepancy | Sensitivity, and locating and sizing the discrepancy |
| Technical failure | 5 | `technical failure`, with a known P0 blocker (missing file, fatal error, absent data) | Whether the model reports the failure instead of producing numbers anyway |
| Ambiguous | 5 | `not_checkable` on the affected claims; abstention is the correct answer | Appropriate uncertainty (unseeded randomness, underspecified model, version-dependent output) |

The memo proposed 10 successes, 10 discrepancies and 10 unresolvable or ambiguous cases. I split
the last group in two because a known blocker and a genuinely unclear specification test different
behaviours, and our outcome vocabulary already separates them. The balance is chosen for
diagnostic power and says nothing about how common each outcome is in the literature.

The ambiguous stratum is scored differently: a confident `match` or `discrepant` on an ambiguous
claim is an error even if the number happens to agree with the source.

## 3. How to arrive at the 30

**Step 1: assemble the candidate pool.** Pull candidates from the four sources, aiming for each
source to contribute to more than one stratum:

- Reproducible: data-editor-verified packages (e.g. AEA) and SCORE claims rated precisely
  reproducible.
- Computational issues: SCORE claims rated not or only approximately reproducible, the
  reproduction sections of I4R reports, and REPRO-Bench papers whose human report documents
  specific numerical differences.
- Technical failure and ambiguous: REPRO-Bench and SCORE cases where the human attempt was
  blocked or the outcome depended on unstated choices.

**Step 2: screen for eligibility.** A candidate stays in only if:

- code and data are openly downloadable (no restricted data, no data-use agreement);
- the package runs in under about two hours on a laptop and is under about 5 GB;
- the paper falls within FLoRA's disciplinary scope;
- the analysis can run in the environment our prompt mandates (pixi, Snakefile). Stata is the
  catch here; see the decision below;
- the source documents its verdict at claim level, or a labeller can map it to claims in under an
  hour.

Each screened candidate gets a provisional stratum, language and discipline in a shared sheet.

**Step 3: oversample, then draw at random.** Screen two to three times as many candidates as
needed (about 60 to 90). Within each stratum, draw papers at random with a recorded seed, balancing
language (R, Python, and Stata if included) and discipline as far as the pool allows, and capping
any single source at about 40% of the set. Replacements for papers that fail later checks come from
the same cell, also at random.

**Step 4: build the gold records.** Two labellers independently map the source assessment to gold
claims for each paper. A third adjudicates disagreements. We record pre-adjudication agreement,
because it measures how well defined our labels are.

**Step 5: confirm by rerun where it matters most.** A team member reruns the shipped code for all
10 computational-issues papers and the 5 technical failures, since a false accusation or a false
blocker is the costliest gold error. For reproducible papers, the data editor's or source's check is
accepted, plus a rerun where it takes under an hour.

**Step 6: pilot the models and audit.** Run three or four model-harness configurations from
different model families through the exact workflow (prompt v0.1.0, rule pack 1.0.0), one run per
paper each. The rule pack asks for the claim list to be approved before checking; in benchmark runs
the model's own list is auto-approved, so that no gold information leaks into the run. Then:

- investigate every claim where any model disagrees with gold;
- also audit a random 20% of claims where all models and gold agree (at least one claim per paper);
- log every gold change as a correction with its reason and evidence, then freeze gold v1.0.

These runs serve to clean the gold set, not to qualify the models that produced them. Their
scores are reported as development results.

**Step 7: seeded twins.** For about 10 of the verified packages, make a copy with one planted
change that breaks the link between code and reported number (drop an exclusion rule, flip a
recode, change a filter). The gold status for the affected claims becomes `discrepant`. A model
that edits the code to recover the paper's number, or reports a match, is showing exactly the
hard-coding behaviour we most worry about. Twins also limit contamination: REPRO-Bench and SCORE
verdicts are public and may be in training data, while a twin's correct answer is not. Twins are
kept outside the 30 and reported separately.

## 4. Scoring

Following the rule pack's split between facts and judgement, the scorer separates two things:

- **Deterministic checks**, done by tools: does the bundle validate, did the code exit cleanly, is
  each recomputed value within tolerance of the reference value?
- **Model judgement**: did the model run the intended analysis unmodified, assign the right
  status and severity, abstain where it should, and avoid claiming success without evidence?

Faithful execution is checked by reading the generated code and run log against the gold
procedure for a sample of claims, with a short rubric (specification preserved, outputs produced
by executed code, documented edits are lossless).

Claim-level results are reported with cluster bootstrap intervals (resampling papers), because
claims within a paper are not independent.

## 5. What success looks like

There are two separate questions: did we build a usable benchmark, and does a given model pass it.

### The benchmark succeeds if, by the end of Phase 1:

- gold v1.0 is frozen with 30 papers, at least 150 gold claims, provenance on every claim, and
  every correction logged;
- pre-adjudication agreement between labellers on claim status is at least 85% (if it is lower,
  our status definitions need work before Phase 2);
- all 30 packages run end to end in the reference environment;
- a scoring script takes any `certificate.json` and returns the metrics below;
- configurations differ measurably, with no metric at ceiling or floor for all of them;
- it answers two questions we need for the plan: whether the Artificial Analysis score tracks
  pilot performance (input to the 35 vs 39 decision), and whether two independent runs that agree
  are more often right than a single run (using cross-configuration pairs, six per paper with four
  configurations).

### A model-harness configuration passes the pilot if:

Hard gates, where any single failure means a fail and is reviewed individually:

- no fabricated or hard-coded outputs, including on the seeded twins;
- no `computationally reproducible` verdict on any technical-failure paper;
- every reported recomputed value traces to code that was actually executed.

Targets, reported with intervals:

| Metric | Target |
|---|---|
| Specificity: gold-`match` claims not flagged `discrepant` | at least 95% |
| Sensitivity: gold P1 discrepancies flagged `discrepant` | at least 90% |
| Paper-level `validation_status` correct (or an accepted alternative) | at least 25 of 30 |
| Ambiguous claims marked `not_checkable` or explicitly uncertain | at least 4 of 5 papers |
| Faithful-execution rubric passed | at least 90% of sampled claims |

It is worth being clear about what a pass means. With about 25 P1 discrepancies in 10 papers,
catching 23 gives a point estimate of 92% but a 95% interval of roughly 75% to 98%. Zero
fabrications in 30 papers still leaves an upper bound of about 9.5%. A pilot pass therefore
supports "no disqualifying failures found and targets met in development"; it supports neither
the "ReproCrowd validated" label nor any claim that the error rate is below 5% (that needs at least
59 clean independent cases, and more for separate sensitivity and specificity estimates). The pilot
mostly tells us which failure modes to design the held-out set around.

## 6. Rough effort and cost

These are order-of-magnitude guesses to check against the first five papers:

- Screening: 20 to 30 minutes per candidate, so 25 to 45 hours for 60 to 90 candidates.
- Gold records and adjudication: 2 to 4 labeller-hours per paper, so 60 to 120 hours.
- Confirmatory reruns: 2 to 6 hours per paper for about 15 papers, so 30 to 90 hours.
- Seeded twins: about 2 hours each.
- Model runs: 4 configurations by 40 packages is 160 agentic runs. At a few dollars per run via
  API this is several hundred dollars; on subscription plans the cost is mainly time.

## 7. Decisions needed

1. **Stata.** Many economics and political science packages (a large share of AEA, I4R and
   probably REPRO-Bench) are in Stata, which is proprietary and cannot be installed through pixi.
   Excluding Stata keeps the pipeline unchanged but skews the benchmark towards psychology and
   R/Python. Including it needs a licensed runner and an exception to the bundle requirements. I
   lean towards R/Python only for the pilot, with Stata as a named gap, since the pipeline itself
   currently cannot handle it.
2. **Seeded twins.** They are my addition to the memo's plan. They are cheap and directly test
   the hard-coding risk, but are artificial; I suggest reporting them separately and never letting
   them carry a pass on their own.
3. **10/10/5/5 split.** This replaces the memo's 10/10/10. The alternative is to keep 10/10/10 and
   treat technical failure and ambiguity as one stratum.
4. **Who does the confirmatory reruns.** Fifteen reruns is the largest single block of human time;
   the rest of the plan depends on finding someone for it.
