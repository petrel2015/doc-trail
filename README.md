# DocTrail · 文迹

English | [简体中文](README.zh.md)

Progressive project documentation and evidence-backed decision history for people and agents.

Start with a short README. Follow task-specific links. Learn why an apparently better approach was tried, rejected or reverted before repeating it.

## Use it

Ask your agent to read [the DocTrail skill](skills/doctrail/SKILL.md), then request either:

- **Initialize / retrofit:** organize existing docs and recover significant history from code and Git.
- **Maintain:** update affected guides and record important experiments, choices and reversals.

For host installation and example prompts, read [usage](docs/en/usage.md). Helpers require Python 3.10+; Git is needed only for Git metadata/history. No Python packages are required.

## Read next

- [Documentation map](docs/en/index.md) — find usage, design, checks and limitations.
- [AI entry](README_FOR_AI.md) — choose the smallest relevant context.
- [Decision index](docs/decisions/README.md) — understand important choices before replacing them.

Initial implementation: skill workflows plus read-only inventory, history and structural checks. Initialization requires an agent; the script does not generate project facts. Host activation and real-world retrofit quality are not yet qualified. No release is claimed.

Agent dispatch, run state, budgets and handoffs belong to the host orchestrator. DocTrail has no dependency on AgentRelay. This public repository does not yet include an open-source license.
