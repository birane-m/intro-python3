"""Nettoyage de numéros français et traitement du fichier fourni au TP1."""

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

TP_ROOT = Path(__file__).resolve().parents[1]


def format_phone_number(phone_number: str) -> tuple[bool, str | None]:
    """Applique les règles du sujet : préfixe français puis dix chiffres."""
    digits = "".join(c for c in phone_number if c.isdigit() or c == "+")
    if digits.startswith("+33"):
        digits = "0" + digits[3:]
    elif digits.startswith("0033"):
        digits = "0" + digits[4:]
    digits = [c for c in digits if c != "+"]
    if not (digits and digits[0] == "0" and len(digits) == 10):
        return False, None
    return True, "-".join(digits[i] + digits[i + 1] for i in range(0, 10, 2))


def read_entries(source: Path) -> list[tuple[str, str]]:
    """Lit « nom : numéro », ignore les lignes vides, signale les lignes mal formées."""
    entries = []
    with source.open(encoding="utf-8", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        for row in reader:
            if not row or (len(row) == 1 and not row[0].strip()):
                continue
            if len(row) != 1 or ":" not in row[0]:
                raise ValueError(f"Ligne {reader.line_num} : format attendu « nom : numéro ».")
            name, number = row[0].split(":", 1)
            if not name.strip():
                raise ValueError(f"Ligne {reader.line_num} : nom manquant.")
            entries.append((name.strip(), number.strip()))
    return entries


def process_file(source: Path, destination: Path, summary_path: Path) -> dict:
    """Écrit les entrées valides et un bilan JSON ; retourne le bilan."""
    source, destination, summary_path = map(Path, (source, destination, summary_path))
    if len({p.resolve() for p in (source, destination, summary_path)}) != 3:
        raise ValueError("L'entrée, la sortie et le bilan doivent être des fichiers distincts.")
    entries = read_entries(source)
    names, numbers = zip(*entries) if entries else ((), ())
    formatted = list(map(format_phone_number, numbers))
    valid_entries = [(name, number) for name, (valid, number) in zip(names, formatted) if valid]
    invalid_names = [name for name, (valid, _) in zip(names, formatted) if not valid]
    counts = Counter(number for _, number in valid_entries)
    families = [[name for name, value in valid_entries if value == number]
                for number, count in counts.items() if count > 1]
    summary = {
        "input": str(source), "output": str(destination), "entries": len(entries),
        "valid": len(valid_entries), "invalid": len(invalid_names),
        "duplicate_groups": len(families), "duplicate_group_sizes": sorted(map(len, families)),
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as stream:
        csv.writer(stream).writerows([f"{name} : {number}"] for name, number in valid_entries)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Les noms des personnes ayant transmis un mauvais numéro de téléphone :")
    for name in invalid_names:
        print(name)
    print("\nLes foyers partageant un même numéro de téléphone :")
    print(families)
    return summary


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=TP_ROOT / "data/liste_numeros.txt")
    parser.add_argument("--output", type=Path, default=TP_ROOT / "output/output.txt")
    parser.add_argument("--summary", type=Path, help="Bilan JSON ; par défaut <sortie>.summary.json.")
    args = parser.parse_args(argv)
    try:
        process_file(args.input, args.output, args.summary or args.output.with_suffix(".summary.json"))
    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
