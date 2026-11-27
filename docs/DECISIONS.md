# Decisions

This log records how the study's measures, bounds and classifications changed as evidence improved.

## 2026-11-26 — Test the five-fund claim first

Use contemporaneous USD fund values to weight the aggregate. Report native units and per-fund shares separately. Require evidence for the underlying balance, economic link and accessibility of the downstream token. Count each underlying position once. Keep unclassified exposure visible.

Use 5% as the operational cutoff. A verified lower bound at or above it supports continuing. An upper bound below it supports the narrower finding. If the bounds straddle the cutoff, prioritize the largest resolvable gap and document any residual uncertainty.

## Slice order

1. Kill test with primary evidence, pinned inputs, reproducible arithmetic and tests.
2. If warranted, complete the holder classifications, per-fund access diagrams and six-protocol redemption dependency map. Otherwise document the narrower result or the evidence gap.
3. Reconcile results, source register, reproduction instructions and draft posts with verified evidence.
4. Obtain one independent Sonnet review, allow one repair round, verify locally and close with HANDOFF.md.

Sol implements each slice in this repository. Astra owns independent review and final handoff. Authority follows BRIEF.md and the slice instructions.

## 2026-11-26 — Pin September 30 and report both definitions

- September month-end supplies an independently examined custody report, period issuer marks or proxies, and a historical Ethereum market read. Use the period-end Securitize and Circle disclosures with one displayed increment of headroom each. Ondo’s daily label differs from the pinned Ethereum and XRPL supply cross-check, so the model uses the highest adjacent daily mark. The all-chain BUIDL total and exact intraday OUSG value remain open.
- Run the literal direct-contract test first and the custody-inclusive economic backing test separately. Keep unresolved custody form, role or access in the direct upper bound. The first pass left Usual’s USYC treasury unclassified. The later pinned collateral and market checks qualified it for both measures.
- Primary RPC alternatives recovered BNB Chain and Avalanche historical balance and code after archive access was denied or timed out. Solana and Aptos use the same attestation and the overall denominator ceiling for missing chain state. Superstate’s endpoint requires numeric fund ID and the `lookback` parameter. Ondo’s embedded daily marks and the SEC web read supplied figures when direct API discovery or the shell XML fetch did not produce them.

## 2026-11-26 — Certify holder order with the supply residual

- Rank historical balances from current-index, logged-transfer and protocol-address leads. Prove ranks when no omitted balance can match them. This distinguishes a chain with six reconciled holders from a chain with an incomplete candidate set.
- A BNB USYC supply change located one ordinary redemption/burn transaction and its sender became the major holder candidate. Archive balance, code and supply reads certify its September rank and support the strict exclusion. Institutional custody providers are documented without an operator attribution for the address.
- Count Usual’s actual USYC reserve location after identifying the pinned implementation, reading the treasury and collateral mapping, and checking its redemption allowance and Curve route. The empty DaoCollateral balance is consistent with treasury custody.
- Keep non-EVM custody unresolved for the strict upper bound. Apply no-code exclusions within a single corroborated anonymous deployment per fund to avoid cross-chain duplication. Use exact case-specific evidence for the BNB Anchorage reserve and two gated collateral receipts. Leave all unresolved contracts and ambiguous controls inside the ceiling.
- For XRPL OUSG, a full-history ledger query and issuer obligations recover the account-level census. Public state on Solana, Stellar and Aptos does not provide equivalent September holder control. Log-range errors and index denials leave several EVM chains with supply-only coverage.

## 2026-11-26 — Lead with the unresolved direct-contract test

- The conditional direct bounds straddle 5%, so the evidence supports a measured lower bound and an unresolved cutoff. The custody-inclusive backing clears 5% under the wider definition and relies materially on the examined Solana and Aptos reserve legs. Treat the market evidence as small-size quotes on the covered Ethereum routes. Legal ownership and redemption rights follow their own terms. [Results and sensitivities](RESULTS.md)
- Draft standalone posts around the direct-contract result, bank custody, Usual's collateral path, and Flux's credit path. Hold the “allow-lists hold” conclusion while the direct upper bound remains above 5%. Leave review and the final public claim selection to Astra and Rahil. [Drafts and claim links](../posts/DRAFTS.md)

