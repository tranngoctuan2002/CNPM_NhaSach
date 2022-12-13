from bookstoreapp import app, dao, utils
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

@app.route('/receipt')
def receipt():
    list = dao.load_receipt(id=request.args.get("id"),
                            name=request.args.get("name"),
                            sdt=request.args.get("phone"))

    return render_template('receipt.html', receipts=list)

@app.route('/receipt_detail/<int:product_id>')
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


@app.route('/api/import', methods=['post'])
def add_to_list():
    data = request.json

    key = app.config['LIST_KEY']
    list = session.get(key, {})

    p = {
            "name": data['name'],
            "tag": data['tag'],
            "author": data['author'],
            "quantity": 1
        }
    print(p)

    for c in list:
        if(c["name"] == list["name"]):
            return jsonify(utils.stats(list))

    list[len(list)] = p

    print(list)
    session[key] = list

    return jsonify(utils.stats(list))

@app.route('/api/import/<product_id>', methods=['delete'])
def delete_cart(product_id):
    key = app.config['LIST_KEY']
    list = session.get(key)

    if list and product_id in list:
        del list[product_id]

    session[key] = list

    return jsonify(utils.stats(list))
@app.route('/cash')
def cash():
    return render_template('cash.html')

@app.route('/api/cash', methods=["POST"])
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
def delete_from_cash(product_id):
    key = app.config['CASH_KEY']
    cash = session.get(key, {})

    if cash and product_id in cash:
        del cash[product_id]

    session[key] = cash

    return jsonify(utils.cash_stats(cash))
@app.route('/api/cash/<product_id>', methods=['put'])
def update_to_cash(product_id):

    key = app.config['CASH_KEY']
    cash = session.get(key, {})

    if cash and product_id in cash:
        cash[product_id]['quantity'] = int(request.json['quantity'])

    session[key] = cash

    return jsonify(utils.cash_stats(cash))
@app.route('/api/pay', methods=["POST"])
def pay_cash():
    key = app.config['CASH_KEY']
    cash = session.get(key, {})

    cName = request.json['cName']
    cPhone = str(request.json['cPhone'])


    try:
        dao.save_customer(cName, cPhone)
        dao.save_receipt(cash, dao.check_customer(customer_name=cName, customer_phone=cPhone)[0].id)
    except:
        return jsonify({'status': 500})
    else:
        del session[key]
        return jsonify({"status": 200})

@app.route('/api/cash')
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
        'cash': utils.cash_stats(session.get(app.config['CASH_KEY']))
    }

if __name__ == '__main__':
    app.run(debug=True)
