import boto3
import os
import zipfile
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from botocore.config import Config
from lan_party_services.asset_paths import asset_file_paths
from typing import List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure boto3 client with increased max_pool_connections
config = Config(max_pool_connections=50)
s3_client = boto3.client('s3', config=config)

account_number = os.getenv('AWS_ACCOUNT_NUMBER')
bucket_name = f'cdk-hnb659fds-assets-{account_number}-us-east-2'


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


def zip_file(file_path: str) -> str:
    """
    Create a zip file for the given file path.

    :param file_path: The local path of the file to zip.
    :return: The path of the created zip file.
    """
    zip_path = f"{file_path}.zip"
    logging.info(f"Creating zip file for {file_path}")
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, os.path.basename(file_path))
        logging.info(f"Zip file created at {zip_path}")
    except Exception as e:
        logging.error(f"Failed to create zip file for {file_path}: {e}")
    return zip_path


def upload_file(file_path: str, prefix: str, messages: List[str]) -> None:
    """
    Upload a file to the S3 bucket if it does not already exist.

    :param file_path: The local path of the file to upload.
    :param prefix: The prefix to use for the file in the S3 bucket.
    :param messages: List to collect messages for printing later.
    """
    full_path = os.path.join('lan_party_services', file_path)
    if full_path.endswith('.zip'):
        zip_path = full_path
    else:
        zip_path = zip_file(full_path)
    key = os.path.join(prefix, os.path.basename(zip_path))
    if file_exists(bucket_name, key):
        messages.append(f"File s3://{bucket_name}/{key} already exists. Skipping upload.")
    else:
        messages.append(f"Uploading {zip_path} to s3://{bucket_name}/{key}...")
        s3_client.upload_file(zip_path, bucket_name, key)
        messages.append(f"Uploaded {zip_path} to s3://{bucket_name}/{key}")
    if not full_path.endswith('.zip'):
        os.remove(zip_path)


if __name__ == "__main__":
    print("Starting the upload process...")
    total_files: int = len(asset_file_paths)
    messages: List[str] = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(upload_file, file_path, prefix, messages) for file_path, prefix in asset_file_paths]
        for index, future in enumerate(as_completed(futures), start=1):
            try:
                future.result()
                messages.append(f"Completed upload {index} of {total_files}")
            except Exception as e:
                messages.append(f"Error uploading file {index}: {e}")
    print("\n".join(messages))
    print("Upload process completed.")
