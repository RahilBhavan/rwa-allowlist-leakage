# Allow-list leakage: who really holds tokenized Treasury exposure

Question: how much of BUIDL, USTB, USYC, OUSG and BENJI supply sits inside contracts (vaults, PSMs, yield tokens, stablecoin reserves, lending markets) whose own shares anyone can buy without KYC? Anchor: BIS Bulletin 115 (2025-11-26) notes allow-lists only restrict direct holders. Build: classify top holders per fund and chain (EOA, issuer/ops wallet, contract); for each contract decide whether its share token is permissionless, citing code or docs; output share-of-supply table and per-fund 'who can reach it' diagram, plus a cross-protocol collateral map (Aave Horizon, Morpho, Sky/Spark, Ethena, Euler, Ondo Flux) and what each depends on if issuer redemptions pause. Kill test (days 1–2): if under ~5% of supply sits in permissionless wrappers, publish 'the allow-lists hold' as the narrower finding. Limits: economic exposure, not legal ownership; never claim a rule was broken; name protocols, never individuals. Related holder-classification research: Tümer and Mafrur, arXiv 2610.05873.

## Shared rules (all six RWA A-tier projects)

Origin: Rahil commissioned this study on November 26, 2026. Verify each number, date and quote against a primary source before using it.

Purpose: produce a reproducible mechanism study for readers interested in RWAs and tokenization.

Authority

- Rahil authorized publication on public GitHub and sanitization of Git history before the first push on November 26, 2026. The publication owner, Astra, handles the final audit, history rewrite, commits, repository creation and push. The implementation slice prepares the working tree.
- Local code changes, keyless public RPC reads and public pages and filings are in scope. The owner-authorized local comparison datasets are read-only. Query only a copy in ignored `data/`. The offline study runs without those datasets.
- X posts and scheduling, outreach, transactions, paid APIs, API keys, Tenderly and timers remain outside this authorization.
- Run heavy suites and long data pulls through the maintainer's workload budget gate. Use a task-owned directory on disk under `~/scratch/<project>/<task>/` for large files and builds. Delete only task directories you created. Keep source downloads and local datasets in ignored `data/`.

Process:
1. Week-1 kill test first. If it fails, write the narrower finding (or why to drop) in `docs/RESULTS.md`, and stop.
2. Build in small vertical slices, with tests for observable behaviour. Pin blocks, dates and source snapshots so results reproduce.
3. Separate five evidence layers on every claim: issuer statement, legal or offering terms, arithmetic, onchain fact, interpretation.
4. One independent review of the finished result by a different model family from the builder (e.g. Claude Sonnet or Opus via `delegate_task`), checking the numbers and the code. Repair limit: 1 round.

Required documentation
- `README.md`: question, one-line answer, how to reproduce, limits.
- `docs/METHOD.md`: data sources, contracts and addresses (with issuer-doc citations), classification rules, pinned blocks and dates.
- `docs/RESULTS.md`: findings with numbers, each traced to a command or source; what is unknown.
- `docs/SOURCES.md`: every source URL, access date, which claim it supports, primary/secondary.
- `docs/DECISIONS.md`: dated decisions and why, including dead ends.
- `STATE.md`: next action first, under 3,000 characters, rewritten in place.
- `posts/DRAFTS.md`: 3–5 draft X posts (text, at most 20 words on any card image, the point visible at a glance), each number linked to RESULTS. Drafts only; Rahil posts.
- `HANDOFF.md` at the end: DONE / PARTLY DONE / NOT DONE, what was proven and how, what was not checked, and Rahil's decisions.

Stopping: stop at HANDOFF.md, or when blocked on something only Rahil can do. Report the blocker once.
