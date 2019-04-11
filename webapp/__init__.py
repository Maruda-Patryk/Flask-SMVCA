
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

    from .auth import create_module as auth_create_module
    from .main import create_module as main_create_module
    auth_create_module(app)
    main_create_module(app)
    
    return app
