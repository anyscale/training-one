## The Global Object Store
# is a component in the Ray cluster that acts like a distributed key/value
# database.  It holds references to remote results, but can also be manipulated
# directly to hold named datasets.

import ray
from ray import datasets

# This example loads a csv into the object store
with open("data.csv") a f:



