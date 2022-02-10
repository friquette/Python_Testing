import pytest

from server import create_app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_full_routine(client):
    clubs = loadClubs()
    competitions = loadCompetitions()

    # test display club points
    response_points = client.get("/pointsDisplay")
    assert response_points.status_code == 200
    data_points = response_points.data.decode()
    assert "Number of Points:" in data_points

    user = clubs[0]
    competition = competitions[2]

    # test login
    response_login = client.post(
        '/showSummary',
        data=dict(email=user['email']),
        follow_redirects=True
    )
    assert response_login.status_code == 200
    data_login = response_login.data.decode()
    assert f"Welcome, {user['email']}" in data_login

    # test book
    response_book = client.get(
        f'/book/{competition["name"]}/{user["name"]}',
        follow_redirects=True
    )
    assert response_book.status_code == 200
    data_book = response_book.data.decode()
    assert 'How many places?' in data_book

    # test purchase place
    response_purchase = client.post(
        '/purchasePlaces',
        data=dict(
            places='2',
            competition=competition['name'],
            club=user['name']
        ),
        follow_redirects=True
    )
    assert response_purchase.status_code == 200
    data_purchase = response_purchase.data.decode()
    assert "Points available: 7" in data_purchase
    assert 'Great-booking complete!' in data_purchase

    # test logout
    response_logout = client.get('/logout', follow_redirects=True)
    assert response_logout.status_code == 200
    data_logout = response_logout.data.decode()
    assert "Please enter your secretary email to continue:" in data_logout
