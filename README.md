# Decision Graph Research Tools

This repo contains two local agent workflows:

- `research-loop`: validates an idea or wedge from a structured campaign spec.
- `doc-loop`: improves a markdown document through evidence-backed revision cycles.

Both workflows are filesystem-based. They write immutable run artifacts and do not require a database, queue, or hosted service.

## Requirements

- Python 3.13+
- `claude` CLI for Claude-backed roles
- `codex` CLI for Codex-backed roles
- Auth configured for the CLIs you use

Recommended shell setup:

```bash
export PYTHONPATH=src
```

Optional engine/runtime config:

```bash
# Heartbeat print interval while an engine is still running.
export RESEARCH_LOOP_HEARTBEAT_SECS=5

# No timeout by default. Set seconds if you want hard timeouts.
export RESEARCH_LOOP_ENGINE_TIMEOUT_SECS=

# Claude search capability. Default is "assume"; use "on" or "off" to lock it.
export RESEARCH_LOOP_CLAUDE_SEARCH_MODE=on

# Codex research search capability. Default is on.
export RESEARCH_LOOP_CODEX_SEARCH_MODE=on

# Test/mock mode only.
export RESEARCH_LOOP_MOCK_ENGINES=1
export RESEARCH_LOOP_MOCK_FILE=/path/to/mock-scenario.json
```

## Which Loop To Use

Use `research-loop` when the question is:

- Is this idea plausible?
- Is this wedge viable?
- Which claim is unsupported?
- What would reject or advance the campaign?
- What evidence is missing before a pilot or investor story?

Use `doc-loop` when the question is:

- Can this document be made clearer, more truthful, and more defensible?
- Which claims need evidence?
- Which claims should be softened or removed?
- Can external research improve the reasoning?
- Can the document be improved without overwriting the original?

Rule of thumb:

- `research-loop` validates the idea.
- `doc-loop` strengthens the document.

## Research Loop

`research-loop` runs a fixed campaign cycle:

1. `researcher`
2. `skeptic`
3. `rebuttal`
4. `judge`

The judge is the only role that updates campaign state. A campaign can become `active`, `promising`, `plausible`, `rejected`, or `stalled`.

### Campaign Files

Campaigns live in `campaigns/`. Example:

```bash
campaigns/founder-focus-decisions.yaml
```

The campaign YAML is the source of truth for:

- idea and wedge
- idea source document
- core claims
- kill criteria
- evidence policy
- required artifacts
- verdict rules
- engine roles
- notes sources

### Basic Commands

Preflight:

```bash
PYTHONPATH=src bin/research-loop preflight
```

Run one cycle:

```bash
PYTHONPATH=src bin/research-loop run \
  --campaign campaigns/founder-focus-decisions.yaml \
  --cycles 1
```

Check state:

```bash
PYTHONPATH=src bin/research-loop status \
  --campaign campaigns/founder-focus-decisions.yaml
```

Generate reports:

```bash
PYTHONPATH=src bin/research-loop report \
  --campaign campaigns/founder-focus-decisions.yaml
```

Reports are written to:

```text
reports/<campaign-slug>/
```

Cycle artifacts are written to:

```text
runs/<campaign-slug>/cycle-XXXX/
```

### Sequential Research Mode

Sequential mode is the original behavior. It uses one researcher artifact.

```bash
PYTHONPATH=src bin/research-loop run \
  --campaign campaigns/founder-focus-decisions.yaml \
  --research-mode sequential \
  --cycles 1
```

Use this when:

- cost should stay low
- the next question is narrow
- you want easier debugging
- you do not need broad desk research

### Planned Multi-Researcher Mode

Planned mode splits desk research across multiple researcher workers and merges the results back into one canonical researcher artifact.

```bash
PYTHONPATH=src bin/research-loop run \
  --campaign campaigns/founder-focus-decisions.yaml \
  --research-mode planned \
  --research-engines claude,codex \
  --research-workers 6 \
  --research-max-topics 6 \
  --cycles 1
```

