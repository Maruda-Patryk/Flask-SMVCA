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
                    },
                    'auth_setting':{
                        'allow_to_register':True,
                        'roles':True,
                        'login_with_google':{
                            'allow':False,
                            'GOOGLE_CLIENT_ID':None,
                            'GOOGLE_CLIENT_SECRET':None,
                            'scope':['profile' , 'email']
                        }
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
        paths = ('', '/main', '/auth', '/templates' , '/templates/auth')
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
flask-dance
flask-debugtoolbar
Flask-Caching
Flask-Assets
blinker
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
    RECAPTCHA_PUBLIC_KEY = '{0[RECAPTCHA_PUBLIC_KEY]}'
    RECAPTCHA_PRIVATE_KEY = '{0[RECAPTCHA_PRIVATE_KEY]}'
'''.format(self.recaptcha)

            if self.data['auth_setting']['login_with_google']['allow']:
                class_config = class_config + '''
    GOOGLE_CLIENT_ID = '{0[GOOGLE_CLIENT_ID]}'
    GOOGLE_CLIENT_SECRET = '{0[GOOGLE_CLIENT_SECRET]}'
                '''.format(self.data['auth_setting']['login_with_google'])

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
from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()
migrate = Migrate()
debug_toolbar = DebugToolbarExtension()

def page_not_found(error):
    return render_template('404.html') , 404

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app , db)
    debug_toolbar.init_app(app)
    app.register_error_handler(404 , page_not_found)

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

        with open('{}/main/controllers.py'.format(self.data['project_name']) , 'w+') as f:
            f.write('''
from flask import Blueprint , render_template , redirect, url_for

main_blueprint = Blueprint('main' , __name__)

@main_blueprint.route('/test')
def index():
    return 'You are in index'
''')

        with open('{}/auth/__init__.py'.format(self.data['project_name']) , 'w+') as f:
            
            auth_import = ''

            if self.data['auth_setting']['login_with_google']['allow']:
                auth_import = auth_import + '''
from flask_dance.contrib.google import google , make_google_blueprint
from flask_login import login_user
from flask import flash , redirect , url_for , session
'''

            auth_option_create_module = ''
            
            if self.data['auth_setting']['login_with_google']['allow']:

                auth_option_create_module = auth_option_create_module + '''
    google_blueprint = make_google_blueprint(
        client_id = app.config['GOOGLE_CLIENT_ID'],
        client_secret = app.config['GOOGLE_CLIENT_SECRET'],
        scope = {}
    )

    app.register_blueprint(google_blueprint , url_prefix = '/auth/login')
            '''.format(self.data['auth_setting']['login_with_google']['scope'])

            auth_other = ''

            if self.data['auth_setting']['login_with_google']['allow']:
                auth_other = auth_other + '''
from flask_dance.consumer import oauth_authorized

@oauth_authorized.connect
def logged_in(blueprint, token):
    from .models import db, User
    if blueprint.name == 'twitter':
        username = session.get('twitter_oauth_token').get('screen_name')
    elif blueprint.name == 'google':
        resp = google.get('/oauth2/v2/userinfo').json()
        username = resp['email']
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User()
        user.username = username
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash("You have been logged in.", category="success")

    try:
        return redirect(session['next'])
    except:
        return redirect(url_for('main.index'))
'''

            if self.data['auth_setting']['roles']:
                auth_import = auth_import + '''
import functools
from flask_login import current_user
from flask import abort
'''

            has_role_decorator = ''
            if self.data['auth_setting']['roles']:
                has_role_decorator = has_role_decorator + '''
def has_role(name):
    def real_decorator(f):
        def wraps(*args , **kwargs):
            if current_user.has_role(name):
                return f(*args , **kwargs)
            else:
                abort(403)

        return functools.update_wrapper(wraps , f)
    return real_decorator
            '''

            f.write('''
{}
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

{}

def create_module(app , **kwargs):
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from .controllers import auth_blueprint
    app.register_blueprint(auth_blueprint)
    {}

{}
            '''.format(auth_import , has_role_decorator , auth_option_create_module , auth_other))

        if self.data['auth_setting']['allow_to_register']:
            register_template = '''
@auth_blueprint.route('/register' , methods = ['GET' , 'POST'])
def register():
    from .forms import Register_Form
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
'''
        else:
            register_template = ''
             
        with open('{}/auth/controllers.py'.format(data['project_name']) , 'w+') as f:
            f.write('''
from flask_login import login_user , logout_user
from flask import render_template , flash , redirect , url_for , Blueprint , request , session
from .forms import Login_Form
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

    if not form.validate_on_submit():
        if request.args.get('next'):
            session['next'] = request.args.get('next')
        else:
            session['next'] = url_for('main.index')

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        login_user(user , remember=form.remember.data)

        flash("You have been logged in" , category="success")
        return redirect(session['next'])

    return render_template('login.html' , form = form)

@auth_blueprint.route('/logout' , methods = ['GET' , 'POST'])
def logout():
    logout_user()
    flash("You have been logged out" , category = 'success')
    return redirect(url_for('.login'))

{}           '''.format(register_template))

        

        with open('{}/auth/forms.py'.format(data['project_name']) , 'w+') as f:
            if self.recaptcha['integrate_recaptcha']:
                str_recaptcha_ = 'recaptcha = RecaptchaField()\n'
            else:
                str_recaptcha_ = ''
            if self.data['auth_setting']['allow_to_register']:
                register_form = '''
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
            '''.format(str_recaptcha_)
            else:
                register_form =''
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

{}     
'''.format(register_form))

        with open('{}/auth/models.py'.format(data['project_name']) , 'w+') as f:
            
            role_modules = ''
            
            if self.data['auth_setting']['roles']:
                role_modules = role_modules + r'''
roles = db.Table(
    'role_users',
    db.Column('user_id' , db.Integer , db.ForeignKey('user.id')),
    db.Column('role_id' , db.Integer , db.ForeignKey('role.id'))
)

class Role(db.Model):
    id = db.Column(db.Integer() , primary_key = True)
    name = db.Column(db.String(80) , unique = True)
    description = db.Column(db.String(255))

    def __init__(self , name):
        self.name = name

    def __repr__(self):
        return '<Role {}>'.format(self.name)'''
            
            user_module_option = ''
            __init__role = ''
            has_role = ''

            if self.data['auth_setting']['roles']:

                user_module_option = user_module_option + '''
    roles = db.relationship(
        'Role',
        secondary=roles,
        backref = db.backref('users' , lazy='dynamic')
    )'''

                __init__role = __init__role + '''
        default = Role.query.filter_by(name = 'default').one()
        self.roles.append(default)
                '''

                has_role = has_role + '''
    def has_role(self , name):
        for role in self.roles:
            if role.name == name:
                return True
        return False
                '''
            f.write('''
from . import bcrypt , AnonymousUserMixin
from .. import db

'''+role_modules+'''

class User(db.Model):
    id = db.Column(db.Integer() , primary_key=True)
    username = db.Column(db.String(255) , nullable = False , index = True , unique = True)
    password = db.Column(db.String(255))
    '''+user_module_option+'''

    def __init__(self, username = ''):
        '''+__init__role+'''
        self.username = username

    def __repr__(self):
        return '< USER: {} > '.format(self.username)

    def set_password(self , password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self , password):
        return bcrypt.check_password_hash(self.password , password) 

    '''+has_role+'''

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


    def create_templates(self):

        with open('{}/templates/404.html'.format(self.data['project_name']) , 'w+') as f:
            f.write('''
                Error 404
                ''')

        with open('{}/templates/auth/login.html'.format(self.data['project_name']) , 'w+') as f:

            login_with_oauth = ''

            if self.data['auth_setting']['login_with_google']['allow']:
                login_with_oauth = login_with_oauth + '''
                <h2 class="text-center" > Register/Login With Google </h1>
                <a href="{{ url_for('google.login')}}"> Login </a> 
                '''


            f.write('''
{% extends "base.html" %}
{% block title %}Login{% endblock %}
{% block body %}
    <div class="row">
        <div class="col-md-4"></div>
        <div class="col-md-4">
            <h1 class="text-center">Login</h1>
            <form method="POST" action="{{ url_for('.login') }}">
                {{ form.hidden_tag() }}
                <div class="form-group">
                    {{ form.username.label }}
                    {% if form.username.errors %}
                        {% for e in form.username.errors %}
                            <p class="help-block">{{ e }}</p>
                        {% endfor %}
                    {% endif %}
                    {{ form.username(class_='form-control') }}
                </div>
                
                <div class="form-group">
                    {{ form.password.label }}
                    {% if form.password.errors %}
                        {% for e in form.password.errors %}
                            <p class="help-block">{{ e }}</p>
                        {% endfor %}
                    {% endif %}
                    {{ form.password(class_='form-control') }}
                </div>
                <div class="form-group">
                    {{ form.remember.label }}
                    {% if form.remember.errors %}
                        {% for e in form.remember.errors %}
                            <p class="help-block">{{ e }}</p>
                        {% endfor %}
                    {% endif %}
                    {{ form.remember(class_='form-control') }}
                </div>
                <input class="btn btn-primary" type="submit" value="Login">
            </form>
            <hr>
            '''+login_with_oauth+'''
        </div>
        <div class="col-md-4"></div>
    </div>
{% endblock %}
            ''')

        optionals_form = ''

        if self.recaptcha['integrate_recaptcha']:
            optionals_form = optionals_form + r'''
<div class="form-group">
    {{ form.recaptcha.label }}
    {% if form.recaptcha.errors %}
        {% for e in form.recaptcha.errors %}
            <p class="help-block">{{ e }}</p>
        {% endfor %}
    {% endif %}
    {{ form.recaptcha() }}
</div>
            '''


        if self.data['auth_setting']['allow_to_register']:
            with open('{}/templates/auth/register.html'.format(self.data['project_name']) , 'w+') as f:
                f.write('''
{% extends "base.html" %}
{% block title %}Register{% endblock %}
{% block body %}
    <div class="row">
        <div class="col-md-4"></div>
        <div class="col-md-4">
            <h1 class="text-center">Register</h1>
            <form method="POST" action="{{ url_for('.register') }}">
                {{ form.hidden_tag() }}
                <div class="form-group">
                    {{ form.username.label }}
                    {% if form.username.errors %}
                        {% for e in form.username.errors %}
                            <p class="help-block">{{ e }}</p>
                        {% endfor %}
                    {% endif %}
                    {{ form.username(class_='form-control') }}
                </div>
                <div class="form-group">
                    {{ form.password.label }}
                    {% if form.password.errors %}
                        {% for e in form.password.errors %}
                            <p class="help-block">{{ e }}</p>
                        {% endfor %}
                    {% endif %}
                    {{ form.password(class_='form-control') }}
                </div>
                <div class="form-group">
                    {{ form.confirm.label }}
                    {% if form.confirm.errors %}
                        {% for e in form.confirm.errors %}
                            <p class="help-block">{{ e }}</p>
                        {% endfor %}
                    {% endif %}
                    {{ form.confirm(class_='form-control') }}
                </div>'''+ optionals_form + '''
                
                <input class="btn btn-primary" type="submit" value="Register">
            </form>
            <hr>
        </div>
        <div class="col-md-4"></div>
    </div>
{% endblock %}
                ''')

        with open('{}/templates/base.html'.format(self.data['project_name']) , 'w+') as f:
            f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{% block title %}FLASK MVC SIMPLE APP{% endblock %}</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</head>
<body>
    {% block body %}
    {% endblock %}
</body>
</html>
            ''')


data = create_project(sys.argv[1])
if data:
    x = Main(data)
    x.create_paths()
    x.create_main()
    x.create_main_modules()
    x.create_templates()
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