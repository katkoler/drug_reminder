import datetime
import time

print(datetime.datetime.now())

time1 = datetime.datetime.now()
time.sleep(2)

time2 = datetime.datetime.now()

print(time2)

print(time1>time2)

date = datetime.datetime(2018, 3, 11, 12, 30, 50)
delta = datetime.timedelta(0,0,0,0,1,0)

extra = date + delta

print(delta)
print(date)

print(extra)

print(time1>date)