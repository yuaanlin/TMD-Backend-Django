from datetime import datetime, timedelta, timezone

import dateutil


def getTimedeltaSec(todo):
    timedelta = datetime.now() - \
        dateutil.parser.parse(todo['ddl'])
    return timedelta.total_seconds()
