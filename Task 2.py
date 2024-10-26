
#Task 1
Number=int(input("Please enter th number: "))

if (Number%2==0):
    print("even")
else:
    print("odd")

#Task2

Text=str(input("Please enter the text: "))


if ("small" in Text or "tall" in Text or "middle" in Text) :
    print(Text)
else:
    print("Can't find words in this text")



#Task 3
Number1=float(input("Please enter the first number: "))
Number2=float(input("Please enter the second number: "))
Operator=(input("Please enter the operator (+, -, *, /, //, %, **): "))

if(Operator=="+"):
    print(Number1+Number2)
elif(Operator=="-"):
    print(Number1 - Number2)
elif (Operator == "*"):
    print(Number1 * Number2)
elif (Operator == "/"):
    print(Number1 / Number2)
elif (Operator == "//"):
    print(Number1 // Number2)
elif (Operator == "%"):
    print(Number1 % Number2)
elif (Operator == "**"):
    print(Number1 ** Number2)
else:
    print("It is not an operator")