# Final handoff

**DONE — September 30, 2026 research and review.** Three direct contract positions qualify under the study’s acquisition test. Midas held $71.64m of USTB, Usual held $14.03m of USYC, and STBL accounted for $1.00m of attributable OUSG. Together they represent $86.67m. Under the stated supply assumptions, the five-fund direct share lies between 0.94% and 62.20%. The evidence leaves the 5% cutoff open. The upper endpoint includes $1.351bn of unresolved coverage at the modeled floor and $4.272bn of additional denominator allowance. [Results](docs/RESULTS.md)

Including Anchorage’s BUIDL reserves for USDtb raises the lower bound to 6.74%. Omitting the Solana and Aptos balances supported by the accountant-examined report lowers it to 2.63%. The Midas acquisition evidence is a small historical quote at a 79% pool fee. The $35.25m Frax inventory is a separate sensitivity because both route-local mint counters were zero. [Method](docs/METHOD.md) · [Sources](docs/SOURCES.md)

**PARTLY DONE — holder coverage.** The holder tables document all 33 observed contracts, available rankings and unresolved balances. Missing deployments, incomplete historical registers, unidentified operators and the OUSG denominator assumptions limit precision. The five fund diagrams and six-protocol map distinguish verified positions from potential credit and redemption dependencies. [Holder tables](docs/HOLDERS.md) · [Fund diagrams and protocol map](docs/REACH.md)

**NOT DONE — exhaustive census and market depth.** The study does not establish an exact basket share, September BENJI portfolio allocation, executable exit liquidity at size or losses under a redemption pause.

## Verification

Claude Sonnet independently reviewed the pre-repair research. GPT-6.2 Sol completed the research repair and GPT-6.2 Astra verified that revision. The publication evidence reproduces both calculation outputs byte for byte and passes all 19 offline tests. The 18 published JSON fixtures have their own checksum manifest. The later Opus assessment scored the earlier research snapshot 5 overall. Its scores and findings remain in the review record. [Review decisions](docs/DECISIONS.md) · [Opus assessment](docs/QUALITY.md) · [Replay commands](docs/METHOD.md#repair-fixtures-and-replay)

## Rahil’s decision

Choose whether to publish a draft. The direct-contract result answers the original holder question. If using the custody-inclusive figure, retain its separate definition and dependence on attested balances. Rahil authorized public GitHub publication. The draft-post decision and the later quality repair remain separate. [Five draft posts](posts/DRAFTS.md)

## Publication and quality loop

The sanitized study is public. The reopened quality loop scored 5/10 in round one. Sol’s repairs and a fresh Opus review follow. [Public repository](https://github.com/RahilBhavan/rwa-allowlist-leakage)
