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

##


# specify a payload for creating a Cluster Environment
create_cluster_environment = CreateClusterEnvironment(
    name="my-environment",
    config_json={'base_image': 'anyscale/ray-ml:1.6.0-py38',
            'debian_packages': None,
            'env_vars': {"MY_ENV_VAR": "SET_TO_THIS_VALUE"},
            'post_build_cmds': [ f'echo {VERSION} >> version.txt' ],
            'python': { 'pip_packages': ["seaborn","jupytext", "matplotlib"]}
            }
    )


## Heres a trick to inject requirements in (say, read them from a filesystem or potry.lock file)
import pkutils
requirements = list(pkutils.parse_requirements('requirements.txt'))

create_cluster_environment = CreateClusterEnvironment(
    name="my-environment",
    config_json={'base_image': 'anyscale/ray-ml:1.6.0-py38',
            'debian_packages': None,
            'env_vars': {"MY_ENV_VAR": "SET_TO_THIS_VALUE"},
            'post_build_cmds': [ f'echo {VERSION} >> version.txt' ],
            'python': { 'pip_packages': requirements }
            }
    )


##

# this command blocks (use in scripting)
build = sdk.build_cluster_environment(create_cluster_environment)

# to get tricky, throw it in a remote
ray.init("anyscale://my-cluster?cluster_env=my-environment:1")
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

## Jobs


