import csv


def format_phone_number(phone_number: str) -> tuple[bool, str | None]:
    """
    Vérifie et reformate un numéro de téléphone français.

    Args:
        phone_number: numéro brut, dans un format quelconque
            (espaces, tirets, parenthèses, +33, 0033, etc.).

    Returns:
        Un tuple (est_valide, numero_formate).
        - Si le numéro est valide (commence par 0 après nettoyage, 10 chiffres) :
          (True, "01-23-45-67-89")
        - Sinon :
          (False, None)
    """
    digits = [c for c in phone_number if c.isdigit() or c == "+"]
    digits = "".join(digits)

    if digits.startswith("+33"):
        digits = "0" + digits[3:]
    elif digits.startswith("0033"):
        digits = "0" + digits[4:]

    digits = [c for c in digits if c != "+"]

    if not (digits and digits[0] == "0" and len(digits) == 10):
        return False, None

    pairs = [digits[i] + digits[i + 1] for i in range(0, len(digits), 2)]
    return True, "-".join(pairs)


def main() -> None:
    """Lit data/liste_numeros.txt, filtre les numéros valides, et écrit le résultat dans output/output.txt."""
    try:
        with open("data/liste_numeros.txt", "r") as source_file:
            rows = list(csv.reader(source_file))
    except FileNotFoundError:
        print("Fichier Introuvable.")
        return

    names_and_numbers = [row[0].split(":") for row in rows]
    names, phone_numbers = zip(*names_and_numbers)

    formatted_numbers = map(format_phone_number, phone_numbers)

    valid_entries = [
        (name.strip(), formatted)
        for name, (is_valid, formatted) in zip(names, formatted_numbers)
        if is_valid
    ]

    with open("output/output.txt", "w", newline="") as output_file:
        writer = csv.writer(output_file)
        for name, phone_number in valid_entries:
            writer.writerow([f"{name} : {phone_number}"])


if __name__ == "__main__":
    main()