import time
from datetime import datetime, timedelta

dt = datetime.now()
ft = dt + timedelta(seconds=6)
end_time = dt + timedelta(seconds=30)

print(dt.strftime('%Y-%m-%d %H:%M:%S'))
print(ft.strftime('%Y-%m-%d %H:%M:%S'))
print(end_time.strftime('%Y-%m-%d %H:%M:%S'))

while datetime.now() < end_time:
    while datetime.now() < ft:
        time.sleep(0.5)
        print('.', end='', flush=True)

    print(" timer reached")
    ft = datetime.now() + timedelta(seconds=6)

print("end time reached")
