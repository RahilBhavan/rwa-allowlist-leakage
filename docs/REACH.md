# Who can reach the funds

Read left to right as the path through which value or credit risk can reach a user. “Open” means the mapped secondary or lending route does not verify investor identity. Token controls, price, depth and primary redemption can still constrain the exit. “Gated” means that the issuer, transfer agent, protocol or custodian conditions direct access on eligibility. Amounts refer to the September 30 pin unless stated otherwise.

## BUIDL and BUIDL-I

```text
BUIDL/I → whitelist → qualified holder → Securitize redemption or gated RFQ
   ├── Ethereum Frax BUIDL custodian → frxUSD → Curve buyer
   │    [$15.83m inventory, zero route-local minted frxUSD, attribution sensitivity]
   ├── Four Anchorage reserve locations → USDtb → Curve buyer [open, custody backing]
   │    [Solana and Aptos come from the attestation, strict control unresolved]
   ├── Ethereum Grove ALMProxy → Sky allocator credit → USDS ecosystem
   │    [$119.32m BUIDL-I holding; direct USDS reserve attribution unresolved]
   ├── BUIDL-I Ethereum rank-2 Safe [112.91m, operator and backing link unresolved]
   ├── Avalanche sBUIDL [9,240 BUIDL at the wrapper; open acquisition unresolved]
   ├── Ethereum sBUIDL → Euler collateral markets [documented listing]
   ├── Ondo portfolio → eligible OUSG investor → Flux credit → stablecoin lender
   │    [issuer documents portfolio link, exact September allocation unresolved]
   └── Other chain/holder coverage and roles unresolved [see holder census]
```

