# Cargo Build Strategies

Read this reference only when changing build profiles, compiler caches, linkers, feature sets, or
dependency versions, or when diagnosing persistent build time or disk growth.

## Contents

- Choose a profile policy deliberately
- Preserve one cache identity
- Apply speed levers in evidence order
- Interpret disk growth
- Clean only after diagnosis

## Choose a profile policy deliberately

Cargo's `dev` profile defaults to full debug information and incremental compilation; `test`
inherits from `dev`. Incremental state improves workspace-crate recompilation but consumes additional
space in `target`. The `"*"` package override applies to non-workspace dependencies.

Use a speed-oriented baseline when developer edit latency matters and disk is monitored:

```toml
[profile.dev]
debug = "line-tables-only"
incremental = true

[profile.dev.package."*"]
debug = false

[profile.test]
debug = "line-tables-only"
incremental = true

[profile.test.package."*"]
debug = false
```

Use a disk-bounded baseline for constrained agents or CI:

```toml
[profile.dev]
debug = "line-tables-only"
incremental = false

[profile.dev.package."*"]
debug = false

[profile.test]
debug = "line-tables-only"
incremental = false

[profile.test.package."*"]
debug = false
```

Do not apply either preset blindly. Confirm debugger needs, platform behavior, CI cache policy, and
repository conventions. Define workspace profiles only in the root manifest. Avoid a build override
unless measurements justify it; a dependency used both normally and at build time may then compile
twice.

Official reference: [Cargo profiles](https://doc.rust-lang.org/stable/cargo/reference/profiles.html)

## Preserve one cache identity

Cargo output separates by profile and target triple, and compiler inputs such as features,
`RUSTFLAGS`, the Rust toolchain, and wrappers affect reuse. Newer Cargo versions can also separate
final artifacts in `build.target-dir` from intermediate artifacts in `build.build-dir`. Prefer a
committed repository decision over per-command environment variables. Record any necessary identity
change and keep it stable for the task.

Before blaming Cargo for a full rebuild, compare:

- `rustc -vV` and the pinned toolchain;
- selected profile and target triple;
- enabled features and dependency versions;
- `RUSTFLAGS`, encoded flags, incremental settings, and compiler wrappers;
- `CARGO_TARGET_DIR`, configured `build.target-dir`, and configured `build.build-dir`;
- build-script inputs and outputs;
- whether a clean or lockfile update occurred.

Official reference: [Cargo build cache](https://doc.rust-lang.org/stable/cargo/reference/build-cache.html)

## Apply speed levers in evidence order

1. Keep the edit loop package- and target-scoped. Prefer `cargo check` because it skips final code
   generation, while recognizing that some diagnostics appear only during code generation.
2. Run `cargo build --timings` once for a representative build. Read the critical path, concurrency,
   duplicate units, features, build scripts, and link time before tuning.
3. Run `cargo tree -d` to find dependencies built at multiple versions. Align versions only when API
   and MSRV constraints permit it; do not force a version merely to make the tree look smaller.
4. Inspect feature activation with `cargo tree -e features`. Disable default or optional features only
   after tracing the runtime capability they provide and adding relevant validation.
5. Reuse `sccache` when it is already installed and consistently configured. Prefer a stable
   `build.rustc-wrapper` or team environment decision; toggling `RUSTC_WRAPPER` during a task changes
   the build identity and can make results harder to compare.
6. Change the linker only when timings show linking on the critical path. Verify the linker exists on
   every supported target, configure it per target, and compare identical warm builds. Do not add a
   platform-specific linker as a generic Rust optimization.
7. Split an oversized crate only when measurements show it serializes the critical path and the new
   boundary is architecturally coherent. Do not create crates solely to chase a benchmark.

Official references: [cargo check](https://doc.rust-lang.org/cargo/commands/cargo-check.html),
[build timings](https://doc.rust-lang.org/cargo/reference/timings.html), and
[cargo tree](https://doc.rust-lang.org/cargo/commands/cargo-tree.html)

## Interpret disk growth

| Evidence | Likely cause | First response |
|---|---|---|
| `debug/deps` dominates | Large graph, duplicate versions, debug info, or feature variants | Inspect profiles, `cargo tree -d`, and feature activation |
| `debug/incremental` dominates | Incremental state for workspace/path crates | Keep it for speed if within budget; otherwise choose a consistent disk-bounded profile |
| Multiple profile directories | Repeated `--profile` or release/dev workflows | Confirm each profile is necessary and keep task commands consistent |
| Target-triple directories appear | `--target` or configured build target | Confirm cross compilation is intended; host and target artifacts are separate |
| Rebuild follows every command | Build identity or build-script input changes | Compare toolchain, flags, features, wrapper, target dir, and build-script outputs |
| Link step dominates warm builds | Linker or final artifact size | Profile with timings, then evaluate a supported faster linker |

Cargo's automatic cache collection currently covers the global Cargo home cache, not project build
artifacts in `target`. A repository therefore needs its own target budget and observation policy.

Official reference: [Cargo cache configuration](https://doc.rust-lang.org/cargo/reference/config.html#cache)

## Clean only after diagnosis

`cargo clean` without selectors deletes the entire target directory. Use `cargo clean --dry-run` to
preview, add `--verbose` to list files, and select an exact package, profile, target, or docs when that
is sufficient. Cleaning may recover space but guarantees a cold rebuild; it does not repair cache
fragmentation, excessive features, duplicate dependencies, or an unsuitable profile.

Official reference: [cargo clean](https://doc.rust-lang.org/cargo/commands/cargo-clean.html)
