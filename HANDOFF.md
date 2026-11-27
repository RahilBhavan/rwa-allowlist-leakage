# Reopened quality-loop handoff

The public base is `da54eec`. Round three scored its reviewed research commit `6f4b801` **8/10**. Astra reproduced the revised totals and matched both Nest pool-state reads and the Flux market registry to the historical RPC responses. A fresh round-four score is pending. [Public repository](https://github.com/RahilBhavan/rwa-allowlist-leakage) · [Recorded review](docs/QUALITY.md)

## DONE

- Reconstructed the floor, ceiling, exclusions and cutoff independently from the raw observations using Decimal arithmetic. The basket floor is **$4,907,248,681.91**, the cap is **$9,179,057,896.15** and their difference is **$4,271,809,214.24**. The BUIDL floor is **$975,383,966.17** and the USYC floor is **$2,375,813,697.24**. The original floor coverage remainder reproduces at **$1,350,866,876.34**. Crediting the verified Nest lots reduces it to **$1,347,050,929.41**. The direct upper share still rounds to **0.621997** at six decimal places and the custody-inclusive shortfall is zero. [Independent arithmetic check](tests/test_bound_reconstruction.py)
- Reapplied every concrete fault listed by the round-three reviewer. The prose says 24 survivors, but splitting the named behaviors into individual probes gives **25**. All 25 failed a behavioral assertion. The full test suite also covers old and new pin brackets, corrupted contract identities and periods, each replay comparison family, extra and missing logs, and a binding STBL net-deposit cap. [Mutation driver](tests/probe_round3.py)
- Pinned the two Nest share hooks, vault authority and Rooster market state. Both accepted simulated delivery of quoted shares to the test wallet. nTBILL is dust-only under the tested rule. nBASIS survived that filter. Direct backing is **$90.49m** or **$15.04m** after the dust filter. The direct range is **0.98%–62.20%**, leaving 5% unresolved. The companion lower bound is **6.78%** including Anchorage’s Solana and Aptos attestations or **2.67%** on pinned balances alone. [Nest evidence](docs/HOLDERS.md#plume-nest-access) · [Results](docs/RESULTS.md)
- Checked Flux’s five listed markets. Only fOUSG added borrowing power at the pin (92% collateral factor). The draft states the verified $8.68m market total and qualifies attribution of the existing loans. Reworked the threshold candidates around evidence and bridge or cross-fund overlap. Corrected the reach diagram’s Crypto Relief attribution. [Flux](docs/RESULTS.md#gated-collateral-and-open-lending) · [Candidates](docs/RESULTS.md#what-would-move-the-direct-verdict) · [Drafts](posts/DRAFTS.md)
- Preserved the public source URL, MIT license, card artifacts and existing quality records. The new public fixtures contain factual projections, hashes and publisher URLs. [Source register](docs/SOURCES.md) · [Checksums](evidence/SHA256SUMS)

## PARTLY DONE

- Compared November’s **1.325bn** Stellar trust-line units with **667.97m** September and **833.59m** October SEC shares. The top three addresses have no home domain and share a sponsor. The issuer list identifies neither those addresses nor the sponsor. **58.69%** describes a share of observed trust-line units only. The public evidence cannot resolve the transfer-agent accounting or allocate the September BENJI residual. [Stellar and SEC comparison](docs/HOLDERS.md#current-stellar-benji-and-solana-ustb)
- Identified the Crypto Relief donation wallet and confirmed control details for the Optimism BUIDL and Ethereum USYC Safes. Downstream backing remains open for all three, and the Optimism and USYC operators remain unidentified. [Safe evidence](docs/HOLDERS.md#pinned-safe-controls-and-operator-evidence)

## NOT DONE

- Complete September Stellar and Solana registers, beneficial-owner or fund-holder concentration, global bridge deduplication and pinned cross-asset look-through.
- Actual executed Nest swap volumes, executable depth beyond the tested sizes, and borrower-level Flux collateral attribution and recovery. The cited RPC calls are read-only quotes, balances, control reads and transfer simulations.
- Round four’s independent assessment. Rahil chooses the public estimand, approves or declines the USDtb card, and decides whether to post any draft.

## Reproduce the checks

Run from the project root. Use the workload gate described in the brief for the mutation batch, test matrix and live replay. Set `ROUND3_SCRATCH` to an existing task-owned disk directory for mutation copies and command outputs.

```sh
git diff --check
git diff --exit-code -- QUALITY.json docs/QUALITY.md LICENSE
sha256sum -c evidence/SHA256SUMS
TMPDIR="$ROUND3_SCRATCH" python3 -m unittest discover -s tests -v
TMPDIR="$ROUND3_SCRATCH" python3 tests/probe_round3.py --scratch "$ROUND3_SCRATCH"
python3 scripts/holder_audit.py
python3 scripts/kill_test.py
python3 scripts/check_post_card.py
python3 scripts/verify_pdf_facts.py
python3 scripts/replay_evidence.py --workers 1
```

The final **56-test** offline suite passed on Python 3.14.8. The workload-gated 54-test baseline passed on Python 3.10–3.14, and the four subsequently changed or added cases passed on all five versions. The public-tree check found 227 resolving relative links and no sensitive-text flags.

The full replay and targeted reruns matched **947** distinct historical or source comparisons, including **251** in the new market-controls fixture. The full pass had one transient Arbitrum error and the exact read matched on retry. The source check verified **23** fixture hashes and **15** transcription comparisons against three hash-verified publisher PDFs. The original USDtb card checker also passed.

The narrowly scoped replay uses `--fixture pinned-market-controls-2026-09-30`. If a public RPC rate-limits a historical read, rerun the named read with `--read FIXTURE/LABEL`. The replay reports mismatches and errors separately. [Live replay and publisher verification](docs/METHOD.md#repair-fixtures-and-replay)
