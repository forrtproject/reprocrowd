# Luna on ten Stata papers (diagnostic test, 1 November 2026)

**Setup.** The ten papers come from `../gold-set/stata/draw-stata.json`: 5 computationally
reproducible and 5 with computational issues, drawn with seed 20261101. Two draws were replaced
from the seeded reserves (see the draw file).

- **Packages:** each was built locally by `build_stata_packages.py`, with rendered outputs
  stripped, and given the published article PDF.
- **Model:** GPT-6 Luna through the Codex CLI on the ChatGPT subscription.
- **Prompt:** the pilot prompt (rule pack 1.1.0, not yet the 0.6 specification), with no claim
  list. The model was told to extract every reported number and to translate the whole Stata
  pipeline into R.
- **Gold:** none yet for these papers. The comparison below is with the human report's findings
  as recorded in the screening notes.
- **Isolation:** none (diagnostic run).

| | Expected (human report) | Medium effort | High effort | High: results (match / discrepant / not checkable) | High: minutes |
|---|---|---|---|---|---|
| S-01 RB-007 | reproducible | issues | issues | 14 / 37 / 37 | 4 |
| S-02 RB-013 | reproducible | issues | issues | 18 / 4 / 4 | 3 |
| S-03 RB-045 | reproducible | technical failure, nothing run | issues | 428 / 135 / 0 | 28 |
| S-04 RB-020 | reproducible | issues | **reproducible** | 36 / 0 / 0 | 15 |
| S-05 RB-105 | reproducible | technical failure, nothing run | issues | 484 / 1 / 231 | 7 |
| S-06 I4R-243 | issues | technical failure, nothing run | technical failure, nothing run | 0 / 0 / 23 | 2 |
| S-07 I4R-85 | issues | issues | **issues, human finding recovered** | 277 / 17 / 87 (+1 close) | 9 |
| S-08 RB-060 | issues | technical failure, nothing run | issues | 3 / 0 / 0 | 2 |
| S-09 RB-064 | issues | issues | **issues, human finding recovered** | 381 / 20 / 7 (+4 close) | 10 |
| S-10 RB-075 | issues | not checked, nothing run | issues | 10 / 1 / 1 (+1 close) | 4 |

Runs are in `runs/luna-stata/` (medium) and `runs/luna-stata-high/` (high). A first four-paper
attempt without article PDFs is in `runs/luna-stata-attempt1/`.

## What the test shows

1. **At medium effort Luna mostly declines the work.** Five of ten runs ended within 4 minutes with
   no computation. They said so honestly, despite the explicit instruction to translate the whole
   pipeline.
2. **At high effort it does the work, and finds the human reports' discrepancies exactly.**
   - S-07: the Table IV/V coefficients -0.631 and -0.505 against the printed -0.656 and -0.554,
     with matching standard errors.
   - S-09: the Survey 2 religiousness mean 3.848456 against the printed 3.9.

   It extracted hundreds of numbers per paper (563 on S-03, 716 on S-05).
3. **False alarms remain the main weakness, on 4 of 5 reproducible papers.**
   - **Old rule pack:** the prompt still carries rule pack 1.1.0. S-01 marks 1.2058 against a
     printed 1.2 as discrepant, citing the old tolerance text; under the 0.6 rule that is a
     `match`.
   - **Last-digit differences in iterative estimators:** S-03 has Tobit and structural estimates
     off by one unit in the third decimal (0.35858 against 0.358). This is the usual drift between
     Stata's and R's optimisers.
   - **Possible translation errors:** S-02 retains 2,533 respondents against 2,537 printed.
4. **Packages and articles matter.**
   - Without the article PDF, publisher paywalls stopped two runs in the first attempt.
   - One paper (SC-a2Yx) had to be replaced because its article could not be obtained.
   - S-06 stops because the raw files for its cleaning script are not deposited, although an
     analysis dataset is. The run should start from that dataset, as the human report did.

## Open question this raises

Translated iterative estimators (Tobit, logit, structural models) often differ from Stata in the last
printed digit. They are not covered by the 0.6 rules. Strictly, they are `discrepant` and
`unexplained`, which would flood reproducible Stata papers with false discrepancies. One option is
to treat the optimiser difference between Stata and R as a variation source (`optimiser`, section
4.3): the result is `within_variation` if the R estimate converges tightly and its range across
start values or optimisers covers the printed value. This needs a decision before Stata gold is
labelled.
