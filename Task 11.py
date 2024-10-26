import csv

with open('C:/Users/Elene/Desktop/organizations-100.csv', 'r') as file:
    titanic = csv.DictReader(file)

    for row in titanic:
        print(row)