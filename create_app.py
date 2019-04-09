import os
import sys
import json

curent_path = os.getcwd() 
def create_project(app_name):

    def validate_config_file():

        missing_arg = 'Ther was a problem with some key, pls delete config file and execute\
            script again \nor fill key property \nKey: '
        with open('config.json' , 'r') as f:
            data = json.load(f)
            if 'project_name' in data:
                if data['project_name'] != '':
                    pass
                else:
                    print('There must be a project name!!!')
                    return False
            else:
                print(missing_arg + 'project_name')
                return False

            if 'app_settings' in data:
                if len(data['app_settings']) >= 1:
                    for setting in data['app_settings']:
                        parms = ('env' , 'object_name' , 'default' , 'DEBUG' , 'SECRET_KEY' , 'SQLALCHEMY_DATABASE_URI')

                        for parm in parms:
                            if not parm in setting or setting[parm] == '':
                                print(
                                    'ERROR!!!\nTher was a problem in setting {}, key \'{}\' is missing or invalid'.format(setting , parm)
                                )
                                return False
                else:
                    print('key \'app_settings\' is empty')
                    return False

            else:
                print('Ther is not app_setting key')
                return False

            if not 'create_database_table' in data or not isinstance(data['create_database_table'] , bool):
                print(missing_arg + 'create_user_module')
                return False

            if not 'virtual_env' in data:
                print(missing_arg + 'virtual_env')
                return False

            if not 'create_with_venv' in data['virtual_env'] \
                or not isinstance(data['virtual_env']['create_with_venv'] , bool):
                print(missing_arg + 'create_user_module')
                return False

            if not 'install_virtual_env_pack' in data['virtual_env'] \
                or not isinstance(data['virtual_env']['install_virtual_env_pack'] , bool):
                print(missing_arg + 'install_virtual_env_pack')
                return False

            if not 'venv_name' in data['virtual_env']:
                print(missing_arg + 'venv_name')
                return False

            if not 'recaptcha' in data:
                print(missing_arg + 'venv_name')
                return False

            if not 'integrate_recaptcha' in data['recaptcha']:
                print(missing_arg + 'venv_name')
                return False

            return data



    def create_config_file():
        with open('config.json' , 'w') as f:
            data = {'project_name':app_name , 
                    'app_settings':[
                        
                        {
                            'env':'dev', 'object_name':'DevConfig' , 'default':True,
                            'DEBUG':True , 'SECRET_KEY':'if_you_dont_change_this_will_be_change_for_os.urandom(24)' ,
                            'SQLALCHEMY_DATABASE_URI':'mysql+pymysql://root:pass@localhost:3306/admin_page',
                            'other_setting':[
                                {'name':'PORT' , 'value':8080}
                            ]
                        },
                        
                        {
                            'env':'prod', 'object_name':'ProdConfig', 'default':False,
                            'DEBUG':False , 'SECRET_KEY':'if_you_dont_change_this_will_be_change_for_os.urandom(24)' ,
                            'SQLALCHEMY_DATABASE_URI':'mysql+pymysql://root:pass@localhost:3306/admin_page',
                            'other_setting':[]
                        }
                    ],
                    'create_database_table':True,
                    'virtual_env':{
                        'create_with_venv':True,
                        'install_virtual_env_pack':True,
                        'venv_name':'env_{}'.format(app_name)
                        },
                    'recaptcha':{
                        'integrate_recaptcha':False,
                        'RECAPTCHA_PUBLIC_KEY':False,
                        'RECAPTCHA_PRIVATE_KEY':False
                    }
                }
            json.dump(data , f)
            print('Config file was create, execute script egain to create a app')
            return False


    
    if os.path.isfile(curent_path + '/config.json'):
        return validate_config_file()
    else:
        return create_config_file()

class Main:

    def __init__(self , data):
        self.data = data
        self.recaptcha = data['recaptcha']

        self.curent_path = os.getcwd() 

    def virtual_env(self):
        virtual_env_setting = self.data['virtual_env']

        if virtual_env_setting['create_with_venv']:
            if virtual_env_setting['install_virtual_env_pack']:
                os.system('pip install --upgrade virtualenv')

    def create_paths(self):
        paths = ('', '/main', '/auth', '/templates')
        for path in paths:

            try:
                os.mkdir(self.curent_path + '/{}'.format(self.data['project_name']) + path)
            except OSError:
                print('Create of the directory {} failed'.format(path))
            else:
                print('Succesfully created directory {}'.format(path))
                

    def create_main(self):
        with open('main_.py' , 'w+') as f:
            f.write(
'''
import os 
from {} import create_app

env = os.environ.get('WEBAPP_ENV' , 'dev')
app = create_app('config.%sConfig' %env.capitalize())

if __name__ == "__main__":
    app.run()
'''.format(data['project_name'])
            )

        with open('manage.py' , 'w+') as f:
            f.write(
'''
import os 
from {} import db , migrate , create_app
from {}.auth.models import User

env = os.environ.get('WEBAPP_ENV' , 'dev')
app = create_app('config.%sConfig' %env.capitalize())

@app.shell_context_processor
def make_shell_context():
    return dict(app=app , db=db , User=User)
'''.format(self.data['project_name'] , self.data['project_name'])
            )
        with open('requirements.txt' , 'w+') as f:
            f.write(
'''
flask
flask-sqlalchemy
flask-admin
Flask-Login
Flask-WTF
Flask-Migrate
flask-bcrypt
pymysql
'''
            )

        env_list = data['app_settings']
        list_ = ''
        for env in env_list:
            if env['SECRET_KEY'] == "if_you_dont_change_this_will_be_change_for_os.urandom(24)":
                x = os.urandom(24)
            else:
                x = env['SECRET_KEY']
            other_setting_ = ''
            for setting in env['other_setting']:
                other_setting_ = other_setting_ + \
