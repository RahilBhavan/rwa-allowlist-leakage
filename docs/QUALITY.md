# Quality review

Rounds are listed newest first. The dashboard reads the current scores from [`QUALITY.json`](../QUALITY.json). The round-1 gap list is in the version of `QUALITY.json` committed at `af9e1bd`, and the round-2 gap list in the version committed at `c7cb413`.

## Round 3 (final)

- Rubric version: 1
- Reviewed head: `6f4b801dd43d47050c46e234c889512ce0b9519c`. This is a clean tree, identical to `origin/main` at review time (confirmed with `git ls-remote`).
- Reviewer: claude-opus-5-5. The builder was GPT-6.2 Sol and the orchestrator GPT-6.2 Astra, so the reviewer comes from a different model family. This round started fresh: every check was rerun and the mutation probe was new.
- Reviewed at: 2026-11-27T04:39:56Z
- Scope: authority in BRIEF.md only. The review used keyless public RPC and Horizon reads, public web and SEC pages, and local files. It did not post, push, commit, contact anyone, send transactions, use API keys or paid APIs, use Tenderly or set timers. It changed only `QUALITY.json` and this file. All work ran in a task-owned scratch clone on disk, and the live replay ran through the maintainer's workload gate.

### Scores

| Dimension | R1 | R2 | R3 | One-line reason |
| --- | ---: | ---: | ---: | --- |
| Answer | 6 | 8 | 9 | The lead now gives both verdicts: direct 0.94–62.20% (unresolved) and custody-inclusive at least 6.74% (above 5%). The $15.03m dust-free amount sits beside $86.67m. It is dense and does not say what the 6.74% is conditional on. |
| Evidence | 8 | 9 | 8 | The dust rule is derived from pinned fee and output, the layer table covers every material claim, and every traced number matched. The new November Stellar BENJI sum is 1.98× the September fund share count and 1.59× October's, with no reconciliation. |
| Reproducibility | 9 | 10 | 10 | A clean clone reproduces every output on Python 3.9–3.14. All 20 checksums match, the PDF check passes 15/15 with publisher hashes verified, and the gated live replay matched 696/696 reads with zero errors. |
| Usefulness | 7 | 8 | 9 | The shortfall table ($372.28m / $210.41m) and ranked candidate lots make the unresolved result actionable. The featured crossing combination leans on a charity donation wallet. |
| Completeness | 7 | 8 | 9 | Current Stellar and Solana reads, pinned Safe thresholds and modules, the Crypto Relief attribution and Nest terms were added. The Nest September transfer controls were never read at the pin. |
| Documentation | 7 | 8 | 8 | The HOLDERS table is fixed and a table-shape test was added. 209 links and anchors resolve. STATE and HANDOFF again describe the slice as uncommitted, HANDOFF lost the brief's DONE / PARTLY DONE / NOT DONE headings, and REACH contradicts HOLDERS on the Crypto Relief Safe. |
| Post kit | 5 | 8 | 9 | Four one-claim drafts, each linked to a RESULTS anchor. The 12-word card passes its checker and the orphan chart is gone. The Flux draft's scope ('a loan backed by OUSG') is left open. Design approval is Rahil's. |
| Code | 7 | 7 | 8 | All 13 round-2 guards plus the card, PDF and replay modules are now tested, and the 8 builder mutants I re-probed are killed. In a fresh probe, 24 of 36 new mutants survive, including one that silently changes the published floor and slack figures. |
| **Overall (lowest)** | **5** | **7** | **8** | Evidence, documentation and code set the overall score. |

### What I ran

| Command or check | Result |
| --- | --- |
| Clean clone into a task-owned scratch directory on disk and check out `6f4b801` | OK. `git ls-remote origin` shows `refs/heads/main` = `6f4b801…`. |
| `sha256sum -c evidence/SHA256SUMS` | 20/20 OK |
| `python3 -m unittest discover -s tests` on 3.14.8, 3.12, 3.10 and 3.9 | 40/40 pass on all four |
| `python3 scripts/holder_audit.py` | Exit 0 |
| `python3 scripts/kill_test.py` | Exit 0. Direct $86,669,353.88, 0.94421–62.19969%, `inconclusive`, shortfall $372,283,540.93. Custody-inclusive $619,366,062.06 (pinned $241,931,783.06 + attested $377,434,279), lower 6.7476%, `continue`. Pinned-only custody 2.6357%. Dust-free direct $15,032,143.93, custody 5.967%. BUIDL scenario: ceiling $5,941,489,570.40, direct 1.4587–41.602%, shortfall $210,405,124.64. Frax: 1.328% / 7.132%. Bridge balances are all zero. These agree with README, RESULTS, STATE, HANDOFF and the drafts under the stated rounding. |
| Spot arithmetic of the new tables | Exclusion to get below 5%: 0.95 × 9,179.06 − 3,469.71 = 5,250.39, and 0.95 × 5,941.49 − 3,469.71 = 2,174.70. Combinations: 119.32 + 112.91 = 232.23, + 26.47 = 258.70, and 119.32 + 26.47 + 182.60 = 328.39. Floor ratio: 86.67 / 4,907.25 = 1.77%. All match. |
| `python3 scripts/check_post_card.py` | Pass. 12 words, with HTML and PNG hashes matching the receipt. |
| `python3 scripts/verify_pdf_facts.py` (downloads into ignored scratch `data/upstream/`) | 15 checks pass. All three publisher hashes verified. |
| `workload_budget.py run -- python3 scripts/replay_evidence.py --workers 1` | Exit 0. 696 match, 0 mismatch, 0 error across 10 fixtures: EVM 64, holders 437, Ethereum review 115, signer 1, BNB receipt 3, XRPL 5, round-1 supplement 28, round-2 readbacks 18, discovery 23 and Usual source 2. This reproduces the builder's 696. The reservation was released on exit. |
| Horizon `/assets?asset_code=BENJI&asset_issuer=GBHN…ZIW5` | 1,325,203,536.85 authorized + 25.13 unauthorized across 1,406 + 1,170 = 2,576 accounts, which matches the fixture. |
| Franklin N-MFP3 for 2026-10-31 (accession `0002071691-26-025490`, filed 2026-11-06) | Series S000067043, class C000215714, one class. B.4 is $833,554,415.30 and B.5 is 833,590,155.07 shares. That is below the November Stellar trust-line sum (see Evidence). |
| `cryptorelief.in/donate` | Lists `0x68A99f89E475a078645f4BAC491360aFe255Dff1`, the BUIDL-I rank-2 Safe, as claimed. |
| Relative Markdown links and anchors (including this repo's GitHub `main` URLs) | 209 links, 0 broken |
| Scan for private paths, credentials, paid providers and named individuals | None in the public tree. Endpoints are keyless public RPCs and explorers. Crypto Relief is an organization. |
| Re-probe of 8 of the builder's 15 listed mutants (Curve quote/inventory, parentHash, USST cap, bridge balance, Franklin share-class count, PNG link, dust fee rule, USDtb pool > supply) | 8/8 killed, as claimed |
| Fresh mutation probe: 36 new single-line mutants across `kill_test.py`, `check_post_card.py`, `verify_pdf_facts.py` and `replay_evidence.py` | 12 killed, 24 survived. Of the survivors, 4 change `kill_test.py` output and 20 are guards that no test trips. Details are under Code. |

### Round-2 gaps: status

| # | Round-2 gap | Status at `6f4b801` |
| --- | --- | --- |
| 1 | Code: 15 surviving guard mutants; card checker, PDF verifier and replay comparator untested | **Fixed as specified.** Every named guard has a corrupted-copy case, the bridge guard now raises, and three new test modules exercise the checker, verifier and comparator. A fresh probe still finds untested guards (round-3 gap). |
| 2 | Usefulness: nothing showed what would move the direct verdict | **Fixed.** Shortfall table, ranked candidate lots and combinations. The featured combination relies on a donation wallet (round-3 nit). |
| 3 | Answer: lead counted the dust lot and gave no verdict | **Fixed.** Both verdicts and the $15.03m dust-free amount are in the lead. |
| 4 | Documentation: broken HOLDERS table; stale STATE/HANDOFF; no table check | **Partly fixed.** The table is fixed and a column-count test was added. STATE/HANDOFF are stale again, now for `6f4b801` (round-3 gap). |
| 5 | Post kit: drafts 2–4 lacked the open-market link; Flux hedged | **Fixed.** Each draft states one claim with its access link, and Flux gives the pinned $8.68M. |
| 6 | Post kit: orphan custody chart | **Fixed.** Deleted. |
| 7 | Completeness: no current Stellar/Solana indication; Optimism Safe and Nest terms open | **Mostly fixed.** Current reads recorded with endpoint failures, Safe thresholds and modules pinned, and Nest terms cited. The Stellar sum is unreconciled (round-3 evidence gap), and the Nest pinned transfer controls were never read. |
| 8 | Evidence: hand-set dust flag; partial layer table | **Fixed.** A derived rule (fee ≥ 10% or output < $100) is tested at both edges, and the layer table now has nine claims. |

### Red-team notes

#### Answer
- In under 10 seconds a stranger gets the question, the $86.67m / $15.03m direct amounts, an explicit "unresolved" at 5% and an explicit "above the cutoff" for the custody-inclusive measure. There is no overclaim: "conditional" is stated, and the README's Results bullets give the $241.93m / $377.43m split.
- What remains is density and an unstated condition. The lead does not say that without the attested Solana and Aptos legs the custody-inclusive share falls to 2.63%, below 5%. A reader who stops at the first paragraph misses the single assumption the 6.74% depends on.

#### Evidence
- Every headline and table number I traced matched `kill_test.py` output, the fixtures, the PDFs or the live replay. The dust flag now comes from pinned observations, and the claim-by-layer table covers all material claims.
- **New inconsistency.** HOLDERS reports 1,325.2m BENJI in November Stellar trust lines, with the top three accounts holding 58.69%. I confirmed the sum independently through Horizon's asset statistics. Against Franklin's own N-MFP3 share counts, 667.97m at September 30 and 833.59m at October 31 (one class), the Stellar register alone is 1.98× and 1.59× larger. Either the fund grew by more than $490m in November, or trust-line balances include something other than outstanding shares, such as issuer or distribution inventory. The docs don't raise the question. This does not move any September bound, because the BENJI ceiling is the filing value. It does change how the concentration figure and the $585.39m BENJI-residual candidate should be read.

#### Reproducibility
- Offline: deterministic, standard library only, and portable from 3.9 to 3.14. Live: zero mismatches and zero endpoint errors on this run, including the new round-two Safe and current-read fixtures. The publisher PDFs re-verify by hash.
- The card PNG is hash-pinned. Re-rendering it needs licensed fonts kept outside the export, and that procedure is documented. This does not affect results.

#### Usefulness
- An RWA risk team now gets the pause map plus the gap to 5% in both supply models and a ranked list of which unresolved lots could close it. That turns an uninformative 0.94–62.20% interval into a research agenda. Prior art (BIS Bulletin 115, Tümer and Mafrur, RWA.xyz, issuer and LlamaRisk reports) is named and the contribution stated.
- The table gives no plausibility signal. The featured crossing combination uses the Crypto Relief donation Safe. Other identified lots with no contrary evidence also cross the deployment shortfall, for example Grove + XRPL OUSG ($306.73m), but the paragraph doesn't say so.

#### Completeness
- Every brief deliverable is present. The reshaped two-estimand result is reasoned in DECISIONS. New reads record their endpoint failures and capture windows, which is honest.
- The Nest September secondary route rests on terms and current docs only. A pinned read of the share tokens' transfer controls is feasible with keyless Plume RPC and was not attempted. The Optimism and USYC Safe operators stay open after documented attempts. September non-EVM registers are a public-data limit.

#### Documentation
- Numbers agree across README, RESULTS, HOLDERS, STATE, HANDOFF and DRAFTS, and tables render. The new `test_public_docs.py` enforces table shape and draft length.
- STATE.md ("verify the round-two working tree, commit and push") and HANDOFF.md ("This working tree contains the repair for Astra to verify") were committed in the same commit they describe as pending. `6f4b801` is public.
- HANDOFF replaced the brief's required DONE / PARTLY DONE / NOT DONE structure with a per-gap table. The round-one HANDOFF had the headings.
- REACH.md's BUIDL diagram labels the rank-2 Safe "operator and backing link unresolved", while HOLDERS:182 says the organization is corroborated (Crypto Relief).

#### Post kit
- Draft 1 (USDtb) and its card are strong and true as written. Drafts 2 (mTBILL: "only public route … under $0.07 … 79% pool fee") and 3 (Usual: "a stablecoin buyers could acquire on Curve") now carry their own takeaway. All link to RESULTS anchors that exist.
- The Flux draft is true but leaves the scope open. A pinned read of Flux's collateral factors would show whether every fUSDC borrow was OUSG-backed and let the draft drop the conditional.

#### Code
- Tests assert values and error messages on corrupted copies of the real fixtures. There are no skipped, faked or tautological tests. The builder's claimed kills reproduce.
- Fresh survivors that change output:
  - Removing the per-fund floor `max()` shifts the published basket floor ($4.907bn to $4.405bn), unresolved-at-floor ($1.351bn to $0.848bn) and slack ($4.272bn to $4.774bn). Only an identity is asserted.
  - High-NAV OUSG exclusions change the upper bound in the sixth decimal, and the test window is 1e-4.
  - Removing the shortfall clamp gives −$160.41m for the custody-inclusive measure.
  - A $1 BENJI exclusion mark is a near-equivalent mutant.
- Fresh survivors among untested guards:
  - In the pin check: the read's block parameter, the successor number and the block timestamp.
  - Curve coin-address match, Frax deposit destination, RPC cutoff field and USYC NAV > 0.
  - Franklin report period, class and B.5 shares, and the OUSG mark set.
  - Gated-receipt underlying identity.
  - `calculate()` input validation: duplicate fund, floor/ceiling order, nonpositive position and unknown kind.
  - The non-binding STBL net-deposit cap.
  - In the card checker: PNG header and size, and the single-claim check.
  - In replay: the `eth_getLogs` length check, so a live response with an extra log still matches.
- The evidence is checksummed and replayed, which lowers the practical risk. These are breadth gaps, not faked coverage.

### Outstanding gaps (owner)

The fix for each gap is in [`QUALITY.json`](../QUALITY.json).

1. Code: assert the published floor, slack and upper figures exactly. Add corrupted-copy cases for the 20 untested guards, plus a replay extra-log case (agent).
2. Evidence: reconcile the November Stellar BENJI sum against the September and October N-MFP3 share counts, and identify issuer-operated trust lines (agent).
3. Documentation: refresh STATE and HANDOFF for `6f4b801`, restore the DONE / PARTLY DONE / NOT DONE headings, and fix the REACH Crypto Relief label (agent).
4. Usefulness: add role evidence to the candidate table, and lead with crossing sets that have no contrary evidence (agent).
5. Completeness: read the Nest share-token transfer controls at the Plume pin (agent).
6. Answer: state the 6.74% condition and the 2.63% pinned-only share in the lead (agent).
7. Post kit: read Flux collateral factors at the pin and tighten the Flux draft (agent).

### Rahil's decisions (do not lower the score)

- Lead estimand: contract-only direct share (0.94–62.20%, unresolved) or custody-inclusive share (at least 6.74%, conditional on Anchorage's attested Solana and Aptos legs and the modeled ceiling).
- Approval of the Proofline USDtb card, and which of the four drafts, if any, to post on X.
- Already done: public GitHub publication (`origin/main` = `6f4b801`) and the MIT licence for original code. No date-dependent items are pending.

### History

| Round | Head | Overall |
| --- | --- | ---: |
| 1 | `73d93f81409f00f905f036d453d74e124a78ebb1` | 5 |
| 2 | `af9e1bdb2fd81e3130fbc29ce61b7cb6a696527f` | 7 |
| 3 | `6f4b801dd43d47050c46e234c889512ce0b9519c` | 8 |

## Round 2

- Rubric version: 1
- Reviewed head: `af9e1bdb2fd81e3130fbc29ce61b7cb6a696527f`. This is a clean tree, identical to `origin/main` at review time.
- Reviewer: claude-opus-5-5. The builder was GPT-6.2 Sol and the orchestrator GPT-6.2 Astra, so the reviewer comes from a different model family. The reviewer did not see round 1 being produced and reran every check independently.
- Reviewed at: 2026-11-27T04:14:40Z
- Scope: authority in BRIEF.md only. The review used keyless public RPC and web reads and local files. It did not post, push, commit, contact anyone, send transactions, use API keys or paid APIs, use Tenderly or set timers. It changed only `QUALITY.json` and this file. All work ran in a task-owned scratch clone, and the long live replay ran through the maintainer's workload gate.

### Scores

| Dimension | R1 | R2 | One-line reason |
| --- | ---: | ---: | --- |
| Answer | 6 | 8 | The README now leads with a concrete finding and a hero card. Its first sentence still counts $71.64m reachable only through a dust-size route as "traded on open markets" and gives no share or 5% verdict. |
| Evidence | 8 | 9 | Pinned and attested amounts are split, a dust sensitivity exists, the headline claims are tagged by layer, and every number I traced matched. The dust flag is hand-set, and non-headline claims are untagged. |
| Reproducibility | 9 | 10 | A clean clone reproduces every output. The full live replay matched 678/678 reads with zero errors, the PDF check passed 15/15 against hash-pinned originals, and tests pass on Python 3.9, 3.10 and 3.14. |
| Usefulness | 7 | 8 | Prior art is named, and I confirmed it against the primary sources. The pause map and route evidence are citable. The headline restates an issuer attestation, the direct share stays wide, and nothing shows what would flip the verdict. |
| Completeness | 7 | 8 | Optimism BUIDL and Plume USTB now reconcile. Small deployments are capped at $203.48m, which cannot move the 5% test. Current Solana reads were added. BENJI and USTB value outside the censuses has no current indication, and two vault/Safe roles stay open. |
| Documentation | 7 | 8 | The glossary, role key, Python version and reserve-custody class are fixed. A new HOLDERS table does not render on GitHub, and STATE/HANDOFF still describe the slice as uncommitted. |
| Post kit | 5 | 8 | Four one-claim drafts, plus a 12-word Proofline card with a hash-pinned checker. Drafts 2–4 lack the open-market link that makes each a finding (Flux is hedged), and an orphan chart is still tracked. |
| Code | 7 | 7 | The guards named in round 1 are now tested. A fresh probe found 15 of 18 other guard mutants surviving, and the card checker, PDF verifier and replay comparator have no tests. |
| **Overall (lowest)** | **5** | **7** | Code, the lowest dimension, sets the overall score. |

### What I ran

| Command or check | Result |
| --- | --- |
| Clean clone into scratch and check out `af9e1bd` | OK. HEAD equals `origin/main`. |
| `sha256sum -c evidence/SHA256SUMS` | 19/19 OK |
| `python3 -m unittest discover -s tests -v` (3.14.8, plus 3.10 and 3.9) | 22/22 pass on all three versions |
| `python3 scripts/holder_audit.py` | Exit 0 |
| `python3 scripts/kill_test.py` | Exit 0. Direct verified $86,669,353.88, lower 0.9442%, upper 62.1997%, `inconclusive`. Custody-inclusive $619,366,062.06 (pinned $241,931,783.06 plus attested-only $377,434,279), lower 6.7476%, `continue`. Ceiling $9,179,057,896.15. Without dust: $15.03m direct, 5.967% custody-inclusive. BUIDL scenario: ceiling $5.94149bn, direct 1.4587–41.602%, custody 10.424%. Frax sensitivity: 1.328% / 7.132%. All agree with README, RESULTS, STATE, HANDOFF and the drafts under the stated rounding. |
| `python3 scripts/check_post_card.py` | Pass. 12 words. HTML and PNG hashes match the receipt. |
| `workload_budget.py run -- python3 scripts/replay_evidence.py --workers 1` | Exit 0. 678 match, 0 mismatch, 0 error across 9 fixtures (EVM 64, holders 437, Ethereum review 115, signer 1, receipt 3, XRPL 5, supplement 28, discovery 23, Usual source 2). |
| `python3 scripts/verify_pdf_facts.py` (downloads into ignored scratch `data/upstream/`) | 15 checks pass. All three publisher file hashes verified. |
| Independent second-RPC reads (`rpc.mevblocker.io`) at block `0x18e28a9` | USDtb `totalSupply` = 496,571,141.846 and Curve USDtb balance = 10,484,993.79, matching the fixtures exactly. The successor block timestamp 1790812811 brackets the cutoff, and its `parentHash` equals the pinned block hash. A BNB second-RPC read was rate-limited and is not counted. |
| Prior art against primary sources | The arXiv 2610.05873 abstract confirms Ethereum-based tokenized funds, Dec 2025–Aug 2026 windows, and concentration measured with and without intermediaries. The BIS Bulletin 115 page (26 November 2025) says allow lists "only constrain direct holding". Both match RESULTS. |
| Relative Markdown link and anchor check, including links to this repo's GitHub `main` | 181 links, 0 broken |
| Markdown table cell-count check | One failure: `docs/HOLDERS.md:37`, 8 header cells and 9 delimiter cells |
| Scan for private paths, credentials and paid providers | None in the public tree. Only the generic `~/scratch/<project>/<task>/` pattern in BRIEF.md. |
| Scan for rule-breaking language and named individuals | None |
| Mutation probe, 18 single-line mutants of `kill_test.py` and `check_post_card.py` | 3 caught: attested whole-dollar haircut, Midas dust flag, USDtb supply tolerance. 15 survived: 13 in `kill_test.py` and 2 in `check_post_card.py` (listed under Code). The round-1 mutants are covered by the new corrupt-copy test and were not re-probed. |

### Round-1 gaps: status

| # | Round-1 gap | Status at `af9e1bd` |
| --- | --- | --- |
| 1 | Drafts need footnotes, too many numbers | Mostly fixed. Each draft carries one claim and no draft needs the modeled ceiling. Drafts 2–4 still lack a "so what" (round-2 gap). |
| 2 | No card or chart | Fixed. A Proofline 12-word card with receipt, hash pins and a checker. Design approval is Rahil's. |
| 3 | README lead foggy | Improved. A clear title and hero, but no share or verdict, and it counts the dust lot (round-2 gap). |
| 4 | BUIDL-specific denominator | Fixed. Gross EVM sum plus Solana/Aptos allowances, a bridge-balance and implementation check, and a scenario table. |
| 5 | Midas dust sensitivity | Fixed. Shown in code, tests and RESULTS. |
| 6 | Verified and attested mixed, no layer tags | Fixed for the headline claims (split columns and a claim-by-layer table). The remaining claims are a round-2 nit. |
| 7 | No prior art | Fixed and verified. |
| 8 | Unobserved small deployments, no Solana | Largely fixed. Optimism and Plume reconcile, the eight remaining deployments are capped at $203.48m and recorded with failure records, and current Solana reads were added. A residual remains (round-2 gap). |
| 9 | Class label, role key, Python version, glossary | Fixed. The HOLDERS table broke in the same edit (round-2 gap). |
| 10 | Surviving mutants, untested guards | The named guards are fixed. Other guards remain untested (round-2 gap). |
| 11 | No full replay or transcription check | Fixed. `replay_evidence.py` and `verify_pdf_facts.py`, both rerun here. |

### Red-team notes

#### Answer
- The title and hero card ("$533M of BlackRock's BUIDL backed USDtb") land in under 10 seconds and are true as stated.
- The first sentence frames the question as "backed tokens that traded on open markets" and adds "$86.67 million more" from direct contracts. Midas accounts for $71.64m of that, and RESULTS calls its only route "economically prohibitive as evidence of meaningful access". The headline should either use $15.03m or split the figure.
- The lead gives no share or verdict. The brief's kill test is a share against 5%. The evidence supports one plain line for each estimand: custody-inclusive at least 6.74% (clears 5%, conditional on the attestation and the platform ceiling), and contract-only unresolved. Rahil still chooses which one leads. Stating both does not wait on that choice.

#### Evidence
- Every number I traced, from README through RESULTS to the kill_test JSON and then the fixture or PDF, matched. Live and second-RPC reads agree to the last digit.
- The non-pinned November Solana and Aptos reads used in the BUIDL scenario are labelled as scenario inputs, not pinned facts, and RESULTS states the direction of the risk (September supply could exceed the allowance). The bridge check is honest about its scope: two implementations verified, and address equality on the other chains is not treated as proof.
- Nits: `dust_only=True` is a hand-set judgment rather than a rule applied to the pinned fee and input size, and the claim-by-layer table stops at the three headline claims.

#### Reproducibility
- Offline: deterministic, stdlib only, and portable to 3.9. Live: a full replay with zero mismatches and zero errors on this run, with alternate-endpoint fallback and per-read retry documented. The publisher PDFs re-verify by hash.
- The card PNG cannot be re-rendered from the public tree alone, because the fonts are deliberately excluded for licence reasons. The procedure is documented and the PNG is hash-pinned, so this is not a results-reproducibility issue.

#### Usefulness
- Strongest contributions: the block-pinned, code-verified mapping of fund units to specific open tokens (USDtb, USD0, USST, mTBILL), the explicit exclusion of gated receipts (Horizon, Flux), and the six-protocol pause map. An RWA risk lead could cite the pause map and the Flux credit path directly.
- Weaknesses: the headline fact (BUIDL behind USDtb) is published by Anchorage itself and was already broadly known. The direct-contract share, which is the brief's core quantity, is bounded only to 0.94–62.20%, or 1.45–41.61% under the deployment scenario. A short table of what would flip the direct verdict would make the unresolved result useful to a risk team. The gap to 5% is $372.28m at the platform ceiling or $210.41m at the deployment ceiling. The table would set the largest unresolved holders against that gap, for example the BUIDL-I 4-of-7 Safe at $112.91m.

#### Completeness
- Every brief deliverable exists. The reshaped two-estimand finding is reasoned in DECISIONS. The new cap test for small deployments (all eight together could add at most $203.48m, leaving the total below the $458.95m cutoff) is a good way to close coverage holes that cannot be closed directly.
- Residual: $619.72m of BENJI is unclassified outside the Ethereum and Avalanche censuses, mostly the Stellar register and book-entry shares, and USTB beyond Ethereum and Plume is also unclassified. Neither has a current non-pinned indication, though the Solana section shows this can be done. The Optimism Safe role and historical access to the Nest receipts stay open. Full September non-EVM registers cannot be reconstructed from public data, and the docs say so.

#### Documentation
- Numbers agree across README, RESULTS, HOLDERS, REACH, STATE, HANDOFF and DRAFTS. The glossary and role key help a reader who lacks the chat history.
- `docs/HOLDERS.md:37`: the share table has 8 header cells and 9 delimiter cells, so GitHub renders it as raw pipes. This regression came from the round-1 repair.
- STATE.md's next action and HANDOFF's review line still describe the slice as uncommitted and awaiting Astra's commit. `af9e1bd` is committed and public.

#### Post kit
- The card is excellent: one claim, 12 words, a Proofline palette with a recorded 13.2:1 contrast, a value receipted to the Schedule II total, and a checker that pins the exact PNG and HTML. Design approval stays Rahil's.
- Drafts: 1 is strong. 2 (mTBILL) is true but the reader has to supply the takeaway. 3 (Usual) never says USD0 is openly tradable, which is the reason the fact matters. 4 (Flux) is hedged ("could include", "can depend") rather than a claim, and it omits the pinned $8.68m fUSDC borrows. In Draft 1, "exposure to the stablecoin's reserves" slightly overstates holder rights.
- `docs/figures/custody-comparison.png` is tracked, referenced nowhere, has no checker, and draws the dust-inclusive $86.67m as one solid bar.

#### Code
- Tests now corrupt copied fixtures for seven guards and cover the Frax nonzero-counter branch and both new sensitivities. All of these assert observable outputs. I found no faked or skipped tests.
- Surviving mutants: the USDtb pool-above-supply check; the Curve quote/inventory guard; the USYC oracle-round guard; the pin bracket and the `parentHash` check in `load_evidence`, which `holder_audit` tests separately but `kill_test` does not; the Frax deposit code-type check; the Usual cross-capture equality; the BNB USYC rank/code guard; the Midas/STBL runtime-code guard; Franklin's share-class count; the STBL USST-supply cap; the BENJI mark for small deployments; and the bridge balance read. In `check_post_card.py`, the copy-match and PNG-link checks also survive. `check_post_card.py`, `verify_pdf_facts.verify()` and `replay_evidence.compare_rpc()` have no unit tests. `bridge_balances_raw` is reported but never asserted.

### Outstanding gaps (owner)

The fix for each gap is in [`QUALITY.json`](../QUALITY.json).

1. Code: add corrupted-copy tests for the 13 surviving `kill_test.py` guards, tests for the card checker, PDF verifier and replay comparator, and an assertion on bridge balances (agent).
2. Usefulness: add a table of what would move the direct verdict, and attempt to resolve the top Safe roles (agent).
3. Answer: state both estimands' verdicts in the README lead, and split or drop the dust lot from "open markets" (agent).
4. Documentation: fix the HOLDERS.md:37 table, refresh STATE and HANDOFF, and add a table-shape check (agent).
5. Post kit: rewrite drafts 2–4 around the open-market link, and soften Draft 1's reserve-exposure phrase (agent).
6. Post kit: delete the orphan `custody-comparison.png`, or receipt it and split out the dust lot (agent).
7. Completeness: add current, non-pinned holder indications for Stellar BENJI and Solana USTB, and resolve the Optimism Safe and the Nest access terms (agent).
8. Evidence: derive `dust_only` from the pinned observations, and extend the claim-by-layer table (agent).

### Rahil's decisions (do not lower the score)

- Lead estimand: custody-inclusive at least 6.74% (counts USDtb reserves, clears 5%) or contract-only 0.94–62.20% (unresolved).
- Approval of the USDtb card design, and which drafts, if any, to post on X.
- Already done: public GitHub publication (`origin/main` = `af9e1bd`) and the MIT licence for original code. No date-dependent items are pending.

### History

| Round | Head | Overall |
| --- | --- | ---: |
| 1 | `73d93f81409f00f905f036d453d74e124a78ebb1` | 5 |
| 2 | `af9e1bdb2fd81e3130fbc29ce61b7cb6a696527f` | 7 |

## Round 1 (historical record, preserved)

This record preserves the independent Opus assessment of the research snapshot before publication preparation.

- Rubric version: 1
- Reviewed head: `73d93f81409f00f905f036d453d74e124a78ebb1` (clean tree)
- Reviewer: claude-opus-5-5. The builder was GPT-6.2 Sol and the orchestrator GPT-6.2 Astra, so the reviewer is from a different model family.
- Reviewed at: 2026-11-27T03:34:16Z
- Scope: BRIEF.md authority only. Keyless public RPC reads and local files; no posting, pushing, outreach, transactions, keys, paid APIs, Tenderly or timers. No other repo files were changed.

### Scores

| Dimension | Score | One-line reason |
| --- | ---: | --- |
| Answer | 6 | The README lead is foggy (two estimands, a 0.94–62.20% interval and four caveats), and the strongest supported line is never stated. |
| Evidence | 8 | Pinned and replayable, with independent RPC agreement. The Midas lot rests on a dust route with no sensitivity, and 'verified' covers attested legs. |
| Reproducibility | 9 | A clean clone reproduces every output. Checksums pass. Live refetch and replays match exactly. |
| Usefulness | 7 | The route map and the USDtb finding are novel and citable, but no prior art is named or compared. |
| Completeness | 7 | Every brief deliverable exists. Holder coverage is partial on several chains and absent on Solana. |
| Documentation | 7 | Complete and internally consistent numbers, but dense. One class label conflicts with the code, agent names are unexplained, and no Python version is given. |
| Post kit | 5 | Three of the five drafts need a footnote to be true. Drafts carry 3–6 numbers each. There are no cards or charts, although the brief asks for cards. |
| Code | 7 | The negative-path tests are good, but 3 of 6 guard mutations survive and several guards are untested. |
| **Overall (lowest)** | **5** | Capped by the post kit. |

### What I ran

These commands describe the reviewed snapshot. They ran in a clean checkout with Python 3.14.8 and the standard library. The scores and counts below apply to that snapshot.

| Command | Result |
| --- | --- |
| Check out the reviewed revision in a clean clone | OK |
| `sha256sum -c evidence/SHA256SUMS` | 21/21 OK. These cover every evidence file. |
| `/usr/bin/python3 scripts/holder_audit.py` | exit 0, 21 deployments |
| `/usr/bin/python3 scripts/kill_test.py` | exit 0. Direct verified $86,669,353.88, lower 0.9442%, upper 62.1997%, verdict `inconclusive`. Economic verified $619,366,062.06, lower 6.7476%, verdict `continue`. Ceiling $9,179,057,896.15. Matches RESULTS, README, HANDOFF and DRAFTS under the stated rounding (lower down, upper up). |
| `/usr/bin/python3 -m unittest discover -s tests -v` | 19/19 pass |
| METHOD "priority reads" replay (BNB USYC supply, balance and code, Usual linkage, USD0 quote, BNB receipt) | 7/7 reads match. Receipt blockHash and logs match. |
| METHOD "repair fixtures" replay (Midas, STBL, Frax, Flux) | 10/10 match |
| `scripts/fetch_evm.py --chain ethereum ../ethereum-live.json` (fresh live refetch) | Same block hash at 26,093,737. All 32 reads are identical to `evidence/evm-2026-09-30.json`. |
| Independent read on a second RPC (`rpc.mevblocker.io`): USTB `balanceOf(Midas vault)` at `0x18e28a9`, and the block timestamp | 6,379,144.864074 USTB, timestamp 1790812799 (2026-09-30 23:59:59 UTC exactly) |
| Run `pdftotext` on the Securitize release | Footnote 2 says the $4.8bn covers funds and equities across the platform. The release gives no BUIDL-specific figure. |
| Mutation probe of `scripts/kill_test.py` (6 single-line mutants) | 3 caught (STBL high-NAV pricing, Schedule II −$1, OUSG time allowance). 3 survived: Franklin readback check removed, Anchorage attestation-vs-RPC tolerance widened to $1bn, mTBILL supply cap disabled. |
| grep for keys and paid providers (`apikey`, `infura`, `alchemy`, `tenderly`) in scripts and evidence | none |
| grep for rule-breaking language and named individuals in docs and drafts | none. Only protocols are named. |

### Red-team notes

#### Answer
- The first line asks a question in internal terms. A stranger then meets "conditional 0.94%–62.20% direct-contract bounds straddle the 5% cutoff" and a second 6.74% measure, followed by four caveat sentences. The 10-second test fails.
- The evidence supports a sharper line. At least $619m (≥6.7% of a deliberately large basket) backed tokens anyone could buy on a DEX at the pin, and $533m of it was BUIDL behind Ethena/Anchorage's USDtb. Leakage through contracts proper is verified at $86.67m and cannot be capped below 5% with public data. The BRIEF's own list of "contracts" includes stablecoin reserves, and its limits say "economic exposure". DECISIONS defends the contract-only primary estimand, and that is a legitimate reading. Which estimand leads publicly is listed as Rahil's decision.
- The 62.20% ceiling mostly reflects the denominator choice, not the holder evidence. BUIDL's ceiling is Securitize's whole-platform $4.9bn, which includes equities and other funds. That supplies $3.92bn of the $4.27bn slack. Pinned EVM BUIDL supplies sum to about $1.136bn. The top Ethereum BUIDL holders have no code (no lockbox signature), so per-chain classes look additive, but this is untested. A BUIDL-specific scenario would narrow the ceiling substantially. It would probably still not resolve 5%.

#### Evidence
- Strong. Every reviewed onchain number had a URL, method, parameters, result and a block/successor bracket, and the code enforces the pin. My independent second-RPC read and the full live refetch agree to the last digit.
- The Midas lot ($71.64m, 83% of the direct numerator) qualifies on a 0.0001 ETH quote at a 79% LP fee. The docs disclose this, but no sensitivity removes it. My arithmetic without it: direct lower about 0.16%, custody-inclusive lower about 5.97%.
- The column "Economic backing verified" includes $377.4m of Solana/Aptos BUIDL that is attested by an accountant-examined report but not read onchain.
- SOURCES tags each source's layer. RESULTS claims are not tagged by layer, so issuer statements, arithmetic and onchain facts sit in the same paragraph.

#### Reproducibility
- Excellent offline determinism and live agreement. Minor gaps: there is no regeneration script for the repair fixtures, so verification is replay-only, and the hand transcriptions have no automated check.

#### Usefulness
- New relative to public dashboards: a block-pinned, code-verified map from each fund to permissionless tokens (USDtb, mTBILL, USD0, USST), with explicit exclusions of gated receipts (Horizon, Flux) and a redemption-pause dependency table across Aave Horizon, Morpho, Sky/Spark/Grove, Ethena, Euler and Flux. An RWA risk lead could cite the USDtb channel and the Flux credit path.
- No prior-art comparison exists. BIS 115 appears only as "framing", and Tümer & Mafrur, rwa.xyz and issuer transparency pages go unmentioned.

#### Completeness
- Delivered: kill test, holder tables, 33 classified contracts, five ASCII reach diagrams, the six-protocol pause map, all required docs, independent review plus one repair, and HANDOFF.
- Partial: several deployments are 100% unobserved (BUIDL on Arbitrum, Optimism, Polygon and Tempo; BENJI on Arbitrum, Base and Polygon; USTB on Plume). There is no Solana holder coverage for any fund. HANDOFF honestly marks this PARTLY DONE. Some of it can be improved with keyless tools.

#### Documentation
- The numbers agree across README, RESULTS, HANDOFF, STATE, DRAFTS and the code output. STATE is under 3,000 characters with the next action first.
- HOLDERS classes Anchorage's BNB USDtb reserve as "Issuer / ops" (75.996%), while the code treats it as reserve custody for a tradable stablecoin.
- "Sol", "Astra" and "Sonnet" appear without a role key. No Python version is stated. There is no glossary for "strict excluded", "denominator slack" or "route-local".

#### Post kit
- The drafts are 35–47 words each. Each links to RESULTS anchors, and all anchors resolve.
- Draft 1's point is "unresolved", carried by 4 numbers. Draft 2 requires the "modeled ceiling" caveat, which its own evidence note concedes. Draft 3 calls a 79%-fee dust quote "a way to buy". These fail "nothing that needs a footnote to be true" and "point at a glance".
- The brief asks for card images with ≤20 words. There are none, and no chart exists to pass automated checks. Design approval stays Rahil's, but the agent can produce the candidate cards.

#### Code
- Tests exercise observable behaviour and many failure paths: pin mismatch, parent hash, XRPL pagination, Usual linkage and pause, BNB burn reconciliation, delegated EOA, duplicates and the cutoff edge.
- Three surviving mutants show untested guards. Untested too: mixed dates, USDtb supply vs attestation, reserve-leg reconciliation, classified > ceiling, and the nonzero-`frxUSDMinted` cap branch (dead at this pin). No faked code was found.

### Outstanding gaps (owner)

The fix for each gap is in `QUALITY.json`.

1. Post kit: rewrite the drafts so each makes one footnote-free claim, and recast the Midas draft (agent).
2. Post kit: produce 1–2 receipted cards or charts that pass the exhibit checks (agent). Design approval is Rahil's.
3. Answer: plain-language README one-liner that leads with the verified USDtb and contract amounts (agent).
4. Answer: BUIDL-specific denominator sensitivity, after a test for lock-and-mint double counting (agent).
5. Evidence: "exclude dust-only routes" sensitivity, or a better mTBILL route (agent).
6. Evidence: split verified from attested amounts, and tag headline claims by evidence layer (agent).
7. Usefulness: prior-art section with verified comparisons (agent).
8. Completeness: close or justify the unobserved small deployments, and add a non-pinned Solana indication (agent).
9. Documentation: fix the Anchorage class label, add a role key, Python version and glossary (agent).
10. Code: negative tests for the surviving-mutant guards and the other untested guards, plus the Frax cap branch (agent).
11. Reproducibility: a full-fixture replay script and automated transcription checks (agent).

### Rahil's decisions (do not lower the score)

- Which estimand leads publicly: custody-inclusive ≥6.74% or contract-only 0.94% with an open ceiling.
- Whether to publish any draft, and design approval for any card.
- GitHub publication was pending at the time of review. See [current authorization](../BRIEF.md).

### History

| Round | Head | Overall |
| --- | --- | ---: |
| 1 | `73d93f81409f00f905f036d453d74e124a78ebb1` | 5 |
