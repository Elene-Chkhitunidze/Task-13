from idlelib.editor import keynames

#Task 1
Number_1= int(input("Please Enter Number1: "))
Number_2= int(input("Please Enter Number2: "))
Number_3= int(input("Please Enter Number3: "))

print("Sum is: "+str(Number_1+Number_2+Number_3))


#Task 2
Cube_Length= int(input("Please enter the length of a cube: "))

print("The cube volume is: "+str(Cube_Length**3))
print("The cube surface area is: "+str(6*Cube_Length**3))


#Task 3
Monitor= float(input("Please enter the price of the monitor: "))
System_block= float(input("Please enter the price of the system block: "))
Keyboard= float(input("lease enter the price of the keyboard: "))
Mouse= float(input("lease enter the price of the mouse: "))

print("Total Price: "+str(Monitor+System_block+Keyboard+Mouse))
