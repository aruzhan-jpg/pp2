import re
import json
import os

# --- Read raw.txt file ---
base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, "raw.txt")

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Normalize line breaks (important for Windows)
text = text.replace('\r\n', '\n')

# --- 1. Extract product names ---
# Matches pattern:
# 1.
# Product name
products = re.findall(r'\d+\.\n(.+)', text)

# --- 2. Extract item costs ---
# Matches:
# Стоимость
# 308,00
cost_strings = re.findall(r'Стоимость\n([\d ]+,\d{2})', text)

# Convert price strings like "1 200,00" to float
def money_to_float(s):
    return float(s.replace(" ", "").replace(",", "."))

item_costs = [money_to_float(x) for x in cost_strings]

# --- 3. Calculate total sum ---
calculated_total = round(sum(item_costs), 2)

# --- 4. Extract official total from receipt ---
official_total = None
total_match = re.search(r'ИТОГО:\n([\d ]+,\d{2})', text)
if total_match:
    official_total = money_to_float(total_match.group(1))

# --- 5. Extract date and time ---
datetime_match = re.search(
    r'Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})',
    text
)
datetime = datetime_match.group(1) if datetime_match else None

# --- 6. Extract payment method ---
payment_match = re.search(r'Банковская карта', text)
payment_method = payment_match.group(0) if payment_match else None

# --- 7. Create structured JSON output ---
data = {
    "products": products,
    "item_costs": item_costs,
    "calculated_total": calculated_total,
    "official_total": official_total,
    "datetime": datetime,
    "payment_method": payment_method
}

# --- Print formatted JSON ---
print(json.dumps(data, ensure_ascii=False, indent=4))