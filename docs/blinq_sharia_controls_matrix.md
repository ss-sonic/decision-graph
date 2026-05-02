# Blinq Sharia Review Controls Matrix

Status: draft for Sharia scholar / Islamic finance advisor review
Date: 2026-05-01
Related memo: `docs/blinq_shariya.md`
Related scope sheet: `docs/blinq_sharia_product_scope_sheet.md`

## Purpose

This matrix maps the main Sharia and product-risk concerns to the controls Blinq is willing to enforce, the evidence available for review, and the questions that still require qualified scholar or advisor judgment.

It is not a compliance claim. It is a working review tool.

## Controls Matrix

| Concern | Control | Evidence To Provide | Status | Reviewer Question |
|---|---|---|---|---|
| Riba from lending or interest | No lending, no borrowing, no margin, no funding rate, no guaranteed return | Product policy, contract architecture, treasury policy | Confirmed as intended v1 constraint | Does USDC use require additional review because of reserve structure or issuer practices? |
| Yield on user collateral | No yield, no staking, no treasury use, no rehypothecation of user collateral | Collateral custody policy, treasury policy, contract/account flow diagram | Confirmed as intended v1 constraint; evidence pack needed | Is non-yield USDC custody acceptable if user funds remain fully reserved? |
| Leverage and liquidation | Spot-only, fully funded positions, no liquidation engine | Product scope sheet, exchange contract review, UI/API restrictions | Confirmed as intended v1 constraint | Does the absence of leverage materially reduce riba/maysir concerns, or only remove a secondary issue? |
| Gharar in market wording | Every market must have clear question text, expiry, source, payout, and dispute rule before trading; reviewed v1 limited to allowed candidate categories unless scholar separately approves more categories | Market-admissibility policy, sample approved markets, oracle-resolution template | Recommended values selected; standalone policy still useful | Are the proposed wording and resolution controls enough to reduce gharar, or does the event-contract form remain gharar-heavy? |
| Gharar in settlement | UMA-style oracle, public source, dispute window, recommended minimum 24h liveness where technically feasible, manual-resolution rules | Oracle flow diagram, UMA-style adapter docs, sample market resolution record | Recommended values selected; implementation alignment still needed | Are oracle and dispute controls sufficient, and what manual override powers are acceptable? |
| Maysir / qimar from binary payoff | Curated public-benefit or legitimate risk-management markets; no recreational categories | Scope sheet, category policy, market rationale records | Central unresolved issue | Does the binary stake-and-loss payoff remain qimar/maysir regardless of curation and collateralization? |
| Mughalabat / lack of countervalue | Require public-benefit forecasting or verified risk-management rationale for every market | Market rationale template, use-case evidence, external uptake evidence if available | Evidence needed | Is information value acceptable countervalue, or must users have verified real-world exposure? |
| Recreational gambling risk | Ban sports, casino-style, celebrity/gossip, death, war, violence, private harm, ultra-short-duration markets; politics, regulatory, corporate, crypto-price, litigation, health, public-safety, and central-bank/interest-rate markets excluded from reviewed v1 unless separately approved | Market-admissibility policy, prohibited-category list, UI policy | Recommended category posture selected | Are the excluded categories sufficient, and should any allowed candidate categories also be narrowed? |
| Permissionless harmful markets | No permissionless market creation; committee approval required | Governance policy, approval workflow, committee charter | Confirmed as intended v1 constraint; process doc needed | Who must sit on the committee, and when must a scholar approve a category before launch? |
| Market manipulation | Position limits, insider/manipulation policy, committee review of manipulability, oracle safeguards | Market surveillance policy, position-limit policy, rejected-market examples | Policy needed | What minimum controls are required before a market is acceptable? |
| Insider influence over outcomes | Ban or restrict markets where participants can directly cause or materially influence the outcome | Market-admissibility policy, conflict policy | Policy needed | Are some event types impermissible because traders can influence the outcome? |
| Collateral sufficiency | Every position fully collateralized; complete outcome-token set redeemable against collateral | Exchange contract docs, collateral-flow diagram, pre-deployment implementation plan | Contract evidence exists; final deployed verification will be needed later | Does the proposed implementation prove collateral sufficiency, and what must be verified after deployment? |
| Custody and admin powers | Critical powers require a Gnosis committee with at least 15 signers and at least two-thirds approval; operational powers use 3-of-5 where they cannot move funds, change payout logic, change fees, change oracle policy, or alter reviewed constraints | Admin role table, multisig policy, timelock policy, pre-deployment governance plan | Governance threshold now specified; signer identities/roles still needed | Do admin powers create unacceptable discretion, ambiguity, custody, or fairness concerns? |
| Operator control | Operators may execute matching/settlement functions; routine operator rotation may use 3-of-5 operational approval if settlement remains contract-constrained | Operator role table, exchange contract docs, logs/events | Contract evidence exists; product-specific role evidence needed | Are operator powers acceptable if settlement is contract-constrained? |
| Fee model | Trading service fee only; target fee no more than 100 bps; reviewed max fee cap no more than 300 bps; fee receiver is Blinq operating treasury multisig segregated from user collateral; no funding, interest, hidden spread, loss-based monetization, or rewards; reviewed v1 prohibits zero max-fee setting | Fee schedule, fee receiver, fee-cap contract/policy, incentive policy | Recommended values selected | Are trading fees acceptable as service fees, and should scholars require a lower cap? |
| LP / maker / referral incentives | No LP rewards, maker rebates, referral incentives, liquidity mining, volume rewards, promotional rewards, jackpot rewards, or yield-like incentives in reviewed v1 | Fee policy and product scope sheet | Confirmed excluded from v1 | If incentives are introduced later, should they require separate Sharia review? |
| Stablecoin treatment | USDC-only collateral; no yield or treasury deployment | Stablecoin risk note, custody policy | Confirmed as intended v1 constraint; scholar view needed | Is USDC acceptable as collateral for this reviewed product? |
| Oracle rewards and bonds | UMA-style oracle rewards/bonds, if used, paid only from Blinq operating funds or disclosed operating treasury; no user-collateral funding and no yield-bearing user balances | Oracle configuration, reward/bond policy | Recommended values selected; final config needed | Do oracle rewards, proposal bonds, or dispute incentives create any Sharia issue? |
| Manual / emergency resolution | Emergency pause may be instant 3-of-5 operational approval if protective only, max 72h without critical ratification; manual resolution requires critical admin threshold, documented evidence, public/source basis, 24h notice/challenge where feasible, and post-action review | Emergency-resolution policy, admin role table, oracle docs | Recommended values selected | What emergency powers are acceptable without creating excessive discretion? |
| Negative-risk and multi-outcome mechanics | Excluded from first Sharia review | Product scope sheet | Confirmed out of scope | If later included, what separate review is required for wrapped collateral, conversion, vault fees, and multi-outcome fairness? |
| User addiction / loss chasing | Per-user per-market exposure cap: lower of 1% market OI or 1,000 USDC equivalent; daily new exposure cap: 5,000 USDC equivalent; 24h first-use cooling-off where feasible; 24h post-limit cooling-off; risk warnings; no casino UI; no jackpot/degen language | UI policy, responsible-access settings, screenshots, copy guidelines | Recommended values selected; evidence/screenshots needed | What responsible-access controls are mandatory? |
| Product language | No halal/compliance claim before approval; no betting/casino/degen framing | Brand/copy policy, public website screenshots | Policy needed | What exact wording may Blinq use before and after review? |
| Review governance | Sharia scholar / Islamic finance advisor reviews product version, categories, fees, collateral, oracle, and controls | Final review memo, reviewer comments, approval conditions | Pending review | Is the product acceptable, unacceptable, or acceptable only with modifications? |

