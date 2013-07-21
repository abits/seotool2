# -*- coding: utf-8 -*-
# Views modules.  Controller which handle the request-response-flow.  They typically call services to provide
# data and perform actions.  They should not communicate directly with models and providers.
from flask import render_template, flash, redirect, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from seotool import app, db, tools
from forms import LoginForm
from datetime import datetime
from httplib2 import Http
from apiclient.discovery import build
from oauth2client.client import AccessTokenRefreshError, OAuth2Credentials
import json

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', user=g.user)


@app.route('/accounts')
@login_required
def profiles_list():
    credentials = OAuth2Credentials.from_json(json.dumps(g.user.credentials))
    http = Http()
    http = credentials.authorize(http)
    service = build('analytics', 'v3', http=http)
    accounts = service.management().accounts().list().execute()
    return render_template('accounts.html', accounts=accounts, user=g.user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/authorize')
def oauth_step1():
    authorize_url = app.config['FLOW'].step1_get_authorize_url()
    return redirect(authorize_url)

@app.route('/authorized')
def oauth_step_2():
    credentials = app.config['FLOW'].step2_exchange(request.args['code'])
    http = Http()
    try:
        http = credentials.authorize(http)
        users_service = build('oauth2', 'v2', http=http)
        user_document = users_service.userinfo().get().execute()
        user_email = user_document['email']
        stored_user = db.users.User.one({'email': user_email})
        if stored_user:
            stored_user.last_login.date = datetime.utcnow()
            stored_user.last_login.ip = request.remote_addr
            stored_user.credentials = json.loads(credentials.to_json())
            stored_user.save()
            login_user(stored_user)
            g.user = stored_user
        else:
            msg = 'Sorry, we don\'t know %s. Log out from Google and try again.' % user_email
            flash(msg)
    except AccessTokenRefreshError:
        print AccessTokenRefreshError
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated() and tools.is_expired(g.user.credentials):
        redirect(url_for('logout'))
