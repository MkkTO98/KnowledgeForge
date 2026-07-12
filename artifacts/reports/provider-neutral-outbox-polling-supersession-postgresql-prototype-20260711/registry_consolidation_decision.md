# Registry Consolidation Decision

Decision: define `artifacts/release-inbox-unified-v1/seen-release-registry.jsonl` as the production registry authority for future real external releases.

Existing registries are preserved as evidence/fixtures. Real MacroForge manual-handoff history is imported by copying the prior seen-release registry and accepted normalized release into the unified operational state before processing polled releases. No incompatible identities are merged silently.

Classification source: `execution/registry_inventory.json`.
