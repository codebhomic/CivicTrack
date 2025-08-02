from flask import (
    Flask,Blueprint, flash, redirect, render_template, request, session, url_for,abort
)
from models import db, User
from flask_login import login_user,logout_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            # login_user(user=user)
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
        else:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.')
            return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/logout')
def logout():
    session.clear()
    # logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))
