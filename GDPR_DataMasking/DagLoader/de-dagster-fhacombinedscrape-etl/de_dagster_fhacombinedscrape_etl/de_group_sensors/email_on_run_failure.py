from dagster import make_email_on_run_failure_sensor
import os

email_on_run_failure = make_email_on_run_failure_sensor(
    # TODO : Update email_from to a valid email address
    email_from=os.getenv("ALERT_EMAIL_FROM"),
    # email_password=os.getenv("ALERT_EMAIL_PASSWORD"),
    email_to=os.getenv("ALERT_EMAIL_TO"),
    smtp_host=os.getenv("ALERT_EMAIL_SMTP_HOST"),
    smtp_port=os.getenv("ALERT_EMAIL_SMTP_PORT"),
    smtp_type=os.getenv("ALERT_EMAIL_SMTP_TYPE"),
    email_body_fn=lambda context: f"""\
    Pipeline {context.pipeline_name} failed.
    Mode: {context.mode}
    Run ID: {context.run_id}
    Run page: {context.run.page_url}
    """,
    email_subject_fn=lambda context: f"""\
    Pipeline {context.pipeline_name} failed.
    """,
    # should not need to supply a password for current SMTP configuration
    email_password="",
)

