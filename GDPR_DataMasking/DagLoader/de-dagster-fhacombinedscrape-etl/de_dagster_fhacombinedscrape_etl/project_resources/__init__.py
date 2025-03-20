# Configure project specific resources in this package (preferably each in it's own python file,
# then import them in the __init__.py file (this file).
from dagster import (
    local_file_manager,
    EnvVar, FilesystemIOManager,
)
from dagster_aws.s3 import (
    s3_pickle_io_manager,
    s3_file_manager,
    s3_resource,
)
import os


PROJECT_RESOURCES_PROD = {
    # add project specific PROD resources here
}

PROJECT_RESOURCES_UAT = {
    # add project specific UAT resources here
}

PROJECT_RESOURCES_DEV = {
    # add project specific DEV resources here
}

PROJECT_RESOURCES_LOCAL = {
    # add project specific LOCAL resources here
}


import os
import subprocess
from dagster import resource, InitResourceContext
import requests  # Assuming Thycotic secrets can be fetched via HTTP API
import json


@resource(config_schema={"secret_id": int, "thycotic_url":str, "thycotic_token_url":str, "thycotic_user":str, "thycotic_password":str})
def thycotic_secret_resource(context: InitResourceContext):
    secret_id = context.resource_config['secret_id']
    thycotic_url = context.resource_config['thycotic_url']
    thycotic_token_url = context.resource_config['thycotic_token_url']
    thycotic_token = ''

    # Fetch the Thycotic token using the provided credentials
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "grant_type": "password",
        "domain": "VUHL",
        "username": context.resource_config["thycotic_user"],
        "password": context.resource_config["thycotic_password"],
    }
    response = requests.post(
        thycotic_token_url, data=body, headers=headers, verify=False
    )
    context.log.info(json.loads(response.content)["access_token"])
    if response.status_code == 200:
        thycotic_token = json.loads(response.content)["access_token"]
    else:
        raise Exception(
            "Error retrieving Secret Token. %s %s" % (response.status_code, response)
        )
    context.log.info(f"{thycotic_url}/secrets/{secret_id}")
    try:
        # Fetch the secret from Thycotic using an HTTP GET request
        response = requests.get(
            f"{thycotic_url}/secrets/{secret_id}",
            headers={"Authorization": f"Bearer {thycotic_token}"},
            verify=False
        )
        response.raise_for_status()
        secret_data = response.json()
        # May need to change this
        service_account_name = secret_data["items"][1]["itemValue"]
        service_account_password = secret_data["items"][2]["itemValue"]

        if not service_account_name or not service_account_password:
            raise ValueError("Missing service account name or password in the secret data.")

        context.log.info(f"Retrieved service account credentials from Thycotic for account: {service_account_name}")
        return {
            'service_account_name': service_account_name,
            'service_account_password': service_account_password,
        }

    except requests.RequestException as e:
        context.log.error(f"Failed to fetch secrets from Thycotic: {e}")
        raise e


@resource(
    required_resource_keys={"thycotic_secret_resource"},
    config_schema={"keytab_file_path": str, "krb5ccname": str},
)
def kerberos_auth_resource(context: InitResourceContext):
    secrets = context.resources.thycotic_secret_resource
    service_account_name = secrets['service_account_name']
    service_account_password = secrets['service_account_password']
    keytab_file_path = context.resource_config.get('keytab_file_path',
                                                   '/tmp/krb5.keytab')
    # Set the KRB5CCNAME environment variable to manage Kerberos tickets
    # os.environ['KRB5CCNAME'] = context.resource_config.get('krb5ccname',
    #                                                       '/tmp/krb5cc_default')
    # os.environ['KERBEROS_CACHE_FILE'] = '/tmp/krb_ccache/krb5_cc'
    os.environ['KRB5_KTNAME'] = '/etc/krb5/krb5.keytab'

    os.environ["SVC_ACCT_USERNAME"] = service_account_name + "@VUHL.ROOT.MRC.LOCAL"
    os.environ["SVC_ACCT_PASSWORD"] = service_account_password

    context.log.info("Account Name: " + os.environ["SVC_ACCT_USERNAME"])
    # Write service account credentials to a temporary keytab file
    try:
        # Use ktutil or a similar tool to create a keytab
        subprocess.run('./entrypoint.sh', shell=True)

        context.log.info(f"Keytab created successfully at {keytab_file_path}")

    except Exception as e:
        context.log.error(f"Failed to create keytab file: {e}")
        raise e





    return {'principal': service_account_name}

import pyodbc
import sqlalchemy
from urllib.parse import quote_plus
from dagster import resource

@resource(
    required_resource_keys={"kerberos_auth_resource"},
config_schema={"serverName": str, "databaseName": str}
)
def sql_server_resource(context):
    kerberos_auth = context.resources.kerberos_auth_resource
    server_name = context.resource_config["serverName"]
    database_name = context.resource_config["databaseName"]
    # SQL Server connection string using Kerberos authentication
    # UID is deprecated when using Trusted_Connection
    uid = kerberos_auth['principal']
    conn_str = quote_plus(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server_name},1433;"
        f"DATABASE={database_name};"
        "Integrated_Security=SSPI;"
    )

    try:
        connection = sqlalchemy.create_engine(
            f"mssql+pyodbc:///?odbc_connect={conn_str}",
            fast_executemany=False,
            pool_use_lifo=True,
        )
        print("SQL Server connection established successfully.")
    except Exception as e:
        print(f"Failed to connect to SQL Server: {e}")
        raise e

    return connection
