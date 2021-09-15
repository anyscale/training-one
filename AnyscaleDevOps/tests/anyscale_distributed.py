from app.computation import remote_one
import ray


def test_remote():
    print("Running test on remote cluster")
    ray.init("anyscale://test-cluster", cluster_env="my-dd-env")
    assert ray.get(remote_one.remote(22)) == 23



# get out reports / logs from distributed tests

