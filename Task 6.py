#Task 1

txt=input("Please enter the text: ")
result=dict()

for i in (txt.split()):
    result[i]=result.get(i,0)+1

print(result)


#Task 2
number_1=float(input("Please enter the first number: "))
number_2=float(input("Please enter the second number: "))
operator=input("Please enter the operator: ")

final={
    "+": number_1+number_2,
    "-": number_1 - number_2,
    "/": number_1/number_2 if number_2!=0 else "Divide by 0 error" ,
    "*": number_1 * number_2,
    "%": number_1 % number_2 if number_2!=0 else "Divide by 0 error" ,
    "**": number_1 ** number_2,
    "//": number_1 // number_2 if number_2!=0 else "Divide by 0 error"

}

if operator in {"+","-","/","*","%","//","**"}:

    print("The result is: " + str(final.get(operator)))
else:
   print( "You did not enter the operator")


#Task 3
result_1={}
for i in range(1,11):
    result_1[i]=i*i

print(result_1)


#Task 4

job={
    "Marketing Department":{
        "001":{ "Name": "Snow","Surname": "White", "Age": 21,"Salary": 1500},
        "002": {"Name": "Gigi", "Surname": "Hadid", "Age": 34, "Salary": 3000},
        "003": {"Name": "Johnny", "Surname": "Depp", "Age": 60, "Salary": 7000}
    },

    "Finance Department":{
        "004":{ "Name": "Jim","Surname": "Carrey", "Age": 60,"Salary": 2400},
        "005": {"Name": "Tom", "Surname": "Cruise", "Age": 55, "Salary": 6000},

    },

    "Programming Department":{
        "006":{ "Name": "Emma","Surname": "Watson", "Age": 30,"Salary": 3400},
        "007": {"Name": "Chris", "Surname": "Evans", "Age": 35, "Salary": 5000},

    }
}



salary = dict()

for key, value in job.items():
    total = 0
    for key1, value1 in value.items():
        total= total+value1["Salary"]
    avg= total/len(value)
    salary[key]=avg

print(salary)



