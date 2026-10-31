# Model gating (Part 2: models and validation)

This folder holds the working plan for deciding which models' reproductions ReproCrowd puts
into FLoRA. It summarises the draft Part 2 memo of 23 October 2026 (developed in a
[ChatGPT conversation](https://chatgpt.com/share/6ae48bf0-cea8-83ed-b8ed-149661d8cdc0)) and the
design decisions taken before it was drafted. The concrete proposal for the first benchmark is in
[`gold-benchmark-30.md`](gold-benchmark-30.md). The resulting 30-paper gold set (v1.3) is in [`gold-set/`](gold-set/); benchmark runs and their scores are in [`benchmark/`](benchmark/).

Part 2 covers three tasks from the 16 October meeting: propose a two-route acceptance scheme with
a suggested cut-off, outline our own reproduction benchmark, and evaluate the two-model agreement
idea.

## Settled design decisions

1. **What we validate.** Both faithful execution (does the agent run the intended analysis and
   link every output to executed code?) and discrepancy detection (does it correctly flag matches
   and mismatches?), scored with separate metrics.
2. **What a model's status controls.** Publication eligibility. Anyone can deposit results from
   any model, but only results from sufficiently validated models appear in FLoRA by default.
3. **How the benchmark grows.** Progressively. We start with a small, carefully adjudicated set
   and expand it as evidence accumulates.
4. **What corroboration requires.** Agreement between independently produced, executable evidence
   packages. Whether the two runs used different model families is secondary.
5. **How labels work.** One simple public label, with the detailed confidence dimensions stored in
   the metadata.
6. **Two tasks, benchmarked separately (31 October 2026).** Models do *computational
   reproduction* (run the shipped code) and, separately, *blinded recreation* (rebuild the analysis
   from the paper without access to the code). The current gold set covers computational
   reproduction only. There, each claim has three outcomes: it reproduces, it reproduces with
   justified fixes, or it does not. Code a model writes itself counts as "does not reproduce".
7. **`match` and `close` are distinct (31 October 2026).** In a deterministic analysis, `close`
   asserts a minor reporting slip, so a model must not use it where the value matches.
8. **Stata (31 October 2026).** Models translate shipped Stata code directly into R (preferred)
   or Python, and the result is labelled as translated. Stata papers are therefore eligible for
   the benchmark.

The idea running through all five is that confidence in a model (or pipeline) and confidence in a
single reproduction result are different things. A benchmarked model can still fail on a given
paper, and a weaker model can produce a result that is fully checkable from its evidence package.
We record the two separately even where the public label merges them.

## Two routes to eligibility

**Route 1: general benchmark (provisional).** Models at or above a cut-off on the
[Artificial Analysis Intelligence Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)
are eligible without being tested by us. The memo reports the index as v4.3.2, combining ten
evaluations (agentic 30%, coding 20%, scientific reasoning 20%, general 30%). The agentic and
coding weight makes it more relevant than a knowledge benchmark. The memo advises against a
hallucination leaderboard, because our main risk is goal-directed error (silently changing a
specification, hard-coding a value so the output hits the reported number), which those
leaderboards do not measure.

- Cut-off (decided 31 October 2026): a model is eligible if it scores **at or above DeepSeek V4
  Flash** on the index at the time of assessment. The cut-off is pegged to a reference model rather
  than a number because Artificial Analysis rescales its scores when it changes the index.
  This replaces the memo's fixed 35 or 39.
- Record the exact model version and reasoning setting, plus the index version and both scores
  (the model's and DeepSeek V4 Flash's) at the time of submission.
- Artificial Analysis has a free [API](https://artificialanalysis.ai/api-reference), so we store
  scores rather than maintain a hand-curated whitelist.

**Route 2: ReproCrowd benchmark.** A model-harness configuration (model plus our prompt, rule
pack and tools) that passes our own benchmark earns the higher label. Validation attaches to the
configuration: the same model run with substantially changed prompts or tools does not inherit it.

## Our own benchmark

Ground truth comes from existing human reproduction efforts, audited against our definition of
computational reproduction rather than taken at face value. Counts below are as reported in the
memo and still need checking during the source audit.

| Source | What it offers | Main caveat |
|---|---|---|
| [REPRO-Bench](https://github.com/uiuc-kang-lab/REPRO-Bench) ([Hu et al., 2025](https://aclanthology.org/2025.findings-acl.1210/)) | 112 paper-level tasks with PDFs, packages and human reproduction reports; the best of three original agents reached 21.4% accuracy | Paper-level labels; public, so contamination risk |
| SCORE ([Miske et al., 2026](https://doi.org/10.1038/s41586-026-10203-5); [OSF repository](https://doi.org/10.17605/osf.io/ed8pj)) | 143 papers with data, 551 assessed claims, a living repository with corrections | Not every analysis was assessed; unassessed results count as unknown |
| [Institute for Replication](https://www.i4replication.org/reports) | 411 reports, including real discrepancies | Reports mix reproduction with robustness checks; only the reproduction part is usable |
| Journal data editors (e.g. [AEA](https://www.aeaweb.org/journals/data/faq)) | Packages checked against the manuscript before acceptance | Good for known successes; pre-acceptance fixes may be undocumented |
| Seeded cases | Verified packages with deliberately introduced errors | Exact ground truth, uncertain generalisability |

The benchmark is progressive: a 30-paper curated pilot first, then 100+ papers covering more
disciplines, software and failure modes, with a held-out set for qualification. Each paper gets a
structured, versioned reference assessment at the level of individual results, in the same shape
as the `certificate.json` that contributors deposit.

Label quality rests on five safeguards: import source labels with their provenance; have two
reviewers map a sample to our schema and adjudicate disagreements; investigate every model-human
disagreement (models sometimes reveal errors in the source label); audit a pre-specified random
share of agreements too, so correlated errors do not go unnoticed; and version every correction
instead of overwriting.

Success is measured on several dimensions rather than one accuracy score: faithful execution,
discrepancy detection, false alarms, unsupported success claims, and appropriate uncertainty. The
two most damaging failures are claiming success without executed evidence and falsely accusing
authors of a computational error. Proposed targets (to be calibrated) are at least 95%
specificity, at least 90% sensitivity for substantive discrepancies, zero fabricated or
hard-coded outcomes, and full traceability from every reported value to executed code.

A 30-paper pilot cannot establish these rates precisely. With zero failures in 30 independent
cases, the one-sided 95% upper bound on the failure rate is still about 9.5%; showing a rate
below 5% with zero failures needs about 59 cases. The pilot therefore builds and tests the
benchmark; it does not by itself justify a strong reliability claim.

## Two-model agreement

Agreement only counts as corroboration when two attempts were produced independently (neither saw
the other's conclusions or code), each is a complete executable package that passes the schema,
they agree on the specific results within predefined tolerances, and neither contains unresolved
contrary evidence. Corroboration is claim-specific, so two attempts can corroborate five results
and disagree on a sixth.

The stricter rule first suggested ("all submitted attempts must agree") lets a single careless or
malicious submission remove the label. Instead, every attempt stays visible and each result is
*corroborated* (two qualifying packages agree, no credible contrary evidence), *disputed* (a
contrary attempt brings traceable evidence) or *not corroborated*. A bare contrary verdict without
evidence does not revoke corroboration.

Whether agreement improves accuracy is an empirical question. Two frontier models can share
failure modes, especially if they reuse the same extracted procedures. On the benchmark we compare
two agreeing runs with single runs. Until that shows a gain, "corroborated" means independently
supported, not proven correct.

## Public labels

| Label | Criteria | In FLoRA by default? |
|---|---|---|
| Experimental | Model meets neither route | No |
| Provisionally validated | Route 1 cut-off met and pipeline requirements satisfied | Yes |
| ReproCrowd validated | Model-harness configuration passed our benchmark | Yes |
| Corroborated | At least two qualifying independent packages agree | Yes, subject to the eligibility rules |

"ReproCrowd validated" describes the method, not a finding. Corroboration is stored as a separate
flag. Every entry keeps model identifier, version, provider and reasoning setting; pipeline and
prompt versions; general benchmark score and version; ReproCrowd benchmark version and performance;
result-level agreement, disputes and corrections; and the scope of any human verification.

## Implementation sequence

1. Implement Route 1 with the Artificial Analysis API, pegged to DeepSeek V4 Flash.
2. Audit REPRO-Bench, SCORE, selected I4R reports and data-editor packages for coverage, access,
   unit of evaluation and evidence quality.
3. Build the 30-paper pilot (see [`gold-benchmark-30.md`](gold-benchmark-30.md)).
4. Run several model-harness configurations through the exact ReproCrowd workflow.
5. Expand to a held-out qualification set, calibrate thresholds, and test whether the Artificial
   Analysis score predicts benchmark performance well enough to keep Route 1.
6. Test whether corroboration adds accuracy before treating it as the top tier.

## Open decisions for the team

1. **What disqualifies a benchmark attempt outright?** The memo's preference is that clear
   evidence fabrication (hard-coded outputs, reporting a run that never happened) fails the whole
   attempt even when the final verdict is right, while other errors feed into the metrics.
2. **When does corroboration override the ordinary label?** The memo's preference is only after
   the benchmark shows that independent agreement adds predictive value; until then, it is shown
   as a descriptive attribute.
