# Blinq Sharia Review Product Scope Sheet

Status: draft for Sharia scholar / Islamic finance advisor review
Date: 2026-05-01
Audience: Sharia scholar, Islamic finance advisor, internal product/legal/engineering reviewers

## 1. Purpose

This scope sheet defines the specific Blinq product version being submitted for Sharia review.

It is not a fatwa, legal opinion, or public compliance claim. It is intended to prevent ambiguity by making clear what is in scope, what is out of scope, and what product constraints Blinq is willing to enforce for a Sharia-reviewed version.

## 2. Product Version Submitted For Review

The reviewed product is:

> A curated, spot-only, fully collateralized, USDC-settled simple binary event-market product for public-benefit forecasting or legitimate risk-management use cases, subject to qualified Sharia review.

The reviewed v1 is deliberately narrow. It excludes features that would increase riba, gharar, maysir, qimar, mughalabat, addiction, or governance-risk concerns.

## 3. In Scope

- Simple binary event markets only.
- YES/NO outcome-token style markets.
- USDC collateral only.
- Fully funded positions before execution.
- No leverage, no margin, no borrowing, and no liquidation engine.
- No yield, lending, treasury use, staking, or rehypothecation of user collateral.
- Curated market creation only.
- Market approval by an internal review committee.
- UMA-style oracle resolution using public sources and a dispute window.
- Transparent trading fee only.
- Admin controls held by Gnosis committee multisigs, with separate thresholds for critical and operational powers.
- Position limits, cooling-off controls, risk warnings, no casino UI, and loss-chasing prevention.
- Private diligence materials available for reviewer inspection: contract repositories, audit materials, architecture diagrams, and beta product access where appropriate. The reviewed version is pre-deployment; no deployment addresses should be included in this review pack.

## 4. Out Of Scope For First Review

- Permissionless market creation.
- Negative-risk markets.
- Multi-outcome market groups.
- Leverage, margin, borrowing, lending, or liquidation.
- Yield-bearing collateral or treasury yield on user funds.
- Sports betting.
- Casino-style markets.
- Celebrity, gossip, or private-person markets.
- Private-person harm or misfortune markets.
- Death, assassination, violence, war, terrorism, or unlawful-activity markets.
- Ultra-short-duration entertainment markets designed for rapid repeated speculation.
- Any market category the reviewing scholar flags as inappropriate.
- Any public claim that Blinq is halal, Sharia-compliant, or scholar-approved before review is complete.

## 5. Collateral Policy

- Accepted collateral: USDC only.
- User collateral must remain fully reserved for positions and redemptions.
- User collateral must not be lent, staked, rehypothecated, or deployed into yield strategies.
- User collateral must not be used for treasury operations.
- Blinq must disclose where collateral sits, who controls relevant contracts or accounts, and whether any emergency powers can affect balances or settlement.
- If stablecoin reserve treatment is relevant to the scholar's methodology, Blinq should ask whether USDC itself requires additional review.
- Because the reviewed version is not deployed yet, final collateral-address, contract-address, admin-address, oracle-configuration, and fee-configuration verification should happen after implementation and before any public Sharia claim.

## 6. Leverage And Financing Policy

- No leverage.
- No margin.
- No borrowing.
- No debt extension.
- No liquidation engine.
- No funding rate.
- No guaranteed return or yield.
- No financing charge.

## 7. Market Creation And Approval

Market creation is not permissionless.

Every market must be approved by a review committee before launch. The committee should record:

- market question,
- event category,
- public-benefit or risk-management rationale,
- resolution source,
- expiry,
- dispute process,
- prohibited-category check,
- manipulation-risk check,
- insider-information risk,
- whether the market depends on verified exposure,
- whether scholar review is required before launch.

## 8. Reviewed Initial Market Categories

These are the recommended initial categories for the first Sharia review. They are still subject to scholar approval.

### 8.1 Allowed Candidate Categories For Reviewed V1

- Public economic data releases, such as inflation, unemployment, GDP, or other official statistical releases.
- Weather, climate, agriculture, and logistics events where participants may have planning or operational exposure.
- Commodity supply-chain or inventory events where the market can support planning rather than entertainment.
- Technology and protocol milestone events, such as public software launches, blockchain upgrades, or network-availability milestones.
- Public infrastructure or operational events with objective resolution sources.
- Public-benefit research or forecasting questions where the output has planning value and is not tied to private harm.

