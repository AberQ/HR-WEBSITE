from locust import HttpUser, task, between

class MyUser(HttpUser):
    host = "http://127.0.0.1:8000"  # Указание хоста, на котором работает сервер
    wait_time = between(1, 3)

    @task
    def get_tags(self):
        self.client.get("/api/tags/")  # Относительный путь
