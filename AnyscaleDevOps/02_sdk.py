## Use the SDK

# The SDK is for programmatic manipulation of Anyscale's configurations.
# Use it in circumstances where you want to automate the creation of cluster environments, projects, or maybe clusters.
import anyscale
import os
import ray
import time
from datetime import date

VERSION=f"0.0.1-{time.time()}"

from anyscale import AnyscaleSDK
from anyscale.sdk.anyscale_client.models.create_cluster_environment import (
    CreateClusterEnvironment,
    )

## Initialize the SDK.
sdk = AnyscaleSDK(os.environ["ANYSCALE_CLI_TOKEN"])

## This key is for the DataDog API
DD_API_KEY=os.environ["DD_API_KEY"]

# This create_cluster_environment
# * gets requirements from a file
# * includes installation for DataDog agent
import pkutils
requirements = list(pkutils.parse_requirements('requirements.txt'))

create_cluster_environment = CreateClusterEnvironment(
    name="my-dd-env",
    config_json={'base_image': 'anyscale/ray-ml:1.6.0-py38',
            'debian_packages': None,
            'env_vars': {"MY_ENV_VAR": DD_API_KEY},
            'post_build_cmds': [ f'DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=$DD_API_KEY DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"',
                ],
            'python': { 'pip_packages': requirements }
            }
    )
##

# this command blocks (use in scripting)
#build = sdk.build_cluster_environment(create_cluster_environment)

# to get tricky, throw it in a remote
ray.init()
@ray.remote
def remote_build(create_cluster_environment):
    from anyscale import AnyscaleSDK
    sdk = AnyscaleSDK(os.environ["ANYSCALE_CLI_TOKEN"])
    build = sdk.build_cluster_environment(create_cluster_environment)
    return build

build_ref = remote_build.remote(create_cluster_environment)
build_ref

#
build = ray.get(build_ref)

## Clusters

# You may want to start clusters from the SDK.  This method provides control of configuration from the ops layer, while letting the client simply know the cluster name in order to use it ?

CPT_ID="cpt_bLhHW48DcMLMPemCMdh9xjMQ"
PROJECT_ID="prj_7rgb4YJrXvyCSmwyHYuVLBJm"

cluster_id = sdk.launch_cluster(
        project_id=PROJECT_ID,
        cluster_name="my_dd_cluster",
        cluster_environment_build_id=build.id,
        cluster_compute_id=CPT_ID,
        idle_timeout_minutes=10
        )
return cluster_id

## Jobs

from anyscale.sdk.anyscale_client.models.jobs_query import (
    JobsQuery,
    )
jobs = sdk.search_jobs(JobsQuery(project_id=PROJECT_ID))
jobs.results[0:1]

##
sdk.get_job("job_BCPRSYAbGbfLEykQqFMgSfxz")

