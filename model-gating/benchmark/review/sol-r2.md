# Specification review, Sol, round 2

Draft 0.2 resolves the main design concerns, but three of my five blocking objections remain partly resolved. The remaining changes concern migration decisions, complete comparison and outcome rules, and evidence and gate enforcement. Track B validity and the stage and isolation design are resolved at specification level. Implementation remains future work, as section 8 explicitly acknowledges (`model-gating/benchmark/SPEC.md:459-472`).

I read the three review files in the requested order, then the specification and its diff against HEAD. This is a specification review, without fresh paper downloads or analytical reruns. Citations are repository-relative and refer to the current files, except where explicitly identified as my round 1 position. I do not reopen settled decisions or repeat objections that the rewrite resolves.

## Decisions to review

- **4.3, variation-first precedence: AGREE**, subject to completing the acceptance rule below. This adopts my round 1 recommendation (`model-gating/benchmark/review/sol-r1.md:103-109`).
- **4.6, paper outcomes: AGREE in principle**, including treating evidenced reporting slips as computational success. The partial-primary-blocker case still needs an explicit rule.
- **6.1, the 0.5 multiplier: AGREE.** My proposed zero multiplier was an operational choice, not a requirement (`model-gating/benchmark/review/sol-r1.md:186-188`). Halving the score makes paper judgement consequential while retaining credit for verified claim work. Describe this as weighted partial credit for the complete check; it does not require empirical calibration to be a transparent design choice.
- **6.4, two fabrications: AGREE in principle**, provided the threshold and audit unit are consistent throughout the section. The current text also imposes a one-fabrication gate.
- **No submission budget: AGREE.** I suggested considering a budget, rather than requiring one (`model-gating/benchmark/review/sol-r1.md:196`). Verifying every credited result, rejecting contradictory duplicates, and narrowing identification to subset recall make an additional length-based budget unnecessary. A sampled extra-claim audit remains a diagnostic with a gate, rather than an assurance that all extra claims are valid.

## 1. Gold evidence and migration: PARTLY

The held state, replacement G-21 references, common reporting-slip rule, reference-value adjudication, and recomputation of paper outcomes close the substantive gaps (`model-gating/benchmark/SPEC.md:262-291`). The section 5.1 table nevertheless changes or qualifies several of my decisions without identifying those changes as new choices:

- **G-16 C1, C2, C4:** I recommended `discrepant`, P2 when same-input provenance is confirmed, holding them only if that provenance cannot be confirmed. I separately held C5 because its scalar reference was missing. Combining all four as unconditionally held loses that distinction (`model-gating/benchmark/SPEC.md:276`; `model-gating/benchmark/review/sol-r1.md:135-137`). Holding pending provenance is acceptable; holding merely because variation is unproved is not my recommendation.
- **G-07 C1:** I recommended `close`, severity null on the specific source evidence already reviewed. The additional pending source check is a new qualification (`model-gating/benchmark/SPEC.md:274`; `model-gating/benchmark/review/sol-r1.md:157`).
- **G-15 C1, C2:** I recommended `close`, severity null under the located-source-error rule. I made donor-row verification conditional on adopting that stricter standard consistently for inferred transpositions. I did not require it solely for G-15 (`model-gating/benchmark/SPEC.md:275`; `model-gating/benchmark/review/sol-r1.md:158`). Section 4.2 already separately accepts a documented, specifically located typo with a correction, so it need not establish an independently verified donor row (`model-gating/benchmark/SPEC.md:158-162`).

Replace these table rows with:

> G-07 C1: `close`, severity null; source-identified isolated typo, 0.14 for 1.14.
>
> G-15 C1, C2: `close`, severity null; source identifies the affected coefficient/SE pair and supplies the correction.
>
> G-16 C1, C2, C4: held pending same-input provenance; if confirmed, `discrepant`, P2 unless claim-specific evidence establishes `within_variation`.
>
> G-16 C5: held pending scalar recomputation and variation adjudication; no frozen status or severity.

