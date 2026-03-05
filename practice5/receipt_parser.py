import re
import json

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

prices = re.findall(r"\d+,\d{2}", text)
costs = [float(p.replace(",", ".")) for p in prices]

products = re.findall(r"\d+\.\s*(.+)", text)

date_match = re.search(r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}", text)
datetime = date_match.group() if date_match else None

payment_match = re.search(r"(Банковская карта|Наличные)", text)
payment_method = payment_match.group() if payment_match else None

total = sum(costs)

result = {
    "products": products,
    "prices": costs,
    "total": total,
    "datetime": datetime,
    "payment_method": payment_method
}

print(json.dumps(result, indent=4, ensure_ascii=False))