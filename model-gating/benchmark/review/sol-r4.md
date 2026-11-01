# Specification review, Sol, round 4

Draft 0.5 at commit `6c914fb` implements the three settled rulings in substance. I found no surviving selection requirement or numerical contradiction in the three requested gold cases. Agreement requires the operational clarifications below, particularly because an extraction classification can now zero an entire paper. None reopens a settled ruling.

I reviewed the commit diff, all sections of the specification, the round 3 reviews, and the relevant gold records. I checked the three rounded differences using decimal arithmetic and consulted primary implementation sources for the isolation proposal. I did not run paper analyses or reproduce the reported sandbox experiment. Only this review file was written.

## Blocking changes

### 1. Define the extraction unit and freeze its denominator

Section 3.1 identifies the statistical quantities well, but two extractors cannot yet determine the same list from its counting rules. Independent extraction and adjudication resolve disagreements; they do not replace a rule for what counts (`model-gating/benchmark/SPEC.md:96`, `:102`). Add a short convention:

> Extract each in-scope printed occurrence at its own location, including every eligible table cell and each statistic within a cell. Parentheses do not exclude a statistic: an estimate and its parenthesised SE are separate results. An interval remains one result with two endpoints. Repeated values at different locations, including an in-text restatement of a table value, are separate extraction occurrences; their computation may be shared. Repeating the same location and scientific identity in the submission is a duplicate.

This follows the existing location-based mapping and duplicate rule (`model-gating/benchmark/SPEC.md:118`, `:138`, `:469`). It avoids either deduplicating unrelated equal numbers or requiring repeated execution of the same analysis. Large tables receive no cap or sampling exception. Sample sizes, SEs, and other in-scope statistics remain included wherever printed; row identifiers and design constants remain excluded.

Also state whether “main text” includes the abstract, captions, and table notes, and explicitly include the verbal inferential bounds required by section 4.1 (`model-gating/benchmark/SPEC.md:96`, `:172`). A confidence level identifying an interval is not another data-derived result merely because it contains a number. These are boundary clarifications, not grounds for narrowing exhaustive extraction.

Freeze the adjudicated extraction list and its version with the scoring inputs before candidate runs (`model-gating/benchmark/SPEC.md:384`). Clarify that holding a reproduction label, or excluding it from Track B assessment, does not remove an otherwise in-scope occurrence from extraction recall (`:304`, `:328`, `:386`). When a gold miss changes the denominator, version the correction and rescore all affected submissions, rather than crediting only the submission that exposed it (`:461`).

### 2. Make misreading and hallucination mutually exclusive

The present test is not sufficiently decidable or fair for a one-instance gate. A neighbouring-cell value is explicitly a misreading, but assigning it to the target row also satisfies “attaches a number to a referent the article does not give it”. “At or near” has no fixed boundary. Finally, a genuine transcription error requiring two operations becomes a hallucination solely because one operation cannot derive it (`model-gating/benchmark/SPEC.md:454`, `:458`, `:464`). That last restriction is stronger than the settled distinction between transcription and invention.

A lean repair is to classify the source before the token difference: after the permitted typography normalisation, a uniquely identifiable printed target whose token was transcribed incorrectly is a misreading, including evidenced adjacent-cell copying and compound transcription errors. Record the source cell or span and the error. A claimed printed target unsupported by the cited source is a hallucination, verified against the article before the hard gate applies. State that the adjacent-cell exception takes precedence over the wrong-referent clause, and replace “near” with the explicitly recorded source span or neighbouring cell. Do not infer the model's intent.

Use the same normalisation in sections 3.3, 6.1, and 6.4. Otherwise typography accepted during mapping can fail “exact printed token” extraction, and standardising thousands separators conflicts with treating their displacement as a transcription error (`model-gating/benchmark/SPEC.md:140`, `:386`, `:453`). Preserve numerical meaning, precision, signs, and inequality operators; numerical changes remain errors. This keeps one verified hallucination as a hard gate and leaves misreadings with the settled recall and credit penalties.

