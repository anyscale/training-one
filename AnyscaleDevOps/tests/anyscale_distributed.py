from app.computation import remote_one
import ray


def test_remote():
    print("Running test on remote cluster")
    ray.init("anyscale://ci-test-cluster", cluster_env="my-dd-env", cluster_compute="training-compute-1" project_dir=".")
    assert ray.get(remote_one.remote(22)) == 23

# TODO get out reports / logs from distributed tests

