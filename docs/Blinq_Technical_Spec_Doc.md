# **Blinq Technical Spec Doc**

## **Overview**

This document explains the proposed architecture for building a prediction market CLOB natively on Midnight.

Primary Approach

**Matching is a speed problem,**

**Settlement is a correctness problem,**

**Privacy is an identity/state problem.**

Trying to solve all three in the same place will make the system slow and complicated. So the design addresses these concerns separately.

The exchange works as a hybrid system:

* Off-chain matching engine handles orderbooks and trade matching.  
* Midnight contracts handle balances, positions, settlement, resolution, and redemption.  
* User balances, positions, and trade-level details remain private.  
* Public data is limited to what is required for market discovery, pricing, accounting, and verification.

This gives us the performance of a normal CLOB and the privacy/correctness guarantees of Midnight.

---

## **1\. Privacy Model**

This is decided first, being privacy native drives Blinq’s entire design 

### **What remains public**

| Information | Reason |
| ----- | ----- |
| Market question and existence | Users need to discover and trade markets |
| Outcome token supply per outcome | Required for redemption and accounting |
| Aggregate orderbook depth | Traders need market data |
| Settlement event hashes | Proof that settlement happened |
| Oracle resolution result | Outcome must be publicly verifiable |
| Total fees collected | Required for exchange-level accounting |

### **What remains private**

| Information | Reason |
| ----- | ----- |
| User collateral balance | Core privacy requirement |
| User outcome token positions | Users should not reveal market views |
| Order identity and fill size | Prevents strategy leakage and front-running |
| Counterparty relationship | Public should not know who traded with whom |

### **Selective disclosure**

Selective disclosure is important for compliance and audits.

A user should be able to:

* Prove their position to a compliance party.  
* Prove they hold winning positions during redemption.  
* Reveal trade details to a regulator or auditor only with consent.

This is where Midnight is actually useful compared to a normal EVM-based exchange. The design should not leak user-level trading state by mistake.

---

## **2\. Core Data Model**

## **2.1 Markets**

A market is a question about a future binary outcome.

Each market has two outcome tokens:

* YES  
* NO

Market {  
    market\_id:         Bytes32,        // deterministic hash of question parameters  
    question\_text:     String,         // public and verifiable  
    resolution\_time:   UnixSeconds,    // earliest time oracle can resolve  
    oracle\_key:        MidnightPubKey, // trusted oracle key  
    lifecycle:         LifecycleState, // Active | Paused | Flagged | Resolved  
    tick\_size:         u64,            // minimum price increment, scaled 1e18  
    lot\_size:          u64,            // minimum quantity increment  
    min\_order\_size:    u64,  
    yes\_token\_id:      TokenId,  
    no\_token\_id:       TokenId,  
    fee\_policy\_id:     Bytes32,  
}

The `market_id` should be deterministic. This allows off-chain systems to compute the market ID even before the market is registered on-chain.

That is useful for indexing, routing, API references, and order generation.

---

## **2.2 Outcome Tokens**

YES and NO are Midnight-native shielded tokens.

They are not ERC-1155 tokens and should not be designed like EVM assets.

The main invariant is:

1 collateral \= 1 YES \+ 1 NO

A user can:

* Lock collateral and mint YES \+ NO.  
* Burn YES \+ NO and get collateral back.  
* After resolution, redeem only the winning side.

After resolution:

Winning token \= 1 collateral  
Losing token  \= 0 collateral

The exchange contract enforces this invariant.

Amounts are denominated in the smallest collateral unit. For example, if the collateral is USDC-like, then amounts use 6 decimals.

---

## **2.3 Orders**

An order represents a user’s signed intent to trade a specific outcome token at a specific price.

Order {  
    salt:           u64,              // randomness to avoid duplicate/replay issues  
    maker:          MidnightPubKey,   // user who authorized the order  
    token\_id:       TokenId,          // YES or NO token  
    maker\_amount:   u64,              // collateral or token amount depending on side  
    taker\_amount:   u64,  
    price:          u64,              // scaled 1e18  
    side:           Side,             // Buy | Sell  
    expiration:     UnixSeconds,      // 0 means no expiry  
    nonce:          u64,              // replay protection  
    fee\_rate\_bps:   u16,              // max fee user agrees to  
    authorization:  Authorization,    // Midnight authorization proof  
}

Prices are represented as probability values between `0` and `1e18`.

Example:

0.3e18 \= 30 cents for YES  
0.7e18 \= 70 cents for YES

