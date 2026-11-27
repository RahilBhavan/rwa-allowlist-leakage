# Allow-list leakage in tokenized Treasuries

How much of five tokenized Treasury funds backed tokens buyers could acquire on public markets?

On September 30, 2026, five contracts held **$90.49 million** of fund units behind publicly quotable tokens, or **$15.04 million** excluding dust-only routes. The direct range of **0.98%–62.20%** leaves the **5%** cutoff unresolved. Including USDtb’s bank reserves gives a conditional lower bound of **6.78%** under the modeled supply ceiling if Anchorage’s attested Solana and Aptos legs count, and **2.67%** on pinned balances alone. [Direct test](docs/RESULTS.md#direct-contract-test) · [Custody sensitivity](docs/RESULTS.md#custody-inclusive-backing)

![Anchorage reported approximately $533 million of BlackRock’s BUIDL backing USDtb on September 30, 2026.](docs/figures/usdtb-buidl.png)

## Reproduce

Python 3.10 or newer, standard library only. The offline commands require no network or credentials.

```sh
sha256sum -c evidence/SHA256SUMS
python3 -m unittest discover -s tests -v
python3 scripts/holder_audit.py
python3 scripts/kill_test.py
python3 scripts/check_post_card.py
```

The bounds measure economic backing under explicit supply and route assumptions. Fund ownership and primary redemption follow issuer terms. Incomplete registers and bridge mappings leave coverage open. Pinned quotes show access at tested sizes, and depth at institutional size remains unknown. [Method and live replay](docs/METHOD.md) · [Holder coverage](docs/HOLDERS.md) · [Redemption dependencies](docs/REACH.md) · [Sources and provenance](docs/SOURCES.md) · [Independent review history](docs/QUALITY.md)

Original code is [MIT-licensed](LICENSE). Third-party source material retains its own terms. [Public repository](https://github.com/RahilBhavan/rwa-allowlist-leakage)
