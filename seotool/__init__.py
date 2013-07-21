# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.mongokit import Connection
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
import os

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'oauth_step_1'
login_manager.login_message = None

app.config.from_pyfile('../config.py')
connection = Connection(app.config['MONGODB_HOST'],
                        app.config['MONGODB_PORT'])
db = connection[app.config['MONGODB_NAME']]
oid = OpenID(app, os.path.join(app.config['BASEDIR'], 'tmp'))


@login_manager.user_loader
def load_user(user_id):
    collection = db.users
    return collection.User.one({'username': user_id})


from seotool import views, model
connection.register([model.User])

