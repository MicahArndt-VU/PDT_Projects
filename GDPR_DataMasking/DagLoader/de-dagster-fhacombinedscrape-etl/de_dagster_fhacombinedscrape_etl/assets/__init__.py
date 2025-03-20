import os
from typing import Any

from dagster import MetadataValue


# This will use an environment variable set in the code location servers to set the team name across all assets running
# in that container. Please don't hard code team names! Ownership changes and we don't want to have to recode anything
# to accommodate that.
team_name: str | Any = os.environ.get("TEAM_NAME", "team_name_unspecified")
metadata_dictionary = {
    'team': team_name,
    'developer': 'micah.arndt',
    'docs': MetadataValue.url('https://vuconfluence.atlassian.net/wiki/spaces/SS/pages/24590549085/Marketing+-+FHA+Loan+Data+Reports'),
}