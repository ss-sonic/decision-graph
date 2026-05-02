# External Source Pack: Blinq Sharia Design Proposal

Research date: 2026-04-30

## Purpose

This source pack is for improving `docs/blinq_shariya.md` before external scholar/advisor review.

It does not establish that Blinq is halal or Sharia-compliant. It gives the document better source discipline and a stronger internal map of which claims are supported, contested, or require qualified review.

## How To Use This File In `doc-loop`

Use it as an additional supporting document:

```bash
bin/doc-loop run \
  --doc docs/blinq_shariya.md \
  --supporting-doc docs/blinq_sharia_supporting_evidence.md \
  --supporting-doc docs/blinq_sharia_external_source_pack.md \
  --spec docs/blinq_sharia.docspec.yaml \
  --cycles 1
```

## Source Quality Legend

- `primary_standard`: standard-setter, regulator, official body, or official institutional page.
- `institutional_research`: IMF, World Bank, ISRA/INCEIF, academic journal, or recognized institutional research.
- `academic`: journal, NBER, SSRN, arXiv, university-hosted paper.
- `secondary_explainer`: useful for orientation only; do not rely on it as final authority.
- `regulatory_context`: financial-market regulator or legal/regulatory advisory.

## Source Items

### EXT-SHARIA-001: AAOIFI Sharia Standards

- Type: `primary_standard`
- Locator: https://aaoifi.com/standard/sharia-standards-ar/?lang=en
- Use for:
  - Establishing AAOIFI as a major reference point in Islamic finance.
  - Supporting the need to cite recognized standards rather than making free-form religious claims.
- Source note:
  - AAOIFI standards are a major global reference in Islamic finance and are adopted or used as guidance in multiple jurisdictions.
- How to use in public doc:
  - "Final compliance language should be reviewed against recognized Islamic finance standards such as AAOIFI and relevant jurisdictional Sharia guidance."
- Do not overclaim:
  - Do not say AAOIFI has approved prediction markets unless a specific standard/resolution says so.
  - Do not cite AAOIFI generically for a specific Blinq product conclusion.
- Claim status:
  - Supports: formal source discipline and need for qualified review.
  - Does not prove: permissibility of prediction markets.

### EXT-SHARIA-002: IMF Working Paper on Islamic Derivatives

- Type: `institutional_research`
- Locator: https://www.imf.org/en/publications/wp/issues/2016/12/31/operative-principles-of-islamic-derivatives-towards-a-coherent-theory-25752
- PDF: https://www.imf.org/external/pubs/ft/wp/2012/wp1263.pdf
- Authors: Andreas A. Jobst and Juan Sole
- Use for:
  - Showing derivatives and hedging in Islamic finance are contested.
  - Supporting the distinction between speculative exposure and hedging of actual exposure.
  - Supporting the point that assessments vary by scholar/jurisdiction.
- Source note:
  - The paper says Islamic derivatives face objections around `gharar`, `maisir/maysir`, and `riba`, but also discusses acceptance of hedging actual exposures by many scholars and the costs of lacking Sharia-compliant risk-transfer tools.
- How to use in public doc:
  - "Islamic finance literature treats derivatives and risk-transfer instruments as contested, especially where they introduce excessive uncertainty, speculation, or interest-like economics. The stronger argument is therefore not blanket permissibility, but a constrained design focused on clear terms, actual risk management, and qualified review."
- Do not overclaim:
  - The IMF paper is not a Sharia ruling.
  - It does not approve event contracts or prediction markets.

### EXT-SHARIA-003: ISRA Paper On Islamic Hedging

- Type: `institutional_research`
- Locator: https://www.researchgate.net/publication/333118804_Islamic_Hedging_Rationale_Necessity_and_Challenges_Researcher_International_Shari%27ah_Research_Academy_for_Islamic_Finance_ISRA_2_nd_Floor_Annexe_Block_Menara_Tun_Razak_Jalan_Raja_Laut_50350_Kuala_Lump
- Authors: Asyraf Wajdi Dusuki and Edib Smolo, associated with International Shari'ah Research Academy for Islamic Finance (ISRA)
- Use for:
  - Supporting that Islamic hedging is an active research topic, not a settled blanket approval.
  - Supporting that Islamic finance debates include riba, maysir, gharar, speculation, underlying asset existence, and mutual consent.
