from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required,LoginManager
from models import db, User  # ✅ Import db without initializing

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)  # ✅ Initialize db inside create_app

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import blueprints
    from auth import auth_bp
    from admin import admin_bp  # Import the Admin Blueprint
    from order import order_bp
    from milk import milk_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(milk_bp)
    app.register_blueprint(admin_bp)


    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html', user=current_user)
    
    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')


    @app.route('/')
    def home():
        return render_template('index.html')

    return app  # ✅ Return the app instance

app = create_app()    

# Only run if this file is executed directly
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # ✅ Ensure tables are created inside app context
    app.run(debug=True)
