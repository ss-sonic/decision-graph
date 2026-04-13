# Decision Graph — UX Spec: Messy Input → Structured Decision

## The Core Principle

**The user talks. The AI makes the call. The user interrogates.**

The user never fills in fields. They speak naturally. The AI infers structure, evaluates the options, and tells the user what it would do and why. The user's job is to challenge the reasoning — not to organize their own thinking from scratch.

The product is NOT a mirror. It's an advisor that shows all its work.

People who are stuck on a decision don't want "here are your tradeoffs, good luck." They want: "Do X. Here's why. Here's when I'd change my mind." The user feels in control not because the AI withheld its recommendation, but because the AI's reasoning is fully transparent and challengeable.

---

## The Flow: Five Phases

### Phase 1: The Dump (30 seconds)

**What the user sees:** A single text area (or voice button). Nothing else. No sidebar, no fields, no categories, no onboarding.

**Prompt:** "What are you trying to decide?"

**What the user does:** Types or says whatever's in their head, in whatever form it comes:

> "I got a job offer in Berlin but my partner doesn't want to move and I'm also up for promotion at my current company and I don't know if the money is worth the upheaval"

**Design rules:**
- Zero cognitive load. One input. One action.
- Accept any length — one sentence or five paragraphs
- No account required for first use
- No categorization, no templates, no "what type of decision is this?"

**Why this works:** The product's first job is to be a safe container for messy thinking. Every field, label, or dropdown at this stage is friction that kills adoption. The research shows: 83% of productivity app users churn by day 30. The first screen must feel like relief, not work.

---

### Phase 2: The Mirror (appears in ~3-5 seconds)

**What the user sees:** A Decision Card — a structured reflection of what they just said.

