# Supporting Evidence: Blinq Midnight Technical Spec

## Evidence Policy

This file is supporting context for improving `docs/Blinq_Technical_Spec_Doc.md`.

Rules for agents:

- Use this evidence to check technical plausibility and sharpen the architecture.
- Do not quote or expose private repository paths, local filesystem paths, private beta URLs, or private-only implementation details in the revised public spec.
- Use private Blinq implementation evidence to increase confidence in Blinq-owned architecture claims, then phrase public text as "available for technical diligence" or "existing architecture can inform implementation."
- Treat Midnight-specific implementation details as assumptions unless supported by official Midnight documentation or confirmed by the Midnight team.
- Keep useful technical caveats inline as design assumptions or open questions; move private proof reminders to `internal-notes.md`.

## Blinq-Owned Implementation Context

### E-TECH-BLINQ-001: Internal EVM CLOB monorepo

- Type: private_repo
- Locator: `/Users/development/work/blinq/betme/pm-contracts/blinq-clob-monorepo`
- Publicly quotable: no
- Supports:
  - Blinq has an EVM-compatible CLOB implementation context that can inform market models, order models, matching semantics, settlement payloads, and product flow.
  - Blinq can provide implementation artifacts for Midnight technical diligence without exposing repository paths in the public spec.
  - The technical spec can refer to Blinq's existing architecture as reusable design knowledge, not as directly portable Midnight bytecode.
- Suggested public phrasing:
  - "Blinq's existing EVM-compatible CLOB architecture can inform the Midnight implementation's market model, order semantics, matching rules, and service boundaries."
  - "The Midnight implementation should treat EVM components as architectural reference points while rebuilding privacy-sensitive execution paths in Compact."
- Technical review questions:
  - Which CLOB components are pure service logic versus EVM-contract logic?
  - Which invariants and tests can be reused for the Midnight implementation?
  - Which settlement assumptions depend on EVM account/signature semantics?
  - Which pieces must be redesigned around Compact circuits, witnesses, and Midnight authorization?

### E-TECH-BLINQ-002: CTF exchange reference implementation

- Type: private_repo
- Locator: `/Users/development/work/blinq/betme/pm-contracts/ctf-exchange`
- Publicly quotable: no
- Supports:
  - Blinq has prediction-market exchange implementation context relevant to YES/NO markets, conditional-token style accounting, order settlement, and resolution flow.
  - The technical spec's binary-market model and collateral-to-outcome-token invariant can be reviewed against existing prediction-market exchange patterns.
- Suggested public phrasing:
  - "Blinq has prediction-market exchange implementation artifacts available for technical review."
  - "The binary-market accounting model should be validated against Blinq's existing exchange implementation experience and Midnight's asset model."
- Technical review questions:
  - Does the reference implementation use conditional tokens, ERC-1155-like outcome tokens, or a different representation?
  - Which invariants transfer cleanly to Midnight-native assets?
  - Which parts of settlement and redemption must be redesigned for private balances and positions?

### E-TECH-BLINQ-003: Internal beta product surface

- Type: internal_beta_url
- Locator: `https://deva.blinq.fi/markets`
- Publicly quotable: no, unless approved for the target audience
- Supports:
  - Blinq has a product surface for market UX and trading flow review.
  - UI/API assumptions in the technical spec can be evaluated against an internal beta.
  - The beta does not by itself prove production readiness, audits, throughput, or Midnight compatibility.
- Suggested public phrasing:
  - "Blinq has an internal beta product surface available for partner review."
  - "Frontend and API flows can be reviewed against the existing Blinq beta while the Midnight-specific settlement/privacy layer is designed."

## Midnight-Specific Assumptions To Validate

### E-TECH-MIDNIGHT-001: Compact implementation model

