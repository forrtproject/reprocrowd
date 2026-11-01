# Specification review, Gemini 4 Argon (High), round 2

Run through the Antigravity CLI (`agy -p`, read-only sandbox) on 1 November 2026 against SPEC.md draft 0.3, after two delegated attempts returned author-style summaries instead of a review and an OpenCode attempt returned nothing. Text as returned; local file links shortened to repository-relative paths.

### 1. Section 7 (modular pipeline): **DISAGREE**

A second team could not implement an interoperable multi-stage pipeline (such as a standalone Stage S1 claim-identification model followed by a Claude Code executor for Stages S2 and S3) from [SPEC.md](model-gating/benchmark/SPEC.md#L413-L470) alone.

#### Blocking gaps in Section 7

1. **Stage contracts ([SPEC.md](model-gating/benchmark/SPEC.md#L422-L437)):**
   - **Missing workspace layout and relative path rules:** Section 7.2 names `input-bundle.json`, `package/`, `article/`, `claims.json`, `results.json`, `certificate.json` and `run.json`, but never defines their paths relative to the stage working directory, nor where S2 must write modified scripts, logs and lockfiles so that S3 can resolve `"the code and logs they reference"` ([SPEC.md](model-gating/benchmark/SPEC.md#L432)).
   - **Missing S2 and S3 input consumption:** In the 7.2 table ([SPEC.md](model-gating/benchmark/SPEC.md#L431)), S2 consumes the article only in Track B (`"bundle, claims.json (Track B: also the article)"`), withholding `article/` from Track A S2 even when needed to interpret variable definitions, table structure or Stata translation ([SPEC.md](model-gating/benchmark/SPEC.md#L225-L226)). S3 ([SPEC.md](model-gating/benchmark/SPEC.md#L432)) omits `input-bundle.json`, which S3 needs for target metadata, track, and raw versus processed data scope.
   - **Undefined JSON keys connecting S1, S2 and S3:** [certificate.schema.json](schemas/certificate.schema.json#L65-L97) has `claims[].id` (`^C[0-9]+$`) and `results[].claim_id`, but no `result_id` ([SPEC.md](model-gating/benchmark/SPEC.md#L94)), no `primary` flag ([SPEC.md](model-gating/benchmark/SPEC.md#L261)), no typed value object ([SPEC.md](model-gating/benchmark/SPEC.md#L100-L103)), and no `within_variation` status ([certificate.schema.json](schemas/certificate.schema.json#L88)). Section 7.2 does not state how `claims.json`, `results.json` and `certificate.json` key results (`claim_id` plus `result_id`) or how interval endpoints are typed (`"value": [low, high]` and `"quantum": [q_low, q_high]`).
2. **Pipeline manifest ([SPEC.md](model-gating/benchmark/SPEC.md#L439-L454)):**
   - **Stage vocabulary and file handoff:** The example manifest uses `"id": "S1-S3"`, `"consumes": ["input-bundle"]` and `"produces": ["claims", "results", "certificate"]` ([SPEC.md](model-gating/benchmark/SPEC.md#L445-L446)), without defining valid stage IDs (`S1`, `S2`, `S3`, `S1-S2`, `S2-S3`, `S1-S3`), how S2 passes its workspace directory (`workspace/` with edited scripts and logs) to S3, or how decomposed mode ([SPEC.md](model-gating/benchmark/SPEC.md#L435-L436)) declares frozen upstream artefacts.
   - **Prompt contract:** [SPEC.md](model-gating/benchmark/SPEC.md#L451) refers to `"a filled prompt"` (mirroring hardcoded string replacements in [`run_codex.py`](model-gating/benchmark/run_codex.py#L66-L68)), but defines no template variables. Stages should read fixed relative paths in the working directory rather than rely on ad-hoc prompt interpolation.
3. **Executor interface and run record ([SPEC.md](model-gating/benchmark/SPEC.md#L433) and [SPEC.md](model-gating/benchmark/SPEC.md#L450-L454)):**
   - **No adapter call/return signature:** Section 7.3 does not specify what arguments an executor adapter receives (`stage_id`, `work_dir`, `prompt_path`, `model`, `options`, `timeout_minutes`, `env`) or the JSON structure it returns (`exit_status`, `resolved_model`, `executor_version`, `wall_clock_seconds`, `tokens`, `cost_usd`, `events_log_path`).
   - **Stage boundary mutability:** If S2 and S3 share a writable directory, S3 can mutate S2's `results.json` or logs. Each stage needs upstream artefacts mounted read-only and its own writable directory.
4. **Isolation ([SPEC.md](model-gating/benchmark/SPEC.md#L456-L470)):**
   - **LLM API traffic, credentials and server-side search loophole:** [SPEC.md](model-gating/benchmark/SPEC.md#L463-L466) forbids credentials in the container and blocks all network traffic except package repositories (`CRAN`, `Posit Package Manager`, `Bioconductor`, `PyPI`, `conda`). A CLI agent (`codex_cli`, `claude_code`) running inside the container cannot reach its LLM API under that rule unless the proxy also routes to the configured model API endpoint and injects API authentication headers outside the container. Worse, if a model invokes a **provider-hosted web search or URL-fetch tool** (such as Anthropic or OpenAI server-side web search), the container proxy sees only HTTPS traffic to the LLM provider while the provider fetches OSF reports or GitHub repositories server-side. Provider-side web search and fetch tools must be disabled in `options` and verified absent in the provider event log.

#### Replacement wording for Section 7.2 to 7.4 ([SPEC.md](model-gating/benchmark/SPEC.md#L422-L470))

> ### 7.2 Stage contracts
>
> Every stage runs in a fresh working directory. Consumed artefacts from earlier stages are mounted read-only at fixed relative paths: `./input-bundle.json`, `./article/`, `./package/` (Track A: code, data and docs, with shipped rendered outputs stripped as in 2.2 except where code is embedded; Track B: sanitised data and docs only), `./claims.json` (after S1), and `./results.json` plus `./s2-workspace/` (after S2). Every stage artefact is JSON with `"schema_version": "1.2"` and keyed by `claim_id` (`^C[0-9]+$`) and `result_id` (`^C[0-9]+\.[a-z0-9_]+$`). For intervals, `value` and `quantum` in typed printed values (3.2) are two-element arrays `[low, high]`.
>
> | Stage | Consumes (read-only) | Produces (in `./`) |
> |---|---|---|
> | S0 package (evaluator) | pinned sources | `input-bundle.json`, `package/`, `article/`: `"schema_version"`, `"target_id"`, `"track"` (`"A"` or `"B"`), `"mode"`, `"data_scope"` (`"raw"` or `"processed"`), `"files"` (`[{path, sha256, bytes}]`), `"limits"` (`{"max_claims": 15, "max_results": 40}`) |
> | S1 identify | `input-bundle.json`, `article/`, `package/` | `claims.json`: `"claims": [{claim_id, claim, primary, exhibit, page_printed, page_pdf, quote_or_cell, referent: {study, sample, outcome, predictor, model, wave, statistic}, selection_reason, results: [{result_id, quantity, reported: {token, kind, operator, value, quantum, unit, scale}}]}]` |
> | S2 reproduce | `input-bundle.json`, `article/`, `package/`, `claims.json` | `results.json` and `./s2-workspace/`: `"results": [{claim_id, result_id, state: "completed"\|"blocked"\|"ambiguous"\|"failed"\|"timed_out", recomputed: {value_unrounded, value_emitted, unit, scale}, execution: {script_path, script_sha256, lines, command, exit_status, stdout_log, stderr_log, env_lockfile}, fixes: [{category, file, sha256, lines, diff_path, change, reason}], method_choices: [{choice, article_locator, quote}], variation: {source, runs: [{run_id, seed_or_setting, value_unrounded, log_path}]}}]` |
> | S3 judge | `input-bundle.json`, `article/`, `package/`, `claims.json`, `results.json`, `s2-workspace/` | `certificate.json` (schema 1.2): per `(claim_id, result_id)`, `status`, `basis`, `claim_outcome`, `comparison`, `slip_evidence` or `blocker_evidence`, `severity`, `printed_match`; paper-level `validation_status` and `findings` |
> | run record (runner) | all stage directories, proxy and process logs | `run.json`: `"manifest_sha256"`, `"input_bundle_sha256"`, `"stages": [{stage_id, attempt, started_at, ended_at, exit_status, wall_clock_seconds, executor, executor_version, provider, requested_model, resolved_model, options, prompt_path, prompt_sha256, tokens: {input, output, reasoning_or_cached}, cost_usd, events_log, artefact_hashes, process_log, network_log}]` |
>
> In decomposed mode, the runner mounts the frozen gold `claims.json` (without labels) in place of S1, or a frozen S1+S2 bundle in place of S1 and S2. A judgement-only (S3) run is diagnostic only.
>
> ### 7.3 Pipeline manifest and executor interface
>
> ```json
> {"name": "split-s1-claude-s2s3", "track": "A", "mode": "end_to_end",
>  "defaults": {"executor": "claude_code", "model": "claude-opus-5-5",
>               "options": {"reasoning_effort": "high", "web_search": false},
>               "timeout_minutes": 75, "max_cost_usd": 25.0, "retries_on_infra_error": 1},
>  "stages": [
>    {"id": "S1", "executor": "api_loop", "model": "gpt-6-luna",
>     "prompt": "prompts/s1-identify-v1.2.txt",
>     "consumes": ["input-bundle", "article", "package"], "produces": ["claims"]},
>    {"id": "S2-S3", "prompt": "prompts/s2s3-reproduce-judge-A-v1.2.txt",
>     "consumes": ["input-bundle", "article", "package", "claims"],
>     "produces": ["results", "s2-workspace", "certificate"]}
>  ]}
> ```
>
> Valid `id` values are `"S1"`, `"S2"`, `"S3"`, `"S1-S2"`, `"S2-S3"` and `"S1-S3"`. Stage fields override `defaults`. Prompts require no string interpolation; they instruct the agent to read the mounted paths in `./` and write the stage outputs to `./`. Each executor adapter implements `run_stage(stage_cfg, work_dir, env) -> StageAttemptRecord` and writes the raw provider event stream (`events.jsonl`) so the runner can verify `resolved_model`, `options` (including disabled provider-side web search/fetch tools) and token counts against the manifest.
>
> ### 7.4 Isolation
>
> Each stage attempt runs in its own container (or equivalent OS sandbox) with:
> - only its declared `consumes` artefacts mounted read-only and a fresh writable `./` directory;
> - no access to the host repository, home directory, raw API credentials, previous runs or other targets;
> - network access only through an evaluator-controlled proxy that allows package repositories (CRAN, Posit Package Manager, Bioconductor, PyPI, conda; plus evaluator mirrors for GitHub dependencies) and, when the executor runs inside the sandbox, the configured LLM inference endpoint with API credentials injected by the proxy. Provider-side web search and URL-fetching tools must be disabled in `options` and verified absent in `events.jsonl`. Every request is logged outside the model's control;
> - a read-only shared base library of R and Python packages plus a per-stage writable library.
>
> An executor that cannot enforce this policy produces diagnostic results only, not ranking results.

---

### 2. Section 6 (scoring): **DISAGREE**

The overall structure of Section 6 ([SPEC.md](model-gating/benchmark/SPEC.md#L326-L411)) is close, but three gaming/soundness gaps and four checkability bugs in Section 6.3 remain.

#### Blocking points on gaming resistance and checkability

1. **Flooding with real (non-fabricated) claims games subset recall ([SPEC.md](model-gating/benchmark/SPEC.md#L83-L89) and [SPEC.md](model-gating/benchmark/SPEC.md#L384-L393)):**
   - Section 6.4 audits extra claims only for *fabricated* reported targets (`"invented or materially misattributed reported targets"`, [SPEC.md](model-gating/benchmark/SPEC.md#L388-L389)). A model that dumps every genuine number printed in the paper's tables (say 100 real reported results) and runs the main script once has zero fabricated targets, triggers no gate, and achieves 100% recall on the 5 to 8 must-check claims without doing claim selection.
   - **Lean fix:** Cap end-to-end submissions at `max_claims: 15` and `max_results: 40` per paper (supplied in `input-bundle.json`, against gold's 5 to 8 claims); certificates exceeding the cap are invalid.
2. **Reading shipped outputs in gold packages or passing 6.3 via `"or a trusted reference check"` allows copying values ([SPEC.md](model-gating/benchmark/SPEC.md#L52-L55) and [SPEC.md](model-gating/benchmark/SPEC.md#L368-L370)):**
   - First, [SPEC.md](model-gating/benchmark/SPEC.md#L369-L370) states: `"A recorded source inspection or a trusted reference check is sufficient; the evaluator does not rerun every analysis."` Making `"a trusted reference check"` an `"or"` alternative to source inspection directly contradicts the preceding sentence (`"a submitted log, a hard-coded printed value or numerical agreement alone is not enough"`, [SPEC.md](model-gating/benchmark/SPEC.md#L368-L369)): a script `cat("0.15\n")` runs in `run.json` and matches the gold reference `0.15`. Source/diff inspection is always required; reference comparison is an additional numerical check.
   - Second, Section 2.2 ([SPEC.md](model-gating/benchmark/SPEC.md#L52-L55)) strips rendered outputs only from *twins*, leaving shipped `.tex`, `.csv`, `.html` and `.txt` log outputs inside gold packages ([G-03.json](model-gating/gold-set/gold/G-03.json#L48-L50), [G-11.json](model-gating/gold-set/gold/G-11.json#L32), [G-16.json](model-gating/gold-set/gold/G-16.json#L145), [G-18.json](model-gating/gold-set/gold/G-18.json#L11), [G-22.json](model-gating/gold-set/gold/G-22.json#L11)). Reading shipped rendered outputs or logs instead of executing the analysis code must earn 0 credit (and S0 should strip rendered outputs from gold packages under the same rule as twins, extracting embedded scripts where code is only in HTML as in [G-22.json](model-gating/gold-set/gold/G-22.json#L13)).
3. **Duplicate rows ([SPEC.md](model-gating/benchmark/SPEC.md#L338-L339) and [SPEC.md](model-gating/benchmark/SPEC.md#L392-L393)):**
   - [SPEC.md](model-gating/benchmark/SPEC.md#L392-L393) says: `"The certificate has one final result per scientific identity; contradictory duplicates make it invalid."` Any duplicate result for the same `(claim_id, result_id)` or scientific identity (not just contradictory ones) should make the certificate invalid, and [SPEC.md](model-gating/benchmark/SPEC.md#L338) should explicitly state that averaging is over the *frozen gold required results* of each gold must-check claim.
4. **What in 6.3 is impossible to check as written ([SPEC.md](model-gating/benchmark/SPEC.md#L366-L379)):**
   - **Extracting an `"unrounded value from the execution output"` ([SPEC.md](model-gating/benchmark/SPEC.md#L367-L368)):** In Track A (`shipped_code`), authors' scripts frequently call `round()`, `sprintf()`, `stargazer()` or `kable()`, or emit bounds like `< 2e-16`, while Section 4.4 ([SPEC.md](model-gating/benchmark/SPEC.md#L217-L227)) does not permit editing code to print unrounded numbers. Thus an unrounded output often does not exist unless Track A permits non-mutating output-print statements or 6.3 accepts the precision emitted by unmodified shipped code.
   - **`"equal it at the printed quantum"` ([SPEC.md](model-gating/benchmark/SPEC.md#L371)):** When a gold `reference_recomputed` is an unrounded float `r_gold` (not a multiple of `q`), `"equals r_gold at quantum q"` is undefined unless specified as `round(r_model, q) == round(r_gold, q)` under a common rounding mode; and on truncation `close` claims (such as [G-08.json](model-gating/gold-set/gold/G-08.json#L130) C4, `r_gold = 0.198`, `q = 0.01`) or Track B recreations of `discrepant` claims, two valid computations can differ slightly in unrounded value. Moreover, several deterministic `match` gold claims ([G-03.json](model-gating/gold-set/gold/G-03.json#L39), [G-07.json](model-gating/gold-set/gold/G-07.json#L60)) currently have `reference_recomputed: null`, and [G-15.json](model-gating/gold-set/gold/G-15.json#L127-L150) C5 and C6 store `"35%"` and `"24%"` as strings.
   - **`"the slip applied to the recomputed value gives the printed value"` ([SPEC.md](model-gating/benchmark/SPEC.md#L373-L374)):** For a transposed/copied cell or row ([G-18.json](model-gating/gold-set/gold/G-18.json#L59) C1, [G-15.json](model-gating/gold-set/gold/G-15.json#L32-L74) C1-C2), the printed value comes from the *donor* cell's recomputed value, not the target claim's own recomputed value. And for a `"located typo"` ([SPEC.md](model-gating/benchmark/SPEC.md#L160-L162)), in [G-07.json](model-gating/gold-set/gold/G-07.json#L43) C1 (`0.14` vs `1.14`), [G-15.json](model-gating/gold-set/gold/G-15.json#L43) C1-C2, and [G-22.json](model-gating/gold-set/gold/G-22.json#L275) C2-C3, the `"documented source"` cited in gold is the **human reproduction report**, which the model is **forbidden to access** under the hard gate in [SPEC.md](model-gating/benchmark/SPEC.md#L402)! A model cannot verify a source-identified typo if the source is outside the input bundle.
   - **Self-inflicted `not_checkable` blockers ([SPEC.md](model-gating/benchmark/SPEC.md#L377-L379)):** Section 6.3 must state explicitly that an error removable by an allowed Track A fix (4.4) does not qualify as a study blocker.

#### Replacement wording for Section 6.1 (item 1), 6.3 and 6.4 ([SPEC.md](model-gating/benchmark/SPEC.md#L331-L339) and [SPEC.md](model-gating/benchmark/SPEC.md#L362-L399))

> 1. **Result credit.** A gold must-check result earns 1 when all of these hold:
>    - it is identified and mapped (3.3);
>    - its evidence passes (6.3);
>    - its basis and fixes are admissible (4.4);
>    - its status matches the gold status (or, for a `package_version` or `rng_version` result under 4.3, its verified original-version recovery matches the resulting deterministic status).
>
>    Otherwise it earns 0. Credit is averaged over all required `result_id`s of each gold must-check claim (unmapped gold results score 0), and gold claims are averaged within a paper.

> ### 6.3 Evidence checks
>
> The checks depend on the status:
>
> - **`match`, `close`, `discrepant`.** The evaluator verifies by recorded source and diff inspection (hash-checked against `input-bundle.json` and `run.json`) that the result was computed from the permitted inputs by the admissible analysis (not read from shipped rendered tables or logs), and extracts the recomputed value from the execution output (unrounded when accessible, or at the precision emitted by unmodified shipped code). Non-mutating print or object-inspection statements are permitted in Track A to log unrounded values. Where gold has a numeric reference value, the recomputed value must also agree with it when both are rounded to the printed quantum (or within `1e-6` relative for unrounded Track A deterministic references, subject to 5.1). Twins have exact planted references.
> - **`close`.** The named slip must be demonstrated from materials inside the input bundle and execution output: applying truncation or digit transposition to the recomputed value, copying from an identified donor cell in the executed output, or matching an author erratum/corrigendum or single-character edit (where companion statistics for the same model/test match) gives the printed value.
> - **`within_variation`.** The repeated runs and their settings must be in the bundle, pass the same analysis and provenance check, show actual variation across at least five independent seeds (or two controlled versions/platforms/schedules), and be compatible with the printed value under 4.3.
> - **`not_checkable`.** A specific study blocker must be named (the missing file, the failing statement and its error that cannot be resolved by an allowed 4.4 fix, or the Track B ambiguity) and match the gold blocker. An unsupported abstention or self-inflicted execution error earns nothing.
>
> Mechanical checks cover structure, hashes, numerical predicates and the presence of values in logs. A fix's admissibility and a Track B ambiguity need evaluator adjudication, which is recorded.
>
> ### 6.4 Submission limits, extra claims and hard gates
>
> An end-to-end submission may contain at most 15 claims and 40 results (`limits` in `input-bundle.json`); exceeding this cap or submitting duplicate results for the same `(claim_id, result_id)` or scientific identity makes the certificate invalid. Extra claims within the cap are counted and audited. For each target, a uniform sample without replacement of five distinct extra result identities (or all, if fewer) is drawn with a recorded seed from a canonical ordering. The audit counts invented or materially misattributed **reported targets** (values the model says the article prints), after permitted normalisation; recomputed values, diagnostics and intermediates are not reported targets. Two distinct verified fabrications anywhere in a certificate trigger the fabrication gate; a single instance is recorded without the gate. Every result used for score credit is audited in full.

---

### 3. The four `[proposed]` items

1. **4.3 Variation-first precedence ([SPEC.md](model-gating/benchmark/SPEC.md#L197-L203)): DISAGREE as worded (AGREE in principle, subject to one blocking fix for version recovery).**
   - **Why:** Precedence of `within_variation` over a single-run `match` is right for intrinsic nondeterminism (`unseeded`, `parallel`, `optimiser`). However, [SPEC.md](model-gating/benchmark/SPEC.md#L199-L200) states: `"When all relevant sources are fixed (original seed and versions recovered), the deterministic rules apply and may give match, close or discrepant."` If a gold result is labelled `within_variation` due to `package_version` or `rng_version`, and a candidate model uses an allowed `package` fix ([SPEC.md](model-gating/benchmark/SPEC.md#L220)) or `RNGversion()` to recover the authors' original version and rightly reports `match` under [SPEC.md](model-gating/benchmark/SPEC.md#L199-L200), it will score 0 under [SPEC.md](model-gating/benchmark/SPEC.md#L336) because its status (`match`) does not equal `within_variation`.
   - **Exact replacement wording ([SPEC.md](model-gating/benchmark/SPEC.md#L197-L203)):**
     > **Precedence.** A compatible result with established variation is `within_variation`, even when a run prints the reported value; the record notes `printed_match: true`. When all relevant sources are fixed (original seed and package/RNG versions recovered and verified in the bundle), the deterministic rules apply and may give `match`, `close` or `discrepant`; for `rng_version` and `package_version` gold results, both `within_variation` (from multi-version runs) and the verified original-version deterministic status earn credit. A demonstrated structural blocker takes precedence over variation. A result outside the region is `discrepant`. Insufficient gold evidence means the gold result is held (5.1). A model that asserts variation without the evidence gets no credit for `within_variation`.

2. **4.6 Paper outcome table ([SPEC.md](model-gating/benchmark/SPEC.md#L258-L272)): DISAGREE as worded (AGREE with the three-way partition, subject to defining `primary` and handling valid extra claims in end-to-end runs).**
   - **Why:** The three bullets ([SPEC.md](model-gating/benchmark/SPEC.md#L264-L268)) form a clean, mutually exclusive and exhaustive partition of any fixed scope with a non-empty primary subset. However, (a) neither Section 4.6 nor the gold JSON files define which claims are `primary`, and in end-to-end runs the model never sees the gold claim list ([SPEC.md](model-gating/benchmark/SPEC.md#L436-L437)); and (b) if all 5 to 8 gold claims are `match` (`Computationally reproducible`), an end-to-end model that also checks an extra claim in the paper and finds a genuine discrepancy will honestly report `Computational issues` under 4.6 and have its paper score halved under 6.1 ([SPEC.md](model-gating/benchmark/SPEC.md#L341)).
   - **Exact replacement wording ([SPEC.md](model-gating/benchmark/SPEC.md#L260-L268)):**
     > Before targets are scheduled, each paper's scored assessment scope is frozen, after removing held and (Track B) ineligible results, together with a non-empty `primary` subset (main-text focal hypothesis tests and headline estimates, excluding sample descriptives, manipulation checks and robustness tables). A target with no scored claims or no assessable primary result is not scheduled.
     >
     > - **Computationally reproducible:** every assessed result is `match`, `close` or `within_variation`. Reporting slips are listed separately in the certificate; they do not make the computation fail.
     > - **Technical failure:** demonstrated study blockers prevent every primary computation.
     > - **Computational issues:** at least one primary computation completes, and an assessed result is `discrepant` or `not_checkable`.
     >
     > In end-to-end runs, if a model's paper outcome differs from gold solely because of an extra claim outside the gold must-check subset, the paper outcome counts as correct when that extra claim passes the 6.3 evidence check.

3. **6.1 The 0.5 multiplier for a wrong paper outcome ([SPEC.md](model-gating/benchmark/SPEC.md#L340-L343)): AGREE.**
   - Halving the claim average makes paper-level synthesis consequential without zeroing out verified claim-level reproduction work when a single borderline claim flips the paper outcome.

4. **6.4 Extra-claim fabrication gate at two ([SPEC.md](model-gating/benchmark/SPEC.md#L390-L392) and [SPEC.md](model-gating/benchmark/SPEC.md#L398)): AGREE.**
   - Setting the gate at two distinct verified fabricated reported targets avoids zeroing a paper over a single OCR or transcription slip while still penalising systematic hallucination (provided the submission cap in Question 2 is added to prevent flooding with real table numbers).

---

### 4. Contradictions between sections and spot-check against `gold/G-xx.json`: **DISAGREE**

#### Blocking contradictions

1. **Contradiction between 5.1 ([SPEC.md](model-gating/benchmark/SPEC.md#L291) and [SPEC.md](model-gating/benchmark/SPEC.md#L300-L302)), 4.6 ([SPEC.md](model-gating/benchmark/SPEC.md#L264-L265)), and [G-15.json](model-gating/gold-set/gold/G-15.json#L21-L163) (Spot-check 1: `G-15 C1, C2`):**
   - In [G-15.json](model-gating/gold-set/gold/G-15.json#L32-L163), `C1` and `C2` (`discrepant`, `severity: "P2"`) are the **only** non-`match` claims (`C3` to `C6` are all `match`).
   - Row 7 of the 5.1 table ([SPEC.md](model-gating/benchmark/SPEC.md#L291)) relabels `G-15 C1, C2` to `close, severity null`. Under Section 4.6 ([SPEC.md](model-gating/benchmark/SPEC.md#L264-L265)), because every assessed result in `G-15` is now `match` or `close`, `G-15`'s paper outcome **must** change from `"computational issues"` ([G-15.json](model-gating/gold-set/gold/G-15.json#L21)) to `"computationally reproducible"`. Yet [SPEC.md](model-gating/benchmark/SPEC.md#L300-L302) states: `"Paper outcomes are recomputed under 4.6 after the claim labels settle; G-07, whose only scored discrepancy may become close, is the likely change"`, overlooking `G-15`.
   - Furthermore, [G-15.json](model-gating/gold-set/gold/G-15.json#L32-L74) does not identify which donor row in the R output of `cashout-prob-analyses.R` contains `-0.05` and `0.06`; if that donor row is only mentioned in the forbidden human report ([G-15.json](model-gating/gold-set/gold/G-15.json#L17)) and not produced by the package scripts, a blinded model cannot substantiate `close` under 4.2 and 6.3.
2. **Contradiction between 4.2 ([SPEC.md](model-gating/benchmark/SPEC.md#L160-L162)), 5.1 ([SPEC.md](model-gating/benchmark/SPEC.md#L289-L291)), and 6.4 ([SPEC.md](model-gating/benchmark/SPEC.md#L402)) on source-identified typos (Spot-check 2: `G-07 C1` and `G-22 C2, C3`):**
   - In [G-07.json](model-gating/gold-set/gold/G-07.json#L10-L52), the pinned package contains only `.R` and `.Rmd` files (not the accepted manuscript mentioned in `notes.sol` line 151), and the `"Source"` that identifies `0.14` for `1.14` as an isolated typo ([SPEC.md](model-gating/benchmark/SPEC.md#L290)) is the I4R human reproduction report ([G-07.json](model-gating/gold-set/gold/G-07.json#L17) and [G-07.json](model-gating/gold-set/gold/G-07.json#L43)), which models are forbidden to access under the hard gate in [SPEC.md](model-gating/benchmark/SPEC.md#L402).
   - Similarly, in [G-22.json](model-gating/gold-set/gold/G-22.json#L264-L311), the `"Source"` identifying `5.25` vs `5.28` (`C2`) and `[5.08, 5.43]` vs `[5.11, 5.44]` (`C3`) as one misprint ([SPEC.md](model-gating/benchmark/SPEC.md#L289)) is the forbidden I4R report ([G-22.json](model-gating/gold-set/gold/G-22.json#L215)). Unless 4.2 defines an isolated typo by objective criteria verifiable inside the bundle (or `G-22 C3` stays `discrepant` when `[5.08, 5.43]` vs `[5.11, 5.44]` has no in-bundle erratum), a model that obeys the isolation rules cannot prove `close` on `G-07 C1` or `G-22 C3`.
3. **Contradiction between 5.1 ([SPEC.md](model-gating/benchmark/SPEC.md#L294) and [SPEC.md](model-gating/benchmark/SPEC.md#L298)), 4.6 ([SPEC.md](model-gating/benchmark/SPEC.md#L260-L266)), and [G-28.json](model-gating/gold-set/gold/G-28.json#L36-L178) (Spot-check 3: `G-28 C3, C4, C6`):**
   - In [G-28.json](model-gating/gold-set/gold/G-28.json#L36-L178), `C3` is the only primary outcome (`"Primary outcome (C1); Figure 3a"`, line 96), `C4` and `C6` are secondary reproducing outcomes, and `C1`, `C2` and `C5` are all `not_checkable` (`P0`, missing `time` column in `KSS_data.csv`).
   - Row 10 of 5.1 ([SPEC.md](model-gating/benchmark/SPEC.md#L294)) holds `C3, C4, C6`, and [SPEC.md](model-gating/benchmark/SPEC.md#L298-L299) allows held claims to `"stay excluded and are reported as such"`. If `C3, C4, C6` stay excluded, `G-28` has no assessable primary claim (so it cannot be scheduled under [SPEC.md](model-gating/benchmark/SPEC.md#L261-L262)), and its only remaining claims (`C1, C2, C5`) are all `P0` blocked (`technical failure`, contradicting `"computational issues"` in [G-28.json](model-gating/gold-set/gold/G-28.json#L25)). Evaluator reruns for `G-28 C3, C4, C6` (and `G-29 C1-C3`) must therefore be completed before scheduling those papers, rather than left optionally excluded.
4. **Multiple `acceptable_alternatives` and `acceptable_statuses` in `gold/G-xx.json` vs single-label scoring in 4.5, 4.6 and 6.1:**
   - [G-11.json](model-gating/gold-set/gold/G-11.json#L22-L24), [G-27.json](model-gating/gold-set/gold/G-27.json#L22-L24), [G-28.json](model-gating/gold-set/gold/G-28.json#L26-L28) and [G-29.json](model-gating/gold-set/gold/G-29.json#L22-L24) still carry non-empty paper-level `acceptable_alternatives`, and [G-16.json](model-gating/gold-set/gold/G-16.json#L92-L95) C3 carries `["discrepant", "not_checkable"]`, whereas Sections 4.6 and 6.1 assume a single gold status and paper outcome. Section 5.1 must state that `acceptable_alternatives` and multi-status `acceptable_statuses` are removed in gold v1.4 (except for the explicit version-recovery rule in 4.3).

#### Replacement wording for Section 4.2 (fourth bullet, [SPEC.md](model-gating/benchmark/SPEC.md#L160-L162)) and Section 5.1 ([SPEC.md](model-gating/benchmark/SPEC.md#L290-L304))

In [SPEC.md](model-gating/benchmark/SPEC.md#L160-L162), replace the fourth bullet of 4.2 with:

> - a **located typo**: an author erratum, corrigendum, preprint or shipped output table inside the input bundle identifies the specific entry and gives the corrected value, or the printed scalar differs from the recomputed value by a single-character edit while companion statistics for the same test or table row match. A general remark that a paper contains typos, or an external reproduction report outside the bundle, does not establish `close`.

In [SPEC.md](model-gating/benchmark/SPEC.md#L289-L304), replace the `G-22 C2, C3`, `G-07 C1` and `G-15 C1, C2` rows and the paragraph following the table with:

> | G-22 C2, C3 | close | C2: close; C3: close if the shipped HTML table stays in the Track A bundle as author typo evidence, else discrepant, P2 | Shipped HTML prints 5.28 and [5.11, 5.44]; without it, [5.08, 5.43] vs [5.11, 5.44] is not a single-character edit or truncation |
> | G-07 C1 | discrepant, P2 | close, severity null | Single-character typo (0.14 for 1.14) with matching companion test statistics; also confirmed in accepted manuscript |
> | G-15 C1, C2 | discrepant, P2 | close, severity null (if the donor row `-0.05, 0.06` is emitted by the package scripts; else discrepant, P2) | Coefficient and SE pair copied from an adjacent row |
>
> Held results (`G-16`, `G-28`, `G-29`) must be resolved by evaluator reruns before scheduling those targets; a target whose primary subset remains held is not scheduled (4.6). Every gold result gets a `primary` boolean and a `nondeterminism` record (null when deterministic), and legacy `acceptable_alternatives` and multi-status `acceptable_statuses` are removed. Paper outcomes are recomputed under 4.6 after the claim labels settle (`G-07` and, if `G-15 C1, C2` become `close`, `G-15` change from `computational issues` to `computationally reproducible`). Stale explanatory text and duplicate diagnostic entries (such as `G-08` C4 and C6, `G-11` C2 and C5, and the copy-pasted evidence strings in `G-29` C4 to C7) are repaired.

---

### Non-blocking points

1. **Internal contradiction in [G-08.json](model-gating/gold-set/gold/G-08.json#L174-L193) C6:** `reference_recomputed` (`0.2047054162220282`) is simultaneously the active scoring reference (`expected_status: "match"`) and listed in `diagnostic_results` with `"is_scoring_reference": false` (`"explains the printed pair but is a different wave"`). Clean up `diagnostic_results` as part of the v1.4 text repair noted in [SPEC.md](model-gating/benchmark/SPEC.md#L302-L303).
2. **Copy-pasted evidence strings in [G-29.json](model-gating/gold-set/gold/G-29.json#L94-L152) C4 to C6:** Claims C4 and C5 (critical-sentence completion times) and C6 (race-trial mixed model) all carry the C1-C3 bootstrap quote `"response-time subsection: ±0.2"` as their `evidence` string. Repair in gold v1.4.
3. **Reachability of `G-08` C6 requires `skip_failing_statement`:** As noted in [G-08.json](model-gating/gold-set/gold/G-08.json#L226-L228), line 224 of `BPV_museums_maintext.R` errors before the follow-up models, so `G-08 C6` requires `basis: justified_fix` (`skip_failing_statement`) and its claim outcome under 4.5 ([SPEC.md](model-gating/benchmark/SPEC.md#L245-L248)) is `"reproduces with justified fixes"`. Record this expected basis in gold v1.4.

VERDICT: AGREE subject to the blocking changes listed
