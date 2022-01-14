import pytest

from server import loadClubs, loadCompetitions


def test_load_clubs():
    clubs_list = loadClubs()
    clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        },
        {
            "name": "Arrhes Prince",
            "email": "tom@aarprin.es",
            "points": "41"
        }
    ]
    assert clubs_list == clubs


def test_load_competitions():
    competitions_list = loadCompetitions()
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Winter Contest",
            "date": "2022-12-22 14:00:00",
            "numberOfPlaces": "8"
        },
        {
            "name": "Summer Vibe",
            "date": "2022-07-14 08:30:00",
            "numberOfPlaces": "16"
        }
    ]
    assert competitions_list == competitions


"""test d'intégration:
load clubs, load competition, index, summary, book, purchase, logout"""

"""détailler pourquoi max place"""
