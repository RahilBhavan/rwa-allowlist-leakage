# Method

This document explains the September 30 snapshot, the bounds and how to reproduce them.

## Snapshot and scope

Use September 30, 2026 because the USDtb reserve report has a precise month-end pin and all five funds have usable primary figures or ceilings for the same reporting period. EVM state is from the last block at or before **23:59:59 UTC**. Each captured header and successor verifies the timestamp bracket. The Circle and Securitize corporate disclosures and the Franklin filing use the reporting date. Superstate uses its daily NAV and AUM stamp. Ondo’s daily TVL series has midnight UTC labels and displays an evening reporting convention. Reconcile the September 29 through October 4 publisher marks with pinned native Ethereum supply and XRPL issuer obligations. Apply separate reporting-time and unseen-chain allowances. [OUSG denominator model](RESULTS.md#denominator-sensitivity)

Measure a gross five-fund supply basket. It may include both parent fund shares and a fund that invests in them. That deliberately larger denominator puts downward pressure on the aggregate lower share. Count each numerator position once by underlying fund, chain and holding address. Ignore later derivative layers such as accumulating yield tokens or LP tokens backed by the same stablecoin issuance. All stablecoin reserve values here describe dependence of the stablecoin’s backing on the funds, without passing through fund yield or shareholder rights.

## What qualifies

- **Direct wrapper contracts.** The underlying balance has to sit at a documented contract for the wrapper with code at the pin. The publicly obtainable representation must have an economic link to the held fund token. The Midas USTB vault, Usual USD0 collateral treasury and attributable STBL OUSG vault backing qualify. The Midas result relies on a dust-only quote. A sensitivity removes it from both backing totals and leaves its status open for the upper bound. Both Frax custodians showed zero route-local minted frxUSD. Their balances are included in the documentary-reserve sensitivity. Anchorage’s two pinned EVM custody balances are strict exclusions. The two attestation-only custody entries remain unresolved for strict purposes.
- **Custody-inclusive backing.** Include the direct-wrapper positions and separately attested bank reserve custody with a documented economic link and pinned downstream acquisition. The September Anchorage report supplies the four USDtb reserve legs. This is the companion to the primary direct-contract test.
- **Unclassified.** Missing balances, role, access, or economic linkage stay unclassified. Treasury labels, deposits, liquidation channels, and the ability to borrow from a market are insufficient on their own. No venue or chain receives a zero exposure estimate for missing data.
- **Access.** Evaluate acquisition on open secondary markets separately from issuer onboarding, blacklist/freeze authority, sanctions controls, liquidity at size, and primary redemption. A pool quote is a read of the market at its pin. Curve’s code and published pool identity establish the route. Anchorage’s issuer terms and reserve disclosure establish custody and explain the primary service relationship.

## Denominator evidence

| Fund | Denominator and why it covers missing chains |
| --- | --- |
| BUIDL | Securitize’s $4.8 billion September 30 platform total for **all** tokenized fund and equity assets includes BUIDL’s tokenized classes. Use a full $0.1 billion increment above the displayed figure for a $4.9 billion ceiling. The floor is the largest of the individual observed classes and the sum of verified distinct positions. The headline avoids cross-chain supply summation. A separate deployment-based scenario uses the gross sum. Use $1 per native unit for historical contract balances, corroborated by Anchorage’s reserve units and fair value. |
| USTB | Superstate’s September 30 AUM is $754,872,051.01 at NAV $11.229908. It includes Ethereum, Solana, Plume and book-entry shares. The ceiling therefore also covers the sounder, narrower meaning of tokenized supply. Pinned Ethereum supply of 50,620,204.672699 shares at the daily NAV gives the floor. Plume has pinned supply and holder ranks. Solana’s historical breakdown remains open. |
| USYC | Circle’s quarter-end company data shows $2.4 billion of USYC assets. Widen by a full display increment on each side, $2.3–2.5 billion. Ethereum supply 36,774,089.914760 and BNB Chain supply 2,073,937,727.947452 are cross-checks. Use the Ethereum oracle NAV of $1.13879192 published 12:53:11 UTC. The BNB Chain leg alone is approximately $2.362 billion at the Ethereum oracle NAV, assumed to apply to BNB units. Circle’s product-level total covers other deployments. We leave bridge locking and net supply unresolved and use BNB alone for the strict exclusion. Circle lists Arc, BNB Chain, Canton, Ethereum, NEAR and Solana. |
| OUSG | Distinct canonical Ethereum and XRPL units mark to $319.66m at the September 30 displayed price. Use the six-mark low NAV for a $319.63m conditional pinned floor, the greater of high-NAV pinned units and the highest adjacent issuer mark as the ceiling basis, and separate $10m time/NAV and $25m unknown-chain allowances. The modeled ceiling is $356.23m. Omit rOUSG to avoid duplicating OUSG and leave Solana unresolved. [Scenario table](RESULTS.md#denominator-sensitivity) |
| BENJI | SEC Form N-MFP3 for Franklin OnChain U.S. Government Money Fund series S000067043, class C000215714, reports $667,960,091.75 for its single class and 667,967,346.6700 shares. Series-level scope covers the fund’s blockchain deployments and any recordkeeping distinctions without summing balances across chain registries. |

## Network pins and addresses

Addresses, calldata, endpoints, block brackets and measured values are in the [EVM fixture](../evidence/evm-2026-09-30.json) and [holder capture](../evidence/holders-2026-09-30.json). The EVM fixture covers initial supply and reserve observations. The [chain and class ledger](HOLDERS.md) covers the expanded scope, including Arc disclosures and separately pinned Base, Plume and XRP Ledger. Anchorage custody supplies the primary BUIDL custody-inclusive numerator. The Frax-linked BUIDL position contributes only to the documentary attribution sensitivity. Per-deployment supplies are cross-checks. Their sum is not assumed to be canonical.

| Network | EVM block | BUIDL native shares observed | Use |
| --- | ---: | ---: | --- |
| Ethereum | 26,093,737 | 203,389,187.177549 and 239,844,535.090100 I Class | Frax holdings and code, Curve coins, balance and quote, USTB and USYC data. |
| BNB Chain | 125,000,754 | 146,619,491.330000 | Anchorage reserve balance and code, USYC supply. |
| Avalanche | 96,488,899 | 486,533,969.520000 | Anchorage reserve balance and code. |
| Arbitrum | 510,496,863 | 8,577,422.390000 | Supply and issuer-listed bridge balance. |
| Optimism | 157,607,011 | 26,472,554.590000 | Supply, issuer-listed bridge balance and complete holder ranks. |
| Polygon | 94,738,439 | 7,540,191.030000 | Supply and issuer-listed bridge balance. |
| Tempo | 42,021,929 | 17,102,298.050000 | Supply check only. |
| Solana | Issuer report timestamp | Total unknown | Schedule II reports BUIDL reserve custody at `HYP6YSsagbnNtENSXbvNE95a6SUM83fLXiFYQMqLM9sz`. |
| Aptos | Issuer report timestamp | Total unknown | Schedule II reports BUIDL reserve custody at `0xb95ce931098b76d171652108644838eeb3584a6bf89751b0c406b0a223d809a4`. |

The BNB Chain and Avalanche address `0x2004F7f7B600d962170d7f28114Cc123c5e98451` is a custody address on each chain. Neither returns code at the pin. USDtb’s Ethereum contract is `0xC139190F447e929f090Edeb554D95AbB8b18aC1C`. Its Solana mint is `8yXrtJ54jZtE84xEBzTESKuegjcAkAuDrdAhRd8i8n3T`. The Curve pool `0xC2921134073151490193AC7369313c8e0b08e1e7` is separate from both. The frxUSD Curve pool is `0x13e12BB0E6A2f1A3d6901a59a9d585e89A6243e1`. The Frax Ethereum BUIDL contract is `0xe827abf9f462ac4f147753d86bc5f91e186e4e9c` and the Frax USTB contract is `0x5fbAa3A3B489199338fbD85F7E3D444dc0504F33`. The ETH Frax-linked fund contracts are `0x7712c34205737192402172409a8f7ccef8aa2aec` for BUIDL and `0x43415eb6ff9db7e26a15b704e7a3edce97d31c4e` for USTB. See [source register](SOURCES.md) for links.

## Bound arithmetic and rerun

If `V` is verified qualifying value, `X` is verified excluded value and `Dmax` is the denominator ceiling, bound the share by `V / Dmax` and `1 - X / Dmax`. Sum USD components before dividing, then compare against 5% at full precision. Continue at a lower bound of 5% or more. Conclude below the cutoff only when the upper bound is strictly less than 5%. Classify any overlap as inconclusive. The unclassified balance at the ceiling equals unresolved coverage at the modeled floor plus the additional supply allowance. For each fund the floor also incorporates distinct classified balances when they exceed the initial proxy floor. In the calculation output, `verified_usd` is the total qualifying backing used for that estimate. Its `onchain_backing_usd` and `attested_only_backing_usd` fields distinguish balances corroborated onchain from dollar values supported by the examined report alone.

```sh
/usr/bin/python3 scripts/kill_test.py
/usr/bin/python3 -m unittest discover -s tests -v
sha256sum -c evidence/SHA256SUMS
```

Optional keyless replay of a single chain to another path. It does not overwrite the offline evidence. Use the published fixtures for the reproducible calculation and treat new live RPC errors as missing reads.

```sh
/usr/bin/python3 scripts/fetch_evm.py --chain ethereum data/ethereum-live.json
```

For the full EVM refresh, pass a scratch output path and omit `--chain`. Historical RPC state availability varies by provider. The original PublicNode archive state calls asked for a token; dRPC, Blast API and the official Avalanche and Tempo endpoints recovered the specified EVM reads. The timestamp locator was only a block-number hint. Primary RPC block timestamps ground the pin. A historical SOL supply query cannot be pinned with `getTokenSupply`, which returns current mint supply and has no historical block parameter. The public Aptos full node reports a recent oldest ledger version, beyond the snapshot. The project uses attestation evidence and all-chain denominator ceilings for those gaps.

## Slice 2 candidate discovery and ranking

1. Pull a current keyless Routescan holder page, sample bounded indexed `Transfer` pages ending at the pin, and add addresses from protocol deployment books. ERC-20 logs give addresses whose historical net event flows may be informative even with incomplete pagination. Ignore malformed log records and non-Transfer events. Current holder weights and reconstructed net flows never enter the result.
2. For BNB USYC, compare `totalSupply` between September 15 (candidate block 121,929,907) and the pin. Bisect between different totals to find an adjacent pair crossing into the pin value. No monotonic supply assumption is required to find one such pair. Query block 123,939,578 receipts on the official BNB RPC and keep the USYC events. A direct transaction receipt subsequently corroborates the transfer chain and burn. [Discovery fixture](../evidence/usyc-bnb-receipt-2026-09-25.json)
3. Check that the block timestamp and its linked successor bracket the cutoff. Pin `balanceOf`, `totalSupply`, `decimals` and `eth_getCode` to that height. Apply the certificate formula in [holder coverage](HOLDERS.md). Missing or failed RPC results are unknown. The share-of-supply calculation separates issuer operations, third-party stablecoin reserve custody, code-bearing contracts, EOAs with signer or delegation evidence, other no-code holders, observed balances with unknown control and the unobserved supply residual. Code class records no runtime, EIP-7702 designation, ordinary contract code or unresolved code. Entity roles require documentary evidence. A no-code account is EOA-compatible at the pin. A prior signed outer transaction strengthens EOA attribution where available. Ultimate custody remains unresolved unless independently identified.
4. For OUSG on XRPL, query all issuer trust-line pages at the hash of validated ledger 107,347,788. Filter to the exact currency code, then invert the issuer-view negative balances to get outstanding amounts. Independently compare `gateway_balances` obligations to the sum within its published numeric precision. `account_info` documents the issuer’s `ondo.finance` domain and require-authorization flag. Trust-line holders are ranked by account. The ownership or control of a trust-line account remains outside this proof.

The wider discovery run sampled up to six log pages and 25 indexed holders per supported target. Its output and the bounded first-page capture were combined by identical block and successor, preferring the wider run with earlier successful reads retained for missing results. Public-node failures include archive authorization, range caps and throttling. Routescan did not index several networks, and BSC and cross-chain broad log queries were unsuccessful. The [target inventory](../evidence/holder-targets.json) supplies machine-readable contract identities and calldata. [Holder coverage](HOLDERS.md) distinguishes closed, partial and unresolved deployments.

## Strict exclusions and prices

Strict `X` includes code-free balances from one pinned and supply-checked deployment per anonymous group (Avalanche BUIDL, Ethereum USTB, Ethereum OUSG, Ethereum BENJI) and the proved rank-1 no-code BNB USYC balance. Anchorage’s independently confirmed **BNB** reserve is separately recognized as a disclosed BNB native share class. Anchorage’s **Avalanche** balance is part of that chain’s no-code subtotal. Numeric reserve positions on EVM use exact pinned units at $1. The Solana and Aptos custody entries retain their examined report backing status, with a full $1 display increment removed from each economic lower-bound amount. Their technical control stays unresolved.

The exact-balance, same-token collateral receipts for Horizon USTB, Horizon USYC and Flux OUSG qualify as strict exclusions. The direct collateral receipt cannot be obtained by open secondary buyers according to the protocol’s transfer rules. Stablecoin loan receipts transmit credit risk through a different asset and remain visible in the protocol map. Code-bearing addresses with an unresolved role, bridges, and any unsupported owner classification stay within the ceiling. USTB uses the daily NAV. OUSG strict exclusions and STBL valuation use the lowest of the six daily prices to avoid tightening the bound at a higher daily mark. BENJI strict exclusions use September filing net assets divided by shares as the common pro rata NAV. See [results](RESULTS.md) for the denominator mismatch checks and [sources](SOURCES.md#slice-2) for the corroborating protocol and offering evidence.

## Observable verification

The [rank audit](../scripts/holder_audit.py) certifies rank from the supply residual, even when an index returns a different live order. The [bound calculation](../scripts/kill_test.py) checks the exact historical BNB burn and supply delta, recomputes the Usual collateral relationship and DEX quote checks, verifies the gated receipts’ underlying addresses, and applies the reserve distinctions. The tests reject mixed pins, unreconciled or omitted balances masquerading as verified ranks, incomplete trust-line pagination, missing Usual linkage or quote, duplicate positions, and strict exclusion of attestation-only reserve custody.

```sh
/usr/bin/python3 scripts/holder_audit.py
/usr/bin/python3 scripts/kill_test.py
/usr/bin/python3 -m unittest discover -s tests -v
sha256sum -c evidence/SHA256SUMS
```

Optional live verification in ignored storage. Apply the workload gate in [the brief](../BRIEF.md) before a full holder discovery run. The offline count uses the saved addresses and state. Live index order and RPC availability can change independently of the pinned balances.

```sh
mkdir -p data/replay
/usr/bin/python3 scripts/fetch_holders.py data/replay/priority.json \
  --log-pages 1 --index-limit 12 --target usyc/bsc --target usyc/ethereum \
  --target buidl_i/ethereum --target ustb/ethereum
/usr/bin/python3 scripts/fetch_xrpl_holders.py data/replay/ousg-xrpl.json
```

## Repair fixtures and replay

The [repair fixture](../evidence/review-ethereum-2026-09-30.json) is checked against the same block and successor as the holder snapshot. Midas is valued at Superstate’s NAV, with its redemption vault identified via the implementation slot, token and helper addresses and burn role. The no-hook pool’s initialize log precedes the pin. The Uniswap quote uses the same PoolKey and an input of 0.0001 ETH. The separate transfer probe calls the ERC-20 from PoolManager using historical state. STBL’s gross vault balance is capped by recorded net fund units, deposit stable value less haircut and Ethereum USST issuance. Convert those USD caps with the high OUSG NAV and price the resulting attributed units with the low NAV. Frax local mint counters, Flux control settings and Safe observations are in the same fixture.

### Full replay and publisher checks

Run from the repository root. The first command is a network-free calculation over the frozen fixtures. The live replay compares every saved successful historical RPC observation in the EVM, holder, Ethereum review, signer, receipt, XRPL and supplemental files. It also checks the recorded Sourcify discovery projections and Usual and Securitize source hashes. It exits nonzero for a mismatch or a source error and prints per-fixture counts. Explorer candidates and non-pinned Solana and Aptos snapshots can change. Refresh them separately with the supplement command. Unavailable discovery queries are individually recorded in the supplement.

```sh
python3 scripts/kill_test.py
python3 scripts/replay_evidence.py --workers 1
python3 scripts/verify_pdf_facts.py
mkdir -p data
python3 scripts/fetch_supplement.py data/live-supplement.json
```

For a focused replay, use `python3 scripts/replay_evidence.py --fixture review-ethereum-2026-09-30 --fixture review-contract-discovery --fixture usual-source-2026-09-30`. EVM replay uses published RPCs and, when a primary endpoint errors, can retry on the listed Ethereum or Optimism alternative. The historical outputs can be independently compared even when an explorer has changed. Use `--read FIXTURE/LABEL` for a specific rate-limited observation and `--pause` to space queries. [Replay code](../scripts/replay_evidence.py)

The PDF check requires Poppler’s `pdftotext`. It downloads the original documents into ignored `data/upstream/` as needed, verifies all three full-file hashes and checks the keyed dollar values against the transcriptions. It covers the Securitize platform total and its footnote scope, Circle’s USYC assets slide, and Anchorage’s total BUIDL, implied per-unit value, network legs and custody addresses, plus USDtb redeemable totals. PDF files, extracted text and verified contract source bodies stay off the public tree. [PDF check](../scripts/verify_pdf_facts.py) · [Source records](SOURCES.md)

## BUIDL supply and bridge check

The Securitize public feed identifies the EVM contracts, Solana mint and six EVM bridge addresses. All six issuer-listed bridge addresses have zero BUIDL balance at the pin. The Ethereum and BNB Chain proxy implementation slots point to separately verified implementations. Both burn on the outgoing path and issue on receipt. The same implementation address is recorded on Arbitrum, Avalanche, Optimism and Polygon as on Ethereum. The source identification is for the pinned Ethereum and BNB Chain implementations. Address equality across other chains does not by itself certify bytecode identity. Tempo and Ethereum BUIDL-I have no bridge address in the feed, and the feed has no Solana or Aptos bridge address. The Aptos supply probe uses the fungible asset metadata address, distinct from the program address published in the feed. [Issuer feed](https://public-feed.securitize.io/asset-info?symbol=BUIDL) · [Bridge implementation and balance receipts](../evidence/round1-supplement.json)

Ethereum’s top two holders of the original class had no runtime code. The unresolved Ethereum original-class holder residual, other contracts and untested routes leave room for hidden custody. The zero balances and code support burn-and-issue for the tested bridge paths. They cannot rule out lock-and-mint through other addresses or prove fund-wide uniqueness. A lock-and-mint duplicate inside the gross sum would inflate that sum. A missing deployment or higher September non-EVM supply could raise actual September supply above the scenario. No bridge amount is subtracted. Keep the broad platform-based headline and use the deployment sum as a sensitivity with the displayed assumptions. [Holder evidence](HOLDERS.md) · [BUIDL scenario](RESULTS.md#buidl-deployment-scenario)

## Glossary

| Term | Meaning here |
| --- | --- |
| Direct contract backing | Fund units held by a contract and attributable to a downstream token that passed the tested access checks. |
| Reserve custody | Fund units held to back a third-party stablecoin, such as Anchorage’s BUIDL for USDtb. Custody role and runtime account type are separate. |
| Excluded from the direct upper bound | Value supported by evidence of no runtime code or a gated receipt under the model’s counting rules. |
| Supply allowance | Extra value between the observed or modeled supply floor and the modeled ceiling. Unknown holder roles also create unresolved coverage within observed supply. |
| Route-local | A state value belonging to one contract or mint route. Frax’s route-local minted counter measures issuance attributed to that route. |
| Dust-only route | A route evidenced only at a very small input and, in the observed mTBILL case, with a 79% LP fee. |
