import re

# 1. Match 'a' followed by zero or more 'b'
# Pattern: a + any number of b
text = "abbb a ab aaaa"
result = re.findall(r"ab*", text)
print("1:", result)


# 2. Match 'a' followed by 2–3 'b'
# Pattern: a + exactly 2 or 3 b
text = "ab abb abbb abbbb"
result = re.findall(r"ab{2,3}", text)
print("2:", result)


# 3. Find lowercase letters joined with underscore (snake_case)
# Pattern: lowercase letters + "_" + lowercase letters
text = "hello_world test_value abc_def"
result = re.findall(r"[a-z]+_[a-z]+", text)
print("3:", result)


# 4. Find words starting with uppercase letter followed by lowercase letters
# Pattern: one uppercase letter + lowercase letters
text = "Hello World Python Regex"
result = re.findall(r"[A-Z][a-z]+", text)
print("4:", result)


# 5. Match 'a' followed by anything and ending with 'b'
# Pattern: a + any characters + b
text = "acb axxb aс a123b"
result = re.findall(r"a[^ ]*b", text)
print("5:", result)


# 6. Replace space, comma, or dot with colon
# Pattern: space OR comma OR dot
text = "Hello, world. Python regex"
result = re.sub(r"[ ,\.]", ":", text)
print("6:", result)


# 7. Convert snake_case to camelCase
# Split text by underscore and capitalize next words
text = "snake_case_example"
parts = re.split("_", text)

camel = parts[0]
for word in parts[1:]:
    camel += word.capitalize()

print("7:", camel)


# 8. Split string at uppercase letters
# Pattern: split before uppercase letter
text = "HelloWorldPython"
result = re.split(r"(?=[A-Z])", text)
print("8:", result)


# 9. Insert spaces before capital letters
# Pattern: find uppercase letters and add space before them
text = "HelloWorldPython"
result = re.sub(r"([A-Z])", r" \1", text).strip()
print("9:", result)


# 10. Convert camelCase to snake_case
# Pattern: find uppercase letters and add underscore before them
text = "camelCaseString"
result = re.sub(r"([A-Z])", r"_\1", text).lower()
print("10:", result)