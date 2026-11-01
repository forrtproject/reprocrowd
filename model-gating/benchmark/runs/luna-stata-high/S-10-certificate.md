# ReproCrowd reproduction check

**Paper:** Nicola Bianchi and Michela Giorcelli, “The Dynamics and Spillovers of Management Interventions: Evidence from the Training within Industry Program,” *Journal of Political Economy* 130 (2022), DOI [10.1086/719277](https://doi.org/10.1086/719277).

**Outcome:** **Computational issues.** The selected translated analyses executed, and most checked numerical claims recur at the article’s printed precision. The Figure 3 period-8 sales effect does not: the translated coefficient implies 21.8%, compared with 21.7% in the paper. This is a partial benchmark; it does not establish paper-wide reproducibility.

## Scope and method

Stata is not installed. I translated the relevant shipped commands from Figure 2, Figure 3, Figure A3A, Table A4, and Table 1 panel A into R. The translation reads the package’s supplied `.dta` files directly. `haven` reads the data, `fixest` implements the `reg`/`reghdfe` specifications with their listed fixed effects and clustering, and `survival` computes the Kaplan–Meier estimate used by `sts`. For Figure 3 percentage effects I applied `100 * (exp(coefficient) - 1)` to the log outcome estimates. These are direct translations; the model specifications and samples were not changed.

The translated runs reproduced the following prose values: 11,575 applicant firms; 7% trained in all three modules; 48% untrained; 64% survival among nontrained firms; a 26 percentage point lower exit rate; 5.3% sales growth in the first post-training year; 16% sales growth in year 10; 6% and 27% productivity growth in periods 0 and 10; and 11% ROA growth in year 10. The trained-firm survival estimate was 90.9%, consistent with the paper’s coarse 90% statement at the one-percentage-point precision allowed by the rule pack.

The period-8 sales coefficient is 0.19702003. Its percentage transform is 21.8051%, which rounds to 21.8% at one decimal; the article reports 21.7%. I record this as discrepant because the deterministic translation does not identify a rounding slip that explains the printed value.

## Coverage limitation

This certification bundle is incomplete against the requested all-claims scope. It checks the listed abstract/main-text values and executes Table 1 panel A calculations, but does not enumerate/check every numeric result in the article and does not translate or run all 43 scripts listed in the master file. The package contains prepared analysis datasets but no upstream raw-data construction scripts. Accordingly, this report does not claim complete reproduction of the paper. The comparison that 1939 applicant firms employed 40% of the US manufacturing workforce is not checkable from the supplied files because the US workforce denominator is absent.

## Environment and provenance

- **Engine:** Codex; **model/provider:** GPT-6 / OpenAI
- **Rules:** ReproCrowd `crowd-repro` v1.1.0, [rule pack](https://forrtproject.github.io/reprocrowd/crowd-repro/RULEPACK-v1.1.0.md)
- **Schema:** [certificate schema v1.1](https://forrtproject.github.io/reprocrowd/schemas/certificate.schema.json)
- **Date:** 2026-11-01
- **Environment:** macOS Tahoe 26.7, arm64; R 4.6.1; `haven` 2.5.5, `fixest` 0.14.2, `survival` 3.8.6. See [sessionInfo.txt](sessionInfo.txt).
- **Code and logs:** [R translation](code/run_translation.R), [certificate builder](code/build_certificate.py), and captured run output in `logs/`.
- **Source package:** `/tmp/scratch_bench_luna/packages/pkg-775f66` (used in place; no original code or data copied into this bundle).

The FORRT chain outcome is `computational issues`; robustness is `not checked`. No scientific conclusion is assessed.
