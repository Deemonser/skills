# Local Quality Checkpoint

Use this checkpoint only for an explicitly requested module-level quality review, technical-debt
check, or small behavior-preserving refactor. Do not turn it into a repository-wide cleanup.

## Anchor and freeze the scope

1. Restate the original requirement, applicable architecture decision or repository invariant, and
   the exact module or diff under review.
2. Freeze feature development. Treat new capability, API redesign, dependency replacement, and
   unrelated cleanup as out of scope.
3. Compare the current implementation with the anchors. Identify concrete drift before judging
   style or proposing a change.

## Review implementation quality

- Verify that names still describe actual responsibility and that behavior lives at the boundary
  owning its invariant.
- Trace inputs, outputs, state changes, and side effects. Flag hidden global state, implicit
  dependencies, duplicate paths, and manual reconstruction of an existing source of truth.
- Check lifecycle-sensitive behavior such as cleanup, cancellation, retry, idempotency, concurrency,
  and partial failure only where the module actually owns it.
- Check that errors are classified and propagated consistently, retain useful context, and are not
  swallowed or converted into misleading success.
- Reject abstractions without present reuse or an owned invariant. Flag pass-through layers,
  speculative extension points, misleading helpers, and test-only seams that distort production
  design.
- Identify stale names, comments, branches, dependencies, and duplicated logic only within the
  reviewed scope. Do not use the checkpoint to justify broad cleanup.
- Ask whether the implementation merely satisfies current tests while violating the intended model.
  Treat tests as evidence, not as the source of product or architecture truth.

## Review performance proportionately

1. Identify a credible hot path, workload, latency or throughput expectation, data scale, and
   resource constraint. Without them, label performance concerns as hypotheses rather than facts.
2. Inspect the relevant path for avoidable allocations or copies, repeated serialization, N+1 or
   redundant I/O, oversized critical sections, lock contention, unbounded buffering, and unsuitable
   algorithmic complexity.
3. Distinguish cold-start cost, steady-state cost, and cache effects. Compare equivalent inputs and
   configurations.
4. Establish a representative baseline before claiming an improvement. Use existing profiling,
   benchmark, tracing, or production metrics where available; propose the smallest measurement when
   evidence is missing.
5. Do not optimize a hypothetical call rate, invent a performance budget, or trade clarity and
   correctness for an unmeasured micro-optimization.

## Choose the remediation

- Leave sound code unchanged when no material problem is found.
- Prefer the smallest behavior-preserving refactor that restores accurate names, one source of
  truth, clear ownership, consistent errors, or a measured performance property.
- Escalate cross-component ownership, lifecycle, state-machine, or contract failures to
  `$review-architecture-first` instead of stacking a local patch.
- Escalate credible trust-boundary or attack-path findings to `$review-reachable-security`.
- For review-only requests, report findings and the minimal refactor plan before editing. When the
  user requests implementation, validate unchanged behavior and any measured property before and
  after the refactor.

## Report

State the reviewed scope and anchors, then report only concrete findings with evidence, impact, and
the smallest remediation. Separate measured performance results from hypotheses. Record checks run,
behavior intentionally preserved, and material uncertainty left unresolved.
