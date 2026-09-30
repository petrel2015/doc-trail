# D-0002: Keep the core host-neutral and product adapters optional

Lifecycle and topics: [decision index](index.json). Complements [D-0001](D-0001-scope.md); progressive reading paths and durable history remain the purpose.

## Context and evidence

On 2026-09-30 the user clarified that this third-party skill should be usable by Claude, ZCode, DSH, Hermes and other agents without binding to a product. At revision `1948266`, both usage guides foregrounded a Codex installation path and linked Codex instructions; the core directory included `agents/openai.yaml`. Source inspection establishes this product-centric packaging, not a failed cross-host runtime experiment.

## Decision

Make direct reading and capability-based native registration the general entries. Keep the portable core's SKILL.md, references, assets and helper scripts together. Move product UI metadata to an optional adapter outside that core. Use the Agent Skills format specification as a shared layout reference, while actual host loading is verified separately.

Required acceptance for this refinement: no vendor installation path or special invocation syntax is required by the core; both usage guides explain portable entry and capability requirements; optional product metadata is clearly separated and discoverable; local links and decision relationships pass checks. No helper behavior changes are needed.

## Alternatives and consequences

Keeping Codex as the default install example was rejected after the clarified requirement. Removing its useful metadata completely was also considered; retaining it as an optional adapter preserves the prior presentation while making packaging independent. These were design choices, not tested comparative experiments.

Native discovery, file access and execution vary across hosts. The workflow can be read without Python; scripts require their documented environment. Named target hosts are not automatically qualified integrations. Existing installations that need product metadata can retain it in their installed copies.

## Reconsideration

Add a host adapter when actual loading or UI requirements justify it and evidence is available. Reconsider a common loader only if hosts share a verified interface; any loader must preserve direct-reading access and optional product configuration.
