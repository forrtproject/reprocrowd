# Reproduction Study: Checking and Sharing Alt-Facts

**Outcome:** computational issues. This is a partial benchmark check, not a complete certification: the shipped Stata pipeline was not translated and run in full. The executed R translation reproduces several central sharing counts and the rounded unadjusted Table 2 Panel A means, but finds a four-observation sample gap and a voluntary intention mean of 10.9% rather than 10.8%.

**Engine:** Codex · **model:** GPT-6.1 Luna · **provider:** OpenAI · **rules:** ReproCrowd crowd-repro v1.1.0 · **procedure:** 0.1.2 · **audit date:** 2026-11-01.

## Execution

The source package specifies Stata/MP 16.1 and contains a master script and three do-files totaling 2,610 lines. Stata was not installed, so I wrote and executed a direct R translation of the three survey imports, source filters, hourly Google Analytics merge and adjustment, then the unadjusted OLS specifications for Table 2 Panel A. The code is [translated_core.R](code/translated_core.R); run output is [core_run.txt](logs/core_run.txt). The R environment is recorded in [sessionInfo.txt](logs/sessionInfo.txt).

No original files were copied into this bundle or uploaded. The executed code reads directly from the supplied package directory.

## Recomputed values

The translation retained 2,533 participants (844, 845 and 844 across the three arms), compared with the article's 2,537. It counts 302 sharing-intention responses and sums the GA action probabilities to 82, matching the text. The resulting overall rates, using 2,533 as denominator, round to 11.9% and 3.2%.

Unadjusted treatment means for sharing intention were 14.7%, 10.2% and 10.9%; the article reports 14.7%, 10.2% and 10.8%. Sharing-action means were 4.6%, 2.6% and 2.5%, matching at the reported precision. Imposed and voluntary action reductions from these translated means are 43.7% and 46.2%, compared with the reported 43%–45% range. The rate of reconfirmed sharing and the fact-check sharing outcomes were not computed.

## Coverage and interpretation

The remaining data preparation and analysis were not translated or executed: the follow-up survey, other tables and figures, adaptive LASSO predictions, appendix analyses, and the final numbers-in-text do-file. Therefore, this run does not meet the prompt's requirement to check every data-derived number in the abstract, main text and tables. Results not reached are not evidence of reproduction or non-reproduction. The certificate records only the limited values actually computed, marks the overall result **computational issues**, and leaves robustness **not checked** in the FORRT nanopublication chain vocabulary.

### Files

- `certificate.json` — machine-readable record using schema version 1.1.
- `code/translated_core.R` — executed R translation.
- `logs/core_run.txt` — console output for the reported computations.
- `logs/sessionInfo.txt` — R version, platform and session record.
