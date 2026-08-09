---
name: review-architecture-first
description: "Review software architecture before judging local code. Use for architecture or system design, repository-wide or cross-component review, and changes involving responsibility placement, ownership, lifecycle, state machines, data or control flow, trust boundaries, recovery, or cross-module contracts. Do not use for narrow local implementation with no architectural decision."
---

# Review Architecture First

- Establish scope and a coverage map before local judgment. Map responsibilities, ownership and
  trust boundaries, dependencies, state, data and control flows, lifecycle, recovery paths, and
  governing invariants.
- Complete one breadth and cross-component pass before reporting findings or fixing symptoms.
  Evidence gathered by other agents counts as reviewed coverage only after the primary agent
  inspects and integrates it.
- Evaluate responsibility placement, duplicate mechanisms, cross-module contracts, lifecycle and
  recovery behavior, and where invariants are enforced. Distinguish architectural causes from local
  symptoms.
- Prefer remediation at the owning boundary. Do not stack adapters, duplicated state, or local
  guards around a broken ownership or contract model.
- Prioritize findings by realistic trigger and material impact. Include concrete evidence,
  affected paths, uncertainty, and the architectural cause that unifies related symptoms.
- Exclude trivia, style preferences, generic advice, and negligible issues. Disclose incomplete
  coverage instead of implying a full-system review.
- Keep final ownership with the primary agent: integrate findings into one coherent assessment and
  verify that proposed fixes preserve system-wide invariants.
