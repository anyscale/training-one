## The Global Object Store
# is a component in the Ray cluster that acts like a distributed key/value
# database.  It holds references to remote results, but can also be manipulated
# directly to hold named datasets.

import ray
import boto3
import pandas as pd

## A Key/Value store

# This example loads a csv into the object store
s3 = boto3.client('s3')

bucket="anyscale-data"
key="imagenet/imagenet_2012_bounding_boxes.csv"
obj = s3.get_object(Bucket=bucket, Key=key)
df = pd.read_csv(obj['Body'], names=["filename","minx","maxx","miny","maxy"])

# Now that I have a data frame, I can store it in the object store.
# You can store any object that is serializable
df_ref = ray.put(df)
df_ref

# You can get the object just like the result of a remote invocation
df2 = ray.get(df_ref)

##
# Use objects for shared state that is expensive to load.


# pass a ref into a constructor - no copy reference
@ray.remote
class AFactory:
    def __init__(self, bb_ref):
        self.bounding_boxes = bb_ref

    def areas(self):
        print(self.bounding_boxes)
        df = self.bounding_boxes
        return abs((df['maxx'] - df['minx']) * (df['maxy'] - df['miny']))

@ray.remote
class BFactory:
    def __init__(self, bb_ref):
        self.bounding_boxes = bb_ref[0]

    def areas(self):
        print(self.bounding_boxes)
        df = ray.get(self.bounding_boxes)
        return abs((df['maxx'] - df['minx']) * (df['maxy'] - df['miny']))


a = AFactory.remote(df_ref)
areas = ray.get(a.areas.remote())

b = BFactory.remote([df_ref])
areas = ray.get(a.areas.remote())

