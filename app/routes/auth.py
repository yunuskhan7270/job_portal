from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from ..models import User
from ..forms import LoginForm, RegisterForm
from .. import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for(f'{user.role}.dashboard'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('register.html', form=form)

        hashed_pw = generate_password_hash(form.password.data)
        user = User(name=form.name.data, email=form.email.data,
                    password=hashed_pw, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
