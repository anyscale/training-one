## Scaling topics
# You put functions and Actors into Anyscale to scale them!
# Some things are automatic, and some merely easy if you know how.

import ray
import time
import math
import random
import pandas as pd
ray.init(address="auto", namespace="scaling")

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

for x in range(5):
    ray.get([approximator.approximate.remote(i*100000,10000) for i in range(1,20)])
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

## Tuning
# I really don't know what this code will do exactly, but we can work with it and see.

from ray import tune

def trainable(config):
    approximation = ray.get(
            approximator.approximate.remote(
                config["num_samples"],
                config["batch_size"])
            )
    score = approximation["pi"]
    tune.report(mean_loss = score)

config = {
        "num_samples" : tune.grid_search([x for x in range(10000,100000,10000)]),
        "batch_size" : tune.grid_search([10,100,1000,10000])
        }
tune.run(trainable, config=config)

