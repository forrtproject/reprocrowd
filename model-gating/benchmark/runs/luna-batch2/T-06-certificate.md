# ReproCrowd reproduction certificate

**Outcome: computational issues.** The shipped R analysis executed to completion. Four of five requested Wilcoxon Z values match the printed values at their stated precision. Experiment 1a does not: the shipped code computes **Z = −3.023324**, while the paper reports **Z = −1.03**. This report addresses computational reproducibility only; it does not assess the scientific conclusion.

## Procedure and environment

- Reproduction Study, same methodology and tools; prompt version 0.1.2.
- Rule pack: crowd-repro v1.1.0; certificate schema 1.1.
- Engine: Codex · model: GPT-6 · provider: OpenAI.
- Environment: R 4.6.1 on macOS Tahoe 26.7 (aarch64-apple-darwin23). Package versions and `sessionInfo()` are recorded in [sessionInfo.txt](sessionInfo.txt).
- The original package was left in place and not copied or uploaded. The unchanged shipped analysis is included in `code/`; execution was from the package's `Code/` directory so its relative data paths resolve. The only additional command sourced the script and printed its already-created claim result objects and `sessionInfo()`; it performed no analysis.

## Claim results

| Claim | Printed | Recomputed | Status |
|---|---:|---:|---|
| C1 · Experiment 1a probability, 50% | −1.03 | −3.023324 | **Discrepant** |
| C2 · Experiment 2a probability, 60% | −3.65 | −3.647424 | Match |
| C3 · Experiment 2a probability, 40% | −1.77 | −1.774780 | Match |
| C4 · Experiment 2b point prediction, 60% | −0.95 | −0.952358 | Match |
| C5 · Experiment 2b point prediction, 40% | −7.57 | −7.572409 | Match |

Values are from the exact objects created by the shipped script. Its Z calculation is `qnorm(two-sided p / 2)`. C1's difference is too large to be rounding at the printed precision. No missing analysis was written, and no specification, sample, or data was changed.

## FORRT nanopublication chain vocabulary

This is a **Reproduction Study**. The computational outcome is **computational issues**: C2–C5 reproduce; C1 does not reproduce. **Outcome robustness: not checked.**

## Files

- `code/statistical_analysis.R`: shipped analysis script, unchanged.
- `code/run.sh`: execution and result-capture command.
- `logs/statistical_analysis.log`: full console output and recorded values.
- `sessionInfo.txt`: runtime and package session record.
- `certificate.json`: machine-readable certificate.

Original code and data link: local package `/tmp/scratch_bench_luna/packages/T-06` (not redistributed).
