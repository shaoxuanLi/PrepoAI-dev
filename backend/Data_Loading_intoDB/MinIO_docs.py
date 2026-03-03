from minio import Minio          # pip install minio
from minio.error import S3Error
import io
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Overall_Pipeline import run_pipeline

class MinIOStorage:
    def __init__(self, endpoint="localhost:9000", access_key="your_access_key", 
                 secret_key="your_secret_key", secure=False):
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )

    def _ensure_bucket(self, bucket_name: str):
        """Create bucket if it doesn't exist"""
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
            print(f"Created bucket: {bucket_name}")

    def store_raw_file(self, file_path: str, bucket_name: str = "raw-files"):
        """Store original raw large files and images directly from path"""
        self._ensure_bucket(bucket_name)
        file_name = os.path.basename(file_path)
        self.client.fput_object(bucket_name, file_name, file_path)
        print(f"Stored raw file: {file_name} → bucket: {bucket_name}")

    def store_processed_data(self, bucket_name: str = "processed-data"):
        """Run pipeline and store processed data as JSON in MinIO"""
        self._ensure_bucket(bucket_name)

        # get processed data from pipeline
        processed_data = run_pipeline()

        # convert to JSON bytes
        data_bytes = json.dumps(processed_data, ensure_ascii=False, indent=2).encode("utf-8")
        data_stream = io.BytesIO(data_bytes)

        self.client.put_object(
            bucket_name,
            "processed_data.json",      # file name in bucket
            data_stream,
            length=len(data_bytes),
            content_type="application/json"
        )
        print(f"Stored processed data → bucket: {bucket_name}/processed_data.json")

    def store_export_result(self, export_data: dict, export_name: str, bucket_name: str = "export-results"):
        """Store final labelled export results"""
        self._ensure_bucket(bucket_name)

        data_bytes = json.dumps(export_data, ensure_ascii=False, indent=2).encode("utf-8")
        data_stream = io.BytesIO(data_bytes)

        self.client.put_object(
            bucket_name,
            export_name,
            data_stream,
            length=len(data_bytes),
            content_type="application/json"
        )
        print(f"Stored export result: {export_name} → bucket: {bucket_name}")


# Usage example
if __name__ == "__main__":
    minio = MinIOStorage(  
        endpoint="localhost:9000",
        access_key="your_access_key",
        secret_key="your_secret_key"
    )

    # 1. store raw file directly
    minio.store_raw_file("path/to/raw_file.csv", bucket_name="raw-files")

    # 2. run pipeline and store processed data
    minio.store_processed_data(bucket_name="processed-data")

    # 3. store export/labelled results
    minio.store_export_result(
        export_data={"task_id": 1, "labels": ["positive", "negative"]},
        export_name="export_task1.json",
        bucket_name="export-results"
    )