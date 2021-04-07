from datetime import datetime
from pytz import timezone

nowTime = datetime.now(timezone('EST'))
def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return startTime <= nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime
    print(nowTime)
