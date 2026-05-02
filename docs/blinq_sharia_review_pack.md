# Proposal: Blinq as a Candidate Onchain Information Market for Sharia Review

## Design Principles for Reducing Gambling-Like Mechanics and Supporting Qualified Sharia Assessment

---

## 1. Executive Summary

Prediction markets are often misunderstood because they appear similar to gambling at the surface level: a user takes a view on an uncertain future event and may profit if correct.

However, this framing misses the deeper function of prediction markets.

A prediction market should not be treated as outside the gambling analysis merely because it produces prices. The narrower thesis of this proposal is that a carefully constrained event-market design may be presented for qualified review as an information-market candidate rather than as recreational wagering, if its markets are curated, objectively resolvable, non-levered, fully collateralized, and focused on public-benefit forecasting or legitimate risk management.

Its proposed function is to aggregate distributed knowledge, beliefs, research, and private conviction into a public price signal. That price is intended to operate as a live probability estimate of a future event.

In this sense, Blinq should be evaluated as a candidate for:

> **An onchain information-market design for pricing socially useful uncertainty, subject to qualified Sharia review.**

The Sharia-focused design goal would not be to create random games of chance or entertainment wagering. It would be to make selected forms of real-world uncertainty more legible and verifiable, while recognizing that usefulness, transparency, and maysir mitigation depend on actual market categories, implementation, user behavior, and scholar review.

This proposal argues a narrower and more contested point: Blinq may be presented for qualified review as a candidate information-market design only if it satisfies the following conditions. This framing must be tested against existing adverse Sharia analysis of prediction markets, binary-option-style payoffs, qimar, maysir, and mughalabat, and should not be presented as an established Sharia conclusion.

- Markets are based on real-world, objectively resolvable events.
- Prices emerge from user-driven market activity, not house-controlled odds.
- The output of the market is useful public information.
- Settlement is transparent and rule-based.
- Contracts are fully collateralized.
- Market creation is curated to avoid harmful or purely recreational speculation.
- The system avoids interest, excessive ambiguity, manipulation, and exploitative mechanics.

The proposal also argues that a Sharia-aligned design candidate is possible if the design avoids the core prohibited elements of Islamic finance:

- **Riba**: interest or usury.
- **Gharar**: excessive uncertainty or contractual ambiguity.
- **Maysir**: gambling or games of chance.

This document is a design proposal for qualified Sharia review. It is not a religious ruling, legal opinion, or final final compliance claim.

The key conclusion is:

> A curated, non-levered, fully collateralized, transparent event-market design focused on public-interest forecasting and legitimate risk management may reduce gambling-like characteristics and may support an information-market argument, subject to qualified Sharia review of the actual market categories, contract terms, collateral handling, fee model, oracle process, governance controls, and user-protection mechanics.

---

## 2. The Core Misunderstanding

The common criticism is simple:

> "Users are betting on events, therefore it is gambling."

This is an incomplete argument.

Many commercial and financial activities involve uncertain future outcomes, but that observation is not enough to establish Sharia permissibility. Equities, commodities, insurance, futures, options, and credit each have their own Islamic-finance treatment and cannot be used as blanket analogies for prediction markets.

The narrower point is this:

> Uncertainty alone is not the complete Sharia analysis. The relevant review must examine the contract structure, traded subject matter, purpose, payoff mechanics, collateral, fees, user behavior, and whether the arrangement creates riba, excessive gharar, or maysir.

A prediction market may become more distinguishable from recreational gambling at the product-purpose level when it is designed for:

- Forecasting.
- Price discovery.
- Information aggregation.
- Risk transfer tied to actual exposure.
- Hedging under a scholar-reviewed structure.
- Accountability of claims.
- Public knowledge formation.

However, purpose does not by itself resolve the Sharia analysis. Qualified reviewers may still ask whether the binary payoff, countervalue, and gain/loss structure resemble qimar or maysir even where the market produces information.

---

## 3. What Makes Gambling Different

Gambling is typically characterized by:

- A game of chance or entertainment-first event.
- No meaningful public informational output.
- Odds controlled by the house or operator.
- A structural edge against users.
- Wealth transfer without productive economic value.
- High addiction risk.
- Outcomes that are random, artificial, or recreational.
- Little or no connection to real economic exposure.

Examples include:

- Roulette.
- Slot machines.
- Dice games.
- Pure sports betting for entertainment.
- Random outcome games.
- Casino-style wagering.

The primary output of gambling is private excitement and monetary gain or loss.

It does not produce a useful public signal.

---

## 4. What Makes Prediction Markets Different

The proposed distinction is functional and conditional, not automatic. A curated prediction market can convert participant beliefs into prices, but that price signal is relevant to the Sharia argument only if the market is objectively resolvable, adequately liquid, resistant to manipulation, and tied to a public-benefit or legitimate risk-management purpose.

Such a market asks:

> What do capital-weighted participants currently imply about the probability of a future event?

For example:

- If a fully collateralized binary event contract trades at `$0.65`, the price may be interpreted as an approximate market-implied estimate of trader beliefs about the event, not as a literal or guaranteed 65% probability. Wolfers and Zitzewitz argue that prediction-market prices can often be close to mean trader beliefs under certain assumptions, while later calibration work and platform-level studies suggest that liquidity, fees, time value, trader concentration, manipulation, and favorite-longshot bias can materially distort the probability interpretation.
- If new information arrives, the price updates.
- If participants disagree, they trade.
- If someone believes the market is wrong, they can express that belief with capital.
- The market price is intended to operate as a live, public forecast.

Under those conditions, the market may function as a mechanism for information discovery.

The intended public output is not merely the transfer of gains and losses between traders.

The intended public output is a probability signal, while the Sharia review must still assess whether the payoff structure, countervalue, market purpose, and user behavior create maysir or gharar concerns.

---

## 5. Blinq as an Onchain Information Market

Blinq-style markets may be offered for qualified review as candidate event-information markets, but that characterization is contested and should not be treated as a settled Sharia conclusion.

They allow people to trade claims about future outcomes. These claims are:

- Event-based.
- Time-bound.
- Objectively resolvable.
- Priced by market participants.
- Settled through transparent rules.

The market price acts as a real-time estimate of collective belief.

When these conditions are actually implemented and enforced, Blinq may ask qualified scholars to evaluate whether the public-information function is sufficient to distinguish the design from qimar, maysir, or mughalabat objections. The document should not assume that this distinction will be accepted.

