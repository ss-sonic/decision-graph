# Private Contract Evidence Pack: Blinq Sharia Review

Research date: 2026-05-01

## Purpose

This file is private supporting evidence for improving `docs/blinq_shariya.md`.

It gives the document-improvement loop concrete implementation context for the Sharia review questions around collateralization, market resolution, settlement, fees, operator controls, and contract transparency.

This file does not establish that Blinq is halal, Sharia-compliant, scholar-approved, audited, deployed, or production-ready. It should only help the public document move from abstract design language to concrete diligence questions and implementation-backed conditional claims.

## Public-Document Handling Rules

- Do not expose local repository paths in the public revised document.
- Do not say these repos are public proof unless Blinq separately provides public links or permission.
- Do not say these contracts are deployed for the Sharia-reviewed product. The reviewed product version is pre-deployment.
- Do not say these contracts are audited for Blinq or production-ready unless Blinq supplies scope-specific audit evidence and approval to share it.
- Do not cite these repos as Sharia authority.
- Use this material to strengthen implementation review language: "Blinq can provide contract-level implementation artifacts for technical and Sharia diligence."
- If discussing architecture publicly, describe capability categories, not private repository names or filesystem paths.

## Evidence Items

### C-EVM-001: Conditional Token Framework Exchange

- Type: `private_repo`
- Locator: `/Users/development/work/blinq/betme/pm-contracts/ctf-exchange`
- Relevant files:
  - `docs/Overview.md`
  - `docs/CTFExchange.md`
  - `docs/mixins/AssetOperations.md`
  - `docs/mixins/Auth.md`
  - `docs/mixins/Pausable.md`
  - `src/exchange/CTFExchange.sol`
  - `audit/ChainSecurity_Polymarket_Exchange_audit.pdf`

#### What it supports

- A CTF-style binary outcome-token exchange can be modeled around ERC1155 outcome tokens and ERC20 collateral.
- The exchange design supports atomic swaps between outcome tokens and collateral.
- Signed EIP-712 orders are used in a hybrid model where order matching/execution services are offchain while settlement happens onchain.
- Complementary binary outcome tokens can be minted from collateral and merged back into collateral, supporting the invariant that a complete YES/NO set maps back to one unit of collateral.
- Trading entry points are guarded by operator controls, pause controls, and reentrancy protection.
- The fee receiver, max fee rate, proxy factory, safe factory, token registration, admin roles, and operator roles are governance/diligence items that must be disclosed for review.

#### Sharia-review relevance

- Supports the claim that Blinq can provide concrete contract artifacts for review of collateralization, settlement, fee logic, market lifecycle, and operator controls.
- Helps the Sharia document ask sharper questions about whether the payoff, tokenization, fee, and settlement mechanics create maysir, gharar, riba, or unfairness concerns.
- Supports a public statement that contract-level review should include full-set collateralization, mint/merge logic, signed order semantics, fee constraints, pausing, operator powers, and token registration controls.

#### Limits / do not overclaim

- This does not prove Blinq has deployed the reviewed product. The current reviewed version should be treated as pre-deployment.
- This does not prove the final deployed system will use this exact contract unchanged.
- This does not prove user funds are non-custodial in every Blinq product surface.
- This does not prove there is no riba, gharar, or maysir.
- This does not prove admin/operator controls are acceptable for Sharia or compliance review.
- The audit file is for the referenced exchange implementation; do not present it as a Blinq audit unless Blinq confirms scope and permission.

#### Public phrasing allowed

- "Blinq can provide private contract-level materials for review of binary outcome-token accounting, signed-order settlement, collateral mint/merge mechanics, fee logic, and operator controls."
- "The Sharia review should inspect the actual exchange contracts, including collateral handling, order authorization, fee limits, pause/admin controls, and market-token registration."

#### Public phrasing forbidden

- "Blinq's contracts are audited."
- "Blinq's exchange is Sharia-compliant."
- "Blinq has no custody risk."
- "The contracts prove this is not gambling."

### C-EVM-002: Negative-Risk Conditional Token Adapter

