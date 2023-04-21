import base64
import boto3
import uuid
import hashlib

from auraframes.aws.awsclient import AWSClient

BUCKET_KEY = 'images.senseapp.co'
# TODO: May want to redact the pool ids -- read them in through config?
UPLOAD_IDENTITY_POOL_ID = 'us-east-1:b92826c0-8274-43db-abff-136977c13598'
AWS_UPLOAD_PART_SIZE = 16384


def get_md5(data):
    return base64.b64encode(hashlib.md5(data).digest()).decode('utf-8')


class S3Client(AWSClient):
    s3_client = None

    def __init__(self, pool_id=None, region_name='us-east-1'):
        super().__init__(pool_id if pool_id else UPLOAD_IDENTITY_POOL_ID, region_name)

    def auth(self, pool_id):
        super().auth(pool_id)
        self.s3_client = boto3.client('s3', aws_access_key_id=self.credentials['AccessKeyId'],
                                      aws_secret_access_key=self.credentials['SecretKey'],
                                      aws_session_token=self.credentials['SessionToken'])

    def upload_file(self, data, extension):
        filename = f'{str(uuid.uuid4())}{extension}'
        self.s3_client.put_object(Body=data, Bucket=BUCKET_KEY, Key=filename)

        return filename, get_md5(data)

    def get_file(self, filename):
        return self.s3_client.head_object(Bucket=BUCKET_KEY, Key=filename)