The default planned topics are:

- decision cadence and workflow reality
- existing tools and workarounds
- switching pressure and willingness to pay
- competitor and adjacent product map
- failure modes and objections
- pilot design and measurable test

Use planned mode when:

- the campaign is still in desk-research mode
- the question can be split across sub-hypotheses
- you want broader source coverage
- you want Claude and Codex to independently inspect different angles

Do not expect planned mode to replace primary research. If the judge says the blocker is interviews, user calls, deployment proof, or expert review, more desk research is usually not the next step.

### Research Loop Flags

```text
--campaign PATH
  Campaign YAML to run. Defaults to campaigns/client-discovery.yaml.

--research-mode sequential|planned
  sequential: one researcher.
  planned: multiple focused researcher workers, then merge.

--research-engines claude,codex
  Comma-separated engines for planned research.
  Defaults to the campaign researcher engine.

--research-workers N
  Maximum parallel researcher workers.

--research-max-topics N
  Maximum desk-research topics to assign.

--cycles N
  Number of cycles to run. The runner stops early if verdict closes.
```

### How To Read Research Outputs

Important files:

```text
runs/<campaign>/cycle-XXXX/cycle.log
runs/<campaign>/cycle-XXXX/researcher/normalized.json
runs/<campaign>/cycle-XXXX/skeptic/normalized.json
runs/<campaign>/cycle-XXXX/rebuttal/normalized.json
runs/<campaign>/cycle-XXXX/judge/normalized.json
```

In planned mode, also read:

```text
runs/<campaign>/cycle-XXXX/research-plan.json
runs/<campaign>/cycle-XXXX/researcher-0001/normalized.json
runs/<campaign>/cycle-XXXX/researcher-0002/normalized.json
runs/<campaign>/cycle-XXXX/research-merge.json
```

Interpretation:

- `supports_claims`: claims with positive evidence.
- `weakens_claims`: claims that took damage.
- `triggered_kill_criteria`: potential reasons to reject.
- `contradictions`: unresolved tensions that must be answered.
- `open_questions`: what still needs evidence.
- `recommended_verdict`: the agent's recommendation.
- `status`: the persisted campaign state after judge/scoring.

If the loop says no claim advanced because primary interviews were not completed, that means the campaign is blocked on human evidence, not another desk-research cycle.

## Doc Loop

`doc-loop` improves a markdown document without overwriting the original.

Each cycle runs:

1. `extractor`: finds claims, weak reasoning, vague sections, and evidence gaps.
2. `researcher`: researches high-impact gaps.
3. `improver`: proposes concrete edits.
4. `skeptic`: approves or rejects proposals.
5. `editor`: applies approved edits into a full revised markdown document.
6. `judge`: decides whether to continue, stop, or block.

### Basic Commands

Run one document improvement cycle:

```bash
PYTHONPATH=src bin/doc-loop run \
  --doc docs/blinq_sharia_review_pack.md \
  --cycles 1
```

Check status:

```bash
PYTHONPATH=src bin/doc-loop status \
  --doc docs/blinq_sharia_review_pack.md
```

Print latest revised document path:

```bash
PYTHONPATH=src bin/doc-loop latest \
  --doc docs/blinq_sharia_review_pack.md
```

Doc runs are written to:

```text
doc-runs/<doc-slug>/cycle-XXXX/
```

The original document is not overwritten.

### Supporting Evidence Documents

Use `--supporting-doc` for private or public supporting markdown files.

```bash
PYTHONPATH=src bin/doc-loop run \
  --doc docs/blinq_sharia_review_pack.md \
  --supporting-doc docs/blinq_sharia_review_pack_supporting_evidence.md \
  --cycles 1
```

You can pass multiple supporting docs:

