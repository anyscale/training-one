import anyscale
import os
import sys
import ray
from anyscale.sdk.anyscale_client.sdk import AnyscaleSDK

ray.init(ignore_reinit_error=True)

students = os.environ["STUDENTS"].split(",")
cluster_names = [f"training-cluster-{i}" for i in students]


from anyscale import AnyscaleSDK
from anyscale.sdk.anyscale_client.models.create_cluster_environment import (
    CreateClusterEnvironment,
   )

# By using num_cpus < 0.1 I start up to 10x number of CPUs available
@ray.remote(num_cpus=0.1)
def launch_cluster(cluster_name):
    # set this to your RayAndAnyscaleBasics project
    PROJECT_ID = os.environ["PROJECT_ID"]
    # set this to the ID of your training-suitbale cluster compute
    CPT_ID = os.environ["CPT_ID"]
    # read this buildid from environment
    BUILD_ID = os.environ["BUILD_ID"]

    print(f"Using build id {BUILD_ID}")
    sdk = AnyscaleSDK(os.environ["ANYSCALE_CLI_TOKEN"])
    cluster_id = sdk.launch_cluster(
            project_id=PROJECT_ID,
            cluster_name=cluster_name,
            cluster_environment_build_id=BUILD_ID,
            cluster_compute_id=CPT_ID
            )
    return cluster_id

cluster_refs = [launch_cluster.remote(cluster_name) for cluster_name in cluster_names]

cluster_ids = ray.get(cluster_refs)
print(cluster_ids)
