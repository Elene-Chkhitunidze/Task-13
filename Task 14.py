##Task 1
class BankAccount:
    def __init__(self,account_number, account_holder,balance):
        self.account_number=account_number
        self.account_holder=account_holder
        self.balance=balance

    def money_in(self, x):
        if x<0:
            print("Please enter Positive number")
        else:
            self.balance=self.balance+x
            print(f"Balance is: {self.balance}")

    def money_out(self,y):
        if y<0:
            if -y<self.balance:
                self.balance=self.balance+y
                print(f"Balance is: {self.balance}")
            else:
                print("There is not enough money")
        else:
            print("Please enter a negative number")




account=BankAccount(123456,'John',200)
account_=BankAccount(12456,'Kate',0)
account.money_in(300)
account.money_out(600)

account_.money_in(300)
account_.money_out(-100)


##Task 2
class Student:
    def __init__(self,name, student_id):
        self.name=name
        self.student_id=student_id
        self.course=list()

    def register(self, course):
        if course not in self.course:
            self.course.append(course)
            print(f"{self.name}'s Registered course: {course}")
        else:
            print(f"{course} already registered for {self.name}")


    def info(self):
        print(f"{self.name}'s courses:")
        if self.course==[]:
            print("No course registered")
        else:
            for i in self.course:
                print(i)


st_1=Student('John',123)
st_1.register('History')
st_1.register('Art')
st_1.register('Art')
st_1.info()


st_2=Student('Kate',124)
st_2.register('History')
st_2.register('Biology')
st_2.register('Music')
st_2.register('Art')
st_2.info()