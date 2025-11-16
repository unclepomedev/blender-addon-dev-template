#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

TEMPLATE_MARK = "addon_hello_world"
TEXT_EXTS = {".py", ".toml", ".md", ".txt", ".cfg", ".ini", ".rst", ".yml", ".yaml"}
EXCLUDE_DIRS = {".git", "dist", "build", "__pycache__", ".venv", ".idea", ".vscode", ".pytest_cache"}
EXCLUDE_FILES = {"addon_hello_world.zip"}  # Enter any files you want to explicitly exclude.


def is_text_candidate(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTS


def dest_from_template_name(src_path: Path, src_root: Path, dest_root: Path, new_name: str) -> Path:
    # Replace names that include TEMPLATE_MARK in each path component with new_name
    rel = src_path.relative_to(src_root)
    parts = [p.replace(TEMPLATE_MARK, new_name) for p in rel.parts]
    return dest_root.joinpath(*parts)


def copy_and_replace(src_root: Path, dest_root: Path, new_name: str, dry_run: bool, verbose: int) -> tuple[
    int, int, int]:
    files_copied = 0
    files_rewritten = 0
    total_replacements = 0

    for src in src_root.rglob("*"):
        if any(part in EXCLUDE_DIRS for part in src.relative_to(src_root).parts):
            continue  # skip excluded directories
        if src.is_dir():
            dest_dir = dest_from_template_name(src, src_root, dest_root, new_name)
            if verbose >= 2:
                print(f"[DIR] {src} -> {dest_dir}")
            if not dry_run:
                dest_dir.mkdir(parents=True, exist_ok=True)
            continue

        if src.name in EXCLUDE_FILES:
            if verbose >= 1:
                print(f"[SKIP FILE] {src}")
            continue

        dest_file = dest_from_template_name(src, src_root, dest_root, new_name)
        if not dry_run:
            dest_file.parent.mkdir(parents=True, exist_ok=True)

        wrote = False
        if is_text_candidate(src):
            try:
                text = src.read_text(encoding="utf-8")
                replaced_count = text.count(TEMPLATE_MARK)
                if replaced_count > 0:
                    text = text.replace(TEMPLATE_MARK, new_name)
                    if verbose >= 2:
                        print(f"[REWRITE] {src} -> {dest_file} ({replaced_count})")
                    if not dry_run:
                        dest_file.write_text(text, encoding="utf-8")
                    files_rewritten += 1
                    total_replacements += replaced_count
                    wrote = True
                else:
                    if not dry_run:
                        shutil.copy2(src, dest_file)
                    if verbose >= 2:
                        print(f"[COPY] {src} -> {dest_file}")
                    wrote = True
            except UnicodeDecodeError:
                pass

        if not wrote:
            if not dry_run:
                shutil.copy2(src, dest_file)
            if verbose >= 2:
                print(f"[BINCOPY] {src} -> {dest_file}")

        files_copied += 1

    return files_copied, files_rewritten, total_replacements


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Initialize a new Blender addon project from template with renamed identifier")
    parser.add_argument("new_name", help=f"New identifier to replace '{TEMPLATE_MARK}' (e.g. my_cool_addon)")
    parser.add_argument(
        "--template",
        default=str(Path.cwd()),
        help="Path to the template repository root (default: current directory)",
    )
    parser.add_argument(
        "--outdir",
        default=str(Path.cwd()),
        help="Directory to create the new project in (default: current directory)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    parser.add_argument("--force", action="store_true", help="Overwrite existing destination directory if needed")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity (-v, -vv)")

    args = parser.parse_args(argv)

    template_root = Path(args.template).resolve()
    outdir = Path(args.outdir).resolve()

    if not template_root.exists():
        print(f"[ERROR] Template not found: {template_root}", file=sys.stderr)
        return 2

    dest_project_root = outdir / args.new_name
    if dest_project_root.exists():
        if not args.force and not args.dry_run:
            print(f"[ERROR] Destination already exists: {dest_project_root}. Use --force or choose another name.",
                  file=sys.stderr)
            return 3
    else:
        if not args.dry_run:
            dest_project_root.mkdir(parents=True, exist_ok=True)

    files_copied, files_rewritten, total_replacements = copy_and_replace(
        src_root=template_root,
        dest_root=dest_project_root,
        new_name=args.new_name,
        dry_run=args.dry_run,
        verbose=args.verbose or 0,
    )

    mode = "DRY-RUN" if args.dry_run else "WRITE"
    print(
        f"[{mode}] created: {dest_project_root}\n"
        f" files processed: {files_copied}, files rewritten: {files_rewritten}, total replacements: {total_replacements}"
    )

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
