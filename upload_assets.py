#!/usr/bin/env python3
import boto3
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from lan_party_services.asset_paths import asset_file_paths

## Upload assets to S3 - only needed one time prior to deployment. Copyrighted assets are not included in this repo,
# so you will need to provide them to work, ie, Quake, Unreal Tournament, Total Annihilation, etc.
# Uploads files from the lan_party_services/asset_paths.py module

s3_client = boto3.client('s3')
bucket_name = 'cdk-hnb659fds-assets-145023128664-us-east-2'


def upload_file(file_path, prefix):
    full_path = os.path.join('lan_party_services', file_path)
    key = os.path.join(prefix, os.path.basename(file_path))
    print(f"Uploading {full_path} to s3://{bucket_name}/{key}...")
    s3_client.upload_file(full_path, bucket_name, key)
    print(f"Uploaded {full_path} to s3://{bucket_name}/{key}")


if __name__ == "__main__":
    print("Starting the upload process...")
    total_files = len(asset_file_paths)
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(upload_file, file_path, prefix) for file_path, prefix in asset_file_paths]
        for index, future in enumerate(as_completed(futures), start=1):
            try:
                future.result()
                print(f"Completed upload {index} of {total_files}")
            except Exception as e:
                print(f"Error uploading file {index}: {e}")
    print("Upload process completed.")
