from datetime import datetime, timedelta, timezone

import dateutil

from todos.models import Todo


def getStatus(todo: Todo):
    left_time = todo.deadline.astimezone(
        timezone.utc) - datetime.now(timezone.utc)

    if left_time < timedelta(seconds=0):
        return "EXPIRED"

    elif left_time > timedelta(seconds=0) and left_time < timedelta(days=1):
        return "ONE_DAY_LEFT"

    elif left_time > timedelta(days=1) and left_time < timedelta(days=7):
        return "ONE_WEEK_LEFT"

    else:
        return "MORE_THAN_ONE_WEEK_LEFT"