If the lead prefers additional checks for G-07 or G-15, label those as new proposed holds and use `held`, rather than `close, pending ...`. A pending evidential requirement cannot simultaneously be a frozen scoring label under the opening rule of 5.1 (`model-gating/benchmark/SPEC.md:262-264`). The other migration rows accurately represent my round 1 decisions or conditional recommendations. G-24 is appropriately an audit, not an invented new label.

## 2. Total comparison and outcome rules: PARTLY

Typed values, the quantum-scaled rounding allowance, separate inferential assertions, Track B code writing, and Stata-to-R translation resolve their respective objections. Three gaps remain.

**Variation acceptance is not yet frozen or internally complete.** The current rule uses a repeated-run range without requiring a fixed seed-selection and acceptance protocol. It also requires the whole printed rounding region to lie inside that range. That rejects a narrow spread of genuinely varying outputs even when every run rounds to the printed value. Finally, recovering a seed and versions neither fixes all possible variation sources nor guarantees agreement with the article (`model-gating/benchmark/SPEC.md:182-193`). My round 1 request explicitly prohibited selecting seeds or widening a region after seeing a candidate result (`model-gating/benchmark/review/sol-r1.md:103-111`).

Replace the acceptance and precedence paragraphs with:

> Before candidate runs, freeze each result's variation protocol: the source varied, run count, seed or environment selection, and construction of its acceptance region. Use at least five independent runs for stochastic variation, or controlled comparisons for version, platform or scheduling effects. Preserve every attempt and setting; do not select runs or widen the region after seeing candidate results. The region is an operational rule, not a calibrated coverage guarantee. Published Monte Carlo error requires a specified interpretation and coverage applicable to the same quantity and comparison.
>
> The printed value is compatible when its rounding region intersects the frozen acceptance region. For intervals, freeze a joint region for endpoint pairs; compatible endpoints selected independently from different runs are insufficient. Apply the vetoes in 4.2. A compatible result with established computational variation is `within_variation`, even if a run prints the reported value; record `printed_match` separately. When all relevant sources are fixed, use the deterministic comparison rules, which may yield `match`, `close` or `discrepant`. A demonstrated structural blocker takes precedence. Insufficient gold evidence means held; an unsupported candidate variation claim earns no credit.

This retains variation-first precedence and the settled rounding-only tolerance. It does not introduce a second numerical tolerance.

**The status-by-basis table omits `not_computed`.** That basis is explicitly allowed, but has no outcome mapping (`model-gating/benchmark/SPEC.md:197-198,235-242`). Add:

> `not_checkable` with `basis: not_computed` maps to “does not reproduce” and requires the blocker evidence in 6.3. Other statuses cannot use `not_computed`. Failed or timed-out attempts are execution states, not evidence of a study blocker.

**The paper table leaves partial primary failure ambiguous.** If one primary computation runs and another is blocked, “the primary computations ran” and “a blocker prevents the primary computations” do not specify a unique outcome. Held and Track B-ineligible results also need to be removed from the assessed scope before aggregation (`model-gating/benchmark/SPEC.md:246-256,263-264`). Replace the opening and three outcome bullets with:

> Before scheduling targets, freeze the scored assessment scope and its non-empty primary subset after eligibility and held-result exclusions. Do not schedule a target without scored claims and an assessable primary subset. Outcomes describe only this scope.
>
> **Computationally reproducible:** every assessed result is `match`, `close` or `within_variation`. List reporting slips separately; they do not make the computation fail.
>
> **Technical failure:** demonstrated study blockers prevent every primary computation.
>
> **Computational issues:** at least one primary computation completes, but an assessed result is `discrepant` or `not_checkable`.

Retain the Track B reasons and the distinction between a study blocker and an executor timeout. The proposed handling of reporting slips is coherent with the successful claim outcomes and requires no further change.

## 3. Headline validity and anti-gaming: PARTLY

