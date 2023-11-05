from sqlalchemy import func
from . import db


# login
class loginModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String(length=25), nullable=False,)

    def __repr__(self):
        return f"{self.username} {self.password}"


# add new customer
class CEntry(db.Model):
    cust_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=60), nullable=False)
    address = db.Column(db.String(length=150), nullable=True)
    contact = db.Column(db.Integer(), nullable=True)
    d_entries = db.relationship('DEntry', backref='customer', lazy=True)

    def __repr__(self):
        return f"{self.name} {self.address} {self.contact}"

# add purchased/sale data
class DEntry(db.Model):
    entry_id = db.Column(db.Integer(), primary_key=True)
    parts = db.Column(db.String(length=1000), nullable=False)
    qty = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Numeric(scale=2), nullable=False)
    time = db.Column(db.DateTime(timezone=True), server_default=func.now())
    cust_id = db.Column(db.Integer, db.ForeignKey('c_entry.cust_id'), nullable=False)

    def __repr__(self):
        return f"{self.entry_id} {self.parts} {self.qty} {self.price} {self.time} {self.cust_id}"

# add new products
class PEntry(db.Model):
    part_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=150), nullable=False)
    qty = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Numeric(scale=2), nullable=False)

    def __repr__(self):
        return f"{self.part_id} {self.name} {self.price}"