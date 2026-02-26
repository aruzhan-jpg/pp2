
# Working with JSON

import json

person = {
    "name": "Ali",
    "age": 18,
    "city": "Almaty"
}

json_string = json.dumps(person, indent=4)
print("JSON string:")
print(json_string)

parsed_data = json.loads(json_string)
print("Parsed name:", parsed_data["name"])

with open("data.json", "w") as file:
    json.dump(person, file, indent=4)

with open("data.json", "r") as file:
    data = json.load(file)
    print("Read from file:", data)


#2
# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y["age"])

#3

# a Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into JSON:
y = json.dumps(x)

# the result is a JSON string:
print(y)