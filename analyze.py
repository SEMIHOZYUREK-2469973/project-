from tijdloze100_types import *
from typing import List, Dict
from stemmen_types import Edities, Nummer

def aantal_voorkomens(edities: Edities) -> Dict[Nummer, int]:
    """
    Bereken het aantal voorkomens van elk nummer in de Tijdloze 100.

    Args:
        edities (Edities): Een lijst van edities waarin elk nummer voorkomt.

    Returns:
        Dict[Nummer, int]: Een dictionary met als sleutel een nummer en als waarde het aantal voorkomens.
    """
    voorkomens = {}

    for editie in edities.values():
        for nummer in editie:
            if nummer not in voorkomens:
                voorkomens[nummer] = 0
            voorkomens[nummer] += 1

    return voorkomens

def eenjaarsvliegen(edities: Edities) -> List[Nummer]:
    """
    Vind nummers die slechts één keer voorkomen in een editie van de Tijdloze 100,
    maar niet in de vorige of volgende editie.

    Args:
        edities (Edities): Een dictionary met jaren als keys en lijsten van nummers als values.

    Returns:
        List[Nummer]: Een lijst van nummers die eenjaarsvliegen zijn.
    """
    eenjaarsvliegen_set = set()
    edities_keys = sorted(edities.keys())

    for i, jaar in enumerate(edities_keys):
        huidige = set(edities[jaar])
        vorige = set(edities[edities_keys[i - 1]]) if i > 0 else set()
        volgende = set(edities[edities_keys[i + 1]]) if i < len(edities_keys) - 1 else set()

        uniek = huidige - vorige - volgende
        eenjaarsvliegen_set.update(uniek)

    return list(eenjaarsvliegen_set)

def definitieve_eenjaarsvliegen(edities: Edities) -> List[Nummer]:
    """
    Vind nummers die definitieve eenjaarsvliegen zijn: ze komen slechts één keer
    voor in de gehele Tijdloze 100 en in geen enkele andere editie.

    Args:
        edities (Edities): Een dictionary met jaren als keys en lijsten van nummers als values.

    Returns:
        List[Nummer]: Een lijst van nummers die definitieve eenjaarsvliegen zijn.
    """
    voorkomens = aantal_voorkomens(edities)
    eenjaarsvliegen_set = set(eenjaarsvliegen(edities))

    definitieve = [nummer for nummer in eenjaarsvliegen_set if voorkomens[nummer] == 1]

    return definitieve
