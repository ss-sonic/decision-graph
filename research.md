# Decision Graph — Research Synthesis

**Date:** 2026-04-13
**Purpose:** Structured research to validate the Decision Graph thesis for users and investors.

---

## Part 1: The Problem Is Real and Quantified

### People decide poorly — and they know it

- **90%** of people regret rushing career choices; **87%** regret hurrying financial decisions
- **82–93%** of homebuyers report purchase regrets
- **60%** of technology buyers regret nearly every purchase (Gartner)
- **85%** of business leaders report "decision distress" — regretting or second-guessing calls (Oracle/Deloitte)

### The cost to organizations is massive

- Fortune 500 companies waste **~530,000 days of manager time annually** on ineffective decisions — equivalent to **$250M/year in wages** (McKinsey)
- **95%** correlation between companies that excel at decision-making and those with top-tier financial results (Bain)
- **72%** of senior executives say bad strategic decisions are as frequent as or more frequent than good ones (McKinsey)
- Insurance underwriters varied **55%** on identical cases; judges' sentences ranged from **1.1 to 15 years** for identical cases (Kahneman, "Noise")

### Decision fatigue is neurologically documented

- Adults make **~35,000 decisions/day** (CNBC)
- Judges' favorable rulings drop from **65% to near 0%** within each session, resetting after breaks (Royal Society)
- Financial analysts' forecast accuracy degrades with each additional forecast in a day

### What people actually do today

- **81%** rely on their own research; **43%** on friends/family; only **31%** on experts (Pew)
- Cross-cultural study (13 languages, 12 countries): people globally default to self-reliant decision-making even when advice would help
- Primary methods: Google, asking friends, gut feeling, pros/cons lists
- Pros/cons lists — the most common "formal" tool — don't weight criteria and are "best suited for simpler decisions"

**Bottom line:** The gap between how people decide (gut + Google + ask a friend) and how they *should* decide (structured, weighted, tracked) is enormous.

---

## Part 2: Why Existing Tools Don't Solve It

### The market is bifurcated

**Enterprise platforms ($100M+ revenue, $1B+ valuations):**
- FICO ($227M platform ARR, Gartner MQ Leader) — credit scoring, fraud
- SAS ($3B+ revenue) — business rules + ML for automated decisions
- o9 Solutions ($157.5M revenue, $3.7B valuation) — supply chain
- Quantexa ($100M+ ARR, $2.6B valuation) — financial crime, risk
- Aera Technology ($97M revenue) — enterprise automation

These automate *operational* decisions. They don't help humans think.

**Consumer/individual tools (tiny, fragmented, no meaningful traction):**
- Rationale (Jina AI) — GPT-4 wrapper for pros/cons/SWOT; $99/month; unclear traction
- Decision Journal App — lightweight outcome tracking; no AI, no graph
- The Decision Log — AI mental models; very early
- Cloverpop — most direct comparable, $12.6M raised, **shrunk to 5 employees** by 2022

**The missing middle:** No well-funded product helps individuals or teams make structured, updateable, contextual decisions that persist over time. This is precisely where Decision Graph sits.

### Adjacent tools that get close but miss

| Tool | What it does well | What it misses |
|------|------------------|----------------|
| Roam/Obsidian/LogSeq | Graph-structured thinking | Not purpose-built for decisions; no typed edges, no confidence tracking |
| Kialo | Structured argumentation | Collaborative debate, not personal reasoning; no temporal evolution |
| Metaculus/Guesstimate | Bayesian updating, probabilistic thinking | Predictions/estimates, not personal decisions |
| Mem0/Personal.ai | AI memory and continuity | Stores raw context, not structured reasoning |
| ADRs (software) | Structured decision records with status | No graph relationships between decisions; software-only |

### Why decision tools fail (the adoption graveyard)

