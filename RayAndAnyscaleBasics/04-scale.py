## Scaling topics
# You put functions and Actors into Anyscale to scale them!
# Some things are automatic, and some merely easy if you know how.

import ray
import time
import math
import random
import pandas as pd
ray.init(address="auto", namespace="scaling", runtime_env={"pip":"requirements.txt"})

## Monte Carlo
# This simulation is useful because it gives you an opportunity to see how to scale 
# loads

@ray.remote
def random_batch(batch_size):

    total_in = 0
    for i in range(batch_size):
        x,y = random.uniform(-1,1), random.uniform(-1,1)
        if (math.hypot(x,y) <= 1):
            total_in += 1
    return total_in

@ray.remote
class PiApproximator():
    def __init__(self):
        self.approximations = []
    def approximate(self, num_samples, batch_size):
        start = time.time()
        num_inside = []
        for i in range(0, num_samples, batch_size):
            num_inside.append(random_batch.remote(batch_size))
        pi = (4 * sum(ray.get(num_inside)) / num_samples )
        end = time.time()
        self.approximations.append({ "time":end - start,
            "num_samples":num_samples,
            "batch_size":batch_size,
            "pi":pi})
        return pi
    def get_approximations(self):
        return pd.DataFrame(self.approximations)

#ray.kill(ray.get_actor("approximator"))
approximator = PiApproximator.options(name="approximator").remote()
ray.get(approximator.approximate.remote(100, 1))
ray.get(approximator.approximate.remote(1000, 1))
ray.get(approximator.approximate.remote(1000, 10))
ray.get(approximator.approximate.remote(1000, 100))
ray.get(approximator.get_approximations.remote())

# use these numbers to start talking about efficiency
#for x in range(5):
    #ray.get([approximator.approximate.remote(i*100000,10000) for i in range(1,20)])
df = ray.get(approximator.get_approximations.remote())
df.plot("num_samples","pi", kind="scatter")
df.plot("num_samples", "time")



## Provisioning
#This example pre-provisions a cluster.  Autoscaling is a slow-reacting
# process.  If you need a lot of machines fast, this technique helped

import ray.autoscaler.sdk
INIT_CPUS=40
tot_cpus = ray.cluster_resources()["CPU"]
if tot_cpus < INIT_CPUS:
    ray.autoscaler.sdk.request_resources(num_cpus=INIT_CPUS)
    # this kind of loop was required when CPU count was in the 1000s
    while tot_cpus < INIT_CPUS:
        print(f"Total CPUs so far: {tot_cpus}")
        # wait some amount of time for machines to come up
        time.sleep(15)
        tot_cpus = ray.cluster_resources()["CPU"]

## When you're ready, scale that cluster back down again.
ray.autoscaler.sdk.request_resources(num_cpus=8)


## Ray Serve
# Ray serve is a library for scaffolding highly parallel endpoints.
# Since it's integrated with the Ray framework, it's suitable for creating
# self-contained APIs for model inference.

import ray
from ray import serve
from io import BytesIO
from PIL import Image
import requests
from fastapi import FastAPI, Request
BACKEND = "resnet18:v0"
app = FastAPI()

@serve.deployment(name="predictor", route_prefix="/")
@serve.ingress(app)
class ImageModel:
    def __init__(self):
        self.model = resnet18(pretrained=True).eval()
        self.preprocessor = transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Lambda(lambda t: t[:3, ...]),  # remove alpha channel
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    @app.post("/image_predict")
    async def predict(self, request : Request):
        image_payload_bytes = await request.body()
        pil_image = Image.open(BytesIO(image_payload_bytes))
        print("[1/3] Parsed image data: {}".format(pil_image))

        pil_images = [pil_image]  # Our current batch size is one
        input_tensor = torch.cat(
            [self.preprocessor(i).unsqueeze(0) for i in pil_images])
        print("[2/3] Images transformed, tensor shape {}".format(
            input_tensor.shape))

        with torch.no_grad():
            output_tensor = self.model(input_tensor)
        print("[3/3] Inference done!")
        return {"class_index": int(torch.argmax(output_tensor[0]))}


## Start Serve and use it

serve.start(detached=True)

#set up actor with 1 replicas
ImageModel.options(num_replicas=1)
# change the above line to '10' and see RPS go up
ImageModel.deploy()
    

