#Task 1
from random import random
from unittest import removeResult

mylist=[36, 73, 1, 7, 54, 100, 237, 34, 76, 10, 7, 9 , 12, 34, 49]
print(mylist[3]+mylist[9]+mylist[14])

#Task 2
import random

randomlist= [random.randint(1, 100) for _ in range(20)]
newlist=list()

for i in randomlist:
    if i%2!=0:
        newlist.append(i)

newlist.sort()
print(newlist[0]) ## min
print(newlist[len(newlist)-1]) ## max

#Task 3
my_list = [43, '22', 12, 66, 210, ["hi"]]
#a
print (my_list.index(210))

#b
my_list.append('hello')
print (my_list)

#c
my_list.remove(my_list[2])
print(my_list)

#d
my_list_2=my_list
my_list_2.clear()
print(my_list)
print(my_list_2)

#Task 4
matrix1 = [
    [1, 2, 3,11],
    [4, 5, 6,11],
    [7, 8, 9,11]
]

matrix2 = [
    [1, 2, 3,11],
    [4, 5, 6,11],
    [7, 8, 9,11]
]

row1= len(matrix1) #row
column1= len(matrix1[0]) #Column

final =[]
if len(matrix1)!=len(matrix2) or len(matrix1[0])!= len(matrix2[0]):
    print('Not Equal')
else:
 for i in range(row1):
    result = []
    for j in range(column1):
        result.append(matrix1[i][j] + matrix2[i][j])
    final.append(result)

print(final)


##Taks 5

matrix = [
    [1, 2, 3,4],
    [4, 5, 6,5],
    [7, 8, 9,6]
]


row= len(matrix) #row
column= len(matrix[0]) #Column
newmatrix= []

for i in range(column):
    newmatrix.append([0] * row)

for i in range(row):
    for j in range(column):
        newmatrix[j][i]=matrix[i][j]
print(newmatrix)