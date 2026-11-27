# Standalone X drafts

Drafts for Rahil’s tokenization audience. Editorial evidence links sit below each block.

## Direct contracts

> On Sep 30, 2026, I found $86.67M in contracts backing DEX-tradable tokens across five tokenized Treasury funds. That’s at least 0.94% by value. Missing holder coverage and supply headroom put the modeled ceiling at 62.20%, leaving the 5% cutoff unresolved.

- The five funds, verified amount and rounded bounds come from the aggregate row. The ceiling combines missing coverage with denominator slack. [Direct-contract test](../docs/RESULTS.md#direct-contract-test)

## Bank reserves

> On Sep 30, Anchorage reported $532.7M of BUIDL backing USDtb. Including bank custody takes the five-fund lower bound to 6.74%. That relies on the Solana and Aptos attestation legs. Without those two legs, the lower bound is 2.63%.

- The date is September 30, 2026. The first dollar figure rounds the examined report value. Both shares are conditional on the modeled ceiling. [USDtb bank custody](../docs/RESULTS.md#usdtb-bank-custody) · [Custody-inclusive arithmetic](../docs/RESULTS.md#custody-inclusive-backing)

## Midas redemption vault

> On Sep 30, 2026, a Midas vault held $71.64M of USTB to support mTBILL redemptions. A Uniswap v4 quote showed a way to buy mTBILL without onboarding, even with a 79% pool fee. That tiny quote tells us the route existed. Depth at size is still unknown.

- The vault links to mTBILL by pinned source, token, helper and burn permission. The quote was for 0.0001 ETH, and a separate read-only token delivery call succeeded for a non-greenlisted address. [Midas results](../docs/RESULTS.md#midas-mtbill)

## Usual’s collateral treasury

> On Sep 30, 2026, Usual’s treasury contract held $14.03M of USYC backing USD0. Curve quoted a swap from USDC to USD0. A DEX buyer gets USD0, while direct USYC access still follows Circle’s eligibility rules.

- The pinned treasury linkage, trade direction, value and issuer access distinction trace to the collateral evidence. [Usual USD0 collateral](../docs/RESULTS.md#usual-usd0-collateral)

## Flux lending

> On Sep 30, 2026, Flux held about 336,340 OUSG. Eligible users could supply OUSG, and borrowing OUSG was paused. USDC lending stayed open. Its lenders could bear losses if a borrower defaulted and the pledged OUSG was hard to sell.

- The figure rounds the pinned fOUSG balance. Pinned Comptroller flags and protocol rules support the conditional credit path. [Gated collateral and open lending](../docs/RESULTS.md#gated-collateral-and-open-lending)
