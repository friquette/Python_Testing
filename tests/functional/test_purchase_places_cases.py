import pytest

from server import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_max_places_is_12(client):
    places_requested = '13'
    competition = "Summer Vibe"
    club = "She Lifts"

    response = client.post(
        '/purchasePlaces',
        data=dict(
            places=places_requested,
            competition=competition,
            club=club
        ),
        follow_redirects=True
    )

    assert response.status_code == 200
    data = response.data.decode()
    assert "purchase more than 12 places for a competition" in data


def test_not_enough_points(client):
    places_requested = '5'
    competition = "Summer Vibe"
    club = "She Lifts"

    response = client.post(
        '/purchasePlaces',
        data=dict(
            places=places_requested,
            competition=competition,
            club=club
        ),
        follow_redirects=True
    )

    assert response.status_code == 200
    data = response.data.decode()
    assert "have enough points" in data


def test_not_enough_places(client):
    places_requested = '10'
    competition = "Winter Contest"
    club = "Arrhes Prince"

    response = client.post(
        '/purchasePlaces',
        data=dict(
            places=places_requested,
            competition=competition,
            club=club
        ),
        follow_redirects=True
    )

    assert response.status_code == 200
    data = response.data.decode()
    assert "Not enough places available in this competition" in data


def test_successful_purchase(client):
    places_requested = '5'
    competition = "Summer Vibe"
    club = "Arrhes Prince"

    response = client.post(
        '/purchasePlaces',
        data=dict(
            places=places_requested,
            competition=competition,
            club=club
        ),
        follow_redirects=True
    )

    assert response.status_code == 200
    data = response.data.decode()
    print(data)
    assert "Points available: 26" in data
    assert "Great-booking complete!" in data
