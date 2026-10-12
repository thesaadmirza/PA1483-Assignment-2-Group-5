from locust import HttpUser, task


class Visitor(HttpUser):
    @task
    def index(self):
        with self.client.get("/", catch_response=True) as response:
            if response.status_code != 200 or response.text.count("<li>") != 20:
                response.failure("Unexpected response")