**The card is NOT a form.** It looks like something a great advisor would write on a whiteboard after listening to you for 5 minutes.

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  THE REAL DECISION                              │
│  "Should I take the Berlin offer or stay        │
│   and pursue the promotion?"                    │
│                                                 │
│  WHAT'S PULLING YOU                             │
│  → Berlin: higher pay, fresh start, new market  │
│  → Stay: promotion path, partner's preference,  │
│    stability, existing network                  │
│                                                 │
│  WHAT SEEMS TO MATTER MOST                      │
│  1. Partner's happiness                         │
│  2. Career trajectory (long-term, not just now) │
│  3. Financial improvement                       │
│  4. Desire for change                           │
│                                                 │
│  WHAT I DON'T KNOW YET                          │
│  • Is your partner's "no" firm or a negotiation │
│    starting point?                              │
│  • How real is the promotion — guaranteed or     │
│    possible?                                    │
│  • How big is the salary difference?            │
│                                                 │
│  ┌──────────────┐  ┌────────────────────┐       │
│  │  Feels right  │  │  Something's off   │       │
│  └──────────────┘  └────────────────────┘       │
│                                                 │
└─────────────────────────────────────────────────┘
```

**The two buttons are critical:**

- **"Feels right"** → Moves to Phase 3 (sharpening questions)
- **"Something's off"** → Opens a text input: "What did I miss?" → AI regenerates the card

**This is the therapist moment.** "It sounds like what you're really deciding is... does that feel right?" The user's emotional response — recognition ("yes, exactly") or correction ("no, the real issue is...") — is itself productive. Both paths deepen understanding.

**Design rules:**
- The card appears as an artifact/panel (like Claude Artifacts or ChatGPT Canvas), not as a chat message
- Use natural language, not field labels. "What seems to matter most" not "Decision Criteria"
- Show only 4 sections in the initial mirror. Don't overwhelm.
- The "What I don't know yet" section is the bridge to Phase 3 — it tells the user exactly why the conversation needs to continue

**Why this works:** The user typed a mess and instantly sees clarity. That gap — between what was in their head and what they see on screen — is the product's value. It's cognitive relief delivered in seconds.

---

### Phase 3: The Sharpening (2-5 minutes)

**What the user sees:** Chat continues alongside the Decision Card. As they answer questions, the card updates in real-time.

**The AI asks 2-3 targeted questions.** Never more than 3 before showing an updated card.

**Question design rules:**

Each question must:
1. Reference something the user already said (so it feels like listening, not interrogating)
2. Target a specific gap that would change the outcome
3. Offer concrete anchors, not open-ended exploration

**Good questions:**
- "You said your partner doesn't want to move. Is that a 'never' or a 'not unless something changes'? That distinction changes everything here."
- "If you stay and get the promotion, what does that look like in 2 years? Is it a stepping stone or the destination?"
- "How much more is the Berlin offer? Enough to change your lifestyle, or just a nice bump?"

**Bad questions:**
- "Tell me more about your partner's feelings about Berlin." (too open-ended)
- "What are your career goals?" (too broad, feels like a form)
- "On a scale of 1-10, how important is salary?" (this is a form delivered via chat)

**The card updates live.** After each answer, the user can see fields filling in, options getting more concrete, tradeoffs getting weighted. They watch their decision sharpen in real time.

**After 2-3 rounds (4-8 questions total max),** the system is ready for Phase 4.

---

### Phase 4: The Decision Card (the artifact the user keeps)

After sharpening, the full Decision Card appears. This is what gets stored as a node in the graph.

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  DECISION                                       │
│  "Should I take the Berlin offer or stay        │
│   and pursue the promotion?"                    │
│                                                 │
│  Status: Active          Date: April 13, 2026   │
│                                                 │
│  ─────────────────────────────────────────────── │
│                                                 │
│  CONTEXT                                        │
│  Senior PM at a mid-stage startup. 3 years in.  │
│  Partner is in a stable local role she values.   │
│  Berlin offer is from a larger company,          │
│  30% salary increase, 2-year initial commitment. │
│                                                 │
│  ─────────────────────────────────────────────── │
│                                                 │
│  OPTIONS                                        │
│                                                 │
│  A: Take Berlin                                 │
│     + Higher pay, new market exposure, growth    │
│     − Partner disruption, new network needed,    │
│       2-year lock-in                             │
│                                                 │
│  B: Stay and pursue promotion                   │
│     + Partner stability, existing relationships, │
│       known environment                          │
│     − Promotion not guaranteed, salary stays     │
│       flat, may resent the "what if"             │
│                                                 │
│  C: Negotiate (stay but ask for raise/role)      │
│     + Low risk, tests employer's commitment      │
│     − May not match Berlin offer, doesn't        │
│       address the desire for change              │
│                                                 │
│  ─────────────────────────────────────────────── │
│                                                 │
│  WHAT MATTERS MOST                              │
│  1. Partner's wellbeing .............. high      │
│  2. Long-term career trajectory ...... high      │
│  3. Financial improvement ............ medium    │
│  4. Novelty and growth ............... medium    │
│  5. Short-term stability ............. low       │
│                                                 │
│  ─────────────────────────────────────────────── │
│                                                 │
│  KEY ASSUMPTIONS                                │
│  • Partner's position is firm (no to relocation) │
│  • Promotion is likely but not certain (~60%)    │
│  • Berlin offer open for 2 more weeks            │
│  • Current company won't counter-offer           │
│                                                 │
│  ─────────────────────────────────────────────── │
│                                                 │
│  WHAT I'D DO                                    │
│  Negotiate with your current company first.     │
│                                                 │
│  WHY                                            │
│  Your top priority is your partner's wellbeing, │
│  and right now that blocks Berlin. But the      │
│  Berlin offer proves you're underpaid — use it  │
│  as leverage. Test whether your company values  │
│  you enough to close the gap. If they don't,    │
│  that tells you something important about       │
│  staying.                                       │
│                                                 │
│  THIS DEPENDS ON                                │
│  • Your partner's no being firm                 │
│  • The promotion being real, not a stall        │
│  • Your company being willing to negotiate      │
│                                                 │
│  I'D CHANGE MY MIND IF                          │
│  • Partner opens up to relocating               │
│    → Berlin becomes the answer                  │
│  • Company dismisses the negotiation            │
│    → Leaving becomes clearer                    │
│  • Promotion timeline slips past 6 months       │
│    → Your leverage weakens, act sooner          │
│                                                 │
│  CONFIDENCE: 64%                                │
│  Moderate — one conversation with your partner  │
│  or your manager could push this to 85%+ in     │
│  either direction.                              │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │  Disagree? Tell me which part is wrong.  │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Design rules for the card:**
- Scannable in 30 seconds. Useful to revisit months later.
- Natural language throughout. No field codes, no IDs, no jargon.
- The recommendation is DIRECT. "What I'd do" not "where the logic points." The AI makes the call.
- But the reasoning is TRANSPARENT. Show why, what it depends on, and what would change the answer. User agency comes from seeing the full chain and challenging any link — not from the AI withholding its opinion.
- Confidence is shown as a percentage — honest about uncertainty.
- "I'd change my mind if" is the bridge to the update mechanism (Phase 5).
- "Disagree? Tell me which part is wrong" invites challenge, not blind acceptance.
- Every field on this card was INFERRED from the conversation, not entered by the user.
- The card adapts to the decision type. Not all fields appear every time.

**Confidence calibration — how direct the AI should be:**

| Confidence | Tone | What the AI says |
|-----------|------|-----------------|
| **>75%** | Direct, decisive | "Do X. Here's why." The reasoning is clear, one option dominates, assumptions are strong. |
| **50-75%** | Clear lean, acknowledges tension | "I'd lean toward X. But it's close because of Y. One conversation could tip this." |
| **<50%** | Honest about limits, still useful | "I can't give you a strong call yet. But if you find out [specific thing], the answer becomes clear." |

Even at low confidence, the AI is useful — it tells you exactly what information would unlock the answer. "I don't know" is never the final output. "I don't know, but here's the one thing that would make me sure" is.

---

### Phase 5: The Revisit (days, weeks, or months later)

**Trigger:** User returns and says "something changed." Or the system nudges them based on a review trigger (e.g., "Your Berlin offer deadline is in 3 days").

**What the user does:** Types what changed:

> "My partner said she'd be open to Berlin if it's only for 2 years."

**What the system does:**

1. Pulls up the existing Decision Card
2. Identifies which assumption changed
3. Shows a diff view:

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  SOMETHING CHANGED                              │
│                                                 │
│  ASSUMPTION UPDATED:                            │
│  ✗ "Partner's position is firm (no relocation)" │
│  ✓ "Partner open to Berlin if ≤2 years"         │
│                                                 │
│  ─────────────────────────────────────────────── │
│                                                 │
│  HOW THIS CHANGES THINGS:                       │
│                                                 │
│  • Option A (Berlin) is now viable — was blocked │
│    by partner constraint, now conditional        │
│  • Criteria #1 (partner wellbeing) shifts from   │
│    "blocking Berlin" to "conditional on timeline"│
│  • New consideration: return path after 2 years  │
│                                                 │
│  ─────────────────────────────────────────────── │
│                                                 │
│  UPDATED RECOMMENDATION:                        │
│  Take Berlin (2-year commitment)                │
│  Confidence: 34% → 72%                          │
│                                                 │
│  Because: The main blocker (partner opposition)  │
│  is now conditional. A 2-year stint addresses    │
│  the salary gap, provides growth, and has a      │
│  defined endpoint that respects the constraint.  │
│                                                 │
│  ─────────────────────────────────────────────── │
│                                                 │
│  NEW ASSUMPTIONS:                               │
│  • 2-year timeline is genuine (not bait)         │
│  • Return path to current city/industry exists   │
│  • Partner's conditional yes holds under stress  │
│                                                 │
│  NEW REVISIT TRIGGERS:                          │
│  • If return path is unclear after investigation │
│  • If partner's conditional yes feels pressured  │
│  • At 18-month mark: extend decision or return   │
│                                                 │
└─────────────────────────────────────────────────┘
```

