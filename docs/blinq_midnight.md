# Blinq × Midnight Roadmap

## Launching a Privacy-Enabled Prediction Market on Midnight

## 1. Why Privacy Matters

Prediction markets are not just financial markets. They are belief markets.

Today, most prediction market activity is public by default. A user's wallet, positions, sizing, entry/exit history, and strategy can often be traced publicly. This is a real barrier for serious traders, larger wallets, and users trading sensitive markets.

Public-by-default trading creates concrete risks for prediction-market users:

* visible positions can expose conviction, sizing, timing, and strategy
* visible wallets make large traders easy to monitor, copy, or counter-position against
* public order flow can contribute to manipulation and suspicious-volume dynamics in thinner markets
* traceable positions can connect market activity to real-world identity, creating legal, reputational, and personal-safety exposure

Users may be comfortable trading an event, but not comfortable broadcasting:

* what they believe
* how much they are sizing
* when they enter or exit
* how they are positioned across related markets
* which political, macro, sports, crypto, or cultural outcomes they care about

This is why privacy is not cosmetic for prediction markets. It is a core product unlock.

To meet this demand and address user concerns, Blinq is building a prediction market platform with a privacy layer.

## 2. Synergies

**Midnight can position privacy-enabled prediction markets as a natural consumer-facing use case for programmable privacy, with Blinq as a concrete partner application to explore that thesis.**

Blinq has an EVM-compatible CLOB and prediction-market derivatives stack available for Midnight technical diligence. Blinq brings reusable market, order-book, margining, and trading-system components that can inform a Midnight-native implementation, including:

* EVM-compatible CLOB architecture and market/order semantics
* prediction-market exchange implementation experience
* margining, liquidation, indexing, and trading-flow components for technical review
* an internal beta product surface that can be reviewed during partner diligence

Midnight brings:

* privacy-first infrastructure
* a strong base layer for protected user activity
* a differentiated launch narrative for consumer-facing private markets
* cross-chain composability

Together, Blinq and Midnight can define a differentiated category: **privacy-first prediction markets**.

## 3. Roadmap

### Phase 1: Build Blinq's Privacy-Enabled Spot Prediction Market on Midnight

Blinq aims to use its existing EVM-compatible spot prediction market CLOB as the architecture and product baseline for a Midnight-native implementation.

The Midnight implementation should treat Blinq's existing EVM components as reusable architecture and product logic, while rebuilding privacy-sensitive execution paths in Compact. The goal is to carry forward existing market/order semantics, trading flows, indexing assumptions, and settlement logic into a Midnight-native design:

**"A privacy-enabled prediction market where users can trade without exposing their full position, wallet-level activity, or strategy publicly."**

An achievable V1 product would include:

* carry forward existing market/order semantics and product logic from Blinq's EVM-compatible CLOB, with privacy-sensitive execution paths rebuilt in Compact
* support simple YES/NO prediction markets
* preserve familiar spot market trading flows
* add privacy around user positions
* add privacy around wallet-level market activity
* keep market resolution public and verifiable
* keep market-level price/liquidity public where required
* support selective disclosure where needed
* define clear settlement logic on Midnight

A clear V1 privacy model should distinguish three layers:

* **Public:** market definitions, resolution outcomes, and aggregate price/liquidity data where needed for market integrity
* **Private by default:** user identity, wallet-level market history, position size, entry/exit timing, and cross-market exposure
* **Selectively disclosed:** proofs or records needed for settlement, compliance, partner reporting, or user-controlled account recovery

### Phase 2: Joint Launch With Midnight

The ideal timing would be to align Blinq's private spot prediction market with Midnight's current ecosystem rollout, including the phases focused on stable mainnet dApps and broader developer adoption.

The GTM angle should be: **Blinq is launching a privacy-enabled prediction market on Midnight, designed to make private trading behavior a consumer-facing use case for programmable privacy.**

This gives Midnight a concrete, market-facing application to showcase as its privacy app ecosystem expands.

Marketing communication to focus on:

