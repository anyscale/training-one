## Welcome to Ray Basics.  
# Let's import and connect to ray:


# Imports
import ray
import time
ray.init(address="auto")

## Remote invocation
# The fundamental pattern in Ray.

# Here is a remote task.
@ray.remote
def my_remote_task():
    print("Starting a task")
    time.sleep(2)
    print("Finishing a task")
    return "Finished a task"

# Here is how to invoke it and retrieve its results
ray.get(my_remote_task.remote())

# Remote invocation and blocking
# Think of how to distribute remote invocation and blocking returns.

obj_ref = my_remote_task.remote()

print(f"An object reference: {obj_ref}")

result = ray.get(obj_ref)

print(f"The result: {result}")

## The most common error
# Pay attention to types in your error messages.  
# Sometimes you will find you have an object ref
# instead of what you're looking for, which is the output of ray.get(obj_ref)

# calling a remote function directly ERROR
my_remote_task()

# adding refs ERROR
obj_ref + obj_ref


## Repeating tasks

def a_func(i):
    time.sleep(0.1)
    return f"The square of {i} is {i*i}"

# this is the same as annotating...
remote_func = ray.remote(a_func)

# this is slow
for i in range(100):
    print(a_func(i))

# how about this:
for i in range(100):
    print(remote_func.remote(i))

for i in range(100):
    print(ray.get(remote_func.remote(i)))


## BEST PRACTICE ONE -- delay ray.get()

refs = []
for i in range(100):
    refs.append(remote_func.remote(i))

print(refs)

print(ray.get(refs))

nothing = [print(ray.get(r)) for r in refs]

## BEST PRACTICE TWO -- backpressure
# https://docs.ray.io/en/master/ray-design-patterns/limit-tasks.html

@ray.remote(num_cpus=0.1)
def n_rands(n):
    """
    Generate a list of n random numbers. Gets more expensive as n increases
    """
    import random
    return [random.uniform(0,1) for x in range(n)]

arguments = range(10000)
BATCH_SIZE = 8
result_refs = []
for i in arguments:

    if len(result_refs) > BATCH_SIZE:
        print(f"batching {BATCH_SIZE}")
        num_ready = i-BATCH_SIZE
        ray.wait(result_refs, num_returns=num_ready)

    print(f"appending results {i}")
    result_refs.append(n_rands.remote(i))


## PATTERN Tree of tasks
# https://docs.ray.io/en/master/ray-design-patterns/tree-of-tasks.html

def partition(collection):
    # Use the last element as the first pivot
    pivot = collection.pop()
    greater, lesser = [], []
    for element in collection:
        if element > pivot:
            greater.append(element)
        else:
           lesser.append(element)
    return lesser, pivot, greater

def quick_sort(collection):
    if len(collection) <= 200000:  # magic number
        return sorted(collection)
    else:
        lesser, pivot, greater = partition(collection)
        lesser = quick_sort(lesser)
        greater = quick_sort(greater)
        return lesser + [pivot] + greater

@ray.remote(num_cpus=0.2)
def quick_sort_distributed(collection):
    if len(collection) <= 200000:  # magic number
        return sorted(collection)
    else:
        lesser, pivot, greater = partition(collection)
        lesser = quick_sort_distributed.remote(lesser)
        greater = quick_sort_distributed.remote(greater)
        return ray.get(lesser) + [pivot] + ray.get(greater)

@ray.remote
def driver():
    BIG_LIST = 1_000_000
    from numpy import random
    import time
    unsorted = random.randint(1000000, size=(BIG_LIST)).tolist()
    s = time.time()
    quick_sort(unsorted)
    print("Sequential execution: " + str(time.time() - s))
    s = time.time()
    ray.get(quick_sort_distributed.remote(unsorted))
    print("Distributed execution: " + str(time.time() - s))

if __name__ == "__main__":
    ray.get(driver.remote())



