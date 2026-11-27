# Holder coverage at September 30, 2026

The [holder audit](../scripts/holder_audit.py) prints the full ranked address lists, exact balances, code class, documented roles, and supply residuals. The EVM residual is `totalSupply − sum(positive pinned balances)` for one token contract. Each unobserved address can hold at most the entire residual. An observed balance strictly above it has a verified rank. A tie can be certified only when the omitted balance ceiling is strictly lower than the tied balances. The candidate order below that threshold can change. Zero-supply rows refer to the identified token contract at the pin.

## EVM and XRP Ledger coverage

Native units, rounded for readability. “Verified” counts addresses with a certified rank, including ties. A holder address is an account location, which can aggregate many beneficiaries.

| Fund / chain or class | Pin | Native supply | Unaccounted native supply | Verified / positive addresses read | Key classifications and gap |
| --- | ---: | ---: | ---: | ---: | --- |
| BUIDL Ethereum original | 26,093,737 | 203,389,187.177549 | 12,502,006.256775 | 3 / 32 | Ranks 1 and 2 are no-code holders with 54.85m and 51.52m. Frax holds 15.83m at verified rank 3. Remaining historical holders are unresolved. |
| BUIDL-I Ethereum | 26,093,737 | 239,844,535.090100 | 0 | 6 / 6 | Grove ALMProxy is rank 1 with 119.32m. Rank 2 is Crypto Relief’s published donation Safe, a 4-of-7 holding 112.91m. Its backing role remains unresolved. Rank 3 has no runtime code and holds 7.61m. Rank 5 has EIP-7702 delegation code. |
| BUIDL BNB Chain | 125,000,754 | 146,619,491.33 | 35,194,533.68 | 1 / 1 | Anchorage is rank 1 with 111.42m at a no-code address. Other holders remain unresolved. |
| BUIDL Avalanche | 96,488,899 | 486,533,969.52 | 0 | 6 / 6 | Rank 1 is a no-code holder at 432.87m with a signed redemption-route transfer before the pin. Anchorage is rank 2 at 43.84m. Rank 5 is the sBUIDL token contract with 9,240 BUIDL. All five other positive accounts have no runtime code. |
| BUIDL Arbitrum | 510,496,863 | 8,577,422.39 | 8,577,422.39 | 0 / 0 | Supply read. Holder index rejected the network. |
| BUIDL Optimism | 157,607,011 | 26,472,554.59 | 0 | 2 / 2 | Rank 1 held 26,472,446.76 in a 1-of-1 Safe with no enabled modules. Rank 2 had no runtime code. |
| BUIDL Polygon | 94,738,439 | 7,540,191.03 | 7,540,191.03 | 0 / 0 | Supply read. Holder index rejected the network. |
| BUIDL Tempo | 42,021,929 | 17,102,298.05 | 17,102,298.05 | 0 / 0 | Supply read. Holder index rejected the network and the official RPC caps log windows. |
| USTB Ethereum | 26,093,737 | 50,620,204.672699 | 5,374,817.685102 | 3 / 29 | Rank 1 has no code and holds 13.83m. Verified rank 2 is the Midas mTBILL vault at 6.38m. Rank 3 holds 5.85m with no runtime code and unresolved identity. Frax holds 1.73m and Horizon’s non-transferable USTB collateral receipt contract holds 1.41m. |
| USTB Plume | 96,561,570 | 339,802.153683 | 0 | 2 / 2 | Two Nest vault contracts reconcile supply. nTBILL held 338,816.706554 and nBASIS held 985.447129 USTB. |
| USYC Ethereum | 26,093,737 | 36,774,089.914760 | 6,593,845.515318 | 2 / 23 | Rank 1 is a 2-of-4 Safe with 13.85m and unresolved operator and wrapper role. Usual’s collateral treasury is rank 2 with 12.32m. Horizon holds 100 USYC. Morpho Blue’s documented Ethereum singleton holds zero USYC. |
| USYC BNB Chain | 125,000,754 | 2,073,937,727.947452 | 10.002084 | 1 / 1 | Rank 1 is a transaction signer with no runtime code at the pin and holds 2,073,937,717.945368. Transfer receipt discovery and pinned balance plus supply prove rank 1. Custody operator and the residual holders are unresolved. |
| USYC Arc | 23,620,687 | 0 | 0 | 0 / 0 | Zero supply at the discovered mainnet address. The explorer denied holder-list access. Arc’s post-launch product references do not provide a September holder register. |
| OUSG Ethereum | 26,093,737 | 1,132,837.419415 | 1,190.194469 | 20 / 23 | Flux fOUSG is rank 1 at 336,339.56. Ranks 2 and 3 are Safes with unresolved custody roles. Rank 12 is the STBL PT1 vault. |
| OUSG Polygon | 94,738,439 | 0 | 0 | 0 / 0 | Pinned contract returned zero supply. |
| OUSG XRP Ledger | 107,347,788 | 1,605,617.7253523406 | 0 | 5 / 5 | Exhaustive issuer trust-line pages, five positive balances. First three hold 1,181,505.57614436, 245,456.57619873 and 178,655.564832. All five are issuer-authorized. Account ownership, custody and wrapper arrangements are unresolved. |
| BENJI Ethereum | 26,093,737 | 48,238,907.896735 | 0 | 3 / 3 | Three no-code holders with 16.113m, 16.112m and 16.014m. Their roles and beneficial holders remain unresolved. |
| BENJI Avalanche | 96,488,899 | 34,330,417.201451 | 0 | 4 / 4 | Four no-code holders, with a rank-1 tie at 16.113m each. Deployment totals and wallet control are separate from Franklin’s official share register. |
| BENJI Arbitrum | 510,496,863 | 47,980,254.137611 | 47,980,254.137611 | 0 / 0 | Issuer-address supply read. Holder index rejected the network. |
| BENJI Base | 52,011,726 | 59,762,338.010118 | 59,762,338.010118 | 0 / 0 | Issuer-address supply read. Holder index rejected the network. |
| BENJI Polygon | 94,738,439 | 32,226,231.994119 | 32,226,231.994119 | 0 / 0 | Issuer-address supply read. Holder index rejected the network. |

