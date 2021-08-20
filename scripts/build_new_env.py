import anyscale
import os
import ray
import time

VERSION=f"0.0.1-{time.time()}"

from anyscale import AnyscaleSDK
from anyscale.sdk.anyscale_client.models.create_cluster_environment import (
    CreateClusterEnvironment,
    )



sdk = AnyscaleSDK(os.environ["ANYSCALE_CLI_TOKEN"])
PROJECT_NAME="RayAndAnyscaleBasics"
# This project is in the Customer Organization
PROJECT_ID = "prj_rwzCbneuBN9Ys5k9PDj4KbHY"
# Created by hand in the Customer environment
APT_ID = "apt_u67hgnSqWNujfLV3pvJBAiTz"

create_cluster_environment = CreateClusterEnvironment(
    name="training-environment",
    config_json={'base_image': 'anyscale/ray:1.5.2-py37',
            'debian_packages': None,
            'env_vars': {},
            'post_build_cmds': [f'cd /home/ray && echo "{VERSION}" >> version && git init && git remote add origin https://github.com/anyscale/training-one.git && git pull origin main',
                                'cd /home/ray && git log | head -1 > git_commit.txt'],
            'python': {'conda_packages': None,
                       'pip_packages': ["jupytext", "matplotlib"]}
            }
    )


print("OK, building a new cluster environment")
build = sdk.build_cluster_environment(create_cluster_environment)

if (build.status == 'succeeded'):
    print(f"Your build is ready {build.id}")
    with open("build_id.txt", "w") as f:
        f.write(build.id)
else:
    print("Something happened...")
    print(build)
