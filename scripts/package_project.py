"""Crée une archive de sources sans dossier enveloppe, Git ni environnement local."""

import argparse
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = {"README.md", "GUIDE_EXECUTION.md", "MODIFICATIONS.md", "INTEGRATION.md", "Makefile", ".gitignore", "requirements.txt"}
DIRECTORIES = {"tests", "scripts", "docs", ".github", "validation",
               "tp1-filtage-spam", "tp2-chiffrement-substitution",
               "tp3-random-number-generator", "tp4-nombres-premiers-et-images"}
EXCLUDED = {".git", ".venv", "venv", "__pycache__", "output", "outputs", ".pytest_cache", "dist", ".idea", ".vscode", "token", "token.txt"}


def project_files(root=ROOT):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in EXCLUDED or part.endswith(".egg-info") for part in relative.parts):
            continue
        if relative.parts[0] not in DIRECTORIES and relative.as_posix() not in ROOT_FILES:
            continue
        if relative.parts[:2] == ("tp3-random-number-generator", "data"):
            continue
        if path.suffix in {".zip", ".pyc", ".pyo"} or path.is_symlink():
            continue
        yield path, relative


def create_archive(destination, root=ROOT):
    destination = Path(destination)
    files = list(project_files(root))
    if destination.resolve() in {path.resolve() for path, _ in files}:
        raise ValueError("L'archive de sortie doit être hors des sources sélectionnées.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path, relative in files:
            info = zipfile.ZipInfo(relative.as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    return len(files)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/intro-python3-ameliore.zip")
    args = parser.parse_args(argv)
    count = create_archive(args.output)
    print(f"Archive créée : {args.output} ({count} fichiers)")


if __name__ == "__main__":
    main()