```bash
PYTHONPATH=src bin/doc-loop run \
  --doc docs/blinq_sharia_review_pack.md \
  --supporting-doc docs/blinq_sharia_review_pack_supporting_evidence.md \
  --supporting-doc docs/blinq_sharia_contract_evidence.md \
  --cycles 1
```

Supporting docs are used as context. If they contain private links, repo paths, or internal details, the loop should use them for confidence and reasoning without leaking them into the public revised document.

### Document Specs

Use `--spec` to define audience, goal, tone, risk posture, forbidden phrases, and constraints.

```bash
PYTHONPATH=src bin/doc-loop run \
  --doc docs/blinq_sharia_review_pack.md \
  --spec docs/blinq_sharia_review_pack.docspec.yaml \
  --supporting-doc docs/blinq_sharia_review_pack_supporting_evidence.md \
  --cycles 1
```

A docspec is useful when:

- the document has a specific audience
- public wording must avoid unsafe claims
- private evidence must not be exposed
- the document has hard constraints
- the output should preserve a specific posture

Common docspec fields:

```yaml
document_type: sharia_review_pack
author: Blinq
audience: Qualified Sharia scholar and Islamic finance advisor
goal: Improve reviewability and evidentiary defensibility
tone: careful, rigorous, non-promotional
risk_posture: highest_caution
private_evidence_policy: use_for_confidence_do_not_quote
diligence_language: inline_for_review_scope
strict_public_pattern_validation: false

forbidden_public_patterns:
  - /Users/
  - deployment address

forbidden_public_assertions:
  - Blinq is Sharia-compliant
  - Blinq is halal

allowed_disclaimer_patterns:
  - This document is not a religious ruling, legal opinion, or final compliance claim.
```

### Sequential Doc Research

Sequential mode uses one researcher.

```bash
PYTHONPATH=src bin/doc-loop run \
  --doc decision-graph.md \
  --research-mode sequential \
  --cycles 1
```

Use this when:

- the document is short
- cost should stay low
- you want simpler artifacts
- the improvement target is narrow

### Planned Multi-Researcher Doc Mode

Planned mode asks the extractor to create research units, assigns them to researcher workers, and merges their evidence before improvement.

```bash
PYTHONPATH=src bin/doc-loop run \
  --doc docs/blinq_sharia_review_pack.md \
  --spec docs/blinq_sharia_review_pack.docspec.yaml \
  --supporting-doc docs/blinq_sharia_review_pack_supporting_evidence.md \
  --research-mode planned \
  --research-engines claude,codex \
  --research-budget standard \
  --research-workers 4 \
  --research-max-units 8 \
  --cycles 1
```

Use planned mode when:

- the document has many claims
- multiple sections need evidence
- you want cross-engine research coverage
- compliance, investor, technical, or reviewer-facing claims need more diligence

### Doc Loop Flags

```text
--doc PATH
  Markdown document to improve. Required.

--supporting-doc PATH
  Markdown evidence/context file. May be repeated.

--spec PATH
  YAML or JSON docspec controlling audience, tone, risk posture, and constraints.

--research-mode sequential|planned
  sequential: one researcher.
  planned: extractor-created research units, multiple workers, merged evidence.

--research-engines claude,codex
  Comma-separated research engines for planned mode.

--research-budget cheap|standard|deep|audit
  Planning profile for number of units, workers, and redundancy.

--research-workers N
  Maximum parallel researcher workers.

--research-max-units N
  Maximum research units selected from extractor output.

--cycles N
  Number of document improvement cycles.
```

### Research Budgets

Use these as operator intent:

- `cheap`: fewer units, lower cost, less redundancy.
- `standard`: balanced default for serious document improvement.
- `deep`: broader coverage and more worker capacity.
- `audit`: highest redundancy, useful for high-risk documents.

### How To Read Doc Outputs

Important files:

