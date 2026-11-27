# Round-one repair handoff

**DONE — findings and sensitivity.** USDtb’s examined reserve report lists about $533m of BUIDL. The custody-inclusive estimate is $619.37m, with $241.93m supported by pinned balances and $377.43m from attested-only legs. Direct contracts account for $86.67m, or $15.03m without the dust-only mTBILL route. The new BUIDL scenario narrows the conditional direct range from 0.94%–62.20% to 1.45%–41.61%. Both ranges still span 5%. [Results and scenarios](docs/RESULTS.md)

**DONE — scope and drafts.** The report compares prior art, distinguishes onchain and examined amounts, documents the observed bridge implementations and adds a glossary. Four X drafts link to the public evidence. The original Proofline USDtb card passed its 12-word, artifact hash, contrast and layout checks and was inspected at full and phone widths. Design review is pending. [Method](docs/METHOD.md) · [Drafts and card](posts/DRAFTS.md)

**PARTLY DONE — deployment coverage.** Optimism BUIDL and Plume USTB now reconcile to pinned supply. The Optimism Safe’s role and the pinned secondary-access terms for the two Nest vault lots remain unresolved. The holder report gives request and failure records for small deployments and tests how much their full supply could move the bounds. Current Solana reads cover all five mint supplies plus BENJI’s largest returned token account. Four other largest-account requests failed at the tested endpoints. [Coverage details](docs/HOLDERS.md)

**NOT DONE — full September registers, global bridge deduplication and market depth.** The public evidence leaves some chain state and operators unknown. The current non-EVM supply scenario cannot certify September supply. A pinned quote tests one route at its stated size. The study leaves exit depth, recovery under a pause and the exact five-fund share unresolved. [Decisions](docs/DECISIONS.md#2026-11-26--round-one-quality-repair)

## Verification

Role key. Sol implemented the repair. Astra verifies and owns publication. Sonnet reviewed the earlier research and Opus recorded the historical round-one score. Use Python 3.10 or newer from the repository root. The offline checks passed on Python 3.10.21 and 3.14.8.

```sh
git status --short --branch
git diff --check
git diff --exit-code -- QUALITY.json docs/QUALITY.md LICENSE
sha256sum -c evidence/SHA256SUMS
python3 -m unittest discover -s tests -v
python3 scripts/holder_audit.py
python3 scripts/kill_test.py
python3 scripts/check_post_card.py
```

All 22 offline tests and 19 fixture checksums passed. The clean public-tree audit checked 177 relative Markdown links and found no credential patterns or private paths. Eight isolated code mutations were rejected, including removal of the Franklin check, widening the reserve tolerance, removing the mTBILL supply cap and ignoring a nonzero Frax mint counter. Use the optional live checks from [the method](docs/METHOD.md#repair-fixtures-and-replay). The first command replays saved historical evidence and reports mismatches and endpoint errors by read. The full pass matched 677 checks and encountered one Arbitrum HTTP 429. The exact-read retry matched the remaining check, for 678 matches and zero mismatches across the two runs. The PDF verifier passed 15 checks against three hash-verified publisher files fetched to an empty directory. Its normal destination is ignored `data/upstream/`. A separate supplement refresh completed with live results or explicit per-request errors in ignored storage.

```sh
python3 scripts/replay_evidence.py --workers 1
python3 scripts/replay_evidence.py --fixture round1-supplement \
  --read round1-supplement/bridge/buidl/arbitrum/implementation --workers 1
python3 scripts/verify_pdf_facts.py
```

## Rahil’s decisions and review

Choose the public lead, approve the exact card and decide whether to publish a draft. The original-code license is recorded on the public base. Review the revised slice independently after Astra verifies and commits it. [Historical round-one review](docs/QUALITY.md) · [Public repository](https://github.com/RahilBhavan/rwa-allowlist-leakage)
