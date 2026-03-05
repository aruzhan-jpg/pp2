from datetime import datetime, timedelta, UTC

now = datetime.now()
print("Current date and time:", now)

utc_now = datetime.now(UTC)
print("Current UTC time:", utc_now)

specific_date = datetime(2026, 3, 1)
print("Specific date:", specific_date)

print("Formatted:", now.strftime("%Y-%m-%d"))

start = datetime(2026, 1, 1)
end = datetime(2026, 3, 1)

difference = end - start
print("Days difference:", difference.days)

future = now + timedelta(days=7)
print("Date after 7 days:", future)

#---------------------------------------

from datetime import datetime, timedelta

#ex1
# Subtract five days from current date
today = datetime.now()
five_days_ago = today - timedelta(days=5)

print("Today:", today)
print("Five days ago:", five_days_ago)


#ex2
# Print yesterday, today, tomorrow
today_date = datetime.now().date()

yesterday = today_date - timedelta(days=1)
tomorrow = today_date + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today_date)
print("Tomorrow:", tomorrow)


#ex3
# Drop microseconds from datetime
now = datetime.now()
without_microseconds = now.replace(microsecond=0)

print("Original:", now)
print("Without microseconds:", without_microseconds)


#ex4
# Calculate difference between two dates in seconds
date1 = datetime(2026, 2, 20, 10, 0, 0)
date2 = datetime(2026, 2, 25, 12, 30, 0)

difference = date2 - date1
seconds = difference.total_seconds()

print("Difference in seconds:", seconds)