```text
doc-runs/<doc>/state.json
doc-runs/<doc>/cycle-XXXX/input.md
doc-runs/<doc>/cycle-XXXX/extractor/normalized.json
doc-runs/<doc>/cycle-XXXX/researcher/normalized.json
doc-runs/<doc>/cycle-XXXX/improver/normalized.json
doc-runs/<doc>/cycle-XXXX/skeptic/normalized.json
doc-runs/<doc>/cycle-XXXX/editor/normalized.json
doc-runs/<doc>/cycle-XXXX/judge/normalized.json
doc-runs/<doc>/cycle-XXXX/revised.md
doc-runs/<doc>/cycle-XXXX/change-log.md
doc-runs/<doc>/cycle-XXXX/internal-notes.md
```

In planned mode, also read:

```text
doc-runs/<doc>/cycle-XXXX/research-plan.json
doc-runs/<doc>/cycle-XXXX/researcher-0001/normalized.json
doc-runs/<doc>/cycle-XXXX/researcher-0002/normalized.json
doc-runs/<doc>/cycle-XXXX/research-merge.json
```

Interpretation:

- `extractor`: what is weak or unsupported in the current document.
- `researcher`: evidence gathered for the highest-impact gaps.
- `improver`: proposed edits.
- `skeptic`: approved and rejected proposals.
- `editor`: full revised markdown.
- `judge`: whether another cycle is useful.
- `revised.md`: the version to inspect or share.
- `internal-notes.md`: private caveats, evidence gaps, and warnings.

Judge verdicts:

- `improved`: useful revision was made.
- `needs_more_research`: another evidence cycle may help.
- `blocked_on_primary_research`: desk research is exhausted; human/expert/product evidence is needed.
- `stable`: remaining changes are not worth another cycle.
- `overclaiming_risk`: the document may be trying to say more than evidence supports.

## Recommended Workflows

### Validate A Wedge

```bash
PYTHONPATH=src bin/research-loop preflight

PYTHONPATH=src bin/research-loop run \
  --campaign campaigns/founder-focus-decisions.yaml \
  --research-mode planned \
  --research-engines claude,codex \
  --research-workers 6 \
  --research-max-topics 6 \
  --cycles 1

PYTHONPATH=src bin/research-loop status \
  --campaign campaigns/founder-focus-decisions.yaml

PYTHONPATH=src bin/research-loop report \
  --campaign campaigns/founder-focus-decisions.yaml
```

If the output says primary discovery is required, stop desk research and run interviews.

### Improve A Reviewer-Facing Document

```bash
PYTHONPATH=src bin/doc-loop run \
  --doc docs/blinq_sharia_review_pack.md \
  --spec docs/blinq_sharia_review_pack.docspec.yaml \
  --supporting-doc docs/blinq_sharia_review_pack_supporting_evidence.md \
  --research-mode planned \
  --research-engines claude,codex \
  --research-budget standard \
  --cycles 1

PYTHONPATH=src bin/doc-loop latest \
  --doc docs/blinq_sharia_review_pack.md
```

Inspect the latest `revised.md`, `change-log.md`, and `internal-notes.md` before running another cycle.

### Improve A Short Blurb

```bash
PYTHONPATH=src bin/doc-loop run \
  --doc docs/ryan_message.md \
  --spec docs/blurb.docspec.yaml \
  --research-mode sequential \
  --cycles 1
```

For blurbs, sequential mode is usually enough. Planned research is overkill unless the message depends on factual claims.

## Practical Guidance

- Run one cycle, inspect outputs, then decide whether another cycle is justified.
- Do not keep running loops after the judge says the next step is primary research.
- Use supporting docs for private proof, but use docspec rules to prevent leaking private details.
- Use planned research for broad desk research, not for editing polish.
- Use sequential mode for narrow or cheap runs.
- Treat `plausible` as "worth piloting", not "validated".
- Treat `promising` as "real signal exists, but key claims remain unresolved".
- Treat `blocked_on_primary_research` as a stop sign for agent-only work.

## Tests

Run the test suite:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

Compile check:

```bash
python3 -m compileall -q src
```

