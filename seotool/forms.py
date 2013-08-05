# -*- coding: utf-8 -*-
# Forms module.  Represents HTML forms.
from flask.ext.wtf import Form, \
    TextField, BooleanField, PasswordField, \
    TextAreaField, DateField, FormField, SelectField, HiddenField
from flask.ext.wtf import Required, Length, Email
from datetime import date


class LoginForm(Form):
    username = TextField('Username', validators=[Required(), Length(max=32)])
    # password = PasswordField('Password',
    #                          validators=[Required(), Length(max=32)])
    # remember_me = BooleanField('Remember me', description="Remember me",
    #                            default=False)


class EditReportForm(Form):
    include_monthly_visitors_section = BooleanField(u'Besucher im Vergleich zum Vormonat')
    month_monthly_visitors_section = TextField()
    year_monthly_visitors_section = TextField()