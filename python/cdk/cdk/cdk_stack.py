from aws_cdk import (
    App,
    # Duration,
    RemovalPolicy,
    Stack,
    aws_s3 as s3,
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        bucket = s3.Bucket(self, "ikenticus",
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=RemovalPolicy.DESTROY,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL)

        #bucket = s3.Bucket(self, "ikenticus", {
        #    blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
        #    encryption: s3.BucketEncryption.S3_MANAGED,
        #    removalPolicy: cdk.RemovalPolicy.DESTROY,
        #})
