from sqlalchemy import create_engine, Integer, Column, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime


host = 'localhost'
port = '5432'
user = 'postgres'
password = 'Eleniko123'
database = 'Orders'

Base = declarative_base()
engine = create_engine("sqlite:///:memory:", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity_in_stock = Column(Integer, nullable=False)

class CartItems(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    order_date = Column(DateTime, nullable=False)
    total_amount = Column(Float, nullable=False)

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_item = Column(Float, nullable=False)


Base.metadata.create_all(engine)

def products_info():
    products = [
        Product(name="Apple", price=2.65, quantity_in_stock=100),
        Product(name="Banana", price=3.00, quantity_in_stock=50),
        Product(name="Lemon", price=1.45, quantity_in_stock=30),
        Product(name="Pineapple", price=20.0, quantity_in_stock=35)
    ]
    session.add_all(products)
    session.commit()

def cart_items_info():
    cart_items = [
        CartItems(product_id=1, quantity=10),  # Apple
        CartItems(product_id=2, quantity=7),  # Banana
        CartItems(product_id=3, quantity=3)   # Lemon
    ]
    session.add_all(cart_items)
    session.commit()


def order_info():
    order = Order(order_date=datetime.datetime.now(), total_amount=0.0)
    session.add(order)
    session.commit()

    order_items = [
        OrderItem(order_id=order.id, product_id=1, quantity=2, price_per_item=2.65),  # Apple
        OrderItem(order_id=order.id, product_id=2, quantity=5, price_per_item=3.00)   # Banana
    ]
    session.add_all(order_items)
    session.commit()

    total_amount = sum(item.quantity * item.price_per_item for item in order_items)
    order.total_amount = total_amount
    session.commit()

def fetch_data():
    products = session.query(Product).all()
    cart_items = session.query(CartItems).all()
    orders = session.query(Order).all()
    order_items = session.query(OrderItem).all()


    print("Products:")
    for product in products:
        print(
            f"ID: {product.id}, Name: {product.name}, Price: {product.price}, Quantity in stock: {product.quantity_in_stock}")

    print("\nCart Items:")
    for item in cart_items:
        print(f"ID: {item.id}, Product ID: {item.product_id}, Quantity: {item.quantity}")

    print("\nOrders:")
    for order in orders:
        print(f"ID: {order.id}, Order Date: {order.order_date}, Total Amount: {order.total_amount}")

    print("\nOrder Items:")
    for item in order_items:
        print(
            f"ID: {item.id}, Order ID: {item.order_id}, Product ID: {item.product_id}, Quantity: {item.quantity}, Price per item: {item.price_per_item}")


products_info()
cart_items_info()
order_info()
fetch_data()