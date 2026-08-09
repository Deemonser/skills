# Commander-Led Delegation

- The primary, higher-capability agent is the commander. It owns system understanding,
  architecture, priorities, cross-module contracts and state machines, core implementation,
  integration, actual diff review, and final acceptance. Delegate independent work to reduce risk
  or wall time; directly complete work cheaper than handoff plus review.
- Classify assignments as read-only reconnaissance, isolated implementation, or core implementation.
  Proactively delegate useful bounded reconnaissance, reproduction, and independent review.
  Uncertainty permits only evidence gathering until the commander reviews it and reclassifies.
- State ownership, lifecycle, cross-module contracts, and semantic changes to protocols,
  persistence, migrations, recovery, concurrency, cancellation, scheduling, continuation, or
  authorization are core; retain their design and key implementation. Delegate implementation only
  for a clear-owner, low-coupling leaf under a fixed interface, with no new state machine or
  cross-module contract, independent validation, and low integration cost. Mechanical changes under
  fixed contracts may qualify.
- For delegated implementation, define the outcome, writable files and interfaces, invariants,
  non-goals, applicable failure, cancellation, recovery, and resource semantics, and acceptance
  checks. The worker must stop before crossing a boundary or changing an invariant. On non-trivial
  work, dispatch qualifying disjoint bundles early once prerequisites and ownership are clear; keep
  one writer per state machine or core file and use redundant workers only when confirmation
  materially reduces risk.
- Worker conclusions and code are candidates. The commander must inspect the actual final diff for
  scope, cross-module consistency, applicable success, failure, cancellation, recovery,
  resource-limit, and fairness paths, then run risk-proportionate final gates. Worker summaries and
  passing tests do not replace code review.
- If review exposes a wrong model of state ownership, lifecycle, or a cross-module contract, stop
  stacking local patches. Rebuild the complete model and then decide whether to repair or rewrite.