This is the usual binary prediction market pricing model, but here we define the scaling explicitly.

### **Authorization**

This is not an ECDSA signature like EVM.

On Midnight, authorization should be treated as a proof that the private key corresponding to `maker` authorized this exact order.

The API can do a fast pre-check before accepting the order, but the contract is still the final authority during settlement.

---

## **2.4 Collateral**

Collateral is a Midnight-native asset.

The exchange contract tracks collateral using shielded cells.

Users:

* Deposit collateral before trading.  
* Trade using private balances.  
* Withdraw collateral after trading or redemption.

The contract should be collateral-agnostic.

For Phase 1, DUST can be used for testing. For production, a Midnight-native stablecoin is the proper collateral choice, once available.

---

# **3\. Contract Architecture**

There are three main contracts:

BlinqOracle ──resolution──\> BlinqExchange \<──fee routing── BlinqFeeModule

The exchange is the core contract. Oracle and fee handling are supporting modules.

---

## **3.1 BlinqExchange**

This is the main contract, written in Compact.

It owns all critical private state.

### **Public state**

* Market registry  
* Public market metadata  
* YES/NO total supply per market  
* Fee accumulator per market

### **Private state**

* User collateral balances  
* User outcome token positions  
* Filled order tracking  
* Private settlement/accounting state

### **Core circuits**

circuit deposit(collateral\_amount: Uint) {  
    // user transfers collateral into exchange  
    // exchange updates user's shielded balance  
}  
circuit matchOrders(  
    taker: Order,  
    makers: List\<Order\>,  
    taker\_fill\_amount: Uint,  
    maker\_fill\_amounts: List\<Uint\>  
) {  
    // verify order authorizations  
    // verify operator authorization  
    // verify fill amounts  
    // verify prices cross  
    // move collateral and tokens between shielded cells  
    // deduct fees  
}  
circuit mintOutcomeTokens(market\_id: Bytes32, collateral\_amount: Uint) {  
    // lock collateral  
    // mint YES \+ NO  
}  
circuit mergeOutcomeTokens(market\_id: Bytes32, token\_amount: Uint) {  
    // burn YES \+ NO  
    // release collateral  
}  
circuit resolve(market\_id: Bytes32, winning\_side: Side, oracle\_proof: OracleAttestation) {  
    // verify oracle attestation  
    // check resolution time  
    // mark market as resolved  
}  
circuit redeem(market\_id: Bytes32, token\_id: TokenId, amount: Uint) {  
    // burn winning tokens  
    // release collateral  
}  
circuit withdraw(collateral\_amount: Uint) {  
    // withdraw from shielded balance to user's wallet  
}

The important point:

**Users do not directly settle their own trades.**

The settlement worker submits matched trades to the contract. Users only authorize orders. The operator executes them.

This is normal for a CLOB system.

Security comes from contract checks:

* Operator cannot exceed signed amounts.  
* Operator cannot change price beyond user authorization.  
* Operator cannot move funds to arbitrary accounts.  
* Contract validates every order before settlement.

---

## **3.2 BlinqOracle**

The oracle contract handles market resolution.

A fully centralized oracle is risky. A fully consensus-based oracle is slow. So the suggested design is an optimistic resolution with a dispute window.

### **State machine**

INITIALIZED → proposeResolution() → PROPOSED

PROPOSED → dispute() → DISPUTED  
PROPOSED → finalize() → FINAL

DISPUTED → repropose() → PROPOSED  
DISPUTED → emergencyResolve() → FINAL

### **Parameters**

| Parameter | Purpose |
| ----- | ----- |
| `challenge_window` | Time during which resolution can be disputed |
| `repropose_window` | Time given to oracle after dispute |
| `dispute_bond` | Prevents spam/grief disputes |

Minimum window can be 1 hour for early versions, but production values should depend on market size and risk.

### **Resolution payload**

ResolutionPayload {  
    question\_id:       Bytes32,  
    winning\_side:      Side,  
    observation\_time:  UnixSeconds,  
    observation\_proof: Bytes32,  
    oracle\_sig:        OracleSig,  
}

Once final, the oracle calls `BlinqExchange.resolve()`.

The exchange verifies:

* Oracle signature  
* Registered oracle key  
* Resolution time  
* Market state

---

## **3.3 BlinqFeeModule**

The fee module is a thin contract sitting around settlement.

It should not complicate the core exchange contract.