- Source note:
  - The paper frames derivative permissibility as ongoing and highlights fiqhi issues around hedging.
- How to use in public doc:
  - "The Sharia question should be framed as a structured review question because Islamic finance scholarship treats hedging and derivative-like instruments as nuanced and contested."
- Do not overclaim:
  - Do not use this paper to say Blinq is compliant.

### EXT-SHARIA-004: IIFM Hedging Standards

- Type: `primary_standard`
- Locator: https://www.iifm.net/public/standards/published-standards/hedging-standards
- Use for:
  - Showing Islamic finance has standardized documentation for some Sharia-compliant hedging products.
  - Supporting the idea that risk-management instruments can be structured, but only under specific frameworks.
- Source note:
  - IIFM describes itself as a global standard-setting body for Shariah-compliant financial contracts and product templates.
- How to use in public doc:
  - "Risk-management use cases should be evaluated against Islamic hedging standards and documentation approaches rather than treated as automatically permissible."
- Do not overclaim:
  - IIFM hedging standards are not prediction-market standards.

### EXT-SHARIA-005: ISDA/IIFM Tahawwut Master Agreement

- Type: `primary_standard`
- Locator: https://www.isda.org/2010/03/01/iifm-and-isda-launch-tahawwut-hedging-master-agreement/
- Use for:
  - Supporting that Islamic finance has developed formal hedging documentation where transactions are structured for Sharia-compliant risk management.
  - Supporting the internal distinction between hedging purpose and speculative purpose.
- Source note:
  - The Tahawwut Master Agreement is a framework for certain Islamic hedging transactions such as profit-rate and currency swaps.
- How to use in public doc:
  - "If Blinq wants to rely on a risk-management argument, it should show actual exposure, clear risk reduction purpose, and structure review, similar in spirit to how Islamic hedging products are documented."
- Do not overclaim:
  - Do not analogize too strongly; event markets differ from OTC hedging products.

### EXT-SHARIA-006: Securities Commission Malaysia Single Stock Futures Resolution

- Type: `primary_standard`
- Locator: https://www.sc.com.my/resources/media/media-release/sc-shariah-advisory-council-accepts-single-stock-futures-as-shariah-compliant-instrument
- Use for:
  - Showing jurisdictional Sharia bodies may approve derivative-like instruments under conditions.
  - Supporting the point that permissibility can depend on structure, underlying asset, clarity, and absence of gambling/uncertainty elements.
- Source note:
  - Malaysia's SC Shariah Advisory Council accepted certain single stock futures where the underlying stocks were Shariah-compliant and the instrument was structured to avoid muqamarah, bai' ma'dum, jahalah, and gharar.
- How to use in public doc:
  - "Some Sharia authorities have accepted derivative-like instruments under strict conditions, which supports a design-review approach rather than a categorical yes/no claim."
- Do not overclaim:
  - This is Malaysia-specific.
  - It does not approve event contracts or prediction markets.
  - It should be treated as evidence that structure and jurisdiction matter.

### EXT-SHARIA-007: World Bank Islamic Finance Overview

- Type: `institutional_research`
- Locator: https://openknowledge.worldbank.org/bitstream/handle/10986/25738/9781464809262.pdf
- Use for:
  - Broad Islamic finance grounding.
  - Avoiding simplistic statements about risk, risk sharing, gharar, maysir, and Islamic financial contracts.
- Source note:
  - Use as a general institutional reference, not as a product-specific ruling.
- How to use in public doc:
  - Cite only if the loop needs broad Islamic finance context; prefer AAOIFI/ISRA/IIFM for specific product review claims.

### EXT-SHARIA-008: Secondary Gharar/Maysir Explainer

