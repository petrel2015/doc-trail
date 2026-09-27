# D-0001: Progressive documentation and durable rationale

Lifecycle and topics: [decision index](index.json).

## Context

The project brief requested two capabilities: help new people/agents understand current use, and preserve significant experiments and reversals so later contributors do not unknowingly repeat them. It also requested lightweight entry points, linked detail and initialization of existing repositories with messy or missing docs.

## Decision

Use a short README and skill router, task-oriented links, and separate current guides from decision history. Provide agent-guided initialization and maintenance supported by read-only deterministic tools. Keep dispatch, task state and agent handoff in AgentRelay or another orchestrator. Existing project conventions take precedence over generating a fixed directory tree.

## Alternatives and evidence

Considered a single comprehensive instruction document and a fixed page-count template. Neither was experimentally evaluated in this project; do not describe them as failed trials. The choice is based on the explicit project brief and the documented practices in [research sources](../research.md), not a measured context-cost comparison.

A fully automatic Git-to-rationale generator was considered out of scope: diffs show changes but may omit motives. The helper only supplies bounded metadata; unknown historical reasons remain unknown.

## Consequences

Readers can navigate selectively, but links and topic indexes require maintenance. Interpretation still requires an agent or person. Optional machine-readable relationships improve structural checking but do not verify reasoning.

## Reconsideration

Revisit directory conventions if real migrations reveal repeated navigation failures. Consider automated rationale drafting only with claim-level evidence attribution and evaluation that distinguishes missing reasons from inferred explanations. Any expansion into task execution requires an explicit scope decision.
