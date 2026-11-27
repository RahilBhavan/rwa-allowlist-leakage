# Standalone X drafts

Drafts for Rahil’s tokenization audience. The card is an original draft pending design approval.

## USDtb reserves

> On September 30, 2026, Anchorage reported that $533M of BlackRock’s BUIDL backed USDtb. Curve offered a way to buy USDtb, a stablecoin backed in part by BUIDL.

[USDtb reserve evidence and Curve quote](https://github.com/RahilBhavan/rwa-allowlist-leakage/blob/main/docs/RESULTS.md#usdtb-bank-custody) · [Anchorage’s examined report](https://learn.anchorage.com/09.30.26_USDtb-Stablecoin-Attestation-Report-signed.pdf)

![Anchorage reported approximately $533 million of BlackRock’s BUIDL backing USDtb on September 30, 2026.](../docs/figures/usdtb-buidl.png)

[Card source](cards/usdtb-buidl.html) · [Card evidence and checks](cards/usdtb-buidl.json)

## The mTBILL market

> Midas’s USTB vault backed mTBILL, but the only public route we found on September 30, 2026 quoted under $0.07 of mTBILL at a 79% pool fee.

[Midas vault and quote](https://github.com/RahilBhavan/rwa-allowlist-leakage/blob/main/docs/RESULTS.md#midas-mtbill)

## Usual’s collateral treasury

> On September 30, 2026, Usual’s treasury held $14.03M of Circle’s USYC backing USD0, a stablecoin buyers could acquire on Curve.

[Usual’s treasury balance and contract linkage](https://github.com/RahilBhavan/rwa-allowlist-leakage/blob/main/docs/RESULTS.md#usual-usd0-collateral)

## Flux lending

> Flux had $8.68M in outstanding USDC loans on September 30, 2026. OUSG was the only asset that added borrowing power at the snapshot. Only eligible liquidators can seize pledged OUSG. How much of the existing debt was secured by OUSG remains unverified.

[Pinned Flux controls and credit path](https://github.com/RahilBhavan/rwa-allowlist-leakage/blob/main/docs/RESULTS.md#gated-collateral-and-open-lending)

## Card verification

Run `python3 scripts/check_post_card.py` from the repository root. It checks the exact exported PNG, the visible-text word count, the amount and date against the source transcription, and the links from the draft. The visual receipt records the layout, palette and feed-size checks. The editable HTML uses Archivo Variable and IBM Plex Sans Regular from the selected Proofline kit. To re-render, place those font files in a sibling `fonts/` directory beside a scratch copy of the HTML. Open the copy with Chromium at 1200 × 675, device scale 1, wait for fonts to load and capture the viewport. Fonts are linked as dependencies and kept outside the public export. [Archivo](https://github.com/Omnibus-Type/Archivo) · [IBM Plex](https://github.com/IBM/plex)
