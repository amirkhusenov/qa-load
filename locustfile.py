from queue import Queue, Empty

from locust import HttpUser, task, constant_pacing


latest_id = None
verified_ids = Queue()

class FirstUser(HttpUser):
    fixed_count = 30
    wait_time = constant_pacing(1)

    @task 
    def first_request(self):
        global latest_id

        response = self.client.get('/api/first', name='/api/first')

        latest_id = response.json()['id']

class SecondUser(HttpUser):
    fixed_count = 20
    wait_time = constant_pacing(1)
    
    @task
    def second_request(self):
        if latest_id is None:
            return

        response = self.client.get(
            "/api/second",
            params={"value": latest_id},
            name="/api/second"
        )

        if response.status_code == 200:
            verified_ids.put(latest_id)


class ThirdUser(HttpUser):
    fixed_count = 10
    wait_time = constant_pacing(1)

    @task
    def third_request(self):
        try:
            id_value = verified_ids.get(timeout=2)
        except Empty:
            return

        self.client.get(
            "/api/third",
            params={"value": id_value},
            name="/api/third"
        )