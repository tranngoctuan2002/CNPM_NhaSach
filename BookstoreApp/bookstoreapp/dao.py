from bookstoreapp.models import Category, Product, User, Receipt, ReceiptDetails, Customer, prod_tag, Rule
from bookstoreapp import db, app
from flask_login import current_user
from sqlalchemy import func

def load_categories():
    return Category.query.all()

def load_receipt_by_id(receipt_id=0):
    query = db.session.query(Product.id, Product.name, ReceiptDetails.quantity, ReceiptDetails.price, Receipt.id, \
                             Receipt.created_time, Customer.name, User.name, Receipt.is_active, Category.name)\
                            .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id))\
                            .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))\
                            .join(Customer, Receipt.customer_id.__eq__(Customer.id))\
                            .join(User, Receipt.user_id.__eq__(User.id))\
                            .join(Category, Product.category_id.__eq__(Category.id))

    if receipt_id:
        query = query.filter(Receipt.id.__eq__(int(receipt_id)))
        return query.all()

def load_receipt(id=None, name=None, sdt=None):
    query = db.session.query(Receipt.id, Receipt.created_time, Customer.name, Receipt.is_active)\
                            .join(Customer, Receipt.customer_id.__eq__(Customer.id))

    if id:
        query = query.filter(Receipt.id.__eq__(id))

    if name:
        query = query.filter(Customer.name.contains(name))

    if sdt:
        query = query.filter(Customer.sdt.__eq__(sdt))

    return query.all()

def load_product(limit, id=None, name=None, category_id=None):
    query = db.session.query(Product.id, Product.image, Product.name, Product.quantity, Category.name, Product.price,\
                             Product.description).join(Category)

    if limit:
        query = query.filter(Product.quantity.__le__(limit))

    if id:
        query = query.filter(Product.id.__eq__(id))

    if name:
        query = query.filter(Product.name.contains(name))

    if category_id:
        query = query.filter(Product.category_id.__eq__(category_id))

    return query.all()

def load_book_by_name(book_name=None):
    query = Product.query.filter(Product.name.contains(book_name))
    return query.all()

def load_info_by_id(book_id = None):
    query = db.session.query(Product.name, Product.price, Category.name, Product.image)\
                            .join(Product, Product.category_id.__eq__(Category.id))

    if book_id:
        query = query.filter(Product.id.__eq__(book_id))
        return query.all()
    return []

def check_customer(customer_name, customer_phone):
    query = Customer.query.filter(Customer.name.contains(customer_name))
    query = query.filter(Customer.sdt.__eq__(customer_phone))

    return query.all()

def save_customer(customer_name, customer_phone):
    if not(check_customer(customer_name, customer_phone)):
        c = Customer(name=customer_name, sdt=customer_phone)
        db.session.add(c)
        db.session.commit()
    return True


def save_receipt(session, customer_id):
    if session:
        r = Receipt(is_active=True, user_id=1, customer_id=int(customer_id))
        db.session.add(r)

        for c in session.values():
            rd = ReceiptDetails(quantity=c['quantity'], price=c['price'], receipt=r, product_id=c['id'])
            db.session.add(rd)

        try:
            db.session.commit()
        except:
            return False
        else:
            return True

def load_rule_by_id(rule_id):
    return Rule.query.get(rule_id)

def load_category_by_id(category_id = None):
    return Category.query.get(category_id)

if __name__ == "__main__":
    with app.app_context():
        print(load_categories())