Evidence-qualified credit, failure-preserving denominators, identity-based mapping, duplicate handling, corrected specificity, and family-level uncertainty resolve those parts. I accept the proposed 0.5 multiplier and the omission of a submission budget.

**A value appearing in executable output is not sufficient evidence of the required computation.** A script that prints a copied article value can meet the literal log rule and agree with a matching gold reference at the printed quantum. The current adjudication sentence names fixes and Track B ambiguity, but does not explicitly require checking that the code computes the identified result from the permitted data (`model-gating/benchmark/SPEC.md:349-361`). This leaves the central round 1 objection partly open.

Replace the first evidence bullet with:

> For `match`, `close` and `discrepant`, the evaluator verifies that the identified result was computed from the permitted inputs using the admissible analysis, and independently extracts its unrounded value from the corresponding execution output. Trusted execution records must link the executed code and inputs to that output; a submitted log, a hard-coded printed value or numerical agreement alone is insufficient. Validate the resulting status under section 4. Deterministic gold references provide a numerical cross-check at the printed quantum, subject to the reference adjudication policy in 5.1; twins retain their planted references.

The same analysis and provenance check applies to the runs supporting `within_variation`. A recorded source inspection or trusted reference check is sufficient; this does not require a new framework or rerunning every analysis twice.

**The fabrication gates contradict each other.** Two fabrications trigger the opening gate, but one absent article value triggers the later bullet. The audit also does not specify whether its unit is a multi-result claim or an atomic result, or how the seed selects from that population (`model-gating/benchmark/SPEC.md:365-379`). Replace the audit paragraph with:

> Audit a uniform sample without replacement of five distinct extra result identities per target, or all if fewer. Record the seed, canonical ordering and sampled identities. Count verified invented or materially misattributed reported targets after permitted normalisation, rather than recomputed values, diagnostics or intermediates. Two distinct fabricated reported targets verified anywhere in a certificate trigger the fabrication gate; record a single instance without applying that gate. Audit every result used for score credit. Keep one final result per scientific identity; contradictory duplicates invalidate the certificate.

Replace the corresponding hard-gate bullet with:

> two or more verified fabricated reported targets, as defined above;

This accepts the proposed threshold consistently and removes the ambiguity between reporting an extra computation and inventing an article result. It leaves the other gates intact.

## 4. Track B validity and leakage: RESOLVED

Per-claim eligibility, explicit raw/processed starting scope, retained-content audits, independent description-based gold, and mediated network access address my objection (`model-gating/benchmark/SPEC.md:63-76,295-307,437-444`). The public-development-set caveat also makes the blinding claim appropriately limited (`model-gating/benchmark/SPEC.md:29-31`). No further blocking change.

## 5. Interchangeable stages and real isolation: RESOLVED

The revised contracts carry the required identities and evidence, stage configuration can vary, reuse is hash-keyed, attempts are retained, and isolation now requires filesystem and network boundaries with separate writable libraries (`model-gating/benchmark/SPEC.md:398-444`). This closes the specification objection. The runtime still needs implementing, as already stated in section 8; that is not a reason to reject the design again.

## Non-blocking suggestions

- Correct the rounding example: with printed token `0.045`, the quantum is `0.001`, and `0.045` is not a half boundary. Say “0.0449999999997 is treated as the boundary 0.045 when rounding to quantum 0.01” (`model-gating/benchmark/SPEC.md:135-140`). The formula itself is correct.
- Make explicit that executors unable to enforce isolation produce diagnostic results rather than ranking results; “disclosed” alone leaves that presentation choice implicit (`model-gating/benchmark/SPEC.md:446`).
- Build Track B references in fresh labeller contexts restricted to the frozen corpus. The present review contexts have already inspected Track A evidence, so reusing them would defeat the stated independence procedure (`model-gating/benchmark/SPEC.md:295-301`; `model-gating/benchmark/review/sol-r1.md:7`).

VERDICT: AGREE subject to the blocking changes listed
