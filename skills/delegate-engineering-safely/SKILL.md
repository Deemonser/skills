---
name: delegate-engineering-safely
description: "Delegate engineering work while preserving architectural and integration ownership. Use only when subagents or parallel engineering work are explicitly requested or otherwise permitted and will actually be used, including reconnaissance, isolated implementation, or independent verification. Do not trigger for ordinary single-agent coding."
---

# Delegate Engineering Safely

- Keep the primary agent responsible for system understanding, architecture, priorities,
  cross-module contracts, core implementation, integration, final diff review, and acceptance.
  Delegate only when reduced risk or wall time exceeds handoff and review cost.
- Classify assignments as read-only reconnaissance, isolated implementation, or core
  implementation. Under uncertainty, delegate evidence gathering only until the primary agent
  reviews it and fixes the boundary.
- Retain design and key implementation for ownership, lifecycle, state machines, persistence,
  migrations, recovery, concurrency, cancellation, scheduling, continuation, and authorization.
  Delegate code only for low-coupling leaves under fixed interfaces and invariants.
- For writable work, specify the outcome, owned files, interfaces, invariants, non-goals, applicable
  failure and recovery semantics, and acceptance checks. Keep one writer per state machine or core
  file, and require the worker to stop before crossing a boundary.
- Dispatch disjoint, qualified work early once prerequisites are clear. Do not create subagents for
  trivial work, sequential dependencies, or overlapping edits merely to appear parallel.
- Treat worker conclusions and code as candidates. Inspect the actual final diff, reconcile
  cross-module behavior, and run proportionate final checks; summaries and passing worker tests do
  not replace primary review.
- If integration reveals a wrong model of ownership, lifecycle, or contract, stop stacking local
  patches. Rebuild the model before deciding whether to repair or rewrite.
