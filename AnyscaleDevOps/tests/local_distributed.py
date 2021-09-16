from app.computation import remote_one

import ray

# local connection for functional verification
# only suitable for small compute, esp with cloud resources.

def test_remote():
    print("Running test on local cluster")
    ray.init()
    assert ray.get(remote_one.remote(10)) == 11
