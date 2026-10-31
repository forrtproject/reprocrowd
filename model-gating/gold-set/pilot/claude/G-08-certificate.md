# ReproCrowd certificate RC-2026-908

Engine: Claude Code (Claude Agent SDK) · Claude Opus 5.5 (`claude-opus-5-5`) via Anthropic · rules: crowd-repro v1.0.0 · prompt 0.1.0 · audit date 2026-10-30

**Paper:** Balcells, L., Palanza, V., & Voytas, E. (2022). Do transitional justice museums persuade visitors? Evidence from a field experiment. *The Journal of Politics, 84*(1), 496–510. <https://doi.org/10.1086/714765> (metadata checked against Crossref)

**Code and data (linked, not redistributed):** [REPRO-Bench mirror, revision 74958fb, folder 19/replication_package](https://huggingface.co/datasets/chuxuan/REPRO-Bench/tree/74958fba32daeacff51f2e1fd37be3916595648f/19/replication_package). The package has five files: two R scripts, two `.Rdata` files and a codebook. `notebooks/01_data_download.py` downloads them and checks their SHA-256 hashes.

## Outcome: computational issues

- **As shipped, the main-text script does not run to completion.** It stops at Figure 2 with `replacement has 25 rows, data has 24` (finding RUN-001, P0). A one-line lossless edit fixes it. After the edit, the script regenerates Figures 1–4, and the appendix script runs unmodified to exit 0.
- **Of 30 checked values covering 17 claims, 23 match, 4 differ only in the last reported digit and 3 are discrepant.** The discrepant values are the in-text one-week durability statistic for pardoning (C14, two values) and one percentage (C13).

This certificate covers computational reproducibility only. It does not judge whether the paper's conclusions are correct. Robustness was not checked.

## Environment

| Item | Version |
|---|---|
| Host | macOS 26.7 (Darwin 25.6.0, arm64) |
| R (certified run) | 4.5.3, from `pixi.lock` (host R 4.6.1 not used) |
| R packages | sandwich 3.1-3, lmtest 0.9-40, zoo 1.9-0, plyr 1.8.9, dplyr 1.2.1, gridExtra 2.3.1, RColorBrewer 1.1-3, ggplot2 4.0.3, jsonlite 2.0.0 |
| Python | 3.12.16 (snakemake-minimal 9.27.1, jsonschema 4.26.0) |
| pixi | 0.83.0 (installed inside the pilot folder) |
| Lockfile | `pixi.lock` (osx-arm64 and linux-64 solved; only osx-arm64 executed) |

The full inventory is in `environment.json`. A first run leaked packages from the host user library (ggplot2 4.0.2, dplyr 1.2.0, sandwich 3.1-1) and produced identical estimates. `pixi.toml` now isolates R through `[activation.env]`.

## Procedure

1. `01_data_download.py` downloads the pinned files into `extracted/`, which is never edited.
2. `02_data_clean.py` copies them to `working/` and applies one lossless edit. In `BPV_museums_maintext.R` line 224, `for (i in 22:34){results.df.tj$Variable[i] <- "pardoned"}` becomes `for (i in 22:24){...}`. Rows 22–24 get the same label as before. No estimate, standard error or p-value changes. The data needed no cleaning because the scripts do all recoding themselves.
3. `03_analysis.py` runs three things:
   - the shipped script unchanged, to record the failure in `results/maintext_unedited.log`;
   - the edited main-text script through `scripts/run_maintext.R`, which sources it and exports the computed objects;
   - the appendix script through `scripts/run_appendix.R`.

   It then compares each claim with the recomputed value. A value **matches** if it rounds to the reported value at the reported precision, and is **close** if it differs only in the last reported digit.
4. `04_figures.py` collects Figures 1, 2, 3A, 3B and 4 into `figures/`. The shipped script draws Figure 4 with base graphics and never saves it, so the wrapper opens a PDF device to capture it.
5. `scripts/build_certificate.py` writes the JSON reports and validates them against the ReproCrowd schemas. Both are valid; see `results/schema_validation.txt`.

`pixi run snakemake --cores 1` re-runs the whole workflow from an empty folder. I ran it from a clean state and it exited 0.

## Claims and results

| Claim | Quantity | Reported | Recomputed | Status |
|---|---|---|---|---|
| C1 | Govt satisfaction b / p | 0.15 / .04 | 0.152 / .0350 | match / close |
| C2 | Democracy satisfaction b / p | 0.14 / .03 | 0.136 / .0318 | match / match |
| C3 | Democracy, left b / p | 0.16 / .10 | 0.161 / .0965 | match / match |
| C4 | Church trust b / p | 0.18 / .01 | 0.181 / .0113 | match / match |
| C5 | Military govt (0–1), all | −0.11 | −0.114 | match |
| C6 | Military govt (0–1), right | −0.17 | −0.170 | match |
| C7 | Right–left gap, military govt, pre → post | 0.43 → 0.34 | 0.436 → 0.343 | close / match |
| C8 | Right–left gap, democracy, pre → post | 0.26 → 0.12 | 0.256 → 0.121 | match / match |
| C9 | Dwelling on past b / p | −0.32 / .03 | −0.319 / .0321 | match / match |
| C10 | Victim compensation b / p | 0.19 / .00 | 0.198 / .0091 | close / close |
| C11 | Public apology b / p | 0.18 / .09 | 0.182 / .0880 | match / match |
| C12 | Pardon b / p | 0.22 / .02 | 0.217 / .0203 | match / match |
| C13 | Museum info new: n / % | 18 / 13.14% | 18 / 13.33% | match / discrepant |
| C14 | Pardon, one-week follow-up b / p | 0.20 / .16 | 0.308 / .0041 | discrepant / discrepant |
| C15 | Control n; treated compliers n | 126; 138 | 126; 138 | match / match |
| C16 | Final-round n | 131 | 131 | match |
| C17 | Figures 1–4 regenerated | published | 5 PDFs | match (visual) |

C7 and C8 rest on my reading of how the gap was computed: the difference between right and left means among treated participants, before and after the visit. The paper does not state the computation. For C17, I compared the regenerated PDFs with the published pages 505–507 by eye. The plotted values are the tool-checked estimates in `results/estimates.csv`.

## Findings

- **RUN-001 (P0, defect).** As shipped, the main-text script stops at Figure 2 because the label loop `22:34` writes past a 24-row data frame. Figures 2–4 are not produced. Fix: change the bound to `22:24`. This edit was applied in `working/` and changes no numbers.
- **RES-001 (P2, defect).** For C14, the text gives b = 0.20, p = .16 for the one-week follow-up. The recomputed one-week (wave 1) estimate is b = 0.308, p = .004 (n = 222). The reported numbers equal the 24-week (wave 3) estimate instead: b = 0.205, p = .164 (n = 129). Published Figure 4B also shows a week-1 point near 0.31 and a week-24 point near 0.20. The code therefore reproduces the figure, and the wave named in the text does not match it. I rated this P2 because it is a secondary (durability) result and the figure reproduces.
- **RES-002 (P2, defect).** For C13, n = 18 recurs but 13.14% does not: 18/135 non-missing treated answers is 13.33%, and 18/138 treated is 13.04%. 13.14% equals 18/137. Several other post-visit items have 137 non-missing answers among treated participants (for example `justice_advance`), so the authors may have used one of those denominators. I could not confirm this.
- **RES-003 (P3, normalisation).** The code divides the whole `coeftest` row by `itt.d` (0.965), including the p-value, so every reported p equals the heteroscedasticity-consistent p divided by 0.965. With this division, C3 (.096) and C11 (.088) match the text. Without it they would read .09 and .08. I record this as computed and do not judge the method.
- **RES-004 (P3, normalisation).** Two-decimal reporting is not uniform. C10 and C7 match truncation rather than rounding. C1's p of .0350 is reported as .04, which neither rounding nor truncation gives.
- **DOC-001 (P3, defect).** The package has no README, no software versions and no run instructions. Figure 4 is never saved. The Figure 1 label loop `13:25` overruns, which is harmless because later loops overwrite the labels.

## Limitations and pilot notes

- **Broken URLs.** The URLs in the prompt (`https://lukasroeseler.github.io/reprocrowd/...`) return 404, including the site root. I fetched the rule pack and schemas from `https://forrtproject.github.io/reprocrowd/...`, which redirects to `https://forrt.org/reprocrowd/...`. The rule pack's own `URI` header and the schemas' `$id` still point to the dead domain.
- **Bundle not published.** `github_url` points to the ReproCrowd project repository, not to a repository holding this bundle. No nanopublications were minted (see `nanopubs/PUBLISHED.md`).
- **Appendix not compared.** The appendix script ran to exit 0, but I did not compare its tables (A1–A22) with the online appendix.
- **No verification tools.** The rule pack's `verify_quote`, `resolve_doi` and `wikidata_lookup` tools were not available. I took the claim text from the paper PDF using `pdftotext` and checked it by reading. The DOI was checked against Crossref.
- **One platform.** Only osx-arm64 was executed.
- **Not redistributed.** The original code and data are not included in the bundle; `.gitignore` excludes `extracted/` and `working/`.
