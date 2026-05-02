# Supporting Evidence: Blinq Sharia Design Proposal

## Evidence Policy

This file is supporting context for improving `docs/blinq_shariya.md`.

Rules for agents:

- Treat this as a high-caution religious/compliance design topic.
- Do not write or imply a fatwa, final Sharia ruling, or legal opinion.
- Use evidence to sharpen the design argument and identify review requirements.
- If an Islamic finance issue is contested, present it as contested or requiring qualified scholar review.
- Do not convert a design thesis into a definitive claim that Blinq is halal or Sharia-compliant.
- Prefer primary Islamic finance standards, recognized scholarly sources, and reputable Islamic finance institutions over generic blog content.

## Core Concepts To Ground

### E-SHARIA-001: Riba

- Type: Islamic finance concept
- Publicly quotable: yes, if supported by a cited Islamic finance source in the final draft
- Working definition:
  - Riba generally refers to prohibited interest/usury or unjustified increase in loan/debt exchange contexts.
- Relevance to Blinq:
  - A Sharia-aligned Blinq design should avoid interest-bearing deposits, lending-based leverage, debt-based margin, guaranteed yield, and funding-rate mechanics that resemble interest.
  - A spot-only, fully collateralized event market is easier to defend than leveraged or debt-financed trading.
- Suggested public phrasing:
  - "The design should avoid riba by excluding interest-bearing balances, debt-based leverage, guaranteed yield, and lending-style margin."
- Review questions:
  - Does any collateral, margin, fee, or reward mechanism create an interest-like return?
  - Are user balances ever lent, rehypothecated, or yield-bearing?
  - Would any funding-rate or borrow-cost mechanism be introduced in later leverage products?

### E-SHARIA-002: Gharar

- Type: Islamic finance concept
- Publicly quotable: yes, if supported by a cited Islamic finance source in the final draft
- Working definition:
  - Gharar generally refers to excessive uncertainty, ambiguity, deception, or indeterminacy in a contract.
- Relevance to Blinq:
  - Prediction markets inherently involve uncertain future outcomes, so the key distinction is whether the contract terms are themselves ambiguous or whether the event outcome is uncertain but clearly specified.
  - The Sharia argument is stronger when market wording, oracle source, expiry, resolution process, payout, collateralization, fees, and dispute rules are explicit before users participate.
- Suggested public phrasing:
  - "The design should minimize gharar by making each market's wording, expiry, oracle, resolution rule, payout, fees, and dispute process explicit before trading begins."
- Review questions:
  - Are market questions objective and externally resolvable?
  - Can users understand exactly what they are buying, selling, and entitled to receive?
  - Are oracle and dispute processes clear enough to reduce ambiguity?

### E-SHARIA-003: Maysir

- Type: Islamic finance concept
- Publicly quotable: yes, if supported by a cited Islamic finance source in the final draft
- Working definition:
  - Maysir generally refers to gambling, games of chance, or zero-sum wagering where gain comes from another party's loss without productive purpose.
- Relevance to Blinq:
  - This is the central risk for prediction markets.
  - The strongest defense is not "prediction markets are never gambling"; it is that a constrained implementation can be designed around information discovery, public-benefit forecasting, and legitimate risk management rather than entertainment wagering.
- Suggested public phrasing:
  - "The maysir risk is reduced only if Blinq excludes recreational betting, random games, harmful markets, sports-style entertainment markets, and addictive mechanics, while focusing on public-interest forecasting or legitimate risk-management use cases."
- Review questions:
  - Are users primarily trading for information, hedging, or socially useful forecasting, or for entertainment wagering?
  - Are market categories curated to exclude gambling-like use cases?
  - Do product mechanics encourage addiction, rapid-fire speculation, or recreational betting behavior?

## Product Design Constraints

### E-SHARIA-004: Spot-only and no leverage

- Type: design constraint
- Publicly quotable: yes
- Supports:
  - A Sharia-aligned version should begin with spot-only, fully collateralized markets.
  - Leverage, margin, funding rates, liquidation games, and debt-based exposure increase riba/maysir concerns and should be excluded from the Sharia-focused design.
