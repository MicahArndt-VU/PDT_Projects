import os
from dagster import (
    sensor,
    RunRequest,
    RunConfig,
    SkipReason, Any,
)
from dagster_aws.s3.sensor import get_s3_keys


@sensor(minimum_interval_seconds=30)
def s3_file_sensor(context) -> list[RunRequest | Any]:
    """Sensor that triggers a pipeline run when a file is uploaded to S3"""
    since_key = context.cursor or None
    new_s3_keys = get_s3_keys(bucket=os.getenv("S3_FILE_DROP_BUCKET"), since_key=since_key)
    if not new_s3_keys:
        return SkipReason("No new s3 files found for bucket my_s3_bucket.")
    last_key = new_s3_keys[-1]
    run_requests = [RunRequest(run_key=s3_key, run_config={}) for s3_key in new_s3_keys]
    context.update_cursor(last_key)
    return run_requests

