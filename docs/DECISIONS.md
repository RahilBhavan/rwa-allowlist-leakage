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

## 2026-11-26 — Round-one quality repair

Role key. Sol was the implementation agent. Astra owns verification and publication. Sonnet reviewed the earlier research. Opus produced the historical round-one quality assessment.

- **Lead with measured positions.** The README leads with the examined USDtb reserve and directly measured contract backing. The direct estimand still answers the original holder question and the custody-inclusive result still depends on the non-EVM attestation. The report now shows pinned and attested-only amounts separately. Rahil chooses the public lead. [Results](RESULTS.md)
- **Keep the broad BUIDL ceiling and report a tighter scenario.** The issuer-listed bridges held zero BUIDL at the pin. The pinned Ethereum and BNB Chain implementations burn and issue. Coverage of other bridge modes, unidentified holders and the full September non-EVM register is incomplete. The alternative scenario sums EVM supplies gross and allows the higher of current supply and September Anchorage custody on Solana and Aptos. Both direct ranges straddle 5%. [Bridge checks](METHOD.md#buidl-supply-and-bridge-check) · [Sensitivity](RESULTS.md#buidl-deployment-scenario)
- **Keep technical and practical access visible.** The pinned mTBILL quote qualifies under the original technical rule. The only open route found carried a 79% LP fee at dust size. Removing all Midas backing from both lower estimates leaves the direct decision unresolved and the custody-inclusive lower share above 5% under the platform-based assumptions. No better September route was established. [Midas and scenario](RESULTS.md#midas-mtbill)
- **Certify ranks where the supply reconciles.** Optimism BUIDL and Plume USTB now have complete pinned ranks. That pass left the Optimism Safe role and historical secondary access to the Nest receipts unresolved. Other small EVM discovery attempts have explicit request and failure records plus per-deployment supply caps. Successful current Solana reads cover five mint supplies and one BENJI largest-account indication. Other largest-account requests failed at the tested endpoints. None of the current Solana reads substitutes for the historical holder register. [Holder coverage](HOLDERS.md#small-evm-deployments-revisited)
- **Use original public draft media.** Four standalone posts use one claim each. The USDtb sentence card rounds the Schedule II total and uses Proofline 1.0.0. The round-one suggestion referred to the older research-exhibit theme. The current identity governs the export. Its artifact-specific checker enforces linked evidence, a 20-word cap and exact source and PNG hashes. Design approval and post selection remain with Rahil. [Drafts and card](../posts/DRAFTS.md)
- **Preserve source rights and review history.** Publisher PDFs and contract source files are fetched for verification only. The public supplement keeps requests, factual observations and hashes. Both round-one quality records remain historical. The public base advanced to `633c092` with the MIT license for original code during the repair. This slice made no license change.

## 2026-11-27 UTC — Round-two quality repair

- Preserve the direct-contract cutoff as primary and report custody-inclusive backing as a companion. Rank disjoint underlying token lots against both ceilings. Keep denominator slack out of candidate sums. [Threshold table](RESULTS.md#what-would-move-the-direct-verdict)
- Use the pinned fee and quoted output value to flag dust. Show both thresholds and the effect of dropping the entire lot. Require zero balances at issuer-listed bridges for the deployment scenario. [Method](METHOD.md#repair-fixtures-and-replay)
- Record Crypto Relief’s public donation wallet attribution. Keep the possibility of downstream backing unresolved there and leave the Optimism and USYC Safe operators open. Use Nest’s published restrictions as terms evidence. The historical Plume secondary routes remain open questions. [Control reads and terms](HOLDERS.md#round-two-holder-and-control-reads)
- Keep the November Stellar and Solana holder observations out of the September numerical test. Publish factual readbacks with requests and capture dates. [Current evidence](../evidence/round2-readbacks.json)
- Retain the receipted USDtb card and remove the orphan custody chart. Drafts now distinguish public token acquisition, issuer access and the Flux credit path. [Drafts](../posts/DRAFTS.md)

## Close after the third independent review

Scores rose from 5 to 7 to 8. The three-round limit closes this loop. The third score applies to the published research snapshot at `6f4b801`. The subsequent closeout records the review, remaining work and owner decisions. See [the final review](QUALITY.md) and [handoff](../HANDOFF.md).

## 2026-11-27 — Reopened repair after round three

- Count the two Plume Nest lots after the pinned share controls, DEX quotes and output transfers were corroborated. An empty DEX Screener result and zero logs in a short window missed live market state. Correcting the GeckoTerminal chain slug surfaced Rooster and Curve leads. nTBILL enters only the technical-access lower bound. nBASIS survives the dust filter at the tested size. The direct result still spans the cutoff. [Nest evidence](HOLDERS.md#plume-nest-access)
- Compare November Stellar trust-line units with October and September filing shares. The common sponsor and absent home domains leave the large accounts unresolved. Keep the September filing denominator and bar use of the live ranks for fund concentration or September residual attribution. [BENJI reconciliation](HOLDERS.md#current-stellar-benji-and-solana-ustb)
- Rank unresolved balance lots by underlying evidence of a protocol link, then by identified holders and open register gaps. Treat any crossing sum as conditional on proving distinct eligible backing across bridges and nested funds. [Candidate ranking](RESULTS.md#what-would-move-the-direct-verdict)
- Report Flux’s sole positive collateral factor as a pinned setting. Keep the size of OUSG-secured existing debt unresolved and the draft conditional. [Flux evidence](RESULTS.md#gated-collateral-and-open-lending)
