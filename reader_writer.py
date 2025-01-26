from tijdloze100_types import *
import os
import csv
import pytest



def lees_tijdloze100(root_folder: str) -> Edities:
    """
    Leest de Tijdloze 100 data in vanuit de gespecificeerde root folder.

    Args:
        root_folder (str): Pad naar de root folder van de data.

    Returns:
        Edities: Een dictionary met edities als key (jaartal) en een lijst van nummers als waarde.

    Raises:
        FileNotFoundError: Als een bestand (artiest.txt, titel.txt, release_jaar.txt) ontbreekt.
    """
    edities: Edities = {}

    for editie_folder in sorted(os.listdir(root_folder)):
        editie_pad = os.path.join(root_folder, editie_folder)
        if not os.path.isdir(editie_pad):
            continue

        nummers: Editie = []
        for i in range(1, 101):
            nummer_folder = os.path.join(editie_pad, f"nummer{i}")

            try:
                with open(os.path.join(nummer_folder, "artiest.txt")) as f:
                    nummer_artiest = f.read().strip()
                with open(os.path.join(nummer_folder, "titel.txt")) as f:
                    nummer_titel = f.read().strip()
                with open(os.path.join(nummer_folder, "release_jaar.txt")) as f:
                    nummer_jaar = int(f.read().strip())
            except FileNotFoundError as e:
                raise FileNotFoundError(f"Bestand ontbreekt in {nummer_folder}: {e}")

            nummers.append((nummer_artiest, nummer_titel, nummer_jaar))

        edities[int(editie_folder)] = nummers

    return edities


def schrijf_tijdloze100(edities: dict, csv_out: str) -> None:
    """
    Schrijft de Tijdloze 100 data naar een CSV-bestand zonder gebruik van .writerow().

    Args:
        edities (dict): De dictionary met edities en hun nummers.
        csv_out (str): Pad naar het CSV-bestand.
    """
    with open(csv_out, mode="w", newline="", encoding="utf-8") as f:
        # Iterate over the sorted editions and their respective songs
        for jaar, nummers in sorted(edities.items()):
            for rank, nummer in enumerate(nummers, start=1):
                # Maak een regel in het CSV-formaat
                regel = f"{jaar};{rank};{nummer[0]};{nummer[1]};{nummer[2]}\n"
                f.write(regel)  # Schrijf de regel direct naar het bestand
