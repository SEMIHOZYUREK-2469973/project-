import os
import pytest
from reader_writer import lees_tijdloze100, schrijf_tijdloze100
from tijdloze100_types import Edities

def tijdelijke_testmap(tmp_path):
    """Maakt een tijdelijke testmap met testdata."""
    root_folder = tmp_path / "tijdloze"
    root_folder.mkdir()

    # Testdata voor 2020
    editie_2020 = root_folder / "2020"
    editie_2020.mkdir()
    for i in range(1, 3):  # Voeg twee nummers toe (nummer1 en nummer2)
        nummer_map = editie_2020 / f"nummer{i}"
        nummer_map.mkdir()

        artiest_bestand = nummer_map / "artiest.txt"
        titel_bestand = nummer_map / "titel.txt"
        jaar_bestand = nummer_map / "release_jaar.txt"

        artiest_bestand.write_text(f"Artiest{i}")
        titel_bestand.write_text(f"Titel{i}")
        jaar_bestand.write_text(f"200{i}")

    return str(root_folder)

def test_lees_tijdloze100(tijdelijke_testmap):
    """Test de lees_tijdloze100 functie."""
    edities = lees_tijdloze100(tijdelijke_testmap)

    # Verwacht resultaat
    verwacht: Edities = {
        2020: [
            ("Artiest1", "Titel1", 2001),
            ("Artiest2", "Titel2", 2002),
        ]
    }

    assert edities == verwacht, "De ingelezen data komt niet overeen met de verwachte data."

def test_lees_tijdloze100_bestand_ontbreekt(tijdelijke_testmap):
    """Test of een FileNotFoundError wordt opgegooid als een bestand ontbreekt."""
    # Verwijder een bestand om de fout te simuleren
    os.remove(os.path.join(tijdelijke_testmap, "2020", "nummer1", "artiest.txt"))

    with pytest.raises(FileNotFoundError, match=r"Bestand ontbreekt in .+nummer1.+"):
        lees_tijdloze100(tijdelijke_testmap)

def test_schrijf_tijdloze100(tmp_path):
    """Test de schrijf_tijdloze100 functie."""
    # Testdata
    edities: Edities = {
        2020: [
            ("Artiest1", "Titel1", 2001),
            ("Artiest2", "Titel2", 2002),
        ]
    }

    # Pad voor het test-CSV-bestand
    csv_out = tmp_path / "tijdloze100.csv"

    # Schrijf data naar CSV
    schrijf_tijdloze100(edities, str(csv_out))

    # Controleer de inhoud van het bestand
    with open(csv_out, encoding="utf-8") as f:
        inhoud = f.readlines()

    verwacht_inhoud = [
        "2020;1;Artiest1;Titel1;2001\n",
        "2020;2;Artiest2;Titel2;2002\n",
    ]

    assert inhoud == verwacht_inhoud, "De inhoud van het CSV-bestand komt niet overeen met de verwachting."

def test_schrijf_tijdloze100_leeg(tmp_path):
    """Test de schrijf_tijdloze100 functie met lege data."""
    # Lege edities
    edities: Edities = {}

    # Pad voor het test-CSV-bestand
    csv_out = tmp_path / "tijdloze100.csv"

    # Schrijf lege data naar CSV
    schrijf_tijdloze100(edities, str(csv_out))

    # Controleer dat het bestand leeg is
    with open(csv_out, encoding="utf-8") as f:
        inhoud = f.read()

    assert inhoud == "", "Het CSV-bestand zou leeg moeten zijn."
