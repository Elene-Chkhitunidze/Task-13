import csv
##Task 1

with open('C:/Users/Elene/Desktop/titanic.csv', 'r') as file:
    titanic = csv.reader(file)
    header = next(titanic)

    with open("Survived.csv", "w", newline='') as file_1:
        survived = csv.writer(file_1)
        survived.writerow(header)

        for row in titanic:
            if row[1] == '1':
                survived.writerow(row)

##Task 2

def sorted_num(x):

        return int(x['Number of employees'])


with open('C:/Users/Elene/Desktop/organizations-100.csv', 'r') as file_2:
    organizations = csv.DictReader(file_2)
    header = organizations.fieldnames
    Sorted_org= sorted(organizations,key=sorted_num, reverse=True)

    with open("sorted_csv.csv","w",newline="") as file_3:
        sorted_csv=csv.DictWriter(file_3, fieldnames=header)
        sorted_csv.writeheader()

        for i in Sorted_org:
            sorted_csv.writerow(i)



##Task 3

code="https"
selected_headers=['Organization Id','Name',	'Website','Industry','Number of employees']

with open('C:/Users/Elene/Desktop/organizations-100.csv', 'r') as file_4:
    websites=csv.DictReader(file_4)


    with open("ssl_companies.csv","w",newline="") as file_3:
        companies=csv.DictWriter(file_3, fieldnames=selected_headers)
        companies.writeheader()

        for row in websites:
            if row['Website'].startswith(code):
                result = dict()
                for h in selected_headers:
                    if h in row:
                        result[h] = row[h]
                companies.writerow(result)























