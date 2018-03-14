from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user,login_user, current_user

from . import auth
from .forms import RegistrationForm, LoginForm
from app import login_manager, db, mail
from ..models import User
from ..email import send_email

@auth.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        user = User.objects(email=form.loginemail.data)[0]
        if user and user.verify_password(form.loginpassword.data):
            user = User(form.loginemail.data)
            login_user(user, remember=True)
            return redirect(url_for('main.account'))
        form.loginemail.errors.append("Email or password invalid")
    return render_template("home.html", loginform=form, registrationform=RegistrationForm())


@login_manager.user_loader
def load_user(user_id):
    user_password = User.objects(email=user_id)
    if user_password:
        return User(user_id)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@auth.route("/register", methods=['POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        if User.objects(email=form.email.data):
            form.email.errors.append("Email address already registered")
            return render_template("home.html", loginform=LoginForm(), registrationform=form)
        user = User(email=form.email.data)
        user.password = form.password.data
        user.save()
        token = user.gen_comfirm_token()
        send_email(user.email, 'Confirm Your Account',
                   'confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return render_template("home.html", loginform=LoginForm(), registrationform=RegistrationForm())
    return render_template("home.html", loginform=LoginForm(), registrationform=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.home'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.home'))



