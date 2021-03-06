from flask import render_template, redirect, request, url_for, flash
from . import auth
from .forms import LoginForm,RegistrationForm
from flask_login import logout_user, login_required,login_user
from ..models import User
from ..models import db
from ..email import send_email

@auth.route('/login',methods=['GET','POST'])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            next=request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password!')
        return redirect('/login')

    return render_template('login/login.html',form=form)

@auth.route('/register',methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()

        token = user.generate_confirmation_token()
        send_email(user.email,'Confirm Your Account','register/email/confirm',user=user,token=token)
        flash('A confirmation email has been sent to your email, {} .'.format(user.email))
        return redirect(url_for('main.index'))

    return render_template('register/register.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


from flask_login import current_user
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.route('/confirmed')
@login_required
def confirmed():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account','register/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))



@auth.route('/unconfirmed')
def unconfirmed():

    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('register/unconfirmed.html')

@auth.route('/forgot_password',methods=["GET","POST"])
def forgot_password():
    from .forms import ForgotPasswordForm
    form=ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.generate_reset_token()
        send_email(user.email,'Reset Your Password!','register/email/resetPass',user=user,token=token)
        print("\n\n HI\n\n")
        return redirect(url_for('main.index'))

    return render_template('register/forgot_password.html',form=form)

@auth.route('/password_reset/<token>',methods=["GET","POST"])
def password_reset(token):
    from .forms import PasswordResetForm
    form=PasswordResetForm()
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash("Your Password Has Been Updated.")
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('register/reset_pass.html',form=form)
