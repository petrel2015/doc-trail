# Architecture

DocTrail has two modes: retrofit an existing project and maintain affected documentation during development. Both use the same separation of current facts from historical choices.

The short skill entry routes to mode-specific references. Templates support significant records without imposing fixed page counts. A Python standard-library helper handles deterministic inventory, bounded current-HEAD history and local structural checks. It never writes the target project or calls a model. An agent performs source interpretation and documentation edits.

Optional decision JSON is the lifecycle authority for automated checks; Markdown supplies rationale and human navigation. Existing ADR/OpenSpec layouts may be retained without the index, with manual relationship review reported explicitly. A file-target check cannot establish that documentation matches implementation.

Task contracts, dispatch, retry, cost accounting and handoff stay with an orchestrator. See [integration boundaries](../../skills/doctrail/references/integration.md). DocTrail is independently usable and carries no AgentRelay dependency.

Before changing these boundaries, read [D-0001](../decisions/D-0001-scope.md). No automatic model evaluation or semantic verification is implemented.

The portable core is `skills/doctrail/`; host tools supply file access and optional command execution. Product UI metadata lives separately in [adapters](../../adapters/README.md). It cannot change core workflow requirements. Before adding a product dependency, read [D-0002](../decisions/D-0002-host-neutral.md).
