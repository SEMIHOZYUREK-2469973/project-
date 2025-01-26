import pytest
from unittest.mock import patch, mock_open
from datetime import datetime
from stemmen_types import Stem, Stemmenlijst
from stemmen_tellen import bereken_top100, maak_stemmenlijst, filter_domein, filter_email, filter_laatste_stem

def stemmenlijst_bereken_top100():
    return [
        Stem(nummer=("Artist A", "Song A", 2023), naam_van_stemmer="User 1", email="user1@example.com", tijd="2023-01-26 14:00:00"),
        Stem(nummer=("Artist B", "Song B", 2023), naam_van_stemmer="User 2", email="user2@example.com", tijd="2023-01-26 15:00:00"),
        Stem(nummer=("Artist A", "Song A", 2023), naam_van_stemmer="User 3", email="user3@example.com", tijd="2023-01-26 16:00:00"),
    ]


def test_bereken_top100(stemmenlijst_bereken_top100):
    result = bereken_top100(stemmenlijst_bereken_top100)
    
   
    assert len(result) == 2 
    assert result[0] == ("Artist A", "Song A", 2023, 2)  
    assert result[1] == ("Artist B", "Song B", 2023, 1)  


@pytest.fixture
def mock_csv_data():
    return "Artist A;Song A;2023;User 1;user1@example.com;2023-01-26 14:00:00\n" \
           "Artist B;Song B;2023;User 2;user2@example.com;2023-01-26 15:00:00"


def test_maak_stemmenlijst(mock_csv_data):
    with patch("builtins.open", mock_open(read_data=mock_csv_data)):
        result = maak_stemmenlijst("fake_path.csv")
    
    assert len(result) == 2  
    assert result[0].nummer == ("Artist A", "Song A", 2023)
    assert result[1].nummer == ("Artist B", "Song B", 2023)


@pytest.fixture
def stemmenlijst_filter_email():
    return [
        Stem(nummer=("Artist A", "Song A", 2023), naam_van_stemmer="User 1", email="valid@example.com", tijd="2023-01-26 14:00:00"),
        Stem(nummer=("Artist B", "Song B", 2023), naam_van_stemmer="User 2", email="invalid_email", tijd="2023-01-26 15:00:00"),
    ]


def test_filter_email(stemmenlijst_filter_email):
    result = filter_email(stemmenlijst_filter_email)
    
    assert len(result) == 1 
    assert result[0].email == "valid@example.com"


@pytest.fixture
def stemmenlijst_filter_laatste_stem():
    return [
        Stem(nummer=("Artist A", "Song A", 2023), naam_van_stemmer="User 1", email="user1@example.com", tijd="2023-01-26 14:00:00"),
        Stem(nummer=("Artist A", "Song A", 2023), naam_van_stemmer="User 1", email="user1@example.com", tijd="2023-01-26 15:00:00"),
        Stem(nummer=("Artist B", "Song B", 2023), naam_van_stemmer="User 2", email="user2@example.com", tijd="2023-01-26 14:00:00"),
    ]


def test_filter_laatste_stem(stemmenlijst_filter_laatste_stem):
    result = filter_laatste_stem(stemmenlijst_filter_laatste_stem)
    
    assert len(result) == 2  
    assert result[0].email == "user1@example.com"  
    assert result[1].email == "user2@example.com"


@pytest.fixture
def stemmenlijst_filter_domein():
    return [
        Stem(nummer=("Artist A", "Song A", 2023), naam_van_stemmer="User 1", email="user1@example.com", tijd="2023-01-26 14:00:00"),
        Stem(nummer=("Artist B", "Song B", 2023), naam_van_stemmer="User 2", email="user2@domain.com", tijd="2023-01-26 15:00:00"),
    ]


def test_filter_domein(stemmenlijst_filter_domein):
    result = filter_domein(stemmenlijst_filter_domein, "domain.com")
    
    assert len(result) == 1  
    assert result[0].email == "user1@example.com"