**This is the "Git diff for decisions" moment.** The user doesn't re-explain everything. They say what changed, and the system shows exactly how it ripples through their reasoning.

**This is what ChatGPT cannot do.** In a chat, you'd re-explain the entire context every time. Here, the structure persists, and updates are surgical.

---

## Handling Emotional Decisions

Not every decision is a rational multi-option evaluation. Some are emotionally loaded, ambiguous, or value-driven.

**Detection:** If the user's input contains strong emotional language ("I'm torn," "I feel guilty," "I don't know what I want"), the system should NOT immediately jump to a Decision Card.

**Instead, Phase 2 becomes acknowledgment first:**

> "This sounds like it's weighing on you beyond just the practical question. Before I try to organize the options — what's the feeling that's hardest to sit with right now?"

Then, after 1-2 exchanges that acknowledge the emotional dimension, transition to the card with a gentler frame. The card might lead with "What's really at stake" instead of "Options."

**The system needs different card types:**
- **Multi-option evaluation** (career, hiring, purchasing) — full options + criteria + weights
- **Yes/No with emotional complexity** (quitting, ending a relationship, confrontation) — lighter on options, heavier on values and consequences
- **Timing decision** (when, not what) — focuses on conditions and readiness
- **Value conflict** (two things you care about are in tension) — focuses on priority and acceptance

