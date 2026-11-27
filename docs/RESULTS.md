# September 30, 2026 holder test

This report gives the measured positions, conditional bounds and unresolved coverage at the September cutoff.

## Direct-contract test

On **September 30, 2026** the conditional direct-contract bounds for **BUIDL, USTB, USYC, OUSG and BENJI** were **0.94%–62.20% by value**. The bounds straddle the brief's **5%** cutoff. The qualifying positions were Midas’s USTB redemption vault for mTBILL, Usual’s USYC collateral treasury for USD0, and the attributable portion of STBL’s OUSG vault for USST. The EVM snapshot uses the last block at or before **23:59:59 UTC**. The fund figures use the reporting dates and conventions detailed below. [Cutoff in the brief](../BRIEF.md) · [Snapshot and scope](METHOD.md#snapshot-and-scope)

`python3 scripts/kill_test.py` emits `date`, `threshold`, the underlying `positions`, and the two estimates as `direct_contract_holdings` and `economic_exposure`. The table reports USD millions to nearest, lower shares down and upper shares up. The code compares unrounded values to the cutoff. BUIDL and BENJI each have a zero direct lower bound under the strict evidence threshold. [Calculation and classification rules](METHOD.md#bound-arithmetic-and-rerun)

| Fund | Denominator ceiling | Direct verified | Strict excluded | Direct share interval | Economic backing verified | Economic share lower |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BUIDL, including I Class | 4,900.00 | 0.00 | 597.95 | 0.00–87.80% | 532.70 | 10.87% |
| USTB | 754.87 | 71.64 | 386.56 | 9.48–48.80% | 71.64 | 9.48% |
| USYC | 2,500.00 | 14.03 | 2,361.78 | 0.56–5.53% | 14.03 | 0.56% |
| OUSG | 356.23 | 1.00 | 75.18 | 0.28–78.90% | 1.00 | 0.28% |
| BENJI / FOBXX | 667.96 | 0.00 | 48.24 | 0.00–92.78% | 0.00 | 0.00% |
| **Total** | **9,179.06** | **86.67** | **3,469.71** | **0.94–62.20%** | **619.37** | **6.74%** |

At the **$9.17906bn** modeled ceiling, 5% corresponds to **$458.95m**. The **$5.623bn** between verified and excluded balances and the modeled ceiling comprises **$1.351bn** of unresolved coverage at the modeled floor and **$4.272bn** of denominator slack. The upper endpoint therefore combines missing coverage, including unknown holder roles and access, with room in the supply model. Most denominator slack comes from using Securitize’s whole-platform figure for BUIDL. Treat 62.20% as a coverage ceiling under these assumptions. [Bound calculation](../scripts/kill_test.py) · [Coverage by holder class](HOLDERS.md#share-of-pinned-deployment-supply)

## Custody-inclusive backing

Including Anchorage’s BUIDL reserves adds **$532,696,708.18** after reporting adjustments. The custody-inclusive total of **$619.37m** is a **6.74%** rounded-down lower bound for the same basket. This companion clears 5% and relies on Anchorage’s examined Solana and Aptos reserve legs. Removing those two legs leaves **$241.93m** and a **2.63%** lower share. The arithmetic upper bound is 100% because the strict exclusions address contract form or receipt access. [Calculation and sensitivity](../scripts/kill_test.py) · [USDtb bank custody](#usdtb-bank-custody)

## Evidence that moves the bounds

### USYC on BNB Chain

The address `0x87433fec6f8d9df13d1e17c4b11364ecd2e93a51` held **2,073,937,717.945368 USYC**, leaving **10.002084** of the deployment’s pinned supply elsewhere. A supply change located block 123,939,578. Matching `Transfer` logs in its receipts show the address transferring 25 million USYC into the redemption/burn path on September 25. September 30 `balanceOf`, `totalSupply` and `eth_getCode` verify its rank and lack of runtime code at the pin. The $2.362bn strict exclusion applies the contemporaneous Ethereum USYC NAV to BNB units. Circle describes an institutional Binance custody arrangement without attributing this holder address. [Receipt evidence](../evidence/usyc-bnb-receipt-2026-09-25.json) · [Pinned reads under `usyc/bsc`](../evidence/holders-2026-09-30.json) · [Circle announcement](https://investor.circle.com/news/news-details/2025/Circles-USYC-Now-Supported-as-Yield-Bearing-Off-Exchange-Collateral-for-Binances-Institutional-Clients/default.aspx)

### Usual USD0 collateral

The **12,320,132.708463 USYC** in Usual's Ethereum collateral treasury qualifies as **$14,030,067.58** of direct USD0 backing at the pinned Ethereum USYC NAV. At block 26,093,737, USD0 DaoCollateral's implementation routes deposits into its configured treasury and draws collateral redemptions from it. The treasury pointer equals the funded contract, the token mapping marks USYC eligible, and the treasury allowance to DaoCollateral covers the balance. DaoCollateral itself holds zero USYC. See `observations.usual_usd0_verified` for the collateral and quote checks. [Implementation manifest](../evidence/usual-source-2026-09-30.json) · [Pinned reads under `usyc/ethereum`](../evidence/holders-2026-09-30.json)

USD0's implementation checks blacklist and pause status on transfers. At the pin USD0 was unpaused and the Curve pool held **404,823.235297858206754919 USD0**, quoting **1.001064975518393547 USD0** for 1 USDC. Ethereum USD0 supply was **546,650,642.502627572424541858**. The counted USYC is one collateral leg. A buyer on the covered route obtains USD0. Circle's eligibility and entitlement rules govern direct USYC access. [Curve registry row](../evidence/curve-usd0-pool.json) · [Fund and secondary routes](REACH.md#usyc)

### BUIDL and BUIDL-I

Ethereum Frax holds **15,830,037.48 BUIDL** with zero route-local minted frxUSD at the pin. Its liability attribution stays open. The Avalanche inventory fully reconciles to total supply, with **486,524,729.52 BUIDL** in no-code locations and **9,240 BUIDL** at the sBUIDL wrapper. The BNB Anchorage reserve adds **111,424,957.65 BUIDL** to the strict exclusion, supported by the separately disclosed native BNB share class. Ethereum BUIDL-I ranks fully reconcile and Grove’s Ethereum ALMProxy holds **119,322,905.35 BUIDL-I**. Sky governance ties Grove’s investments to an allocator credit line. Exact reserve attribution to USDS and an open direct Grove receipt for the holdings remain unverified. BUIDL-I rank 2 holds **112.91m** in a pinned 4-of-7 Safe. Its operator and economic link to any downstream token remain unresolved. The Avalanche sBUIDL secondary acquisition route also remains unresolved at the pin. Euler's collateral listing evidence concerns Ethereum. [Pinned holder reads](../evidence/holders-2026-09-30.json) · [Holder coverage](HOLDERS.md) · [Protocol map](REACH.md)

### Midas mTBILL

Ethereum USTB rank 2 is Midas’s USTB-backed redemption vault at `0x569d7dccbf6923350521ecbc28a555a500c4f0ec`. Its **6,379,144.864074 USTB** equals **$71,637,209.94** at Superstate’s September 30 NAV. The pinned implementation matches verified `RedemptionVaultWithUSTB` source. `mToken()` points to mTBILL, `ustbRedemption()` points to a helper that names USTB and USDC, and the vault holds mTBILL’s burn role. The proxy admin is owned by the Midas timelock listed by the protocol. The separate Midas access controller manages operating roles. Both the vault and token were unpaused. The implementation burns mTBILL on instant redemption and can convert the held USTB to cover a USDC shortfall. At the pin Ethereum had **67.71m mTBILL**, worth about **$72.70m** at its pinned **$1.07370197** feed, above the attributed USTB lot. [Historical reads](../evidence/review-ethereum-2026-09-30.json) · [Midas sources and offering evidence](SOURCES.md#independent-review-repair)

An initialized, hook-free Uniswap v4 pool had active liquidity at the pin. Its quoter returned **0.062855948318360643 mTBILL for 0.0001 ETH** with a **79% LP fee**. A separate read-only call accepted an mTBILL transfer from PoolManager to an address without the Midas greenlist role. Verified token code checks pause and blacklist on transfers. The quote establishes a costly small-size route. Trading depth and primary redemption remain separate from this access test. [Pool event, state, quote and token checks](../evidence/review-ethereum-2026-09-30.json)

### STBL USST

STBL’s registry at the pin maps OUSG PT1 to the observed rank-12 vault, its OUSG token and authorized deposit issuer. The vault held **8,693.543272 OUSG** and recorded **8,648.511182 OUSG** in net deposits. Its USD deposit ledger less cumulative haircuts supported **$1,002,487.94** of net stable value. Curve held **128,071.3174 USST** and quoted **1.0003214355 USST for 1 USDC**. A read-only transfer from Curve to the test address also succeeded. The calculation conservatively counts **$1,002,076.35**, capped in units by the recorded net stable value at the high OUSG price and translated at the low price. Remaining vault inventory, YLD rights, and other STBL markets stay outside the verified amount. [STBL evidence and source](SOURCES.md#independent-review-repair) · [Pinned fixture](../evidence/review-ethereum-2026-09-30.json)

### Frax frxUSD attribution sensitivity

The pinned Frax BUIDL custodian held **$15.83m** and the USTB custodian held **1,729,693.761124 USTB**, worth **$19.42m**. Both `frxUSD()` and `custodianTkn()` returned the expected tokens. Both `frxUSDMinted()` counters read **zero**. In the verified implementations a redemption can burn fungible frxUSD with the route’s counter already zero. Redemptions can draw down pooled inventory subject to eligibility and available collateral, so zero local mint accounting leaves system-wide liability attribution open. The primary numerators leave both lots unresolved. Treating the two documented reserve balances as attributable adds **$35.25m** and gives a **1.32%** direct lower bound and **7.13%** custody-inclusive lower bound. [Frax source and pinned reads](SOURCES.md#independent-review-repair) · [Sensitivity calculation](../scripts/kill_test.py)

### BENJI and unresolved holdings

The EVM BENJI censuses reconcile Ethereum and Avalanche. The strict bound uses Ethereum only to avoid summing registry representations across chains. The September SEC filing corroborates the fund denominator. Ondo’s public holdings disclosure provides a BENJI portfolio lead. Its September 30 BENJI allocation and holder identity remain unverified. [Coverage by fund and chain](HOLDERS.md) · [Franklin filing readback](../evidence/franklin-filing-readback-2026-09-30.json)

### Gated collateral and open lending

Horizon held **1,410,692.832857 USTB** and **100 USYC**. Flux’s Ethereum fOUSG contract held **336,339.561725865749857494 OUSG**. Pinned reads identify the underlying tokens. The protocol transfer rules restrict those collateral receipts, so these receipts are strict exclusions. Flux's open stablecoin lending can still expose lenders to a borrower's default and to the recovery value obtainable by eligible liquidators. The pinned Comptroller showed fOUSG mint unpaused and borrowing paused. Both controls were unpaused for fUSDC. The separate admin and pause guardian and the market-level fUSDC `totalBorrows()` read are in the evidence. Borrower-level attribution to OUSG remains open. That credit path stays outside both backing numerators. [Pinned balances and underlying](../evidence/holders-2026-09-30.json) · [Pinned Flux control reads](../evidence/review-ethereum-2026-09-30.json) · [Protocol terms and recovery paths](REACH.md#six-protocol-collateral-and-redemption-pause-map)

### USDtb bank custody

Anchorage's examined report itemizes **$532,696,711 of BUIDL** backing USDtb across Solana, Aptos, Avalanche and BNB Chain in Schedule II. The economic measure includes all four after conservative rounding adjustments. The Avalanche and BNB Chain custody addresses have historical no-code corroboration and enter the strict exclusion once each. The Avalanche leg is already included in its no-code subtotal. The Solana and Aptos legs remain unresolved for strict classification. At the Ethereum pin the Curve USDtb pool held **10,484,993.79 USDtb**, quoting **1.000011446292664265 USDtb** for 1 USDC. [Anchorage report, Schedules I–II](https://learn.anchorage.com/09.30.26_USDtb-Stablecoin-Attestation-Report-signed.pdf) · [Pinned reads](../evidence/evm-2026-09-30.json) · [Curve registry row](../evidence/curve-usdtb-pool.json)

### Covered secondary markets

The crvUSD/frxUSD pool held **5,441,463.32 frxUSD**, quoting **0.999470742651074479 frxUSD** for 1 crvUSD. The primary counted positions use the Midas, STBL, USD0 and USDtb routes above. This frxUSD quote supports the reserve-attribution sensitivity. The evidence covers pool inventory and read-only quotes at the pin. Execution remains subject to token controls, and liquidity at size is unknown. This study follows dependence on reserve assets. Fund ownership, pass-through yield and primary redemption eligibility follow the applicable issuer and offering terms. [Pinned Ethereum capture](../evidence/evm-2026-09-30.json) · [frxUSD registry row](../evidence/curve-frxusd-pool.json) · [Issuer terms and pool code](SOURCES.md)

## Denominator sensitivity

The gross basket uses fund-level values or wider proxies. Missing deployments and book-entry shares are covered to the extent the relevant disclosures include them. Parent fund holdings can overlap with a constituent fund's portfolio. The bounds rely on the following assumptions about scope, rounding and valuation. [Denominator method](METHOD.md#denominator-evidence)

- **BUIDL and USYC.** Use the September 30 point-in-time disclosures. Securitize reports **$4.8bn** of all tokenized assets on its platform, including equity and funds. The Q3 average reported separately is **$5.0bn**. Circle reports **$2.4bn** of USYC assets at quarter end. Treat each point-in-time disclosure as rounded and add a full displayed increment (**$0.1bn**) to each for the **$4.9bn** and **$2.5bn** ceilings. The headroom is a modeling choice. The BUIDL ceiling depends on the platform metric covering all relevant classes. The USYC ceiling depends on the product metric covering the relevant deployments. Use $1 per BUIDL and apply the pinned Ethereum USYC oracle NAV to BNB units as well as Ethereum units. The BNB NAV assumption affects the major strict exclusion. [Securitize release, platform metric and footnote 2](https://www.sec.gov/Archives/edgar/data/2094496/000162828026072463/exhibit991-secz3q26earning.htm) · [Circle Q3 slide 12](https://s206.q4cdn.com/265218871/files/doc_earnings/2026/q3/presentation/3Q26-Earnings-Presentation.pdf#page=12) · [Transcription and headroom](../evidence/primary-transcriptions-2026-09-30.json)
- **USTB and BENJI.** Use Superstate's daily AUM and NAV, with AUM covering book-entry shares. Use Franklin's September filing net assets and implied NAV across BENJI representations, with only Ethereum counted toward the strict exclusion. [Superstate daily row](../evidence/superstate-ustb-2026-09-30.json) · [Franklin filing reference and transcription](SOURCES.md)
- **OUSG.** Ondo’s September 30 midnight label is **$312.94m**. At the 23:59:59 UTC pin Ethereum and XRPL supply totals sum to **2,738,455.1447673774 OUSG**, worth **$319.66m** at the September 30 displayed price. Ethereum’s native OUSG ERC-20 and XRPL’s direct issuer obligations have separately documented subscription/redemption rails. The working floor assumes distinct native issuance and omits rOUSG and other receipts, zero Polygon supply, and unknown Solana supply. At the lowest of the six observed NAVs the two-chain floor is **$319.63m**. At the highest NAV the same units imply **$319.76m**. If the native-issuance assumption fails, the larger single deployment supports only **$187.41m** of floor using the same low NAV. That change moves dollars from floor coverage into denominator slack while keeping the headline shares unchanged at a fixed ceiling. [Pinned counts and gaps](HOLDERS.md) · [Issuer deployment and reporting evidence](SOURCES.md#independent-review-repair)

Ondo’s October 2–4 marks of **$319.73m**, **$319.76m** and **$321.23m** exceed the old **$319.69m** ceiling. The new basis is the greater of the pinned high-NAV value and the highest observed issuer mark across September 29–October 4. Add **$10m** for reporting-time/NAV mismatch, rounded above the largest adjacent daily move in that window, and a separate **$25m** scenario allowance for unseen Solana or other scope. This gives **$356.23m**. The $25m is a modeling allowance without a pinned chain maximum. The resulting ceiling is conditional on those scope and reporting assumptions. [Issuer marks](../evidence/ondo-ousg-2026-09-30.json) · [Subsequent adjacent marks](../evidence/ondo-ousg-adjacent-2026-10.json) · [Model](../scripts/kill_test.py)

| OUSG scenario | OUSG ceiling | Aggregate direct range | Aggregate custody-inclusive lower |
| --- | ---: | ---: | ---: |
| Highest reconciled observation, before allowances | $321.23m | 0.94–62.06% | 6.77% |
| $10m time and $25m unknown-chain allowances | $356.23m | 0.94–62.20% | 6.74% |
| Double both allowances | $391.23m | 0.94–62.35% | 6.72% |
| Double the modeled OUSG ceiling | $712.45m | 0.90–63.62% | 6.49% |
