import datetime
import time

print(datetime.datetime.now())

time1 = datetime.datetime.now()
time.sleep(2)

time2 = datetime.datetime.now()

print(time2)

print(time1>time2)