- Suggested public phrasing:
  - "The Sharia-focused version should be spot-only and fully collateralized; leverage should be excluded from the compliant design unless separately reviewed and approved by qualified scholars."
- Review questions:
  - Does the product include any borrowing, margin, liquidation, or synthetic leverage?
  - Are all user positions fully funded before trade execution?

### E-SHARIA-005: Market curation

- Type: design constraint
- Publicly quotable: yes
- Supports:
  - Open-ended "bet on anything" positioning weakens the Sharia argument.
  - Curation is necessary to exclude harmful, frivolous, entertainment-only, private-person misfortune, and manipulation-prone markets.
- Suggested public phrasing:
  - "The Sharia-aligned design should use a curated market list rather than permissionless creation, with explicit exclusions for sports betting, random games, celebrity gossip, death/assassination markets, harmful events, and addictive short-duration markets."
- Review questions:
  - Who approves markets?
  - What criteria determine public-benefit or legitimate risk-management value?
  - What markets are categorically excluded?
  - Is there an appeals or governance process?

### E-SHARIA-006: Information-market and risk-management framing

- Type: design thesis
- Publicly quotable: yes, with caution
- Supports:
  - Blinq's strongest framing is as an information market for pricing uncertainty, not as a gambling venue.
  - The argument is strongest when markets produce useful public probability signals or help participants manage real exposure.
- Suggested public phrasing:
  - "Blinq should be framed as an onchain information market for pricing uncertainty, with the Sharia-aligned product limited to market categories that serve public-benefit forecasting or legitimate risk-management purposes."
- Review questions:
  - Does each market category create useful information beyond private entertainment?
  - Can participants plausibly have real-world exposure to the events?
  - Is there evidence that the market price improves public understanding or risk planning?

### E-SHARIA-007: Scholar and governance review

- Type: governance requirement
- Publicly quotable: yes
- Supports:
  - The document should not claim Sharia compliance without qualified review.
  - A Sharia review board or advisor process should review market categories, contract structures, oracle/resolution rules, fee model, collateral model, and user protections.
- Suggested public phrasing:
  - "Final compliance positioning should be subject to qualified Sharia review of the market categories, contract terms, fee model, collateral handling, oracle process, governance controls, and user-protection mechanics."
- Review questions:
  - Which scholars or Islamic finance advisors will review the product?
  - Is review one-time or ongoing?
  - How are new market categories approved?
  - How are disputes, ambiguous outcomes, and harmful markets handled?

## Source Targets For Researcher

The researcher should look for credible, preferably primary or institutional sources on:

- AAOIFI standards or recognized Islamic finance guidance on riba, gharar, maysir, derivatives, and hedging.
- Islamic finance scholarship on derivatives, futures, options, risk management, and speculation.
- Scholarly or institutional discussion distinguishing hedging/risk management from gambling.
- Takaful / cooperative insurance analogies and limits.
- Islamic finance treatment of uncertainty in commercial contracts.
- Any scholarship directly discussing prediction markets, event contracts, binary options, gambling, or wagering.
- Regulatory or Sharia board examples where product purpose, contract clarity, and market category affect permissibility analysis.

## Internal Risk Notes

- The document should not argue that uncertainty alone is enough to make markets permissible. The Islamic finance question is not merely whether uncertainty exists, but whether the contract structure, purpose, payoff, and behavior create prohibited riba, gharar, or maysir.
- The comparison to equities, commodities, futures, options, and insurance should be softened. These instruments have their own Islamic finance debates and cannot be used as blanket validation.
- The phrase "not gambling by default" is risky because prediction markets may be treated as gambling by some scholars depending on market category and user behavior. Prefer "not necessarily gambling by design" or "can be designed to reduce gambling-like characteristics."
- "Sharia-compliant prediction market" should usually become "Sharia-aligned design candidate" or "candidate design for Sharia review" unless there is a formal approval.
- Sports markets are especially risky and should remain excluded in any Sharia-focused product.
- Leverage should remain excluded from the Sharia-focused design unless a separate scholar-reviewed structure is developed.

