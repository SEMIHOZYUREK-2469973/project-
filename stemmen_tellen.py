from stemmen_types import *
from tijdloze100_types import *
import csv
import re

def bereken_top100(stemmenlijst: Stemmenlijst) -> Editie:
    """
    Berekent de top 100 nummers uit een lijst van stemmen zonder gebruik van .timestamp of datetime.strptime.

    Args:
        stemmenlijst (Stemmenlijst): Lijst van stemmen.

    Returns:
        Editie: De top 100 nummers gesorteerd volgens de gegeven regels.
    """
    stemmen_telling = {}

    for stem in stemmenlijst:
        nummer = stem.nummer
        stemtijd = stem.tijd  # Veronderstel dat `stem.tijd` een string is zoals "2023-01-26 14:00:00"
        if nummer not in stemmen_telling:
            stemmen_telling[nummer] = [0, None]
        stemmen_telling[nummer][0] += 1
        if stemmen_telling[nummer][1] is None or stemtijd > stemmen_telling[nummer][1]:
            stemmen_telling[nummer][1] = stemtijd

    # Sorteer de nummers volgens de regels
    gesorteerd = sorted(
        stemmen_telling.items(),
        key=lambda item: (
            -item[1][0],  # Aantal stemmen (aflopend)
            item[1][1],   # Laatste stemtijd (lexicografisch oplopend)
            item[0][2],   # Releasejaar (oplopend)
            item[0][1],   # Titel (alfabetisch)
            item[0][0]    # Artiest (alfabetisch)
        )
    )

    # Beperk tot de top 100
    top100 = []
    for nummer, stemmen in gesorteerd[:100]:
        top100.append((nummer[0], nummer[1], nummer[2], stemmen[0]))

    return top100



def maak_stemmenlijst(pad_naar_bestand_met_stemmen: str) -> Stemmenlijst:
    """
    Leest een CSV-bestand in en converteert elke geldige regel naar een Stem-object.

    Args:
        pad_naar_bestand_met_stemmen (str): Pad naar het csv-bestand met stemmen.

    Returns:
        Stemmenlijst: Een lijst van Stem-objecten.
    """
    stemmenlijst = []

    try:
        with open(pad_naar_bestand_met_stemmen, mode='r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            for regel in reader:
                if len(regel) != 6:
                    # Sla regels over die niet het juiste aantal velden hebben
                    continue

                artiest, titel, release_jaar, naam_stemmer, email_stemmer, tijd = regel

                # Maak een Stem-object en voeg toe aan de lijst
                stem = Stem(
                    nummer=(artiest, titel, int(release_jaar)),
                    naam_van_stemmer=naam_stemmer,
                    email=email_stemmer,
                    tijd=tijd  # Gebruik tijd als een string
                )
                stemmenlijst.append(stem)

    except FileNotFoundError:
        print(f"Fout: Het bestand '{pad_naar_bestand_met_stemmen}' kon niet worden gevonden.")
    except Exception as e:
        print(f"Fout tijdens het verwerken van het bestand: {e}")

    return stemmenlijst




def filter_email(stemmenlijst: Stemmenlijst) -> Stemmenlijst:
    """
    Filtert de stemmenlijst en verwijdert stemmen met ongeldige e-mailadressen.

    Args:
        stemmenlijst (Stemmenlijst): Lijst van stemmen.

    Returns:
        Stemmenlijst: Gefilterde lijst met enkel geldige e-mailadressen.
    """
    def is_geldig_email(email: str) -> bool:
        email_regex = re.compile(r'^[a-zA-Z0-9._-]+(\.[a-zA-Z0-9._-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$')
        return bool(email_regex.match(email))

    return [stem for stem in stemmenlijst if is_geldig_email(stem.email)]

def filter_laatste_stem(stemmenlijst: Stemmenlijst) -> Stemmenlijst:
    """
    Houdt enkel de laatste stem per e-mailadres over.

    Args:
        stemmenlijst (Stemmenlijst): Lijst van stemmen.

    Returns:
        Stemmenlijst: Gefilterde lijst met slechts één stem per e-mailadres.
    """
    laatste_stemmen = {}

    for stem in stemmenlijst:
        email = stem.email
        tijd = stem.tijd  # Veronderstel dat 'tijd' een string is in het formaat "YYYY-MM-DD HH:MM:SS"
        if email not in laatste_stemmen or tijd > laatste_stemmen[email].tijd:
            laatste_stemmen[email] = stem

    return list(laatste_stemmen.values())


def filter_domein(stemmenlijst: Stemmenlijst, domein: str) -> Stemmenlijst:
    """
    Verwijdert stemmen van een specifiek domein.

    Args:
        stemmenlijst (Stemmenlijst): Lijst van stemmen.
        domein (str): Het domein dat gefilterd moet worden.

    Returns:
        Stemmenlijst: Gefilterde lijst zonder stemmen van het opgegeven domein.
    """
    def heeft_domein(email: str, domein: str) -> bool:
        # Controleer of het e-mailadres eindigt op "@" gevolgd door het domein
        at_domein = f"@{domein}"
        return len(email) >= len(at_domein) and email[-len(at_domein):] == at_domein

    return [stem for stem in stemmenlijst if not heeft_domein(stem.email, domein)]

