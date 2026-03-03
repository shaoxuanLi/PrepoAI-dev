# dataloader/s3_loader.py



from Base_model_Loader import BaseDataLoader
import boto3  #allows access to AWS services(Amazon Web Services) like S3, EC2, etc. through Python code
import json

class S3Loader(BaseDataLoader):

    def __init__(self, bucket, key):
        self.bucket = bucket
        self.key = key

    def load(self):
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=self.bucket, Key=self.key)
        return json.loads(obj['Body'].read())