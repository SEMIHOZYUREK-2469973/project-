from tijdloze100_types import *

class Stem:
    """Dit is de klasse die een Stem representeert

    Attributes:
        nummer (Nummer): Het nummer waarop gestemd wordt
        naam_van_stemmer (str): de naam van de persoon die stemde (voornaam en achternaam)
        email (str): het e-mailadres van de persoon die stemde
        timestamp (str): het moment waarop de stem gebeurde
    """
    def __init__(self, nummer : Nummer, naam_van_stemmer : str, email : str, timestamp : str):
        self.nummer = nummer
        self.naam_van_stemmer = naam_van_stemmer
        self.email = email 
        self.timestamp = timestamp 
        
# Een Stemmenlijst is een lijst van stemmen van het type Stem. 
Stemmenlijst = list[Stem]
