from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username is taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists! Try another one.', 'danger')
            return redirect(url_for('auth.signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        # If username is not found
        if not user:
            flash('Username not found! Please sign up.', 'danger')
            return redirect(url_for('auth.login'))

        # If password is incorrect
        if not check_password_hash(user.password, password):
            flash('Incorrect password! Try again.', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('home'))
