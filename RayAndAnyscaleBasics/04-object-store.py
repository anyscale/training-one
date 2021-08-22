## The Global Object Store
# is a component in the Ray cluster that acts like a distributed key/value
# database.  It holds references to remote results, but can also be manipulated
# directly to hold named datasets.

import ray
import boto3
import pandas as pd

# A Key/Value store

# This example loads a csv into the object store
s3 = boto3.client('s3')

bucket="anyscale-data"
key="nyc-taxi-train.csv"
obj = s3.get_object(Bucket=bucket, Key=key)
obj_ref = ray.put(obj['Body'].read())



