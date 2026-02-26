
# Working with dates and time

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

now = datetime.now()
print("Current date and time:", now)

utc_now = datetime.utcnow()
print("Current UTC time:", utc_now)

specific_date = datetime(2026, 3, 1)
print("Specific date:", specific_date)

specific_datetime = datetime(2025, 12, 31, 23, 59)
print("Specific date and time:", specific_datetime)

print("Formatted (YYYY-MM-DD):", now.strftime("%Y-%m-%d"))
print("Formatted (DD/MM/YYYY HH:MM):", now.strftime("%d/%m/%Y %H:%M"))

start = datetime(2026, 1, 1)
end = datetime(2026, 3, 1)

difference = end - start
print("Days difference:", difference.days)

future = now + timedelta(days=7)
print("Date after 7 days:", future)

almaty_time = datetime.now(ZoneInfo("Asia/Almaty"))
print("Almaty time:", almaty_time)

london_time = datetime.now(ZoneInfo("Europe/London"))
print("London time:", london_time)