- Type: `secondary_explainer`
- Locator: https://abrahamicfinance.com/uncertainty-or-gharar-in-islamic-finance/
- Use for:
  - Orientation on gharar/maysir language and Kamali-style framing.
  - Helping draft plain-English explanations.
- Do not overclaim:
  - Do not rely on this as final authority for Sharia analysis.
  - Replace with primary/recognized sources where possible.

## Prediction Market / Information Market Sources

### EXT-PM-001: CFTC Prediction Markets And Event Contracts Explainer

- Type: `regulatory_context`
- Locator: https://www.cftc.gov/LearnandProtect/PredictionMarkets
- Use for:
  - Supporting the regulated-finance framing that event contracts can be used for hedging or speculation.
  - Supporting requirements for transparent contract terms, payout, settlement determination, customer protections, market integrity, and manipulation controls.
- Source note:
  - CFTC frames event contracts as frequently structured as swaps and notes they can be used to hedge economic risk or to speculate.
  - CFTC also emphasizes transparent rules, contract terms, settlement determination, market manipulation controls, and customer rights.
- How to use in public doc:
  - "Even in regulated financial-market framing, event contracts can serve both hedging and speculative purposes. A Sharia-aligned design must therefore constrain market categories, user protections, and product mechanics toward public-benefit forecasting or actual risk-management use cases."
- Do not overclaim:
  - U.S. regulatory classification is not Sharia approval.

### EXT-PM-002: CFTC Proposed Event Contract Rulemaking

- Type: `regulatory_context`
- Locator: https://www.cftc.gov/PressRoom/PressReleases/8907-24
- Use for:
  - Supporting a strict exclusion list for market categories.
  - Supporting sensitivity around gaming, war, terrorism, assassination, and unlawful activities.
- Source note:
  - In 2024, the CFTC proposed treating event contracts involving enumerated categories such as gaming, war, terrorism, assassination, and unlawful activity as contrary to the public interest.
- How to use in public doc:
  - "The Sharia-focused market policy should categorically exclude harmful, entertainment-only, violence-linked, and manipulation-prone markets. This is aligned not only with Sharia risk controls but also with broader event-contract regulatory concerns."
- Do not overclaim:
  - This is regulatory context, not Sharia authority.
  - Check current legal status before using as final regulatory statement.

### EXT-PM-003: CFTC Enforcement Advisory On Prediction Markets

- Type: `regulatory_context`
- Locator: https://www.cftc.gov/PressRoom/PressReleases/9158-26
- Use for:
  - Supporting market integrity controls around fraud and nonpublic information.
  - Strengthening the document's manipulation/insider-information section.
- Source note:
  - CFTC issued an advisory after enforcement cases involving misuse of nonpublic information and fraud in event contracts.
- How to use in public doc:
  - "Market integrity controls should address manipulation, fraud, nonpublic information, and participants who can influence outcomes."
- Do not overclaim:
  - This does not settle Sharia permissibility.

### EXT-PM-004: NBER - Interpreting Prediction Market Prices As Probabilities

- Type: `academic`
- Locator: https://www.nber.org/papers/w12200
- Authors: Justin Wolfers and Eric Zitzewitz
- Use for:
  - Supporting the information-market thesis with caveats.
  - Replacing absolute "price equals probability" language with "prices can be useful, sometimes biased estimates of trader beliefs."
- Source note:
  - Wolfers and Zitzewitz argue prediction-market prices can often be close to mean beliefs and useful estimates, but not perfectly literal probabilities in all conditions.
- How to use in public doc:
  - "Prediction-market prices can provide useful, sometimes biased estimates of trader beliefs about event probabilities."
- Do not overclaim:
  - Do not state that prices are always accurate probabilities.

### EXT-PM-005: Economic Journal - Calibration Of Prediction Markets

- Type: `academic`
- Locator: https://academic.oup.com/ej/article/123/568/491/5079498
- Authors: Lionel Page and Robert T. Clemen
- Use for:
  - Adding calibration caveats.
  - Supporting that prediction markets can be reasonably calibrated near expiration, while farther-out events may show bias.
