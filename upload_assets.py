import boto3
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from botocore.config import Config
from lan_party_services.asset_paths import asset_file_paths
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure boto3 client with increased max_pool_connections
config = Config(max_pool_connections=50)
s3_client = boto3.client('s3', config=config)

account_number = os.getenv('AWS_ACCOUNT_NUMBER')
bucket_name = f'grlanparty.info'
folder_key = 'assets/'


def folder_exists(bucket: str, key: str) -> bool:
    """
    Check if a folder exists in the S3 bucket.

    :param bucket: The name of the S3 bucket.
    :param key: The key (path) of the folder in the S3 bucket.
    :return: True if the folder exists, False otherwise.
    """
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except s3_client.exceptions.ClientError:
        return False


def create_folder(bucket: str, key: str) -> None:
    """
    Create a folder in the S3 bucket.

    :param bucket: The name of the S3 bucket.
    :param key: The key (path) of the folder in the S3 bucket.
    """
    s3_client.put_object(Bucket=bucket, Key=key)


def file_exists(bucket: str, key: str) -> bool:
    """
    Check if a file exists in the S3 bucket.

    :param bucket: The name of the S3 bucket.
    :param key: The key (path) of the file in the S3 bucket.
    :return: True if the file exists, False otherwise.
    """
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except s3_client.exceptions.ClientError:
        return False


def upload_file(file_path: str, prefix: str, messages: List[str]) -> None:
    """
    Upload a file to the S3 bucket if it does not already exist.

    :param file_path: The local path of the file to upload.
    :param prefix: The prefix to use for the file in the S3 bucket.
    :param messages: List to collect messages for printing later.
    """
    full_path = os.path.join('lan_party_services', file_path)
    key = os.path.join(prefix, os.path.basename(full_path))
    if file_exists(bucket_name, key):
        messages.append(f"File s3://{bucket_name}/{key} already exists. Skipping upload.")
    else:
        messages.append(f"Uploading {full_path} to s3://{bucket_name}/{key}...")
        s3_client.upload_file(full_path, bucket_name, key)
        messages.append(f"Uploaded {full_path} to s3://{bucket_name}/{key}")


if __name__ == "__main__":
    print("Starting the upload process...")
    if not folder_exists(bucket_name, folder_key):
        create_folder(bucket_name, folder_key)
        print(f"Created folder s3://{bucket_name}/{folder_key}")

    total_files: int = len(asset_file_paths)
    messages: List[str] = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(upload_file, file_path, folder_key, messages) for file_path, prefix in asset_file_paths]
        for index, future in enumerate(as_completed(futures), start=1):
            try:
                future.result()
                messages.append(f"Completed upload {index} of {total_files}")
            except Exception as e:
                messages.append(f"Error uploading file {index}: {e}")
    print("\n".join(messages))
    print("Upload process completed.")
