# Task 1
import unittest


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        self.items.append({
            'name': name,
            'price': price,
            'quantity': quantity
        })

    def total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.items)

    def remove_item(self, name):
        self.items = [item for item in self.items if item['name'] != name]

    def is_empty(self):
        return len(self.items) == 0


class Test(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()  # ტესტის დაწყებამდე, ვქმნით ახალ, ცარიელ კალათას

    # ტესტი ამოწმებს, რომ ახალი კალათა ინიციალიზაციისას ცარიელია
    def test_cart_empty(self):
        self.assertTrue(self.cart.is_empty())  # ახალი კალათა ცარიელია
        self.assertEqual(self.cart.items, [])  # ნივთების სია ცარიელია

    # ტესტი ამოწმებს, რომ ცარიელი კალათის ჯამური ფასი 0-ია
    def test_empty_price(self):
        self.assertEqual(self.cart.total_price(), 0)

    # ტესტი ამოწმებს ნივთის სწორად ამატებს თუ არა კალათაში
    def test_adding_item(self):
        self.cart.add_item('მარწყვი', 3.5, 10)  # მარწყვის დამატება
        self.assertEqual(len(self.cart.items), 1)  # მარწყვის დამატების შემდეგ, კალათაში უნდა იყოს 1 ნივთი
        self.assertEqual(self.cart.items[0],
                         {'name': 'მარწყვი', 'price': 3.5, 'quantity': 10})  # დამატებული ნივთი სწორად შეინახა

    # ტესტი ამოწმებს შეყვანილი რაოდენობა თუ ლოგიკურია (მაგალითად, არ უნდა იყოს 0 ან უარყოფითი)
    def test_invalid_quantity(self):
        with self.assertRaises(ValueError):  # ველოდებით, რომ გამოიწვევს ValueError-ს
            self.cart.add_item('ატამი', 2.5, -5)  # უარყოფითი რაოდენობა არ შეიძლება

    # ტესტი ამოწმებს ჯამურ ფასს ერთი ნივთის დამატებისას
    def test_one_item_total_price(self):
        self.cart.add_item('ალუჩა', 1, 15)
        self.assertEqual(self.cart.total_price(), 15)

    # ტესტი ამოწმებს ჯამურ ფასს რამდენიმე ნივთის დამატებისას
    def test_some_items_total_price(self):
        self.cart.add_item('ალუჩა', 1, 15)
        self.cart.add_item('მარწყვი', 2, 5)
        self.assertEqual(self.cart.total_price(), 25)

    # ტესტი ამოწმებს ნივთის სწორად ამოღებას კალათიდან
    def test_remove_item(self):
        self.cart.add_item('მარწყვი', 2.5, 10)  # დამატება ნივთის
        self.cart.add_item('ატამი', 1.0, 10)  # დამატება მეორე ნივთის (ანუ კალათის ზომაა 2)
        self.cart.remove_item('მარწყვი')  # ნივთის ამოღება (კალათის ზომა დარჩება 1)
        self.assertEqual(len(self.cart.items), 1)  # კალათაში უნდა დარჩეს 1 ნივთი
        self.assertEqual(self.cart.items[0], {'name': 'ატამი', 'price': 1.0, 'quantity': 10})

        # ტესტი ამოწმებს, რომ ყველა ნივთის ამოღების შემდეგ კალათა ცარიელი იყოს

    def test_all_items_out(self):
        self.cart.add_item('მარწყვი', 2.5, 10)  # დამატება ნივთის
        self.cart.add_item('ატამი', 1.0, 10)  # დამატება მეორე ნივთის (ანუ კალათის ზომაა 2)
        self.cart.remove_item('მარწყვი')
        self.cart.remove_item('ატამი')
        self.assertTrue(self.cart.is_empty())  # კალათა ცარიელია

    # კალათაში არარსებული ნივთის ამოღების შემთხვევაში, ერორი არ დაწეროს
    def test_remove_item_not_exist(self):
        self.cart.add_item('მარწყვი', 2.5, 10)  # დამატება ნივთის
        self.cart.remove_item('ატამი')  # ატამის ამოღება კალათიდან, რომელიც კალათაში არც არის
        self.assertEqual(len(self.cart.items), 1)  # კალათის ზომა 1

    # ტესტი ამოწმებს ცარიელი კალათიდან ამოღების სცენარს
    def test_remove_empty(self):
        self.cart.remove_item('ატამი')
        self.assertTrue(self.cart.is_empty())


if __name__ == '__main__':
    unittest.main()


# Task 2

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def get_balance(self):
        return self.balance


class Test2(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount(owner="Elene", balance=100000)

    # ტესტი ამოწმებს, რომ დეპოზიტი იყოს დადებითი და ამოვარდეს ერორი უარყოფითის შემთხვევაში
    def test_deposit(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100000)

    # მთლიანად გამოტანა თანხის
    def test_withdraw_all(self):
        self.account.withdraw(100000)
        self.assertEqual(self.account.get_balance(), 0)

    # თანხის განაღდების დროს, რომ სწორი რაოდენობის თანხა დარჩეს
    def test_withdraw_left(self):
        self.account.withdraw(20000)
        self.assertEqual(self.account.get_balance(), 80000)

    # თუ იმაზე მეტი თანხა გაიტანა ვიდრე ანგარიშზე აქვს, ერორი უნდა ამოვარდეს
    def test_withdraw_than_have(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(200000)

    def test_get_balance(self):
        self.assertEqual(self.account.get_balance(), 100000)


if __name__ == '__main__':
    unittest.main()



