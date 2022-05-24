# Contains login and user authentication information
from hashlib import sha256
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User #for new user creation
from werkzeug.security import generate_password_hash, check_password_hash #imported so passwords are never stored in plain text
from . import db #imports db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # This line of code is how you look for specific entries in the db
        # the .first() returns the first result (but there should only be one result)
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                # The remember=True is stored in the flask session
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Username does not exist', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required # You can only access this route if user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        current_user == None
        return render_template('sign_up.html', user=current_user)

    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user and user.is_active:
            flash(f'Hi {user.username}, you are signed up already, please sign in', category='warning')
            already_signed_up = True
            return redirect(url_for('auth.login'))
        elif len(username) < 2:
            flash('Username must be longer than 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 5:
            flash('Your password must be longer than 5 characters', category='error')
        elif user == None:
            # code to actually create a new user in database
            new_user = User(username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('views.home', user=new_user))

    return render_template('sign_up.html', user=current_user)