1. **Manual entry kills retention.** 45.6% cite "collection costs" as reason for abandoning tracking tools
2. **Productivity apps lose 83% of users by day 30.** Day-one retention: 17.1%. Day-30: 4.1%
3. **Decision journals fail** because they're all effort and no immediate reward
4. **Status quo bias** — switching from "winging it" is perceived as a potential loss
5. **The timing problem** — people feel the pain of bad decisions *after* the fact, but tools need adoption *before*
6. **Maximizer anxiety** — tools that frame toward "optimal decisions" trigger anxiety rather than reducing it (Schwartz)

**Cloverpop lesson:** Academically sound, behaviorally wrong. Too much process, not enough immediate relief.

---

## Part 3: Why Decision Graph Is Different

### The conceptual gap it fills

No existing product combines:
1. Decisions as first-class graph nodes with structured fields
2. Typed edges modeling real-world decision relationships (dependency, revision, blocking)
3. Confidence tracking with evidence-based updating
4. Review triggers that surface when decisions should be revisited
5. Personal scope (individual reasoning, not team debate or enterprise analytics)

### Intellectual lineage (this isn't invented from nothing)

| Precedent | Contribution | Gap Decision Graph fills |
|-----------|-------------|------------------------|
| IBIS/Compendium (1960s–2000s) | Issues → Positions → Arguments graph notation | Unmaintained, collaborative-only, no confidence/review |
| Kahneman ("Noise", 2021) | Structured decision processes, decision hygiene, noise audits | Academic framework, no product implementation |
| Annie Duke ("Thinking in Bets") | Separate decision quality from outcome quality | Books/workshops, no persistent tool |
| Kozyrkov (Decision Intelligence) | "Turning information into better actions" discipline | Enterprise/organizational focus, no personal tool |
| Discourse Graph (Roam extension) | Typed semantic nodes (questions, claims, evidence) | Academic literature synthesis, not personal decisions |
| Graph of Thoughts (ETH, 2023) | LLM reasoning as arbitrary graph with feedback loops | AI research infrastructure, not consumer product |
| Mem0 (graph-based AI memory) | Graph memory representations with 91% lower latency | Raw context storage, not structured reasoning |

### Why the timing is right (2026)

- Gartner published its **inaugural Magic Quadrant for Decision Intelligence Platforms** (Jan 2026)
- **60%** of executives now regularly use AI to support decisions (Deloitte 2026)
- Decision intelligence market: **$16.34B** (2025) → **$68.2B** (2035), 15.4% CAGR
- AI memory infrastructure is maturing (Mem0, Personal.ai)
- Graph-based AI reasoning is a proven paradigm (GoT, AGoT)
- **33%** of people already use ChatGPT for advice; **49%** of chatbot users say AI influenced a financial decision

---

## Part 4: What the User Research Says About How to Build It

### The trust equation

- People prefer AI advice over human advice in many domains (Logg, Minson, Moore — 6 experiments)
- **But autonomy is the #1 trust driver.** "When consumers feel decision-making agency, they embrace AI-based services" (Syracuse)
- Explainability alone doesn't build trust. Moderate transparency beats over-explanation.
- AI trust is **more volatile** than human trust — one error can shatter it

### What makes decision tools sticky vs. abandoned

**What works:**
- Zero friction to start (no setup, no learning curve)
- Immediate cognitive relief (not "you'll see results in 6 months")
- "Help me think" framing, not "optimize your decisions"
- Compounding value through history (switching cost increases over time)
- Integration into existing workflow

**What kills adoption:**
- Manual data entry
- Framework-first design (requiring users to learn a methodology before getting value)
- Maximizer/perfectionist framing
- Self-improvement positioning (easily abandoned like gym memberships)

### The language that resonates

**Say this:**
- "Help me think through this"
- "What am I missing?"
- "I'm stuck on a decision"
- Relief and clarity framing

**Not this:**
- "Optimize your decision-making"
- "Eliminate cognitive bias"
- "Use our decision framework"
- Rigor and process framing

