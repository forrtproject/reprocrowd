# Reproduction Study: *Reshaping Global Trade*

**Outcome: computational issues.** The translated R workflow prepared the trade and short-run panels and ran the shipped Table I, II, IV, and V commands. Many reported values recur. Several Table IV and V regression estimates do not recur at the paper’s printed precision. The full shipped pipeline does not complete: the supplied package omits the custom `ssaggregate` command needed for the balance datasets, and the Table IV Poisson command references an uncreated `post_country` variable.

This is a computational reproducibility check only. It does not assess whether the paper’s scientific conclusions are correct. The FORRT chain records `outcome_computational: computational issues` and `outcome_robustness: not checked`.

## Sources and method

- Paper: [Xu (2022), DOI 10.1093/qje/qjac016](https://doi.org/10.1093/qje/qjac016). Printed values were read from the supplied PDF at `/tmp/scratch_bench_luna/articles/pkg-6165a5/article.pdf`.
- Shipped code and data: [Harvard Dataverse replication package](https://doi.org/10.7910/DVN/EIEQIS). The local package supplied for this check was `/tmp/scratch_bench_luna/packages/pkg-6165a5`; the original files were not copied into this bundle.
- Procedure: ReproCrowd benchmark reproduction check 0.1.2; rule pack `crowd-repro v1.1.0`.
- Engine: Codex · GPT-6 · OpenAI. Stata was unavailable, so the Stata commands were translated to R. Environment details are in [sessionInfo.txt](sessionInfo.txt).

## Execution and fixes

The preparation translation executed through the final bilateral and port-level short-run panels. It saved intermediate DTA files only during execution; those data files are not included here. The last preparation blocks could not run because the custom `ssaggregate` implementation is not present in the package. The console record is [translated_pipeline.log](logs/translated_pipeline.log).

Documented translation fixes were limited to equivalent field and temporary-variable names: `expr_ff`→`expr_f`, `event_og`→`event`, country-level `post_london`→`post_lon`, and the `_gdp` suffixes omitted from the structural-gravity temporary-variable references. They preserve the supplied values and intended commands. The R translation of `reghdfe`/Poisson calls uses `fixest`, with the stated absorbed effects, weights, and clustered errors. The Table IV Poisson model itself could not run because `post_country` is not supplied or created.

## What recurred

Table I’s port summaries and most country summaries recur at displayed precision. The country bank-count and non-British-bank descriptive values differ. Table II’s displayed means, standard deviations, group differences, and standard errors recur at printed precision. In the short-run regressions, Table IV columns 1–3 and Table V columns 1–2 recur; Table IV columns 4, 5, and 7 and Table V columns 3–5 differ. The certificate records each scalar separately, including coefficients, standard errors, and table counts. Across the enumerated claims, 277 values match, one is close due to a truncation, 17 are discrepant, and 87 are not checkable. Table III balance results and narrative outcomes that depend on analysis beyond the executed translation remain uncheckable.

A discrepancy means the translated run returned a different value at the paper’s displayed precision. It is reported as an observed computational difference, without attributing it to a scientific error. The missing helper, absent variable, incomplete analysis coverage, and results are itemized in [certificate.json](certificate.json).

## Re-run

From this directory, run `Rscript code/translated_pipeline.R` to reproduce the preparation attempt and its stopping point. Run `Rscript code/translated_tables_I_II.R` and `Rscript code/translated_tables_IV_V.R` for the translated tables that were executed. The output tables in the article were not generated as files because this bundle records console results only.