The point is not that every event contract is automatically outside the gambling analysis. The narrower claim is that a curated market with objective resolution, public informational value, and responsible-access controls may be a stronger candidate for Sharia review than an open-ended betting product, while recognizing that contemporary Islamic-finance commentary has reached adverse conclusions on similar designs.

---

## 6. Why Onchain Settlement Matters

Onchain settlement may support parts of the information-market argument, but blockchain implementation is not by itself Sharia-dispositive.

A properly designed onchain event market can potentially provide:

- Transparent settlement.
- Public auditability.
- Fully collateralized contracts.
- Open market history.
- Verifiable liquidity.
- Rule-based redemption.
- Composable data feeds.
- Reduced reliance on opaque operators.
- Public verification of balances, collateral flows, and settlement actions.

These properties are not automatic merely because a system is onchain. They depend on Blinq's smart-contract architecture, collateral custody, oracle design, administrative controls, dispute process, and whether any offchain operator can alter outcomes, freeze assets, or change settlement conditions. For qualified review, Blinq should be prepared to disclose whether contracts are upgradeable, who controls admin keys, how collateral is held, whether collateral or treasury assets earn yield, whether stablecoin reserves or rewards introduce interest-like exposure, how oracle disputes are resolved, and what emergency powers can affect user balances or settlement.

This is materially different from traditional opaque betting venues where the operator controls odds, internal risk, settlement, and user exposure.

Where the smart-contract architecture, oracle process, collateral custody, permissions, and governance controls actually permit public inspection, the system may be easier to audit and challenge.

That transparency can support the market-infrastructure framing, but it does not by itself resolve maysir, gharar, contract-structure, or user-purpose concerns.

---

## 7. Why Financial Risk Does Not Equal Gambling

Risk exists in every meaningful market.

The presence of risk does not automatically make an activity gambling.

The distinction depends on:

- Purpose.
- Structure.
- Contract clarity.
- Economic function.
- Social utility.
- Presence or absence of manipulation.
- Whether the market produces useful information.
- Whether the market helps manage real-world exposure.

A prediction market can be speculative, but speculation alone is not the same as gambling.

Speculation becomes more defensible when it contributes to:

- Liquidity.
- Price discovery.
- Forecasting accuracy.
- Risk distribution.
- Better public understanding of uncertainty.

This is similar to how traders in commodity or financial markets may speculate, but their activity can still contribute to market depth and price discovery.

---

## 8. The Public-Good Argument

A curated and well-functioning prediction market may create a public-good-like output: a live probability signal that others can observe and use. This claim is strongest where markets are liquid, resistant to manipulation, tied to socially or economically relevant events, and not driven primarily by entertainment speculation.

Traditional information sources have weaknesses:

- Polls are slow.
- Experts can be biased.
- Media narratives are distorted.
- Social media is noisy.
- Surveys are cheap talk.
- Forecasts are rarely financially accountable.

Prediction markets can improve on casual opinion by requiring participants to attach economic cost to belief. Foundational empirical work, including Wolfers and Zitzewitz on prediction-market prices as probability estimates, supports the narrower claim that prediction markets can sometimes produce useful, though imperfect and assumption-dependent, estimates of trader beliefs. That literature should be read with the caveats below: performance varies by platform, market design, liquidity, category, time to resolution, participation constraints, and trader concentration.

That support should be stated with limits. More recent evidence on modern prediction-market platforms is mixed: accuracy varies materially by platform, market structure, liquidity, participation limits, and category. Prices can diverge across platforms for the same event, and observed favorite-longshot bias means a quoted price should be treated as an imperfect market-implied estimate rather than a neutral probability oracle. Accuracy can deteriorate in thin, entertainment-driven, highly concentrated, or manipulation-prone markets.

A prediction market is therefore useful, in well-designed contexts, because it can make claims:

- Comparable.
- Tradable.
- Accountable.
- Continuously updated.
- Publicly visible.
- Economically weighted.

That signal may in principle be useful outside the trading venue if it is sufficiently liquid, calibrated, manipulation-resistant, and relevant to a reviewed market category. Blinq should not claim actual use by external audiences unless it can provide adoption evidence.

---

## 9. Candidate Framing for Scholar Evaluation

One framing Blinq may present for qualified review is:

> Blinq may be evaluated as a candidate organized information market or price-discovery venue, while scholars separately assess whether the binary payoff, countervalue, and stake-and-loss structure remain qimar-, maysir-, or mughalabat-like.

In this framing, Blinq would argue that market activity can contribute to a public probability signal. Reviewers should still assess the adverse view that the traded position remains a stake-and-loss event contract without sufficient countervalue, even if a useful signal is produced as a byproduct.

This framing is strongest only where market categories are curated, resolution is objective, and the market produces useful public information or supports credible risk-management use cases. It remains a Blinq design proposal; no qualified reviewer is treated here as having endorsed it.

A roulette table produces no knowledge.

A prediction market on inflation, regulation, elections, protocol upgrades, weather, supply chains, or economic indicators may produce useful public information, subject to liquidity, calibration, manipulation-resistance, and category review.

The price becomes a compressed signal of collective belief.

A sufficiently liquid, well-calibrated, and category-appropriate market signal could in principle inform external observers or risk-planning users. No Blinq-specific external uptake should be claimed unless Blinq provides implementation or adoption evidence.

---

## 10. The Sharia Question

A Sharia-aligned design candidate requires careful review.

It cannot be assumed that every prediction market is automatically aligned with Islamic finance principles.

Islamic finance is generally concerned with avoiding:

- **Riba**: interest, usury, or guaranteed return on debt.
- **Gharar**: excessive uncertainty, ambiguity, or hidden risk in the contract.
- **Maysir**: gambling, games of chance, or wealth transfer through wagering.

For qualified review, these concepts should be anchored in recognized Islamic-finance standards and scholar analysis rather than treated as informal labels. Relevant reference points include AAOIFI Sharia Standard No. 31 on controls of gharar in financial transactions, AAOIFI Sharia Standard No. 20 on sale of commodities in organized markets, and AAOIFI Sharia Standard No. 21 on financial papers. None of these standards directly addresses prediction markets or onchain event contracts. Applied here by analogy, they direct attention to contract terms, subject matter, price, delivery, ownership transfer, gharar, and whether the transaction has productive economic substance.