### 3. Complete the numerical predicate for `close`

The scalar rule correctly measures distance from the correctly rounded value, rather than the unrounded reference. “One unit” and “at most one unit” are consistent once `match` takes precedence (`model-gating/benchmark/SPEC.md:153`, `:184`). State that precedence and add the interval counterpart:

> After unit conversion, each interval endpoint must either match or differ by no more than its own printed quantum from its correctly rounded reference; at least one endpoint must differ. The identified slip and all vetoes still apply.

Without this sentence, section 4.2 does not specify how its singular “last digit” applies to the endpoint arrays already required elsewhere (`model-gating/benchmark/SPEC.md:167`, `:191`, `:510`). Retain exact counts and the false-bound veto. Make the explanation-evidence list explicitly include demonstrable truncation or misrounding, as section 6.3 already does, so its examples cannot be read as requiring companion statistics for every truncation (`:187`, `:197`, `:435`). `unexplained` needs evidence of the discrepancy, not evidence of an identified cause.

The requested cases pass, conditional on the in-bundle execution evidence required before freezing labels:

- **G-08 C4:** printed `0.19`, reference `0.198`, correctly rounded `0.20`, quantum `0.01`. The rounded difference is one unit and truncation yields `0.19`. The independent base-run record corroborates the reference (`model-gating/gold-set/gold/G-08.json:123`; `model-gating/gold-set/twins/README.md:54`). Keep `close` in section 5.1 (`model-gating/benchmark/SPEC.md:335`).
- **G-18 C1:** printed `.01`, reference `.004`, correctly rounded `.00`, quantum `.01`. One unit. The donor `.012` rounds to `.01`, supporting the paired transposition; the companion C2 remains `discrepant` because `.012` violates `< .01` (`model-gating/gold-set/gold/G-18.json:39`, `:59`, `:62`; `model-gating/benchmark/SPEC.md:337`). This is partial eta-squared, not a p value.
- **G-22 C1:** printed `.07`, reference `.07849`, correctly rounded `.08`, quantum `.01`. One unit and demonstrable truncation (`model-gating/gold-set/gold/G-22.json:241`; `model-gating/benchmark/SPEC.md:338`). C2/C3 correctly become `discrepant`: the intercept differs by more than one unit, and the interval's lower endpoint does too, although its upper endpoint differs by only one unit (`model-gating/gold-set/gold/G-22.json:264`, `:287`; `model-gating/benchmark/SPEC.md:339`).

For p values, apply the same scalar quantum rule, with no extra relative tolerance. A printed `0.000` remains a scalar; an inequality is tested against the unrounded value, and a relied-on threshold crossing remains `discrepant` (`model-gating/benchmark/SPEC.md:169`, `:191`). For percentages, convert to the printed unit first: a quantum of one percentage point is `0.01` on a proportion scale, not one whole proportion unit (`:131`, `:160`). These existing rules are sound; the interval clarification completes them.

### 4. Make sandbox acceptance enforce the whole isolation policy

**Agree in principle with macOS Seatbelt plus an external allowlist proxy, subject to verification.** The proposed home-directory denial is not equivalent to section 7.4's general boundary: it leaves unspecified reads and writes elsewhere, including shared temporary directories and other volumes (`model-gating/benchmark/SPEC.md:559`, `:577`). Require default-denied access with explicit runtime, read-only input/library, login-token, and fresh writable stage exceptions. Keep earlier-stage artefacts read-only even when located beneath the stage directory. Launch the whole executor and its descendants inside that boundary with a clean environment and fresh configuration/session state.

