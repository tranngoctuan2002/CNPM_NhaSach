from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Boolean, Enum, DateTime
from bookstoreapp import db, app
from sqlalchemy.orm import relationship, backref
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime

class UserRole(UserEnum):
    CASH = 1
    INVEN = 2
    ADMIN = 3

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class Category(BaseModel):
    __tablename__ = 'category'
    name = Column(String(50), nullable=False)
    Products = relationship('Product', backref='category', lazy=True)
    def __str__(self):
        return self.name

class Product(BaseModel):
    name = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(200))
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship("ReceiptDetails", backref='product', lazy=True)
    bookentry_details = relationship("BookEntryDetails", backref='product', lazy=True)

class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    def __str__(self):
        return self.name

prod_tag = db.Table('prod_tag',
                  Column('product_id', ForeignKey(Product.id), nullable=False, primary_key=True),
                  Column('tag_id', ForeignKey(Tag.id), nullable=False, primary_key=True))


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(50))
    user_role = Column(Enum(UserRole), default=UserRole.CASH)
    bookentrys = relationship("BookEntry", backref="user", lazy=True)
    def __str__(self):
        return self.name

class Customer(BaseModel):
    name = Column(String(50), nullable=False)
    address = Column(Text, nullable=False)
    sdt = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    receipts = relationship('Receipt', backref='customer', lazy=True)

class Receipt(BaseModel):
    created_time = Column(DateTime, default=datetime.now())
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)

class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)

class BookEntry(BaseModel):
    entry_time = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship("BookEntryDetails", backref='bookentry', lazy=True)

class BookEntryDetails(BaseModel):
    quantity = Column(Integer, default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    bookentry_id = Column(Integer, ForeignKey(BookEntry.id), nullable=False)

class Rule(BaseModel):
    name = Column(String(50), nullable=True)
    value = Column(Integer, default=0)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()