AAOIFI Sharia Standard No. 20 is reported in Islamic-finance source materials as containing strong restrictions on current-form futures and options trading. Together with scholar analysis of binary-option-style transactions, this gives reviewers a concrete analogical basis to argue that an all-or-nothing event-contract payoff may remain qimar-, maysir-, or mughalabat-like even if market wording is clear, positions are fully collateralized, and settlement is transparent. Whether that analogy controls the analysis for a fully collateralized, curated, cash-settled event-information market is itself a question for qualified scholars. Blinq should treat this as a central review issue and should obtain paragraph-level standard review from qualified advisors before relying publicly on any contrary interpretation.

In addition, named scholar analysis gives reviewers a more direct objection than general analogy. Mufti Muhammad Taqi Usmani has, in published work on options and futures, treated options as impermissible where the option itself is not a tangible sale object and the transaction contains gharar or qimar, and has objected to futures where settlement is often price-only and speculative. This does not decide Blinq's case and is not a ruling on prediction markets specifically, but it means a binary event contract should be reviewed against established objections to option-like and futures-like structures, not only against broad definitions of uncertainty.

Therefore, the question is:

> Can a prediction market be designed in a way that avoids riba, minimizes gharar, and reduces maysir-related concerns to a level acceptable on qualified Sharia review?

This proposal argues that the answer can be yes, but only under a disciplined design framework and subject to qualified scholar evaluation.

---

## 11. Avoiding Riba

A basic spot prediction market does not require interest.

There is no need for:

- Interest-bearing deposits.
- Debt-based leverage.
- Guaranteed yield.
- Lending against positions.
- Time-based return on capital.
- Interest paid to liquidity providers.

A Sharia-aligned prediction market should use:

- Fully collateralized positions.
- Non-interest-bearing collateral.
- No margin lending.
- No debt-based leverage.
- No yield generated from interest-bearing instruments.

Under this structure, Blinq may be better positioned to avoid riba-related concerns than a leveraged, margin-based, yield-bearing, or debt-financed product. This is a necessary but not sufficient condition: avoiding interest, debt financing, and leverage does not resolve the separate gharar and maysir objections to binary event-contract payoffs. Qualified review must therefore separately examine the actual collateral custody model, treasury policy, fee model, liquidity-provider incentives, rebates, rewards, and any future financing or leverage features.

The intended design principle is that the user should not lend money for guaranteed excess return, earn interest on idle balances, borrow to take positions, or receive interest-like compensation through the product structure.

---

## 12. Reducing Gharar

The contract itself must not be ambiguous.

A prediction market can reduce gharar by ensuring:

- Clear market wording.
- Objective resolution criteria.
- Known expiry time.
- Transparent oracle source.
- Fixed payout rule.
- Fully collateralized settlement.
- No hidden operator discretion.
- Public dispute process.
- Clear redemption mechanics.
- No unclear counterparty obligation.

The key distinction Blinq should ask qualified scholars to evaluate is:

> The event outcome is uncertain, but the contract terms should be made as explicit as possible before trading begins.

This distinction may reduce ambiguity in market wording, oracle source, expiry, payout, fees, and dispute process. It does not by itself resolve gharar concerns at the contract-structure level. Reviewers should separately assess whether the traded claim has acceptable subject matter and countervalue, whether settlement is merely cash-settled speculation, and whether the event contract resembles an impermissible option-like or binary payoff structure under the relevant Sharia methodology.

Example of clear market design:

> "Will BTC close above $100,000 on Coinbase at 00:00 UTC on 31 December 2026?"

This market has:

- A defined asset.
- A defined price source.
- A defined threshold.
- A defined timestamp.
- A defined settlement condition.
- A defined payout rule.

This reduces contractual ambiguity, while leaving the substantive Sharia review of structure and countervalue open to qualified scholars.

---

## 13. Addressing Maysir

Maysir is the hardest objection.

A related review category is mughalabat: staking money on an uncertain outcome where the losing side pays the winning side without receiving real countervalue. Contemporary public Islamic-finance commentary located in this review has applied this framing directly to Polymarket- and Kalshi-style prediction markets and reached adverse conclusions. Blinq does not need to accept those conclusions as final for its own proposed design, but it should explicitly ask qualified scholars whether curation, public-information value, full collateralization, and objective resolution are sufficient to distinguish Blinq from that mughalabat analysis.

A prediction market becomes gambling-like when it is used for:

- Pure entertainment.
- Addiction-driven speculation.
- Random events.
- Sports-style betting.
- Celebrity gossip.
- Harmful outcomes.
- Markets with no informational or economic value.
- Markets where users only seek thrill-based payoff.

This remains the central review-risk area even with strong curation. Reviewers may evaluate prediction-market and binary event-contract payoff structures as qimar, maysir, or mughalabat at the contract-structure level, especially where payment is certain from one side but uncertain from the other, the participant either loses the stake or receives more money, and the trade lacks productive countervalue, ownership transfer, cooperative risk-sharing, or a genuine risk-management function. Under that view, information production and curation may be relevant mitigating factors, but they do not automatically transform a wagering-like payoff into a permissible transaction.

Therefore, a Sharia-focused Blinq design should not be an open-ended betting platform.

It should be presented for review as a curated information market focused on socially useful uncertainty and legitimate risk-management use cases.

The difference is not only technical. It is also moral and product-level.

The market must be designed around:

- Public benefit.
- Useful forecasting.
- Legitimate risk management.
- Transparent information discovery.
- Research-backed participation.
- Exclusion of harmful or frivolous markets.
- Controls against manipulation and addiction.

The pro-Sharia argument is strongest when the platform is not positioned as "bet on anything."

It should be positioned as:

> A market for pricing socially useful uncertainty.

---

## 14. Market Categories That Can Be Defensible

A Sharia-focused information-market candidate should distinguish between categories with a stronger initial review case and categories requiring heightened review, rather than treating all public events alike.

Categories that may warrant initial scholar review include events where Blinq can document actual, identifiable hedging or planning use cases and show that the market is designed for forecasting or risk management rather than open-ended speculation. Until that evidence is supplied, the categories below should be treated as illustrative candidates, not as established defensible use cases:

- Economic indicators.
- Inflation outcomes.
- Commodity supply events.
- Weather events.
- Agricultural risks.
- Supply-chain disruptions.
- Energy production outcomes.
- Business milestone verification.
- Risk indicators relevant to real-world planning.

Categories requiring heightened scholar review include:

- Public governance outcomes.
- Elections or political outcomes.
- Protocol governance outcomes.
- Public policy outcomes.
- Technology milestones.
- Scientific forecasts.
- Market structure events.

These categories may produce useful information, but usefulness alone should not be treated as sufficient. Review should ask whether the market has objective resolution, plausible non-recreational use, limited manipulation risk, and a credible connection to planning or legitimate risk management.

---

## 15. Market Categories That Should Be Excluded

A Sharia-aligned information market should avoid:

- Sports betting.
- Casino-style games.
- Random number outcomes.
- Celebrity gossip markets.
- Death or assassination markets.
- War escalation markets that create perverse incentives.
- Markets involving private individual harm.
- Markets based on unlawful activity.
- Markets where participants can directly cause the outcome.
- Markets with unclear or subjective resolution.
- Pure entertainment wagers.
- Highly addictive short-duration markets.
- Markets that encourage compulsive trading.

This exclusion framework is essential.

Without curation, the Sharia argument becomes much weaker.

---

## 16. Hedging and Risk Management

The strongest economic defense of prediction markets is risk management.

A participant may have real-world exposure to an event and use a prediction market to hedge that exposure.

Illustrative exposure categories may include:

- Rainfall.
- Port closures.
- Regulatory changes.
- Protocol governance.
- Election-related policy.
- Weather.
- Commodity supply.
- Energy production.

These remain illustrative scenarios, not evidence of identified Blinq users or pilot deployments.

In these cases, the market is not merely a recreational wager.

It becomes a tool for managing uncertainty.

This may make a narrow, exposure-based use case closer to risk-management infrastructure than recreational wagering, but the analogy must be handled carefully. Conventional insurance, futures, and options are themselves contested in Islamic finance, and takaful is the more relevant Sharia reference point for cooperative risk-sharing.

For Blinq, the stronger and narrower claim is:

> Markets are more defensible for Sharia review when participants have actual, identifiable pre-existing exposure to the event and when the product is designed to reduce or manage that exposure rather than enable entertainment speculation. If Blinq relies on a hedging argument, it should consider whether scholars require an institutional or gated risk-management mode, exposure verification, position limits tied to documented exposure, or a separately reviewed takaful-style or cooperative-pool structure.

Even this narrower claim requires caution. Takaful-style risk sharing is based on cooperative pooling and tabarru'-style mutual support, which is structurally different from open-market counterparty trading where one participant's gain may be funded by another participant's loss. Blinq should therefore not assume that a user's hedging purpose alone is sufficient. Scholar review should assess whether any hedging use case calls for exposure verification, institutional access controls, position limits, cooperative-pool features, or other design changes.

A Sharia-focused design should therefore prioritize markets where hedging and planning use cases are credible.

---

## 17. Product Design Principles for Sharia Alignment

A Sharia-aligned prediction market should follow these design principles:

### 17.1 No Interest

- No interest on deposits.
- No interest-bearing treasury strategy.
- No lending-based leverage.
- No guaranteed yield.

### 17.2 No Leverage

- Spot-only markets.
- Fully funded positions.
- No margin.
- No liquidation engine.
- No debt extension.

### 17.3 Full Collateralization

- Every contract must be backed by collateral.
- No fractional reserve.
- No hidden counterparty exposure.

### 17.4 Clear Resolution

- Objective event definition.
- Public resolution source.
- Fixed expiry.
- Transparent dispute rules.

### 17.5 Market Curation

- No sports betting.
- No random games.
- No harmful markets.
- No private-person misfortune markets.
- No manipulation-prone markets.

### 17.6 Public-Benefit Focus

- Markets should produce useful forecasts.
- Markets should help with planning, research, or hedging.
- Markets should not exist only for entertainment.

### 17.7 Manipulation Controls

- Insider trading rules.
- Position limits.
- Oracle safeguards.
- Market surveillance.
- Dispute resolution.
- Anti-manipulation enforcement.

### 17.8 Responsible Access

- Cooling-off periods.
- User limits.
- Risk warnings.
- No addictive product loops.
- No casino-style UI.
- No gamified loss chasing.
- No misleading payout framing.

### 17.9 Scholar and Governance Review

- Sharia review process.
- Market admissibility committee.
- Transparent governance standards.
- Periodic compliance review.

---

## 18. Why Blanket Permissibility Is Not the Right Claim

The correct claim is not:

> All prediction markets are approved under Sharia.

That would be too broad and easy to attack.

The stronger and more cautious claim is:

> The prediction market primitive can be designed as a candidate for Sharia review when implemented as a curated, non-interest, non-levered, fully collateralized information market focused on public-benefit forecasting and legitimate risk management. Whether such a design qualifies as Sharia-aligned in any specific jurisdiction or under any specific school of fiqh remains a matter for qualified scholars.

This framing is more precise.

It admits that bad implementations can become gambling-like.

But it defends the underlying primitive as worth bringing to formal review.

---

## 19. Why "All Prediction Markets Are Gambling" Is Also Wrong

The opposite claim is also too broad.

Saying all prediction markets are gambling ignores their potential informational and economic function.

A prediction market may, under appropriate design and conditions:

- Produce real-time public forecasts.
- Aggregate distributed knowledge.
- Improve planning.
- Support hedging.
- Discipline narratives.
- Make uncertainty measurable.
- Reveal market expectations.
- Create transparent probability signals.

These functions are not what ordinary gambling is designed to produce. Their realization depends on liquidity, calibration, manipulation resistance, market category, and scholar review of the underlying contract structure.

Therefore, the proposal's narrower claim is that Blinq-style markets should be evaluated by design, purpose, market category, payoff structure, user protections, and actual use case, rather than judged only by their surface resemblance to betting. That evaluation may still lead some scholars to maysir concerns, especially for speculative binary event contracts without real exposure or productive purpose.

---

## 20. Proposed Positioning

Blinq should not be positioned as:

> "Bet on anything."

For Sharia-review materials, the safest interim positioning is:

> "A candidate event-risk market design for forecasting and risk management, presented for qualified Sharia review."

More categorical phrases such as "public probability layer," "transparent market for pricing uncertainty," or "onchain information market for real-world event probabilities" should be avoided unless qualified reviewers accept that framing for the implemented product.