circuit matchOrdersWithFees(  
    taker: Order,  
    makers: List\<Order\>,  
    taker\_fill\_amount: Uint,  
    maker\_fill\_amounts: List\<Uint\>,  
    taker\_fee\_amount: Uint,  
    maker\_fee\_amounts: List\<Uint\>  
) {  
    // call exchange settlement  
    // collect gross fees  
    // refund if needed  
    // retain platform fee  
}

A market can either:

* Use direct `BlinqExchange.matchOrders`, or  
* Use `BlinqFeeModule.matchOrdersWithFees`

For Phase 1, no fee module is needed. Add it only after the core flow works.

---

# **4\. Off-Chain Services Architecture**

The off-chain services handle everything that needs speed.

This is the right model for a prediction market CLOB.

User  
  ↓  
order-api  
  ↓  
rs-engine  
  ↓  
settlement-worker  
  ↓  
Midnight contracts  
  ↓  
indexer  
  ↓  
query-api / frontend

Kafka is used for internal coordination.

---

## **4.1 Order API**

The Order API accepts signed orders from users.

Responsibilities:

* Validate order format  
* Check market config  
* Verify authorization pre-flight  
* Verify balance proof  
* Assign deterministic order ID  
* Publish accepted orders to Kafka

The API should not blindly accept orders and let them fail during settlement. That will pollute the engine and create operational problems.

So the user submits a balance proof along with the order.

The API verifies that the user has enough balance, without seeing the actual balance.

This is more expensive than an EVM `eth_call`, but that is the cost of privacy.

### **Session authentication**

API authentication is separate from order authorization.

Users can authenticate to the REST API using HMAC API keys or session tokens.

This is only for API-level access. It does not authorize trading. Trading is authorized by the Midnight order proof.

---

## **4.2 Matching Engine**

The matching engine should be simple and deterministic.

Its job:

* Consume valid commands  
* Maintain in-memory orderbooks  
* Match orders  
* Emit settlement payloads

It should not read chain state directly.

### **Sharding**

Markets are partitioned by:

hash(market\_id) mod N

Each shard is single-threaded.

This gives us deterministic matching without complicated locking.

### **Orderbook rules**

* Bids: highest price first, then earliest order  
* Asks: lowest price first, then earliest order

This is standard price-time priority.

### **Binary market matching**

For binary markets:

BUY YES at 0.7

is economically similar to:

SELL NO at 0.3

So the engine can support reciprocal liquidity.

This is useful because it improves liquidity without requiring users to manually think in both YES and NO books.

### **Supported order types**

| Type | Meaning |
| ----- | ----- |
| GTC | Rest until filled or cancelled |
| GTD | Rest until expiry |
| FAK | Fill immediately, cancel remaining |
| FOK | Fill fully immediately or reject |

### **Self-trade prevention**

If maker and taker are the same user, the engine should skip the match.

This avoids fake volume and accidental self-trading.

---

## **4.3 Settlement Worker**

This is the most critical off-chain service.

It takes matched trades and submits them to Midnight.

It is also the only service holding the operator private key.

### **Required properties**

The settlement worker must use an outbox pattern.

Before submitting a transaction, it writes the settlement job to its own DB.

This is mandatory. Without this, restarts and network errors will create messy settlement failures.

### **Submission states**

Pending → Submitted(tx\_id) → Confirmed

Pending → TransientFailure → Retry

Submitted → Reverted → DeadLetter

Submitted → Unknown → Query chain before doing anything

The `Unknown` state is dangerous.

A timeout after transaction submission does not mean the transaction failed. It may already be included.

So the worker must check the transaction hash before retrying.

Blind retries can cause duplicate settlement attempts.

The contract should also reject duplicates using deterministic `job_id`.

---

## **4.4 Control Processor**

The control processor converts admin/oracle events into engine commands.

Example:

* Oracle finalizes market  
* Indexer observes event  
* Control processor emits `MarketUpdate`  
* Engine marks market as resolved  
* Resting orders are cancelled

This keeps the engine clean. It does not need to understand oracle logic directly.

---

## **4.5 Query API**

The Query API serves data to frontend and users.

It should read from:

* Postgres  
* Engine snapshots  
* Indexed chain data

It should not directly query the Midnight node for normal requests.

### **Data served**

* Market list  
* Market details  
* Aggregate orderbook  
* Last traded price  
* 24h volume  
* User order history  
* User fill history  
* Resolution status

For private user data, the user must prove identity/ownership.

Do not expose user-level fills publicly.

---

## **4.6 Midnight Indexer**

The indexer listens to Midnight contract events and writes normalized data into Postgres.

