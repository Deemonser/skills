#!/usr/bin/env python3
"""Read-only Cargo capacity preflight and workspace change scoping."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from collections import deque
from pathlib import Path
from typing import Any


GIB = 1024**3
CACHE_ENV_NAMES = {
    "CARGO_TARGET_DIR",
    "CARGO_BUILD_TARGET_DIR",
    "CARGO_BUILD_BUILD_DIR",
    "CARGO_BUILD_TARGET",
    "CARGO_INCREMENTAL",
    "CARGO_BUILD_INCREMENTAL",
    "RUSTFLAGS",
    "CARGO_BUILD_RUSTFLAGS",
    "CARGO_ENCODED_RUSTFLAGS",
    "RUSTC_WRAPPER",
    "CARGO_BUILD_RUSTC_WRAPPER",
    "RUSTC_WORKSPACE_WRAPPER",
    "CARGO_BUILD_RUSTC_WORKSPACE_WRAPPER",
}
WORKSPACE_WIDE_FILES = {
    "Cargo.lock",
    "Cargo.toml",
    "rust-toolchain",
    "rust-toolchain.toml",
}


def run(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def cargo_metadata(manifest: Path | None, allow_unlocked: bool) -> dict[str, Any]:
    command = ["cargo", "metadata", "--format-version", "1", "--no-deps", "--color", "never"]
    if manifest:
        command.extend(["--manifest-path", str(manifest)])
    if not allow_unlocked:
        command.append("--locked")
    result = run(command)
    if result.returncode:
        hint = " Pass --allow-unlocked only if a lockfile update is acceptable." if not allow_unlocked else ""
        raise RuntimeError(f"cargo metadata failed:\n{result.stderr.strip()}{hint}")
    return json.loads(result.stdout)


def allocated_bytes(path: Path) -> int:
    if not path.exists():
        return 0
    resolved = path.resolve()
    if shutil.which("du"):
        result = run(["du", "-sk", str(resolved)])
        if result.returncode == 0 and result.stdout.split():
            return int(result.stdout.split()[0]) * 1024
    if resolved.is_file():
        return resolved.stat().st_size
    total = 0
    for root, _, files in os.walk(resolved, followlinks=False):
        for filename in files:
            try:
                total += (Path(root) / filename).stat(follow_symlinks=False).st_size
            except OSError:
                continue
    return total


def human_size(value: int) -> str:
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024 or unit == "TiB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{value} B"
        value /= 1024
    raise AssertionError("unreachable")


def cache_environment() -> dict[str, str]:
    return {
        key: value
        for key, value in sorted(os.environ.items())
        if key in CACHE_ENV_NAMES or key.startswith("CARGO_PROFILE_")
    }


def version(command: list[str]) -> str:
    result = run(command)
    return result.stdout.strip() if result.returncode == 0 else result.stderr.strip()


def disk_usage(path: Path, fallback: Path) -> Any:
    candidate = path
    while not candidate.exists() and candidate != candidate.parent:
        candidate = candidate.parent
    return shutil.disk_usage(candidate if candidate.exists() else fallback)


def largest_entries(directory: Path) -> list[tuple[str, int]]:
    if not directory.is_dir():
        return []
    return sorted(
        ((child.name, allocated_bytes(child)) for child in directory.iterdir()),
        key=lambda item: item[1],
        reverse=True,
    )[:8]


def scan(args: argparse.Namespace) -> int:
    metadata = cargo_metadata(args.manifest_path, args.allow_unlocked)
    workspace = Path(metadata["workspace_root"])
    target = Path(metadata["target_directory"])
    build = Path(metadata.get("build_directory", metadata["target_directory"]))
    target_size = allocated_bytes(target)
    build_size = target_size if build.resolve() == target.resolve() else allocated_bytes(build)
    footprint_size = target_size + (0 if build.resolve() == target.resolve() else build_size)
    locations = {target.resolve(), build.resolve()}
    disks = {str(location): disk_usage(location, workspace) for location in locations}
    free_size = min(disk.free for disk in disks.values())
    incremental_paths = {
        path.resolve()
        for pattern in ("*/incremental", "*/*/incremental")
        for path in build.glob(pattern)
        if path.is_dir()
    }
    incremental_size = sum(allocated_bytes(path) for path in incremental_paths)
    target_children = largest_entries(target)
    build_children = [] if build.resolve() == target.resolve() else largest_entries(build)

    hard_reasons = []
    soft_reasons = []
    if footprint_size >= args.hard_build_gib * GIB:
        hard_reasons.append("target/build footprint reached the hard size limit")
    elif footprint_size >= args.soft_build_gib * GIB:
        soft_reasons.append("target/build footprint reached the soft size limit")
    if free_size <= args.hard_free_gib * GIB:
        hard_reasons.append("free disk reached the hard floor")
    elif free_size <= args.soft_free_gib * GIB:
        soft_reasons.append("free disk reached the soft floor")
    status = "hard-limit" if hard_reasons else "soft-limit" if soft_reasons else "ok"
    report = {
        "status": status,
        "reasons": hard_reasons or soft_reasons,
        "workspace_root": str(workspace),
        "target_directory": str(target),
        "build_directory": str(build),
        "target_bytes": target_size,
        "build_bytes": build_size,
        "footprint_bytes": footprint_size,
        "incremental_bytes": incremental_size,
        "free_bytes": free_size,
        "free_bytes_by_location": {location: disk.free for location, disk in disks.items()},
        "top_level_target_entries": [
            {"name": name, "bytes": size} for name, size in target_children
        ],
        "top_level_build_entries": [
            {"name": name, "bytes": size} for name, size in build_children
        ],
        "cache_identity_environment": cache_environment(),
        "cargo_version": version(["cargo", "--version"]),
        "rustc_version": version(["rustc", "-vV"]),
    }
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Rust build preflight: {status}")
        for reason in report["reasons"]:
            print(f"  reason: {reason}")
        print(f"  workspace: {workspace}")
        print(f"  target: {target} ({human_size(target_size)})")
        if build.resolve() != target.resolve():
            print(f"  build: {build} ({human_size(build_size)})")
        print(f"  build footprint: {human_size(footprint_size)}")
        print(f"  incremental: {human_size(incremental_size)}")
        for location, disk in disks.items():
            print(f"  free disk at {location}: {human_size(disk.free)}")
        if target_children:
            print("  largest target entries:")
            for name, size in target_children:
                print(f"    {name}: {human_size(size)}")
        if build_children:
            print("  largest build entries:")
            for name, size in build_children:
                print(f"    {name}: {human_size(size)}")
        overrides = report["cache_identity_environment"]
        print("  cache identity overrides:")
        if overrides:
            for name, value in overrides.items():
                print(f"    {name}={value}")
        else:
            print("    none")
        print(f"  {report['cargo_version']}")
        rustc_head = report["rustc_version"].splitlines()[0] if report["rustc_version"] else "rustc unavailable"
        print(f"  {rustc_head}")
    return 2 if status == "hard-limit" else 0


def git_changed(workspace: Path, reference: str, include_untracked: bool) -> list[str]:
    result = run(["git", "diff", "--name-only", "--diff-filter=ACMR", reference, "--"], workspace)
    if result.returncode:
        raise RuntimeError(f"git diff failed:\n{result.stderr.strip()}")
    changed = [line for line in result.stdout.splitlines() if line]
    if include_untracked:
        untracked = run(["git", "ls-files", "--others", "--exclude-standard"], workspace)
        if untracked.returncode:
            raise RuntimeError(f"git ls-files failed:\n{untracked.stderr.strip()}")
        changed.extend(line for line in untracked.stdout.splitlines() if line)
    return sorted(set(changed))


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def scope(args: argparse.Namespace) -> int:
    metadata = cargo_metadata(args.manifest_path, args.allow_unlocked)
    workspace = Path(metadata["workspace_root"]).resolve()
    members = set(metadata["workspace_members"])
    packages = [package for package in metadata["packages"] if package["id"] in members]
    roots = {package["id"]: Path(package["manifest_path"]).resolve().parent for package in packages}
    names = {package["id"]: package["name"] for package in packages}
    changed = list(args.changed)
    if args.git_diff:
        changed.extend(git_changed(workspace, args.git_diff, args.include_untracked))
    if not changed:
        raise RuntimeError("no changed paths supplied; use --changed or --git-diff")

    workspace_wide = False
    direct: set[str] = set()
    unmapped: list[str] = []
    normalized = []
    for raw_path in sorted(set(changed)):
        path = Path(raw_path)
        path = (path if path.is_absolute() else workspace / path).resolve(strict=False)
        normalized.append(str(path))
        if is_within(path, workspace):
            relative = path.relative_to(workspace)
            if relative.as_posix() in WORKSPACE_WIDE_FILES or relative.parts[:1] == (".cargo",):
                workspace_wide = True
                continue
        owners = [package_id for package_id, root in roots.items() if is_within(path, root)]
        if owners:
            direct.add(max(owners, key=lambda package_id: len(roots[package_id].parts)))
        else:
            unmapped.append(str(path))

    reverse: dict[str, set[str]] = {package_id: set() for package_id in members}
    root_to_id = {root: package_id for package_id, root in roots.items()}
    for package in packages:
        for dependency in package.get("dependencies", []):
            dependency_path = dependency.get("path")
            if dependency_path:
                dependency_id = root_to_id.get(Path(dependency_path).resolve())
                if dependency_id:
                    reverse[dependency_id].add(package["id"])

    affected = set(members if workspace_wide else direct)
    queue = deque(affected)
    while queue:
        for dependent in reverse.get(queue.popleft(), set()):
            if dependent not in affected:
                affected.add(dependent)
                queue.append(dependent)

    report = {
        "workspace_root": str(workspace),
        "workspace_wide": workspace_wide,
        "changed_paths": normalized,
        "direct_packages": sorted(names[package_id] for package_id in direct),
        "affected_packages": sorted(names[package_id] for package_id in affected),
        "unmapped_paths": unmapped,
    }
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Rust change scope: {'workspace-wide' if workspace_wide else 'package-scoped'}")
        print(f"  direct packages: {', '.join(report['direct_packages']) or 'none'}")
        print(f"  affected packages: {', '.join(report['affected_packages']) or 'none'}")
        if unmapped:
            print("  unmapped paths (inspect manually):")
            for path in unmapped:
                print(f"    {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--manifest-path", type=Path)
    common.add_argument("--allow-unlocked", action="store_true")
    common.add_argument("--json", action="store_true")

    scan_parser = subparsers.add_parser("scan", parents=[common], help="report capacity and cache identity")
    scan_parser.add_argument("--soft-build-gib", "--soft-target-gib", dest="soft_build_gib", type=float, default=8)
    scan_parser.add_argument("--hard-build-gib", "--hard-target-gib", dest="hard_build_gib", type=float, default=10)
    scan_parser.add_argument("--soft-free-gib", type=float, default=25)
    scan_parser.add_argument("--hard-free-gib", type=float, default=20)
    scan_parser.set_defaults(handler=scan)

    scope_parser = subparsers.add_parser("scope", parents=[common], help="map changed paths to workspace packages")
    scope_parser.add_argument("--changed", action="append", default=[], metavar="PATH")
    scope_parser.add_argument("--git-diff", metavar="REF")
    scope_parser.add_argument("--include-untracked", action="store_true")
    scope_parser.set_defaults(handler=scope)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "scan":
        if args.soft_build_gib > args.hard_build_gib:
            parser.error("soft build limit must not exceed hard build limit")
        if args.soft_free_gib < args.hard_free_gib:
            parser.error("soft free-disk floor must not be below hard free-disk floor")
    try:
        return args.handler(args)
    except (OSError, RuntimeError, json.JSONDecodeError, KeyError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
