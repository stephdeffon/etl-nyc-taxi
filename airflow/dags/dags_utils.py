# dags/utils.py
import logging

log = logging.getLogger(__name__)


def on_failure_callback(context):
    log.error(
        "Task '%s' failed — DAG: %s, date: %s, tentative: %s",
        context["task_instance"].task_id,
        context["dag"].dag_id,
        context["ds"],
        context["task_instance"].try_number,
    )
