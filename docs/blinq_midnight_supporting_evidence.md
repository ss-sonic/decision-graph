# Supporting Evidence: Blinq Midnight Roadmap

## Evidence Policy

This file is supporting context for the document-improvement loop. It may include private repositories, internal paths, and non-public beta surfaces.

Rules for agents:

- Use this evidence to judge whether Blinq capability claims are supportable.
- Do not quote, cite, or expose private repository paths in the revised public document.
- Do not include private URLs or local filesystem paths in the revised public document.
- If a claim is supported only by private evidence, use clean public phrasing such as "available for technical diligence" or "Blinq has built components that can be reviewed during diligence."
- Public beta URLs may be referenced only if the final document is intended for an audience allowed to access them.

## Evidence Items

### E-BLINQ-001: Internal EVM CLOB monorepo

- Type: private_repo
- Locator: `/Users/development/work/blinq/betme/pm-contracts/blinq-clob-monorepo`
- Publicly quotable: no
- Supports:
  - Blinq has a standard EVM-supported CLOB stack available for technical diligence.
  - Blinq has reusable order-book, market, and trading-system components relevant to a Midnight port assessment.
  - Blinq's CLOB capability should not be treated as merely hypothetical if this repository verifies implementation status.
- Suggested public phrasing:
  - "Blinq has an EVM-compatible CLOB stack available for technical diligence."
  - "Blinq's existing CLOB architecture can be evaluated as reusable market/order semantics for a Midnight-specific implementation."
- Diligence questions:
  - Which contracts/components are production-ready, beta, experimental, or test-only?
  - Which chains or environments are supported?
  - Are there deployed contract addresses, audits, or test reports that can be shared privately with Midnight?
  - Which components can be reused conceptually on Midnight, and which must be redesigned in Compact?

### E-BLINQ-002: CTF exchange reference implementation

- Type: private_repo
- Locator: `/Users/development/work/blinq/betme/pm-contracts/ctf-exchange`
- Publicly quotable: no
- Supports:
  - Blinq has access to or has worked with conditional-token / prediction-market exchange architecture relevant to CLOB and market-resolution design.
  - Blinq can provide implementation artifacts for technical review rather than relying only on pitch claims.
- Suggested public phrasing:
  - "Blinq can provide prediction-market exchange implementation artifacts for technical review."
  - "Blinq has implementation experience with prediction-market exchange mechanics that can inform the Midnight design."
- Diligence questions:
  - Is this code forked, original, modified, or used as a reference?
  - What parts are used in Blinq's current stack?
  - What licenses or dependency constraints apply?
  - Does it include conditional-token, oracle, order-matching, settlement, or market-resolution logic relevant to the roadmap?

### E-BLINQ-003: Internal beta application

- Type: internal_beta_url
- Locator: `https://deva.blinq.fi/markets`
- Publicly quotable: no, unless explicitly approved for the target audience
- Supports:
  - Blinq has an internal beta product surface.
  - Blinq's roadmap can refer to a beta-stage product rather than a purely conceptual product, if the beta surface verifies working market flows.
  - Claims about live user traction, deposits, volume, retention, or Polymarket user migration still require metrics; the beta URL alone does not prove traction.
- Suggested public phrasing:
  - "Blinq has an internal beta product surface available for partner diligence."
  - "Blinq's current product should be described as beta-stage unless public launch and traction metrics are available."
- Diligence questions:
  - Which market flows are live in beta?
  - Does the beta include spot markets, leverage, CLOB order placement, settlement, margining, liquidation, or only UI/demo flows?
  - Are there active users, deposits, volume, open interest, retention, or repeat-trader metrics?
  - Is the beta permissioned, testnet, mainnet, or off-chain simulated?

## Recommended Document Treatment

The next revision should upgrade claims only where the private evidence directly supports them:

- It is reasonable to strengthen "Blinq has claimed CLOB components" to "Blinq has an EVM-compatible CLOB stack available for technical diligence" if the monorepo confirms implementation.
- It is reasonable to keep the Midnight port caveat: an EVM CLOB does not directly migrate to Midnight Compact; the reusable part is market/order semantics, architecture, tests, indexing assumptions, and product flow.
- It is not yet reasonable to claim meaningful user migration from Polymarket leverage unless Blinq provides user, deposit, volume, or integration metrics.
- It is not yet reasonable to claim audited, production-ready, or institutionally validated infrastructure unless audits, deployments, or partner diligence artifacts are provided.

