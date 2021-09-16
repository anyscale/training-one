from locust import HttpUser, task, between

class ServingUser(HttpUser):

    @task
    def get_job(self):
        response = self.client.get("/get_something", cookies={'anyscale-token': '7e7e8227-02c1-4b23-9015-d7ca530014ae'})
        print(response)

    def on_start(self):
        pass
