from datetime import date, datetime

default_date = datetime.now().strftime("%a %b %d %y")

date_object = datetime.strptime(default_date, "%a %b %d %y")


example_string = '2022-05-04'

date_example = datetime.strptime(example_string, "%Y-%m-%d")

print(date_example)
print(type(date_example))

print(default_date)
print(type(default_date))
print(date_object)
print(type(date_object))
# print(default_date.strftime("%d %B %Y"))
