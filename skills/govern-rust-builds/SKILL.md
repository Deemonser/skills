---
name: govern-rust-builds
description: "Govern Rust and Cargo build scope, cache identity, artifact growth, and development iteration speed. Use before Codex runs or recommends nontrivial Cargo build, check, test, clippy, doc, bench, or clean commands in a Rust project, and when diagnosing repeated recompilation, slow builds, oversized target directories, profile or feature changes, cache configuration, linker bottlenecks, or CI/local cache reuse."
---

# Govern Rust Builds

Keep Cargo validation proportionate, cache-coherent, and bounded by available disk. Prefer evidence
from the current workspace over generic tuning advice.

## Establish the build contract

1. Read repository instructions, the workspace root `Cargo.toml`, `rust-toolchain*`, and applicable
   `.cargo/config*` files before choosing a command.
2. Preserve repository-required gates and user-specified targets. Do not weaken correctness checks
   to improve speed.
3. Treat the workspace-root profile and Cargo config as authoritative. Do not introduce temporary
   `CARGO_PROFILE_*`, `CARGO_INCREMENTAL`, `RUSTFLAGS`, `CARGO_TARGET_DIR`, `--profile`, or
   `--target` variations unless the task requires them; each variation can fork reusable artifacts.
4. Do not change build configuration as an incidental optimization. Make profile, linker, feature,
   or cache changes only when build governance or performance is in scope, and state the tradeoff.

## Run a read-only preflight

Resolve this skill's directory and run:

```text
python3 <skill-dir>/scripts/rust_build_guard.py scan --manifest-path <workspace>/Cargo.toml
```

The script reads Cargo metadata with `--locked`, resolves the effective target and intermediate-build
directories, reports disk capacity and build-identity overrides, and never compiles or cleans. If the
project intentionally has no lockfile, use `--allow-unlocked` only after accepting that Cargo may
create or update one.

Honor documented repository budgets. When none exist, use these fallback gates for an ordinary
workspace:

- Soft gate: effective target/build footprint at least 8 GiB or free disk at most 25 GiB. Do not
  begin a broad build; inspect scope and growth first.
- Hard gate: effective target/build footprint at least 10 GiB or free disk at most 20 GiB. Stop
  nonessential Cargo commands and report the constraint.

For a documented large monorepo, pass its explicit thresholds to the script instead of pretending
the fallback budget fits. Never use a cleanup to hide an unexplained growth pattern.

## Select the narrowest sufficient command

Determine changed packages before compiling. For a working-tree change, run:

```text
python3 <skill-dir>/scripts/rust_build_guard.py scope \
  --manifest-path <workspace>/Cargo.toml --git-diff HEAD --include-untracked
```

Use `direct packages` for the first check and `affected packages` to identify workspace dependents
that may need later validation. Treat workspace manifests, lockfiles, toolchains, and root Cargo
configuration as workspace-wide. Inspect unmapped build inputs manually.

Choose commands in this order:

1. Use inspection or a non-build check for documentation and mechanical changes.
2. Use `cargo check -p <package>` for compile feedback. Add `--lib`, `--bin`, or another exact target
   selector when only one target matters.
3. Use `cargo test -p <package> <test-filter>` when behavior must execute. Broaden the test target or
   package set only for credible dependents or cross-crate behavior.
4. Use targeted `cargo clippy -p <package>` after compilation behavior settles.
5. Run repository-required workspace gates once at final acceptance. Do not rerun them after docs,
   comments, formatting-only changes, dependency downloads, or retries that cannot invalidate them.

Do not use `--workspace`, `--all-targets`, or `--all-features` as a substitute for impact analysis.
Remember that a virtual workspace without `default-members` can select every member even when
`--workspace` is absent; use `-p` explicitly.

## Keep the development loop fast

- Keep the toolchain, profile, target, feature set, flags, wrapper, and target directory stable across
  comparable commands. Diagnose why a dependency rebuilt before clearing its cache.
- Prefer `cargo check` during editing; build or test only when code generation, linking, build-script
  behavior, or execution matters.
- Preserve incremental compilation when edit-loop latency is the priority and disk has budget.
  Disable it for disk-bounded agents or CI only through a consistent repository profile, not a
  one-off environment override.
- Remove debug information from third-party dependencies when debugger requirements allow it while
  retaining line tables for workspace code. Apply profiles only at the workspace root.
- Reuse an already configured compiler cache such as `sccache`; do not install one or toggle
  `RUSTC_WRAPPER` within a task without authorization and a persistent configuration decision.
- Use `cargo build --timings` only for a deliberate profiling run. Optimize the measured critical
  path: duplicate dependency versions, excess features, expensive build scripts, or linking.
- Read [Cargo strategies](references/cargo-strategies.md) before changing profiles, cache wrappers,
  linkers, features, or dependency versions.

## Diagnose repeated or oversized builds

Compare the preflight with the command history and ask which cache identity changed: toolchain,
profile, feature set, `RUSTFLAGS`, target triple, build-script output, dependency graph, or target
directory. Inspect `target` subdirectory sizes and run `cargo tree -d` when duplicate versions are a
credible contributor. Do not claim Cargo rebuilt "everything" without identifying the rebuilt units
or the changed input.

If timing rather than disk is the problem, perform one representative warm build before collecting
`--timings`; a cold build answers a different question. Keep benchmark inputs identical.

## Finish and clean safely

1. Rerun `scan` after the final Cargo batch and report target/build footprint and free-disk deltas.
2. If over budget, use `cargo clean --dry-run` with the same manifest, target, and profile selectors
   to estimate the exact deletion. With no selector, `cargo clean` removes the entire target tree.
3. Require explicit user authorization before any actual `cargo clean`. Prefer the smallest effective
   package, profile, target, or doc selection, and explain that the next relevant build will be cold.
4. Never replace Cargo cleanup with `rm -rf target`, unresolved variables, globs, or broad paths.
5. Report the exact commands run, whether they were cold or warm, what was not validated, capacity
   before and after, and any deliberate cache-identity changes.
