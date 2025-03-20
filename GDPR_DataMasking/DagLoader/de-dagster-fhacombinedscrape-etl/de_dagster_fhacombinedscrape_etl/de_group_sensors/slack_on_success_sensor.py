from dagster import (
    run_status_sensor,
    make_slack_on_success_sensor,
    DagsterRunStatus,
)
import os


def slack_on_success(context):
    """Sensor that sends a Slack message when a pipeline run succeeds,
    requires settings SLACK_DAGSTER_ETL_BOT_TOKEN and SLACK_DAGSTER_ETL_BOT_CHANNEL environment variables"""
    return make_slack_on_success_sensor(
        channel=os.getenv(f"{os.getenv("DAGSTER_DEPLOYMENT")}_SLACK_DAGSTER_ETL_BOT_CHANNEL"),
        slack_token=os.getenv(f"{os.getenv("DAGSTER_DEPLOYMENT")}_SLACK_DAGSTER_ETL_BOT_TOKEN"),
        dagit_base_url=context.solid_config["base_url"],
    )
