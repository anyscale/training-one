from app.computation import remote_one
import ray
import time


def test_remote():
    print("Running test on remote cluster")
    ts = time.time()
    ray.init(f"anyscale://ci-test-cluster-{ts}", cluster_env="my-dd-env", cluster_compute="training-compute-1", project_dir=".", namespace="ns")
    assert ray.get(remote_one.remote(22)) == 23

# TODO get out reports / logs from distributed tests

