---
name: optimize-gpt-engineering
description: "Apply high-standard engineering discipline when Codex implements, debugs, refactors, or reviews code; decides whether to add or broaden tests; uses subagents for engineering work; performs architecture or system review; or changes security-sensitive boundaries. Route only to the relevant guidance for minimal coherent implementation, risk-gated delegation, proportionate validation, architecture-first review, and reachable-risk security. Do not use for non-code tasks or explanations with no engineering decision."
---

# Optimize GPT Engineering

## Route

Before taking engineering action, classify the task and read every applicable reference completely:

- **Implementation** — Read [implementation.md](references/implementation.md) when creating,
  modifying, debugging, refactoring, or assessing implementation quality in code.
- **Delegation** — Read [delegation.md](references/delegation.md) only when subagents or parallel
  engineering work are permitted and will actually be used.
- **Validation** — Read [validation.md](references/validation.md) before adding or modifying tests,
  fixtures, mocks, or harnesses, or before broadening validation beyond the narrowest existing check.
- **Architecture review** — Read [architecture-review.md](references/architecture-review.md) for
  system design, repository-wide or cross-component review, or changes to ownership, lifecycle,
  state machines, or cross-module contracts.
- **Security** — Read [security.md](references/security.md) for security review or work involving
  authentication, authorization, data isolation, untrusted input, sensitive data, irreversible
  operations, or unbounded resource entry points.

Load the union for mixed tasks. Do not load an unrelated reference merely because it is available.
If no route applies, continue without applying this skill.

## Apply

- Treat loaded references as decision gates, not required plans or reporting templates.
- Follow explicit user and repository requirements where they conflict with these defaults.
- Do not copy reference content into `AGENTS.md` or inspect or edit Codex configuration during
  ordinary use.
- Only when explicitly asked to add persistent project routing, read
  [agents-md-router.md](references/agents-md-router.md) and install only that minimal hook.
- Complete the task normally. Report only material outcomes, validation, tradeoffs, and unresolved
  risk.
