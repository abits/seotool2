# -*- coding: utf-8 -*-
# Views modules.  Controller which handle the request-response-flow.  They typically call services to provide
# data and perform actions.  They should not communicate directly with models and providers.
from flask import render_template, flash, redirect, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user
from seotool import app, db, tools
from forms import LoginForm
from datetime import datetime
import json


@app.route('/index')
def index():
    return render_template('index.html', form=LoginForm())


@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html', form=LoginForm())


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.users.User.one({'username': form.username.data})
        if user:
            user.last_login.date = datetime.utcnow()
            user.last_login.ip = request.remote_addr
            user.save()
            if login_user(user):
                if tools.is_expired(user.credentials):
                    return redirect(url_for('oauth_step1'))
                else:
                    return redirect(url_for('index'))
        else:
            flash('Fail! We don\'t know your Google Account.', 'error')
        return redirect('/login')
    return render_template('login.html', form=form)


@app.route('/authorize')
def oauth_step1():
    authorize_url = app.config['FLOW'].step1_get_authorize_url()
    return redirect(authorize_url)


@app.route('/authorized')
def oauth_step_2():
    credentials = app.config['FLOW'].step2_exchange(request.args['code'])
    g.user.credentials = json.loads(credentials.to_json())
    g.user.save()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = current_user