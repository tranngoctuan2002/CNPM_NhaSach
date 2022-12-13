def stats(session):
    total_value, total_quantity = 0, 0

    if session:
        for c in session.values():
            total_quantity += c['quantity']
            # total_value += c['quantity'] * c['price']

    return {
        # 'total_value': total_value,
        'total_quantity': total_quantity
}

def cash_stats(session):
    total_value, total_quantity = 0, 0

    if session:
        for c in session.values():
            total_quantity += c['quantity']
            total_value += c['quantity'] * c['price']

    return {
        'total_value': total_value,
        'total_quantity': total_quantity
    }