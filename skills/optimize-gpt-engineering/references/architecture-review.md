# Architecture-First Review

- Before local judgment, map responsibilities, ownership and trust boundaries, dependencies, state,
  data and control flows, and governing invariants; define the scope and coverage map.
- The primary agent must complete one breadth and cross-component pass before ordinary reporting or
  fixing and must integrate the final findings. Workers may gather bounded evidence or independently
  verify a suspicion, but their output is not reviewed coverage until the primary agent inspects it.
- Evaluate whole-system responsibility placement, duplicate mechanisms, cross-module contracts,
  lifecycle and recovery paths, and invariant enforcement. Consolidate symptoms under architectural
  root causes and remediate at the owning boundary rather than stacking local patches.
- Return one prioritized review with coverage, evidence, realistic triggers, material impact, and
  uncertainty. Exclude trivia, style preferences, generic advice, and negligible issues; disclose
  incomplete coverage.
