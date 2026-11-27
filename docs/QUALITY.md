# Quality review — round 1

This record preserves the independent Opus assessment of the research snapshot before publication preparation.

- Rubric version: 1
- Reviewed head: `73d93f81409f00f905f036d453d74e124a78ebb1` (clean tree)
- Reviewer: claude-opus-5-5. The builder was GPT-6.2 Sol and the orchestrator GPT-6.2 Astra, so the reviewer is from a different model family.
- Reviewed at: 2026-11-27T03:34:16Z
- Scope: BRIEF.md authority only. Keyless public RPC reads and local files; no posting, pushing, outreach, transactions, keys, paid APIs, Tenderly or timers. No other repo files were changed.

## Scores

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

## What I ran

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

## Red-team notes

### Answer
- The first line asks a question in internal terms. A stranger then meets "conditional 0.94%–62.20% direct-contract bounds straddle the 5% cutoff" and a second 6.74% measure, followed by four caveat sentences. The 10-second test fails.
- The evidence supports a sharper line. At least $619m (≥6.7% of a deliberately large basket) backed tokens anyone could buy on a DEX at the pin, and $533m of it was BUIDL behind Ethena/Anchorage's USDtb. Leakage through contracts proper is verified at $86.67m and cannot be capped below 5% with public data. The BRIEF's own list of "contracts" includes stablecoin reserves, and its limits say "economic exposure". DECISIONS defends the contract-only primary estimand, and that is a legitimate reading. Which estimand leads publicly is listed as Rahil's decision.
- The 62.20% ceiling mostly reflects the denominator choice, not the holder evidence. BUIDL's ceiling is Securitize's whole-platform $4.9bn, which includes equities and other funds. That supplies $3.92bn of the $4.27bn slack. Pinned EVM BUIDL supplies sum to about $1.136bn. The top Ethereum BUIDL holders have no code (no lockbox signature), so per-chain classes look additive, but this is untested. A BUIDL-specific scenario would narrow the ceiling substantially. It would probably still not resolve 5%.

### Evidence
- Strong. Every reviewed onchain number had a URL, method, parameters, result and a block/successor bracket, and the code enforces the pin. My independent second-RPC read and the full live refetch agree to the last digit.
- The Midas lot ($71.64m, 83% of the direct numerator) qualifies on a 0.0001 ETH quote at a 79% LP fee. The docs disclose this, but no sensitivity removes it. My arithmetic without it: direct lower about 0.16%, custody-inclusive lower about 5.97%.
- The column "Economic backing verified" includes $377.4m of Solana/Aptos BUIDL that is attested by an accountant-examined report but not read onchain.
- SOURCES tags each source's layer. RESULTS claims are not tagged by layer, so issuer statements, arithmetic and onchain facts sit in the same paragraph.

### Reproducibility
- Excellent offline determinism and live agreement. Minor gaps: there is no regeneration script for the repair fixtures, so verification is replay-only, and the hand transcriptions have no automated check.

### Usefulness
- New relative to public dashboards: a block-pinned, code-verified map from each fund to permissionless tokens (USDtb, mTBILL, USD0, USST), with explicit exclusions of gated receipts (Horizon, Flux) and a redemption-pause dependency table across Aave Horizon, Morpho, Sky/Spark/Grove, Ethena, Euler and Flux. An RWA risk lead could cite the USDtb channel and the Flux credit path.
- No prior-art comparison exists. BIS 115 appears only as "framing", and Tümer & Mafrur, rwa.xyz and issuer transparency pages go unmentioned.

### Completeness
- Delivered: kill test, holder tables, 33 classified contracts, five ASCII reach diagrams, the six-protocol pause map, all required docs, independent review plus one repair, and HANDOFF.
- Partial: several deployments are 100% unobserved (BUIDL on Arbitrum, Optimism, Polygon and Tempo; BENJI on Arbitrum, Base and Polygon; USTB on Plume). There is no Solana holder coverage for any fund. HANDOFF honestly marks this PARTLY DONE. Some of it can be improved with keyless tools.

### Documentation
- The numbers agree across README, RESULTS, HANDOFF, STATE, DRAFTS and the code output. STATE is under 3,000 characters with the next action first.
- HOLDERS classes Anchorage's BNB USDtb reserve as "Issuer / ops" (75.996%), while the code treats it as reserve custody for a tradable stablecoin.
- "Sol", "Astra" and "Sonnet" appear without a role key. No Python version is stated. There is no glossary for "strict excluded", "denominator slack" or "route-local".

### Post kit
- The drafts are 35–47 words each. Each links to RESULTS anchors, and all anchors resolve.
- Draft 1's point is "unresolved", carried by 4 numbers. Draft 2 requires the "modeled ceiling" caveat, which its own evidence note concedes. Draft 3 calls a 79%-fee dust quote "a way to buy". These fail "nothing that needs a footnote to be true" and "point at a glance".
- The brief asks for card images with ≤20 words. There are none, and no chart exists to pass automated checks. Design approval stays Rahil's, but the agent can produce the candidate cards.

### Code
- Tests exercise observable behaviour and many failure paths: pin mismatch, parent hash, XRPL pagination, Usual linkage and pause, BNB burn reconciliation, delegated EOA, duplicates and the cutoff edge.
- Three surviving mutants show untested guards. Untested too: mixed dates, USDtb supply vs attestation, reserve-leg reconciliation, classified > ceiling, and the nonzero-`frxUSDMinted` cap branch (dead at this pin). No faked code was found.

## Outstanding gaps (owner)

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

## Rahil's decisions (do not lower the score)

- Which estimand leads publicly: custody-inclusive ≥6.74% or contract-only 0.94% with an open ceiling.
- Whether to publish any draft, and design approval for any card.
- GitHub publication was pending at the time of review. See [current authorization](../BRIEF.md).

## History

| Round | Head | Overall |
| --- | --- | ---: |
| 1 | `73d93f81409f00f905f036d453d74e124a78ebb1` | 5 |