Frax and Anchorage carry different custody evidence. BUIDL’s Securitize and UniswapX RFQ route is gated at onboarding and among eligible market participants. Grove’s issuer-facing conversion and risk accrue through its portfolio and credit line. An Euler liquidation route may provide a way to take sBUIDL while converting back into BUIDL still depends on eligibility or matched liquidity. [Frax routes](https://docs.frax.com/frxusd/mint-and-redeem-routes) · [Anchorage report](https://learn.anchorage.com/09.30.26_USDtb-Stablecoin-Attestation-Report-signed.pdf) · [Securitize RFQ disclosure](https://investors.securitize.io/news/news-details/2026/Uniswap-Labs-and-Securitize-Collaborate-to-Unlock-Liquidity-Options-for-BlackRocks-BUIDL-02-11-2026/default.aspx) · [Grove governance](https://vote.sky.money/executive/template-executive-vote-sky-token-rewards-rebalance-aligned-delegate-compensation-for-june-2025-atlas-core-development-payments-for-july-2025-hv-bank-rwa009-a-dao-resolution-auxiliary-actions-for-token-transfer-between-spark-and-grove-star-proxy-spells-july-24-2025) · [Euler sBUIDL proposal and implementation](https://forum.euler.finance/t/accept-sbuidl-as-collateral-in-stablecoin-vaults-in-euler-prime-and-euler-yield/1467)

## USTB

```text
USTB → qualified investor / book-entry account → Superstate USD or USDC exit
   ├── Midas Ethereum redemption vault → mTBILL → Uniswap v4 dust quote
   │    [$71.64m USTB backing, small open quote at 79% LP fee]
   ├── Ethereum Frax USTB custodian → frxUSD → Curve buyer
   │    [$19.42m inventory, zero route-local minted frxUSD, attribution sensitivity]
   ├── Ethereum Horizon aToken → permissioned borrower → open stablecoin lender
   │    [1.41m USTB; collateral receipt cannot be traded by end users]
   ├── Other Ethereum contracts [operators or downstream backing unresolved]
   ├── Plume Nest nTBILL and nBASIS [vault balances pinned, offering restricted, historical secondary access unresolved]
   └── Solana Kamino and book entry [historical holder data incomplete]
```

Book entry and Solana/Plume are included in issuer AUM. Kamino is a product integration, with size at the pin unresolved. The only open mTBILL acquisition evidence found at the pin is a dust quote with a 79% pool fee. Primary redemption follows issuer terms and relies on USTB liquidation when USDC balances run short. [Midas pinned evidence](RESULTS.md#midas-mtbill) · [Plume holder evidence](HOLDERS.md#small-evm-deployments-revisited) · [Superstate instrument and integrations](https://superstate.com/assets/ustb) · [Aave RWA receipt mechanics](https://aave.com/docs/aave-v3/smart-contracts/tokenization)

## USYC

```text
USYC → Circle eligibility and token entitlements → Circle USDC redemption
   ├── Ethereum Usual collateral contract → USD0 → Curve buyer [open, $14.03m backing]
   │    ├── bUSD0-backed Morpho loans [documented route; pin exposure unknown]
   │    └── Euler USD0 lending / eUSD0 [documented route; pin exposure unknown]
   ├── Ethereum Horizon collateral → eligible borrower → open stablecoin lender [100 USYC]
   ├── Ethereum rank-1 Safe [13.85m USYC, operator and backing link unresolved]
   ├── BNB rank-1 signer [2.074bn units, no runtime at pin, custody operator unresolved]
   └── Solana, Canton and NEAR [historical holder coverage unresolved]
```

Usual’s primary USYC delivery depends on the collateral engine, treasury allowance and issuer token entitlements. DEX trading accesses USD0 and depends on token transfer controls and pool liquidity. It delivers stablecoin exposure to the backing and its liquidity. Circle’s Binance announcement supports a distinct institutional channel and supplies no mapping of the rank-1 address to any entity. [Usual collateral and secondary trading](https://docs.usual.money/resources-and-ecosystem/fact-sheets/usual-products/usd0) · [Circle USYC eligibility and redemptions](https://www.circle.com/usyc) · [Circle Binance custody announcement](https://investor.circle.com/news/news-details/2025/Circles-USYC-Now-Supported-as-Yield-Bearing-Off-Exchange-Collateral-for-Binances-Institutional-Clients/default.aspx)

## OUSG

```text
Funds and cash → Ondo OUSG portfolio [September BUIDL/BENJI weights unverified]
   ├── OUSG / rOUSG → qualified holder → Ondo manager → stablecoin/cash exit
   ├── OUSG → Ethereum Flux fOUSG → gated borrower
   │    └── borrower debt and collateral recovery → fUSDC lender [open credit]
   ├── OUSG → STBL PT1 vault → USST → Curve buyer [$1.00m attributed backing]
   ├── OUSG → Ethereum ranks 2–3 Safes [operator and backing link unresolved]
   ├── OUSG → XRPL authorized trust line → qualified RLUSD subscription/redemption
   │    [controller and wrapper roles unresolved for all five observed accounts]
   └── Solana holder coverage and global supply reconciliation unresolved
```

Flux held 336,339.56 OUSG. At the pin fOUSG mint was unpaused for eligible accounts and fOUSG borrowing was paused. Both fUSDC flags were unpaused. The Comptroller admin is the Flux DAO timelock and the pause guardian is a separate address. [Pinned control reads](../evidence/review-ethereum-2026-09-30.json) · [Flux deployment registry](https://docs.fluxfinance.com/addresses) Ondo describes instant settlement for eligible users, with issuer-facing cash and portfolio conversion dependencies. XRPL account permissions and outstanding balances are pinned. Share eligibility follows Ondo’s offering and token rules. [Ondo eligibility and holdings](https://ondo.finance/ousg) · [Ondo redemption integration](https://ondo.finance/blog/introducing-instant-24-7-365-subscriptions-and-redemptions-shifting-ousg-funds-into-blackrocks-b) · [XRPL launch](https://ondo.finance/blog/ondo-finance-brings-tokenized-treasuries-to-the-xrp-ledger-with-seamless-mint-redeem-via-ripples-rlusd-stablecoin) · [Flux fTokens](https://docs.fluxfinance.com/protocol/ftokens)

## BENJI / FOBXX

```text
BENJI → transfer-agent whitelist → registered shareholder → Franklin redemption
   ├── Ondo portfolio disclosure → OUSG [September BENJI allocation unverified]
   │    └── pledged OUSG → Flux debt book → stablecoin lender [open credit]
   └── Ethereum and Avalanche location counts only, register/other-chain gaps remain
```

Ondo’s holdings disclosure identifies BENJI in its portfolio, with no pinned custody control or full September 30 look-through attribution. Its downstream credit route inherits OUSG’s funding and liquidation dependencies. Franklin’s transfer agent maintains the official register. [Franklin August 2026 prospectus](https://www.franklintempleton.com/forms-literature/download-preview/9001-P) · [Ondo portfolio](https://ondo.finance/ousg) · [Flux borrower and lender access](https://docs.fluxfinance.com/)

## Six-protocol collateral and redemption-pause map

Here “pause” means the relevant issuer stops processing primary redemptions. The consequences are conditional inferences. Transfer freezes, oracle staleness, liquidation restrictions and insolvency are separate events that can interact with the pause.

| Protocol | Fund custody at pin and documentary scope | Economic transmission | If fund redemptions pause | Unknowns |
| --- | --- | --- | --- | --- |
| Aave Horizon | Ethereum RWA aToken contracts hold **1,410,692.832857 USTB** and **100 USYC**, with underlying identities verified onchain. RWA receipts are non-transferable for end users. | Approved borrowers post restricted collateral. Anyone can supply borrowable stablecoins and take utilization and credit risk. | Existing stablecoin liquidity and borrower repayment can support withdrawals. The liquidation path depends on usable oracle marks, eligibility to take collateral and the ability to turn seized RWA into cash. An unchanged mark can conceal impaired exit liquidity. | No full pin-by-pool debt allocation, oracle shock test, inventory of eligible liquidators or realized recovery. [Aave Horizon](https://aave.com/docs/aave-v3/horizon) · [Address book](https://github.com/bgd-labs/aave-address-book/blob/main/src/AaveV3EthereumHorizon.sol) |
| Morpho | The Ethereum Blue singleton held **0 USYC** at the pin. Morpho’s RWA page lists direct USYC as a market asset and its governance forum documents bUSD0 collateral configurations. Current market listings are discovery evidence. | Blue collateral secures loans. Vault depositors earn loan-asset interest and bear withdrawal and bad-debt risk. A USD0 derivative can transmit USYC exposure through collateral valuation and liquidity. | Borrowers may repay normally. Recovery on an impaired position depends on oracle behavior, available buyers for the collateral and sellability under upstream rules. The vault’s ability to return loan assets depends on cash and borrower repayment. | No pin-sized bUSD0 debt, vault share allocation, or all-market inventory. The singleton read does not cover vaults, other chains or later markets. [Morpho market mechanics](https://docs.morpho.org/learn/concepts/blue/) · [USYC market discovery](https://data.morpho.org/rwa) · [Usual market submission](https://forum.morpho.org/t/usual-boosted-usdc-vault-whitelisting/686) |
| Sky / Spark / Grove | The two sampled Spark ALM addresses and the named deposit/redemption wallets held **zero BUIDL-I**. Grove’s registered Ethereum ALMProxy held **119,322,905.35 BUIDL-I**. Sky published Spark offboarding and Grove onboarding changes. | Grove’s allocator credit finances investments. Losses or delayed proceeds affect that credit and capacity to replenish system liquidity. Holding USDS or savings tokens does not give a pro rata claim on BUIDL-I. | Unwinding BUIDL-I to meet allocator repayment loses its ordinary issuer exit. USDS liquidity can still draw on unrelated assets, buffers and market routes. The size, timing and availability of alternatives determine how far stress transmits. | September 30 allocator liability attributable to this exact lot, available liquidity buffers and any alternative execution channels. [Grove mainnet proxy](https://v2.vote.makerdao.com/sky-executive/template-executive-vote-monthly-settlement-cycle-for-june-2026-lssky-sky-rewards-normalization-complete-rwa001-a-offboarding-add-emergency-spells-to-the-chainlog-whitelist-osero-almproxy-adjust-vault-parameters-update-safe-harbor-agreement-prime-agent-proxy-spells-july-16-2026) · [Spark offboarding](https://vote.sky.money/executive/template-executive-vote-allocator-4-technical-launch-monthly-settlement-cycle-for-september-2025-ranked-delegate-compensation-atlas-core-development-compensation-execute-prime-agent-proxy-spells-october-16-2025) |
| Ethena / Anchorage | September report names **$532.70m BUIDL** in USDtb reserves. Anchorage is the USDtb issuer. Ethena’s USDe terms allow USDtb in the mix of eligible USDe reserve assets. | USDtb’s public market inherits BUIDL reserve and liquidity exposure. USDe may inherit it through USDtb and runs a separate reserve and hedging strategy. | Eligible USDtb redemption depends on available cash, secondary sales and Anchorage’s capacity to realize reserves. USDtb trading can continue at a discount. Any USDe effects depend on held USDtb, other reserves, market liquidity and hedge unwinds. The separately announced November BUIDL liquidity facility is outside the pin. | No attributable September USDe-through-USDtb position, no firm USDtb redemption capacity after a pause, and no recourse beyond the published terms. [USDtb attestation](https://learn.anchorage.com/09.30.26_USDtb-Stablecoin-Attestation-Report-signed.pdf) · [Anchorage terms](https://www.anchorage.com/anchorage-digital-bank-n-a-covered-stablecoin-terms) · [USDe reserve terms](https://docs.ethena.fi/resources/usde-terms-and-conditions) |
| Euler | Securitize and Euler document DS Token integration for whitelisted investors. Euler governance marks the Ethereum sBUIDL collateral proposal implemented. A pinned Avalanche BUIDL holder self-identifies as sBUIDL and holds **9,240 BUIDL**. That balance is wrapper custody. | Isolated vault loans transmit collateral price and liquidation risk to stablecoin lenders. sBUIDL holders can have an underlying BUIDL dependency. Usual separately documents eUSD0 credit as part of its historical reserve architecture. | Even if the EVC can seize collateral or an sBUIDL transfer succeeds, recovery depends on a qualified buyer, secondary execution or a working unwrap and issuer exit. Caps, oracle and liquidation settings are vault-specific. | September vault-by-vault sBUIDL deposits, active liquidator/secondary routes and net exposure through eUSD0. No claim that Euler holds all of the Avalanche wrapper supply. [Securitize integration](https://investors.securitize.io/news/news-details/2026/Securitize-and-Euler-Integrate-DS-Tokens-Expanding-Onchain-Utility-for-Tokenized-Assets-in-DeFi-02-19-2026/default.aspx) · [Euler governance](https://forum.euler.finance/t/accept-sbuidl-as-collateral-in-stablecoin-vaults-in-euler-prime-and-euler-yield/1467) · [Euler EVC](https://docs.euler.finance/build/evc/) · [Usual risk policy](https://docs.usual.money/resources-and-ecosystem/risk-policy) |
| Ondo Flux | Ethereum fOUSG held **336,339.561725865749857494 OUSG**. `getCash()` agrees with the pinned fund balance. fUSDC `totalBorrows()` was **8,681,335.923738 USDC**, a market-level debt measure. | fOUSG receipt follows the OUSG gate. The pinned fOUSG mint/borrow flags were unpaused/paused. Both fUSDC flags were unpaused, and fUSDC can be acquired through open stablecoin lending. Its holder bears the risk that borrowers do not repay and pledged OUSG is hard to liquidate. | An eligible liquidator can only realize market or cash redemption value through a working route. Ondo’s own ability to meet OUSG redemptions also depends on liquid buffers and portfolio conversion, including underlying BUIDL or BENJI. Lender withdrawals depend on unborrowed stablecoins and repayments. | Per-borrower collateral attribution, other fToken debt legs and liquidity under stress. [Flux addresses](https://docs.fluxfinance.com/addresses) · [Gated liquidation and bad debt](https://docs.fluxfinance.com/protocol/liquidations) · [Ondo portfolio and eligibility](https://ondo.finance/ousg) |
