import anyscale
import os
import ray

from anyscale import AnyscaleSDK
from anyscale.sdk.anyscale_client.models.create_cluster_environment import (
    CreateClusterEnvironment,
    )



sdk = AnyscaleSDK(os.environ["ANYSCALE_CLI_TOKEN"])
PROJECT_NAME="RayAndAnyscaleBasics"
PROJECT_ID = "prj_BvJETqqBBBx4zXySjTL8EpRs"
APT_ID = "apt_WpyVHX5qi1tBQdLxu72d9Wrr"

create_cluster_environment = CreateClusterEnvironment(
    name="training-environment",
    config_json={'base_image': 'anyscale/ray:1.4.1-py37',
            'debian_packages': None,
            'env_vars': {},
            'post_build_cmds': ['cd /home/ray && echo "1.0.1" >> version && git init && git remote add origin https://github.com/anyscale/training-one.git && git pull origin main',
                                'cd /home/ray && make install',
                                'git log | head -1 > git_commit.txt'],
            'python': {'conda_packages': None,
                       'pip_packages': ["jupytext"]}
            }
    )

build = sdk.build_cluster_environment(create_cluster_environment)
print(build)

os.environ["BUILD_ID"]=build.result.id
