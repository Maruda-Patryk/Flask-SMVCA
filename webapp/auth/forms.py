
from flask_wtf import FlaskForm as Form
from flask_wtf import RecaptchaField
from wtforms.validators import DataRequired , Length , EqualTo , URL
from wtforms import (
    StringField,
    TextAreaField,
    PasswordField,
    BooleanField
)
from .models import User

class Login_Form(Form):
    username = StringField('Username' , [DataRequired() , Length(max=255)])
    password = PasswordField('Password' , [DataRequired()])
    remember = BooleanField()

    def validate(self):
        check_validate = super(Login_Form , self).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(username = self.username.data).first()
        if not user:
            self.username.errors.append(
                'Invalid username or password'
            )
            return False

        if not user.check_password(self.password.data):
            self.username.errors.append(
                'Invalid username or password'
            )
            return False
        return True

        
class Register_Form(Form):
    username = StringField('Username' , [DataRequired() , Length(max=255)])
    password = PasswordField('Password' , [DataRequired()])
    confirm = PasswordField('Confirm Password' , [DataRequired() , EqualTo('password')])
    
    recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(Register_Form , self).validate()
        if not check_validate:
            return False
        
        user = User.query.filter_by(username = self.username.data).first()

        if user:
            self.username.errors.append(
                'User with that name already exist'
            )
            return False

        return True
            