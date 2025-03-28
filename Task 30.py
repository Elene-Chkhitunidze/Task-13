from Models import session, Product, CartItems, Order, OrderItem
from datetime import datetime

def view():
    items = session.query(CartItems).all()
    for i in items:
        product = session.query(Product).filter(Product.id == i.product_id).first()
        print(f"ID: {i.id}, Product: {product.name}, Quantity: {i.quantity}")

def add():
    products = session.query(Product).all()

    # მომხმარებელს სთხოვს აირჩიოს პროდუქტის ID და რაოდენობა
    product_id = int(input("გთხოვ აირჩიე პროდუქტის ID, რომლის დამატებაც გინდა: "))
    quantity = int(input("გთხოვ აირჩიე რაოდენობა: "))

    product = session.get(Product, product_id)
    if product and product.quantity_in_stock >= quantity:
        # თუ პროდუქტი არსებობს და საკმარისი რაოდენობაა
        cart_item = session.query(CartItems).filter_by(product_id=product_id).first()
        if cart_item:  # რაოდენობას გაუზრდის
            cart_item.quantity += quantity
        else:  # თუ არ არსებობს, ჩაამატებს
            cart_item = CartItems(product_id=product_id, quantity=quantity)
            session.add(cart_item)
        product.quantity_in_stock -= quantity  # მარაგების რაოდენობა შესაბამისად შემცირდება
        session.commit()
        print("პროდუქტი დაემატა კალათას")
    else:
        # თუ პროდუქტი ან რაოდენობა არ არის საკმარისი
        print("პროდუქტი არ არსებობს, ან თქვენი სასურველი რაოდენობა არ არის მარაგში")

def remove():
    cart_item_id = int(input("გთხოვ შეიყვანო ID, რომლის ამოღებაც გინდა კალათიდან: "))
    cart_item = session.get(CartItems, cart_item_id)
    if cart_item:
        product = session.get(Product, cart_item.product_id)
        # პროდუქტის მარაგის გაზრდა და ელემენტის წაშლა
        product.quantity_in_stock += cart_item.quantity  # მარაგის ისევ გაიზრდება
        session.delete(cart_item)  # პროდუქტი წაიშლება კალათიდან
        session.commit()
        print("პროდუქტი აღარ არის კალათაში")
    else:
        # თუ არასოწრი ID შეიყვანა
        print("ID არასწორია")


def orders():
    cart_items = session.query(CartItems).all()
    if not cart_items:
        print("კალათა ცარიელია")
        return

    total_amount = sum(i.quantity * session.query(Product).filter(Product.id == i.product_id).first().price for i in cart_items)

    order = Order(total_amount=total_amount, order_date=datetime.now())
    session.add(order)
    session.flush()

    for item in cart_items:
        product = session.query(Product).filter(Product.id == item.product_id).first()
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_per_item=product.price
        )
        session.add(order_item)
        session.delete(item)

    session.commit()
    print(f"შეკვეთა განხორიელდა. სულ გადასახდელია: {total_amount:.2f}")


def view_orders():
    orders = session.query(Order).all()
    if not orders:
        print("შეკვეთა არ არის განხორციელებული")
        return

    for i in orders:
        print(f"Order ID: {i.id}, Date: {i.order_date}, Total: {i.total_amount:.2f}")
        order_items = session.query(OrderItem).filter(OrderItem.order_id == i.id).all()
        for item in order_items:
            product = session.query(Product).filter(Product.id == item.product_id).first()
            print(f"  {product.name}: {item.quantity} * {item.price_per_item:.2f}")