'''    {} = {}
'''.format(setting['name'] , setting['value'])
            
            list_ = list_ + '''
class {}(Config):
    DEBUG = {}
    SECRET_KEY = {}
    SQLALCHEMY_DATABASE_URI = "{}"
'''.format(env['object_name'] ,env['DEBUG'] , x , env['SQLALCHEMY_DATABASE_URI']) + other_setting_

            class_config = '''
class Config(object):  
'''
            if self.recaptcha['integrate_recaptcha'] and self.recaptcha['RECAPTCHA_PUBLIC_KEY'] != False and self.recaptcha['RECAPTCHA_PRIVATE_KEY'] != False:
                class_config = class_config + '''
    RECAPTCHA_PUBLIC_KEY = '{}'
    RECAPTCHA_PRIVATE_KEY = '{}'
'''.format(self.recaptcha['RECAPTCHA_PUBLIC_KEY'] , self.recaptcha['RECAPTCHA_PRIVATE_KEY'])

        if class_config == '''
class Config(object):  
''':
            class_config = class_config + '''    pass\n'''

        with open('config.py' , 'w+') as f:
            f.write(
'''
import os

''' +class_config + list_
            )

    def create_main_modules(self):

        with open('{}/__init__.py'.format(self.data['project_name']) , 'w+') as f:
            f.write('''
from flask import Flask , render_template
from flask_migrate import Migrate 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

def page_not_found(error):
    return render_template('404.html') , 404

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app , db)

    app.register_error_handler(404 , page_not_found)
    register blueprints

    from .auth import create_module as auth_create_module
    from .main import create_module as main_create_module
    auth_create_module(app)
    main_create_module(app)
    
    return app
''')

        with open('{}/main/__init__.py'.format(self.data['project_name']) , 'w+') as f:
            f.write('''
def create_module(app , **kwargs):
    from .controllers import main_blueprint
    app.register_blueprint(main_blueprint)
            ''')

        with open('{}/main/__init__.py'.format(self.data['project_name']) , 'w+') as f:
            f.write('''
from flask import Blueprint , render_template , redirect, url_for

main_blueprint = Blueprint('main' , __name__)

@main_blueprint.route('/test')
def index():
    return 'You are in index'
''')

        with open('{}/auth/__init__.py'.format(self.data['project_name']) , 'w+') as f:
            f.write('''
from flask_login import LoginManager , AnonymousUserMixin
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please login to access this page'
login_manager.login_message_category = 'info'

class Anonymous_Guest(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'

@login_manager.user_loader
def load_user(userid):
    from .models import User
    return User.query.get(int(userid))

def create_module(app , **kwargs):
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from .controllers import auth_blueprint
    app.register_blueprint(auth_blueprint)
            ''')

        with open('{}/auth/controllers.py'.format(data['project_name']) , 'w+') as f:
            f.write('''
from flask_login import login_user , logout_user
from flask import render_template , flash , redirect , url_for , Blueprint
from .forms import Register_Form , Login_Form
from .models import db , User

auth_blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='../templates/auth',
    url_prefix="/auth"
)

@auth_blueprint.route('/login' , methods = ['POST' , 'GET'])
def login():
    form = Login_Form()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        login_user(user , remember=form.remember.data)

        flash("You have been logged in" , category="success")
        return redirect(url_for('main.index'))

    return render_template('login.html' , form = form)

@auth_blueprint.route('/logout' , methods = ['GET' , 'POST'])
def logout():
    logout_user()
    flash("You have been logged out" , category = 'success')
    return redirect(url_for('.login'))

@auth_blueprint.route('/register' , methods = ['GET' , 'POST'])
def register():
    form = Register_Form()
    if form.validate_on_submit():
        new_user = User()
        new_user.username = form.username.data
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash(
            'Your user has been created, please login.',
            category='success'
        )
        return redirect(url_for('.login'))
    
    return render_template('register.html' , form=form)
            ''')

        with open('{}/auth/forms.py'.format(data['project_name']) , 'w+') as f:

            if self.recaptcha['integrate_recaptcha']:
                str_recaptcha_ = 'recaptcha = RecaptchaField()\n'
            else:
                str_recaptcha_ = ''

            f.write('''
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
    
    {}
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
            '''.format(str_recaptcha_))

        with open('{}/auth/models.py'.format(data['project_name']) , 'w+') as f:
            f.write(r'''
from . import bcrypt , AnonymousUserMixin
from .. import db

class User(db.Model):
    id = db.Column(db.Integer() , primary_key=True)
    username = db.Column(db.String(255) , nullable = False , index = True , unique = True)
    password = db.Column(db.String(255))

    def __init__(self, username = ''):
        self.username = username

    def __repr__(self):
        return '< USER: {} > '.format(self.username)

    def set_password(self , password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self , password):
        return bcrypt.check_password_hash(self.password , password) 

    @property
    def is_authenticated(self):
        if isinstance(self , AnonymousUserMixin):
            return False
        else:
            return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return str(self.id)
            ''')

data = create_project(sys.argv[1])
if data:
    x = Main(data)
    x.create_paths()
    x.create_main()
    x.create_main_modules()
# if not data:
#     print('cos poszlo nie tak')

# else:
#     print('done')

# os.system('pip install --upgrade virtualenv')
# print(sys.platform)

# import subprocess
# commands = '''
# C:/Users/Patryk/Desktop/Programing/test_with_create_a_file/env/Scripts/activate
# pip install flask
# '''

# process = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
# out, err = process.communicate(commands.encode('utf-8'))
# print(out)