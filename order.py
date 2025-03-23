from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Order

order_bp = Blueprint('order', __name__)

@order_bp.route('/history')
@login_required
def history():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('order_history.html', orders=orders)


@order_bp.route('/order', methods=['GET', 'POST'])
@login_required
def order_milk():
    if request.method == 'POST':
        milk_type = request.form.get('milk_type')
        liters = int(request.form.get('liters', 1))

        if current_user.tokens < liters:
            flash('Not enough tokens for this order!', 'danger')
            return redirect(url_for('order.order_milk'))

        new_order = Order(user_id=current_user.id, milk_type=milk_type)
        current_user.tokens -= liters  # Deduct tokens based on liters ordered
        db.session.add(new_order)
        db.session.commit()

        return redirect(url_for('order.order_milk', ordered=True))  # Show greeting message

    return render_template('order.html', tokens=current_user.tokens, user=current_user)

    #return render_template('order.html', tokens=current_user.tokens)
