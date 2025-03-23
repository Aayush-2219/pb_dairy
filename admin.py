from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Order  # Ensure Order model is imported

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')  # Ensure url_prefix is set

# Admin Login Page
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')

        if password == "pbdoodh@22":  # Change for security
            session['admin_logged_in'] = True
            flash('Logged in as Admin!', 'success')
            return redirect(url_for('admin.admin_dashboard'))  # Ensure correct url_for
        else:
            flash('Invalid Admin Password!', 'danger')
    
    return render_template('admin_login.html')

# Admin Dashboard
@admin_bp.route('/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        flash('Access denied! Please log in as admin.', 'danger')
        return redirect(url_for('admin.admin_login'))

    orders = Order.query.all()  # Fetch orders
    return render_template('admin_dashboard.html', orders=orders)  # Ensure user=current_user

# Admin Logout
@admin_bp.route('/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Admin logged out.', 'info')
    return redirect(url_for('admin.admin_login'))
