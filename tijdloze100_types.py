# Een nummer bestaat uit een artiest, een titel en een releasejaar.
# bv: ("The Beatles", "Hey Jude", 1968)
Nummer = tuple[str, str, int]

# Een editie van de Tijdloze bestaat uit een lijst van nummers.
# De index van een nummer in de lijst (+1) is de positie van het nummer in de Tijdloze.
# Het element op index 0 is de nummer 1 van die editie,
# het element op index 1 is de nummer 2 van die editie, enz.
Editie = list[Nummer]


# Alle edities van de Tijdloze 100.
# De key van de dictionary is het jaartal van de editie.
Edities = dict[int, Editie]


def artiest(nr: Nummer) -> str:
    """Geeft de artiest van een nummer.

    Args:
        nr (Nummer): Het nummer.

    Returns:
        str: de artiest van het nummer.
    """
    return nr[0]


def titel(nr: Nummer) -> str:
    """Geeft de titel van een nummer.

    Args:
        nr (Nummer): Het nummer.

    Returns:
        str: de titel van het nummer.
    """
    return nr[1]


def releasejaar(nr: Nummer) -> int:
    """Geeft het releasejaar van een nummer.

    Args:
        nr (Nummer): Het nummer.

    Returns:
        int: het releasejaar van het nummer.
    """
    return nr[2]
