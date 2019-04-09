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

            if not 'create_user_module' in data or not isinstance(data['create_user_module'] , bool):
                print(missing_arg + 'create_user_module')
                return False

            if not 'create_auth_module' in data or not isinstance(data['create_user_module'] , bool):
                print(missing_arg + 'create_user_module')
                return False
            
            if not 'create_database_table' in data or not isinstance(data['create_user_module'] , bool):
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
                    'create_user_module':True,
                    'create_auth_module':True,
                    'create_database_table':True,
                    'virtual_env':{
                        'create_with_venv':True,
                        'install_virtual_env_pack':True,
                        'venv_name':'env_{}'.format(app_name)
                        }
                    }
            json.dump(data , f)
            print('Config file was create, execute script egain to create a app')
            return False


    
    if os.path.isfile(curent_path + '/config.json'):
        return validate_config_file()
        paths = ('', '/main', '/auth', '/templates')
        for path in paths:

            try:
                os.mkdir(curent_path + '/{}'.format(app_name) + path)
            except OSError:
                print('Create of the directory {} failed'.format(path))
            else:
                print('Succesfully created directory {}'.format(path))

    else:
        return create_config_file()

class Main:

    def __init__(self , data):
        self.data = data

    def virtual_env(self):
        virtual_env_setting = self.data['virtual_env']

        if virtual_env_setting['create_with_venv']:
            if virtual_env_setting['install_virtual_env_pack']:
                os.system('pip install --upgrade virtualenv')

    def create_main(self):
        with open('main_.py' , 'w+') as f:
            f.write(
'''
import os 
from webapp import create_app

env = os.environ.get('WEBAPP_ENV' , 'dev')
app = create_app('config.%sConfig' %env.capitalize())

if __name__ == "__main__":
    app.run()
'''
            )

        with open('manage.py' , 'w+') as f:
            f.write(
'''
import os 
from webapp import db , migrate , create_app
from webapp.auth.models import User

env = os.environ.get('WEBAPP_ENV' , 'dev')
app = create_app('config.%sConfig' %env.capitalize())

@app.shell_context_processor
def make_shell_context():
    return dict(app=app , db=db , User=User)
'''
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
                other_setting_ = other_setting_ + '''
    {} = {}
'''.format(setting['name'] , setting['value'])

            list_ = list_ + '''
class {}(Config):
    DEBUG = {}
    SECRET_KEY = {}
    SQLALCHEMY_DATABASE_URI = "{}"
'''.format(env['object_name'] ,env['DEBUG'] , x , env['SQLALCHEMY_DATABASE_URI']) + other_setting_

        with open('config.py' , 'w+') as f:
            f.write(
'''
import os

class Config(object):
    pass
''' + list_
            )

data = create_project(sys.argv[1])
if data:
    x = Main(data).create_main()
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