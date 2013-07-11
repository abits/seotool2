# -*- coding: utf-8 -*-
# Views modules.  Controller which handle the request-response-flow.  They typically call services to provide
# data and perform actions.  They should not communicate directly with models and providers.
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user
from seotool import app, db
from forms import LoginForm
from datetime import datetime
import json


@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()
    return render_template('index.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
#     if g.user is not None and g.user.is_authenticated():
#         return redirect(url_for('profiles'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.users.User.one({'username': form.username.data})
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            user.last_login.date = datetime.utcnow()
            user.last_login.ip = request.remote_addr
            user.save()
            return redirect(url_for('index'))
        else:
            flash('Login failed! Password and user did not match.', 'error')
            return redirect('/index')
    return render_template('index.html', form=form)


@app.route('/authorize')
def oauth_step1():
    authorize_url = app.config['FLOW'].step1_get_authorize_url()
    return redirect(authorize_url)


@app.route('/authorized')
def oauth_step_2():
    credentials = app.config['FLOW'].step2_exchange(request.args['code'])
    g.user.credentials = json.loads(credentials.to_json())
    g.user.build()
    return redirect(url_for('profiles'))


@app.before_request
def before_request():
    g.user = current_user