import pytest

from server import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_max_places_is_12(client):
    places_requested = '13'
    competition = {
        "name": "Summer Vibe",
        "date": "2022-07-14 08:30:00",
        "numberOfPlaces": "16"
    }
    club = {
        "name": "She Lifts",
        "email": "kate@shelifts.co.uk",
        "points": "50"
    }

    response = client.post(
        '/purchasePlaces',
        data=dict(places=places_requested, competition=competition, club=club),
        follow_redirects=True
    )

    assert response.status_code == 200
    data = response.data.decode()
    assert "You can't purchase more than 12 places for a competition" in data


def test_not_enough_points(client):
    places_requested = '5'
    competition = {
        "name": "Summer Vibe",
        "date": "2022-07-14 08:30:00",
        "numberOfPlaces": "16"
    }
    club = {
        "name": "She Lifts",
        "email": "kate@shelifts.co.uk",
        "points": "12"
    }

    response = client.post(
        '/purchasePlaces',
        data=dict(places=places_requested, competition=competition, club=club),
        follow_redirects=True
    )

    assert response.status_code == 200
    data = response.data.decode()
    assert "You don't have enough points" in data


def test_not_enough_places(client):
    places_requested = '10'
    competition = {
        "name": "Summer Vibe",
        "date": "2022-07-14 08:30:00",
        "numberOfPlaces": "8"
    }
    club = {
        "name": "She Lifts",
        "email": "kate@shelifts.co.uk",
        "points": "50"
    }

    response = client.post(
        '/purchasePlaces',
        data=dict(places=places_requested, competition=competition, club=club),
        follow_redirects=True
    )

    assert response.status_code == 200
    data = response.data.decode()
    assert "Not enough places available in this competition" in data


def test_successful_purchase(client):
    places_requested = '5'
    competition = {
        "name": "Summer Vibe",
        "date": "2022-07-14 08:30:00",
        "numberOfPlaces": "8"
    }
    club = {
        "name": "She Lifts",
        "email": "kate@shelifts.co.uk",
        "points": "50"
    }

    response = client.post(
        '/purchasePlaces',
        data=dict(places=places_requested, competition=competition, club=club),
        follow_redirects=True
    )

    assert response.status_code == 200
    data = response.data.decode()
    assert club['points'] == '35'
    assert "Great-booking complete!" in data
