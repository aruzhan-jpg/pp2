import re

# 1. 'a' followed by zero or more 'b'
text = "abbb a ab aaaa"
print(re.findall(r"ab*", text))


# 2. 'a' followed by 2-3 'b'
text = "ab abb abbb abbbb"
print(re.findall(r"ab{2,3}", text))


# 3. lowercase with underscore
text = "hello_world test_value abc_def"
print(re.findall(r"[a-z]+_[a-z]+", text))


# 4. uppercase followed by lowercase
text = "Hello World Python Regex"
print(re.findall(r"[A-Z][a-z]+", text))


# 5. a ... b
text = "acb axxb ab a123b"
print(re.findall(r"a.*b", text))


# 6. replace space comma dot with colon
text = "Hello, world. Python regex"
print(re.sub(r"[ ,\.]", ":", text))


# 7. snake_case → camelCase
text = "snake_case_example"
print(re.sub(r"_([a-z])", lambda x: x.group(1).upper(), text))


# 8. split at uppercase
text = "HelloWorldPython"
print(re.split(r"(?=[A-Z])", text))


# 9. insert spaces before uppercase
text = "HelloWorldPython"
print(re.sub(r"([A-Z])", r" \1", text).strip())


# 10. camelCase → snake_case
text = "camelCaseString"
print(re.sub(r"([A-Z])", r"_\1", text).lower())