## Share of pinned deployment supply

Percentages use each deployment's own `totalSupply()`, or reconciled issuer obligations for XRPL. They describe account locations and are mutually exclusive. Documented fund operations and third-party stablecoin reserve custody take precedence over account type. EOA requires a signed transaction corroboration or EIP-7702 designation. No-code means empty runtime at the pin with insufficient signer or role evidence. Unknown control is an observed balance with unresolved account class, including trust-line accounts. Unobserved is the supply residual. Rounding can affect the row sum. A dash means the share is undefined. Where supply is unavailable, see the remaining deployment gaps. The holdings in different rows may represent the same fund shares. [Class calculation](../scripts/holder_audit.py) · [Avalanche signed transaction](../evidence/buidl-avalanche-signer.json) · [BNB signed sender and burn](../evidence/usyc-bnb-receipt-2026-09-25.json)

| Fund / chain | Issuer / ops | Third-party stablecoin reserve custody | Contract | EOA | No-code | Unknown control | Unobserved |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| benji/arbitrum | 0.000% | 0.000% | 0.000% | 0.000% | 0.000% | 0.000% | 100.000% |
| benji/avalanche | 0.000% | 0.000% | 0.000% | 0.000% | 100.000% | 0.000% | 0.000% |
| benji/base | 0.000% | 0.000% | 0.000% | 0.000% | 0.000% | 0.000% | 100.000% |
| benji/ethereum | 0.000% | 0.000% | 0.000% | 0.000% | 100.000% | 0.000% | 0.000% |
| benji/polygon | 0.000% | 0.000% | 0.000% | 0.000% | 0.000% | 0.000% | 100.000% |
| buidl/arbitrum | 0.000% | 0.000% | 0.000% | 0.000% | 0.000% | 0.000% | 100.000% |
| buidl/avalanche | 0.000% | 9.010% | 0.002% | 88.971% | 2.017% | 0.000% | 0.000% |
| buidl/bsc | 0.000% | 75.996% | 0.000% | 0.000% | 0.000% | 0.000% | 24.004% |
| buidl/ethereum | 0.000% | 0.000% | 10.558% | 0.000% | 83.296% | 0.000% | 6.147% |
| buidl/optimism | 0.000% | 0.000% | 100.000% | 0.000% | 0.000% | 0.000% | 0.000% |
| buidl/polygon | 0.000% | 0.000% | 0.000% | 0.000% | 0.000% | 0.000% | 100.000% |
| buidl/tempo | 0.000% | 0.000% | 0.000% | 0.000% | 0.000% | 0.000% | 100.000% |
| buidl_i/ethereum | 0.000% | 0.000% | 96.825% | 0.000% | 3.175% | 0.000% | 0.000% |
| ousg/ethereum | 0.000% | 0.000% | 72.729% | 0.000% | 27.166% | 0.000% | 0.105% |
| ousg/polygon | — | — | — | — | — | — | — |
| ousg/xrpl | 0.000% | 0.000% | 0.000% | 0.000% | 0.000% | 100.000% | 0.000% |
| ustb/ethereum | 0.000% | 0.000% | 24.167% | 0.000% | 65.215% | 0.000% | 10.618% |
| ustb/plume | 0.000% | 0.000% | 100.000% | 0.000% | 0.000% | 0.000% | 0.000% |
| usyc/arc | — | — | — | — | — | — | — |
| usyc/bsc | 0.000% | 0.000% | 0.000% | 100.000% | 0.000% | 0.000% | 0.000% |
| usyc/ethereum | 0.000% | 0.000% | 71.159% | 0.000% | 10.911% | 0.000% | 17.931% |

