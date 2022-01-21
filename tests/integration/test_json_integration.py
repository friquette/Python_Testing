import pytest

from server import create_app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_authentication_with_json_datas(client):
    clubs = loadClubs()

    club_to_login = clubs[0]

    response = client.post(
        '/showSummary',
        data=dict(email=club_to_login['email']),
        follow_redirects=True
    )
    assert response.status_code == 200
    data = response.data.decode()
    assert f"Welcome, {club_to_login['email']}" in data


def test_book_with_json_datas(client):
    clubs = loadClubs()
    competitions = loadCompetitions()

    club_logged_in = clubs[0]
    competition_to_book = competitions[2]

    response = client.get(
        f'/book/{competition_to_book["name"]}/{club_logged_in["name"]}',
        follow_redirects=True
    )

    assert response.status_code == 200
    data = response.data.decode()
    assert 'How many places?' in data