- Type: `private_repo`
- Locator: `/Users/development/work/blinq/betme/pm-contracts/neg-risk-ctf-adapter`
- Relevant files:
  - `docs/NegRiskAdapter.md`
  - `docs/NegRiskOperator.md`
  - `docs/MarketDataManager.md`
  - `docs/index.md`
  - `src/NegRiskAdapter.sol`
  - `src/NegRiskOperator.sol`
  - `src/WrappedCollateral.sol`
  - `src/Vault.sol`
  - `audit/Polymarket Multi-Outcome Markets Audit.pdf`

#### What it supports

- The adapter converts collections of NO tokens in mutually exclusive binary markets into corresponding YES-token and collateral positions.
- The design uses wrapped collateral to collateralize negative-risk markets and positions.
- Complete YES/NO positions can be split, merged, redeemed, and converted.
- Market creation and question preparation are permissioned through operator/admin roles.
- Outcome reporting and resolution involve oracle/admin flows, including flagged-question and emergency-resolution paths.
- Fees on negative-risk conversion can be collected into a vault.
- The implementation includes invariant tests and gas snapshots, which are useful for technical diligence.

#### Sharia-review relevance

- This is directly relevant to the Sharia questions around mutually exclusive market groups, synthetic position conversion, collateral adequacy, fees, vault flows, oracle authority, and admin discretion.
- It supports adding a dedicated diligence section asking whether negative-risk conversions create additional gharar, qimar/maysir, countervalue, or fairness issues beyond simple binary markets.
- It supports asking whether vault-held fees, wrapped collateral mechanics, and synthetic minting introduce riba-like, custody, or trust issues that need separate review.

#### Limits / do not overclaim

- Negative-risk conversion is technically useful but may make the Sharia analysis harder, not easier.
- Synthetic wrapped collateral and NO-token burning should be treated as review-critical mechanics, not as automatically acceptable.
- Admin/oracle resolution powers must be reviewed as possible trust, fairness, and ambiguity concerns.
- The audit file should not be represented as a Blinq audit unless Blinq confirms scope and permission.

#### Public phrasing allowed

- "If Blinq supports mutually exclusive event groups or negative-risk-style conversions, scholar and technical review should separately inspect the conversion, collateralization, fee, vault, and resolution mechanics."
- "The strongest review package should distinguish simple binary markets from multi-outcome or negative-risk market groups because the latter introduce additional accounting and fairness questions."

#### Public phrasing forbidden

- "Negative-risk markets are Sharia-safe."
- "Wrapped collateral removes all Sharia concerns."
- "Admin resolution powers are harmless."

### C-EVM-003: UMA CTF Oracle Adapter

- Type: `private_repo`
- Locator: `/Users/development/work/blinq/betme/pm-contracts/uma-ctf-adapter`
- Relevant files:
  - `README.md`
  - `src/UmaCtfAdapter.sol`
  - `src/interfaces/IUmaCtfAdapter.sol`
  - `audit/Polymarket_UMA_Optimistic_Oracle_Adapter_Audit.pdf`

#### What it supports

- A CTF prediction-market system can use an optimistic oracle adapter to initialize questions, store ancillary resolution data, request outcome data, handle liveness windows, handle disputes, and resolve markets.
- The adapter prepares CTF conditions and sends resolution requests to UMA's Optimistic Oracle.
- Undisputed requests resolve after a liveness period; disputed requests can reset or fall back to UMA's DVM process.
- Anyone can call `resolve` after resolution data is available.
- Admin/manual resolution paths exist and need explicit review.
- Reward tokens, proposal bonds, liveness, and ancillary data are resolution-design parameters.

#### Sharia-review relevance

- Supports concrete diligence around objective resolution, oracle design, dispute process, market ambiguity, and post-event settlement.
- Helps strengthen the document's claim that gharar mitigation depends not only on clear market wording but also on the oracle process, liveness period, dispute handling, manual override rules, and evidence source for final resolution.
- Supports a review question about whether reward tokens, proposer bonds, dispute incentives, or oracle fees create any interest-like, unfair, or excessive-uncertainty concerns.

#### Limits / do not overclaim

