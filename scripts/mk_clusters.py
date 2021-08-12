import anyscale

cluster_names = [f"class-one-{i}" for i in range(3)]

PROJECT_ID = prj_bYLM4Aj5fuBDSSEqTYWQUvvx

sdk = AnyscaleSDK(os.environ["ANYSCALE_CLI_TOKEN"])

from anyscale import AnyscaleSDK
from anyscale.sdk.anyscale_client.models.create_cluster_environment import (
    CreateClusterEnvironment,
   )

requirements = list(pkutils.parse_requirements('requirements.txt'))
cluster = sdk.launch_cluster_with_new_cluster_environment(
        project_id=PROJECT_ID,
        cluster_name=cluster_name,
        build_id=build_id,
        cluster_compute_id="cpt_H4SfGXXZ64rNpbEBcNNq9hNU",
        )
post_build_commands = []
