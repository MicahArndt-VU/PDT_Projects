import os
from . import assets
from dagster import (
    Definitions,
    ScheduleDefinition,
    load_assets_from_package_module,
    define_asset_job,
    AssetSelection,
    RunConfig,
)

from . import de_group_resources as group_resources
from . import project_resources as project_resources

# Merges the dictionaries containing resources from de_group_resources and project_resources
# Group resources with the same key will be overwritten by the project resources version
resources_by_deployment_name = {
    "prod": project_resources.PROJECT_RESOURCES_PROD | group_resources.GROUP_RESOURCES_PROD,
    "uat": project_resources.PROJECT_RESOURCES_UAT | group_resources.GROUP_RESOURCES_UAT,
    "dev": project_resources.PROJECT_RESOURCES_DEV | group_resources.GROUP_RESOURCES_DEV,
    "local": project_resources.PROJECT_RESOURCES_LOCAL | group_resources.GROUP_RESOURCES_LOCAL
}

# team_name = os.environ.get("TEAM_NAME", "team_name_unspecified")
deployment_name = os.environ.get("DAGSTER_DEPLOYMENT", "local")


job = define_asset_job(name="Snowflake_DataFaker",
                       selection=AssetSelection.all(),
                       )

defs = Definitions(
    assets=load_assets_from_package_module(assets),
    jobs=[job],
    schedules=[
        ScheduleDefinition(job=job, cron_schedule="17 10 * * *"),
    ],
)