- Source note:
  - The abstract reports evidence of favorite/longshot bias and says calibration is better when time to expiration is shorter.
- How to use in public doc:
  - "The public-information argument should be caveated: prediction markets may produce useful forecasts, but calibration varies with liquidity, market design, and time to resolution."
- Do not overclaim:
  - Do not imply all event-market prices are reliable public goods.

### EXT-PM-006: Price Discovery In Prediction Markets

- Type: `academic`
- Locator: https://papers.ssrn.com/sol3/Delivery.cfm/5331995.pdf?abstractid=5331995&mirid=1&type=2
- Use for:
  - Supporting the claim that trading activity can aggregate information and shape price discovery in contemporary platforms.
- Source note:
  - Use as a current working-paper signal; treat as lower authority than peer-reviewed literature.
- How to use in public doc:
  - "Recent market research also studies price discovery and information aggregation in platforms such as Polymarket and Kalshi."

## Claim-To-Source Map

| Document claim | Recommended treatment | Source IDs |
| --- | --- | --- |
| Blinq should not claim final Sharia compliance internally | Strongly supported | EXT-SHARIA-001, EXT-SHARIA-003 |
| Riba/gharar/maysir are core design constraints | Supported, cite recognized sources | EXT-SHARIA-001, EXT-SHARIA-002, EXT-SHARIA-003 |
| Derivative-like instruments are contested in Islamic finance | Supported | EXT-SHARIA-002, EXT-SHARIA-003, EXT-SHARIA-006 |
| Hedging/risk-management purpose can matter | Supported but not decisive | EXT-SHARIA-002, EXT-SHARIA-004, EXT-SHARIA-005, EXT-SHARIA-006 |
| Spot-only, non-levered, fully collateralized design is stronger | Reasonable design inference; needs scholar review | EXT-SHARIA-002, EXT-SHARIA-003 |
| Prediction markets can be information markets | Supported with caveats | EXT-PM-001, EXT-PM-004, EXT-PM-005 |
| Price equals probability | Should be softened | EXT-PM-004, EXT-PM-005 |
| Public-good forecasting claim | Plausible but must be caveated | EXT-PM-001, EXT-PM-004, EXT-PM-005 |
| Market curation should exclude sports/gaming/harmful categories | Strong design recommendation | EXT-PM-002, EXT-PM-003, EXT-SHARIA-003 |
| "All prediction markets are halal" | Must be rejected | EXT-SHARIA-001, EXT-SHARIA-002, EXT-SHARIA-003 |
| "All prediction markets are gambling" | Too broad; replace with design-dependent analysis | EXT-PM-001, EXT-SHARIA-002, EXT-SHARIA-006 |

## Recommended Public Wording Upgrades

Use these as candidate replacements in the Sharia doc.

### Opening Boundary

```md
This document is a design proposal for qualified Sharia review. It is not a fatwa, legal opinion, or final Sharia-compliance claim. Blinq should not publicly describe any product as halal or Sharia-compliant unless qualified scholars have reviewed the actual market categories, contract terms, collateral handling, fee model, oracle process, governance controls, and implemented product mechanics.
```

### Information Market Thesis

```md
Blinq's strongest candidate framing is not "betting made halal." It is an onchain information market for pricing uncertainty, limited to curated market categories where the output can serve public-benefit forecasting or legitimate risk-management use cases. That framing remains a design thesis, not a Sharia ruling.
```

### Price As Probability Caveat

```md
Prediction-market prices can be useful indicators of trader beliefs about event probabilities, but they should not be presented as perfectly accurate probabilities. Academic literature treats the interpretation of market prices as probabilities as conditional on model assumptions, liquidity, time to expiration, trader incentives, and market design.
```

### Riba/Gharar/Maysir Design Standard

```md
The Sharia-focused design should begin with the most conservative product boundary: spot-only markets, no leverage, no lending, no funding rates, no yield on user balances, full collateralization, objective market wording, transparent settlement rules, and curated categories reviewed by qualified advisors.
```