## Observed contracts and wrapper decisions

This is the full positive-balance contract census in the observed EVM candidates. The pinned holder fixture and supplemental reads carry runtime classifications and byte hashes alongside exact balances. Ranks marked “uncertified” are candidate observations. Ranks use exact raw units and the supply residual. Source verification leads identify contract types where available. A control type, including a Safe with no enabled module, cannot resolve offchain reserve commitments or a downstream receipt. Safes with unresolved backing stay in the direct upper bound. [Pinned holder capture](../evidence/holders-2026-09-30.json) · [Supplemental control and market reads](../evidence/review-ethereum-2026-09-30.json) · [Round-one coverage additions](../evidence/round1-supplement.json) · [Source-match leads](../evidence/review-contract-discovery.json) · [Protocol documents and source limits](SOURCES.md)

| Fund / chain | Certified rank | Holder | Native units | Control and evidence | Direct wrapper decision |
| --- | ---: | --- | ---: | --- | --- |
| buidl/avalanche | 5 | `0xaeb1fa0853c7c98eab10fcf0ea669ae3d07fbb10` | 9,240.000000 | sBUIDL custody from pinned symbol, balance and supply and issuer filing. | Open Avalanche acquisition unresolved. |
| buidl/ethereum | 3 | `0xe827abf9f462ac4f147753d86bc5f91e186e4e9c` | 15,830,037.480000 | Frax BUIDL custodian. Pinned owner and backing token. | Route-local minted frxUSD zero. Sensitivity only. |
| buidl/ethereum | uncertified | `0xc0d9ed97ccdfca762b1bbeb40c9c7679a7290e43` | 5,508,491.790000 | Pinned Safe 2-of-4 via master copy and threshold/owner reads. | Operator and backing relationship unresolved. Kept inside strict ceiling. |
| buidl/ethereum | uncertified | `0xa2af0b03aaf167cfc9624c6ef587581b6fcced92` | 104,248.161651 | Current verified source lead names GnosisSafeProxy / GnosisSafe. Historical operator unresolved. | Downstream backing and access unresolved. Kept inside strict ceiling. |
| buidl/ethereum | uncertified | `0x51c72848c68a965f66fa7a88855f9f7784502a7f` | 20,185.000000 | Current verified source lead names Bot. Historical operator unresolved. | Downstream backing and access unresolved. Kept inside strict ceiling. |
| buidl/ethereum | uncertified | `0xb1748c79709f4ba2dd82834b8c82d4a505003f27` | 10,000.000000 | Current verified source lead names GnosisSafeProxy / GnosisSafe. Historical operator unresolved. | Downstream backing and access unresolved. Kept inside strict ceiling. |
| buidl_i/ethereum | 1 | `0x491edfb0b8b608044e227225c715981a30f3a44e` | 119,322,905.350000 | Grove ALMProxy named in Sky governance. | Allocator credit path. Exact public-receipt reserve attribution unresolved. |
| buidl_i/ethereum | 2 | `0x68a99f89e475a078645f4bac491360afe255dff1` | 112,907,656.670000 | Pinned Safe 4-of-7 with no enabled modules. [Crypto Relief lists it as its donation wallet](https://cryptorelief.in/donate). | Backing relationship unresolved. Kept inside strict ceiling. |
| buidl/optimism | 1 | `0xd06fc8c16fa5ab9e32f1bb5e3a41bc2212342d29` | 26,472,446.760000 | Pinned master copy, one owner, threshold one and empty module list. | Operator, custody function and downstream token unresolved. |
| ustb/plume | 1 | `0xe72fe64840f4ef80e3ec73a1c749491b5c938cb9` | 338,816.706554 | Pinned symbol nTBILL and runtime code. Nest documents vault shares. | Pinned Rooster V2 route, dust-only at tested size. [Access](#plume-nest-access) |
| ustb/plume | 2 | `0x11113ff3a60c2450f4b22515cb760417259ee94b` | 985.447129 | Pinned symbol nBASIS and runtime code. Nest documents vault shares. | Pinned Rooster V2 quote and delivery check. [Access](#plume-nest-access) |
| ousg/ethereum | 1 | `0x1dd7950c266fb1be96180a8fdb0591f70200e018` | 336,339.561726 | Flux fOUSG. Pinned underlying, Comptroller markets and controls. | Gated fOUSG excluded. Indirect stablecoin lending mapped separately. |
| ousg/ethereum | 2 | `0x5d87fa995c54fff52cfe1c18d8ebf79f0eeb3aeb` | 261,208.832946 | Pinned Safe 2-of-3 via master copy and threshold/owner reads. No enabled module returned. | Operator and backing relationship unresolved. Kept inside strict ceiling. |
| ousg/ethereum | 3 | `0x56e60979d5934a05d22606b0455d52f59f20a6a0` | 187,133.335682 | Pinned Safe 2-of-4 via master copy and threshold/owner reads. 1 enabled module returned. Module purpose unresolved. | Operator and backing relationship unresolved. Kept inside strict ceiling. |
| ousg/ethereum | 9 | `0x3ee60c57d70a6ec4877dc24aa7d0e6fac61cd11a` | 17,178.793854 | Pinned Safe 3-of-7 via master copy and threshold/owner reads. | Operator and backing relationship unresolved. Kept inside strict ceiling. |
| ousg/ethereum | 11 | `0x609517eacd9ec2e24dffd4eeca54c6fd88c866fe` | 9,147.242110 | Pinned Safe 2-of-4 via master copy and threshold/owner reads. | Operator and backing relationship unresolved. Kept inside strict ceiling. |
| ousg/ethereum | 12 | `0x64bef4478942d8fd62be281707076442aa2d055e` | 8,693.543272 | STBL OUSG PT1. Registry pins OUSG and deposit issuer. Vault ledger measures deposits and haircut. | Partially counted for USST. Net attributed stable value plus Curve quote and transfer. |
| ousg/ethereum | 16 | `0xe257e2f1f544dfda152ba508bdd87832cec1406c` | 3,218.381289 | Current verified source lead names GnosisSafeProxy / GnosisSafe. Historical operator unresolved. | Downstream backing and access unresolved. Kept inside strict ceiling. |
| ousg/ethereum | uncertified | `0x9ca46d1b02be5283111499a2f188a0a16fb4546d` | 980.333548 | Current verified source lead names GnosisSafeProxy / GnosisSafe. Historical operator unresolved. | Downstream backing and access unresolved. Kept inside strict ceiling. |
| ustb/ethereum | 2 | `0x569d7dccbf6923350521ecbc28a555a500c4f0ec` | 6,379,144.864074 | Midas-controlled redemption vault. Pinned implementation, mToken, helper, burn role and timelock. | Counted for mTBILL. Hook-free Uniswap v4 quote and transfer corroborate access. |
| ustb/ethereum | uncertified | `0x5fbaa3a3b489199338fbd85f7e3d444dc0504f33` | 1,729,693.761124 | Frax USTB custodian. Pinned owner and backing token. | Route-local minted frxUSD zero. Sensitivity only. |
| ustb/ethereum | uncertified | `0x4e58a2e433a739726134c83d2f07b2562e8dfdb3` | 1,410,692.832857 | Aave Horizon RWA aToken. Protocol address book and pinned underlying. | Gated, non-transferable collateral receipt excluded. |
| ustb/ethereum | uncertified | `0xb4370cf83bae43beb4539fa5882a128d0c772402` | 909,490.671183 | Pinned Safe 2-of-3 via master copy and threshold/owner reads. Operator unresolved. | Downstream backing and access unresolved. Kept inside strict ceiling. |
| ustb/ethereum | uncertified | `0x2ec96c9af82ddd650c0776cb0da93beaa7ce2a10` | 695,174.023857 | Pinned Safe 3-of-9 via master copy and threshold/owner reads. Operator unresolved. | Downstream backing and access unresolved. Kept inside strict ceiling. |
| ustb/ethereum | uncertified | `0xbb50bf72fa9f301478befb8c4f021b22b7315b31` | 652,789.819385 | Pinned contract. Sourcify and Blockscout returned no verified identity, Safe getters reverted and EIP-1967 implementation slot was zero. | Wrapper and control unresolved. |
| ustb/ethereum | uncertified | `0x25ec9e5a96add501cb544ccd9451be551acefab6` | 267,874.794450 | Pinned Safe 3-of-7 via master copy and threshold/owner reads. Operator unresolved. | Downstream backing and access unresolved. Kept inside strict ceiling. |
| ustb/ethereum | uncertified | `0x9d9588c082634fd4c7f54cb0243d6792cfd7b4c4` | 186,150.394703 | Pinned Safe 3-of-5 via master copy and threshold/owner reads. Operator unresolved. | Downstream backing and access unresolved. Kept inside strict ceiling. |
| ustb/ethereum | uncertified | `0xb1748c79709f4ba2dd82834b8c82d4a505003f27` | 2,403.114685 | Current verified source lead names GnosisSafeProxy / GnosisSafe. Historical operator unresolved. | Downstream backing and access unresolved. Kept inside strict ceiling. |
| usyc/ethereum | 1 | `0xb1a6ac52a21435c744b5b4129b07e6c44bcd629b` | 13,846,970.460298 | Pinned Safe 2-of-4 via master copy and threshold/owner reads. No enabled module returned. | Operator and backing relationship unresolved. Kept inside strict ceiling. |
| usyc/ethereum | 2 | `0xdd82875f0840aad58a455a70b88eed9f59cec7c7` | 12,320,132.708463 | Usual treasury. Pinned DaoCollateral pointer, eligibility and allowance. | Counted for USD0. Pinned Curve quote and liquidity. |
| usyc/ethereum | uncertified | `0x0529fb0d7493e8c76babf80c0b51c87e4e5c852e` | 786.896431 | Current verified source lead names GnosisSafeProxy / GnosisSafe. Historical operator unresolved. | Downstream backing and access unresolved. Kept inside strict ceiling. |
| usyc/ethereum | uncertified | `0xc167932ac4eec2b65844ef00d31b4550250536a5` | 100.000000 | Aave Horizon RWA aToken. Protocol address book and pinned underlying. | Gated, non-transferable collateral receipt excluded. |
| usyc/ethereum | uncertified | `0x341c281d11677795f1192bf1f7438666909841c8` | 0.083777 | Current verified source lead names CrossMarginPhysicalEngineProxy / CrossMarginPhysicalEngine. Historical operator unresolved. | Downstream backing and access unresolved. Kept inside strict ceiling. |
| usyc/ethereum | uncertified | `0x9c742aef14cc875c49f52bbd4473b35bebad26ae` | 0.010206 | Current verified source lead names CrossMarginEngineProxy / CrossMarginCashEngine. Historical operator unresolved. | Downstream backing and access unresolved. Kept inside strict ceiling. |
| usyc/ethereum | uncertified | `0x5c73e1cfdd85b7f1d608f7f7736fc8c653513b7a` | 0.010000 | Circle Teller in deployment docs. Issuer operations. | Position's downstream reserve attribution unresolved. Kept inside strict ceiling. |
| usyc/ethereum | uncertified | `0x2cf8d5089d3cc289b369bff29646d4070459c66b` | 0.000001 | Current verified source lead names PositionPauser. Historical operator unresolved. | Downstream backing and access unresolved. Kept inside strict ceiling. |

## Remaining deployment and register gaps

| Fund / deployment | Coverage |
| --- | --- |
| BUIDL Solana | Anchorage Schedule II attests 231,923,254 BUIDL at the report timestamp. The current mint supply is below. Historical rank and independent control attribution remain unresolved. |
| BUIDL Aptos | Schedule II reports 145,511,027 BUIDL. The public node’s retention does not reach the report time. No historic rank or independent control attribution. |
| BUIDL Arc | Circle names BUIDL in its mainnet launch ecosystem. A September issuer token-address mapping and supply were not independently established. |
| USTB Solana | Issuer provides the SPL mint. Historical payer or program-controlled holder ranking and supply are unresolved. |
| USTB book entry | Superstate includes register-only shares in AUM. Public AUM gives a ceiling, with no investor-address list. |
| USYC Solana | Issuer provides the Token-2022 mint and permissions program. Historic owner/program balance snapshot was unavailable. |
| USYC Canton | Network documentation describes balances as private to the holder and Hashnote. No public aggregate holder register. |
| USYC NEAR | Circle lists the network. A dated contract and historical holder register were not recovered. |
| OUSG Solana | Ondo documents deployment. The public SPL interface supplies current state, leaving September 30 chain balances unresolved. |
| BENJI Stellar | Franklin publishes the asset issuer and describes a transfer-agent register. A September holder census from that register or a complete ledger replay was unavailable. |
| BENJI Solana | Franklin publishes the mint. Current holder index candidates lack a pinned account-owner reconstruction. |
| BENJI Aptos | Franklin publishes the asset. Historical state and asset-store controller enumeration were unavailable at the public endpoint. |
| Franklin BNB Chain | Franklin’s contract directory identifies the BNB deployment as iBENJI, a different fund. No FOBXX BNB contract was established. |

[Evidence and discovery sources](SOURCES.md) · [Pin and exclusion rules](METHOD.md)

Solana and Aptos BUIDL have known Anchorage custody balances on the attestation date. Each chain’s September total supply and technical account control remain unknown, so the share of supply in reserve custody remains undefined. All other deployments in the gap table have unknown class shares. The September BENJI allocation inside OUSG remains unverified.

### Small EVM deployments revisited

The [supplement capture](../scripts/fetch_supplement.py) tries at most 12 explorer holders and a 1,000-block `eth_getLogs` window ending at each pin. It reads candidate balances and code at the historical block. The rows below describe the exact endpoints, requests and responses recorded in the [supplement fixture](../evidence/round1-supplement.json). The Blockscout results give candidate addresses. The supply residual certifies the Optimism and Plume ranks.

```sh
mkdir -p data
python3 scripts/fetch_supplement.py data/live-supplement.json
```

| Target | Explorer holder query | Pinned transfer window | Maximum supply at the pin |
| --- | --- | --- | ---: |
| BUIDL Arbitrum | Arbitrum Blockscout 403 | Blast API 400 | $8.58m |
| BUIDL Optimism | Optimism Blockscout found both holders | dRPC 400 | $26.47m |
| BUIDL Polygon | Polygon Blockscout 403 | dRPC 400 | $7.54m |
| BUIDL Tempo | Tempo explorer 404 | Tempo RPC returned zero logs in the window | $17.10m |
| BENJI Arbitrum | Arbitrum Blockscout 403 | Blast API 400 | $47.98m |
| BENJI Base | Base Blockscout 403 | Base RPC 429 | $59.76m |
| BENJI Polygon | Polygon Blockscout 403 | dRPC 400 | $32.23m |
| USTB Plume | Plume explorer found both positive holders at the pin | Plume RPC returned zero logs in the window | $3.82m |
| OUSG Polygon | Zero identified contract supply | Holder ranking undefined | $0 |
| USYC Arc | Zero identified contract supply | Holder ranking undefined | $0 |

The eight positive-supply deployments together are worth at most **$203.48m** at the applied fund marks (see `observations.small_deployments_supply_usd`), even with gross counting across chains. Counting all eight in full, including the two Plume lots already credited, would bring the direct numerator to at most **$290.15m**. That is below the $458.95m headline cutoff and the $297.07m BUIDL deployment scenario cutoff. Excluding the remaining unresolved balances from possible direct backing still leaves both direct upper endpoints above 5%. These extremes hold the rest of the model fixed. [Arithmetic](RESULTS.md#buidl-deployment-scenario) · [Nest vaults](https://docs.nest.credit/about/available-vaults) · [Plume integration](https://www.plume.org/blog/plume-brings-institutional-real-world-yield-to-solana-with-launch-of-rwa-nest-vaults)

### First Solana observations

November 27, 2026 UTC, separate from the September pin. Each successful `getTokenSupply` response reports its finalized slot. A largest token account can be a custody or program account and is not an owner or beneficial-holder count. Recorded keyless attempts that hit rate limits, index exclusions or access denials leave rank unknown. [Requests and responses](../evidence/round1-supplement.json) · [Solana RPC](https://solana.com/docs/rpc/http/gettokenlargestaccounts)

| Fund | Supply slot | Current mint units | Largest-account indication |
| --- | ---: | ---: | --- |
| BUIDL | 474,405,838 | 380,840,998.07 | Index unavailable at the tested endpoints |
| USTB | 474,405,845 | 110,538.814980 | Index unavailable at the tested endpoints |
| USYC | 474,405,845 | 122.481545 | Index unavailable at the tested endpoints |
| OUSG | 474,405,838 | 0 | Zero current supply for the issuer-listed mint. The largest-account requests failed. |
| BENJI | 474,405,841 | 512,250.879500249 | At slot 474,405,851, one returned account held 512,250.879500249. Owner and September balance are unknown. |

## Round-two holder and control reads

### Current Stellar BENJI and Solana USTB

**November 27, 2026 UTC.** These reads record current chain state independently of the September 30 cutoff. Horizon walked accounts with a trust line for Franklin’s exact FOBXX representation `BENJI:GBHNGLLIE3KWGKCHIKMHJ5HVZHYIK7WTBE4QF5PLAKL4CJGSEU7HZIW5`. The final short page completed the 13-page traversal across Horizon ledgers 65,693,450–65,693,454. The observed 2,576 accounts included 1,019 positive trust lines totaling **1,325,203,561.9795506 BENJI**. This is a live trust-line sum across several ledgers. Other forms of issued balance and shareholder accounting require separate evidence. [Issuer asset mapping](https://www.franklintempleton.com/.well-known/stellar.toml) · [Horizon accounts API](https://developers.stellar.org/docs/data/apis/horizon/api-reference/list-all-accounts) · [Requests, page boundaries and balances](../evidence/round2-readbacks.json)

| Largest observed Stellar trust lines | BENJI units | Authorized |
| --- | ---: | --- |
| 1 | 314,738,922.2426427 | Yes |
| 2 | 254,239,914.5875924 | Yes |
| 3 | 208,775,429.2102662 | Yes |

The three addresses held **58.69% of the observed positive trust-line units**. Franklin’s `stellar.toml` lists four issuer accounts. None equals a top-three address. Direct Horizon account lookups show no `home_domain` for any of the three, and all three show the same account-reserve sponsor. The sponsor also has no home domain and does not appear in the issuer list. The operator and accounting role of **each** address and the sponsor remain unresolved. A shared sponsor identifies who supplies the account reserve and is insufficient to identify control, issuer inventory, custody or beneficial ownership. The authorization flag records issuer permission on the trust line. [Public account IDs and fields](../evidence/stellar-benji-identification-2026-11-27.json) · [Franklin issuer mapping](https://www.franklintempleton.com/.well-known/stellar.toml) · [Stellar account fields](https://developers.stellar.org/docs/data/apis/horizon/api-reference/resources/accounts/object)

| SEC reporting period | FOBXX class net assets (B.4) | Shares outstanding (B.5) | November traversal units ÷ fund shares |
| --- | ---: | ---: | ---: |
| September 30, 2026 | $667,960,091.75 | 667,967,346.67 | 1.98× |
| October 31, 2026 | $833,554,415.30 | 833,590,155.07 | 1.59× |

Both filings identify the same series `S000067043` and sole class `C000215714`. The November traversal shows **491,613,406.91 more units** than the October filing shows shares. A later Horizon `/assets` response returned **1,325,210,161.9795506** units grouped by authorization, 6,600 more than the traversal, and the same **2,576** trust-line accounts. The reads were taken at different times. Even the closer October comparison mixes dates and account semantics. The unexplained difference could include November subscriptions, distribution or custody inventory, or a different mapping from chain balances to the transfer agent’s register. Public data here cannot apportion those explanations. Until a same-date, transfer-agent-backed reconciliation exists, **do not infer beneficial ownership, fund-holder concentration, or the September Stellar share of the BENJI residual** from these units. The September SEC denominator remains in the model. [September SEC readback](../evidence/franklin-filing-readback-2026-09-30.json) · [October SEC readback](../evidence/franklin-filing-readback-2026-10-31.json) · [Horizon asset fields](https://developers.stellar.org/docs/data/apis/horizon/api-reference/resources/assets/object)

**Solana USTB.** `getTokenLargestAccounts` failed at the official endpoint (429), PublicNode (403) and dRPC (400), then succeeded at Pocket at finalized slot **474,414,430**. Its three largest token accounts held **110,486.371703**, **45.480468** and **2.000000 USTB**. `getTokenSupply` returned **110,538.814980 USTB** one finalized slot later. The largest account alone was about **99.95%** of that nearby supply. Account-level concentration leaves controller and beneficial ownership unresolved. The September Solana and book-entry splits remain unknown. [Exact calls, errors and responses](../evidence/round2-readbacks.json) · [Solana RPC semantics](https://solana.com/developers/docs/rpc/http/gettokenlargestaccounts) · [Superstate deployment API](https://api.superstate.com/v3/funds/USTB)

### Pinned Safe controls and operator evidence

| September 30 position | Owner threshold and module page | Public attribution and disposition |
| --- | --- | --- |
| Ethereum BUIDL-I rank 2 | 4-of-7, zero enabled modules | **Organization and wallet role corroborated.** Crypto Relief’s first-party donation page lists the exact Safe. The sources do not establish any downstream backing or its absence. [Crypto Relief](https://cryptorelief.in/donate) |
| Optimism BUIDL rank 1 | 1-of-1, zero enabled modules | **Safe control resolved. Operator and downstream token unresolved.** Blockscout named the proxy with no public tags. The Securitize feed and launch disclosure establish the deployment, without attributing this holder. [Blockscout](https://optimism.blockscout.com/api/v2/addresses/0xd06fc8c16fa5ab9e32f1bb5e3a41bc2212342d29) · [Issuer feed](https://public-feed.securitize.io/asset-info?symbol=BUIDL) · [Securitize launch disclosure](https://investors.securitize.io/news/news-details/2025/BlackRock-and-Securitize-Debut-New-BUIDL-Share-Class-on-Solana-Network-03-25-2025/default.aspx) |
| Ethereum USYC rank 1 | 2-of-4, zero enabled modules | **Safe control resolved. Operator and downstream token unresolved.** The explorer supplied no public tags. Circle’s public Binance arrangement does not attribute this Ethereum wallet. [Blockscout](https://eth.blockscout.com/api/v2/addresses/0xb1a6ac52a21435c744b5b4129b07e6c44bcd629b) · [Circle disclosure](https://investor.circle.com/news/news-details/2025/Circles-USYC-Now-Supported-as-Yield-Bearing-Off-Exchange-Collateral-for-Binances-Institutional-Clients/default.aspx) |

The archive calls include the master copy, threshold, `getOwners()` count and `getModulesPaginated(address,uint256)` count and terminal cursor, plus the pin and its linked successor. The readbacks omit signer account lists. Module counts describe one Safe extension mechanism. They do not establish offchain liabilities or any other contract’s claims on the underlying. [Pinned calls](../evidence/round2-readbacks.json) · [Safe contract source](https://github.com/safe-global/safe-smart-account)

### Plume Nest access

The nTBILL and nBASIS contracts held **338,816.706554** and **985.447129 USTB** at Plume block **96,561,570**. The pinned share, hook and authority runtime bytes match the Plume explorer bytecode. The explorer marks the two BoringVault share sources partially verified and the BlacklistHook and RolesAuthority sources fully verified. The source hashes and URLs are in the readback. Both share contracts call their configured hook on the sender for `transfer` and `transferFrom`. At the pin both hooks were unpaused and the examined pool senders were clear of the blacklist. The test recipient had no runtime code, and neither vault authority allowed it to call the privileged `enter` or `exit` directly. Read-only transfers from the two pools still delivered the quoted share quantities to that recipient in simulation. This distinguishes primary vault permissions from secondary receipt acquisition. Nest describes both receipts as portfolio shares and currently lists USTB in both strategies. At the pin the same contracts both held USTB and controlled share issuance and burns through privileged asset entry and exit. This supports vault-level attribution. The current allocation weights supply no September amounts, and the receipt confers no specific claim to USTB units. [Vault directory](https://docs.nest.credit/about/available-vaults) · [Pinned calls and source hashes](../evidence/pinned-market-controls-2026-09-30.json)

| Receipt and Rooster V2 pool | Pinned share inventory | Read-only quotes | Transfer and depth |
| --- | ---: | --- | --- |
| nTBILL / USDC.e, `0x0aa5e0458d48cc7911381a66b9f227c64983b2c4` | 58.466196 | 1 USDC.e → 0.957206 shares. 1,000 USDC.e → 54.540327 shares. 0.05% fee. | Quoted output transfer returned true. The large input runs into shallow liquidity. The output is worth about $56.98 at the one-unit quote and the route is dust-only under the study's rule. |
| nBASIS / pUSD, `0x0a3951519c8c3b15a65e42562ac8ab5071b7a5ac` | 842.057378 | 1 pUSD → 0.937254 shares. 200 pUSD → 182.761636 shares. 0.05% fee. | Quoted output transfer returned true. About $195.00 at the one-unit quote, or about 2.50% below the linear one-unit estimate. Access is evidenced at a retail-size quote. |

**Trade funding.** The pUSD route does not require access to primary pUSD minting for the tested size. A separate pinned Rooster V2 pool quoted **204.465623 pUSD for 205 native USDC**, and a transfer of that quoted amount from the pool to the same recipient returned true. A second pool quoted **205.336651 pUSD for 205 USDC.e**, also with a successful delivery check. The two Curve pUSD funding leads returned less than 200 pUSD at the same input. These are separate read-only probes, without an executed multi-leg swap. [Official Plume token addresses](https://docs.plume.org/plume/developers/contract-addresses) · [pUSD mint terms](https://docs.plume.org/plume/tokens/plume-usd) · [Pinned funding reads](../evidence/pinned-market-controls-2026-09-30.json)

**Market discovery.** DEX Screener returned empty arrays and an initial GeckoTerminal query used the wrong chain slug. The corrected `plume-network` token-pools queries surfaced eight nTBILL and six nBASIS candidate pools. The fixture preserves their addresses and pinned token and market probes, including Curve quotes and Rooster V1 pool state. Plume’s earlier Royco disclosure names the Rooster nBASIS/pUSD pair. Rooster V2’s published factory confirmed the two selected pairs, and its quoter identified the same factory. No share Transfer logs appeared in the final 1,000 blocks for either token. The zero-log window cannot rule out swaps before it or an available but unused route at the pin. Both selected Rooster pools and the native-USDC funding pool were unlocked with plugin configuration 195. Their resolved plug-ins have byte-identical code after masking eight occurrences of the immutable pool address in each. The nTBILL pool plug-in matches explorer source for `AlgebraLimitOrderPlugin`. Its swap callbacks are callable by the pool and handle price observations, fees, farming and limit-order bookkeeping. The callbacks do not check trader or recipient eligibility. The fixture preserves the partial source-verification status and the pinned hashes, including hashes after masking. The quote inputs are maximum requested amounts. The captures contain output and fee only, so an out-of-range quote does not establish how much input a swap would consume. The read-only tests do not establish executed volume or exhaustive venue coverage. [Plume’s Rooster market announcement](https://www.plume.org/blog/royco-markets) · [Rooster V2 addresses](https://docs.rooster.trade/developers) · [Exact queries](../evidence/pinned-market-controls-2026-09-30.json)

**Terms.** Nest’s March 20, 2026 terms distinguish interface and protocol restrictions, and Plume’s pre-pin SEC submission describes contractual and IP restrictions for U.S. persons. The geographic policy also addresses direct smart-contract interaction. Receiving ERC-20 shares at the technical level does not confer eligibility for the offering, primary redemption privileges or fund shareholder rights. [Nest terms](https://docs.nest.credit/security-and-compliance/terms-and-conditions) · [Pre-pin SEC submission](https://www.sec.gov/files/ctf-memo-plume-network-inc-092226.pdf#page=2) · [Geographic policy](https://docs.nest.credit/security-and-compliance/geographic-restrictions) · [Vault directory](https://docs.nest.credit/about/available-vaults)
