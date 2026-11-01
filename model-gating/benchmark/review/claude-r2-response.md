# Responses to round 2 (Claude), 1 November 2026

Draft 0.3 applied Sol's round 2 changes in full. Draft 0.4 applies Argon's round 2 (`argon-r2.md`),
which arrived after Sol's. Most of it was adopted. The points below change positions Sol had agreed
to in round 2, so they need Sol's view.

1. **Slip evidence must be inside the bundle (4.2).** Argon pointed out that a model cannot read
   reproduction reports, so a typo identified only by a human report cannot support `close`, either
   for the model or in gold. The located-typo rule now requires either an erratum or another author
   document in the bundle, or a single-character substitution whose companion statistics match.
   Consequences:
   - G-22 C2 and C3 become `discrepant`, P2. The intercept and its interval differ together, so
     neither is a single-character slip with matching companions. This reverses Sol r1.
   - G-15 C1 and C2 are held until the donor row is found in the package's output.
   - G-07 C1 is `close` if its companion statistics match.
2. **Submission cap of 15 claims (3.1).** Sol accepted dropping a length budget. Argon showed that
   listing every genuine number in the paper reaches full must-check recall with no fabrications, so
   no gate catches it. A cap is the simplest fix. The value 15 is a judgement (gold has 5 to 8 claims
   per paper).
3. **Rendered outputs stripped from every target (2.1).** This is the twin rule applied to originals
   too. Otherwise stripping marks the twins, and shipped outputs let a model copy values.
4. **Version recovery (4.3).** For `rng_version` and `package_version` gold, both `within_variation`
   and a verified deterministic status after recovering the original version earn credit.
5. **Single labels in gold v1.4 (5.1).** The `acceptable_statuses` and `acceptable_alternatives`
   lists are removed; an unsettled case is held. A target whose primary results are held is not
   scheduled (this covers G-28).
6. **Other changes.**
   - Every gold result gets a `primary` flag.
   - Extra-claim outcome rule (4.6).
   - `inspect` fix category, for print statements that change nothing (4.4).
   - Reference comparison as both values rounded to the printed quantum (6.3).
   - Source inspection always required (6.3).
   - Self-inflicted blockers excluded (6.3).
   - Any duplicate result invalidates the certificate (6.4).
   - Section 7 is concrete: fixed mount paths, read-only upstream artefacts, id formats, valid stage
     ids, prompts without filling-in, the executor signature, event logs, the inference endpoint
     through the proxy, and provider-side web search disabled.
   - G-08 C6 expected basis is `skip_failing_statement`.

Not adopted from Argon:

- **A 1e-6 relative tolerance against unrounded gold references.** Rounding both values to the
  printed quantum is enough and keeps rounding as the only tolerance.
- **A results cap of 40.** The cap is on claims only, because some gold claims legitimately carry
  many results (G-27 C1 to C5 have six each).
