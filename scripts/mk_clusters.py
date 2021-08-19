import anyscale
import os
import sys
import ray
from anyscale.sdk.anyscale_client.sdk import AnyscaleSDK

ray.init(ignore_reinit_error=True)

cluster_names = [f"training-cluster-{i}" for i in range(3)]


from anyscale import AnyscaleSDK
from anyscale.sdk.anyscale_client.models.create_cluster_environment import (
    CreateClusterEnvironment,
   )

@ray.remote
def launch_cluster(cluster_name):
    # set this to your RayAndAnyscaleBasics project
    PROJECT_ID = "prj_BvJETqqBBBx4zXySjTL8EpRs"
    # set this to the ID of your training-suitbale cluster compute
    CPT_ID = "cpt_bLhHW48DcMLMPemCMdh9xjMQ"
    # read this buildid from a file
    BUILD_ID = ""
    with open("build_id.txt") as f:
        BUILD_ID = f.read().strip()

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