The language matters.

The product should avoid:

- casino language
- betting language
- gambling metaphors
- jackpot framing
- degen positioning
- addictive urgency
- entertainment-first framing

The product should emphasize:

- information
- probabilities
- forecasting
- research
- public signals
- risk management
- transparency
- collateralization
- responsible access
- compliance
- market integrity

---

## 21. Candidate Argument and Adverse Review Issue

Prediction markets are often misunderstood because they appear similar to gambling: a user takes a position on an uncertain future event and may profit if correct.

But uncertainty alone is not the complete Sharia analysis.

Financial markets, insurance markets, commodity markets, and risk markets all involve uncertainty, but each has its own Islamic-finance treatment and cannot be used as a blanket analogy for prediction markets. The relevant review must examine purpose, structure, payoff mechanics, countervalue, collateral handling, fees, user behavior, and whether the arrangement creates riba, excessive gharar, or maysir.

A prediction market should not be analyzed only by surface resemblance to gambling, but contemporary public Islamic-finance commentary located in this review indicates that many scholars may still classify prediction markets as impermissible because of their binary payoff, stake-and-loss structure, and lack of countervalue. Blinq's argument is therefore not that prediction markets become acceptable whenever they avoid entertainment and randomness. The narrower argument is that Blinq should ask qualified scholars whether a constrained implementation can be distinguished from qimar, maysir, or mughalabat at the contract-structure level.

Blinq may distinguish its proposed design from casino-style products by emphasizing curation, objective resolution, collateralization, and public-information intent. However, adverse Sharia analysis may treat those differences as insufficient if the contract still functions as a binary stake-and-loss arrangement where one side's gain is funded by another side's loss without acceptable countervalue.

That price signal may carry information value when the market is liquid, curated, resistant to manipulation, and tied to events with public-benefit or risk-management relevance.

It may show what capital-weighted participants believe about the probability of an event, while still requiring review of whether the payoff structure, user purpose, and market category create maysir concerns.

Under those conditions, Blinq can argue that market prices may carry information value. That argument remains subject to scholar review and should not be treated as resolving qimar, maysir, mughalabat, gharar, or countervalue concerns.

Under the design conditions above, Blinq's proposed function is to aggregate dispersed knowledge, update as new information enters the market, and produce a public probability signal whose reliability depends on liquidity, market integrity, oracle quality, and governance controls.

Onchain implementation may strengthen this model where it actually delivers transparent settlement, auditable collateral, public market history, and rule-based redemption. These benefits depend on the smart-contract architecture, collateral custody, oracle process, administrative controls, dispute rules, and governance limits.

From a Sharia perspective, the same distinction matters.

A prediction market is not automatically permissible, and adverse contemporary commentary classifies similar designs as qimar, maysir, or mughalabat regardless of curation or collateralization. Blinq's proposal is that a constrained design may at least be brought to qualified review, not that it has overcome those objections.

It can avoid riba by eliminating interest, debt, and guaranteed yield.

It can reduce gharar by making every market's wording, expiry, oracle, payout, and settlement rule explicit, while recognizing that gharar at the contract-structure level remains a separate question for scholars.

It can reduce some maysir-related operational concerns by excluding recreational betting, harmful events, sports gambling, random games, and addictive product mechanics, while recognizing that qualified scholars must still review whether the event-contract payoff structure and user purpose remain impermissibly wagering-like.

Under this design, Blinq may submit the proposed product as a contested candidate for qualified Sharia review rather than as a position that has resolved the adverse maysir, qimar, or mughalabat objections.

The position this proposal should submit for review is therefore:

> Blinq should not ask reviewers to accept the information-market framing as settled. It should ask whether a transparent, fully collateralized, non-interest-based, curated event-market design for public-interest forecasting or verified risk management can be distinguished from qimar, maysir, or mughalabat. Qualified scholars may reject that distinction, require structural changes, or limit any acceptable design to narrower reviewed use cases.

---

## 22. Recommended Design Standard

To make the design suitable for serious Sharia review, Blinq should present the following as review questions, not as a self-certifying compliance checklist. Each answer should be accompanied by implementation evidence, such as smart-contract documentation, collateral custody records, treasury-yield policy, oracle and dispute procedures, admin-key disclosures, fee schedules, liquidity-incentive terms, market-admissibility minutes, and responsible-access controls. Qualified scholars should evaluate the implemented product, including market categories, contract terms, collateral handling, fee model, liquidity incentives, oracle process, governance controls, and user-protection mechanics.

Because contemporary public Islamic-finance commentary located in this review appears adverse to prediction markets in their current form, this review package should also include a dedicated response to that adverse analysis. In particular, Blinq should ask reviewers to address whether the proposed design remains mughalabat or qimar despite curation, full collateralization, transparent settlement, and public-information intent, and what structural changes would be required if the answer is yes.

1. Are markets spot-only, with no borrowing or synthetic leverage?
2. Are all positions fully funded before execution?
3. Is collateral non-interest-bearing, and are treasury or reward practices free of interest-like returns?
4. Does each market have objective resolution criteria, a fixed expiry, a disclosed oracle, and a dispute process?
5. Does the contract structure avoid excessive gharar in subject matter, countervalue, payout, fees, and settlement?
6. Does the payoff structure avoid or sufficiently mitigate maysir concerns, including zero-sum wagering without productive purpose?
7. Is there a published market-admissibility framework?
8. Are harmful, entertainment-only, random, sports, private-harm, and addictive short-duration markets excluded?
9. Are public-benefit or risk-management categories defined with concrete criteria?
10. Are responsible-access limits, cooling-off periods, and loss-chasing controls implemented?
11. Are manipulation, insider-trading, oracle, and governance controls enforceable?
12. Is there ongoing Sharia review for new market categories and material product changes?
13. Does the product avoid casino-style language, UI, incentives, and promotional framing?
14. Is forecasting infrastructure clearly separated from recreational wagering?
15. What evidence will be provided to scholars to verify these answers?
16. If scholars conclude that binary event contracts remain structurally maysir-like despite curation and collateralization, what alternative structure will Blinq evaluate, such as a verified-exposure risk-management mode, a cooperative-pool or takaful-inspired model, or another scholar-reviewed contract form?
17. For each proposed market category, will Blinq document whether the use case depends on public-benefit forecasting, verified hedging of actual exposure, or both, and what evidence (including identifiable pre-existing exposure, documented external uptake of price signals, and exposure verification mechanics) is available to support that documentation?
18. Which adverse Sharia analyses of prediction markets, binary options, futures, qimar, maysir, and mughalabat have the reviewers considered, and how does the final review memorandum distinguish Blinq's implemented structure from those objections, if at all?
19. If no qualified reviewer accepts the information-market distinction for binary event contracts, will Blinq limit the Sharia-focused product to a different structure, such as verified-exposure risk management, cooperative pooling, or another reviewer-accepted contract form?