### 8.2 Excluded From Reviewed V1 Unless Separately Approved

The following categories are excluded from the first reviewed version unless a scholar separately approves a narrower category-specific policy:

- Regulatory decisions.
- Central-bank or interest-rate-related events.
- Corporate events.
- Election or political events.
- Crypto-token price or market-cap events.
- Litigation or enforcement outcomes.
- Health or public-safety events.

### 8.3 Categorically Excluded Categories

- Sports.
- Casino-style or random outcomes.
- Celebrity gossip.
- Private-person personal outcomes.
- Death, assassination, injury, violence, war, terrorism, or unlawful activity.
- Markets that incentivize harm or manipulation.
- Markets involving minors.
- Short-duration dopamine-loop markets.
- Pure entertainment markets without public-benefit or risk-management rationale.

## 9. Oracle And Resolution Policy

The reviewed design assumes:

- UMA-style optimistic oracle process.
- Publicly identified resolution source.
- Clear ancillary market wording.
- Fixed expiry.
- Dispute window.
- Transparent liveness period, recommended minimum `24` hours for reviewed v1 where technically feasible.
- Defined manual or emergency resolution conditions.
- Public logging of resolution updates where possible.

Oracle rewards, proposal bonds, dispute costs, and related oracle operating costs should be paid only from Blinq operating funds or a disclosed operating treasury, not from user collateral and not through yield-bearing user balances.

If the implementation-reference oracle adapter's default liveness or manual-resolution safety period is shorter than the reviewed policy, Blinq should either modify the implementation, configure a longer period where supported, or document the compensating governance control before review.

Reviewer question:

> Is this oracle and dispute design sufficient to reduce gharar in market wording and settlement, or does the underlying binary event-contract structure remain problematic regardless of resolution clarity?

## 10. Fee Policy

Blinq will use a transparent trading service fee only.

For the Sharia-reviewed v1, the proposed fee posture is:

- target trading fee: no more than `100` basis points (`1.00%`) per charged trade leg,
- reviewed maximum fee cap: no more than `300` basis points (`3.00%`),
- fee receiver: Blinq operating treasury multisig, segregated from user collateral accounts and not connected to any yield-bearing user-collateral strategy,
- fee changes: critical admin action requiring the critical Gnosis committee threshold,
- fee type: service fee for exchange operation, not interest, funding, yield, loss-based monetization, or promotional incentive,
- fee policy: no maker rebates, LP incentives, referral rewards, liquidity mining, volume rewards, or promotional rewards in reviewed v1.

The implementation-reference exchange contract includes a maximum fee-rate control:

- default maximum fee rate: `1000` basis points,
- ceiling for configured maximum fee rate: less than `10000` basis points,
- fee receiver changes and max-fee changes are admin-controlled,
- a zero max-fee setting disables the max-rate check, so the Sharia-reviewed v1 should prohibit setting the max fee to zero unless the contract is changed or an equivalent nonzero policy/guard is enforced.

For Sharia review, Blinq should commit to configuring the reviewed deployment with a nonzero maximum trading-fee cap no higher than `300` basis points, even though the implementation-reference contract default is higher. If the contract is modified before deployment, the safer implementation is to make the reviewed max-fee cap explicit in deployment configuration or contract constants.

For the reviewed v1, fees should not include:

- interest,
- funding rates,
- borrow charges,
- yield participation,
- loss-based monetization,
- hidden spread controlled by the platform,
- jackpot-like rewards,
- LP rewards,
- maker rebates,
- referral incentives,
- liquidity mining,
- volume rewards,
- promotional rewards.

## 11. Admin And Governance Policy

Blinq will use Gnosis committee multisigs for admin and operational controls.

Critical admin powers should require a broad committee threshold:

- signer set: at least 15 signers,
- threshold: at least two-thirds of the signer set,
- example: at least 10 of 15 signers if the committee has exactly 15 signers.

Critical powers should include:

- contract upgrades, if any,
- collateral configuration,
- oracle configuration,
- fee receiver changes,
- max fee changes,
- emergency/manual resolution,
- permanent market shutdown,
- adding or removing admin signers,
- changes to the market-admissibility policy,
- changes to Sharia-reviewed product constraints.

Operational powers may use a smaller Gnosis committee threshold:

- signer set: 5 signers,
- threshold: 3 of 5 signers.

