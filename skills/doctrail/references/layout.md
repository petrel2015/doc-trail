# Progressive reading paths

Use the smallest useful structure. Paths below are examples, not mandatory scaffolding.

- README: purpose, audience, minimal verified start, limitations, links by reader intent.
- AI entry: concise project map and routes to relevant capability/decision documents. Reuse README_FOR_AI.md or the existing equivalent; this is project knowledge, not a new agent persona or task handoff log.
- Topic guide: current usage, reference or architectural explanation for one capability, with links to pertinent decisions.
- Decision records: historical context and evidence. A topic index exposes current choices and superseded predecessors without copying their full text.

Keep everyday instructions separate from long historical explanations. Distinguish tutorials, task guides, technical reference and explanation when helpful; do not create empty Diátaxis directories. A bilingual project should keep entry/usage facts equivalent; internal evidence need not be duplicated unless the project requires it.

An index entry should answer: what topic, what is currently chosen, when to read more? For example: “Before changing replay behavior, read the decision explaining why automatic replay was withdrawn.” A generic list of dates is not enough.

Aim for roughly one screen for the first entry, but do not treat line counts as a correctness gate. A direct topic link is preferable to a chain of indexes. Each detailed page needs enough context to stand alone.

Agent-specific files are adapters: point them at the shared project docs and relevant read-before-change guidance. Do not replicate the entire knowledge base into AGENTS.md, CLAUDE.md and other host configuration. A Markdown link alone does not guarantee automatic loading; verify the host's behavior separately.
