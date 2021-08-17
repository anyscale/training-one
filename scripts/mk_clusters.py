import anyscale
import os
import ray
from anyscale.sdk.anyscale_client.sdk import AnyscaleSDK

ray.init(ignore_reinit_error=True)

cluster_names = [f"class-one-{i}" for i in range(3)]


from anyscale import AnyscaleSDK
from anyscale.sdk.anyscale_client.models.create_cluster_environment import (
    CreateClusterEnvironment,
   )

@ray.remote
def launch_cluster(cluster_name):
    PROJECT_ID = "prj_BvJETqqBBBx4zXySjTL8EpRs"
    BUILD_ID = "bld_MCvQkDmrs7qx1Pt3TheEJXvH"
    CPT_ID = "cpt_bLhHW48DcMLMPemCMdh9xjMQ"

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