- An optimistic oracle can reduce ambiguity only if market terms and resolution data are precise.
- Oracle liveness and dispute handling do not by themselves resolve maysir/qimar concerns.
- Admin/manual resolution powers must be disclosed and reviewed.
- The audit file should not be represented as a Blinq audit unless Blinq confirms scope and permission.

#### Public phrasing allowed

- "The Sharia review should inspect the oracle and resolution process, including ancillary market wording, liveness, dispute paths, manual override rights, and who can influence final settlement."
- "Objective resolution is an implementation requirement, not merely a document claim."

#### Public phrasing forbidden

- "UMA resolution makes the product Sharia-compliant."
- "Oracle-based settlement removes gharar."
- "The system has no discretion risk."

## Cross-Cutting Diligence Questions For The Sharia Document

### Collateral / custody

- What collateral assets are accepted?
- Are user positions fully collateralized at all times?
- Can complete outcome-token sets always be merged or redeemed for collateral?
- Does any collateral sit in a treasury, vault, or reserve that earns yield?
- If stablecoins are used, does the review need to consider issuer reserves or yield-bearing wrappers?
- Who can move collateral outside normal settlement/redemption flows?

### Fees / revenue

- What fees are charged on trades, conversions, redemptions, market creation, oracle resolution, or liquidity incentives?
- Are fees fixed service fees, percentage trading fees, spreads, funding charges, interest-like charges, or yield participation?
- Who receives fees?
- Can admin change fee rates?
- Are fee limits enforced onchain?

### Market creation / admissibility

- Who can create markets?
- Who approves market categories?
- Are recreational, entertainment-only, harmful, violence-linked, death, war, or manipulation-prone markets excluded?
- Does each market have a written public-benefit, forecasting, or verified-risk-management rationale?
- Are multi-outcome or negative-risk markets reviewed separately from simple binary markets?

### Oracle / resolution

- What source determines the final outcome?
- What exact ancillary data or resolution wording is used?
- Who can dispute?
- How long is the liveness period?
- What happens if the outcome source is ambiguous?
- Who has emergency/manual resolution power?
- Are resolution changes visible and challengeable?

### Admin / operator controls

- Who controls admin roles?
- Who controls operator roles?
- Can trading be paused?
- Can fees, factories, markets, tokens, or oracle parameters be changed after market launch?
- Are admin powers timelocked, multisig-controlled, disclosed, and logged?
- What are the user protections if an admin/operator acts incorrectly?

### Negative-risk / multi-outcome mechanics

- Does conversion between NO-token sets and YES/collateral positions create additional countervalue or fairness concerns?
- Does synthetic wrapped collateral change the Sharia analysis?
- Are all mutually exclusive outcomes clearly exhaustive?
- What happens if all questions resolve false?
- Are conversion fees acceptable as service fees or do they require separate treatment?

## Recommended Public Document Improvements

Use this file to help the next doc-loop cycle do the following:

- Add or strengthen a "Contract Implementation Evidence Needed" section.
- Replace generic "fully collateralized" claims with a review requirement that the actual mint/merge/redeem contracts prove collateral sufficiency.
- Replace generic "objective resolution" claims with a review requirement that market wording, oracle source, liveness, dispute, and manual override rules are disclosed.
- Add a specific warning that negative-risk or multi-outcome markets require separate Sharia analysis from simple binary markets.
- Add a private/internal note that Blinq should prepare a contract diligence pack for scholars and advisors.
- Keep all private paths, audit PDFs, and repo names out of the public document unless Blinq chooses to disclose them.

## Suggested Private Diligence Pack To Prepare Before Scholar Review

- Architecture diagram mapping exchange, conditional tokens, adapter, oracle, collateral, vault, fee receiver, admin, operator, and user flows.
- Contract list with explicit pre-deployment status. Do not include unrelated or reference deployment addresses in the Sharia review pack.
- Admin/operator role table.
- Collateral-flow diagram.
- Fee-flow diagram.
- Oracle-resolution and dispute-flow diagram.
- Market-admissibility policy.
- Negative-risk / multi-outcome explanation, if used.
- Audit reports with scope notes and permission to share.
- Known limitations, open issues, and planned changes.
