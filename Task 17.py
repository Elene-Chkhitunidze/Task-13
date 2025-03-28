#Task 1

class Node:
    def __init__(self,data=None):
        self.data=data #საწყისი კვანძი
        self.next=None #შემდეგი კვანძი

class LinkedList:
    def __init__(self):
        self.head=None #სიის პირველი კვანძი, რომელიც თავიდან არის None, რადგან ჯერ სია ცარიელია

#ახალი კვანძის ჩამატება სიის ბოლოს
    def append(self,data):
        new_node=Node(data) #შეიქმნა ახალი კვანძი მონაცემის მიხედვით
        if self.head is None: #ვამოწმებთ სია ცარიელია თუ არა
            self.head=new_node #თუ ცარიელია, პირველი კვანძი ხდება Head
            return

        last_node= self.head  #თუ სია ცარიელი არ არის, მაშინ ვპოულობთ სიის ბოლო კვანძს, რომელიც ჯერ არის Head
        while last_node.next:  #სანამ სიის ბოლო ელემენტამდე არ მივალთ
            last_node=last_node.next  #იგი იღებს შემდეგი კვანძის მნიშვნელობას
        last_node.next=new_node  #ვამატებთ ახალ კვანძს

 #სიის დაბეჭდვა
    def print(self):
        current_node=self.head #საწყისი წერტილი არის ჰედი
        while current_node: #სანამ სიის ბოლო კვნძამდე მივალთ
            print(current_node.data,end="-->")  #დაბეჭდავს მიმდინარე კვანძს
            current_node=current_node.next  #და გადავა შემდეგ კვანძზე
        print() #ახლის დაბეჭდვა შემდეგი ხაზიდან რომ დაიწყოს

    #კვანძის წაშლა
    def remove(self, index):
        if index<0 or self.head is None: #ვამოწმებთ სია არის თუ არა ცარიელი ან ინდექსი უარყოფითი
            return
        if index==0: #ვამოწმებთ წასაშლელი კვანძი head ხომ არაა. თუ ჰედია
            self.head  = self.head.next #მაშინ უკვე ახალი ჰედი ხდება, წაშლამდე არსებული ჰედის შემდეგ მდგარი კვანძი
            return

        #თუ უნდა წავშალოთ სიის რომელიმე შუა კვანძი ან ბოლო
        current_node=self.head #საწყისი ყოველთვის იქნება ჰედი
        position=0 #პოზიცია კი 0

        while current_node.next and position<index-1: #მივდივართ წასაშლელი კვანძის წინა კვანძამდე, რომ მერე წასასლელი წავშალოთ
            current_node=current_node.next
            position = position+1

        if current_node.next: #თუ მივედით იმ წასაშლელ კვანძამდე და ვნახეთ რომ მას შემდეგი კვანძი აქვს
            current_node.next=current_node.next.next #მაშინ ამ კვანძის ადგილს დაიკავებს შემდეგი კვანძი

    #ვშლით არ ინდექსის მიხედვით, არამედ მნიშვნელობის მიხედვით
    def remove_value(self,value):
        if self.head is None: #ვამოწმებთ სია ცარიელია თუარა
            return

        if self.head.data==value: #თუ არ არის ცარიელი, მაშინ ვამოწმებთ წასაშლელი კვანში ჰედი ხომ არ არის
            self.head=self.head.next #თუ ჰედია, მაშინ ძველი ჰედის ადგილს იკავბს მისი შემდეგი მნიშვნელობა და ხდება ახალი ჰედი
            return

        #თუ შუა ან ბოლო კვანძს ვშლით
        current_node=self.head
        while current_node.next and current_node.next.data!=value: #სანამ რაც უნდა წავშალოთ, მის წინა კვანძამდე არ მივალთ
            current_node=current_node.next #მიმიდნარე კვანძიდან გადავდივართ შემდეგ კვანძზე

        if current_node.next: ##თუ მივედით იმ წასაშლელ კვანძამდე და ვნახეთ რომ მას შემდეგი კვანძი აქვს
            current_node.next=current_node.next.next #რაც უნდა წავშალოთ, მას ჩავანაცვლებთ მის შემდგომ მდგომი კვანძით

    def insert_value(self,index, data):
        new_node=Node(data)

        if index<0: #თუ გადაცემული ინდექსი უარყოფითია, არაფერი არ მოხდება
            return

        if index==0: #თუ ჩამატება გვინდა ჰედზე
            new_node.next = self.head #ახალ კვანძის next ვუთითებთ არსებულ head-ს, რათა ის გახდეს მეორე ელემენტი
            self.head = new_node #ჰედს ვანიჭებთ ამ კვანძის მნიშვნელობას
            return