---

## 23. Final Conclusion

Blinq-style prediction markets should not be dismissed as gambling simply because they involve uncertain future outcomes, nor should they be assumed to escape that classification simply because they produce prices.

A more defensible interpretation, when the design constraints in this proposal are actually implemented, is that Blinq-style markets can be evaluated as candidate markets for pricing uncertainty, contested by adverse Islamic-finance analysis and subject to qualified scholar review.

Their intended public output is information, not entertainment-first wagering, but qualified scholars must decide whether that intent is sufficient to distinguish the design from qimar, maysir, or mughalabat at the contract-structure level.

When designed and governed properly, they may produce public probability signals, aggregate knowledge, and support planning. The risk-management argument is strongest only where actual exposure is identified and the structure is reviewed for Sharia acceptability. Even then, qualified scholars must review maysir, gharar, contract structure, payoff mechanics, countervalue, user behavior, and whether the binary event-contract form can be distinguished from qimar-like transactions.

From a Sharia perspective, the primitive can be made more defensible through disciplined design:

- remove interest,
- avoid leverage,
- fully collateralize positions,
- reduce contractual ambiguity,
- curate market categories,
- prohibit harmful and recreational markets,
- focus on public-benefit forecasting,
- implement responsible access,
- and establish Sharia review.

Therefore, the strongest position is:

> Blinq should be evaluated as a candidate onchain information market, not assumed to be approved under Sharia by default. The Sharia-focused design should be spot-only, non-levered, fully collateralized, objectively resolved, curated for public-benefit forecasting or legitimate risk management, and subject to qualified Sharia review before any public claim of permissibility or compliance.

This proposal distinguishes product design principles from a final religious ruling.

---

---

# Appendices: Review Scope, Controls, and Evidence Map

These appendices make the reviewed product concrete. They are part of the same review pack as the memo above and should be read as design constraints for the pre-deployment v1 submitted to a Sharia scholar or Islamic finance advisor.

## Appendix A: Product Scope and Reviewed v1 Constraints

### Product Version Submitted for Review

The reviewed product is a curated, spot-only, fully collateralized, USDC-settled simple binary event-market product for public-benefit forecasting or legitimate risk-management use cases, subject to qualified Sharia review.

The reviewed v1 is deliberately narrow. It excludes features that would increase riba, gharar, maysir, qimar, mughalabat, addiction, or governance-risk concerns.

### In Scope

- Simple binary event markets only.
- YES/NO outcome-token style markets.
- USDC collateral only.
- Fully funded positions before execution.
- No leverage, no margin, no borrowing, and no liquidation engine.
- No yield, lending, treasury use, staking, or rehypothecation of user collateral.
- Curated market creation only.
- Market approval by an internal review committee.
- UMA-style oracle resolution using public sources and a dispute window.
- Transparent trading service fee only.
- Admin controls held by Gnosis committee multisigs, with separate thresholds for critical and operational powers.
- Position limits, cooling-off controls, risk warnings, no casino UI, and loss-chasing prevention.
- Private diligence materials available for reviewer inspection: contract repositories, audit materials, architecture diagrams, and beta product access where appropriate.
- The reviewed version is pre-deployment; no live contract locations should be included in this review pack.

### Out of Scope for First Review

- Permissionless market creation.
- Multi-outcome market groups.
- Leverage, margin, borrowing, lending, or liquidation.
- Yield-bearing collateral or treasury yield on user funds.
- Sports betting.
- Casino-style markets.
- Celebrity, gossip, or private-person markets.
- Private-person harm or misfortune markets.
- Death, assassination, injury, violence, war, terrorism, or unlawful-activity markets.
- Ultra-short-duration entertainment markets designed for rapid repeated speculation.
- Public claims of religious approval before qualified review is complete.

### Reviewed Initial Market Categories

Allowed candidate categories for reviewed v1:

- Public economic data releases, such as inflation, unemployment, GDP, or other official statistical releases.
- Weather, climate, agriculture, and logistics events where participants may have planning or operational exposure.
- Commodity supply-chain or inventory events where the market can support planning rather than entertainment.
- Technology and protocol milestone events, such as public software launches, blockchain upgrades, or network-availability milestones.
- Public infrastructure or operational events with objective resolution sources.
- Public-benefit research or forecasting questions where the output has planning value and is not tied to private harm.

Excluded from reviewed v1 unless separately approved by a scholar under a narrower category-specific policy:

- Regulatory decisions.
- Central-bank or interest-rate-related events.
- Corporate events.
- Election or political events.
- Crypto-token price or market-cap events.
- Litigation or enforcement outcomes.
- Health or public-safety events.

Categorically excluded categories:

- Sports.
- Casino-style or random outcomes.
- Celebrity gossip.
- Private-person personal outcomes.
- Death, assassination, injury, violence, war, terrorism, or unlawful activity.
- Markets that incentivize harm or manipulation.
- Markets involving minors.
- Short-duration dopamine-loop markets.
- Pure entertainment markets without public-benefit or risk-management rationale.

## Appendix B: Controls Matrix

