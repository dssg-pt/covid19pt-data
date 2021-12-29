import sys
from datetime import date
from datetime import timedelta

today = date.today()

offset = (today.weekday() - 4) % 7
if len(sys.argv) > 1:
    offset += int(sys.argv[1])

format = "%Y-%m-%d" 
if len(sys.argv) > 2:
    format = "%d-%m-%Y" # sys.argv[2]

last_wednesday = today - timedelta(days=offset)
print(last_wednesday.strftime(format))
