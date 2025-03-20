import json

from dagster import (
    AssetKey,
    DagsterEventType,
    EventRecordsFilter,
    RunRequest,
    SensorDefinition,
    sensor,
)


# This sensor will need to be customized to fit the asset you're using as a trigger
# It is meant to serve as an dim, not to be used as-is
# It's important to add the proper asset key and the triggered_by_table variable values
def asset_updated_sensor(context) -> list[RunRequest]:
    """Sensor that triggers a pipeline run when an asset is updated"""
    cursor_dict = json.loads(context.cursor) if context.cursor else {}
    table_dict = cursor_dict.get("triggered_by_table")
    events = context.instance.events_for_asset_key(
        asset_key=AssetKey("my_asset"),
        after_cursor=context.cursor,
        before_cursor=None,
        ascending=False,
        limit=1,
        event_type=DagsterEventType.ASSET_MATERIALIZATION,
        asset_partitions=None,
        partitions_filter=None,
        cursor_filter=EventRecordsFilter(
            event_type=DagsterEventType.ASSET_MATERIALIZATION,
            asset_key=AssetKey("my_asset"),
        ),
    )
    if events:
        last_event = events[0]
        context.update_cursor(last_event.cursor)
        return [RunRequest(run_key=last_event.run_id, run_config={})]
    else:
        return []
