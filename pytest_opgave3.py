import pytest
from tijdloze100_types import Nummer, Edities
from collections import defaultdict
from analyze import definitieve_eenjaarsvliegen, aantal_voorkomens, eenjaarsvliegen

def edities_sample():
    return {
        2023: [("Artist A", "Song A", 2023), ("Artist B", "Song B", 2023)],
        2024: [("Artist A", "Song A", 2023), ("Artist C", "Song C", 2024)],
        2025: [("Artist B", "Song B", 2023), ("Artist D", "Song D", 2025)],
    }

def test_aantal_voorkomens(edities_sample):
    result = aantal_voorkomens(edities_sample)
    
    # Check if the occurrences match the expected results
    assert result[("Artist A", "Song A", 2023)] == 2  # This song appears in two editions
    assert result[("Artist B", "Song B", 2023)] == 2  # This song also appears in two editions
    assert result[("Artist C", "Song C", 2024)] == 1  # This song appears only in 2024
    assert result[("Artist D", "Song D", 2025)] == 1  # This song appears only in 2025


def edities_sample():
    return {
        2023: [("Artist A", "Song A", 2023), ("Artist B", "Song B", 2023)],
        2024: [("Artist A", "Song A", 2023), ("Artist C", "Song C", 2024)],
        2025: [("Artist B", "Song B", 2023), ("Artist D", "Song D", 2025)],
    }

def test_eenjaarsvliegen(edities_sample):
    result = eenjaarsvliegen(edities_sample)
    
    # Check if the result contains the expected unique songs
    assert ("Artist C", "Song C", 2024) in result  # "Song C" appears only in 2024
    assert ("Artist D", "Song D", 2025) in result  # "Song D" appears only in 2025
    assert ("Artist A", "Song A", 2023) not in result  # "Song A" appears in both 2023 and 2024
    assert ("Artist B", "Song B", 2023) not in result  # "Song B" appears in both 2023 and 2025


def edities_sample():
    return {
        2023: [("Artist A", "Song A", 2023), ("Artist B", "Song B", 2023)],
        2024: [("Artist A", "Song A", 2023), ("Artist C", "Song C", 2024)],
        2025: [("Artist B", "Song B", 2023), ("Artist D", "Song D", 2025)],
    }

def test_definitieve_eenjaarsvliegen(edities_sample):
    result = definitieve_eenjaarsvliegen(edities_sample)
    
    # Check if the definitive one-year flies are correct
    assert ("Artist C", "Song C", 2024) in result  # This song only appears in 2024
    assert ("Artist D", "Song D", 2025) in result  # This song only appears in 2025
    assert ("Artist A", "Song A", 2023) not in result  # "Song A" appears in multiple editions
    assert ("Artist B", "Song B", 2023) not in result  # "Song B" appears in multiple editions
