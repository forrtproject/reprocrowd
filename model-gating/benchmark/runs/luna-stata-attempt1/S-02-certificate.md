# ReproCrowd computation check

**Outcome: technical failure for the complete reproduction.** A limited translated check of the Figure 2 cumulative sharing calculations reproduced all three reported maxima exactly. The full shipped analysis was not run, so the abstract’s approximately 45% estimate and other article results remain unchecked. This report concerns computation only and makes no assessment of the scientific conclusion.

Engine: Codex · model: GPT-6 (OpenAI) · rules: crowd-repro v1.1.0 · audit date: 2026-11-01.

## What was checked

The package README identifies 749, 612, and 52 as the maxima for Alt-Facts shares, Alt-Facts shares through the 72-hour cutoff, and fact-check shares. A direct R translation of the corresponding Stata calculations returned 749, 612, and 52. See [the executed translation](code/figure2_translation.R) and [its console log](logs/figure2_translation.log). These three results are `match`, basis `translated`.

The paper abstract reports an approximately 45% reduction. Its underlying Table 2 estimates could not be recomputed; this result is `not_checkable`. The package README also maps participant counts (2,537; 302; 82; 21) to the data-cleaning and generated analysis dataset. Those counts were not recomputed.

## Scope and environment

The supplied package contains 2,610 lines across three Stata do-files and specifies Stata 16.1. Stata is unavailable in this environment. Only the figure/text calculation using `share_facebook.dta` was translated; the full import, merge, cleaning, regression, LASSO, table, and figure pipeline was not translated. Consequently, the requested exhaustive extraction of every numeric result in the article and complete claim-by-claim check has not been achieved. The publisher PDF endpoint returned HTTP 403, and the package’s online appendix is not a substitute for the article’s full text.

The translated calculation used R 4.6.1 and haven 2.5.5 on macOS Tahoe 26.7 (arm64). [sessionInfo](sessionInfo.txt) records the R environment. Original package data and code were not copied into this deliverable. Public links: [article](https://doi.org/10.1257/pol.20210037) and [data/code DOI](https://doi.org/10.3886/E140161V1).

FORRT chain vocabulary: `outcome_computational = technical failure`; `outcome_robustness = not checked`. The full machine-readable record is [certificate.json](certificate.json).
