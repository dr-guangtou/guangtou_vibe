"""Export the transferable skill without build outputs or local environments."""

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("archive", type=Path, help="Destination ZIP file")
arguments = parser.parse_args()

skill_root = Path(__file__).resolve().parent.parent
archive_path = arguments.archive.expanduser().resolve()
excluded_directories = {".git", ".venv", "_build", "__pycache__", ".ruff_cache"}
source_files = [
    file_path
    for file_path in sorted(skill_root.rglob("*"))
    if file_path.is_file()
    and file_path.resolve() != archive_path
    and not excluded_directories.intersection(file_path.relative_to(skill_root).parts)
]

archive_path.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as archive:
    for file_path in source_files:
        archive.write(file_path, Path("note-style") / file_path.relative_to(skill_root))

print(f"Packaged {len(source_files)} files into {archive_path}")
