
#Task 1
txt= input("გთხოვთ, შეიყვანეთ ტექსტი: ")
length= len(txt)
string=""

while length>0:
    string=string+txt[length-1]
    length=length-1

if(txt==string):
    print('შეყვანილი ტექსტი არის პალინდრომი')
else:
    print('შეყვანილი ტექსტი არ არის პალინდრომი')



#Task 2
txt1= input("Please enter the txt: ")
lenght1=len(txt1)
sequence=""
num=0

while lenght1>0:
    if lenght1==1:
        sequence = sequence + str(ord(txt1[num]))
        lenght1 = lenght1 - 1
    else:
        sequence = sequence + str(ord(txt1[num])) + ", "
        num = num + 1
        lenght1 = lenght1 - 1

print("ASCII coding result: " + sequence)



