from math import trunc
from random import randint, random

# Task 1
number= int(input("Please Enter a Number: "))

while   number!=0:
    if number>0:
        print(number)
        number = number - 1
    else:
        print(number)
        number = number + 1
print("There are no intermediate numbers")


#Task 2
total_sum = 0


while True:
    input_ = input('Please enter the value: ')

    if input_ == "sum":
        break

    if input_.isnumeric() or (input_.replace(',','',1) and input_.count('.') < 2):
        num_ = float(input_)
        if num_ > 0:
            total_sum = total_sum + num_
        else:
            print("Please enter a positive number:")
    else:
        print("Please enter a positive number or text 'sum': ")

print("Sum is:", total_sum)

2310263

##Task 3
import random

lower= int(input("Please enter the lower bound: "))
upper= int(input("Please enter the upper bound: "))
rand= random.randint(lower,upper)
lives= int(input("Please enter the number of lives: "))


while lives>0:
    num = int(input("Please enter a number: "))
    if num>rand:
        print("Your number is higher")
        lives=lives-1
    elif num<rand:
        print("Your number is Lower")
        lives = lives - 1
    else:
        print("You guessed the number")
        break
else:
    print("Game Over")







