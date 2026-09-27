# Evidence-backed decision history

Use the [decision template](../assets/decision.md) for important choices, failed experiments and reversals. Preserve the project's existing ADR convention if it already works.

A useful record contains: context and original aim; alternatives and their actual trial stage; observed results and scope; current choice and costs; source evidence; reconsideration conditions. Associate evidence with specific claims. Record commit IDs, relevant paths, PR/test references and version/environment where available. Avoid publishing private source bodies.

Evidence labels:

- **Observed:** inspected diff, reproduced behavior or recorded test result; state scope.
- **Attributed rationale:** a source explicitly states a reason; identify that source.
- **Hypothesis:** plausible interpretation with no direct support; never present it as historical fact.
- **Unknown:** insufficient or contradictory evidence. A useful outcome, not a field to fill creatively.

Use separate dimensions: decision lifecycle (proposed, accepted, rejected, superseded) and experiment stage (considered, tested, deployed). A superseded decision may previously have been accepted; do not relabel it as if it had never been used. A tested approach that was never adopted may be rejected.

Keep old records when a successor replaces them. Stable IDs are never reused. Link successor to predecessor, and let the index show the current lifecycle. Corrections can be appended with evidence; do not erase the old explanation. Reconsideration conditions should be observable, such as a dependency fix plus the old regression scenario passing, not “when AI improves.”

## Optional machine-readable index

For automated relationship checks, adapt or create `docs/decisions/index.json`:

```json
{
  "version": 1,
  "records": [
    {"id": "D-0001", "path": "docs/decisions/D-0001.md", "status": "accepted", "topics": ["retry"], "supersedes": []}
  ]
}
```

Paths are repository-relative, must stay inside the repository and identify distinct Markdown files. IDs and paths are unique. Every supersedes target must exist, have status superseded, and have no replacement cycle. Every superseded record must have a successor. An accepted record is not required to have a predecessor. Multiple unrelated accepted decisions may share a topic.

This index is the lifecycle authority when enabled; prose links to it instead of duplicating status fields. Existing ADR repositories need not adopt JSON: report relationship validation as manual if the index is absent. Topic navigation remains human-readable Markdown. The helper checks structure and relationships, not the truth or sufficiency of evidence.
