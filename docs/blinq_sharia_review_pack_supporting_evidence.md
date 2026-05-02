# Blinq Sharia Review Pack Supporting Evidence and Improvement Instructions

This file is private support context for improving `docs/blinq_sharia_review_pack.md`. It should guide the document loop, but it should not be pasted into the public reviewer pack verbatim.

## Purpose of the Review Pack

The review pack is intended for a qualified Sharia scholar and/or Islamic finance advisor. Its job is to make the reviewed product concrete enough for assessment, not to market Blinq or claim approval.

The improved document should remain a single sendable review pack containing:

- the cautious Sharia design memo
- product scope
- controls matrix
- contract implementation evidence summary
- market admissibility policy
- responsible access and UI policy
- collateral, treasury, and fee policy
- oracle, pause, and manual-resolution policy
- reviewer questions and review ask

## Current Reviewed Product Scope

The reviewed v1 should remain:

- pre-deployment
- simple binary event markets only
- USDC collateral only
- fully collateralized
- no yield
- no lending
- no treasury use of user collateral
- no rehypothecation
- no leverage
- no margin
- no borrowing
- no liquidation engine
- no permissionless market creation
- committee-approved markets only
- objective-resolution markets only
- public-source oracle resolution with dispute window
- no incentives, rebates, referral rewards, LP rewards, liquidity mining, or promotional rewards

Do not broaden this scope during improvement. If an edit would broaden scope, reject it or move it to internal notes as a future separately reviewed version.

## Governance Defaults to Preserve

Use these as selected review defaults unless the loop proposes stricter settings:

- Critical non-emergency governance actions should have a minimum 48h timelock.
- Critical governance should use a Gnosis committee with at least 15 signers and a 2/3 threshold.
- If exactly 15 signers are used, the threshold should be 10-of-15.
- Operational routine actions may use a smaller 3-of-5 process only when bounded and not value-transfer-critical.
- Emergency pause may be instant 3-of-5, but only as protective action.
- Emergency pause should expire or require critical ratification within 72h.
- Manual resolution is a critical action, not routine admin.
- Manual resolution should require evidence, public/source basis, notice/challenge where feasible, and post-action review.
- Where feasible, manual resolution should provide 24h notice/challenge before finalization.

## Fee and Collateral Defaults to Preserve

The reviewed v1 should use a trading service fee only.

Recommended defaults:

- Target trading fee: no more than 100 bps.
- Reviewed max fee cap: no more than 300 bps.
- No funding rate.
- No interest.
- No hidden spread.
- No loss-based monetization.
- No maker rebates.
- No referral incentives.
- No liquidity incentives.
- No volume rewards.
- User collateral should remain segregated and used only for settlement of user positions.

Contract evidence indicates a configurable fee cap mechanism exists in the exchange reference implementation, but the public review pack should not claim the reviewed product is deployed, audited, or production-ready.

## Responsible Access Defaults to Preserve

Responsible access controls should remain concrete:

- Per-user per-market exposure cap: lower of 1 percent of market open interest or 1,000 USDC equivalent.
- Daily new exposure cap: 5,000 USDC equivalent.
- First-use cooling-off: 24h where feasible.
- Post-limit cooling-off: 24h where feasible.
- Risk warnings before first trade and before increasing exposure.
- No casino UI.
- No streaks, jackpots, leaderboards, loss-chasing prompts, or dopamine-loop market surfacing.

## Market Category Policy

Allowed initial categories should remain narrow and public-benefit oriented:

- public economic data releases, excluding interest-rate and central-bank policy markets unless separately reviewed
- weather, climate, agriculture, and logistics events with objective public data
- commodity supply-chain or inventory events where the market can support real-world planning
- technology or protocol milestone events with objective public verification
- public infrastructure and operational events
- public-benefit research or forecasting topics with objective resolution

Categories requiring separate review before inclusion:

- regulatory outcomes
- central-bank or interest-rate outcomes
- corporate events
- election or political outcomes
- crypto-token price, market-cap, or volatility outcomes
- litigation or enforcement outcomes
- health and public-safety outcomes

Excluded categories:

- sports
- casino-style or random outcomes
- celebrity or gossip outcomes
- private-person harm
- death, injury, assassination, violence, war, terrorism, or unlawful activity
- minors
- markets that incentivize manipulation, harassment, panic, or real-world harm
- ultra-short-duration markets designed mainly for compulsive trading
- pure entertainment markets with no public-benefit or risk-management rationale

## Contract Evidence Language

The contract appendix should summarize implementation evidence by category, not by private path or deployment address.

In scope for the reviewed v1:

- exchange implementation reference, corresponding to the CTF exchange stack
- UMA-style oracle adapter reference

Out of scope:

- negative-risk or multi-outcome mechanics
- any chain-specific reference deployment
- any address currently present in repositories
- any claim that Blinq contracts are deployed

Preferred public language:

- "private implementation-reference materials"
- "exchange implementation reference"
- "UMA-style oracle implementation reference"
- "pre-deployment implementation plan"
- "reviewer inspection materials"

Avoid public language:

- local filesystem paths
- chain names or addresses from upstream/reference repos
- "deployed"
- "audited"
- "production-ready"
- "verified onchain" unless later proven for the exact reviewed version

## Evidence Hierarchy for the Loop

When improving the document, prioritize evidence in this order:

1. The consolidated review pack itself.
2. This supporting evidence file for stable scope and policy constraints.
3. `docs/blinq_sharia_external_source_pack.md` for external Islamic-finance and prediction-market source context.
4. `docs/blinq_sharia_contract_evidence.md` for private implementation-reference summaries.
5. Existing product scope and controls sheets, if provided, only to confirm appendices remain aligned.

Private evidence can justify whether the reviewed pack is internally coherent, but it should not be quoted as a public source unless separately approved for disclosure.

## Desired Improvements

Useful improvements include:

- reducing repetition without weakening caution
- making the reviewer ask more concrete
- making appendices internally consistent with the main memo
- clarifying which controls are hard constraints versus review questions
- moving private proof gaps to internal notes
- tightening overbroad claims about prediction markets, hedging, probability, or public benefit
- making the controls matrix easier for a reviewer to verify
- ensuring every implementation claim is phrased as pre-deployment or private-reference evidence

Do not optimize for persuasive tone if doing so reduces caution, truthfulness, or reviewer usefulness.

## Acceptance Checklist for a Revised Review Pack

A revised pack should:

- start with the same candidate-design posture
- keep Appendix A through Appendix H
- keep the reviewed v1 pre-deployment
- keep simple binary, USDC-only, fully collateralized, non-levered scope
- keep no incentives or rebates in reviewed v1
- keep the selected governance, fee, and responsible-access defaults
- avoid private paths, private URLs, deployment addresses, and chain-specific reference addresses
- avoid claiming approval, permissibility, deployment, audit completion, or production readiness
- separate public reviewer-facing text from internal proof gaps
