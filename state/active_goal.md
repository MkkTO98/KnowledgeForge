# Active Goal

Current active goal: operational state backup, restore, and durability gate is complete at decision gate D.

Result: local operational-state checkpoint creation, validation, isolated restore, protected-state configuration, sensitive exclusions, PostgreSQL reconstruction evidence, and updated validator semantics are implemented and verified. The validated checkpoint is same-host only and must be reported as `tested_local_only = true` and `machine_loss_durable = false`.

Do not stage, unstage, commit, push, delete, reset, clean, checkout, restore, or revert without explicit authorization.

Next required authorization: configure and verify a durability destination outside the host failure domain for operational checkpoints, or separately authorize staging of ordinary-Git durability groups after reviewing the remaining validator blocks.
