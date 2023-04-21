import boto3
import botocore

SESSION_CONFIG = botocore.config.Config(
    user_agent="aws-sdk-android/2.13.1 Linux/5.4.61-android11 Dalvik/2.1.0/0 en_US"
)


# TODO: Convert this to use os.environ vars?
class AWSClient:

    def __init__(self, pool_id: str, region_name='us-east-1'):
        # boto3.set_stream_logger('', logging.DEBUG)

        self.region_name = region_name
        self.cognito = boto3.client('cognito-identity', region_name=self.region_name)
        if pool_id:
            self.auth(pool_id)

    def auth(self, pool_id):
        ident_resp = self.cognito.get_id(IdentityPoolId=pool_id)
        cred_resp = self.cognito.get_credentials_for_identity(IdentityId=ident_resp['IdentityId'])
        self.credentials = cred_resp['Credentials']
