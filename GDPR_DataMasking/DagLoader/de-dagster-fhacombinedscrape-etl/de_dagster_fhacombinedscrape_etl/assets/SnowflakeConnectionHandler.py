from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col
def create_session_object(acct, user, pw, role, wh, db, schema):
    # Define the connection parameters
    connection_parameters = {
        "account": acct,
        "user": user,
        "password": pw,
        "role": role,
        "warehouse": wh,
        "database": db,
        "schema": schema
    }
    session = Session.builder.configs(connection_parameters).create()
    return session

def write_df_to_snowflake(df, dest_table, session):
    # Convert df to snowflake df
    session.sql("USE WAREHOUSE COMPUTE_WH").collect()
    snow_df = session.create_dataframe(df)
    snow_df.write.mode("append").save_as_table(dest_table, column_order="name")

