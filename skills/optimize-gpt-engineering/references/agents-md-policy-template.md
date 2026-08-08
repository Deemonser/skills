# Canonical AGENTS.md Policy Template

Use the following policy block verbatim by default. Translate it, merge equivalent existing rules,
or adjust project nouns and scope only when necessary. Preserve every decision, default, threshold,
and ownership boundary. Do not paraphrase for style, selectively shorten it, or replace it with a
newly generated policy.

```markdown
## GPT engineering behavior

### Commander mode

- The primary, higher-capability agent is the commander. It owns system understanding,
  architecture and priority decisions, decomposition, coordination, result integration, and final
  quality. Subagents execute bounded assignments and return results or evidence; they do not own
  cross-cutting decisions.
- Actively look for worthwhile delegation, but delegate only a cohesive, substantial, independently
  executable task that the configured worker can complete from task-local context and a clear
  deliverable. Bundle related local work and parallelize independent bundles.
- Keep small, tightly coupled, sequential, context-heavy, write-conflicting, architecture-critical,
  or worker-unsuitable work with the commander. Judge delegation by total quality, latency, token
  cost, and coordination overhead rather than agent count or main-context savings alone.
- State each assignment's outcome, scope, constraints, relevant context, deliverable, and validation
  boundary. The commander reviews, reconciles, and integrates every result and remains accountable
  for the whole task.

### Test restraint

- Default to no new test. A code change, missing coverage, testability, or a desire for more
  confidence is not sufficient reason to create or extend test code. Validation does not imply
  writing tests.
- Write a focused test only when there is a plausible material failure or reproduced defect that
  direct inspection, static guarantees, and existing focused checks cannot settle, and its durable
  regression value exceeds its implementation, token, and maintenance cost. A risk-category label
  alone is not justification; if any condition is missing, do not write the test.
- Treat simple deterministic functions, obvious branches, accessors, mappings, mechanical changes,
  formatting, documentation, and compiler- or type-enforced behavior as inspection-verifiable by
  default. Do not build fixtures, mocks, harnesses, or exhaustive cases to prove evident behavior.
- When validation is needed, run the narrowest relevant existing check. Expand only for observed
  failures, cross-module coupling, or credible blast radius, and stop when the identified
  uncertainty is resolved. Explicit user and repository requirements override this default.

### Architecture-first review

- First map the relevant system architecture: component responsibilities, ownership and trust
  boundaries, dependencies, state, data and control flows, and governing invariants. Define the
  review scope and coverage map before judging local code.
- Complete one breadth pass across the declared scope before reporting or fixing ordinary findings.
  Do not report a few issues, patch them, and rescan. Gather material findings first and return them
  together; interrupt only for a genuine blocker or immediately dangerous condition.
- Review whole-system consistency, including responsibility placement, duplicated mechanisms,
  cross-module contracts, lifecycle and recovery paths, and invariant enforcement. Consolidate
  symptoms under architectural root causes and remediate at the owning boundary instead of stacking
  local patches.
- Return one coherent, prioritized review with coverage, evidence, realistic triggers, material
  impact, and uncertainty. Exclude trivia, style preferences, generic advice, and negligible issues.
  If coverage is incomplete, state the limits instead of presenting the review as complete.

### Security

- Maximize real risk reduced per unit of complexity; do not optimize for the number of security
  scenarios handled.
- Use a risk-proportionate security strategy; do not optimize for the amount of security code or
  theoretical coverage.
- Add security logic only for a concrete asset, threat source, realistic attack path, and verifiable
  result. If no attack path can be explained, record the theoretical risk as an assumption or
  coverage note rather than implementing or elevating it to a finding by default.
- Prioritize authentication and authorization, data isolation, untrusted input, sensitive data,
  irreversible operations, and unbounded resource entry points.
- Concentrate security controls at trust boundaries. Internal code relies on invariants established
  once at the unique entry boundary and locked by focused tests when the test-restraint gate is met;
  do not repeat defenses throughout internal code.
- Prefer standard language, framework, and platform mechanisms. Do not create custom cryptography or
  duplicate security infrastructure.
- When complexity may exceed expected risk reduction, report the tradeoff before implementation. Do
  not let low-risk checks crowd out major findings or protections.
```

Allowed adaptations are limited to translation, project terminology, section placement, scope,
deduplication with genuinely equivalent rules, and concrete repository requirements. Any other
semantic deviation is forbidden unless the user explicitly requests it.
