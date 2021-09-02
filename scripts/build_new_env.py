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



sdk = AnyscaleSDK(os.environ["ANYSCALE_CLI_TOKEN"])
# ENV file stores build id
ENV_FILE = os.environ["ENV_FILE"]

create_cluster_environment = CreateClusterEnvironment(
    name="training-environment",
    config_json={'base_image': 'anyscale/ray-ml:1.6.0-py38',
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
    with open(ENV_FILE, "a") as f:
        f.write(f"# updating BUILD_ID on {date.today()}\n")
        f.write(f"export BUILD_ID={build.id}\n")
else:
    print("Something happened...")
    print(build)