* joint Midnight × Blinq announcement
* private prediction market launch campaign
* incentivized trading campaign
* creator-led markets
* liquidity incentives
* migration campaign for Blinq's Polymarket-adjacent leverage users

Blinq's Polymarket-adjacent product flows can become a top-of-funnel for the Midnight-native product once it is live, with migration targets set after Blinq and Midnight review beta usage, deposits, volume, and repeat-trader metrics during diligence.

### Phase 3: Launch Privacy-Enabled Leverage on Blinq Prediction Markets

Once the private spot market has enough liquidity, Blinq will launch leverage on top of its own Midnight-native markets.

This is the full-stack version: **private spot prediction markets + private leverage**.

At that point, Blinq is no longer only routing leverage to Polymarket-adjacent flows; it can support leverage on its own private markets as well.

Phase 3 should be scoped jointly with Midnight engineering because private leverage introduces harder design questions than private spot trading. The design target is:

* leverage on selected Blinq markets after spot liquidity is established
* private margin positions with proof-based solvency checks
* market-level risk parameters and position caps that can be enforced without exposing the full user portfolio
* liquidation paths that disclose only the minimum information needed to protect solvency and LPs
* LP / vault participation with aggregate risk visibility and user-level privacy preserved

## 4. How Midnight Wins

This is a strong use case for Midnight because privacy is central to its product and creates a unique entry point to privacy-focused prediction markets through Blinq.

**The Strategic Fit:**

* **Privacy as a Native Feature:** Prediction markets like Polymarket expose user beliefs, sizing, timing, market selection, and strategy. Blinq can use Midnight to make privacy a competitive advantage, allowing users to trade with high conviction without exposing their edge.
* **The High-Intent Use Case:** Blinq can provide a simple, consumer-facing entry point to the Midnight ecosystem, demonstrating how programmable privacy can support higher-conviction trading, selective disclosure, and more sophisticated prediction-market risk products over time.

For Midnight, Blinq can become a flagship application that shows privacy in a simple and consumer-facing way.

**Market Momentum: Opportunity**

1. **Market Growth:** Prediction markets have moved from a niche crypto-native category into a high-volume event-trading market. TRM Labs reported that sector-wide monthly volume exceeded **$20B in January 2026**, up from roughly **$1.2B in early 2025**. Bernstein's April 2026 coverage forecasts approximately **$240B in 2026 volume** and **$1T in annual volume by 2030**; Eilers & Krejcik's December 2025 report independently projects the category could reach **$1T annually by 2030**.
2. **Scaled Venues:** The category now has two scaled reference venues. In March 2026, Kalshi processed approximately **$13.07B in notional volume** and **88.4M transactions**, while Polymarket recorded its first month above **$10B in monthly volume**. Polymarket's on-chain depth has also continued to grow, with TVL crossing roughly **$500M in April 2026** after its CLOB v2 / pUSD migration.
3. **Execution Privacy:** Without execution privacy, prediction-market participants trade in an environment where positions, sizing, timing, and wallet relationships can be monitored. Recent public reporting shows that high-profile Polymarket positions can be linked to identifiable individuals through media investigation, while independent research has flagged suspicious-volume dynamics and profit concentration on public prediction-market rails. For serious traders, that creates a material strategy-leakage and identity-exposure problem that privacy can directly address.

## 5. Partnership Ask

Blinq is asking Midnight to begin a focused technical and GTM exploration for a privacy-enabled prediction market launch on Midnight.

Proposed next steps:

* schedule a 60-90 minute technical diligence session with Midnight engineering to review Blinq's EVM-compatible CLOB, market/order semantics, and the Compact design work needed for a Midnight-native implementation
* align with the Midnight ecosystem team on whether this should enter a grant, launch-partner, or ecosystem-support track
* define a joint V1 scope covering simple YES/NO markets, privacy boundaries, settlement, public market data, and selective disclosure requirements
* agree on a proposed 30/60/90-day plan for technical architecture, prototype milestones, and GTM timing

The immediate ask is a Midnight engineering and ecosystem review session, followed by a shared decision on whether to move into a scoped build plan for a V1 privacy-enabled spot prediction market.
