import json

from task_factory import task_factory
from task_engine import TaskEngine


def lambda_handler(event, context):
    print(json.dumps(event))

    tasks = list(map(task_factory, event.get("Records", [])))
    filtered_tasks = list(filter(None, tasks))
    TaskEngine(*filtered_tasks).run()
    return event