# თუ დამატება ხდება სიის შუაში ან ბოლოში
        current_node = self.head #სიის გავლა იწყება head-დან
        position = 0
#უნდა ვიპოვოთ რომელ ინდექსზეც გვინდა ჩამატება, მის წინ მდგარი კვანძი
        while current_node and position<index-1: #მივდივართ წინა პოზიციაზე
            current_node=current_node.next #გადავდივართ შემდეგ კვანძზე
            position=position+1

# თუ მივედით სიის ბოლოში, ანუ current_node გახდა None და index მეტია სიის სიგრძეზე, მაშინ ფუნქცია სრულდება
        if current_node is None:
            return

        new_node.next=current_node.next #შემდეგ ინდექსზე არსებული კვანძი გადაგვაქ შემდეგ კვანძზე
        current_node.next=new_node #შემდეგ ადგილზე ვსვამთ ახალ კვანძს


linked_list=LinkedList()
linked_list.append(50)  # 0
linked_list.append(15)  # 1
linked_list.append(20)  # 2
linked_list.append(11)  # 3
linked_list.append(5)  # 4
linked_list.append(25)  # 5

linked_list.print()
linked_list.remove(5)
linked_list.print()
linked_list.remove_value(20)
linked_list.print()
linked_list.insert_value(5,30)
linked_list.print()


#stack

class Node:
    def __init__(self, data=None):
        self.data = data #საწყისი კვანზი
        self.next = None #შემდეგი კვანძი


class Stack:
    def __init__(self):
        self.top_node = None #როცა სია ცარიელი, პირველი კვანძის მნიშვნელობა ნანია
        self.length = 0 #სტეკის სიგრძე თავიდან არის 0, რადგან ის ცარიელია

    def empty(self): #ამოწმებ სია სტეკი თუ არა
        return self.length == 0 #სტეკს გააჩნია სიგრძე, თუ ეს სიგრძე 0, ანუ სტეკი ცარიელია და დააბრუნებს True, თუარადა False

    def size(self): #აბრუნებს სტეკის სიგრძეს
        return self.length

#სტეკში ამატებს კვანძს
    def push(self, data):
        new_node = Node(data) #ქმნის ახალ კვანძს მონაცემით `data`
        new_node.next = self.top_node #ახალ კვანძის `next` ვუთითებთ ამჟამინდელ ტოპ კვანძს
        self.top_node = new_node  #ტოპ კვანძი ხდება ახალ კვანძი
        self.length += 1 #რადგან ელემეტი დაემატა, სიგრძესაც ვუზრდით

#სტეკიდან კვანძის წაშლა
    def pop(self):
        if not self.empty(): #ამოწმებს სტეკი ცარიელი ხომ არა რის. თუ არ არის, მაშინ
            popped_item = self.top_node.data #ვინახავთ ამოღებული ელემენტის მონაცემს
            self.top_node = self.top_node.next # ტოპ კვანძი გადაგვაქვს შემდეგ კვანძზე, ამიტომ ახალი ტოპი ხდება წინა კვანძი
            self.length -= 1 #რადგან კვანძი მოაკლდა, სიგრძეც მხირდება სტეკის
            return popped_item #წაშლილ ელემენტს დააბრუნებს
        else: #თუ არის, ვერაფერსაც ვერ წაშლია, ამიტომ ერორი დაარტყას
            raise IndexError("Stack is empty")




