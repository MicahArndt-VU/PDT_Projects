from dagster_aws.s3 import (
    s3_resource,
    s3_pickle_io_manager,
    s3_file_manager,
    # s3_partitioned_parquet_io_manager,
)
from dagster import (
    local_file_manager,
    EnvVar, FilesystemIOManager,
)
import os


GROUP_RESOURCES_PROD = {
    "io_manager": s3_pickle_io_manager.configured(
        {
            "s3_bucket": "s3-d07dagster01-dagster-k8s-test-02",
            "s3_prefix": "pyviz",
        }
    ),
    "s3": s3_resource.configured(
        {
            "endpoint_url": "https://s3.redchimney.com:443",
            "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID_PROD"),
            "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY_PROD"),
        }
    ),
    "file_manager": s3_file_manager.configured(
        {
            "s3_bucket": "s3-d07dagster01-dagster-k8s-test-02",
            "endpoint_url": "https://s3.redchimney.com:443",
            "max_attempts": 3,
        }
    ),
    # "parquet_io_manager": s3_partitioned_parquet_io_manager,
}

GROUP_RESOURCES_UAT = {
    "io_manager": s3_pickle_io_manager.configured(
        {
            "s3_bucket": "s3-u07dagster01-dagster-k8s-test-02",
            "s3_prefix": "pyviz",
        }
    ),
    "s3": s3_resource.configured(
        {
            "endpoint_url": "https://s3.redchimney.com:443",
            "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID_UAT"),
            "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY_UAT"),
        }
    ),
    "file_manager": s3_file_manager.configured(
        {
            "endpoint_url": "https://s3.redchimney.com:443",
            "s3_bucket": "s3-d07dagster01-dagster-k8s-test-02",
            "max_attempts": 3,
        }
    ),
}

GROUP_RESOURCES_DEV = {
    "io_manager": s3_pickle_io_manager.configured(
        {
            "s3_bucket": "s3-d07dagster01-dagster-k8s-test-02",
            "s3_prefix": "pyviz",
        }
    ),
    "s3": s3_resource.configured(
        {
            "endpoint_url": "https://s3.redchimney.com:443",
            "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID_DEV"),
            "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY_DEV"),
        }
    ),
    "file_manager": s3_file_manager.configured(
        {
            "endpoint_url": "https://s3.redchimney.com:443",
            "s3_bucket": "s3-d07dagster01-dagster-k8s-test-02",
            "max_attempts": 3,
        }
    ),
}

# can supply base_dir to both io_manager and file_manager if you have a specific path that you'd like to use locally
# otherwise it defaults to a temporary folder location 
GROUP_RESOURCES_LOCAL = {
    "io_manager": FilesystemIOManager(),
    "s3": s3_resource.configured(
        {
            "endpoint_url": "https://s3.redchimney.com:443",
            # "aws_access_key_id": "UJZE7R80THX4XZNB1YJD",
            "aws_access_key_id": {"env": "AWS_ACCESS_KEY_ID"},
            # "aws_secret_access_key": "/LcZ9clML3m/TRXMcHkqiDwRp+o54si9m6la8i65",
            "aws_secret_access_key": {"env": "AWS_SECRET_ACCESS_KEY"},
        }
    ),
    "file_manager": local_file_manager.configured({"base_dir": r"C:\temp"}),
        # {
        #   "base_dir": "C:\\dagster\\dagster-storage"
        # }
    # ),
}