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
df2


## Data Wrapping
# Use objects for shared state that is expensive to load.

# 
@ray.remote
class DataWrapper:
    def __init__(self):
        import boto3
        s3 = boto3.client('s3')
        bucket="anyscale-data"
        key="imagenet/imagenet_2012_bounding_boxes.csv"
        obj = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(obj['Body'], names=["filename","minx","maxx","miny","maxy"])
        self.bounding_boxes = ray.put(df)

    def get_bb(self):
        return self.bounding_boxes

@ray.remote
class DataConsumer:
    def __init__(self, bb_ref):
        self.bounding_boxes = bb_ref

    def areas(self):
        df = ray.get(self.bounding_boxes)
        return abs((df['maxx'] - df['minx']) * (df['maxy'] - df['miny']))


# Make a singleton remote object to hold the data
a = DataWrapper.remote()
bb_ref = a.get_bb.remote()

# Pass it as argument to constructor
b = DataConsumer.remote(bb_ref)
areas = ray.get(b.areas.remote())
areas

