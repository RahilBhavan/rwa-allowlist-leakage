# Final research handoff

## DONE

The third independent review scored published research commit `6f4b801` **8/10**, after rounds of **5/10** and **7/10**. Reproducibility scored 10. The reviewer matched 696 historical reads, 20 fixture hashes and 15 publisher-document checks, and passed all 40 tests on four Python versions. Publication and MIT licensing are complete. The three-round review budget is exhausted. [Independent review](docs/QUALITY.md) · [Public repository](https://github.com/RahilBhavan/rwa-allowlist-leakage)

The September direct-contract result spans 0.94%–62.20%. The custody-inclusive lower bound of 6.74% uses Anchorage’s examined Solana and Aptos reserves and the modeled supply ceiling. Excluding those two attestation-only legs reduces it to 2.63%. [Results](docs/RESULTS.md)

## PARTLY DONE

The earlier repair dispositions below document changes present in the reviewed commit. Evidence, documentation and code each received 8/10 in the final review.

| Round-two gap | Disposition |
| --- | --- |
| Code and mutation coverage | **Done.** Corrupted-copy tests cover all 13 calculation faults, including BENJI’s filing NAV mark, the binding USST cap and the bridge guard. Card tests cover six classes of failure, including exact copy and the PNG link. PDF tests exercise all 15 comparisons and missing source structure. Replay tests cover mismatches, endpoint failures and alternate-endpoint recovery. The 15 targeted source changes each failed a behavioral assertion. |
| Usefulness | **Done.** The direct shortfall is $372.28m at the platform ceiling and $210.41m in the BUIDL deployment scenario. The report ranks separate holder lots and coverage gaps, checks combinations and keeps denominator margins out of the candidate sums. [Shortfalls and candidates](docs/RESULTS.md#what-would-move-the-direct-verdict) |
| Answer | **Done.** Primary direct-contract result stays unresolved at 5% with a 0.94%–62.20% range. The $86.67m technical result falls to $15.03m after removing dust. The companion custody-inclusive conditional lower bound is 6.74%. [README](README.md) |
| Documentation | **Done.** Repaired the holder table, added Markdown column-count and draft-length checks, and updated state, sources and dates. |
| Drafts | **Done.** Four standalone drafts link to the September evidence. USDtb and USD0 describe publicly quotable tokens, Midas states the size and fee limitation, and Flux gives the pinned $8.68m fUSDC borrow total and gated OUSG liquidation path. [Drafts](posts/DRAFTS.md) |
| Orphan chart | **Done.** Removed the unused custody comparison. The receipted USDtb card verifies at 12 words and retains its exact checked HTML and PNG. |
| Holder and control coverage | **Partly resolved.** Added current Stellar BENJI trust lines and a successful current Solana USTB largest-account read after three endpoint failures. Pinned calls establish the Optimism Safe’s 1-of-1 threshold and empty module list. Crypto Relief publishes its BUIDL-I donation Safe. The Optimism and USYC Safe operators, downstream backing for those Safes, and September Nest secondary liquidity and permissions remain unresolved. Nest’s offering restrictions have first-party, pre-pin evidence. [Controls, current reads and terms](docs/HOLDERS.md#round-two-holder-and-control-reads) |
| Evidence layers and dust | **Done.** The numeric dust rule uses the pinned LP fee and quoted output value at NAV. A tighter sensitivity still flags Midas. Material claims identify the supporting onchain facts, issuer statements, terms, arithmetic and interpretation as applicable. [Material claim evidence](docs/RESULTS.md#how-the-material-claims-are-supported) |

**Unresolved coverage.** Complete September Stellar and Solana holder registers, global bridge deduplication, borrower-level Flux collateral attribution and executable depth beyond the quoted sizes remain open. Current observations inform discovery and leave the September bounds unchanged.

## NOT DONE

The November Stellar BENJI trust-line total has not been reconciled to fund shares. It cannot support a fund-holder concentration claim. Other open checks include floor arithmetic under corrupted inputs, unexpected extra logs on replay, Plume Nest transfer controls and Flux collateral factors. Candidate balances in the cutoff table show mathematical capacity. Evidence for a downstream wrapper role is particularly weak for the Crypto Relief donation wallet. Its public address attribution and the economic use of the lot are separate questions. The final review records specific fixes and owners for each gap. [Remaining gaps](QUALITY.json)

## Verification

Run from the repository root with Python 3.10 or newer. The 40 offline tests passed on Python 3.10 and 3.14. All 20 hashes matched. The three freshly fetched publisher PDFs match their known hashes and pass all 15 transcription checks. Third-party documents remain publisher-hosted.

```sh
git diff --check
git diff --exit-code -- QUALITY.json docs/QUALITY.md LICENSE
sha256sum -c evidence/SHA256SUMS
python3 -m unittest discover -s tests -v
python3 scripts/holder_audit.py
python3 scripts/kill_test.py
python3 scripts/check_post_card.py
python3 scripts/verify_pdf_facts.py
```

On an isolated copy, the following source edits were applied separately, each followed by the relevant `unittest discover -s tests -v -k <test-name-fragment>` run and restoration of the original file. Each run failed an assertion for the intended behavior.

| Mutation probes | Test name fragment | Result |
| --- | --- | --- |
| Disable pool inventory vs supply, Curve quote/inventory, USYC oracle round, time bracket, parent hash, Frax deposit code, Usual cross-capture equality, BNB rank/code, Midas/STBL runtime code, Franklin share-class count or replace bridge balance with zero | `guards_reject_corrupt` | 11/11 killed |
| Remove the USST supply cap | `stbl_credit_is_capped` | 1/1 killed |
| Set the small-deployment BENJI mark to $1 | `separate_attested_and_dust` | 1/1 killed |
| Skip exact visible-text match or skip draft PNG link | `hash_verified_html`, `missing_draft_links` | 2/2 killed |

The workload-gated command `python3 scripts/replay_evidence.py --workers 1` replayed **696 checks with zero mismatches and zero endpoint errors**, including 18 round-two Safe calls and block-header checks. The public-tree audit checked 205 relative Markdown links with zero failures or sensitive-text flags. The [method](docs/METHOD.md#repair-fixtures-and-replay) records the replay commands. The [readbacks](evidence/round2-readbacks.json) record current holder refresh requests and results by UTC capture window, ledger or finalized slot.

## Rahil’s decisions

Choose which result leads publicly. Approve or decline the USDtb card and decide whether to publish any of the four drafts. Publication of an X draft and design approval remain Rahil’s decisions. [Drafts and card](posts/DRAFTS.md)
