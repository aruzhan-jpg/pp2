import re
import json
import os

# open raw.txt from the same folder
path = os.path.join(os.path.dirname(__file__), "raw.txt")

with open(path, "r", encoding="utf-8") as file:
    text = file.read()

# find product names (lines starting with number)
products = re.findall(r"\d+\.\n(.+)", text)

# find prices
prices = re.findall(r"\n(\d{1,3}(?: \d{3})*,\d{2})\nСтоимость", text)

# convert prices to numbers
item_costs = [float(p.replace(" ", "").replace(",", ".")) for p in prices]

# calculate total
calculated_total = sum(item_costs)

# find official total
official_total = re.search(r"ИТОГО:\n([\d ]+,\d{2})", text)
if official_total:
    official_total = float(official_total.group(1).replace(" ", "").replace(",", "."))

# find date and time
datetime = re.search(r"Время: ([\d\.]+\s[\d:]+)", text)
if datetime:
    datetime = datetime.group(1)

# find payment method
payment = re.search(r"(Банковская карта)", text)
if payment:
    payment = payment.group(1)

# output result
result = {
    "products": products,
    "item_costs": item_costs,
    "calculated_total": calculated_total,
    "official_total": official_total,
    "datetime": datetime,
    "payment_method": payment
}

print(json.dumps(result, indent=4, ensure_ascii=False))