## Independent review of 1420b1c

Sonnet reproduced the arithmetic and flagged the $71.64m Midas vault, incomplete holder-role classification, loose upper bounds, conflicting OUSG supply data, missing negative tests and stale handoff text. It matched 228 of 230 historical reads attempted and independently checked the Anchorage PDF. It could not verify Franklin's SEC figure, the mTBILL market at the pin or several other historical data gaps. Use the single repair round for these findings. Keep direct contracts as the primary estimand given the brief's holder criterion, and report custody-inclusive backing alongside it.

## 2026-11-26 — Single repair dispositions

- **Midas USTB rank 2, verified and counted.** The issuer registry and pinned implementations, helper asset, burn role and proxy-admin ownership support the $71.64m backing lot. Ethereum mTBILL supply at the pinned feed value covers the attributed lot. A hook-free Uniswap v4 market returned a small quote at a 79% LP fee, and a read-only transfer to a non-greenlisted account succeeded. The market evidence establishes access for the tested size. Primary eligibility and full-size liquidity remain open. The ETH market lead came from GeckoTerminal after the DEX Screener lookup yielded no pairs. [Midas result](RESULTS.md#midas-mtbill)
- **Holder census, completed within observed coverage.** Report exclusive classes per pinned deployment plus unknown residual, and record each observed contract’s evidence, rank if certified and wrapper decision. Pinned Safe reads resolve execution control type for the large BUIDL, BUIDL-I, USYC, OUSG and USTB candidates. An unverified operator, missing backing link or unresolved Safe module leaves that amount inside the upper bound. STBL PT1 qualifies partially from the OUSG registry, recorded net stable-value cap after haircut, Curve quote and transfer. Include the additional 100 USYC gated Horizon receipt as a strict exclusion. [Holder tables](HOLDERS.md) · [STBL result](RESULTS.md#stbl-usst)
- **Estimand and drafts, updated.** Keep strict direct backing primary and custody-inclusive backing as the companion. Split the unclassified amount into unresolved coverage at the floor and denominator slack. Draft 2 specifies reliance on Anchorage’s Solana and Aptos reserve legs. Drafts and per-fund access diagrams retain large gaps and limited market depth. [Results](RESULTS.md) · [Drafts](../posts/DRAFTS.md) · [Access diagrams](REACH.md)
- **OUSG, prior ceiling superseded.** October 2–4 issuer marks exceed the old ceiling. Use the conservative pinned Ethereum plus XRPL floor conditional on distinct native issuance. Leave rOUSG out, document the single-chain fallback and missing Solana inventory, and model separate $10m timing/NAV and $25m unknown-scope allowances above the highest observed basis. These are explicit assumptions. Stress both and double the whole OUSG ceiling. [Denominator sensitivity](RESULTS.md#denominator-sensitivity)
- **Frax and Flux, pinned evidence saved.** Frax’s asset getters match and both mint counters are zero. Verified code allows pooled redemption with a saturating route-local counter. Attribute neither lot to primary minted liabilities without stronger evidence, and show both positions in a documentary reserve sensitivity. Flux fOUSG mint and borrow flags were unpaused and paused. fUSDC mint and borrow were unpaused. Record the distinct timelock admin and pause guardian. [Frax result](RESULTS.md#frax-frxusd-attribution-sensitivity) · [Flux result](RESULTS.md#gated-collateral-and-open-lending)
- **Franklin and regression coverage.** SEC’s formatted financial filing corroborates period, B.4/B.5 and the share class readback. The index confirms the accession and period. This is a separate read of the same filing. Ondo’s September BENJI portfolio allocation remains unverified. Tests reject delegated or unknown code as plain no-code exclusions, aggressive OUSG price assumptions, missing gated code, wrong parent hash, USD0 pause and ineligible USYC, unreconciled BNB burn and XRPL obligation mismatches. Market-proof negative cases reject missing Midas or STBL acquisition evidence. [Source register](SOURCES.md#independent-review-repair) · [Rerun and replay](METHOD.md#repair-fixtures-and-replay)
