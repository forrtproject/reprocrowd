---
title: "ReproCrowd certificate RC-2026-923: Tomai et al. (2023)"
---

# ReproCrowd certificate RC-2026-923

**Engine:** Claude Code (Claude Agent SDK) · Claude Opus 5.5 (`claude-opus-5-5`) via Anthropic · **rules:** crowd-repro v1.0.0 · **procedure:** ReproCrowd prompt 0.1.0 · **audit date:** 2026-10-30 · **host:** macOS 26.7 (Darwin 25.6.0, arm64) · **environment:** pixi 0.83.0, R 4.4.3, Python 3.12.16, Snakemake 9.27.1 (full inventory in `environment.json`, lockfile `pixi.lock`)

**Paper:** Tomai, E., Kokla, M., Charcharos, C., & Kavouras, M. (2023). Does spatial thinking ability relate to performance when using web-mapping services? A survey with digital natives. *AGILE: GIScience Series, 4*, 13. <https://doi.org/10.5194/agile-giss-4-13-2023>

**Code and data (linked, not redistributed):** figshare <https://doi.org/10.6084/m9.figshare.22132940.v1>. The paper cites v2; the figshare API shows v1 and v2 hold byte-identical files (same MD5 for all four files).

This certificate covers computational reproducibility only. It does not assess whether the conclusions are correct; robustness was not checked.

## Outcome

**`technical failure`**: the shipped script cannot be executed as shipped.

- Run byte-for-byte with `Rscript`, it stops at line 22 (`View()` needs a display: "X11 is not available").
- With the two `View()` calls commented out (a lossless edit), 86 of 418 top-level expressions still fail, from line 771 onwards. The Group 2 (Google Maps vs HERE WeGo) code is omitted ("hence code is omitted"), but later shipped code uses its objects. The README says the script reproduces the analysis "only partially".

The computation that is present reproduces almost entirely:

| Route | Numbers checked | Match | Discrepant |
|---|---|---|---|
| Shipped code (View() commented out) | 90 | 89 | 1 (Table 8 BM–HWG W) |
| Reviewer-completed Group 2 block | 70 | 70 | 0 |
| Figure 7 image (no code) | 1 | | not checkable |
| **Total** | **161** | **159** | **1** |

Figures 1–6 regenerate from the shipped code. They look plausible but were not compared pixel by pixel with the published figures. Figure 7 has no code.

## Decisions to review

1. **Outcome label.** I chose `technical failure` because the rule pack defines it as "could not be executed as shipped (missing code/data, fatal error)", and both conditions apply. `computational issues` would also be defensible, since 89 of 90 numbers that the shipped code produces recur.
2. **Group 2 completion.** To check the 70 numbers that the shipped code cannot reach, I wrote a Group 2 block (`scripts/group2_completion.R`) that mirrors the Group 1 code line by line. It is inserted where the authors write that the code is omitted. It is not part of the shipped code, and those numbers are reported separately.
3. **Missing cells in `GM_HWG.csv`.** Five task-success cells are empty. In the primary completion they are set to 0, which is the rule the shipped code applies to `STAT.csv` (line 127). It is also the only rule consistent with the Fig. 7 means, which need N = 37 denominators. With the cells kept as NA, many Group 2 values are discrepant (e.g. Fig. 7 HWG mean 2.18 vs 2.11; Table 4 GM–HWG V 198 vs 281; Table 9 HWG rows). The NA-kept value for every affected number is in the `note` field of `certificate.json`.
4. **Second pass for ordering.** The step-wise runner retries failed expressions once after the full script. This resolves one ordering defect in the shipped code (line 776 uses objects defined at line 1075).

## Claims (treated as approved)

| ID | Claim | Exhibit | p. | Route | Result |
|---|---|---|---|---|---|
| C1 | N = 74, 40 male | §3.2 | 3 | shipped | match |
| C2 | DNAS α = .802, M = 105.51 ± 13.98 | §4.2 | 6 | shipped | match |
| C3 | STAT α = .549, M = 10.62 ± 2.45 | §4.3 | 6 | shipped | match |
| C4 | Group 1 means BM 3.19, GM 2.54 | Fig. 6 | 6 | shipped | match |
| C5 | Group 2 means GM 2.54, HWG 2.11 | Fig. 7 | 7 | completed | match (figure image: not checkable) |
| C6 | GM vs BM success, McNemar (5 tasks) | Table 1 | 7 | shipped | 20/20 match |
| C7 | GM vs HWG success, McNemar (5 tasks) | Table 2 | 7 | completed | 20/20 match |
| C8 | BM vs HWG Fisher tests | Table 3 | 7 | shipped | 10/10 match |
| C9 | All-task score tests | Table 4 | 7 | GM–BM shipped; GM–HWG, BM–HWG completed | 12/12 match |
| C10 | BM vs HWG successful times, Tasks 4, 5 | Table 5 | 7 | completed (BM values shipped) | 16/16 match |
| C11 | SUS descriptives | Table 6 | 8 | shipped | 12/12 match |
| C12 | SUS α | Table 7 | 8 | shipped | 4/4 match |
| C13 | SUS differences | Table 8 | 8 | shipped | 11/12 match; **BM–HWG W = 1137.5 vs reported 1037.5** |
| C14 | Fligner χ² = 3.15, df = 4, p = .533; W = 644.5, p = .668 | §4.5 | 8 | Fligner completed; W shipped | 5/5 match |
| C15 | Kendall correlations, GM (N = 74) and BM rows | Table 9 | 8 | BM shipped; GM completed | 24/24 match |
| C16 | Kendall correlations, HWG rows | Table 9 | 8 | completed (BM code mirrored) | 12/12 match |
| C17 | 7% moderately familiar with Boston | §4.2 | 5 | completed (no shipped code; computed as share of rating 3 across both task files) | match |

