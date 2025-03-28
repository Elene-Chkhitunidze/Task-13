import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

#Task 1

squared_numbers=set()

for i in range(1,11):
    squared_numbers.add(i*i)

print(squared_numbers)



#Task 2
txt= str(input("Please enter the text: "))
length= len(txt)
txt_set=set()

for i in range(0,length-1):
    txt_set.add(txt[i])

print(txt_set)

#Task 3

tuple1 = (1,2,3,4,5,6)
tuple2 = (4,5,5,6,6,7)
tuple3= tuple1+tuple2
duplicated_value=list()

print(set(tuple3)) # combined_tuple

for i in tuple1:
    if i in tuple2:

        duplicated_value.append(i)
print(duplicated_value) # duplicated value


#Task 4

tuple_=(11,5,6,20,8,9,10)
output=((tuple_[-1],)+tuple_[1:len(tuple_)-1])+(tuple_[0],)
print(tuple_) #input
print(output) #output

#Task 5

input1= (1, (2, 3), (4, (5, 6)))
final_list=list()

for i in input1:
   if isinstance(i,tuple):
       for j in i:
           if isinstance(j,tuple):
               final_list.extend(j)
           else:
               final_list.append(j)
   else:
       final_list.append(i)

print(tuple(final_list))


#Task 6
set1={1,2}
set2={'a','b'}
final_set=set()
for i in set1:
    for j in set2:
        final_set.add((i,j))

print(final_set)