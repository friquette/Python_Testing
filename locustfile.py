from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def index(self):
        self.client.get('/')

    @task
    def showSummary(self):
        with self.client.post(
            '/showSummary',
            {'email': "tom@aarprin.es"},
            catch_response=True
        ) as response:
            if "Welcome, tom@aarprin.es" not in response.text:
                response.failure("Not a valid email")

    @task
    def book(self):
        competition = "Summer Vibe"
        club = "Arrhes Prince"
        self.client.get(f'/book/{competition}/{club}')

    @task
    def purchasePlaces(self):
        self.client.post(
            '/purchasePlaces',
            {
                'competition': 'Summer Vibe',
                'club': 'Arrhes Prince',
                'places': '1'
            }
        )

    @task
    def pointsDisplay(self):
        club = "Arrhes Prince"
        self.client.get(f'/pointsDisplay/{club}')

    @task
    def logout(self):
        self.client.get('/logout')