The 16-field schema from the doc is a MAXIMUM, not a template. Many decisions need only 4-5 sections.

---

## The Layout

**Chat-first with artifact emergence** (like Claude Artifacts / ChatGPT Canvas):

- **Phase 1:** Full-screen chat. Nothing else. Zero cognitive load.
- **Phase 2:** Decision Card slides in as a panel/artifact alongside the chat.
- **Phase 3-4:** Split view — chat continues left, card updates right.
- **Phase 5 (Revisit):** Card is primary, chat is secondary — the user is editing an existing artifact, not starting fresh.

**Mobile:** Card appears as a slide-up sheet or a swipeable tab. Chat is the default view; card is one swipe away.

---

## What You DON'T Need for the Pilot

- A graph (retention hook, not first-session hook)
- Accounts or sign-up
- A recommendation engine (the LLM IS the engine)
- Memory across sessions (test single-session value first)
- Multiple decision types (start with multi-option only)
- Beautiful UI (a clean web page is enough)

## What You DO Need for the Pilot

- A chat interface (even basic)
- An AI backend that takes messy input and returns a structured Decision Card
- The Mirror step (structured reflection)
- The Sharpening step (2-3 follow-up questions that update the card)
- The final card output (can be markdown or a simple styled view)
- One question after the card: "Did this help you think more clearly?" (thumbs up/down)

## The Zero-Code Test (Do This First)

Before building anything:

1. Write a Claude/GPT system prompt that implements the three phases
2. Share it as a Claude Project or custom GPT with 20 people
3. Ask them to bring a real decision they're facing
4. After the session, ask one question: "Did this help you think more clearly about your decision?"
5. If >70% say yes → build the product
6. If <50% say yes → the problem isn't UX, it's deeper

The system prompt should encode:
- Phase 1: Accept messy input without premature structuring
- Phase 2: Reflect back a structured Decision Card (initial mirror)
- Phase 3: Ask max 3 targeted questions, then show the final card
- Phase 4: Make a clear recommendation with full reasoning chain
- The card format from this spec
- The emotional detection rules
- Direct recommendation with confidence calibration
- "Disagree? Tell me which part is wrong" as a standard closing
- "I'd change my mind if" as mandatory section (bridges to revisit flow)

## The Product Pitch (Updated)

Not: "Structure your decisions."
Not: "See your tradeoffs clearly."

**"Tell me what's going on. I'll tell you what I'd do and exactly why — so you can decide if my reasoning holds."**

That's what people actually want when they're stuck. Not a framework. Not a mirror. An answer they can interrogate.
