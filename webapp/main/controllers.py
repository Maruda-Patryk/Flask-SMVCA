
from flask import Blueprint , render_template , redirect, url_for

main_blueprint = Blueprint('main' , __name__)

@main_blueprint.route('/test')
def index():
    return 'You are in index'
