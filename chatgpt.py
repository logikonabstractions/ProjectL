import yaml

with open("tests.yaml", "r") as file:
    data = yaml.safe_load(file)

employee_list = data["employees"]
print(employee_list)
