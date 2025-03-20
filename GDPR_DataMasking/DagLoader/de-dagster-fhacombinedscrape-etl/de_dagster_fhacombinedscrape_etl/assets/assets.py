from dagster import asset, Config

from . import metadata_dictionary as asset_metadata
import pandas as pd
import polars as pl
import os
import sqlalchemy
from sqlalchemy import text
from urllib.parse import quote_plus
import datetime
from . import fakeDataSuite as fds
from . import SnowflakeConnectionHandler as sh

# Upgrade to 1.9.x coming soon
# Dagster 1.8.13 Upgrade 1/17/2025

# Bump for poetry fix

@asset(metadata=asset_metadata,
    key_prefix=os.getenv('DAGSTER_DEPLOYMENT'),
    )
def load_fake_data(context):
    snow_acct = 'SNOWFLAKE_ACCT'
    snow_user = 'SNOWFLAKE_USER'
    snow_pw = 'SNOWFLAKE_PW'
    role = 'SYSADMIN'
    snow_db = 'DATABASE_NAME'
    snow_schema = 'LANDING'
    snow_wh = 'WAREHOUSE'
    try:
        snow_session = sh.create_session_object(snow_acct, snow_user, snow_pw, role, snow_wh, snow_db, snow_schema)

        # Generate fake data
        df = fds.generate_fake_df()
        sh.write_df_to_snowflake(df, 'fake_data', snow_session)
        snow_session.close()
        context.log.info("Fake Data Upload is now complete.")

    except Exception as e:
        raise e