"Match" means equal at the precision reported in the paper (p < .001 counts as a match when the recomputed p is below .001). Every number is listed in `outputs/results.csv` and `certificate.json`.

## Findings

| ID | Sev. | Finding | Suggested fix |
|---|---|---|---|
| RC-001 | P0 | Group 2 code omitted; shipped code fails from line 771 (86 of 418 expressions). Fig. 7, Table 2, parts of Tables 4, 5 and 9, and the §4.5 Fligner test cannot be produced as shipped. | Ship the full Group 2 block. |
| RC-002 | P1 | Table 8 BM–HWG SUS: the shipped code gives W = 1137.5, but the paper reports 1037.5. The p-value and CI [12.5, 30.0] from the same test match. The pattern fits a transcription error; this was not adjudicated. | Authors to confirm W. |
| RC-003 | P2 | Undocumented handling of five empty cells in `GM_HWG.csv`. Group 2 values reproduce only if the cells are set to 0. | Document and code the rule. |
| RC-004 | P2 | Ordering defect: line 776 uses `SUS_ScoresGroup1/2`, which are defined at lines 1075–1086. | Move the §4.5 block after the SUS block. |
| RC-005 | P2 | `View()` calls (lines 22, 126) are fatal under non-interactive `Rscript`. | Guard with `if (interactive())`. |
| RC-006 | P3 | `SUS_GMCorrelation` is overwritten at line 1511 by a STAT test. The Table 9 SUS–GM value was recomputed using the definition at line 1402. | Remove the duplicate block. |
| RC-007 | P3 | Table 3 hard-codes the HWG success counts (19, 24, 11, 14, 10). These agree with the data once empty cells are 0. Other issues: files are joined by row position rather than ID, the header typo `Partiicipant_ID`, and the paper cites figshare v2 while the link given is v1 (the files are identical). | Compute counts from the data; merge on ID. |

## Edits to shipped code

- **Lossless:** two `View()` calls commented out (`working/EDITS.json`). No number changes.
- **Not lossless, kept separate:** the reviewer-written Group 2 block, inserted after line 765 (`completed` variant). An NA-kept alternative (`completed_nakept`) is also run.
- The data files were used byte-for-byte (MD5s in `data/original/MANIFEST.json`).

## Environment and version drift

R 4.4.3 (conda-forge, via pixi) was used; the host's R 4.6.1 was not. Compared with the versions the paper cites: DescTools 0.99.45 → 0.99.59, gdata 2.18.0.1 → 3.0.1, psych 2.2.9 → 2.6.9; the paper gives no R version (2022 release). conda-forge has no `r-ltm` build, so ltm 1.2-0 is installed from CRAN source into `.rlib/`. The near-complete agreement suggests the drift did not affect these results.

## Process notes

- The prompt's rule-pack and schema URLs (`https://lukasroeseler.github.io/reprocrowd/...`) returned HTTP 404 on 2026-10-30. Following the coordinator's pilot note, I used the copies at `https://forrtproject.github.io/reprocrowd/` (rule pack v1.0.0, certificate and FLoRA schemas, copied into `schemas/`).
- `certificate.json` and `flora-entry.json` are generated by `scripts/build_certificate.py` and validated against those schemas, using `jsonschema` 4.26.0 with format checking.
- No existing reproduction or review report was consulted. The paper links an AGILE reproducibility review, which I did not open.
- No nanopublications were published (see `nanopubs/PUBLISHED.md`). The bundle has not been pushed to `github_url`.

## Re-run

```
pixi run snakemake --cores 1
```

This downloads the figshare files and checks their MD5s, builds the four working variants, runs all analyses, collects the figures, and regenerates `environment.json`, `certificate.json` and `flora-entry.json`. A clean run from an empty state completed in this pilot (7 of 7 steps).
