from operator import index
from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import path
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

# Define new database
db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '@ByTheFireGuild383'
    # The below code stores the database in the website folder
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Below code initializes database
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # create the database (do after setting up models.py)
    from .models import User, Note, Asset

    create_database(app)

    # class MyModelView(ModelView):
    #     def is_accessible(self):
    #         return current_user.is_authenticated

    #     def inaccessible_callback(self, name, **kwargs):
    #         return redirect(url_for('auth.login'))

    # class MyAdminIndexView(AdminIndexView):
    #     pass


    ### Pick up right here with the Admin section


    admin = Admin(app)
    admin.add_view(ModelView(User, db.session))

    login_manager = LoginManager()
    # Says where to be redirected if NOT logged in and a login is required
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
        # get automatically looks for the primary key

    return app

# function that checks if database exists, then creates database
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created database')