| Concern | Reviewed v1 Control | Evidence to Provide | Status | Reviewer Question |
|---|---|---|---|---|
| Riba from lending or interest | No lending, borrowing, margin, funding rate, or guaranteed return | Product policy, contract architecture, treasury policy | Confirmed intended constraint | Does USDC use require additional review because of reserve structure or issuer practices? |
| Yield on user collateral | No yield, staking, treasury use, or rehypothecation of user collateral | Collateral custody policy, treasury policy, account-flow diagram | Confirmed intended constraint | Is non-yield USDC custody acceptable if user funds remain fully reserved? |
| Leverage and liquidation | Spot-only, fully funded positions, no liquidation engine | Product scope sheet, exchange contract review, UI/API restrictions | Confirmed intended constraint | Does absence of leverage materially reduce riba/maysir concerns, or only remove a secondary issue? |
| Gharar in market wording | Clear question text, expiry, source, payout, and dispute rule before trading; category limits enforced | Market-admissibility policy, sample approved markets, oracle template | Recommended values selected | Are wording and resolution controls enough to reduce gharar, or does the event-contract form remain gharar-heavy? |
| Gharar in settlement | UMA-style oracle, public source, dispute window, recommended minimum 24h liveness where feasible | Oracle flow diagram, adapter docs, sample resolution record | Implementation alignment still needed | Are oracle and dispute controls sufficient? |
| Maysir / qimar from binary payoff | Curated public-benefit or legitimate risk-management markets; no recreational categories | Scope, category policy, market rationale records | Central unresolved issue | Does the binary stake-and-loss payoff remain qimar/maysir regardless of curation and collateralization? |
| Mughalabat / lack of countervalue | Require public-benefit forecasting or verified risk-management rationale for every market | Market rationale template, use-case evidence | Evidence needed | Is information value acceptable countervalue, or must users have verified real-world exposure? |
| Recreational gambling risk | Ban sports, casino-style, celebrity/gossip, death, war, violence, private harm, and short-duration entertainment markets | Prohibited-category list, UI policy | Recommended category posture selected | Should any allowed candidate categories also be narrowed? |
| Permissionless harmful markets | No permissionless market creation; committee approval required | Governance policy, approval workflow, committee charter | Confirmed intended constraint | Who must sit on the committee, and when must a scholar approve a category before launch? |
| Market manipulation | Position limits, insider/manipulation policy, committee review, oracle safeguards | Market surveillance policy, position-limit policy | Policy evidence needed | What minimum controls are required before a market is acceptable? |
| Collateral sufficiency | Every position fully collateralized; complete outcome-token set redeemable against collateral | Exchange contract docs, collateral-flow diagram, pre-deployment implementation plan | Contract evidence exists | What must be verified after implementation? |
| Custody and admin powers | Critical powers require at least 15 signers and at least two-thirds approval; operational powers use 3-of-5 only for bounded routine actions | Admin role table, multisig policy, timelock policy | Threshold specified | Do admin powers create unacceptable discretion, ambiguity, custody, or fairness concerns? |
| Operator control | Operators may execute matching/settlement functions; routine operator rotation may use 3-of-5 if settlement remains contract-constrained | Operator role table, exchange docs, logs/events | Contract evidence exists | Are operator powers acceptable if settlement is contract-constrained? |
| Fee model | Trading service fee only; target fee no more than 100 bps; reviewed max fee cap no more than 300 bps; no funding, interest, hidden spread, loss-based monetization, or rewards | Fee schedule, fee receiver, fee-cap policy | Recommended values selected | Are trading fees acceptable as service fees, and should reviewers require a lower cap? |
| Incentives | No LP rewards, maker rebates, referral incentives, liquidity mining, volume rewards, promotional rewards, jackpot rewards, or yield-like incentives in reviewed v1 | Fee policy and product scope | Confirmed excluded | Should any future incentive require separate review? |
| Stablecoin treatment | USDC only; no yield or treasury deployment | Stablecoin risk note, custody policy | Confirmed intended constraint | Is USDC acceptable as collateral for this reviewed product? |
| Oracle rewards and bonds | If used, paid only from Blinq operating funds or disclosed operating treasury; no user-collateral funding | Oracle configuration, reward/bond policy | Final config needed | Do oracle rewards, proposal bonds, or dispute incentives create any Sharia issue? |
| Manual / emergency resolution | Emergency pause may be instant 3-of-5 protective-only action, max 72h without critical ratification; manual resolution requires critical threshold, evidence, public/source basis, 24h notice/challenge where feasible, and post-action review | Emergency-resolution policy, admin role table, oracle docs | Recommended values selected | What emergency powers are acceptable without excessive discretion? |
| Multi-outcome mechanics | Excluded from first Sharia review | Product scope | Confirmed out of scope | What separate review is required if added later? |
| User addiction / loss chasing | Per-user per-market cap lower of 1% market OI or 1,000 USDC equivalent; daily new exposure cap 5,000 USDC equivalent; 24h first-use and post-limit cooling-off where feasible | UI policy, responsible-access settings, screenshots | Recommended values selected | What responsible-access controls are mandatory? |
| Product language | No public religious-approval claim before approval; no betting/casino/degen framing | Brand/copy policy, public screenshots | Policy evidence needed | What exact wording may Blinq use before and after review? |

## Appendix C: Contract Implementation Evidence Summary

This appendix summarizes private implementation-reference materials available for diligence. It does not embed private repository paths, live contract locations, or raw internal evidence.

### Exchange Implementation Reference

The exchange implementation-reference materials support review of:

- atomic swaps between binary outcome tokens and ERC20 collateral,
- hybrid exchange design where matching is offchain and settlement is onchain,
- signed order authorization,
- YES/NO outcome-token mint and merge mechanics,
- full-set collateral accounting where a complete complementary set maps back to collateral,
- symmetric trading fees,
- fee receiver and max-fee controls,
- admin/operator role separation,
- pause controls,
- token registration controls,
- non-reentrant operator fill and match functions.

Review relevance:

- Supports contract-level diligence around collateral sufficiency, settlement mechanics, fee routing, role permissions, and pause controls.
- Does not prove the reviewed product has been launched.
- Does not by itself resolve qimar, maysir, gharar, or countervalue questions.
- Final implementation should be reviewed again after deployment configuration is complete.

### UMA-Style Oracle Implementation Reference

The oracle implementation-reference materials support review of:

- optimistic oracle based resolution,
- public ancillary data used to define the question,
- binary condition preparation,
- liveness period configuration,
- dispute handling,
- request reset when disputes or ignore outcomes occur,
- public resolution once data is available,
- admin flag, unflag, pause, reset, and manual-resolution paths.

Review relevance:

- Supports diligence around objective resolution, dispute windows, manual override boundaries, and settlement clarity.
- Does not remove the need for scholar review of the binary event-contract structure.
- Any oracle reward, proposal bond, dispute cost, or manual-resolution authority should be separately disclosed.

### Private Attachments for Reviewer Inspection

Blinq may provide the reviewer private access to:

