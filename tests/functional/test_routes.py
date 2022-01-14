import pytest

from server import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_index_route(client):
    response = client.get('/')

    assert response.status_code == 200
    data = response.data.decode()
    assert "Please enter your secretary email to continue:" in data


def test_logout_route(client):
    response = client.get('/logout', follow_redirects=True)

    assert response.status_code == 200
    data = response.data.decode()
    assert "Please enter your secretary email to continue:" in data


def test_login_user_should_log(client):
    email = 'tom@aarprin.es'

    response = client.post(
        '/showSummary',
        data=dict(email=email),
        follow_redirects=True
    )
    assert response.status_code == 200
    data = response.data.decode()
    assert f"Welcome, {email}" in data


def test_login_fail_should_redirect_to_index(client):
    email = "fake@email.com"

    response = client.post(
        '/showSummary',
        data=dict(email=email),
        follow_redirects=True
    )

    assert response.status_code == 200
    data = response.data.decode()
    assert "Sorry, this email" in data


def test_book_route(client):
    competition = "Winter Contest"
    club = "Arrhes Prince"

    response = client.get(
        f'/book/{competition}/{club}',
        follow_redirects=True
    )

    assert response.status_code == 200
    data = response.data.decode()
    assert 'How many places?' in data


def test_purchase_places_route(client):
    places = '5'
    competition = "Winter Contest"
    club = "Arrhes Prince"

    response = client.post(
        '/purchasePlaces',
        data=dict(places=places, competition=competition, club=club),
        follow_redirects=True
    )

    assert response.status_code == 200
    data = response.data.decode()
    assert 'Great-booking complete!' in data


def test_points_display_route(client):
    club = "Arrhes Prince"

    response = client.get(f"/pointsDisplay/{club}")

    assert response.status_code == 200
    data = response.data.decode()
    assert "Number of Points:" in data