This approach is technically credible: the primary [Codex Seatbelt base policy](https://github.com/openai/codex/blob/main/codex-rs/sandboxing/src/seatbelt_base_policy.sbpl) starts with default denial and permits child execution under the inherited policy; its [network implementation](https://github.com/openai/codex/blob/main/codex-rs/sandboxing/src/seatbelt.rs) supports exceptions for specific loopback proxy ports. That does not establish that the proposed benchmark profile is equivalent.

Before ranking use, retain a small acceptance test and its profile/proxy hashes in the run record. It must demonstrate:

- The actual agent CLI, subprocesses, R/Python, package installation, inference, and any required login refresh work without widening host access. Verify the executor's sandbox configuration rather than relying on a universal assertion about nesting (`model-gating/benchmark/SPEC.md:581`).
- Gold, reports, previous runs, Track B code, host configuration, and out-of-stage writes are blocked, including through symlinks, shared temporary paths, inherited file descriptors, and unapproved local services. Earlier-stage inputs and the shared library cannot be changed.
- Removing proxy environment variables does not enable direct IPv4/IPv6 traffic. Only the designated proxy is reachable, not arbitrary loopback ports or local sockets. The proxy rejects forbidden destinations, redirects to them, and arbitrary GitHub fetches; approved mirrors supply dependencies only. Provider-side browsing remains disabled and verified (`model-gating/benchmark/SPEC.md:562`, `:569`).
- HTTPS inference and package traffic are handled and logged outside the stage. A CONNECT tunnel alone cannot inject an API key into an encrypted request or enforce its path; use a suitable TLS-terminating proxy or inference broker where those controls are required. The primary [Codex proxy documentation](https://github.com/openai/codex/blob/main/codex-rs/network-proxy/README.md) likewise distinguishes host filtering from HTTPS method/path controls requiring TLS interception.

The reported R/gold-read/direct-CRAN test is useful but insufficient for these boundaries (`model-gating/benchmark/SPEC.md:579`). The existing diagnostic-only fallback is appropriate until acceptance passes (`:573`). The specification needs the acceptance condition, not a large security framework or a promise that the proxy fits in a few dozen lines.

## Proposed score and consistency audit

**Recall multiplication: agree as a deliberate completeness penalty**, once the extraction denominator is fixed. The unweighted paper mean means a table-heavy paper has the same total headline weight as another paper, rather than receiving weight proportional to its number of cells (`model-gating/benchmark/SPEC.md:397`, `:401`). Dense tables and repeated occurrences do affect what dominates recall within a paper, so the occurrence convention above is necessary.

Add one interpretive sentence: labelled omissions are penalised in both factors. Result credit already assigns zero to a missed labelled result; multiplying by recall adds a further penalty (`model-gating/benchmark/SPEC.md:386`, `:394`). When omissions alone make both extraction recall and result credit equal `r`, the paper factor is `r²` before the outcome multiplier. The product is therefore not simply the fraction of labelled results successfully checked. This is defensible for the stated spell-checking goal. Report the existing recall, precision, and misreading diagnostics with extraction counts so paper density remains visible (`:406`). No alternative headline or cap is needed.

Across **sections 1, 3, 4, 5.1, 6, 7, and 8**, exhaustive extraction, the separate labelled subset, numerical closeness, mandatory deviation explanations, and the single-hallucination gate are consistently carried through (`model-gating/benchmark/SPEC.md:15`, `:108`, `:194`, `:335`, `:448`, `:518`, `:600`). Explanation accuracy is explicitly diagnostic, so a wrong explanation for an otherwise correctly classified `discrepant` result does not currently remove headline credit (`:388`, `:409`); that is consistent with requiring an explanation field without separately scoring its correctness.

I found no leftover **must-check**, submission **cap**, **extra claims**, or **selection reason** requirement in `SPEC.md`. The “5 to 8” wording describes the retained labelled subset, not a model selection task (`model-gating/benchmark/SPEC.md:108`). The remaining uses of selection concern variation protocols, not claim selection. Section 8 correctly treats exhaustive gold, schemas, evidence scoring, and runner isolation as work still to implement, rather than claiming the current pilot already complies (`:590`, `:600`, `:603`, `:608`).

VERDICT: AGREE subject to the blocking changes listed
