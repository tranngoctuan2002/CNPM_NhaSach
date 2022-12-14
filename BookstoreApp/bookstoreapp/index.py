from bookstoreapp import app, dao, utils
from bookstoreapp.decorators import anonymous_user
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, request, session, jsonify, redirect


@app.route('/')
def index():
    product = dao.load_product(0, category_id=request.args.get("category_id"),
                               name=request.args.get("kw"))
    category = dao.load_category_by_id(category_id=request.args.get("category_id"))
    return render_template('index.html', products=product, category=category)
@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = dao.load_product(0, id=product_id)
    return render_template('product_detail.html', product=product)
@anonymous_user
@app.route('/login', methods=['get','post'])
def login_my_user():
    if request.method.__eq__("POST"):
        username = request.form['username']
        password = request.form['password']
        user = dao.auth_user(username, password)

        if user:
            login_user(user=user)

            n = request.args.get('next')
            return redirect(n if n else '/')

    return render_template('login.html')
@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')
@app.route('/cart')
def cart():
    return render_template('cart.html')
@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    key = app.config["CART_KEY"]
    cart = session.get(key,{})

    id = str(data['id'])
    name = data['name']
    category = data['category']
    price = data['price']
    img = data['img']

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "category": category,
            "price": price,
            "img": img,
            "quantity": 1
        }

    session[key] = cart

    return jsonify(utils.cash_stats(cart))
@app.route('/api/cart/<product_id>', methods=['put'])
def update_from_cart(product_id):
    key = app.config['CART_KEY']
    cart = session.get(key, {})

    if cart and product_id in cart:
        cart[product_id]['quantity'] = int(request.json['quantity'])

    session[key] = cart

    return jsonify(utils.cash_stats(cart))
@app.route('/api/cart/<product_id>', methods=['delete'])
def delete_from_cart(product_id):
    key = app.config['CART_KEY']
    cart = session.get(key, {})

    if cart and product_id in cart:
        del cart[product_id]

    session[key] = cart
    return jsonify(utils.cash_stats(cart))
@app.route('/api/cart/pay', methods=["POST"])
def pay_cart():
    data = request.json
    key = app.config["CART_KEY"]
    cart = session.get(key,{})

    name = data['name']
    phone = data['phone']
    address = data['address']
    email = data['email']
    payment = int(data['payment'])
    address_delivery = data['address_delivery']

    try:
        dao.save_customer(customer_name=name, customer_phone=phone, address=address, email=email)
        dao.save_receipt(session=cart, customer_id=dao.check_customer(customer_name=name, customer_phone=phone)[0].id, user_id=1,
                         is_active=bool(payment), delivery=address_delivery)
    except:
        return jsonify({'status': 500})
    else:
        del session[key]
        return jsonify({"status": 200})

@app.route('/api/cart')
def new_cart():
    key = app.config['CART_KEY']
    cart = session.get(key, {})

    if cart:
        del session[key]
    else:
        return jsonify({"status": 500})

    return jsonify({"status": 200})
@app.route('/receipt')
@login_required
def receipt():
    list = dao.load_receipt(id=request.args.get("id"),
                            name=request.args.get("name"),
                            sdt=request.args.get("phone"))
    return render_template('receipt.html', receipts=list)

@app.route('/receipt_detail/<int:product_id>')
@login_required
def receipt_detail(product_id):
    d = dao.load_receipt_by_id(product_id)
    total = 0
    total_quantity = 0
    if d:
        for r in d:
            total_quantity += r[2]
            total += r[2] * r[3]
    return render_template('receipt_detail.html', receipt=d, tQuantity=total_quantity, total=total)

@app.route('/import')
def import_book():
    limit = dao.load_rule_by_id(2).value
    products = dao.load_product(limit,
                                id=request.args.get("id"),
                                name=request.args.get("name"))
    return render_template('import.html', products=products)

@app.route('/api/import', methods=['POST'])
def add_to_list():
    data = request.json
    key = app.config['LIST_KEY']
    list = session.get(key,{})

    id = str(data['id'])
    name = data['name']
    category = data['category']
    rule = dao.load_rule_by_id(3).value

    if id in list:
        list[id]['quantity'] += 1
    else:
        list[id] = {
            "id": id,
            "name": name,
            "category": category,
            "quantity": rule
        }

    session[key] = list

    return jsonify(utils.stats(list))

@app.route('/import-cart')
def import_cart():
    return render_template('import_cart.html')
@app.route('/cash')
@login_required
def cash():
    return render_template('cash.html')

@app.route('/api/cash', methods=["POST"])
@login_required
def add_to_cash():
    data = request.json
    key = app.config['CASH_KEY']
    cash = session.get(key, {})

    id = str(data['id'])
    p = dao.load_info_by_id(id)
    quantity = int(data['quantity'])
    name = p[0][0]
    price = p[0][1]
    category = p[0][2]
    image = p[0][3]

    if id in cash:
        cash[id]['quantity'] += quantity
    else:
        cash[id] = {
            "id": id,
            "name": name,
            "category": category,
            "quantity": quantity,
            "price": price,
            "image": image
        }

    session[key] = cash

    return jsonify(utils.cash_stats(cash))
@app.route('/api/cash/<product_id>', methods=["DELETE"])
@login_required
def delete_from_cash(product_id):
    key = app.config['CASH_KEY']
    cash = session.get(key, {})

    if cash and product_id in cash:
        del cash[product_id]

    session[key] = cash

    return jsonify(utils.cash_stats(cash))
@app.route('/api/cash/<product_id>', methods=['put'])
@login_required
def update_to_cash(product_id):

    key = app.config['CASH_KEY']
    cash = session.get(key, {})

    if cash and product_id in cash:
        cash[product_id]['quantity'] = int(request.json['quantity'])

    session[key] = cash

    return jsonify(utils.cash_stats(cash))
@app.route('/api/pay', methods=["POST"])
@login_required
def pay_cash():
    key = app.config['CASH_KEY']
    cash = session.get(key, {})

    cName = request.json['cName']
    cPhone = str(request.json['cPhone'])


    try:
        dao.save_customer(cName, cPhone)
        dao.save_receipt(session=cash, customer_id=dao.check_customer(customer_name=cName, customer_phone=cPhone)[0].id, user_id=current_user.id)
    except:
        return jsonify({'status': 500})
    else:
        del session[key]
        return jsonify({"status": 200})

@app.route('/api/cash')
@login_required
def new_cash():
    key = app.config['CASH_KEY']
    cash = session.get(key, {})

    if cash:
        del session[key]
    else:
        return jsonify({"status": 500})

    return jsonify({"status": 200})


@app.context_processor
def commit_attr():
    categories = dao.load_categories()
    return {
        'categories': categories,
        'cash': utils.cash_stats(session.get(app.config['CASH_KEY'])),
        'cart': utils.cash_stats(session.get(app.config['CART_KEY'])),
        'list': utils.stats(session.get(app.config['LIST_KEY']))
    }

@app.route('/login_admin', methods=["POST"])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')

if __name__ == '__main__':
    from bookstoreapp.admin import *
    app.run(debug=True)
