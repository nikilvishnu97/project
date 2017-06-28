from flask_wtf import Form
from wtforms import StringField, BooleanField,PasswordField
from wtforms.validators import DataRequired

class SignUpForm(Form):
    name=StringField('username', validators=[DataRequired()])
    age=StringField('username', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired()])
    email= StringField('email',validators=[DataRequired()])
   
