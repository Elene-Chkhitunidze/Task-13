import functools
from functools import reduce
from logging import exception


##Task 1
def union(x, y):
    list_1 = list()
    for a, b in zip(x, y):
        list_1.append((a, b))
    return list_1

lst1 = [1, 2, 3]
lst2 = ['a', 'b', 'c']

print(union(lst1, lst2))

##Task 2

list_2= [1, 2, 3, 4, 5, 6, 7]

even_num= list(filter(lambda n: n%2==0,list_2))
print(even_num)

##Task 3

list_3= [1, 2, 3, 4, 5, 6, 7,-1,-5,0,-20]
positive_num= list(filter(lambda n: n>0,list_3))
print(positive_num)


##Task 4

list_4= ["one","aiia","computer","lol"]
polindrom_value= list(filter(lambda n: n[::1]==n[::-1],list_4))
print(polindrom_value)

##Task 5


def num_mult (a):
    try:
        if not all(isinstance(i, (int, float)) for i in a):
            raise TypeError
        return reduce(lambda x,y:x*y,a)
    except TypeError:
        return "შეიყვანეთ მხოლოდ რიცხვები"
    except Exception as e:
        return e


list_5= [1,2,3,4,5,-1]
print(num_mult(list_5))

##Task 6
list_6= ['hello', 'world', 'coding', 'nod',"cooking","ing","ng"]
ending="ing"

def same_ending(lst, end):
    try:
        return list(filter(lambda x: x[-len(end):] == end, lst))
    except TypeError:
        return "შეიყვანეთ მხოლოდ ტექსტი"
    except Exception as e:
        return e

print(same_ending(list_6,ending))

