import csv

# keys = column names, and value = column values:
# my_dict = {"test": 1, "testing": 2}
# with open('cls.csv', 'wb') as f:  # use 'w' mode in 3.x
#     w = csv.DictWriter(f, my_dict.keys())
#     w.writeheader()
#     w.writerow(my_dict)

# no column names, just "key, value" in each row:
somedict = {"raymond":'red', "rachel":'blue', "matthew":'green'}
with open('cls.csv','wb') as f:
  w = csv.writer(f)
  w.writerow(["URL", "title"])
  w.writerows(somedict.items())
