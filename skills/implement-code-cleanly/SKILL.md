---
name: implement-code-cleanly
description: "Implement, debug, refactor, or review code with the smallest coherent design. Use for actual code changes and implementation-quality review, including explicit local quality checkpoints, technical-debt review, small-scope refactoring, and maintainability or performance review of a completed module. Avoid unnecessary helpers, abstractions, parallel paths, speculative extensibility, and unrelated refactors. Do not use for pure explanation, non-code work, or system-wide architecture review."
---

# Implement Code Cleanly

- Trace the existing path far enough to identify the owning boundary and governing invariants.
  Implement the requested behavior there through the smallest coherent change.
- Prefer existing mechanisms, standard language or platform features, and installed dependencies.
  Do not create parallel paths, speculative branches, extension points, configuration, or unrelated
  refactors.
- Add an abstraction only when it removes real duplication, owns an invariant or volatile boundary,
  or names a domain operation that lowers reasoning cost. Otherwise keep the logic direct.
- Extract a method only for an independent responsibility. Add a variable only to name a meaningful
  concept, avoid repeated or unsafe evaluation, or clarify a genuinely complex expression. Remove
  pass-through helpers, one-use renamings, and layers that merely forward data.
- Prefer a readable local implementation over factories, interfaces, wrappers, or generic machinery
  that have no present requirement. Minimize concepts and state, not merely line count.
- Preserve established repository conventions and behavior outside the request. Do not hide a wrong
  ownership or state model behind adapters; repair the owning boundary when the task requires it.
- When the user explicitly requests a quality checkpoint, technical-debt review, small-scope
  refactor, or module-level maintainability or performance review, pause feature work and read
  [Local Quality Checkpoint](references/quality-checkpoint.md). Keep review-only requests read-only;
  implement the bounded refactor only when requested.
- Inspect the final diff and simplify it once more. Remove needless indirection, duplicate paths,
  dead code, and orphaned files or dependencies. Every changed line must support requested behavior,
  correctness or safety, or necessary validation.
