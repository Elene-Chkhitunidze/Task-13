
class Person:
    def __init__(self,name, deposit=1000, loan=0):
        self.name=name
        self.deposit=deposit
        self.loan=loan

    def __str__(self):
        return f"Name: {self.name}, Deposit: {self.deposit}, Loan: {self.loan}"



class House:
    def __init__(self,ID,price, owner):
        self.ID=ID
        self.price=price
        self.owner=owner
        self.status='გასაყიდი'

    def selling(self,buyer,loan=None):
        self.owner.deposit=self.owner.deposit+self.price
        self.owner=buyer
        if loan==None:
            self.status='გაყიდული'
            print(f"The house status: {self.status} New Owner: {self.owner}")
        else:
            self.owner.loan=self.owner.loan+loan
            self.status='გაყიდული სესხით'
            print(f"The house status: {self.status}, New Owner: {self.owner}")


owner = Person("John")
buyer = Person("Kate",0)

house_1 = House("12345", 750000, owner)

house_1.selling(buyer)
house_1.selling(buyer,20000)

