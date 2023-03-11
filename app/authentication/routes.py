from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = UserLoginForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)
            user = User(email=email, password=password)
            db.session.add(user)
            db.session.commit()
            flash(f'You have successfully created a user account {email}', 'User-created')
            return redirect(url_for('site.home'))
    except:
        raise Exception("Invalid form data: no cars for you")
    return render_template('sign_up.html', form=form)

@auth.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = UserLoginForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)
            logged_user = User.query.filter_by(email=email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successful', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Invalid email or password', 'auth-failed')
    except:
        raise Exception('Invalid form data: check your form')
    return render_template('sign_in.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))


