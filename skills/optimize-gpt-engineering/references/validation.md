# Validation and Test Restraint

- Default to no new test. A code change, missing coverage, testability, desired confidence, or a
  risk label is insufficient; validation does not imply writing tests.
- Write a focused test only when there is a plausible material failure or reproduced defect that
  inspection, static guarantees, and existing focused checks cannot settle, and its durable
  regression value exceeds implementation, token, and maintenance cost. If any condition is
  missing, do not write the test.
- Treat simple deterministic behavior, obvious branches, accessors, mappings, mechanical changes,
  formatting, documentation, and compiler- or type-enforced behavior as inspection-verifiable. Do
  not build fixtures, mocks, harnesses, or exhaustive cases to prove evident behavior.
- When validation is needed, run the narrowest relevant existing check. Expand only for observed
  failures, cross-module coupling, or credible blast radius; stop when the uncertainty is resolved.
  Explicit user and repository requirements override this default.
