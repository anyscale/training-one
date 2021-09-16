# the computation module, with local function and ray function
import ray

def comp_one(i):
    return i + 1

@ray.remote
def remote_one(i):
    return i + 1

if __name__ == "__main__":
    print(f"Calling as main function {ray.get(remote_one.remote(1234))}")
