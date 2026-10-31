# ReproCrowd computational reproduction check

**Outcome:** computationally reproducible, with justified fixes. The eight selected headline estimates recur at the printed precision, with one minor truncation difference for victim compensation. This is a computational check only; it does not assess whether the scientific conclusions are correct.

**Paper:** Laia Balcells, Valeria Palanza, and Elsa Voytas, “Do Transitional Justice Museums Persuade Visitors? Evidence from a Field Experiment,” *The Journal of Politics* 84(1), 496–510 (2022), [DOI](https://doi.org/10.1086/714765).

**Original code and data:** [pinned Repro-Bench snapshot](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/19/replication_package). Original code and data are linked, not included in this certificate.

## Procedure and environment

- **Procedure:** ReproCrowd `crowd-repro` v1.1.0; prompt/procedure version 0.1.2.
- **Engine:** Codex · rules: 1.1.0.
- **Model/provider:** GPT-6.1 Luna · OpenAI.
- **Date:** 2026-10-31.
- **Environment:** R 4.6.1 on macOS Tahoe 26.7 (aarch64-apple-darwin23). The complete session record and loaded package inventory are in [sessionInfo.txt](sessionInfo.txt). Packages: sandwich 3.1-3, plyr 1.8.9, lmtest 0.9-40, dplyr 1.2.1, gridExtra 2.3.1, RColorBrewer 1.1-3, ggplot2 4.0.3, zoo 1.9-1, plus their recorded dependencies.

## What was run

The authors’ main-text and appendix R scripts and data were fetched from the pinned snapshot into a temporary working copy; the originals were left untouched. At first, both scripts failed because the packages named in their `require()` calls were not installed. Installing those packages allowed the appendix script to finish.

The main-text script then stopped at a Figure 2 plotting-label loop: it attempted to assign the “pardoned” label through row 34 although that table has 24 rows. The range was corrected from 22:34 to 22:24 in the working copy. This affects only plot labels. The models, observations, data, and estimates were unchanged. The full script then exited successfully. An output-only wrapper printed existing estimate objects from the authors’ script; it calculated no additional estimates. See [patch.diff](code/patch.diff), [run_maintext.R](code/run_maintext.R), and the complete console logs in [logs/](logs/).

## Claim results

| Claim | Reported | Recomputed from shipped analysis | Status |
|---|---:|---:|---|
| Current-government satisfaction, coefficient; p | 0.15; 0.04 | 0.1521649; 0.03496835 | Match |
| Democracy satisfaction, coefficient; p | 0.14; 0.03 | 0.1364780; 0.03177851 | Match |
| Church trust, coefficient; p | 0.18; 0.01 | 0.1808914; 0.01126659 | Match |
| Support for military government | −11% | −0.1136308 (−11.36%) | Match |
| “Dwelling on the past prevents progress,” coefficient; p | −0.32; 0.03 | −0.3190497; 0.03208726 | Match |
| Victim compensation, coefficient; p | 0.19; 0.00 | 0.1980145; 0.009119984 | Close |
| Public apology from military, coefficient; p | 0.18; 0.09 | 0.1817317; 0.08799839 | Match |
| Pardon perpetrators, coefficient; p | 0.22; 0.02 | 0.2167946; 0.02026355 | Match |

The victim-compensation values appear truncated to two decimals in the paper. Truncation gives 0.19 and 0.00; conventional rounding would give 0.20 and 0.01. This is recorded as `close` under the rule pack’s reporting-slip definition.

## FORRT nanopublication chain

- **Claim:** the eight quantified main-results statements listed above.
- **Evidence:** authors’ supplied R scripts, supplied data, generated figures/results, and run logs.
- **Method:** same authors’ R methodology and tools; packages installed; one plot-label index corrected; output-only extraction wrapper used.
- **Outcome (computational):** computationally reproducible.
- **Outcome (robustness):** not checked.
- **Limitations:** this claim list focuses on the quantified main-results claims and does not test robustness or scientific correctness.

**Source-text note:** claim wording and printed values were read from the publicly accessible September 1, 2020 author manuscript associated with this DOI; claim page numbers refer to that version. The publisher full text was not accessible during this check. The paper identity and DOI were confirmed through Crossref/journal metadata.

Python 3.14.6 was used only for downloading/organizing files and validating the certificate schema; the full pip environment record is in [python-freeze.txt](python-freeze.txt). No Python analysis was run.
