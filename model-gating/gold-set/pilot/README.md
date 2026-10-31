# Feasibility pilot: the real prompt on three gold papers

A smoke test of the full loop: run the ReproCrowd prompt, collect `certificate.json`, and score it
against the gold set. It is not a benchmark result. There are three papers per configuration.
Scores are against gold v1.3, in which G-08 is again `computationally reproducible` (see point 2).

**Setup.** Prompt v0.1.0, unchanged, with the article DOI and code link filled in. Two
configurations: GPT-6.1 Sol (Codex, high reasoning) and Claude Opus 5.5 (Claude Code). Each paper got
a fresh agent in an isolated workspace, with no access to the gold files. Agents were told not to
read existing reproduction reports and to treat their own claim list as approved. Papers: G-08
(gold: reproducible), G-21 (issues) and G-23 (technical failure). Files:
`runs.csv`, `{sol,claude}/G-xx-certificate.json` (plus `certificate.md` where written) and
`scores.json`. Rescore with:

```sh
python3 model-gating/scripts/score_certificate.py model-gating/gold-set/pilot/runs.csv
```

## Scores against gold v1.3

Rescored on 31 October 2026 against gold v1.3, with `match` and `close` as distinct outcomes.
The distinction mainly costs Sol, whose certificates use `close` where gold has `match`. The pilot certificates follow schema 1.0 (no `basis` field) and are checked against
the archived schema in `../../schemas-archive/`.

| | Sol | Claude |
|---|---|---|
| Paper status correct | 1/3 | 2/3 |
| Certificates failing the schema | 1 (G-23) | 0 |
| Gold claims found in the certificate | 11/16 | 16/16 |
| Claim outcome correct (reproduces vs does not) | 10/16 | 12/16 |
| Claim status correct | 6/16 | 12/16 |
| Specificity (no false discrepancy) | 11/11 | 10/11 |
| Sensitivity, P1+P2 | 0/2 | 2/2 |
| Blocked claims reported as not reproducing | 0/3 | 0/3 |
| Hard-gate violations | 0 | 3 (G-23 C1, C2, C5) |

With three papers, these numbers say nothing about model quality. They show that the scorer works
and where the protocol breaks.

## What the pilot showed

1. **The prompt's rule-pack and schema URLs were dead.** `lukasroeseler.github.io/reprocrowd/...`
   returned 404; the site lives at `forrtproject.github.io/reprocrowd/`. Agents that were told the
   correct URL produced schema-valid certificates. The one that was not (Sol, G-23) fell back to its
   own format and invented the status "PartiallySupported". This is fixed in the repository
   (prompt v0.1.1, deployed).
2. **Both models flagged G-08 numbers that, on closer reading, are not errors.** Both runs
   reported that the durability paragraph prints the one-week pardon effect as b = 0.20, p = .16
   while the code gives 0.31, p = .004, and that 13.14% should be 13.33%. The paragraph never
   says "one week": 0.20/.16 is exactly the 24-week estimate, the only wave that is no longer
   significant. 13.14% is exactly 18/137, and the right denominator cannot be determined. Gold
   v1.1 had adopted both findings; v1.3 reverses them, so the I4R report's verdict stands. Models
   and labellers alike over-read plausible discrepancies.
3. **The pilot also corrected gold elsewhere.** Claude's G-23 run showed that two claims labelled
   blocked (C3, C4) are computed by the shipped code. A check confirmed this: C3 matches, and C4 is
   a transcription error (W = 1137.5 printed as 1037.5).
4. **Both models "repaired" analyses, openly, and still labelled the result as recurring.** Sol
   reached G-21's printed AIC (1722) only by swapping in the mixed-model specification that a code
   comment describes, then called it `close`; unchanged code gives 1766. Claude wrote the missing
   Group 2 code for G-23 itself and labelled those recreated results `match`. Both said so in notes,
   but the certificate has no field that separates rerun from recreated values, so a reader of the
   status alone is misled. This is the failure mode the benchmark is meant to catch, and it appeared
   in two of six runs.
5. **Neither model reported a blocked claim as not reproducing.** No run marked a blocked gold
   claim `not_checkable` or `discrepant`; Sol's G-23 format simply lacked the vocabulary.
6. **Certificates vary hugely in granularity.** They range from 17 to 225 claims and from 30 to 698
   results. Mapping certificate results to gold claims by printed value worked for every
   schema-valid certificate once the scorer handled repeated claim ids and numbers inside structured
   values.
7. **Unsupported assertions slip in.** Claude's G-23 certificate states that Figshare v1 and v2 hold
   byte-identical files; the Figshare API shows the scripts differ.
8. **The bundle requirements are heavy.** Every run installed pixi locally. MyST was never built,
   no nanopublications were minted, and one run certified numbers from host R rather than the pixi
   environment. Runs took 12 to 17 minutes for Claude on these small packages.
9. **Status judgements diverge where the rules are vague.** On G-08, Sol chose `technical failure`
   because a figure script crashes, although every number recurs. Claude chose
   `computational issues`.
