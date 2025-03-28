##Task 1
from unicodedata import numeric

int_list = [10,20,30,40]

def number(n):
    global int_list
    int_list.append(n)

    return  int_list

print(number(float(input("Please enter a number: "))))

##Task 2
def numbers_sum(n):
    if n<10:
        return n
    else:
        return n % 10 + numbers_sum(n // 10)


print(numbers_sum(int(input("Please enter a number: "))))

##Task 3

def reverse(n):
    if  len(n)==1:
        return n
    else:
        return n[-1] +reverse(n[:-1])

print(reverse(str(input("Please enter a text: "))))

##Task 4




def fibonacci(n):

    if n==1:
        return 0
    if n==2:
        return 1
    else:
        return fibonacci(n-1)+fibonacci(n-2)


num=int(input("Please enter a number: "))

for i in range(1,num+1):
    print(fibonacci(i))

