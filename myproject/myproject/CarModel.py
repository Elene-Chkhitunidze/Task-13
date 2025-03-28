from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):

    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(50))
    model = db.Column(db.String(50))
    instock = db.Column(db.String(3))
    price = db.Column(db.Float)

    def __init__(self, manufacturer, model, instock, price):
        self.manufacturer = manufacturer
        self.model = model
        self.instock = instock
        self.price = price