Events from `BlinqExchange`:

* `MarketCreated`  
* `SettlementExecuted`  
* `MarketResolved`

Events from `BlinqOracle`:

* `ResolutionProposed`  
* `ResolutionDisputed`  
* `ResolutionFinalized`  
* `EmergencyResolved`

Settlement events should not contain private fill details.

They should only prove that a settlement batch happened.

User-level fill history should be returned only after user authentication/proof.

---

# **5\. Kafka Topic Design**

Kafka is used for internal coordination.

| Topic | Producer | Consumer |
| ----- | ----- | ----- |
| `commands.raw.v1` | order-api, control-processor | rs-engine |
| `settlement.payloads.v1` | rs-engine | settlement-worker |
| `orderbooks.v1` | rs-engine | query-api / ws-gateway |
| `market-configs.v1` | control-processor / engine | query-api |
| `market-fee-policies.v1` | market-control | order-api, settlement-worker |
| `bootstrap.markets.v1` | control-processor | order-api |
| `ingress.control-events.v1` | market-control | control-processor |
| `settlement.results.v1` | settlement-worker | query-api / indexer |

### **Partitioning**

`commands.raw.v1` should be partitioned by `market_id`.

This ensures all commands for one market go to the same engine shard in order.

### **Schema versioning**

Every message should carry:

schema\_version: u16

Adding fields should be backward compatible.

Removing or renaming fields needs a version bump and migration plan.

---

# **6\. Order Authorization Design**

This is where Midnight differs from EVM.

In EVM:

Order → EIP-712 hash → ECDSA signature → recover address

In Midnight:

Order → authorization proof → contract verifies proof

The user proves:

* They know the private key for `maker`  
* They authorized this exact order  
* The order was not modified

The API can do lightweight verification before accepting the order.

But final verification happens inside the exchange contract during settlement.

### **Balance proof**

The user also provides a proof that their shielded balance is sufficient.

The API verifies this before sending the order to the engine.

The proof should be valid only for a short block range. Otherwise, stale balance proofs can create issues.

### **Order ID**

Order ID is derived from the full order struct including salt.

order\_id \= hash(order)

The salt makes the ID unique and prevents simple replay/guessing.

### **Nonce**

Each user should have a per-market nonce.

Orders with old nonces are rejected.

This is useful for cancellation and replay protection.

---

# **7\. Market Lifecycle**

Draft → Active → Resolved  
          │  
          ├── Paused  
          │  
          └── Flagged

### **Active**

Normal trading is allowed.

Users can place orders, engine can match, settlement can continue.

### **Paused**

New order placement is blocked.

Resting orders are preserved.

Already matched settlements should continue.

### **Flagged**

Same as paused from engine point of view.

Used when oracle resolution is under dispute or market needs review.

### **Resolved**

Market has final outcome.

Engine cancels resting orders.

Users can redeem winning tokens.

---

# **8\. Fee Model**

Each market has a fee policy.

FeePolicy {  
    market\_id:               Bytes32,  
    maker\_fee\_bps:           u16,  
    taker\_fee\_bps:           u16,  
    order\_fee\_envelope\_bps:  u16,  
    effective\_at:            UnixSeconds,  
    fee\_policy\_version:      u64,  
}

### **Fee envelope**

The fee envelope is the maximum fee the user agrees to when signing an order.

Example:

User signs max fee \= 100 bps  
Actual fee charged \= 30 bps  
Refund \= 70 bps difference

This allows fee changes without invalidating all outstanding orders, as long as the actual fee does not exceed the signed envelope.

### **Fee validation**

The fee module verifies that:

fee\_amount \<= signed\_fee\_envelope

If not, settlement should fail.

---

# **9\. Settlement Flow**

This is the most important reliability path.

A matched trade that does not settle is the worst case.

## **Step 1: Engine emits settlement payload**

struct SettlementPayload {  
    job\_id:               Uuid,  
    market\_id:            MarketId,  
    fee\_module\_address:   Option\<ContractId\>,  
    taker\_order:          Order,  
    maker\_orders:         Vec\<Order\>,  
    taker\_fill\_amount:    u64,  
    maker\_fill\_amounts:   Vec\<u64\>,  
    taker\_fee\_amount:     u64,  
    maker\_fee\_amounts:    Vec\<u64\>,  
}

`job_id` should be deterministic.

Example:

job\_id \= hash(taker\_order\_id, sorted\_maker\_order\_ids, fill\_amounts)

This helps with deduplication during recovery.

---