- implementation-reference repositories,
- audit materials with scope notes,
- architecture diagrams,
- collateral-flow diagram,
- fee-flow diagram,
- oracle-resolution diagram,
- beta product access where appropriate.

These materials are diligence attachments. They are not public claims and should not be quoted externally without Blinq's approval.

## Appendix D: Market Admissibility Policy

Market creation is not permissionless. Every market must be approved by a review committee before launch.

Each approved market record should include:

- market question,
- event category,
- public-benefit or risk-management rationale,
- resolution source,
- expiry,
- dispute process,
- prohibited-category check,
- manipulation-risk check,
- insider-information risk,
- whether verified exposure is required,
- whether scholar review is required before launch.

Committee review should reject any market that:

- falls into a categorically excluded category,
- is mainly entertainment-oriented,
- incentivizes harm,
- involves private-person outcomes,
- has ambiguous resolution terms,
- is likely to be manipulated by participants,
- depends on nonpublic information in a way that makes the market unfair,
- creates rapid repeated speculation without public-benefit or risk-management value.

New categories outside Appendix A should require separate scholar review before being included in a Sharia-focused product version.

## Appendix E: Responsible Access and UI Policy

The reviewed v1 should include the following controls:

- per-user per-market exposure cap: lower of `1%` of market open interest or `1,000` USDC equivalent, unless separately approved for a lower-risk institutional or hedging use case,
- per-user daily new exposure cap: `5,000` USDC equivalent during the initial reviewed phase,
- first-use cooling-off period: `24` hours between account approval/deposit and first trade where feasible,
- post-limit cooling-off: additional `24` hour cooling-off after a user hits a position or daily exposure cap,
- risk warnings before trading,
- no casino-style UI,
- no jackpot language,
- no leaderboards or gamified loss-chasing,
- no "bet", "wager", "degen", or "win big" framing,
- no push notifications or UI prompts designed to encourage immediate re-entry after loss.

The UI should emphasize information, forecasting, market integrity, public-benefit categories, risk controls, and qualified review boundaries.

## Appendix F: Collateral, Treasury, and Fee Policy

### Collateral and Treasury

- Accepted collateral: USDC only.
- User collateral must remain fully reserved for positions and redemptions.
- User collateral must not be lent, staked, rehypothecated, or deployed into yield strategies.
- User collateral must not be used for treasury operations.
- Blinq should disclose where collateral sits, who controls relevant contracts or accounts, and whether any emergency powers can affect balances or settlement.
- If stablecoin reserve treatment is relevant to the reviewer's methodology, Blinq should ask whether USDC itself requires additional review.

Because the reviewed version is pre-deployment, final collateral configuration, admin configuration, oracle configuration, and fee configuration should be verified after implementation and before any public religious-approval claim.

### Fees

- Target trading fee: no more than `100` basis points (`1.00%`) per charged trade leg.
- Reviewed maximum fee cap: no more than `300` basis points (`3.00%`).
- Fee receiver: Blinq operating treasury multisig, segregated from user collateral accounts and not connected to any yield-bearing user-collateral strategy.
- Fee changes: critical admin action requiring the critical Gnosis committee threshold and timelock.
- Fee type: service fee for exchange operation, not interest, funding, yield, loss-based monetization, or promotional incentive.
- No maker rebates, LP incentives, referral rewards, liquidity mining, volume rewards, promotional rewards, or jackpot-like rewards in reviewed v1.
- A zero max-fee setting should be prohibited because it disables max-rate validation in the implementation-reference exchange logic.

## Appendix G: Oracle, Emergency Pause, and Manual Resolution Policy

### Oracle Resolution

The reviewed design assumes:

- UMA-style optimistic oracle process,
- publicly identified resolution source,
- clear ancillary market wording,
- fixed expiry,
- dispute window,
- recommended minimum `24` hour liveness period where technically feasible,
- public logging of resolution updates where possible.

Oracle rewards, proposal bonds, dispute costs, and related operating costs should be paid only from Blinq operating funds or a disclosed operating treasury, not from user collateral and not through yield-bearing user balances.

If the implementation-reference oracle adapter's default liveness or manual-resolution safety period is shorter than the reviewed policy, Blinq should modify the implementation, configure a longer period where supported, or document a compensating governance control before review.

### Governance Timing Controls

- Critical non-emergency admin changes: minimum `48` hour timelock.
- Fee-cap, fee-receiver, collateral, oracle, upgrade, signer, and market-policy changes: critical admin threshold plus timelock.
- Emergency pause: instant `3-of-5` operational action if protective only, with no fund movement, no payout change, and no market resolution.
- Emergency pause duration: maximum `72` hours unless ratified by the critical admin threshold.
- Manual resolution: critical admin threshold, documented evidence memo, public/source basis, and at least `24` hour notice/challenge period where technically and legally feasible.
- Post-action review: required for every emergency pause or manual-resolution event.

Manual resolution should not be treated as a routine operational action because it can directly affect user payout outcomes.

## Appendix H: Reviewer Questions and Review Ask

### Core Questions

1. Does a simple binary event contract remain qimar, maysir, or mughalabat even if it is fully collateralized, non-levered, curated, and objectively resolved?
2. Does public-information value create acceptable countervalue, or is it only a byproduct of a wagering-like transaction?
3. Are public-benefit forecasting markets acceptable, or must participants have verified real-world exposure?
4. Is USDC collateral acceptable for this reviewed product if user collateral is not yield-bearing and remains fully reserved?
5. Are transparent trading service fees acceptable under this structure?
6. Are UMA-style oracle resolution and dispute windows sufficient to reduce gharar in settlement?
7. Are Gnosis committee admin powers acceptable if disclosed, thresholded, timelocked where appropriate, and limited by policy?
8. Which market categories are acceptable, restricted, or prohibited?
9. What product language may Blinq use before formal approval?
10. If the open binary-market structure is not acceptable, what alternative structure should Blinq consider?

### Recommended Review Ask

Please review this constrained v1 product design. Is it acceptable, unacceptable, or acceptable only with modifications? If unacceptable, is the issue the binary event-contract structure itself, the market categories, the collateral/fee/oracle mechanics, user behavior, or another design feature? What structural changes would make the product reviewable?

### Remaining Implementation Evidence Before Launch

Before any public religious-approval claim after implementation, Blinq should prepare a post-implementation verification pack including:

- final contract list,
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

