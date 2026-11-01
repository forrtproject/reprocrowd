# Specification review, Gemini 4 Argon (High), round 4

Run through the Antigravity CLI (`agy -p`, read-only sandbox) on 1 November 2026 against SPEC.md draft 0.5 (commit 6c914fb), in parallel with Sol round 4. Text as returned; local links shortened.

### 1. Implementation of the three settled rulings across sections 1, 3, 4, 5.1, 6, 7 and 8

- **Section 1 ([SPEC.md](model-gating/benchmark/SPEC.md#L13-L35)):** Implements exhaustive extraction, reproduction, and judgement (including deviation explanations) consistently.
- **Section 3 ([SPEC.md](model-gating/benchmark/SPEC.md#L94-L146)):** Replaces the 5 to 8 claim selection and 15-claim cap with exhaustive extraction and treats the existing 5 to 8 claims as the labelled subset. However, [SPEC.md](model-gating/benchmark/SPEC.md#L112) still states that *"Each labelled claim also records whether it is **primary**"*, whereas decomposed runs mount the full gold extraction without labels ([SPEC.md](model-gating/benchmark/SPEC.md#L523-L524)) and S1 records `primary` on every extracted claim ([SPEC.md](model-gating/benchmark/SPEC.md#L518)); see **B1**.
- **Section 4 ([SPEC.md](model-gating/benchmark/SPEC.md#L148-L321)):** Implements the one-unit + identified-slip rule for `close` and `deviation_explanation` in 4.2 ([SPEC.md](model-gating/benchmark/SPEC.md#L176-L206)), but has three leftover conflicts:
  1. In 4.1 ([SPEC.md](model-gating/benchmark/SPEC.md#L172-L174)), prose inferences stated in words (*"significant at the 5% level"*) are still defined as separate results of kind `bound`, which under exhaustive extraction would require extracting prose significance claims across the entire paper (see **B1**).
  2. In 4.6 ([SPEC.md](model-gating/benchmark/SPEC.md#L304-L306)), *"Before targets are scheduled, each paper's scored assessment scope is frozen, after removing held and (Track B) ineligible results... Outcomes describe only this scope"* is left over from the selection-based design and contradicts [SPEC.md](model-gating/benchmark/SPEC.md#L315) (*"The paper outcome draws on every result the model reproduces"*); see **B4**.
  3. Draft 0.5 deleted the definition of `severity` (`P0`, `P1`, `P2`, `null`) from Section 4, leaving `P2`, `P1`, `P0`, and `severity` undefined in 5.1, 6.2, 6.4, and 7.2; see **B5**.
- **Section 5.1 ([SPEC.md](model-gating/benchmark/SPEC.md#L325-L363)):** Correctly updates `G-22 C2, C3`, `G-07 C1`, and `G-15 C1, C2` under the tightened `close` rule, but omits `deviation_explanation` for `G-21 C3, C4, C5`, `G-08 C4`, `G-18 C1, C2`, and `G-22 C1` in the v1.4 table ([SPEC.md](model-gating/benchmark/SPEC.md#L334-L338)) and from the per-result field list in [SPEC.md](model-gating/benchmark/SPEC.md#L354); see **B5**.
- **Section 6 ([SPEC.md](model-gating/benchmark/SPEC.md#L380-L488)):** Removes the old 15-claim cap and extra-claim sampling rule, integrates extraction recall into 6.1, adds `deviation_explanation` accuracy to 6.2, and adds the misreading vs hallucination rules in 6.4. However, 6.3 ([SPEC.md](model-gating/benchmark/SPEC.md#L435-L438)) checks slip evidence only for `close` and not for explained `discrepant` results (see **B3**), and 6.4 has a mechanical-decidability gap between neighbouring-cell misreadings and wrong-referent hallucinations (see **B2**).
- **Section 7 ([SPEC.md](model-gating/benchmark/SPEC.md#L489-L584)):** Updates S1, S3, and decomposed mode for exhaustive extraction, but S1 ([SPEC.md](model-gating/benchmark/SPEC.md#L518)) places locators and referents at the claim level rather than the result level (see **B3**).
- **Section 8 ([SPEC.md](model-gating/benchmark/SPEC.md#L586-L611)):** Consistent with all three rulings.

---

### 2. Implementability analysis

#### (a) Can two extractors agree using the 3.1 scope? What must be added?
Not as currently drafted in [SPEC.md](model-gating/benchmark/SPEC.md#L96-L106). Two independent extractors cannot be *"matched mechanically by locator and token"* ([SPEC.md](model-gating/benchmark/SPEC.md#L104)) unless five rules are added to 3.1:
1. **Document zones:** Explicitly define whether the abstract, table notes, footnotes, and figure captions are in scope. (Simplest rule: abstract, main text, and main-text tables including table notes that report computed values are in scope; footnotes, figure graphics, and figure captions are out of scope.)
2. **Repeated numbers and in-text restatements of table values:** Extraction is per **printed occurrence** (token at a location), not deduplicated per underlying statistic. When a table value or sample size `N` is restated in prose, each printed occurrence is extracted at its own locator (so text-versus-table discrepancies are caught), and S2 may link multiple occurrences of the same quantity to one computation.
3. **Multi-number table cells, parentheses, and intervals:** A table cell or text span that prints multiple statistics (such as an estimate and a parenthesised standard error, t-statistic, p-value, or percentage, for example `0.412*** (0.085)` or `24 (18.5%)`) produces one atomic result per number (`estimate` and `se`, or `count` and `percentage`), whereas a two-endpoint range (`[0.12, 0.45]` or `95% CI: 0.12, 0.45`) is one result of `kind: "interval"`. Surrounding parentheses, brackets, and significance asterisks (`*`, `**`, `***`) are stripped from `token`.
4. **Exclusions inside statistical expressions and verbal bounds:** Explicitly exclude significance asterisks (`*`, `**`, `***`), non-numeric prose inferences, confidence levels (`95%` in `95% CI`), nominal alpha cutoffs (`alpha = .05`), model/column index numbers (`(1)`, `(2)`), variable coding constants (`0 = control, 1 = treatment`), and literature cutoff benchmarks (`alpha > .70` rule of thumb). Restrict the verbal-inference `bound` rule in 4.1 ([SPEC.md](model-gating/benchmark/SPEC.md#L172-L174)) to existing frozen labelled claims so extractors only extract explicit printed numeric bounds (such as `p < .001`).
5. **Canonical locator keys:** Free-text paragraph counts and numeric row/column indices do not match mechanically. Require canonical locators: `(exhibit, panel, row_label, col_label, quantity)` for table results (using printed row stub and column header strings) and `(pdf_page, quote, occurrence, quantity)` for prose results.

#### (b) Is the misreading versus hallucination test in 6.4 mechanically decidable?
Not as written in [SPEC.md](model-gating/benchmark/SPEC.md#L454-L466), for two reasons:
1. **Direct contradiction between neighbouring-cell misreading and wrong-referent hallucination:** [SPEC.md](model-gating/benchmark/SPEC.md#L456) defines *"the value of a neighbouring cell"* as a **misreading**, whereas [SPEC.md](model-gating/benchmark/SPEC.md#L458-L459) defines *"or the model attaches a number to a referent the article does not give it"* as a **hallucination** (hard gate). Whenever an extractor shifts a row or column in a table (or swaps two statistics in the same sentence), it attaches a printed number to its neighbour's referent. Without restricting the referent clause, a table alignment slip or referent-field parse mistake triggers the hard gate.
2. **Incomplete edit operations and undefined neighbourhood:** [SPEC.md](model-gating/benchmark/SPEC.md#L455) lists *"a dropped, added or swapped digit"* but omits **single-digit substitution** (for example reading `0.08` for `0.03`, the most common OCR/vision error), and leaves *"at or near"* / *"nearby"* undefined.

Defining the local neighbourhood as the **same paragraph (for prose) or the same row or column of the same table (for tables)**, including single-digit substitution (Damerau-Levenshtein distance $\le 1$ on the digit string) and `%`/proportion scaling in the single-operation predicate, and specifying that misassigning a printed number to another referent within the same paragraph or table is a **misreading** (while citing a referent not present in that paragraph or table, or a token not derivable from any number in that neighbourhood, is a **hallucination**) makes 6.4 completely mechanical.

#### (c) Do the S1 and certificate contracts in 7.2 carry what extraction scoring and `deviation_explanation` need?
Two gaps exist in [SPEC.md](model-gating/benchmark/SPEC.md#L518-L520):
1. **Per-result locators and referents in `claims.json` and `certificate.json`:** [SPEC.md](model-gating/benchmark/SPEC.md#L518) puts `exhibit, printed and PDF page, quote or table cell, referent` at the **claim** level and gives each result only `(result_id, quantity, typed printed value)`. Multi-result claims (such as the six columns of `G-27 C1` to `C5`, or an estimate and SE/p-value in separate table rows or prose sentences) have different table cells, quotes, or model/outcome referents per result. Both 6.1 item 1 (recall per gold number at its location) and 6.4 (per-number location check and certificate uniqueness per location and scientific identity) require each **result** in `claims.json` to carry its own locator and referent (or inherit the claim's values with per-result overrides), and `certificate.json` must carry or reference `result_id` against `claims.json`.
2. **Structured `deviation_explanation` evidence and 6.3 verification:** [SPEC.md](model-gating/benchmark/SPEC.md#L520) requires `deviation_explanation and its evidence` in `certificate.json`, and 6.2 ([SPEC.md](model-gating/benchmark/SPEC.md#L409-L410)) scores explanation accuracy on both `close` and `discrepant` results, but 6.3 ([SPEC.md](model-gating/benchmark/SPEC.md#L435-L438)) only checks slip evidence for `close`. Section 7.2 should specify that `deviation_explanation` is `null` when status is not `close` or `discrepant`, and when it is an identified explanation (`!= "unexplained"`), `deviation_evidence` records the arithmetic operation, donor `result_id` or log path/line, matching companion `result_id`s, or erratum path; and 6.3 should verify that evidence for explained `discrepant` results as well as `close`.

#### (d) Is the `sandbox-exec` approach sound for isolating an agent CLI plus R and Python, and what can it not enforce?
`sandbox-exec` is a viable host-level MAC filter on macOS, but **as described in [SPEC.md](model-gating/benchmark/SPEC.md#L575-L584) it has three concrete holes and four structural limits**:
- **Holes in the drafted profile and proxy:**
  1. **Paths outside `$HOME`:** Denying reads and writes *"in the home directory except..."* ([SPEC.md](model-gating/benchmark/SPEC.md#L577-L578)) leaves `/private/tmp`, `/private/var/folders` (macOS `$TMPDIR`), `/Users`, and `/Volumes` open, allowing cross-run leakage or writes outside `./` (a hard gate at [SPEC.md](model-gating/benchmark/SPEC.md#L479)). The profile must deny `file-write*` everywhere outside `./` (and device nodes `/dev/null`, `/dev/urandom`, `/dev/tty`) and deny `file-read*` in `/Users`, `/Volumes`, `/private/tmp`, and `/private/var/folders` outside `./`.
  2. **Subscription CLI state and token refresh:** Exposing the real `~/.codex` or `~/.claude` directory exposes prior session transcripts (`~/.codex/sessions`, `~/.claude/projects`), violating [SPEC.md](model-gating/benchmark/SPEC.md#L561), while making the token file read-only breaks OAuth token refreshes during long runs. Each stage must set `HOME` and `TMPDIR` to fresh subdirectories inside `./` with a copy of only the auth credential file.
  3. **What a plain HTTP `CONNECT` proxy ("a few dozen lines of Python") cannot do:** Over HTTPS, a `CONNECT` proxy sees only `host:port` (SNI/authority), **not** URL paths, headers, or request bodies. Therefore it **cannot** inject API keys into HTTPS headers ([SPEC.md](model-gating/benchmark/SPEC.md#L565-L566)), **cannot** distinguish an allowed repo from the public `reprocrowd` repo on `github.com` (so raw `github.com` must never be allowlisted), and **cannot** inspect outbound inference payloads to block provider-side `web_search`. For the model provider API, the local proxy must act as an **HTTP reverse proxy** (or TLS-terminating MITM proxy with a trusted local CA) so it can inject API keys and verify/strip `web_search` and URL-fetch tools in the request JSON; for CRAN/Posit/Bioconductor/PyPI/conda, domain-level `CONNECT` allowlisting suffices.
- **What `sandbox-exec` fundamentally cannot enforce (even with a tight profile):**
  1. **No filesystem namespace/remapping:** Read-only system and toolchain paths (`/usr`, `/opt/homebrew`, `/Library`) remain visible at their host locations.
  2. **No nested sandboxes:** The inner CLI cannot call `sandbox-exec` itself (`EPERM`), so Codex/Claude Code must run with its internal sandbox disabled inside the outer profile, and any tool that invokes `sandbox-exec` internally fails.
  3. **No resource limits (RAM, CPU, PIDs, disk quota):** Seatbelt cannot cap memory or CPU; the runner must enforce process-group timeouts, memory limits, and disk checks externally.
  4. **Unix domain sockets unless explicitly blocked:** `(deny network-outbound)` must cover non-system Unix domain sockets (such as `/var/run/docker.sock` or `~/.colima`), or a sandboxed process can talk to a local container daemon.

---

### 3. Judgement on the two `[proposed]` items

1. **Paper score (`extraction_recall * result_credit_average * outcome_factor`, [SPEC.md](model-gating/benchmark/SPEC.md#L397-L400)): AGREE.**
   Because only 5 to 8 claims per paper are labelled while extraction covers the entire paper, an additive score would reward a model that extracts numbers without reproducing them, while omitting extraction recall from the paper score would let a model skip unlabelled tables without penalty. Multiplying `extraction_recall` by the labelled `result_credit` average (and by `1` or `0.5` for the paper outcome) gives the right incentives, bounded in `[0, 1]`, and reduces cleanly to `result_credit * outcome_factor` in decomposed runs where `extraction_recall = 1`.
2. **Isolation via macOS `sandbox-exec` plus a local allowlist proxy ([SPEC.md](model-gating/benchmark/SPEC.md#L575-L584)): AGREE subject to B6.**
   Using `sandbox-exec` plus a local proxy is practical and lightweight on macOS, provided 7.4 incorporates the global write-deny / temp-dir isolation, per-stage `HOME`/`TMPDIR` with copied auth tokens, Unix-socket denial, and an HTTP reverse (or MITM) proxy for the inference endpoint as specified in **B6**.

---

### 4. Blocking changes required

#### B1. Tighten 3.1 scope and canonical locators for mechanical extractor agreement, and restrict verbal bounds in 4.1
- **Location:** [SPEC.md](model-gating/benchmark/SPEC.md#L96-L115) and [SPEC.md](model-gating/benchmark/SPEC.md#L172-L174).
- **Replace [SPEC.md](model-gating/benchmark/SPEC.md#L96-L115) with:**
  ```markdown
  **Scope.** Every printed number in the abstract, main text and main-text tables (including table
  notes that report computed values) that reports a result computed from the data: descriptive
  statistics, sample sizes, test statistics, estimates, standard errors, intervals, p values, effect
  sizes and model-fit statistics. Excluded: numbers that describe the design rather than results
  (scale points, number of conditions, payment amounts, variable codings), confidence levels (`95%` in
  `95% CI`), nominal significance thresholds (`alpha = .05`), model or column indices, literature
  cutoffs, significance asterisks (`*`, `**`, `***`), prose inferences without an explicit printed
  number, dates, page and reference numbers, footnotes, figure captions, and values that appear only
  graphically in figures. Supplements are out of scope for now.

  **Occurrences and cells.** Extraction is per printed occurrence: an in-text restatement of a table
  value or a repeated sample size is extracted at each location where it is printed (and may share one
  computation in S2). A table cell or text span that prints several statistics (such as an estimate
  and a parenthesised standard error, t statistic, p value or percentage) produces one result per
  number, with surrounding parentheses, brackets and significance asterisks stripped from `token`; a
  two-endpoint range is one `interval` result (3.2).

  **Gold extraction.** Each gold paper gets an exhaustive extraction of these numbers, with canonical
  locator (`exhibit`, `panel`, `row_label`, `col_label` and `quantity` for tables; `pdf_page`, `quote`,
  `occurrence` and `quantity` for prose), referent and typed value (3.2). Two extractors work
  independently; their lists are matched mechanically by canonical locator and normalised token, and
  every difference is adjudicated. Extraction is scored by recall and precision against this list, so
  a model gains nothing by listing numbers that are not there and loses for skipping any.

  **Labelled results.** The existing gold claim lists (5 to 8 claims per paper, chosen from results the
  human source assessed) remain the labelled subset: these numbers carry a reproduction status. They
  are a subset of the extraction. A model reproduces every number it extracts; the numbers without a
  gold label are reported as diagnostics, and its discrepancies on them go to adjudication, which is how
  the labelled set grows. Each claim in the gold extraction also records whether it is **primary** (a
  main-text focal hypothesis test or headline estimate; not sample descriptives, manipulation checks or
  robustness tables).
  ```
- **Replace [SPEC.md](model-gating/benchmark/SPEC.md#L172-L174) with:**
  ```markdown
  Where a frozen labelled claim includes a threshold stated in words (for example "significant at the
  5% level"), it is represented in gold as a separate result of kind `bound` and judged separately, so
  a rounded value can match while the stated inequality is false. Verbal inferences without an explicit
  printed bound (`p < .05`) are not part of the exhaustive extraction in 3.1.
  ```

#### B2. Make the misreading versus hallucination test in 6.4 mechanically decidable
- **Location:** [SPEC.md](model-gating/benchmark/SPEC.md#L454-L469).
- **Replace [SPEC.md](model-gating/benchmark/SPEC.md#L454-L469) with:**
  ```markdown
  - **Misreading:** the article prints a number in the local neighbourhood (the same paragraph for
    prose, or the same row or column of the same table for tables) and either (a) at the stated
    location the model's token is derived from the printed number by one transcription operation (a
    misplaced or dropped decimal point or thousands separator, a dropped, added, substituted or
    adjacent-swapped digit, a lost or added minus sign, or a 100x percentage-proportion scale slip), or
    (b) the model reports the exact token of another number in that neighbourhood or attaches a number
    printed in that neighbourhood to another referent in the same paragraph or table. A misreading
    counts as not extracted, its reproduction result earns no credit, and misreadings are counted.
  - **Hallucination:** the model's token cannot be derived by one such transcription operation from any
    number printed in the local neighbourhood, or the model attaches a number to a referent (outcome,
    predictor or sample) that does not appear in that paragraph or table. **One verified hallucination
    is a hard gate.** A system that invents printed values cannot be trusted to check a paper.
  - **Gold miss:** the article does print the number in scope (3.1) and the gold extraction missed it.
    The gold is corrected (versioned) and the model credited.

  The evaluator decides between misreading and hallucination mechanically from the local neighbourhood
  text and the transcription predicate above, recording both. Numbers outside the scope of 3.1 (dates,
  design parameters, indices) that the article does print are ignored in 6.1 and 6.4. Recomputed
  values, diagnostics and intermediates are not printed values and are never treated as fabrication.
  The certificate has one final result per canonical location and scientific identity; any duplicate
  makes it invalid.
  ```

#### B3. Put locators and referents at the result level in 7.2 and specify `deviation_explanation` evidence checking in 6.3 and 7.2
- **Location:** [SPEC.md](model-gating/benchmark/SPEC.md#L435-L438) and [SPEC.md](model-gating/benchmark/SPEC.md#L518-L520).
- **Replace [SPEC.md](model-gating/benchmark/SPEC.md#L435-L438) with:**
  ```markdown
  - **`close`, and explained `discrepant`.** Whenever `status` is `close` or `deviation_explanation` is
    not `unexplained`, the named slip must be demonstrated from the bundle and the execution output
    (4.2): truncation or digit transposition applied to the recomputed value, the donor value in the
    executed output, an erratum in the bundle, or a single-character substitution with matching
    companion statistics. On a `discrepant` result, an unverified explanation is scored as invalid in
    6.2 without invalidating the `discrepant` status in 6.1.
  ```
- **Replace [SPEC.md](model-gating/benchmark/SPEC.md#L518-L520) with:**
  ```markdown
  | S1 extract | input bundle, article, package | `claims.json`: every reported number in scope (3.1), grouped into claims; per claim `claim_id`, wording, `primary`, and its results (`result_id`, `quantity`, canonical locator (`exhibit`, `panel`, `row_label`, `col_label` or `printed_page`, `pdf_page`, `quote`, `occurrence`), `referent` (`study`, `sample`, `outcome`, `predictor`, `model`, `wave`, `statistic`), typed printed value) |
  | S2 reproduce | input bundle, article, package, `claims.json` | `results.json` and `s2-workspace/`: per result, state (completed, blocked, ambiguous, failed, timed out), recomputed value (unrounded and as emitted), execution (script path and hash, lines, command, exit status, log paths, lockfile), ordered fixes with diff paths, method choices with article quotes (Track B), variation runs (setting, value, log path) |
  | S3 judge | everything above | `certificate.json` (schema 1.2): per result `claim_id`, `result_id`, locator and typed printed value (matching `claims.json`), `status`, `basis`, claim outcome, comparison, `deviation_explanation` (`null` unless `close` or `discrepant`) and `deviation_evidence` (recomputed operation, donor `result_id` or log path and line, matching companion `result_id`s, or erratum path; `null` when `unexplained`), blocker evidence, `severity`, `printed_match`; paper outcome and findings |
  ```

#### B4. Reconcile 4.6 paper outcome between the frozen gold baseline scope and full-paper model assessment
- **Location:** [SPEC.md](model-gating/benchmark/SPEC.md#L304-L318).
- **Replace [SPEC.md](model-gating/benchmark/SPEC.md#L304-L318) with:**
  ```markdown
  Before targets are scheduled, each paper's baseline gold outcome is computed over its frozen labelled
  scope, after removing held and (Track B) ineligible results, together with a non-empty primary
  subset. A target with no scored labelled claims or no assessable primary result is not scheduled. For
  Track B, `input-bundle.json` lists any studies or cohorts in the article whose data are not part of
  the package, and their results are excluded from S2/S3 assessment.

  - **Computationally reproducible:** every assessed result is `match`, `close` or `within_variation`.
    One-unit reporting slips (`close`) are listed separately in the certificate; they do not make the
    computation fail. An explained but larger deviation is `discrepant` and does.
  - **Technical failure:** demonstrated study blockers prevent every primary computation.
  - **Computational issues:** at least one primary computation completes, and an assessed result is
    `discrepant` or `not_checkable`.

  The model's paper outcome draws on every in-scope result it extracts and assesses. If it differs from
  the baseline gold outcome only because of a held gold result or a result outside the labelled subset
  whose `discrepant` or `not_checkable` judgement passes the evidence checks in 6.3, the model's paper
  outcome counts as correct; such cases go to adjudication and, if confirmed, extend the labelled set.
  ```

#### B5. Restore the definition of `severity` (`P0`, `P1`, `P2`) in 4.2 and add `deviation_explanation` to 5.1
- **Location:** [SPEC.md](model-gating/benchmark/SPEC.md#L194-L202), [SPEC.md](model-gating/benchmark/SPEC.md#L334-L338), and [SPEC.md](model-gating/benchmark/SPEC.md#L354).
- **Append to [SPEC.md](model-gating/benchmark/SPEC.md#L201) (end of the **Explanation field** paragraph in 4.2):**
  ```markdown
  Each result also carries `severity`: `P1` for a `discrepant` result that triggers a veto above (flipped
  sign, crossed null or threshold, or false bound), `P2` for any other `discrepant` result, `P0` for a
  `not_checkable` study blocker, and `null` for `match`, `close` and `within_variation`.
  ```
- **Replace [SPEC.md](model-gating/benchmark/SPEC.md#L334-L338) with:**
  ```markdown
  | G-21 C3, C4, C5 | match | discrepant, P2, `other_identified`; scoring reference replaced by the executable fixed-effects output, mixed-effects values kept as diagnostics | Documented-but-unrun option (4.4); Sol r1 checked the pinned script |
  | G-08 C4 | close | close, `truncation` | Truncation; independent rerun 0.1980 |
  | G-08 C6 | match | match, expected basis `justified_fix` (`skip_failing_statement`) | An earlier statement errors before the follow-up models |
  | G-18 C1 | close | close, `transposed_cells` (C2 stays discrepant, P2, `transposed_cells`) | Paired transposition; .012 violates C2's printed bound |
  | G-22 C1 | close | close, `truncation` | Truncation (.07849 printed as .07), demonstrable from the recomputed value |
  ```
- **Replace [SPEC.md](model-gating/benchmark/SPEC.md#L354-L355) with:**
  ```markdown
  exception is the version-recovery rule in 4.3. Every gold result gets a `primary` flag, a
  `deviation_explanation` record (null unless `close` or `discrepant`) and a `nondeterminism` record
  (null when deterministic). Paper outcomes are recomputed under 4.6 after the
  ```

#### B6. Tighten the `sandbox-exec` profile and local proxy specification in 7.4
- **Location:** [SPEC.md](model-gating/benchmark/SPEC.md#L575-L584).
- **Replace [SPEC.md](model-gating/benchmark/SPEC.md#L575-L584) with:**
  ```markdown
  **Implementation [proposed].** On this Mac the lightest option is the built-in macOS sandbox
  (`sandbox-exec`, the mechanism Codex itself uses), not a container runtime. A profile per stage
  attempt denies `file-write*` everywhere except the stage directory `./` and standard device nodes
  (`/dev/null`, `/dev/urandom`, `/dev/tty`), denies `file-read*` across `/Users`, `/Volumes`,
  `/private/tmp` and `/private/var/folders` except `./` and the read-only package library, and denies
  non-system Unix domain sockets and all outbound TCP/UDP except the local proxy. Each stage sets
  `HOME` and `TMPDIR` to subdirectories inside `./`, with a copy of only the executor's login token
  placed in the stage `HOME` so prior CLI session logs are unreachable and token refreshes stay inside
  `./`. The proxy acts as a local HTTP reverse proxy (or TLS-terminating proxy with a stage CA) for the
  model provider's inference endpoint (injecting API keys and verifying that provider-side `web_search`
  and URL fetching are off in the outbound request JSON) and as a domain-allowlisted `CONNECT` proxy for
  CRAN, Posit Package Manager, Bioconductor, PyPI, conda and evaluator mirrors (never raw `github.com`).
  Because `sandbox-exec` does not cap memory or CPU and cannot nest sandboxes, the runner enforces
  process-group timeouts and memory limits on the host and runs Codex with its internal sandbox
  disabled. A test on 1 November 2026 confirmed that R runs and loads packages from the shared library
  under such a profile, while reading a gold file and opening a direct connection to CRAN both fail.
  Still to verify: an agent CLI running inside the profile and its API traffic through the proxy.
  Containers (Docker or Colima, or Apple's `container` tool) remain the fallback, and Linux hosts would
  use `bubblewrap`.
  ```

---

### 5. Non-blocking changes

1. **NB1. Interval closeness in 4.2 ([SPEC.md](model-gating/benchmark/SPEC.md#L184-L186)):** Add one clause stating how `close` applies to intervals.
   - **Replace [SPEC.md](model-gating/benchmark/SPEC.md#L184-L186) with:**
     ```markdown
     - **closeness:** the printed value is one unit away, in its last printed digit, from the correctly
       rounded recomputed value (for example .07849 printed as .07 instead of .08); for an interval, at
       least one endpoint is one unit away in its last digit and the other either matches or is one unit
       away. Counts must be exact; a wrong count is never `close`.
     ```
2. **NB2. Extraction precision denominator and gold-claim outcome aggregation in 6.2 ([SPEC.md](model-gating/benchmark/SPEC.md#L406-L407)):** Clarify that out-of-scope numbers printed in the article (ignored by the 6.4 gate) still count in the denominator of diagnostic extraction precision, and that 6.2 claim outcome accuracy is evaluated per frozen gold labelled claim over its mapped results.
   - **Replace [SPEC.md](model-gating/benchmark/SPEC.md#L406-L407) with:**
     ```markdown
     - extraction recall and precision (where misreadings and out-of-scope printed numbers count against
       precision), and the number of misreadings;
     - three-way claim outcome accuracy (4.5, evaluated per labelled gold claim from its mapped results)
       and the binary version (reproduces vs does not);
     ```

VERDICT: AGREE subject to the blocking changes listed
