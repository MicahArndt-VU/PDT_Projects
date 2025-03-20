import os

from dagster import SensorDefinition
from dagster_slack import make_slack_on_run_failure_sensor


def make_slack_on_failure_sensor(base_url: str) -> SensorDefinition:
    """Sensor that sends a Slack message when a pipeline run fails.
    Requires settings SLACK_DAGSTER_ETL_BOT_TOKEN and SLACK_DAGSTER_ETL_BOT_CHANNEL environment variables
    Environment should be DEV, UAT, PROD"""
    environ_upper = environment.upper()
    return make_slack_on_run_failure_sensor(
        channel=os.getenv(f"{os.getenv("DAGSTER_DEPLOYMENT")}_SLACK_DAGSTER_ETL_BOT_CHANNEL"),
        slack_token=os.getenv(f"{os.getenv("DAGSTER_DEPLOYMENT")}_SLACK_DAGSTER_ETL_BOT_TOKEN"),
        dagit_base_url=base_url,
    )
