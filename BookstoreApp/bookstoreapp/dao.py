import hashlib
from bookstoreapp.models import Category, Product, User, Receipt, ReceiptDetails, Customer, prod_tag, Rule
from bookstoreapp import db, app, login
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
    query = Customer.query.filter(Customer.name.__eq__(customer_name))
    query = query.filter(Customer.sdt.__eq__(customer_phone))

    return query.all()

def save_customer(customer_name, customer_phone, address=None, email=None):
    if not(check_customer(customer_name, customer_phone)):
        c = Customer(name=customer_name, sdt=customer_phone, address=address, email=email)
        db.session.add(c)
        db.session.commit()
    return True


def save_receipt(session, customer_id, user_id, is_active=True, delivery="Tại cửa hàng"):
    if session:
        r = Receipt(is_active=is_active, delivery_to=delivery, user_id=user_id, customer_id=int(customer_id))
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

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()

def product_revenue_by_month(sel_prod=None, from_month=None, to_month=None):
    query = db.session.query(Product.id, Product.name, func.sum(ReceiptDetails.quantity * ReceiptDetails.price)) \
        .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id)) \
        .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))

    if sel_prod:
        query = query.filter(Product.name.contains(sel_prod))
    if from_month:
        query = query.filter(Receipt.created_time.__ge__(from_month))
    if to_month:
        query = query.filter(Receipt.created_time.__le__(to_month))

    return query.group_by(Product.id).all()

def stats_revenue_by_prod(sel_month=None):
    query = db.session.query(Category.id, Category.name, func.sum(ReceiptDetails.quantity * ReceiptDetails.price)) \
        .join(Product, Product.category_id.__eq__(Category.id)) \
        .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id)) \
        .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))

    if sel_month:
        query = query.filter(Receipt.created_time.contains(sel_month))

    return query.group_by(Category.id).all()

@login.user_loader
def load_user_by_id(user_id):
    return User.query.get(user_id)

if __name__ == "__main__":
    with app.app_context():
        print()


