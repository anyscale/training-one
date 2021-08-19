## Scaling topics
# You put functions and Actors into Anyscale to scale them!
# Some things are automatic, and some merely easy if you know how.

import ray
import time
ray.init(address="auto", namespace="scaling")

## Provisioning
#This example pre-provisions a cluster.  Autoscaling is a slow-reacting
# process.  If you need a lot of machines fast, this technique helped

import ray.autoscaler.sdk
INIT_CPUS=50
tot_cpus = ray.cluster_resources()["CPU"]
if tot_cpus < INIT_CPUS:
    ray.autoscaler.sdk.request_resources(num_cpus=INIT_CPUS)
    # this kind of loop was required when CPU count was in the 1000s
    while tot_cpus < INIT_CPUS:
        print(f"Total CPUs so far: {tot_cpus}")
        # wait some amount of time for machines to come up
        time.sleep(15)
        tot_cpus = ray.cluster_resources()["CPU"]

# When you're ready, scale that cluster back down again.
ray.autoscaler.sdk.request_resources(num_cpus=8)

