from locust import HttpUser, task, between

class ServingUser(HttpUser):

    @task
    def post_job(self):
        response = self.client.post("/post", data={"a":"b"})
        print(response)

    def on_start(self):
        pass