Operational powers may include:

- routine operator rotation,
- routine market-operations actions under an already approved market policy,
- emergency pause only, where pause is protective and cannot move funds or resolve outcomes,
- publishing market-review records,
- administrative maintenance that does not alter user balances, payout logic, collateral policy, fee policy, oracle policy, or Sharia-reviewed constraints.

Manual resolution should not be treated as a routine operational action. Because it can directly affect user payout outcomes, it should require the critical admin threshold, documented reason, public/source evidence, and post-action review.

Recommended timing controls:

- critical non-emergency admin changes: minimum `48` hour timelock,
- fee-cap, fee-receiver, collateral, oracle, upgrade, signer, and market-policy changes: critical admin threshold plus timelock,
- emergency pause: instant `3-of-5` operational action if protective only, with no fund movement, no payout change, and no market resolution,
- emergency pause duration: maximum `72` hours unless ratified by the critical admin threshold,
- manual resolution: critical admin threshold, documented evidence memo, public/source basis, and at least `24` hour notice/challenge period where technically and legally feasible,
- post-action review: required for every emergency pause or manual-resolution event.

Blinq should disclose:

- committee members or role categories,
- signer threshold,
- powers controlled by the committee,
- whether the committee can pause markets,
- whether the committee can change fees,
- whether the committee can change oracle settings,
- whether the committee can add operators,
- whether the committee can manually resolve or override outcomes,
- whether contracts are upgradeable,
- whether admin actions are timelocked or publicly logged.

Reviewer question:

> Do the committee powers create unacceptable discretion, ambiguity, custody, or unfairness concerns?

## 12. User Protection Policy

The reviewed design includes:

- position limits,
- cooling-off periods,
- risk warnings,
- no casino-style UI,
- no jackpot language,
- no leaderboards or gamified loss-chasing,
- no "bet", "wager", "degen", or "win big" framing,
- loss-chasing prevention,
- market-category restrictions.

Recommended default limits for reviewed v1:

- per-user per-market exposure cap: lower of `1%` of market open interest or `1,000` USDC equivalent unless the user is separately approved for a lower-risk institutional/hedging use case,
- per-user daily new exposure cap: `5,000` USDC equivalent during the initial reviewed phase,
- first-use cooling-off period: `24` hours between account approval/deposit and first trade where feasible,
- post-limit cooling-off: additional `24` hour cooling-off after a user hits a position or daily exposure cap,
- no push notifications or UI prompts designed to encourage immediate re-entry after loss.

## 13. Evidence Available For Private Review

Blinq can provide the following privately:

- contract repositories,
- audit materials,
- system diagrams,
- beta URL,
- contract architecture explanation,
- collateral-flow diagram,
- fee-flow diagram,
- oracle-resolution diagram,
- market-admissibility process,
- admin/operator role table.

These materials should be used for diligence. They should not be quoted publicly unless Blinq explicitly approves disclosure.

The current reviewed version is pre-deployment. The reviewer should treat contract repositories and diagrams as implementation-reference materials, not as proof of a live deployed Sharia-reviewed product.

Before any public Sharia-related claim after deployment, Blinq should provide a post-deployment verification pack including:

- final deployed contract list,
- bytecode/source verification status,
- collateral token configuration,
- fee receiver configuration,
- max-fee configuration,
- oracle configuration,
- admin multisig configuration,
- operator role configuration,
- market-admissibility policy version,
- responsible-access/UI screenshots,
- treasury/collateral no-yield attestation.

## 14. Core Questions For Reviewer

1. Does a simple binary event contract remain qimar, maysir, or mughalabat even if it is fully collateralized, non-levered, curated, and objectively resolved?
2. Does public-information value create acceptable countervalue, or is it only a byproduct of a wagering-like transaction?
3. Are public-benefit forecasting markets acceptable, or must participants have verified real-world exposure?
4. Are USDC collateral and non-yield custody acceptable under the reviewer's methodology?
5. Are trading fees acceptable as service fees under this structure?
6. Are UMA-style oracle resolution and dispute windows sufficient to reduce gharar in settlement?
7. Are Gnosis committee admin powers acceptable if disclosed and controlled?
8. Which market categories are acceptable, restricted, or prohibited?
9. What product language may Blinq use before formal approval?
10. If the open binary-market structure is not acceptable, what alternative structure should Blinq consider?