- Type: platform_assumption
- Locator: official Midnight / Compact documentation should be attached or cited before finalization
- Publicly quotable: only after replacing this note with official docs
- Supports:
  - The spec should not imply direct EVM bytecode portability.
  - Privacy-sensitive exchange logic must be designed in Compact or whatever Midnight-supported execution model the Midnight team confirms.
- Suggested public phrasing:
  - "Compact-specific circuit design should be validated with the Midnight team before implementation."
  - "EVM architecture can inform the design, but Midnight execution requires a platform-native implementation."
- Technical review questions:
  - What is the correct Compact representation for balances, positions, order authorization, and settlement proofs?
  - Which state can be public ledger state, and which must remain witness/private input?
  - What are the current limits on circuit size, proof generation latency, transaction cost, and composability?

### E-TECH-MIDNIGHT-002: Authorization and identity model

- Type: platform_assumption
- Locator: official Midnight authorization/account documentation should be attached or cited before finalization
- Publicly quotable: only after replacing this note with official docs
- Supports:
  - The spec should distinguish API session authentication from trade authorization.
  - Any claim about "authorization proof" should be validated against Midnight's actual account/key/proof model.
- Suggested public phrasing:
  - "Order authorization should be validated against Midnight's account and authorization model."
  - "The API may pre-check authorizations, but contract-level verification remains the final authority where supported by Midnight."
- Technical review questions:
  - What is the canonical way to authorize private order intent on Midnight?
  - Can authorizations be verified off-chain before matching?
  - How should nonces, expirations, replay protection, and cancellations be represented?

### E-TECH-MIDNIGHT-003: Asset and collateral model

- Type: platform_assumption
- Locator: official Midnight asset/token/collateral documentation should be attached or cited before finalization
- Publicly quotable: only after replacing this note with official docs
- Supports:
  - The spec should avoid assuming ERC-20/ERC-1155 semantics.
  - DUST may be useful for testing, but production collateral depends on available Midnight-native stable assets or bridging strategy.
- Suggested public phrasing:
  - "Phase 1 collateral and outcome-token representation should be validated against Midnight's current asset model."
  - "Production collateral strategy depends on the availability and suitability of a Midnight-native stable asset or approved bridge path."
- Technical review questions:
  - Can outcome tokens be represented as Midnight-native shielded assets, contract state, notes, or another primitive?
  - How should the invariant `1 collateral = 1 YES + 1 NO` be represented and enforced?
  - What collateral is realistic for devnet, testnet, and production?

### E-TECH-MIDNIGHT-004: Events, indexing, and privacy leakage

- Type: platform_assumption
- Locator: official Midnight event/indexing documentation should be attached or cited before finalization
- Publicly quotable: only after replacing this note with official docs
- Supports:
  - Settlement events should prove batch execution without leaking private fill details.
  - Query APIs and indexers must be designed around what Midnight exposes publicly.
- Suggested public phrasing:
  - "Event design should expose only market-level and settlement-proof data required for verification, while keeping user-level fills private."
- Technical review questions:
  - What event/log data is publicly visible on Midnight?
  - Can settlement batch hashes be emitted without leaking order identities or fill sizes?
  - How should users retrieve private fill history?

## Architecture Review Checklist

Use this checklist when improving the technical spec:

- Does the spec clearly separate off-chain matching from on-chain settlement?
- Does it avoid treating Midnight like EVM?
- Does it specify what is public, private, and selectively disclosed?
- Does it define replay protection, cancellation, nonce, expiration, and settlement idempotency?
- Does it include failure modes for settlement worker retries, unknown transaction states, and dead letters?
- Does it avoid leaking private fill details through events, indexers, query APIs, or Kafka topics?
- Does it flag oracle finality, dispute windows, and emergency resolution as design choices requiring Midnight review?
- Does it separate Phase 1 prototype assumptions from production requirements?
- Does it include security review areas: Compact circuits, operator key custody, oracle integrity, settlement batching, liquidation if leverage is added later, and privacy leakage tests?

