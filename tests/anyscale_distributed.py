from app.computation import remote_one
import ray

ray.init("anyscale://test-cluster")

def test_remote():
    assert ray.get(remote_one.remote(22)) == 23

