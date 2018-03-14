from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import TextField
from wtforms.fields.html5 import EmailField
from wtforms import validators





class CreateTableForm(FlaskForm):
    tablenumber = TextField('tablenumber', validators=[validators.DataRequired()])
    submit = SubmitField('createtablesubmit', validators=[validators.DataRequired()])
