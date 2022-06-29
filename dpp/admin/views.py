from flask import (
    render_template, request, flash, g, redirect, url_for, session
)

from flask_login import (
    login_user, logout_user, current_user, login_required
)

from . import admin
from .forms import (
    RegisterAdmin, LoginAdmin
)

from .. import db
from ..models import (
    Admin
)
from werkzeug.exceptions import abort

from ..utils import Target, Username
target = Target()
usernames = Username()

@admin.route('/register', methods=('GET', 'POST'))
def register():

    form =  RegisterAdmin()

    if form.validate_on_submit():
        admin = Admin(
            user='_ad_',
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(admin)
        db.session.commit()

        flash('Admin registered.')
        target.set_target('admin.login')
        return redirect(url_for('admin.flashing'))
    
    return render_template('auth/admin/register.html', form=form)

@admin.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginAdmin()

    if form.register.data:
        return redirect(url_for('admin.register'))
    
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.emial.data).first()

        if admin is not None and admin.verify_password(form.password.data):

            if 'user' in g:
                g.pop('user', None)

            g.user = admin
            if 'user' in session:
                session.pop("user", None)
            
            session['user'] = g.user.user
            session['id'] = g.user.id
            usernames.set_username('Admin : {} {}'.format(g.user.first_name, g.user.last_name))

            login_user(admin)
            
            return redirect(url_for('home.admin'))
        else:
            flash(u'Invalid email or password.', 'error')
        
    return render_template('auth/admin/login.html', form=form)

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out succesfully.')
    target.set_target('home.home_dpp')
    return redirect(url_for('admin.flashing'))



@admin.route('/flashing')
def flashing():
    return render_template('auth/flashing.html', target = target.get_target()) # display the flashes, then


@admin.before_app_request
def load_logged_in_user():
    user_id = current_user.get_id()

    if user_id is None:
        g.user = None
    else:
        g.user = Admin.query.filter_by(id=user_id).first()
