# Specification review, Gemini 4 Argon (High), round 3

Run through the Antigravity CLI (`agy -p`, read-only sandbox) on 1 November 2026 against SPEC.md draft 0.4. Text as returned; local file links shortened to repository-relative paths.

### 1. Status of round 2 blocking points in draft 0.4

All blocking points in [argon-r2.md](model-gating/benchmark/review/argon-r2.md) are resolved in [SPEC.md](model-gating/benchmark/SPEC.md):

- **1.1 Stage contracts (workspace layout, S2/S3 inputs, result keys and interval typing):** **RESOLVED** ([SPEC.md](model-gating/benchmark/SPEC.md#L463-L485)).
- **1.2 Pipeline manifest (valid stage IDs, workspace handoff, decomposed mounts, non-interpolated prompts):** **RESOLVED** ([SPEC.md](model-gating/benchmark/SPEC.md#L486-L508)).
- **1.3 Executor interface, `run.json` fields and read-only stage boundaries:** **RESOLVED** ([SPEC.md](model-gating/benchmark/SPEC.md#L463-L464), [SPEC.md](model-gating/benchmark/SPEC.md#L484), [SPEC.md](model-gating/benchmark/SPEC.md#L509-L515)).
- **1.4 Isolation (proxy routing to inference endpoint, proxy credential injection, disabling provider-side web search and URL fetching):** **RESOLVED** ([SPEC.md](model-gating/benchmark/SPEC.md#L511-L513), [SPEC.md](model-gating/benchmark/SPEC.md#L525-L530)).
- **2.1 Submission cap against flooding with genuine numbers:** **RESOLVED** ([SPEC.md](model-gating/benchmark/SPEC.md#L100-L102), [SPEC.md](model-gating/benchmark/SPEC.md#L432), [SPEC.md](model-gating/benchmark/SPEC.md#L480)).
- **2.2 Stripping rendered outputs from all targets and requiring source inspection in 6.3:** **RESOLVED** ([SPEC.md](model-gating/benchmark/SPEC.md#L50-L55), [SPEC.md](model-gating/benchmark/SPEC.md#L400-L408)).
- **2.3 Duplicate results invalidating the certificate and averaging over frozen gold results:** **RESOLVED** ([SPEC.md](model-gating/benchmark/SPEC.md#L371-L373), [SPEC.md](model-gating/benchmark/SPEC.md#L430-L432)).
- **2.4 Section 6.3 checkability (`inspect` fix category, quantum-rounded reference comparison, in-bundle slip and donor evidence, excluding errors removable by allowed 4.4 fixes):** **RESOLVED** ([SPEC.md](model-gating/benchmark/SPEC.md#L178-L181), [SPEC.md](model-gating/benchmark/SPEC.md#L245-L246), [SPEC.md](model-gating/benchmark/SPEC.md#L403-L417)).
- **3.1 Section 4.3 credit for verified original-version recovery on `rng_version` and `package_version` gold results:** **RESOLVED** ([SPEC.md](model-gating/benchmark/SPEC.md#L220-L222), [SPEC.md](model-gating/benchmark/SPEC.md#L332-L333)).
- **3.2 Section 4.6 `primary` definition and end-to-end extra-claim paper-outcome rule:** **RESOLVED** ([SPEC.md](model-gating/benchmark/SPEC.md#L96-L97), [SPEC.md](model-gating/benchmark/SPEC.md#L294-L296), [SPEC.md](model-gating/benchmark/SPEC.md#L333-L334)).
- **4.1 `G-15 C1, C2` donor-row hold and paper-outcome recomputation note:** **RESOLVED** ([SPEC.md](model-gating/benchmark/SPEC.md#L320), [SPEC.md](model-gating/benchmark/SPEC.md#L334-L335)).
- **4.2 In-bundle located-typo rule (`G-07 C1` and `G-22 C2, C3`):** **RESOLVED** ([SPEC.md](model-gating/benchmark/SPEC.md#L173-L181), [SPEC.md](model-gating/benchmark/SPEC.md#L318-L319)).
- **4.3 `G-28` held primary claim and scheduling exclusion:** **RESOLVED** ([SPEC.md](model-gating/benchmark/SPEC.md#L327-L329)).
- **4.4 Single-label gold v1.4 (`acceptable_statuses` and `acceptable_alternatives` removed):** **RESOLVED** ([SPEC.md](model-gating/benchmark/SPEC.md#L331-L333)).

### 2. The two non-adoptions

1. **No `1e-6` relative tolerance against unrounded gold references:** **ACCEPT.** Requiring both the model's recomputed value and the gold reference to round to the same value at the printed quantum under the same rounding mode ([SPEC.md](model-gating/benchmark/SPEC.md#L405-L408)), paired with mandatory source and diff inspection ([SPEC.md](model-gating/benchmark/SPEC.md#L400-L403)) and reference adjudication ([SPEC.md](model-gating/benchmark/SPEC.md#L338-L341)), is well-defined across all statuses and keeps the settled rounding convention ([SPEC.md](model-gating/benchmark/SPEC.md#L146-L153)) as the sole numerical tolerance.
2. **No 40-result cap (15-claim cap only):** **ACCEPT.** Gold claims with multi-column structures (such as `G-27 C1` to `C5`, which carry 30 atomic results across five claims, [SPEC.md](model-gating/benchmark/SPEC.md#L108-L109)) make a hard cap of 40 results too tight. Because [SPEC.md](model-gating/benchmark/SPEC.md#L100-L102) caps submissions at 15 claims, [SPEC.md](model-gating/benchmark/SPEC.md#L94-L95) and [SPEC.md](model-gating/benchmark/SPEC.md#L481) bind each claim to a single scientific referent, and [SPEC.md](model-gating/benchmark/SPEC.md#L424-L429) samples extra claims at the atomic `result_id` level, a model cannot pack unrelated table numbers into a submission without either breaching the 15-claim cap or falsifying claim referents.

### 3. Check for new errors or contradictions in draft 0.4 (sections 4.2, 5.1 and 7)

No new blocking errors or contradictions were introduced:

- **Sections 4.2 and 5.1 (`G-22 C2, C3` and `G-15 C1, C2`):** Reversing `G-22 C2, C3` to `discrepant, P2` ([SPEC.md](model-gating/benchmark/SPEC.md#L318)) is necessary and consistent with stripping rendered HTML outputs ([SPEC.md](model-gating/benchmark/SPEC.md#L50-L55)) and requiring slip evidence inside the bundle ([SPEC.md](model-gating/benchmark/SPEC.md#L178-L181)): the intercept (`5.25` vs `5.28`) and its confidence interval (`[5.08, 5.43]` vs `[5.11, 5.44]`) differ together, so neither has matching companion statistics for that model term, and only the excluded human report calls them a typo. Holding `G-15 C1, C2` until the donor pair `(-0.05, 0.06)` is verified in the package's executed output ([SPEC.md](model-gating/benchmark/SPEC.md#L320)) is likewise consistent with [SPEC.md](model-gating/benchmark/SPEC.md#L180) and [SPEC.md](model-gating/benchmark/SPEC.md#L306-L308).
- **Non-blocking note on `G-07 C1` ([SPEC.md](model-gating/benchmark/SPEC.md#L175-L176) and [SPEC.md](model-gating/benchmark/SPEC.md#L319)):** In [G-07.json](model-gating/gold-set/gold/G-07.json#L32-L44), `G-07 C1` (`0.14` printed for `1.14`) is an in-text descriptive standard deviation rather than a test statistic or table entry, and its conditional wording in [SPEC.md](model-gating/benchmark/SPEC.md#L319) (`"close, severity null, if the companion statistics match"`) should either be verified when freezing gold v1.4 or phrased as `"held until ...; then close, otherwise discrepant, P2"` to match [SPEC.md](model-gating/benchmark/SPEC.md#L306-L308) and [SPEC.md](model-gating/benchmark/SPEC.md#L320), with `"companion statistics of the same test or table row"` in [SPEC.md](model-gating/benchmark/SPEC.md#L175-L176) read to include an in-text descriptive summary (such as the accompanying mean).
- **Section 7 ([SPEC.md](model-gating/benchmark/SPEC.md#L452-L534)):** Coherent and complete as drafted.

VERDICT: AGREE as drafted