### Market Category Policy

```md
The Sharia-aligned version should not be an open-ended "bet on anything" venue. It should categorically exclude sports betting, random games, celebrity gossip, private-person misfortune, death or assassination markets, war-escalation markets, unlawful events, addictive short-duration markets, and markets where traders can materially influence the outcome.
```

### Hedging/Risk Management Caveat

```md
The risk-management argument is strongest where a participant can identify a real-world exposure and the market reduces uncertainty around that exposure. It is weaker where users participate only for entertainment, short-term thrill, or zero-sum speculation.
```

## Red-Team Objections To Keep

These should stay visible either in the public doc or internal notes:

1. Some scholars may treat binary event contracts as structurally close to `maysir/qimar`, even if the platform frames them as information markets.
2. The fact that a market produces information does not by itself make the trade permissible.
3. Hedging logic is stronger for participants with real exposure; it is weaker for participants with no relation to the event.
4. The zero-sum payout structure may remain a core objection unless scholars accept the information/risk-management function.
5. Forecasting utility is not guaranteed; thin liquidity, manipulation, insider information, market design, and resolution ambiguity can weaken the public-good claim.
6. Elections, politics, crypto, sports, and entertainment-adjacent markets may be especially sensitive and should be reviewed category by category.

## Scholar Review Questions

Use these when approaching advisors:

1. Is a curated, spot-only, fully collateralized event-information market distinguishable from `maysir/qimar`?
2. Does public-benefit forecasting or legitimate risk-management purpose affect the Sharia analysis?
3. Does a binary event contract create unacceptable gharar even if wording, expiry, oracle, payout, settlement, and dispute rules are explicit?
4. Does the platform need to restrict access to users with real-world exposure for the hedging argument to work?
5. Which market categories are acceptable, restricted, or prohibited?
6. Is a platform-level curation/governance process sufficient, or must each market be reviewed individually?
7. Are fees permissible if they are exchange/service fees rather than interest, funding, or yield?
8. What product language may Blinq use before formal approval?
9. What implementation details must be reviewed before any public compliance claim?
10. Would a Sharia board prefer "Sharia-aligned information market candidate" or a different framing?

## Sources To Cite In The Next Run

- AAOIFI Sharia Standards: https://aaoifi.com/standard/sharia-standards-ar/?lang=en
- IMF Working Paper, "Operative Principles of Islamic Derivatives": https://www.imf.org/en/publications/wp/issues/2016/12/31/operative-principles-of-islamic-derivatives-towards-a-coherent-theory-25752
- IMF PDF: https://www.imf.org/external/pubs/ft/wp/2012/wp1263.pdf
- ISRA-linked hedging paper: https://www.researchgate.net/publication/333118804_Islamic_Hedging_Rationale_Necessity_and_Challenges_Researcher_International_Shari%27ah_Research_Academy_for_Islamic_Finance_ISRA_2_nd_Floor_Annexe_Block_Menara_Tun_Razak_Jalan_Raja_Laut_50350_Kuala_Lump
- IIFM Hedging Standards: https://www.iifm.net/public/standards/published-standards/hedging-standards
- ISDA/IIFM Tahawwut launch: https://www.isda.org/2010/03/01/iifm-and-isda-launch-tahawwut-hedging-master-agreement/
- Securities Commission Malaysia SSF ruling: https://www.sc.com.my/resources/media/media-release/sc-shariah-advisory-council-accepts-single-stock-futures-as-shariah-compliant-instrument
- CFTC prediction markets explainer: https://www.cftc.gov/LearnandProtect/PredictionMarkets
- CFTC event-contract rulemaking proposal: https://www.cftc.gov/PressRoom/PressReleases/8907-24
- CFTC prediction-markets enforcement advisory: https://www.cftc.gov/PressRoom/PressReleases/9158-26
- NBER Wolfers/Zitzewitz: https://www.nber.org/papers/w12200
- Economic Journal calibration paper: https://academic.oup.com/ej/article/123/568/491/5079498

