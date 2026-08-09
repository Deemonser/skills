---
name: validate-code-proportionately
description: "Choose and perform proportionate validation for code changes. Use when deciding whether to add or broaden tests, fixtures, mocks, harnesses, builds, linters, static checks, or runtime verification, and when reviewing whether validation matches credible risk. Do not use for non-code tasks with no engineering validation decision."
---

# Validate Code Proportionately

- Define the changed behavior, plausible failure, blast radius, and uncertainty before choosing a
  check. Validation does not automatically mean writing a new test.
- Use inspection and static guarantees for simple deterministic behavior, obvious mappings,
  mechanical edits, formatting, documentation, and compiler- or type-enforced properties.
- Add a focused test when it protects durable behavior against a plausible material regression that
  inspection, static guarantees, and existing focused checks cannot settle. Avoid fixtures, mocks,
  exhaustive cases, and new harnesses whose maintenance cost exceeds the confidence gained.
- Reproduce defects before fixing them when practical. Prefer a regression test when it proves the
  failure and remains valuable after the implementation changes.
- Run the narrowest relevant existing check first. Expand only for an observed failure,
  cross-module coupling, credible blast radius, or an explicit repository or user requirement.
- Stop when the relevant uncertainty is resolved. Report what was checked and any material risk left
  unverified; never imply broader coverage than was actually obtained.
- Follow explicit user instructions and repository-required gates even when they are broader than
  these defaults.