## Evidence Checklist

Before sending the review pack, attach or prepare:

- Final Sharia design memo.
- Product scope sheet.
- This controls matrix.
- Contract architecture diagram.
- Collateral-flow diagram.
- Fee-flow diagram.
- Oracle-resolution and dispute-flow diagram.
- Admin/operator role table.
- Gnosis committee signer and threshold description: critical committee has at least 15 signers with at least two-thirds approval; operational committee uses 3-of-5 for bounded routine actions.
- Market-admissibility policy.
- Responsible-access and UI policy.
- Fee schedule.
- Treasury/collateral policy.
- Contract repositories or reviewer-access bundle.
- Audit materials with scope notes.
- Beta URL.
- Explicit pre-deployment status note. Do not include unrelated or reference deployment addresses.

## Remaining Items Before Review

- Confirm whether the implementation will enforce the reviewed fee cap through deployment configuration, contract constant, or governance policy.
- Confirm whether oracle liveness/manual-resolution timing can match the reviewed policy or needs implementation changes.
- Prepare standalone market-admissibility policy using the selected category posture.
- Prepare standalone responsible-access/UI policy using the selected default limits.
- Prepare standalone collateral/treasury policy with no-yield attestation.
- Prepare standalone emergency/manual-resolution policy using the selected timing and evidence requirements.
- Whether USDC collateral requires a separate stablecoin permissibility note.
- What post-deployment verification evidence scholars require before Blinq can make any public Sharia-related claim.

## Recommended Review Ask

Ask the reviewer:

> Please review this constrained v1 product design. Is it acceptable, unacceptable, or acceptable only with modifications? If unacceptable, is the issue the binary event-contract structure itself, the market categories, the collateral/fee/oracle mechanics, user behavior, or another design feature? What structural changes would make the product reviewable?
