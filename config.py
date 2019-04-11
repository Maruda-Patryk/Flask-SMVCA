
import os


class Config(object):  

    RECAPTCHA_PUBLIC_KEY = 'asdasdasd'
    RECAPTCHA_PRIVATE_KEY = 'false'

class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = b'\xfa\x91l6\x1e\xe4\xe9\xb2\xcd\xe5\xc0\xe4%\xb0\xe0h\xe7\xa9$\xfb\xd9\x18\xf1c'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:pass@localhost:3306/admin_page"
    PORT = 8080

class ProdConfig(Config):
    DEBUG = False
    SECRET_KEY = b'\x94\x82\x0c\x0b\x95%lw\xa3Y\x9c\xd9D\x1c\xf0\xf3\xf6\xfc\xb4\xfc\n\x1f\xd5\x06'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:pass@localhost:3306/admin_page"
