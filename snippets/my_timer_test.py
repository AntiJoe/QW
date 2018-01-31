import time
from datetime import datetime, timedelta

cycle = 5
dt = datetime.now()
ft = dt + timedelta(seconds=cycle)
end_time = dt + timedelta(seconds=20)

print("now:        {}".format(dt.strftime('%Y-%m-%d %H:%M:%S')))
print("timer ends: {}".format(ft.strftime('%Y-%m-%d %H:%M:%S')))
print("end time:   {}".format(end_time.strftime('%Y-%m-%d %H:%M:%S')))


while datetime.now() < end_time:
    cycle_count = cycle
    while datetime.now() < ft:
        time.sleep(1)
        print('.', end='', flush=True)
        print("countdown: {}".format(cycle_count))
        cycle_count -= 1

    print(" timer reached {}".format(ft.strftime('%Y-%m-%d %H:%M:%S')))
    ft = datetime.now() + timedelta(seconds=cycle)

print("end time reached")
