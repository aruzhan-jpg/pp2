import re
import json
import os

# --- Читаем raw.txt ---
base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, "raw.txt")

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Унифицируем переносы строк
text = text.replace('\r\n', '\n')

# --- 1. Товары ---
products = re.findall(r'\d+\.\s*\n(.+)', text)

# --- 2. Стоимость каждой позиции ---
cost_strings = re.findall(r'Стоимость\s*\n([\d ]+,\d{2})', text)

def money_to_float(s):
    return float(s.replace(" ", "").replace(",", "."))

costs = [money_to_float(x) for x in cost_strings]

# --- 3. Подсчёт суммы ---
calculated_total = round(sum(costs), 2)

# --- 4. Официальный итог ---
official_total = None
total_match = re.search(r'ИТОГО:\s*\n([\d ]+,\d{2})', text)
if total_match:
    official_total = money_to_float(total_match.group(1))

# --- 5. Дата и время ---
datetime_match = re.search(r'Время:\s*(.+)', text)
datetime = datetime_match.group(1) if datetime_match else None

# --- 6. Способ оплаты ---
payment_match = re.search(r'Банковская карта', text)
payment_method = payment_match.group(0) if payment_match else None

# --- 7. Вывод ---
data = {
    "products": products,
    "item_costs": costs,
    "calculated_total": calculated_total,
    "official_total": official_total,
    "datetime": datetime,
    "payment_method": payment_method
}

print(json.dumps(data, ensure_ascii=False, indent=4))