## **Step 2: Worker persists and submits**

The settlement worker:

1. Reads payload from Kafka.  
2. Writes job to outbox DB.  
3. Submits transaction to Midnight.  
4. Tracks confirmation.  
5. Retries only when safe.

---

## **Step 3: Contract execution**

The exchange contract:

* Verifies authorization proofs  
* Checks fill amounts  
* Checks price crossing  
* Moves shielded balances  
* Collects fees  
* Emits settlement event

---

## **Step 4: Indexer confirms**

The contract emits:

SettlementExecuted(market\_id, job\_id, block)

The indexer sees this and updates Postgres.

The settlement worker marks the job as done.

---

# **10\. Security Boundaries**

| Risk | Protection |
| ----- | ----- |
| User trades without funds | Balance proof before order acceptance |
| Operator steals funds | Contract only allows signed trade movement |
| Operator overfills order | Contract checks fill amount against signed limits |
| Order replay | Nonce \+ salt |
| Wrong oracle resolution | Oracle key verification |
| Premature resolution | Challenge window |
| Fake disputes | Dispute bond |
| Negative balance | Circuit constraints |
| Excess fee | Fee envelope check |

The operator is trusted for liveness, not custody.

This distinction is important.

If the operator goes down, trading stops.

But the operator should not be able to steal user funds.

---

# **11\. Phased Build Plan**

## **Phase 1: Core contract and single trade flow**

Goal:

Deposit → Place order → Match → Settle → Withdraw

Scope:

* `BlinqExchange.compact`  
* One hardcoded market  
* No oracle  
* No fee module  
* Basic settlement worker  
* Manual order submission  
* Engine emits settlement payload

Success criterion:

One trade settles successfully on Midnight devnet.

---

## **Phase 2: Full trading loop**

Goal:

A usable trading flow with signed orders and market data.

Scope:

* Order API  
* Authorization pre-flight  
* Balance proof validation  
* WebSocket orderbook  
* Query API  
* Settlement retry and DLQ handling

Main benchmark:

How much time does proof generation take per matchOrders call?

This will decide whether batching is needed from day one.

---

## **Phase 3: Oracle and resolution**

Goal:

Markets can be created, resolved, and redeemed.

Scope:

* `BlinqOracle.compact`  
* Dispute window  
* Oracle event indexing  
* Control processor lifecycle updates  
* Resting order cancellation  
* Winning token redemption

---

## **Phase 4: Fee module and production readiness**

Goal:

Add fee collection and operational hardening.

Scope:

* `BlinqFeeModule.compact`  
* Fee policy Kafka snapshots  
* Maker/taker fee routing  
* Reconciliation tooling  
* Monitoring  
* Runbooks  
* Load testing

---

## **Phase 5: Privacy and audit tooling**

Goal:

Make selective disclosure production-grade.

Scope:

* User position proof API  
* Trade disclosure flow with user consent  
* Audit tooling  
* Compact circuit security review  
* Neg-risk market support, if needed

---

# **12\. Key Design Decisions**

## **Operator submits trades, not users**

Users sign orders. The operator submits matched trades.

This reduces on-chain transactions and keeps the CLOB fast.

Trade-off:

The operator is trusted for execution.

Mitigation:

The contract enforces signed limits, price checks, fill limits, and fee limits.

The operator cannot move funds arbitrarily.

---

## **Balance proof is checked before matching**

The Order API requires a balance proof before sending the order to the engine.

This avoids invalid orders entering the book.

Trade-off:

Balance proofs can expire.

For long-lived GTC orders, users may need to refresh proofs or the system needs a revalidation flow.

---

## **Indexer is eventually consistent**

The Query API does not read from the chain directly.

All chain state flows through:

Midnight → Indexer → Postgres → Query API

This adds latency, but keeps the API fast and stable.

For prediction markets, this is acceptable because final confirmation does not need to be millisecond-level.

Orderbook state is still real-time from the engine.

---

## **Sharding is by market**

Each market belongs to one engine shard.

This gives deterministic matching and simple scaling.

Trade-off:

Cross-market operations need separate coordination.

That should be handled outside the core matching engine.

---

## **Settlement is the bottleneck**

Matching, Kafka, and APIs are fast.

The slow part is likely Midnight proof generation and settlement.

So Phase 2 must benchmark:

* Proof generation time  
* Max orders per settlement call  
* Batch settlement throughput  
* Resource/DUST cost per settlement

If settlement is too slow, batching multiple matches into one `matchOrders` call is the practical mitigation.