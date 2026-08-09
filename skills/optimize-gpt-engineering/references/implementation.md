# Implementation Discipline

- Trace the existing path far enough to identify the owning boundary and governing invariants.
  Implement only requested behavior through the smallest coherent change there; do not stack local
  adapters around a wrong model.
- Reuse existing mechanisms, standard language or platform features, and installed dependencies.
  Do not create parallel paths, speculative branches, or unrelated refactors.
- Add an abstraction only to remove real duplication, own an invariant or volatile boundary, or name
  a domain operation that lowers reasoning cost; otherwise inline it. Do not add speculative
  interfaces, factories, configuration, extension points, or dependencies.
- Extract methods only for independent responsibility. Add variables only to name domain concepts,
  avoid repeated or unsafe evaluation, or clarify complex expressions. Remove pass-through layers
  and renamings; minimize concepts, not lines.
- Inspect the final diff and remove needless indirection, duplicate paths, and orphaned code, files,
  or dependencies. Every changed line must support the request, correctness or safety, or required
  validation.
