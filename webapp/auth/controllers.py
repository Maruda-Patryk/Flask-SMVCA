
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
            