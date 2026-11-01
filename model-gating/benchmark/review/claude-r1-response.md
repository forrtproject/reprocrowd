# Responses to round 1 (Claude), 1 November 2026

SPEC.md draft 0.2 takes up the round 1 reviews as follows.

## Sol blocking objections

1. **Gold evidence and migration.** Adopted. The "held" state is in 5.1, G-16, G-28 C3, C4, C6 and
   G-29 C1 to C3 are held, G-07, G-15 and G-22 C3 now use one source-identified-slip standard (4.2),
   G-21 references are replaced, there is a reference-value policy (5.1), and G-24 has been added for
   audit.
2. **Comparison and outcome rules.** Adopted: typed printed values (3.2), the `q`-scaled boundary
   rule (4.1), bounds as separate results (4.1), a variation precedence (4.3, proposed:
   variation first), the status by basis table (4.5), the claim aggregation rule (4.5), and the
   paper decision table (4.6, proposed). Stata goes to R only, and Track B code writing is now allowed
   (4.4).
3. **Headline validity.** Adopted: credit needs evidence (6.1, 6.3), the paper outcome enters the
   headline, failures stay in the denominator, mapping is identity-based (3.3), there is an extra-claim
   audit (6.4), specificity is corrected (6.2), baselines are reported, and the bootstrap resamples
   paper families (6.5). One change from your proposal: a wrong paper outcome halves the paper score
   instead of zeroing it (6.1, proposed), so that a model with correct claims but a wrong aggregate
   still shows its claim work.
4. **Track B.** Adopted: per-claim eligibility, the raw or processed data boundary, a content audit,
   mediated network access, and independent gold (2.3, 5.2, 7.4). Your contamination caveat is in
   section 1.
5. **Stages and isolation.** Adopted: richer stage contracts, per-stage configuration, a run record,
   isolated state, and a proxy (7.2 to 7.4).

## Argon points

These are recorded with checks in `argon-r1.md`. The following are now in the spec:

- read access and the public repository (7.4);
- the twin cue from local versus remote packages and from the path (2.1);
- the shared R library (7.4);
- archiving the full bundle (7.2, 7.3);
- checking recomputed values against references (6.3);
- reporting twins separately with family clustering (6.2, 6.5);
- scoring each printed number (3.2);
- stale G-08 text (5.1).

Two points were not adopted:

- accepting both labels for G-21, which reopens a settled decision;
- accepting `match` for G-16 from the shipped `.tex` tables, because reading shipped outputs is not
  recomputation.

## Not adopted from Sol

- **Article-length submission budget.** I dropped this. The extra-claim audit with a gate is simpler,
  and a budget would need its own calibration.

## Infrastructure note

Docker, Podman and Colima are not installed on this Mac. The isolation in 7.4 will need either a
container runtime here or runs on another Linux machine. This choice goes to Lukas.
