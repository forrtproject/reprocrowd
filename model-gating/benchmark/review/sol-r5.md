# Specification confirmation, Sol, round 5

Draft 0.6, commit `b68783d`. All line references below are to `model-gating/benchmark/SPEC.md`.

1. **Extraction unit and frozen denominator: RESOLVED.** Scope, occurrence counting, canonical locators, freezing, retained recall eligibility, and versioned rescoring are explicit (lines 97–127, 513–514). The double omission penalty is explained (lines 436–439).
2. **Mutually exclusive misreading and hallucination: NOT RESOLVED.** Source identification, shared normalisation, the local neighbourhood, and compound errors are implemented (lines 162–166, 495–507). However, hallucination still includes reporting “a value the article does not contain” (line 510). If `.17` is transcribed as `.71`, with an unambiguous source and correct referent, and `.71` appears nowhere in the article, it satisfies both definitions. Delete that final disjunct or qualify it to exclude evidenced misreadings. Explicit precedence would also resolve the overlap. The one-instance gate remains unchanged.
3. **Complete numerical predicate for `close`: RESOLVED.** Match precedence, endpoint quanta, percentage conversion, p values, exact counts, vetoes, and explanation evidence are specified (lines 208–232, 478–483).
4. **Whole-policy sandbox acceptance: RESOLVED.** Default denial, inherited process isolation, fresh state, proxy controls, acceptance tests, and diagnostic-only use until acceptance are explicit (lines 625–656). This confirms the specification, not an implementation test.

I accept all four choices: (1) source-first classification with the stated neighbourhood and transcription extensions, subject to fixing the overlap above; (2) inclusion of footnotes, table notes, and captions, the explicit exclusions, and numbered verbal bounds (lines 97–106); (3) primary-result severity under rule pack section 9 (lines 239–241); and (4) canonical and per-result locators and referents, `deviation_evidence`, the paper-outcome reconciliation, and the sandbox additions (lines 117–120, 230–231, 339–355, 568–570, 631–638).

No other new contradiction found. The remaining blocker is the unresolved round 4 classification overlap.

VERDICT: AGREE subject to the blocking changes listed
