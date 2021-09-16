## Ray Serve
import ray
from ray import serve
import time
import anyscale

import requests
from fastapi import FastAPI, Request

##
app = FastAPI()

@serve.deployment(name="serve_demo", route_prefix="/")
@serve.ingress(app)
class DemoModel:
    def __init__(self):
        print("Initializing endpoint")

    @app.post("/post")
    async def predict(self, request : Request):
        payload = await request.body()
        time.sleep(2)
        print("Done!")
        return {"class_index": 501}

    @app.get("/get_something")
    async def predict(self, request : Request):
        time.sleep(2)
        print("Done Get!")
        return {"class_index": 101}


if __name__ == "__main__":
    print("Running!")

    # start up session or connect to existing one
    ray.init("anyscale://ci-test-cluster", cluster_env="my-dd-env", cluster_compute="training-compute-1", project_dir=".", namespace="ns")
    serve.start(detached=True)

    #set up actor with 3 replicas
    DemoModel.options(num_replicas=3)
    # change the above line to '10' and see RPS go up
    DemoModel.deploy()
    

## Go look at dashboards
# 
URL = "https://session-7wmfe6bjx8bvrqhy2clfzg5v.i.anyscaleuserdata.com"
resp = requests.get(f"{URL}/serve/get_something", cookies={'anyscale-token': '7e7e8227-02c1-4b23-9015-d7ca530014ae'}).text
