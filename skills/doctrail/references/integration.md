# Integrations and boundaries

## Host tools and skill loading

The core instructions define a workflow and capability requirements, not a specific agent product. Use host-provided file, editing and shell tools when available. Direct reading of the complete skill directory is the baseline; native registration/discovery is a host option and needs its own verification. Preserve project-specific agent entry filenames and governance. Product UI metadata is distributed separately from this directory and is not needed to interpret the core. If required tools or context are missing, report the available scope and gaps rather than inventing execution evidence.

## OpenSpec or another existing specification system

Reuse current specs, design documents and archived changes as sources. Do not create a second behavioral contract. Link significant historical choices from a topic index; add a focused decision only when the rationale, evaluation or lineage is missing. Archive presence alone is not proof of deployment, runtime success or full preservation of abandoned alternatives. Preserve the project's own approval/governance rules.

## AgentRelay or another orchestrator

The orchestrator owns task contracts, handoffs, dispatch, retries, budgets, run/attempt state, fixed-candidate verification and delivery acceptance. DocTrail owns durable project explanation, usage and decision history.

Input: repository path, scoped change or initialization request, candidate revision and available sanitized evidence. Output: changed doc paths, recovered decisions, checks, and unresolved gaps. This is a human/agent workflow contract, not a network API or automatic tool integration.

Update docs within the allowed writable scope. If this changes a frozen candidate, the orchestrator must review the new revision according to its existing process; never silently replace the verified baseline. Raw run ledgers and private conversations remain in orchestrator storage.

DocTrail works without AgentRelay. Missing host installation does not authorize claiming this skill ran: an agent may read the source instructions and report that explicitly, or use the host's verified skill loading mechanism.
