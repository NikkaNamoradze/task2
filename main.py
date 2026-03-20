import argparse
import json
import logging
from os import getenv

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def init_client():
    client = boto3.client(
        "s3",
        aws_access_key_id=getenv("aws_access_key_id"),
        aws_secret_access_key=getenv("aws_secret_access_key"),
        aws_session_token=getenv("aws_session_token"),
        region_name=getenv("aws_region_name"),
    )
    client.list_buckets()
    return client


def get_bucket_policy(client, bucket_name):
    try:
        response = client.get_bucket_policy(Bucket=bucket_name)
        return response["Policy"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchBucketPolicy":
            return None
        raise


def generate_public_read_policy(bucket_name):
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadDev",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/dev/*",
            },
            {
                "Sid": "PublicReadTest",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/test/*",
            },
        ],
    }
    return json.dumps(policy)


def remove_public_access_block(client, bucket_name):
    try:
        client.delete_public_access_block(Bucket=bucket_name)
        logger.info("Removed public access block for '%s'", bucket_name)
    except ClientError as e:
        logger.warning("Could not remove public access block: %s", e)


def create_bucket_policy(client, bucket_name):
    remove_public_access_block(client, bucket_name)
    policy = generate_public_read_policy(bucket_name)
    client.put_bucket_policy(Bucket=bucket_name, Policy=policy)
    return policy


def main():
    parser = argparse.ArgumentParser(
        description="Check/create S3 bucket policy for public read on /dev and /test prefixes."
    )
    parser.add_argument("bucket_name", help="Name of the S3 bucket")
    args = parser.parse_args()

    client = init_client()

    existing_policy = get_bucket_policy(client, args.bucket_name)

    if existing_policy:
        print(f"Bucket '{args.bucket_name}' already has a policy:")
        print(json.dumps(json.loads(existing_policy), indent=2))
    else:
        print(f"No policy found. Creating public read policy for /dev/* and /test/*...")
        policy = create_bucket_policy(client, args.bucket_name)
        print(f"Policy created successfully for '{args.bucket_name}':")
        print(json.dumps(json.loads(policy), indent=2))


if __name__ == "__main__":
    main()