### The Hook Model for Decision Graph

| Phase | Implementation |
|-------|---------------|
| **Trigger** | Moment of confusion/overwhelm facing a decision (internal trigger) |
| **Action** | Dump messy thoughts into the tool (must be frictionless, natural language) |
| **Variable Reward** | Tool reveals structure, connections, blind spots you didn't see |
| **Investment** | Decision history accumulates, becomes uniquely valuable and hard to leave |

---

## Part 5: Market Sizing

### Direct TAM — Decision Intelligence

| Source | 2025 | 2030–2035 | CAGR |
|--------|------|-----------|------|
| Precedence Research | $16.34B | $68.2B (2035) | 15.4% |
| MarketsandMarkets | $17.41B | $50.1B (2030) | 19.1% |
| Grand View Research | ~$14.6B | $36.3B (2030) | 15.4% |

### Adjacent markets

| Market | Size (2025) |
|--------|------------|
| Knowledge Management Software | $13.7–23.2B |
| Professional Coaching | $5.3–16B |
| Productivity Software | $64–80B |

### Conservative SAM framing

Decision management platforms ($841M) + PKM/second-brain tools (~$2–3B) + AI coaching displacement (~$1–2B) = **~$4–6B serviceable addressable market**, with expansion path into the broader $16B+ decision intelligence market.

---

## Part 6: Risks and Failure Modes

1. **Adoption cliff** — productivity apps lose 83% of users by day 30. Must deliver value in first session.
2. **Cold start** — the graph is empty on day 1. Need a compelling single-decision experience before the graph matters.
3. **Cloverpop precedent** — most direct comparable raised $12M+ and effectively failed. Must study why.
4. **Trust volatility** — one bad recommendation could permanently lose a user.
5. **"Good enough" competition** — ChatGPT + notes may feel adequate. Must demonstrate the compounding value of structured history.
6. **Platform risk** — if memory/continuity becomes a standard AI platform feature, the standalone value proposition weakens.

---

## Sources

### Market & Industry
- McKinsey: Make Faster, Better Decisions
- Bain: Measuring Decision Effectiveness
- Deloitte: Human Capital Trends 2026
- Precedence Research: Decision Intelligence Market
- MarketsandMarkets: Decision Intelligence Market
- Grand View Research: Decision Intelligence Market
- Gartner MQ for Decision Intelligence Platforms (Jan 2026)

### Behavioral Science
- Kahneman: Noise (2021)
- Thaler & Sunstein: Nudge Theory
- Schwartz: Paradox of Choice / Maximizers vs Satisficers
- Annie Duke: Thinking in Bets
- Logg, Minson, Moore: Algorithm Appreciation
- Royal Society Open Science: Decision Fatigue

### User Research & Adoption
- Pew Research Center: Americans and Decision-Making
- University of Pittsburgh: Internal Decision-Making (2025)
- HEC Paris: AI Trust
- Syracuse University: AI and Consumer Autonomy
- Frontiers in AI: Trust in Algorithmic Decision-Making
- PMC: Beyond Abandonment — Life After Personal Informatics
- Nir Eyal: Hooked Model

### Technology & Academic
- IBIS / Compendium (Kunz, Rittel, Conklin, Selvin)
- Dung's Abstract Argumentation Framework (1995)
- Toulmin Model of Argumentation (1958)
- Graph of Thoughts (ETH Zurich, 2023)
- Mem0 Graph Memory (arXiv:2504.19413)
- Roam Discourse Graph Extension (Joel Chan)

### Products
- FICO, SAS, o9 Solutions, Quantexa, Aera Technology
- Cloverpop, Decision Lens, 1000Minds, Lumina/Analytica
- FlexRule, Rationale (Jina AI)
- Metaculus, Guesstimate, Squiggle, Elicit
- Mem0, Limitless/Rewind (acquired by Meta), Personal.ai
- TheBrain, InfraNodus, Kialo
