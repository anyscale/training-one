from app.computation import remote_one

import ray

# local connection for functional verification
# only suitable for small compute, esp with cloud resources.
ray.init()

def test_remote():
    assert ray.get(remote_one.remote(22)) == 23
