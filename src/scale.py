import ray.autoscaler.sdk

INIT_CPUS=100
tot_cpus = ray.cluster_resources()["CPU"]

if tot_cpus < INIT_CPUS:
    ray.autoscaler.sdk.request_resources(num_cpus=INIT_CPUS)

    while tot_cpus < INIT_CPUS:
        print(f"Total CPUs so far: {tot_cpus}")
        time.sleep(90)
        tot_cpus = ray.cluster_resources()["CPU"]

